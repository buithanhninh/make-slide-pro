from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from safe_io import InputSafetyError, JsonInputError, OutputSafetyError, assert_new_output, assert_regular_input_file, load_json_strict, write_json_new


def normalized_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    text = str(value).strip()
    try:
        return format(Decimal(text.replace(",", "")).normalize(), "f")
    except InvalidOperation:
        return " ".join(text.casefold().split())


def normalized_key_part(value: Any) -> str:
    return "" if value is None else " ".join(str(value).strip().casefold().split())


def metric_key(item: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        normalized_key_part(item.get("metric_key")),
        normalized_key_part(item.get("period")),
        normalized_key_part(item.get("unit")),
        normalized_key_part(item.get("denominator")),
        normalized_key_part(item.get("actual_or_forecast", "UNKNOWN")),
    )


def write_payload(payload: dict[str, Any], output: Path) -> None:
    write_json_new(payload, output)
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile canonical content atoms with authoritative data ledger.")
    parser.add_argument("--content-atoms", required=True, type=Path)
    parser.add_argument("--data-ledger", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    findings: list[dict[str, Any]] = []
    unverified_count = 0
    try:
        content_path = assert_regular_input_file(args.content_atoms, label="CONTENT_ATOMS")
        data_path = assert_regular_input_file(args.data_ledger, label="DATA_LEDGER")
        output_path = assert_new_output(args.output, protected_paths=[content_path, data_path])
    except (OSError, OutputSafetyError, InputSafetyError) as error:
        payload = {"schema_version": "1.0", "status": "BLOCKED", "error": str(error), "findings": []}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 2
    try:
        content_payload = load_json_strict(content_path)
        data_payload = load_json_strict(data_path)
        if not isinstance(content_payload, dict):
            raise ValueError("content payload must be an object")
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
        atoms = content_payload.get("atoms", [])
        if not isinstance(data_payload, dict):
            raise ValueError("data ledger payload must be an object")
        if data_payload.get("schema_version") != "1.0":
            findings.append({"severity": "P1", "code": "DATA_LEDGER_SCHEMA_VERSION_INVALID", "detail": str(data_payload.get("schema_version", "missing"))})
        metrics = data_payload.get("metrics", [])
        if not isinstance(atoms, list) or not isinstance(metrics, list):
            raise ValueError("content atoms and data ledger metrics must be arrays")
        if not atoms:
            findings.append({"severity": "P1", "code": "CANONICAL_CONTENT_EMPTY", "detail": "No canonical content atoms supplied."})

        valid_atoms: list[dict[str, Any]] = []
        for index, atom in enumerate(atoms, start=1):
            if not isinstance(atom, dict):
                findings.append({"severity": "P1", "code": "INVALID_CONTENT_ATOM_RECORD", "detail": f"atoms[{index}] is not an object"})
                continue
            valid_atoms.append(atom)
        atoms = valid_atoms
        valid_metrics: list[dict[str, Any]] = []
        for index, metric in enumerate(metrics, start=1):
            if not isinstance(metric, dict):
                findings.append({"severity": "P1", "code": "INVALID_DATA_METRIC_RECORD", "detail": f"metrics[{index}] is not an object"})
                continue
            valid_metrics.append(metric)
        metrics = valid_metrics

        metric_groups: dict[tuple[str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
        for metric in metrics:
            metric_groups[metric_key(metric)].append(metric)
        for key, group in metric_groups.items():
            verified_values = {
                normalized_scalar(metric.get("value"))
                for metric in group
                if metric.get("verification_status") == "VERIFIED"
            }
            if len(verified_values) > 1:
                findings.append({"severity": "P1", "code": "DATA_LEDGER_METRIC_CONFLICT", "detail": "|".join(key), "values": sorted(verified_values)})

        matched = 0
        canonical_metrics = 0
        for atom in atoms:
            if atom.get("confidence") == "CONFLICTED":
                findings.append({"severity": "P1", "code": "CONTENT_ATOM_MARKED_CONFLICTED", "detail": str(atom.get("atom_id"))})
            normalized = atom.get("normalized")
            if atom.get("type") != "METRIC":
                continue
            canonical_metrics += 1
            if not isinstance(normalized, dict) or not normalized.get("metric_key"):
                severity = "P1" if atom.get("priority") in {"P0", "P1"} or atom.get("must_preserve") else "P2"
                findings.append({"severity": severity, "code": "METRIC_NOT_NORMALIZED", "detail": str(atom.get("atom_id"))})
                continue
            key = metric_key(normalized)
            candidates = metric_groups.get(key, [])
            if not candidates:
                severity = "P1" if atom.get("priority") in {"P0", "P1"} or atom.get("must_preserve") else "P2"
                findings.append({"severity": severity, "code": "CANONICAL_METRIC_NOT_IN_DATA_LEDGER", "detail": str(atom.get("atom_id")), "metric_key": key})
                continue
            canonical = normalized_scalar(normalized.get("value"))
            matching_candidates = [item for item in candidates if normalized_scalar(item.get("value")) == canonical]
            candidate_values = {normalized_scalar(item.get("value")) for item in candidates}
            if not matching_candidates:
                findings.append(
                    {
                        "severity": "P1",
                        "code": "CONTENT_METRIC_CONFLICT",
                        "detail": str(atom.get("atom_id")),
                        "metric_key": key,
                        "content_value": canonical,
                        "data_values": sorted(candidate_values),
                        "data_metric_ids": [item.get("metric_id") for item in candidates],
                    }
                )
            elif any(item.get("verification_status") == "VERIFIED" for item in matching_candidates):
                matched += 1
            elif any(item.get("verification_status") == "CONFLICTED" for item in matching_candidates):
                findings.append({"severity": "P1", "code": "MATCHED_METRIC_CONFLICTED", "detail": str(atom.get("atom_id")), "metric_key": key})
            else:
                unverified_count += 1
                findings.append({"severity": "P2", "code": "MATCHED_METRIC_NOT_VERIFIED", "detail": str(atom.get("atom_id")), "metric_key": key})

        claim_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for atom in atoms:
            normalized = atom.get("normalized")
            if isinstance(normalized, dict) and normalized.get("claim_key"):
                claim_groups[str(normalized["claim_key"]).strip().casefold()].append(atom)
        for claim_key, group in claim_groups.items():
            meanings = {normalized_scalar((item.get("normalized") or {}).get("canonical_text", item.get("verbatim", ""))) for item in group}
            if len(meanings) > 1 and any(item.get("priority") in {"P0", "P1"} for item in group):
                findings.append({"severity": "P1", "code": "CONTENT_CLAIM_CONFLICT", "detail": claim_key, "atom_ids": [item.get("atom_id") for item in group]})

        critical = any(item["severity"] in {"P0", "P1"} for item in findings)
        status = "BLOCKED" if critical else ("UNVERIFIED" if unverified_count else "PASS")
        report = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "content_atoms_path": str(content_path),
            "data_ledger_path": str(data_path),
            "canonical_metric_count": canonical_metrics,
            "matched_metric_count": matched,
            "findings": findings,
        }
        write_payload(report, output_path)
        return 2 if critical else (3 if unverified_count else 0)
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
