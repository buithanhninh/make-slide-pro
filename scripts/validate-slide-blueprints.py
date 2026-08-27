from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_io import InputSafetyError, JsonInputError, OutputSafetyError, assert_new_output, assert_regular_input_file, load_json_strict, write_json_new


EXEMPT_VISUAL_ROLES = {"TITLE", "CLOSING"}


def write_payload(payload: dict[str, Any], output: Path) -> None:
    write_json_new(payload, output)
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate slide blueprints and P0/P1 source coverage.")
    parser.add_argument("--blueprints", required=True, type=Path)
    parser.add_argument("--content-atoms", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    findings: list[dict[str, Any]] = []
    try:
        blueprints_path = assert_regular_input_file(args.blueprints, label="SLIDE_BLUEPRINTS")
        content_path = assert_regular_input_file(args.content_atoms, label="CONTENT_ATOMS")
        output_path = assert_new_output(args.output, protected_paths=[blueprints_path, content_path])
    except (OSError, OutputSafetyError, InputSafetyError) as error:
        payload = {"schema_version": "1.0", "status": "BLOCKED", "error": str(error), "findings": []}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 2
    try:
        blueprint_payload = load_json_strict(blueprints_path)
        content_payload = load_json_strict(content_path)
        if not isinstance(blueprint_payload, dict):
            raise ValueError("blueprint payload must be an object")
        if blueprint_payload.get("schema_version") != "1.0":
            findings.append({"severity": "P1", "code": "BLUEPRINT_SCHEMA_VERSION_INVALID", "detail": str(blueprint_payload.get("schema_version", "missing"))})
        if not str(blueprint_payload.get("deck_id", "")).strip():
            findings.append({"severity": "P1", "code": "BLUEPRINT_DECK_ID_MISSING", "detail": "deck_id is required"})
        slides = blueprint_payload.get("slides")
        if not isinstance(slides, list):
            raise ValueError("slides must be an array")
        if not isinstance(content_payload, dict):
            raise ValueError("content payload must be an object")
        if content_payload.get("schema_version") != "1.0":
            findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_SCHEMA_VERSION_INVALID", "detail": str(content_payload.get("schema_version", "missing"))})
        if content_payload.get("status") != "PASS":
            findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_NOT_PASS", "detail": f"status={content_payload.get('status', 'missing')}"})
        atoms = content_payload.get("atoms", [])
        if not isinstance(atoms, list):
            raise ValueError("atoms must be an array")

        if not slides:
            findings.append({"severity": "P1", "code": "EMPTY_BLUEPRINT", "detail": "No slide blueprints supplied."})
        if not atoms:
            findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_EMPTY", "detail": "No canonical content atoms supplied."})

        valid_atoms: list[dict[str, Any]] = []
        for index, atom in enumerate(atoms, start=1):
            if not isinstance(atom, dict):
                findings.append({"severity": "P1", "code": "INVALID_CONTENT_ATOM_RECORD", "detail": f"atoms[{index}] is not an object"})
                continue
            valid_atoms.append(atom)
        atoms = valid_atoms

        valid_slides: list[dict[str, Any]] = []
        for index, slide in enumerate(slides, start=1):
            if not isinstance(slide, dict):
                findings.append({"severity": "P1", "code": "INVALID_SLIDE_RECORD", "detail": f"slides[{index}] is not an object"})
                continue
            valid_slides.append(slide)
        slides = valid_slides

        atom_map = {str(atom.get("atom_id")): atom for atom in atoms if atom.get("atom_id")}
        for duplicate in [item for item, count in Counter(str(atom.get("atom_id")) for atom in atoms if atom.get("atom_id")).items() if count > 1]:
            findings.append({"severity": "P1", "code": "DUPLICATE_ATOM_ID", "detail": duplicate})
        slide_ids = [str(slide.get("slide_id", "")) for slide in slides]
        slide_numbers = [slide.get("slide_number") for slide in slides]
        for duplicate in [item for item, count in Counter(slide_ids).items() if item and count > 1]:
            findings.append({"severity": "P1", "code": "DUPLICATE_SLIDE_ID", "detail": duplicate})
        for duplicate in [item for item, count in Counter(slide_numbers).items() if item is not None and count > 1]:
            findings.append({"severity": "P1", "code": "DUPLICATE_SLIDE_NUMBER", "detail": str(duplicate)})
        expected_slide_numbers = list(range(1, len(slides) + 1))
        if (
            any(isinstance(item, bool) or not isinstance(item, int) for item in slide_numbers)
            or slide_numbers != expected_slide_numbers
        ):
            findings.append(
                {
                    "severity": "P1",
                    "code": "BLUEPRINT_SLIDE_SEQUENCE_INVALID",
                    "detail": ",".join(str(item) for item in slide_numbers),
                }
            )

        covered_atoms: set[str] = set()
        for slide in slides:
            slide_number = slide.get("slide_number")
            slide_id = str(slide.get("slide_id", ""))
            role = str(slide.get("role", "")).upper()
            if not slide_id or isinstance(slide_number, bool) or not isinstance(slide_number, int) or slide_number < 1:
                findings.append({"severity": "P1", "code": "INVALID_SLIDE_IDENTITY", "detail": f"{slide_id}:{slide_number}"})
            if not str(slide.get("assertion_title", "")).strip():
                findings.append({"severity": "P1", "code": "ASSERTION_TITLE_MISSING", "slide": slide_number, "detail": slide_id})
            if not str(slide.get("primary_claim", "")).strip():
                findings.append({"severity": "P1", "code": "PRIMARY_CLAIM_MISSING", "slide": slide_number, "detail": slide_id})

            source_atoms = slide.get("source_atoms", [])
            if not isinstance(source_atoms, list):
                findings.append({"severity": "P1", "code": "SOURCE_ATOMS_NOT_ARRAY", "slide": slide_number, "detail": slide_id})
                source_atoms = []
            note_atoms = slide.get("speaker_note_atoms", []) if isinstance(slide.get("speaker_note_atoms", []), list) else []
            appendix_atoms = slide.get("appendix_atoms", []) if isinstance(slide.get("appendix_atoms", []), list) else []
            for atom_id in [str(item) for item in source_atoms + note_atoms + appendix_atoms]:
                if atom_id not in atom_map:
                    findings.append({"severity": "P1", "code": "BLUEPRINT_REFERENCES_UNKNOWN_ATOM", "slide": slide_number, "detail": atom_id})
                else:
                    covered_atoms.add(atom_id)

            if role not in EXEMPT_VISUAL_ROLES:
                if not source_atoms:
                    findings.append({"severity": "P1", "code": "CONTENT_SLIDE_HAS_NO_SOURCE_ATOMS", "slide": slide_number, "detail": slide_id})
                anchor = slide.get("visual_anchor")
                anchor_ids = anchor.get("asset_or_object_ids") if isinstance(anchor, dict) else None
                if not isinstance(anchor, dict) or not anchor.get("kind") or not isinstance(anchor_ids, list) or not anchor_ids:
                    findings.append({"severity": "P1", "code": "MEANINGFUL_VISUAL_ANCHOR_MISSING", "slide": slide_number, "detail": slide_id})

        critical_atoms = [atom for atom in atoms if atom.get("priority") in {"P0", "P1"} or atom.get("must_preserve")]
        for atom in critical_atoms:
            atom_id = str(atom.get("atom_id"))
            destination = atom.get("destination")
            if destination == "INTENTIONALLY_OMITTED":
                findings.append({"severity": "P1", "code": "CRITICAL_ATOM_INTENTIONALLY_OMITTED", "detail": atom_id})
            elif atom_id not in covered_atoms:
                findings.append({"severity": "P1", "code": "CRITICAL_ATOM_NOT_COVERED", "detail": atom_id, "destination": destination})

        critical = any(item["severity"] in {"P0", "P1"} for item in findings)
        report = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "BLOCKED" if critical else "PASS",
            "blueprints_path": str(blueprints_path),
            "content_atoms_path": str(content_path),
            "slide_count": len(slides),
            "critical_atom_count": len(critical_atoms),
            "covered_critical_atom_count": sum(1 for atom in critical_atoms if str(atom.get("atom_id")) in covered_atoms),
            "findings": findings,
        }
        write_payload(report, output_path)
        return 2 if critical else 0
    except (OSError, json.JSONDecodeError, ValueError, TypeError, AttributeError, KeyError) as error:
        status = "BLOCKED" if isinstance(error, JsonInputError) else "UNVERIFIED"
        report = {"schema_version": "1.0", "generated_at": datetime.now(timezone.utc).isoformat(), "status": status, "error": str(error), "findings": []}
        try:
            write_payload(report, output_path)
        except (OSError, OutputSafetyError):
            pass
        return 2 if status == "BLOCKED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
