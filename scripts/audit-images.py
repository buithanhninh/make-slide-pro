from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_io import InputSafetyError, JsonInputError, OutputSafetyError, assert_new_output, assert_regular_input_file, load_json_strict, write_json_new

try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    Image = None
    UnidentifiedImageError = OSError


EVIDENTIARY_ROLES = {"EVIDENCE", "PRODUCT", "DATA_VISUAL", "BRAND"}
SHA256_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")
RASTER_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
RASTER_KINDS = {"IMAGE", "LOGO", "PHOTO", "RASTER"}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_payload(payload: dict[str, Any], output: Path) -> None:
    write_json_new(payload, output)
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def is_positive_finite_number(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(float(value)) and float(value) > 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit image provenance, evidence safety, aspect ratio, and effective PPI.")
    parser.add_argument("--assets", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--minimum-ppi", type=float, default=150.0)
    parser.add_argument("--hero-minimum-ppi", type=float, default=180.0)
    args = parser.parse_args()
    findings: list[dict[str, Any]] = []
    audited: list[dict[str, Any]] = []
    pixel_inspection_unverified = False
    try:
        assets_path = assert_regular_input_file(args.assets, label="ASSET_MANIFEST")
        output_path = assert_new_output(args.output, protected_paths=[assets_path])
    except (OSError, OutputSafetyError, InputSafetyError) as error:
        payload = {"schema_version": "1.0", "status": "BLOCKED", "error": str(error), "findings": []}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 2
    if (
        not math.isfinite(args.minimum_ppi)
        or not math.isfinite(args.hero_minimum_ppi)
        or args.minimum_ppi <= 0
        or args.hero_minimum_ppi <= 0
        or args.hero_minimum_ppi < args.minimum_ppi
    ):
        report = {"schema_version": "1.0", "generated_at": datetime.now(timezone.utc).isoformat(), "status": "BLOCKED", "error": "INVALID_PPI_THRESHOLD", "findings": []}
        write_payload(report, output_path)
        return 2
    try:
        manifest = load_json_strict(assets_path)
        if isinstance(manifest, list):
            assets = manifest
        elif isinstance(manifest, dict):
            assets = manifest.get("assets", [])
        else:
            raise ValueError("asset manifest must be an object or array")
        if not isinstance(assets, list):
            raise ValueError("assets must be an array")
        ids: set[str] = set()
        for asset in assets:
            if not isinstance(asset, dict):
                findings.append({"severity": "P1", "code": "VISUAL_ASSET_RECORD_INVALID", "detail": str(asset)[:200]})
                continue
            asset_id = str(asset.get("asset_id", "")).strip()
            slide = asset.get("slide_number")
            role = str(asset.get("role", "")).upper()
            source_type = str(asset.get("source_type", "UNKNOWN")).upper()
            kind = str(asset.get("kind", "IMAGE")).upper()
            evidence_use = bool(asset.get("used_as_evidence")) or role in EVIDENTIARY_ROLES
            if not asset_id:
                findings.append({"severity": "P1", "code": "VISUAL_ASSET_ID_MISSING", "slide": slide, "detail": str(asset)[:200]})
            elif asset_id in ids:
                findings.append({"severity": "P1", "code": "DUPLICATE_VISUAL_ASSET_ID", "slide": slide, "detail": asset_id})
            ids.add(asset_id)

            if source_type == "AI_GENERATED" and evidence_use:
                findings.append({"severity": "P0", "code": "GENERATED_ASSET_USED_AS_EVIDENCE", "slide": slide, "object": asset_id, "detail": f"role={role}"})
            if source_type == "UNKNOWN" and evidence_use:
                findings.append({"severity": "P1", "code": "EVIDENCE_ASSET_PROVENANCE_UNKNOWN", "slide": slide, "object": asset_id, "detail": f"kind={kind}"})
            provenance = asset.get("provenance")
            if evidence_use and (not isinstance(provenance, dict) or not provenance.get("kind")):
                findings.append({"severity": "P1", "code": "EVIDENCE_ASSET_PROVENANCE_INCOMPLETE", "slide": slide, "object": asset_id, "detail": "provenance.kind missing"})
            if kind == "LOGO" and source_type not in {"USER_PROVIDED", "OFFICIAL"}:
                findings.append({"severity": "P1", "code": "UNOFFICIAL_LOGO_ASSET", "slide": slide, "object": asset_id, "detail": source_type})

            usage = asset.get("usage", {}) if isinstance(asset.get("usage", {}), dict) else {}
            declared_pixel_width = asset.get("pixel_width")
            declared_pixel_height = asset.get("pixel_height")
            display_width = usage.get("display_width_inches")
            display_height = usage.get("display_height_inches")
            actual_pixel_width = None
            actual_pixel_height = None
            effective_ppi = None
            file_path = asset.get("path")
            actual_hash = None
            local_path = None
            raster_asset = kind in RASTER_KINDS
            if file_path:
                try:
                    local_path = assert_regular_input_file(Path(str(file_path)), label="VISUAL_ASSET")
                except (InputSafetyError, OSError) as error:
                    findings.append({"severity": "P1", "code": "VISUAL_ASSET_PATH_UNSAFE", "slide": slide, "object": asset_id, "detail": str(error)})
                if local_path is not None:
                    raster_asset = raster_asset or local_path.suffix.lower() in RASTER_EXTENSIONS
                    actual_hash = file_sha256(local_path)
                    expected_hash = str(asset.get("sha256") or "").strip()
                    if expected_hash and not SHA256_PATTERN.fullmatch(expected_hash):
                        findings.append({"severity": "P1", "code": "VISUAL_ASSET_HASH_INVALID", "slide": slide, "object": asset_id, "detail": expected_hash})
                    elif expected_hash and expected_hash.casefold() != actual_hash:
                        findings.append({"severity": "P1", "code": "VISUAL_ASSET_HASH_MISMATCH", "slide": slide, "object": asset_id, "detail": f"expected={expected_hash.lower()} actual={actual_hash}"})
                    elif evidence_use and not expected_hash:
                        findings.append({"severity": "P1", "code": "EVIDENCE_ASSET_HASH_MISSING", "slide": slide, "object": asset_id, "detail": str(file_path)})

                    if raster_asset:
                        if Image is None:
                            pixel_inspection_unverified = True
                            findings.append({"severity": "INFO", "code": "IMAGE_PIXEL_INSPECTION_UNAVAILABLE", "slide": slide, "object": asset_id, "detail": "Pillow is not installed"})
                        else:
                            try:
                                with Image.open(local_path) as image:
                                    actual_pixel_width, actual_pixel_height = image.size
                                    image.verify()
                            except (OSError, ValueError, UnidentifiedImageError) as error:
                                findings.append({"severity": "P1", "code": "IMAGE_PIXEL_DIMENSIONS_UNREADABLE", "slide": slide, "object": asset_id, "detail": str(error)})

            declared_dimensions_valid = all(is_positive_finite_number(value) for value in [declared_pixel_width, declared_pixel_height])
            actual_dimensions_valid = all(is_positive_finite_number(value) for value in [actual_pixel_width, actual_pixel_height])
            if actual_dimensions_valid and declared_dimensions_valid and (
                int(actual_pixel_width) != int(declared_pixel_width)
                or int(actual_pixel_height) != int(declared_pixel_height)
            ):
                findings.append({
                    "severity": "P1",
                    "code": "IMAGE_PIXEL_DIMENSIONS_MISMATCH",
                    "slide": slide,
                    "object": asset_id,
                    "detail": f"declared={int(declared_pixel_width)}x{int(declared_pixel_height)} actual={int(actual_pixel_width)}x{int(actual_pixel_height)}",
                })

            trusted_pixel_width = actual_pixel_width if actual_dimensions_valid else None
            trusted_pixel_height = actual_pixel_height if actual_dimensions_valid else None
            if raster_asset and local_path is None and Image is not None:
                findings.append({"severity": "P1", "code": "IMAGE_PIXEL_DIMENSIONS_UNVERIFIED", "slide": slide, "object": asset_id, "detail": "raster file unavailable for inspection"})
            if all(is_positive_finite_number(value) for value in [trusted_pixel_width, trusted_pixel_height, display_width, display_height]):
                effective_ppi = min(float(trusted_pixel_width) / float(display_width), float(trusted_pixel_height) / float(display_height))
                hero = bool(usage.get("hero")) or role in EVIDENTIARY_ROLES
                minimum = args.hero_minimum_ppi if hero else args.minimum_ppi
                if effective_ppi < minimum:
                    findings.append({"severity": "P1", "code": "IMAGE_EFFECTIVE_PPI_TOO_LOW", "slide": slide, "object": asset_id, "detail": f"ppi={effective_ppi:.1f} minimum={minimum:.1f}"})
                display_ratio = float(display_width) / float(display_height)
                source_ratio = float(trusted_pixel_width) / float(trusted_pixel_height)
                crop = str(usage.get("crop", "cover")).lower()
                if crop == "stretch" and abs(display_ratio / source_ratio - 1.0) > 0.02:
                    findings.append({"severity": "P1", "code": "IMAGE_ASPECT_RATIO_DISTORTED", "slide": slide, "object": asset_id, "detail": f"source={source_ratio:.4f} display={display_ratio:.4f}"})
            elif kind not in {"ICON", "DATA_VISUAL"} and not pixel_inspection_unverified:
                findings.append({"severity": "P1", "code": "IMAGE_DIMENSIONS_UNVERIFIED", "slide": slide, "object": asset_id, "detail": "verified pixel or display dimensions missing"})
            if role != "DECORATIVE" and kind not in {"ICON", "LOGO"} and not str(usage.get("alt_text", "")).strip():
                findings.append({"severity": "P2", "code": "ALT_TEXT_MISSING", "slide": slide, "object": asset_id, "detail": kind})
            if kind == "DATA_VISUAL" and not bool(asset.get("editable", False)):
                findings.append({"severity": "P1", "code": "FLATTENED_DATA_VISUAL", "slide": slide, "object": asset_id, "detail": "Data visual must remain editable"})

            audited.append({
                "asset_id": asset_id,
                "slide": slide,
                "declared_pixel_width": declared_pixel_width,
                "declared_pixel_height": declared_pixel_height,
                "actual_pixel_width": actual_pixel_width,
                "actual_pixel_height": actual_pixel_height,
                "effective_ppi": None if effective_ppi is None else round(effective_ppi, 2),
                "evidence_use": evidence_use,
                "sha256": actual_hash,
            })

        critical = any(item["severity"] in {"P0", "P1"} for item in findings)
        status = "BLOCKED" if critical else "UNVERIFIED" if pixel_inspection_unverified else "PASS"
        report = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "assets_path": str(assets_path),
            "asset_count": len(assets),
            "minimum_ppi": args.minimum_ppi,
            "hero_minimum_ppi": args.hero_minimum_ppi,
            "findings": findings,
            "assets": audited,
        }
        write_payload(report, output_path)
        return 2 if critical else 3 if pixel_inspection_unverified else 0
    except (OSError, json.JSONDecodeError, ValueError, TypeError, AttributeError) as error:
        status = "BLOCKED" if isinstance(error, JsonInputError) else "UNVERIFIED"
        report = {"schema_version": "1.0", "generated_at": datetime.now(timezone.utc).isoformat(), "status": status, "error": str(error), "findings": []}
        write_payload(report, output_path)
        return 2 if status == "BLOCKED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
