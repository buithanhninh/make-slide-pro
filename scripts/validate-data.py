from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from safe_io import InputSafetyError, JsonInputError, OutputSafetyError, assert_new_output, assert_regular_input_file, load_json_strict, write_json_new


def canonical_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            return "NON_FINITE"
        return format(Decimal(str(value)).normalize(), "f")
    text = str(value).strip()
    try:
        return format(Decimal(text.replace(",", "")).normalize(), "f")
    except InvalidOperation:
        return " ".join(text.casefold().split())


def canonical_key_part(value: Any) -> str:
    return "" if value is None else " ".join(str(value).strip().casefold().split())


def write_payload(payload: dict[str, Any], output: Path) -> None:
    write_json_new(payload, output)
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Make Slide Pro data ledger consistency.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--content-atoms", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    findings: list[dict[str, Any]] = []
    content_path: Path | None = None
    try:
        input_path = assert_regular_input_file(args.input, label="DATA_LEDGER")
        protected_paths = [input_path]
        if args.content_atoms:
            content_path = assert_regular_input_file(args.content_atoms, label="CONTENT_ATOMS")
            protected_paths.append(content_path)
        output_path = assert_new_output(args.output, protected_paths=protected_paths)
    except (OSError, OutputSafetyError, InputSafetyError) as error:
        payload = {"schema_version": "1.0", "status": "BLOCKED", "error": str(error), "findings": []}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 2
    try:
        payload = load_json_strict(input_path)
        if not isinstance(payload, dict):
            raise ValueError("data ledger payload must be an object")
        if payload.get("schema_version") != "1.0":
            findings.append({"severity": "P1", "code": "DATA_LEDGER_SCHEMA_VERSION_INVALID", "detail": str(payload.get("schema_version", "missing"))})
        if "metrics" not in payload:
            findings.append({"severity": "P1", "code": "DATA_LEDGER_METRICS_MISSING", "detail": "metrics property is required"})
        metrics = payload.get("metrics", [])
        if not isinstance(metrics, list):
            raise ValueError("metrics must be an array")

        ids: set[str] = set()
        groups: dict[tuple[str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
        unverified_count = 0
        expected_metric_count: int | None = None
        if content_path is not None:
            content_payload = load_json_strict(content_path)
            if not isinstance(content_payload, dict):
                findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_INVALID", "detail": "content payload must be an object"})
                content_atoms: list[Any] = []
            else:
                if content_payload.get("schema_version") != "1.0":
                    findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_SCHEMA_VERSION_INVALID", "detail": str(content_payload.get("schema_version", "missing"))})
                content_status = content_payload.get("status")
                if content_status not in {"PASS", "UNVERIFIED", "BLOCKED"}:
                    findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_STATUS_INVALID", "detail": str(content_status or "missing")})
                elif content_status == "BLOCKED":
                    findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_NOT_PASS", "detail": "status=BLOCKED"})
                elif content_status != "PASS":
                    unverified_count += 1
                    findings.append({"severity": "P2", "code": "CANONICAL_CONTENT_NOT_PASS", "detail": f"status={content_status}"})
                content_atoms = content_payload.get("atoms", [])
                if not isinstance(content_atoms, list):
                    findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_ATOMS_INVALID", "detail": "atoms must be an array"})
                    content_atoms = []
            if not content_atoms:
                findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_EMPTY", "detail": "No canonical content atoms supplied."})
            invalid_atoms = [index for index, atom in enumerate(content_atoms, start=1) if not isinstance(atom, dict)]
            for index in invalid_atoms:
                findings.append({"severity": "P1", "code": "INVALID_CONTENT_ATOM_RECORD", "detail": f"atoms[{index}] is not an object"})
            expected_metric_count = sum(1 for atom in content_atoms if isinstance(atom, dict) and atom.get("type") == "METRIC")

        if not metrics:
            if content_path is None:
                unverified_count += 1
                findings.append({"severity": "P2", "code": "EMPTY_DATA_LEDGER_CONTEXT_REQUIRED", "detail": "Supply --content-atoms to prove that no metrics are expected."})
            elif expected_metric_count and expected_metric_count > 0:
                findings.append({"severity": "P1", "code": "EXPECTED_METRICS_MISSING", "detail": f"canonical_metric_count={expected_metric_count}"})

        for index, metric in enumerate(metrics, start=1):
            if not isinstance(metric, dict):
                findings.append({"severity": "P1", "code": "INVALID_DATA_METRIC_RECORD", "detail": f"metrics[{index}] is not an object"})
                continue
            metric_id = str(metric.get("metric_id", "")).strip()
            if not metric_id:
                findings.append({"severity": "P1", "code": "METRIC_ID_MISSING", "detail": f"metrics[{index}]"})
            elif metric_id in ids:
                findings.append({"severity": "P1", "code": "DUPLICATE_METRIC_ID", "detail": metric_id})
            if metric_id:
                ids.add(metric_id)

            required = ["metric_key", "value", "unit", "period", "denominator", "source_id", "locator", "verification_status", "actual_or_forecast"]
            for field in required:
                if field not in metric:
                    findings.append({"severity": "P1", "code": "METRIC_FIELD_MISSING", "detail": f"{metric_id or index}:{field}"})

            for field in ["metric_key", "unit", "period", "source_id"]:
                value = metric.get(field)
                if not isinstance(value, str) or not value.strip():
                    findings.append({"severity": "P1", "code": "METRIC_FIELD_INVALID", "detail": f"{metric_id or index}:{field}"})
            denominator = metric.get("denominator")
            if denominator is not None and (not isinstance(denominator, str) or not denominator.strip()):
                findings.append({"severity": "P1", "code": "METRIC_FIELD_INVALID", "detail": f"{metric_id or index}:denominator"})
            locator = metric.get("locator")
            if not isinstance(locator, dict) or not locator:
                findings.append({"severity": "P1", "code": "METRIC_FIELD_INVALID", "detail": f"{metric_id or index}:locator"})

            verification_raw = metric.get("verification_status")
            verification = str(verification_raw or "")
            if verification not in {"VERIFIED", "REVIEW_REQUIRED", "UNVERIFIED", "CONFLICTED"}:
                findings.append({"severity": "P1", "code": "METRIC_FIELD_INVALID", "detail": f"{metric_id or index}:verification_status"})
            if verification == "CONFLICTED":
                findings.append({"severity": "P1", "code": "METRIC_MARKED_CONFLICTED", "detail": metric_id})
            elif verification in {"REVIEW_REQUIRED", "UNVERIFIED"}:
                unverified_count += 1
                findings.append({"severity": "P2", "code": "METRIC_NOT_VERIFIED", "detail": f"{metric_id}:{verification}"})

            value = metric.get("value")
            if isinstance(value, bool) or not isinstance(value, (int, float, str)) or (isinstance(value, str) and not value.strip()):
                findings.append({"severity": "P1", "code": "METRIC_FIELD_INVALID", "detail": f"{metric_id or index}:value"})
            elif isinstance(value, float) and not math.isfinite(value):
                findings.append({"severity": "P1", "code": "NON_FINITE_METRIC_VALUE", "detail": metric_id})
            actual_or_forecast = metric.get("actual_or_forecast")
            if actual_or_forecast is None:
                findings.append({"severity": "P1", "code": "METRIC_ACTUAL_OR_FORECAST_MISSING", "detail": metric_id or str(index)})
            elif actual_or_forecast not in {"ACTUAL", "FORECAST", "TARGET", "ASSUMPTION", "UNKNOWN"}:
                findings.append({"severity": "P1", "code": "METRIC_FIELD_INVALID", "detail": f"{metric_id or index}:actual_or_forecast"})
            if metric.get("formula") and not metric.get("formula_inputs"):
                findings.append({"severity": "P2", "code": "FORMULA_NOT_REPRODUCIBLE", "detail": metric_id})

            key = (
                canonical_key_part(metric.get("metric_key")),
                canonical_key_part(metric.get("period")),
                canonical_key_part(metric.get("unit")),
                canonical_key_part(metric.get("denominator")),
                canonical_key_part(metric.get("actual_or_forecast", "UNKNOWN")),
            )
            groups[key].append(metric)

        for key, group in groups.items():
            values = {canonical_value(item.get("value")) for item in group}
            if len(values) <= 1:
                continue
            verified = [item for item in group if item.get("verification_status") == "VERIFIED"]
            findings.append(
                {
                    "severity": "P1" if len(verified) >= 2 else "P2",
                    "code": "DUPLICATE_METRIC_VALUE_CONFLICT",
                    "detail": "|".join(key),
                    "metric_ids": [item.get("metric_id") for item in group],
                    "values": sorted(values),
                }
            )

        critical = any(item["severity"] in {"P0", "P1"} for item in findings)
        status = "BLOCKED" if critical else ("UNVERIFIED" if unverified_count else "PASS")
        report = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "input_path": str(input_path),
            "content_atoms_path": str(content_path) if content_path else None,
            "metric_count": len(metrics),
            "expected_metric_count": expected_metric_count,
            "group_count": len(groups),
            "findings": findings,
        }
        write_payload(report, output_path)
        return 2 if status == "BLOCKED" else (3 if status == "UNVERIFIED" else 0)
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
