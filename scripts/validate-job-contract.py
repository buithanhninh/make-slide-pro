from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_io import (
    InputSafetyError,
    JsonInputError,
    OutputSafetyError,
    assert_new_output,
    assert_regular_input_file,
    assert_safe_input_directory,
    load_json_strict,
    write_json_new,
)


def write_payload(payload: dict[str, Any], output: Path) -> None:
    write_json_new(payload, output)
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def validate_schema(instance: Any, schema_path: Path, schemas_dir: Path) -> list[dict[str, Any]]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource
    except ImportError as error:
        raise RuntimeError(f"JSON_SCHEMA_RUNTIME_MISSING: {error}") from error

    schema = load_json_strict(schema_path)
    registry = Registry()
    for local_schema_path in sorted(schemas_dir.glob("*.json")):
        local_schema_path = assert_regular_input_file(local_schema_path, label="SCHEMA")
        local_schema = load_json_strict(local_schema_path)
        resource = Resource.from_contents(local_schema)
        schema_id = local_schema.get("$id")
        if schema_id:
            registry = registry.with_resource(schema_id, resource)
        registry = registry.with_resource(local_schema_path.as_uri(), resource)
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda item: tuple(str(part) for part in item.absolute_path))
    return [
        {
            "severity": "P1",
            "code": "JOB_CONTRACT_SCHEMA_INVALID",
            "detail": error.message,
            "instance_path": "/" + "/".join(str(part) for part in error.absolute_path),
            "schema_path": "/" + "/".join(str(part) for part in error.absolute_schema_path),
        }
        for error in errors[:250]
    ]


def semantic_findings(contract: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    policy = contract.get("slide_count_policy")
    if policy == "TARGET_RANGE":
        target_range = contract.get("target_slide_range")
        if isinstance(target_range, list) and len(target_range) == 2:
            if target_range[0] > target_range[1]:
                findings.append(
                    {
                        "severity": "P1",
                        "code": "TARGET_SLIDE_RANGE_REVERSED",
                        "detail": f"lower={target_range[0]} upper={target_range[1]}",
                    }
                )
    if contract.get("preservation_mode") == "LOCKED":
        budget = contract.get("content_change_budget")
        if isinstance(budget, dict):
            if budget.get("max_semantic_change") not in {"NONE", "EQUIVALENT_ONLY"}:
                findings.append(
                    {
                        "severity": "P1",
                        "code": "LOCKED_PRESERVATION_BUDGET_TOO_WIDE",
                        "detail": str(budget.get("max_semantic_change")),
                    }
                )
            if budget.get("allow_derivation") is True:
                findings.append(
                    {
                        "severity": "P1",
                        "code": "LOCKED_PRESERVATION_ALLOWS_DERIVATION",
                        "detail": "content_change_budget.allow_derivation must be false",
                    }
                )
            if budget.get("allow_reorder") is True:
                findings.append(
                    {
                        "severity": "P1",
                        "code": "LOCKED_PRESERVATION_ALLOWS_REORDER",
                        "detail": "content_change_budget.allow_reorder must be false",
                    }
                )
            if budget.get("omission_policy") != "NONE":
                findings.append(
                    {
                        "severity": "P1",
                        "code": "LOCKED_PRESERVATION_ALLOWS_OMISSION",
                        "detail": str(budget.get("omission_policy")),
                    }
                )
        if contract.get("sequence_change_allowed") is True:
            findings.append(
                {
                    "severity": "P1",
                    "code": "LOCKED_PRESERVATION_ALLOWS_SEQUENCE_CHANGE",
                    "detail": "sequence_change_allowed must be false",
                }
            )
    if contract.get("primary_operation") == "MOTION" and contract.get("motion_level") == "NONE":
        findings.append(
            {
                "severity": "P1",
                "code": "MOTION_OPERATION_WITHOUT_MOTION",
                "detail": "motion_level must not be NONE for primary operation MOTION",
            }
        )
    output_contract = contract.get("output_contract")
    if isinstance(output_contract, dict) and output_contract.get("format") == "PDF" and output_contract.get("editable") is True:
        findings.append(
            {
                "severity": "P1",
                "code": "PDF_OUTPUT_CANNOT_BE_EDITABLE",
                "detail": "output_contract.editable must be false for PDF",
            }
        )
    if contract.get("certification_mode") == "CERTIFIED":
        if isinstance(output_contract, dict):
            if output_contract.get("versioned") is not True:
                findings.append(
                    {
                        "severity": "P1",
                        "code": "CERTIFIED_OUTPUT_NOT_VERSIONED",
                        "detail": "output_contract.versioned must be true",
                    }
                )
            if output_contract.get("evidence_package") != "FULL":
                findings.append(
                    {
                        "severity": "P1",
                        "code": "CERTIFIED_EVIDENCE_PACKAGE_NOT_FULL",
                        "detail": str(output_contract.get("evidence_package")),
                    }
                )
            if output_contract.get("source_notes") != "REQUIRED":
                findings.append(
                    {
                        "severity": "P1",
                        "code": "CERTIFIED_SOURCE_NOTES_NOT_REQUIRED",
                        "detail": str(output_contract.get("source_notes")),
                    }
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Make Slide Pro Job Contract.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--schemas-dir", type=Path, default=Path(__file__).resolve().parents[1] / "schemas")
    args = parser.parse_args()
    generated_at = datetime.now(timezone.utc).isoformat()
    try:
        input_path = assert_regular_input_file(args.input, label="JOB_CONTRACT")
        output_path = assert_new_output(args.output, protected_paths=[input_path])
        schemas_dir = assert_safe_input_directory(args.schemas_dir, label="SCHEMAS_DIRECTORY")
        schema_path = assert_regular_input_file(schemas_dir / "job-contract.schema.json", label="JOB_CONTRACT_SCHEMA")
        contract = load_json_strict(input_path)
        if not isinstance(contract, dict):
            raise ValueError("job contract payload must be an object")
        findings = validate_schema(contract, schema_path, schemas_dir)
        findings.extend(semantic_findings(contract))
        report = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": "BLOCKED" if findings else "PASS",
            "input_path": str(input_path),
            "schema_path": str(schema_path),
            "findings": findings,
        }
        write_payload(report, output_path)
        return 2 if findings else 0
    except (OSError, JsonInputError, InputSafetyError, OutputSafetyError, ValueError, RuntimeError) as error:
        status = "UNVERIFIED" if isinstance(error, RuntimeError) and "JSON_SCHEMA_RUNTIME_MISSING" in str(error) else "BLOCKED"
        report = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": status,
            "error": str(error),
            "findings": [],
        }
        try:
            if "output_path" in locals():
                write_payload(report, output_path)
            else:
                print(json.dumps(report, ensure_ascii=True, indent=2))
        except (OSError, OutputSafetyError):
            print(json.dumps(report, ensure_ascii=True, indent=2))
        return 3 if status == "UNVERIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
