from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_io import InputSafetyError, JsonInputError, OutputSafetyError, assert_new_output, assert_regular_input_file, load_json_strict, write_json_new


HEX_PATTERN = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGB_PATTERN = re.compile(r"^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$", re.IGNORECASE)


def parse_color(value: Any) -> tuple[int, int, int] | None:
    text = str(value or "").strip()
    match = HEX_PATTERN.match(text)
    if match:
        digits = match.group(1)
        if len(digits) == 3:
            digits = "".join(character * 2 for character in digits)
        return tuple(int(digits[index : index + 2], 16) for index in (0, 2, 4))
    match = RGB_PATTERN.match(text)
    if match:
        values = tuple(int(part) for part in match.groups())
        if all(0 <= part <= 255 for part in values):
            return values
    return None


def channel_luminance(channel: int) -> float:
    normalized = channel / 255.0
    return normalized / 12.92 if normalized <= 0.04045 else ((normalized + 0.055) / 1.055) ** 2.4


def contrast_ratio(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
    first_luminance = 0.2126 * channel_luminance(first[0]) + 0.7152 * channel_luminance(first[1]) + 0.0722 * channel_luminance(first[2])
    second_luminance = 0.2126 * channel_luminance(second[0]) + 0.7152 * channel_luminance(second[1]) + 0.0722 * channel_luminance(second[2])
    lighter = max(first_luminance, second_luminance)
    darker = min(first_luminance, second_luminance)
    return (lighter + 0.05) / (darker + 0.05)


def write_payload(payload: dict[str, Any], output: Path) -> None:
    write_json_new(payload, output)
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit text and non-text contrast from an authoring manifest.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    findings: list[dict[str, Any]] = []
    audited: list[dict[str, Any]] = []
    try:
        manifest_path = assert_regular_input_file(args.manifest, label="CONTRAST_MANIFEST")
        output_path = assert_new_output(args.output, protected_paths=[manifest_path])
    except (OSError, OutputSafetyError, InputSafetyError) as error:
        payload = {"schema_version": "1.0", "status": "BLOCKED", "error": str(error), "findings": []}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 2
    try:
        manifest = load_json_strict(manifest_path)
        if isinstance(manifest, list):
            items = manifest
        elif isinstance(manifest, dict):
            items = manifest.get("items", [])
            if manifest.get("schema_version") != "1.0":
                findings.append({"severity": "P1", "code": "CONTRAST_MANIFEST_SCHEMA_VERSION_INVALID", "detail": str(manifest.get("schema_version", "missing"))})
        else:
            raise ValueError("contrast manifest must be an object or array")
        if not isinstance(items, list):
            raise ValueError("items must be an array")
        if not items:
            findings.append({"severity": "P1", "code": "CONTRAST_MANIFEST_EMPTY", "detail": "No contrast records supplied."})
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                findings.append({"severity": "P1", "code": "CONTRAST_RECORD_INVALID", "detail": f"items[{index}] is not an object"})
                continue
            item_id = str(item.get("object_id", item.get("name", "unknown")))
            slide = item.get("slide_number")
            foreground = parse_color(item.get("foreground"))
            background = parse_color(item.get("background"))
            if foreground is None or background is None:
                findings.append({"severity": "P1", "code": "CONTRAST_NOT_MEASURABLE", "slide": slide, "object": item_id, "detail": f"foreground={item.get('foreground')} background={item.get('background')}"})
                continue
            ratio = contrast_ratio(foreground, background)
            kind = str(item.get("kind", "TEXT")).upper()
            if kind == "TEXT":
                raw_font_size = item.get("font_size", 0)
                if isinstance(raw_font_size, bool):
                    raise ValueError(f"font_size must be numeric for {item_id}")
                font_size = float(raw_font_size or 0)
                if not math.isfinite(font_size) or font_size < 0:
                    raise ValueError(f"font_size must be finite and non-negative for {item_id}")
                bold = bool(item.get("bold", False))
                large = bool(item.get("large_text", False)) or font_size >= 18 or (bold and font_size >= 14)
                threshold = 3.0 if large else 4.5
            else:
                threshold = 3.0
            if ratio + 1e-9 < threshold:
                findings.append({"severity": "P1", "code": "CONTRAST_BELOW_THRESHOLD", "slide": slide, "object": item_id, "detail": f"ratio={ratio:.2f} threshold={threshold:.2f}"})
            audited.append({"slide": slide, "object": item_id, "ratio": round(ratio, 3), "threshold": threshold})
        critical = any(item["severity"] in {"P0", "P1"} for item in findings)
        report = {"schema_version": "1.0", "generated_at": datetime.now(timezone.utc).isoformat(), "status": "BLOCKED" if critical else "PASS", "manifest_path": str(manifest_path), "item_count": len(items), "findings": findings, "items": audited}
        write_payload(report, output_path)
        return 2 if critical else 0
    except (OSError, json.JSONDecodeError, ValueError, TypeError, AttributeError, KeyError) as error:
        status = "BLOCKED" if isinstance(error, JsonInputError) else "UNVERIFIED"
        report = {"schema_version": "1.0", "generated_at": datetime.now(timezone.utc).isoformat(), "status": status, "error": str(error), "findings": []}
        write_payload(report, output_path)
        return 2 if status == "BLOCKED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
