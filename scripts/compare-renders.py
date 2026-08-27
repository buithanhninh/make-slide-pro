from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_io import OutputSafetyError, assert_new_output, assert_regular_input_file, assert_safe_input_directory, load_json_strict, normalized_path, write_json_new


def emit(payload: dict[str, Any], output: Path) -> None:
    write_json_new(payload, output)
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two native-render directories pixel by pixel.")
    parser.add_argument("--baseline-dir", required=True, type=Path)
    parser.add_argument("--candidate-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-different-ratio", type=float, default=0.0)
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).isoformat()
    baseline_dir = normalized_path(args.baseline_dir)
    candidate_dir = normalized_path(args.candidate_dir)
    try:
        baseline_dir = assert_safe_input_directory(baseline_dir, label="BASELINE_RENDER_DIRECTORY")
        candidate_dir = assert_safe_input_directory(candidate_dir, label="CANDIDATE_RENDER_DIRECTORY")
        if baseline_dir == candidate_dir:
            raise ValueError("RENDER_DIRECTORIES_MUST_DIFFER")
        output_path = assert_new_output(
            args.output,
            protected_directories=[baseline_dir, candidate_dir],
        )
    except (OSError, OutputSafetyError, ValueError) as error:
        payload = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": "BLOCKED",
            "error": str(error),
            "findings": [],
        }
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 2

    if (
        not math.isfinite(args.max_different_ratio)
        or args.max_different_ratio < 0
        or args.max_different_ratio > 1
    ):
        payload = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": "BLOCKED",
            "error": "INVALID_RENDER_THRESHOLD",
            "findings": [],
        }
        emit(payload, output_path)
        return 2

    try:
        from PIL import Image, ImageChops
    except ImportError:
        payload = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": "UNVERIFIED",
            "error": "Pillow is not installed",
            "slides": [],
        }
        emit(payload, output_path)
        return 3

    try:
        baseline = sorted(baseline_dir.glob("slide-*.png"))
        candidate = sorted(candidate_dir.glob("slide-*.png"))
        findings: list[dict[str, object]] = []
        slides: list[dict[str, object]] = []
        if not baseline or not candidate:
            empty_sets = []
            if not baseline:
                empty_sets.append("baseline")
            if not candidate:
                empty_sets.append("candidate")
            findings.append(
                {
                    "severity": "P1",
                    "code": "RENDER_SET_EMPTY",
                    "detail": f"No slide-*.png renders found in: {', '.join(empty_sets)}.",
                }
            )
        if [path.name for path in baseline] != [path.name for path in candidate]:
            findings.append(
                {
                    "severity": "P1",
                    "code": "RENDER_SET_MISMATCH",
                    "detail": "Baseline and candidate render filenames do not match.",
                }
            )
        for baseline_path in baseline:
            baseline_path = assert_regular_input_file(baseline_path, label="BASELINE_RENDER")
            candidate_path = candidate_dir / baseline_path.name
            if not candidate_path.exists():
                continue
            candidate_path = assert_regular_input_file(candidate_path, label="CANDIDATE_RENDER")
            with Image.open(baseline_path).convert("RGBA") as first, Image.open(candidate_path).convert("RGBA") as second:
                if first.size != second.size:
                    ratio = 1.0
                    findings.append(
                        {
                            "severity": "P1",
                            "code": "RENDER_SIZE_MISMATCH",
                            "detail": f"Render dimensions differ for {baseline_path.name}.",
                            "slide": baseline_path.name,
                            "baseline_size": first.size,
                            "candidate_size": second.size,
                        }
                    )
                else:
                    diff = ImageChops.difference(first, second)
                    bbox = diff.getbbox()
                    if bbox is None:
                        ratio = 0.0
                    else:
                        nonzero = sum(1 for pixel in diff.getdata() if pixel != (0, 0, 0, 0))
                        ratio = nonzero / (first.width * first.height)
                    if ratio > args.max_different_ratio:
                        findings.append(
                            {
                                "severity": "P1",
                                "code": "RENDER_PIXEL_MISMATCH",
                                "detail": f"Pixel difference exceeds threshold for {baseline_path.name}.",
                                "slide": baseline_path.name,
                                "different_ratio": ratio,
                            }
                        )
                slides.append({"slide": baseline_path.name, "different_ratio": ratio})
        status = "BLOCKED" if findings else "PASS"
        payload = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": status,
            "baseline_dir": str(baseline_dir),
            "candidate_dir": str(candidate_dir),
            "threshold": args.max_different_ratio,
            "findings": findings,
            "slides": slides,
        }
        emit(payload, output_path)
        return 2 if findings else 0
    except (OSError, ValueError, RuntimeError, TypeError) as error:
        payload = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": "UNVERIFIED",
            "baseline_dir": str(baseline_dir),
            "candidate_dir": str(candidate_dir),
            "error": str(error),
            "findings": [],
        }
        emit(payload, output_path)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
