from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_io import JsonInputError, OutputSafetyError, assert_new_output, assert_regular_input_file, assert_safe_input_directory, load_json_strict, normalized_path, path_is_within, write_json_new


def write_payload(payload: dict[str, Any], output: Path | None) -> None:
    if output:
        write_json_new(payload, output)
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def resolve_schema_path(schema_arg: str, schemas_dir: Path) -> Path:
    schemas_root = normalized_path(schemas_dir)
    candidate = normalized_path(schema_arg)
    if candidate.is_file():
        if not path_is_within(candidate, schemas_root):
            raise JsonInputError(f"SCHEMA_OUTSIDE_APPROVED_DIRECTORY:{candidate}")
        return assert_regular_input_file(candidate, label="SCHEMA")
    names = [schema_arg]
    if not schema_arg.endswith(".json"):
        names.extend([f"{schema_arg}.json", f"{schema_arg}.schema.json"])
    for name in names:
        path = schemas_dir / name
        if path.is_file():
            return assert_regular_input_file(path, label="SCHEMA")
    raise FileNotFoundError(f"Schema not found: {schema_arg}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Make Slide Pro JSON artifact against a local schema.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--schemas-dir", type=Path, default=Path(__file__).resolve().parents[1] / "schemas")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).isoformat()
    output_path = None
    try:
        input_path = assert_regular_input_file(args.input, label="JSON_INPUT")
        schemas_dir = assert_safe_input_directory(args.schemas_dir, label="SCHEMAS_DIRECTORY")
        schema_path = resolve_schema_path(args.schema, schemas_dir)
        if args.output:
            output_path = assert_new_output(args.output, protected_paths=[input_path, schema_path])
    except (OSError, OutputSafetyError, ValueError) as error:
        payload = {"schema_version": "1.0", "generated_at": generated_at, "status": "BLOCKED", "error": str(error), "findings": []}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 2
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource
    except ImportError as error:
        payload = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": "UNVERIFIED",
            "error": f"JSON_SCHEMA_RUNTIME_MISSING: {error}",
            "findings": [],
        }
        write_payload(payload, args.output)
        return 3

    try:
        instance = load_json_strict(input_path)
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
        findings = []
        for error in errors[:250]:
            findings.append(
                {
                    "severity": "P1",
                    "code": "SCHEMA_VALIDATION_FAILED",
                    "detail": error.message,
                    "instance_path": "/" + "/".join(str(part) for part in error.absolute_path),
                    "schema_path": "/" + "/".join(str(part) for part in error.absolute_schema_path),
                }
            )
        payload = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "status": "BLOCKED" if findings else "PASS",
            "input_path": str(input_path),
            "schema_path": str(schema_path),
            "error_count": len(errors),
            "findings": findings,
        }
        write_payload(payload, output_path)
        return 2 if findings else 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        status = "BLOCKED" if isinstance(error, (JsonInputError, json.JSONDecodeError)) else "UNVERIFIED"
        payload = {"schema_version": "1.0", "generated_at": generated_at, "status": status, "error": str(error), "findings": []}
        try:
            write_payload(payload, output_path)
        except (OSError, OutputSafetyError):
            pass
        return 2 if status == "BLOCKED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
