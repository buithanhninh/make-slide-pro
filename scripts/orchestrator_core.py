from __future__ import annotations

import hashlib
import argparse
import json
import os
import re
import shutil
import stat
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator


ZERO_HASH = "0" * 64
COMPLETED_STATUSES = {"PASS", "SKIPPED"}
REENTRANT_STATUSES = {"STALE"}
TERMINAL_STATUSES = {"PASS", "UNVERIFIED", "BLOCKED", "SKIPPED", "QUARANTINED"}
EVENT_STATUSES = {"STARTED", "PASS", "UNVERIFIED", "BLOCKED", "SKIPPED", "STALE", "QUARANTINED", "RECOVERED"}
PROFILES = {"STATIC_READY_FOR_MOTION", "FINAL_RELEASE_STATIC", "FINAL_RELEASE_MOTION"}
ACTOR_KINDS = {"MANAGER", "SPECIALIST", "VALIDATOR", "CERTIFIER", "SYSTEM", "HUMAN"}
GATE_ID_PATTERN = re.compile(r"^G(?:0|[1-9]|1[0-5])_[A-Z0-9_]+$")
CAPABILITY_TTL_GATES = {"G11_STATIC_PRODUCTION", "G13_NATIVE_MOTION", "G15_STATIC_RELEASE", "G15_MOTION_RELEASE"}
CAPABILITY_UNVERIFIED_CODES = {
    "CAPABILITY_REPORT_MISSING",
    "CAPABILITY_REPORT_UNBOUND",
    "CAPABILITY_TTL_MISSING",
    "CAPABILITY_TTL_EXPIRED",
    "CAPABILITY_STATUS_UNVERIFIED",
    "CAPABILITY_FINGERPRINT_MISSING",
    "CAPABILITY_BINDING_METADATA_MISSING",
    "CAPABILITY_REQUIRED_UNAVAILABLE",
    "CAPABILITY_SCHEMA_RUNTIME_MISSING",
}
CAPABILITY_ALIASES = {
    "artifact-tool": ("artifact_tool",),
    "powerpoint-com": ("powerpoint",),
    "release-certifier": ("python", "jsonschema"),
}
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_SUBMISSION_FIELDS = {
    "schema_version", "run_id", "gate_id", "attempt_id", "producer", "actor_context_id",
    "input_artifacts", "output_artifacts", "dependency_hashes", "tool_fingerprint", "status",
    "findings", "generated_at", "review_context_id", "metadata",
}
ALLOWED_ARTIFACT_FIELDS = {"path", "sha256", "kind", "schema", "immutable"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def event_digest(event: dict[str, Any]) -> str:
    payload = dict(event)
    payload.pop("event_sha256", None)
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _timestamp(value: datetime | None = None) -> str:
    return (value or _now()).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_timestamp(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_PATTERN.fullmatch(value))


def _capability_binding(workspace: Path | str) -> dict[str, Any] | None:
    """Return latest valid G1 binding, preferring journal over mutable manifest cache."""
    paths = workspace_paths(workspace)
    binding: dict[str, Any] | None = None
    if not paths["run_manifest"].exists():
        manifest = None
    else:
        try:
            manifest = _load_json(paths["run_manifest"])
        except RuntimeError:
            manifest = None
    if isinstance(manifest, dict) and isinstance(manifest.get("capability_binding"), dict):
        binding = dict(manifest["capability_binding"])
    if paths["journal"].exists():
        try:
            events = _read_events(paths)
        except RuntimeError:
            return binding
        for event in events:
            if event.get("gate_id") != "G1_CAPABILITY_SECURITY":
                continue
            if event.get("status") in {"STALE", "BLOCKED", "QUARANTINED"}:
                binding = None
                continue
            metadata = event.get("metadata")
            if event.get("status") in {"PASS", "UNVERIFIED"} and isinstance(metadata, dict) and isinstance(metadata.get("capability_binding"), dict):
                binding = dict(metadata["capability_binding"])
    return binding


def _build_capability_binding(workspace: Path | str, report_path: Path | str) -> dict[str, Any]:
    """Validate a G1 report and construct its immutable identity binding."""
    paths = ensure_workspace(workspace)
    candidate, path_findings = _resolve_workspace_artifact(paths["root"], str(report_path), "CAPABILITY_REPORT")
    if candidate is None:
        raise RuntimeError("CAPABILITY_REPORT_UNBINDABLE:" + ";".join(item["code"] for item in path_findings))
    report = _load_json(candidate)
    if not isinstance(report, dict):
        raise RuntimeError("CAPABILITY_REPORT_NOT_OBJECT")
    for field in ("schema_version", "probe_id", "fingerprint", "ttl_expires_at", "status", "capabilities"):
        if field not in report:
            raise RuntimeError(f"CAPABILITY_REPORT_FIELD_MISSING:{field}")
    report_findings = _validate_capability_report(report, None)
    if report_findings:
        raise RuntimeError("CAPABILITY_REPORT_INVALID:" + ";".join(item["code"] for item in report_findings))
    return {
        "path": str(candidate),
        "sha256": _sha256_file(candidate),
        "probe_id": str(report["probe_id"]),
        "fingerprint": str(report["fingerprint"]),
        "ttl_expires_at": str(report["ttl_expires_at"]),
        "status": str(report["status"]),
        "bound_at": _timestamp(),
    }


def bind_capability_report(workspace: Path | str, report_path: Path | str) -> dict[str, Any]:
    """Bind one validated G1 capability report to the mutable run manifest."""
    binding = _build_capability_binding(workspace, report_path)
    existing = _capability_binding(workspace)
    if existing:
        identity_keys = ("path", "sha256", "probe_id", "fingerprint", "ttl_expires_at", "status")
        if all(existing.get(key) == binding.get(key) for key in identity_keys):
            return existing
        raise RuntimeError("CAPABILITY_BINDING_CONFLICT")
    _cache_capability_binding(workspace, binding)
    return binding


def _cache_capability_binding(workspace: Path | str, binding: dict[str, Any] | None) -> None:
    """Synchronize mutable run-manifest cache after journal commit or recovery."""
    paths = ensure_workspace(workspace)
    with _workspace_lock(paths):
        manifest = _load_json(paths["run_manifest"])
        if not isinstance(manifest, dict):
            raise RuntimeError("RUN_MANIFEST_NOT_OBJECT")
        if binding is None:
            manifest.pop("capability_binding", None)
        else:
            manifest["capability_binding"] = dict(binding)
        _write_json_atomic(paths["run_manifest"], manifest)


def _load_bound_capability_report(
    workspace: Path | str,
    override_path: Path | str | None = None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[dict[str, str]]]:
    """Load the capability report bound at G1; never scan the filesystem heuristically."""
    findings: list[dict[str, str]] = []
    binding = _capability_binding(workspace)
    source = override_path or (binding.get("path") if binding else None)
    if not source:
        findings.append(_finding("P1", "CAPABILITY_REPORT_UNBOUND", "run manifest has no capability_binding"))
        return None, binding, findings
    paths = workspace_paths(workspace)
    if override_path is not None and binding and isinstance(binding.get("path"), str):
        requested = Path(os.path.abspath(str(Path(str(override_path).expanduser()))))
        bound = Path(os.path.abspath(str(Path(str(binding["path"]).expanduser()))))
        if os.path.normcase(str(requested)) != os.path.normcase(str(bound)):
            findings.append(_finding("P0", "CAPABILITY_BINDING_PATH_DRIFT", f"bound={bound}:requested={requested}"))
            return None, binding, findings
    if binding and not _is_hash(binding.get("sha256")):
        findings.append(_finding("P0", "CAPABILITY_BINDING_HASH_INVALID", str(binding.get("sha256"))))
    candidate, path_findings = _resolve_workspace_artifact(paths["root"], str(source), "CAPABILITY_REPORT")
    if candidate is None:
        findings.extend(path_findings)
        findings.append(_finding("P1", "CAPABILITY_REPORT_MISSING", str(source)))
        return None, binding, findings
    try:
        report = _load_json(candidate)
    except RuntimeError as error:
        findings.append(_finding("P0", "CAPABILITY_REPORT_INVALID_JSON", str(error)))
        return None, binding, findings
    if not isinstance(report, dict):
        findings.append(_finding("P0", "CAPABILITY_REPORT_NOT_OBJECT", str(candidate)))
        return None, binding, findings
    if binding and _is_hash(binding.get("sha256")):
        actual = _sha256_file(candidate)
        if actual != binding["sha256"]:
            findings.append(_finding("P0", "CAPABILITY_REPORT_TAMPERED", f"expected={binding['sha256']}:actual={actual}"))
    return report, binding, findings


def _validate_capability_report(report: dict[str, Any], binding: dict[str, Any] | None) -> list[dict[str, str]]:
    """Verify report identity, fingerprint stability, and TTL presence against the G1 binding."""
    findings: list[dict[str, str]] = []
    allowed_fields = {
        "schema_version", "generated_at", "status", "probe_id", "capabilities", "fingerprint",
        "ttl_expires_at", "target_path", "mode", "profile", "mandatory_ready", "certification_ceiling",
        "office", "runtimes", "hardware", "disk", "issues",
    }
    for field in sorted(set(report) - allowed_fields):
        findings.append(_finding("P0", "CAPABILITY_UNKNOWN_FIELD", field))
    if report.get("schema_version") != "1.0":
        findings.append(_finding("P0", "CAPABILITY_SCHEMA_VERSION_INVALID", str(report.get("schema_version"))))
    probe_id = report.get("probe_id")
    if not isinstance(probe_id, str) or not probe_id.strip():
        findings.append(_finding("P0", "CAPABILITY_PROBE_ID_INVALID", str(probe_id)))
    capabilities = report.get("capabilities")
    if not isinstance(capabilities, dict) or not capabilities:
        findings.append(_finding("P0", "CAPABILITY_ENTRIES_INVALID", "capabilities must be non-empty object"))
    elif any(
        not isinstance(entry, dict)
        or not isinstance(entry.get("available"), bool)
        or not isinstance(entry.get("evidence"), str)
        or not entry.get("evidence", "").strip()
        for entry in capabilities.values()
    ):
        findings.append(_finding("P0", "CAPABILITY_ENTRY_INVALID", "each capability needs boolean available and evidence"))
    status = report.get("status")
    if status not in {"PASS", "UNVERIFIED", "BLOCKED"}:
        findings.append(_finding("P0", "CAPABILITY_STATUS_INVALID", str(status)))
    fingerprint = report.get("fingerprint")
    if not isinstance(fingerprint, str) or not fingerprint.strip():
        findings.append(_finding("P1", "CAPABILITY_FINGERPRINT_MISSING", "fingerprint absent"))
    elif not _is_hash(fingerprint):
        findings.append(_finding("P0", "CAPABILITY_FINGERPRINT_INVALID", str(fingerprint)))
    generated_at = report.get("generated_at")
    if not isinstance(generated_at, str):
        findings.append(_finding("P0", "CAPABILITY_GENERATED_AT_INVALID", str(generated_at)))
    else:
        try:
            if _parse_timestamp(generated_at) > _now() + timedelta(minutes=5):
                findings.append(_finding("P0", "CAPABILITY_GENERATED_AT_IN_FUTURE", generated_at))
        except (ValueError, TypeError):
            findings.append(_finding("P0", "CAPABILITY_GENERATED_AT_INVALID", generated_at))
    ttl_raw = report.get("ttl_expires_at")
    if not isinstance(ttl_raw, str):
        findings.append(_finding("P1", "CAPABILITY_TTL_MISSING", "ttl_expires_at absent"))
    else:
        try:
            ttl = _parse_timestamp(ttl_raw)
            if isinstance(generated_at, str):
                try:
                    if ttl <= _parse_timestamp(generated_at):
                        findings.append(_finding("P0", "CAPABILITY_TTL_NOT_AFTER_GENERATION", ttl_raw))
                except (ValueError, TypeError):
                    pass
        except (ValueError, TypeError):
            findings.append(_finding("P0", "CAPABILITY_TTL_INVALID", ttl_raw))
    if binding:
        if isinstance(probe_id, str) and binding.get("probe_id") not in (None, probe_id):
            findings.append(_finding("P0", "CAPABILITY_PROBE_ID_DRIFT", f"bound={binding.get('probe_id')}:actual={probe_id}"))
        if isinstance(fingerprint, str) and binding.get("fingerprint") not in (None, fingerprint):
            findings.append(_finding("P0", "CAPABILITY_FINGERPRINT_DRIFT", f"bound={binding.get('fingerprint')}:actual={fingerprint}"))
    return findings


def validate_capability_ttl(
    workspace: Path | str,
    registry: dict[str, Any],
    gate_id: str,
    *,
    capability_report_path: Path | str | None = None,
    submission: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    """Check bound capability evidence before production or release gates."""
    if gate_id not in CAPABILITY_TTL_GATES:
        return []
    report, binding, findings = _load_bound_capability_report(workspace, capability_report_path)
    if report is None:
        if not any(item["code"] in {"CAPABILITY_REPORT_MISSING", "CAPABILITY_REPORT_UNBOUND"} for item in findings):
            findings.append(_finding("P1", "CAPABILITY_REPORT_MISSING", f"required for {gate_id}"))
        return findings
    report_findings = _validate_capability_report(report, binding)
    findings.extend(report_findings)
    capabilities = report.get("capabilities") if isinstance(report.get("capabilities"), dict) else {}
    gate = next((item for item in _registry_gates(registry) if item.get("gate_id") == gate_id), None)
    if isinstance(gate, dict):
        for required in gate.get("required_capabilities", []):
            aliases = CAPABILITY_ALIASES.get(str(required))
            if not aliases:
                continue
            unavailable = [name for name in aliases if not isinstance(capabilities.get(name), dict) or capabilities[name].get("available") is not True]
            if unavailable:
                findings.append(_finding("P1", "CAPABILITY_REQUIRED_UNAVAILABLE", f"{gate_id}:{required}:{','.join(unavailable)}"))
    if submission is not None:
        metadata = submission.get("metadata") if isinstance(submission.get("metadata"), dict) else {}
        observed_probe = metadata.get("capability_probe_id")
        observed_fingerprint = metadata.get("capability_fingerprint")
        if not isinstance(observed_probe, str) or not observed_probe or not isinstance(observed_fingerprint, str) or not observed_fingerprint:
            findings.append(_finding("P1", "CAPABILITY_BINDING_METADATA_MISSING", f"{gate_id} requires capability_probe_id and capability_fingerprint"))
        else:
            if binding and observed_probe != binding.get("probe_id"):
                findings.append(_finding("P0", "CAPABILITY_PROBE_ID_DRIFT", f"bound={binding.get('probe_id')}:observed={observed_probe}"))
            if binding and observed_fingerprint != binding.get("fingerprint"):
                findings.append(_finding("P0", "CAPABILITY_FINGERPRINT_DRIFT", f"bound={binding.get('fingerprint')}:observed={observed_fingerprint}"))
    ttl_raw = report.get("ttl_expires_at")
    if isinstance(ttl_raw, str):
        try:
            if _parse_timestamp(ttl_raw) <= _now():
                findings.append(_finding("P1", "CAPABILITY_TTL_EXPIRED", f"ttl_expires_at={ttl_raw} for {gate_id}"))
        except (ValueError, TypeError):
            findings.append(_finding("P0", "CAPABILITY_TTL_INVALID", f"cannot parse ttl_expires_at={ttl_raw}"))
    report_status = report.get("status")
    if report_status == "BLOCKED":
        findings.append(_finding("P0", "CAPABILITY_STATUS_BLOCKED", f"capability report status=BLOCKED for {gate_id}"))
    elif report_status == "UNVERIFIED":
        findings.append(_finding("P1", "CAPABILITY_STATUS_UNVERIFIED", f"capability report status=UNVERIFIED for {gate_id}"))
    return findings


def _path_is_inside(path: Path, directory: Path) -> bool:
    try:
        common = os.path.commonpath([str(path.absolute()), str(directory.absolute())])
    except ValueError:
        return False
    return os.path.normcase(common) == os.path.normcase(str(directory.absolute()))


def _decode_json(text: str, label: str) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        seen: set[str] = set()
        for key, value in pairs:
            folded = key.casefold()
            if folded in seen:
                raise RuntimeError(f"DUPLICATE_JSON_PROPERTY:{label}:{key}")
            seen.add(folded)
            result[key] = value
        return result

    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicates,
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
    except (json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"INVALID_JSON:{label}:{error}") from error


def _is_reparse(path: Path) -> bool:
    try:
        metadata = os.lstat(path)
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(metadata.st_mode):
        return True
    return bool(getattr(metadata, "st_file_attributes", 0) & 0x0400)


def _assert_safe_ancestors(path: Path) -> None:
    current = path.absolute()
    ancestors: list[Path] = []
    while True:
        ancestors.append(current)
        if current == current.parent:
            break
        current = current.parent
    for ancestor in reversed(ancestors):
        if _is_reparse(ancestor):
            raise RuntimeError(f"WORKSPACE_REPARSE_POINT:{ancestor}")


def workspace_paths(workspace: Path | str) -> dict[str, Path]:
    root = Path(workspace).expanduser().absolute()
    _assert_safe_ancestors(root.parent)
    return {
        "root": root,
        "control": root / "control",
        "transactions": root / "control" / "transactions",
        "events": root / "events",
        "inbox": root / "inbox",
        "staging": root / "staging",
        "artifacts": root / "artifacts",
        "quarantine": root / "quarantine",
        "receipts": root / "receipts",
        "release": root / "release",
        "journal": root / "events" / "events.ndjson",
        "state": root / "control" / "state.json",
        "run_manifest": root / "control" / "run.json",
        "lease": root / "control" / "lease.json",
        "lock": root / "control" / "workspace.lock",
    }


def ensure_workspace(workspace: Path | str) -> dict[str, Path]:
    paths = workspace_paths(workspace)
    paths["root"].mkdir(parents=True, exist_ok=True)
    _assert_safe_ancestors(paths["root"])
    for key in ("control", "transactions", "events", "inbox", "staging", "artifacts", "quarantine", "receipts", "release"):
        directory = paths[key]
        if _is_reparse(directory):
            raise RuntimeError(f"WORKSPACE_REPARSE_POINT:{directory}")
        directory.mkdir(parents=True, exist_ok=True)
    return paths


@contextmanager
def _workspace_lock(paths: dict[str, Path]) -> Iterator[None]:
    paths["control"].mkdir(parents=True, exist_ok=True)
    descriptor = os.open(paths["lock"], os.O_CREAT | os.O_RDWR, 0o600)
    try:
        if os.name == "nt":
            import msvcrt

            os.lseek(descriptor, 0, os.SEEK_SET)
            os.write(descriptor, b"0")
            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        try:
            if os.name == "nt":
                import msvcrt

                os.lseek(descriptor, 0, os.SEEK_SET)
                msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _write_json_new(path: Path, payload: Any) -> None:
    if path.exists() or path.is_symlink():
        raise RuntimeError(f"OUTPUT_ALREADY_EXISTS:{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(payload, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def _write_json_atomic(path: Path, payload: Any) -> None:
    if _is_reparse(path):
        raise RuntimeError(f"OUTPUT_REPARSE_POINT:{path}")
    _assert_safe_ancestors(path.parent)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, ensure_ascii=False, allow_nan=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _load_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError as error:
        raise RuntimeError(f"JSON_MISSING:{path}") from error

    try:
        return _decode_json(text, str(path))
    except RuntimeError as error:
        raise RuntimeError(f"INVALID_JSON:{path}:{error}") from error


def _read_events(paths: dict[str, Path]) -> list[dict[str, Any]]:
    journal = paths["journal"]
    if not journal.exists():
        record_files = [item for item in paths["events"].iterdir() if item.is_file() and item.name != "events.ndjson"] if paths["events"].exists() else []
        if record_files:
            raise RuntimeError(f"ORPHAN_EVENT_RECORD:{record_files[0]}")
        return []
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(journal.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            raise RuntimeError(f"EVENT_JOURNAL_BLANK_LINE:{line_number}")
        try:
            event = _decode_json(line, f"journal:{line_number}")
        except RuntimeError as error:
            raise RuntimeError(f"EVENT_JOURNAL_INVALID_JSON:{line_number}:{error}") from error
        if not isinstance(event, dict):
            raise RuntimeError(f"EVENT_JOURNAL_EVENT_NOT_OBJECT:{line_number}")
        events.append(event)
    _validate_event_chain(events)
    _validate_event_records(paths, events)
    return events


def _event_record_name(event: dict[str, Any]) -> str:
    event_id = str(event.get("event_id", ""))
    if not event_id or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for character in event_id):
        raise RuntimeError("EVENT_ID_INVALID_FOR_FILENAME")
    return f"{int(event['state_revision']):020d}-{event_id}.json"


def _event_record_files(paths: dict[str, Path]) -> list[Path]:
    if not paths["events"].exists():
        return []
    return sorted(
        item for item in paths["events"].iterdir()
        if item.is_file() and item.name != "events.ndjson"
    )


def _validate_event_records(paths: dict[str, Path], events: list[dict[str, Any]]) -> None:
    expected_names = {_event_record_name(event): event for event in events}
    actual_files = {item.name: item for item in _event_record_files(paths)}
    missing = sorted(set(expected_names) - set(actual_files))
    if missing:
        raise RuntimeError(f"EVENT_RECORD_MISSING:{missing[0]}")
    orphan = sorted(set(actual_files) - set(expected_names))
    if orphan:
        raise RuntimeError(f"ORPHAN_EVENT_RECORD:{actual_files[orphan[0]]}")
    for name, expected in expected_names.items():
        record = _load_json(actual_files[name])
        if not isinstance(record, dict):
            raise RuntimeError(f"EVENT_RECORD_NOT_OBJECT:{name}")
        _validate_event_shape(record)
        if canonical_json(record) != canonical_json(expected):
            raise RuntimeError(f"EVENT_RECORD_JOURNAL_MISMATCH:{name}")


def _registry_gates(registry: dict[str, Any]) -> list[dict[str, Any]]:
    gates = registry.get("gates", [])
    if not isinstance(gates, list):
        raise RuntimeError("REGISTRY_GATES_INVALID")
    return gates


def _contains_exact_legacy_profile(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_exact_legacy_profile(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_exact_legacy_profile(item) for item in value)
    return value == "FINAL_RELEASE"


def validate_registry(registry: dict[str, Any], schemas_dir: Path | str | None = None) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not isinstance(registry, dict):
        return [{"severity": "P0", "code": "REGISTRY_NOT_OBJECT", "detail": "registry must be an object"}]
    if registry.get("schema_version") != "1.0":
        findings.append({"severity": "P0", "code": "REGISTRY_SCHEMA_VERSION_INVALID", "detail": "schema_version must be 1.0"})
    profiles = registry.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        findings.append({"severity": "P0", "code": "REGISTRY_PROFILES_INVALID", "detail": "profiles must be non-empty"})
        profiles = []
    profile_set = set(profiles)
    unknown_profiles = sorted(profile_set - PROFILES)
    for profile in unknown_profiles:
        findings.append({"severity": "P0", "code": "REGISTRY_PROFILE_INVALID", "detail": str(profile)})
    default_profile = registry.get("default_profile")
    if default_profile not in profile_set or default_profile not in PROFILES:
        findings.append({"severity": "P0", "code": "REGISTRY_DEFAULT_PROFILE_INVALID", "detail": str(default_profile)})
    gates = registry.get("gates")
    if not isinstance(gates, list) or not gates:
        return findings + [{"severity": "P0", "code": "REGISTRY_GATES_INVALID", "detail": "gates must be non-empty"}]
    gate_by_id: dict[str, dict[str, Any]] = {}
    for gate in gates:
        if not isinstance(gate, dict):
            findings.append({"severity": "P0", "code": "REGISTRY_GATE_NOT_OBJECT", "detail": "gate entry must be object"})
            continue
        gate_id = gate.get("gate_id")
        if not isinstance(gate_id, str) or not GATE_ID_PATTERN.fullmatch(gate_id):
            findings.append({"severity": "P0", "code": "REGISTRY_GATE_ID_INVALID", "detail": str(gate_id)})
            continue
        if gate_id in gate_by_id:
            findings.append({"severity": "P0", "code": "REGISTRY_GATE_ID_DUPLICATE", "detail": gate_id})
        gate_by_id[gate_id] = gate
        if _contains_exact_legacy_profile(gate):
            findings.append({"severity": "P0", "code": "LEGACY_PROFILE_FORBIDDEN", "detail": gate_id})
        handler_id = gate.get("handler_id")
        if not isinstance(handler_id, str) or not re.fullmatch(r"[a-z][a-z0-9_.-]+", handler_id):
            findings.append({"severity": "P0", "code": "REGISTRY_HANDLER_INVALID", "detail": gate_id})
        gate_profiles = gate.get("profiles")
        if not isinstance(gate_profiles, list) or not gate_profiles:
            findings.append({"severity": "P0", "code": "REGISTRY_GATE_PROFILES_INVALID", "detail": gate_id})
        else:
            for profile in gate_profiles:
                if profile not in profile_set or profile not in PROFILES:
                    findings.append({"severity": "P0", "code": "REGISTRY_GATE_PROFILE_INVALID", "detail": f"{gate_id}:{profile}"})
        dependencies = gate.get("dependencies", [])
        if not isinstance(dependencies, list):
            findings.append({"severity": "P0", "code": "REGISTRY_DEPENDENCIES_INVALID", "detail": gate_id})
        else:
            for dependency in dependencies:
                if dependency == gate_id:
                    findings.append({"severity": "P0", "code": "REGISTRY_CYCLE", "detail": f"self:{gate_id}"})
                elif dependency not in gate_by_id and not any(isinstance(item, dict) and item.get("gate_id") == dependency for item in gates):
                    findings.append({"severity": "P0", "code": "REGISTRY_DEPENDENCY_MISSING", "detail": f"{gate_id}:{dependency}"})
        output_schema = gate.get("output_schema")
        if not isinstance(output_schema, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.schema\.json", output_schema):
            findings.append({"severity": "P0", "code": "REGISTRY_OUTPUT_SCHEMA_INVALID", "detail": gate_id})
        skip_policy = gate.get("skip_policy")
        if not isinstance(skip_policy, dict) or skip_policy.get("mode") not in {"NEVER", "PROFILE_EXCLUDED", "PREDICATE"}:
            findings.append({"severity": "P0", "code": "REGISTRY_SKIP_POLICY_INVALID", "detail": gate_id})
        invalidation_keys = gate.get("invalidation_keys")
        if not isinstance(invalidation_keys, list) or len(set(invalidation_keys)) != len(invalidation_keys):
            findings.append({"severity": "P0", "code": "REGISTRY_INVALIDATION_KEYS_INVALID", "detail": gate_id})
    if "G10_REPRESENTATIVE_PROTOTYPE" in gate_by_id:
        dependencies = set(gate_by_id["G10_REPRESENTATIVE_PROTOTYPE"].get("dependencies", []))
        if not {"G8_SLIDE_BLUEPRINT", "G9_ART_DIRECTION"}.issubset(dependencies):
            findings.append({"severity": "P0", "code": "REGISTRY_G10_DEPENDENCIES_INVALID", "detail": "G10 requires G8 and G9"})
    if "G13_NATIVE_MOTION" in gate_by_id:
        if gate_by_id["G13_NATIVE_MOTION"].get("profiles") != ["FINAL_RELEASE_MOTION"]:
            findings.append({"severity": "P0", "code": "REGISTRY_G13_PROFILE_INVALID", "detail": "G13 must be motion-only"})
    expected_terminals = {
        "FINAL_RELEASE_STATIC": "G15_STATIC_RELEASE",
        "FINAL_RELEASE_MOTION": "G15_MOTION_RELEASE",
    }
    for profile, terminal_id in expected_terminals.items():
        terminal_ids = {gate_id for gate_id, gate in gate_by_id.items() if gate.get("terminal") is True and profile in gate.get("profiles", [])}
        if terminal_ids != {terminal_id}:
            findings.append({"severity": "P0", "code": "REGISTRY_TERMINAL_INVALID", "detail": f"{profile}:{sorted(terminal_ids)}"})
    if schemas_dir is not None:
        schema_root = Path(schemas_dir).absolute()
        for gate_id, gate in gate_by_id.items():
            output_schema = gate.get("output_schema")
            if isinstance(output_schema, str) and not (schema_root / output_schema).is_file():
                findings.append({"severity": "P0", "code": "REGISTRY_SCHEMA_MISSING", "detail": f"{gate_id}:{output_schema}"})
    adjacency = {gate_id: [dependency for dependency in gate.get("dependencies", []) if dependency in gate_by_id] for gate_id, gate in gate_by_id.items()}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(gate_id: str) -> None:
        if gate_id in visiting:
            findings.append({"severity": "P0", "code": "REGISTRY_CYCLE", "detail": gate_id})
            return
        if gate_id in visited:
            return
        visiting.add(gate_id)
        for dependency in adjacency.get(gate_id, []):
            visit(dependency)
        visiting.remove(gate_id)
        visited.add(gate_id)

    for gate_id in adjacency:
        visit(gate_id)
    return findings


def _validate_event_shape(event: dict[str, Any]) -> None:
    required = ("event_id", "run_id", "state_revision", "previous_event_sha256", "event_sha256", "gate_id", "attempt_id", "actor_id", "actor_kind", "context_id", "status", "input_bindings", "output_bindings", "generated_at", "reason")
    missing = [name for name in required if name not in event]
    if missing:
        raise RuntimeError(f"EVENT_PROPERTY_MISSING:{','.join(missing)}")
    if event.get("schema_version") != "1.0":
        raise RuntimeError("EVENT_SCHEMA_VERSION_INVALID")
    for key in ("event_id", "run_id", "gate_id", "attempt_id", "actor_id", "context_id", "reason"):
        if not isinstance(event[key], str) or not event[key].strip():
            raise RuntimeError(f"EVENT_STRING_INVALID:{key}")
    if not GATE_ID_PATTERN.fullmatch(event["gate_id"]):
        raise RuntimeError("EVENT_GATE_ID_INVALID")
    if not isinstance(event["state_revision"], int) or event["state_revision"] < 1:
        raise RuntimeError("EVENT_STATE_REVISION_INVALID")
    if event["status"] not in EVENT_STATUSES:
        raise RuntimeError(f"EVENT_STATUS_INVALID:{event['status']}")
    if event["actor_kind"] not in ACTOR_KINDS:
        raise RuntimeError(f"EVENT_ACTOR_KIND_INVALID:{event['actor_kind']}")
    if not isinstance(event["input_bindings"], list) or not isinstance(event["output_bindings"], list):
        raise RuntimeError("EVENT_BINDINGS_INVALID")
    if not isinstance(event["generated_at"], str):
        raise RuntimeError("EVENT_TIMESTAMP_INVALID")
    _parse_timestamp(event["generated_at"])
    for key in ("previous_event_sha256", "event_sha256"):
        value = event[key]
        if not isinstance(value, str) or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            raise RuntimeError(f"EVENT_HASH_INVALID:{key}")


def _validate_event_chain(events: list[dict[str, Any]]) -> None:
    previous = ZERO_HASH
    run_id: str | None = None
    event_ids: set[str] = set()
    for expected_revision, event in enumerate(events, start=1):
        _validate_event_shape(event)
        if event["event_id"] in event_ids:
            raise RuntimeError(f"EVENT_ID_DUPLICATE:{event['event_id']}")
        event_ids.add(event["event_id"])
        if event["state_revision"] != expected_revision:
            raise RuntimeError(f"EVENT_REVISION_SEQUENCE_INVALID:{expected_revision}")
        if event["previous_event_sha256"] != previous:
            raise RuntimeError(f"EVENT_PREVIOUS_HASH_MISMATCH:{expected_revision}")
        if event_digest(event) != event["event_sha256"]:
            raise RuntimeError(f"EVENT_HASH_MISMATCH:{expected_revision}")
        if run_id is None:
            run_id = event["run_id"]
        elif event["run_id"] != run_id:
            raise RuntimeError(f"EVENT_RUN_ID_MISMATCH:{expected_revision}")
        previous = event["event_sha256"]


def _load_run_manifest(paths: dict[str, Path]) -> dict[str, Any] | None:
    if not paths["run_manifest"].exists():
        return None
    manifest = _load_json(paths["run_manifest"])
    if not isinstance(manifest, dict):
        raise RuntimeError("RUN_MANIFEST_NOT_OBJECT")
    return manifest


def _profile_for(registry: dict[str, Any], events: list[dict[str, Any]], manifest: dict[str, Any] | None = None) -> str:
    if manifest and manifest.get("active_profile") in PROFILES:
        return str(manifest["active_profile"])
    for event in events:
        metadata = event.get("metadata")
        if isinstance(metadata, dict) and metadata.get("active_profile") in PROFILES:
            return str(metadata["active_profile"])
    profile = registry.get("default_profile", "FINAL_RELEASE_MOTION")
    if profile not in PROFILES:
        raise RuntimeError("REGISTRY_DEFAULT_PROFILE_INVALID")
    return profile


def _initial_gate_state(gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "PENDING",
        "attempts": 0,
        "invalidation_keys": list(gate.get("invalidation_keys", [])),
        "receipt_path": None,
        "receipt_sha256": None,
        "reason": None,
    }


def _is_gate_in_profile(gate: dict[str, Any], profile: str) -> bool:
    return profile in gate.get("profiles", [])


def _gate_is_skippable(gate: dict[str, Any], profile: str) -> bool:
    policy = gate.get("skip_policy", {})
    if policy.get("mode") == "PROFILE_EXCLUDED":
        return profile in policy.get("excluded_profiles", [])
    return False


def _next_gate(gates: list[dict[str, Any]], gate_states: dict[str, dict[str, Any]], profile: str) -> str | None:
    for gate in gates:
        gate_id = gate["gate_id"]
        current = gate_states[gate_id]["status"]
        if current in TERMINAL_STATUSES:
            continue
        if not _is_gate_in_profile(gate, profile):
            if _gate_is_skippable(gate, profile):
                return gate_id
            continue
        dependencies = gate.get("dependencies", [])
        if all(gate_states.get(dependency, {}).get("status") in {"PASS", "SKIPPED"} for dependency in dependencies):
            return gate_id
    return None


def _finding(severity: str, code: str, detail: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "detail": detail}


def _resolve_workspace_artifact(workspace: Path, raw_path: Any, label: str) -> tuple[Path | None, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    if not isinstance(raw_path, str) or not raw_path.strip():
        findings.append(_finding("P1", f"{label}_PATH_INVALID", "path must be non-empty string"))
        return None, findings
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = workspace / candidate
    candidate = Path(os.path.abspath(str(candidate)))
    if not _path_is_inside(candidate, workspace):
        findings.append(_finding("P0", "ARTIFACT_OUTSIDE_WORKSPACE", f"{label}:{candidate}"))
        return None, findings
    try:
        _assert_safe_ancestors(candidate)
    except RuntimeError as error:
        findings.append(_finding("P0", "ARTIFACT_REPARSE_POINT", f"{label}:{error}"))
        return None, findings
    if _is_reparse(candidate):
        findings.append(_finding("P0", "ARTIFACT_REPARSE_POINT", f"{label}:{candidate}"))
        return None, findings
    if not candidate.is_file():
        findings.append(_finding("P1", f"{label}_MISSING", str(candidate)))
        return None, findings
    return candidate, findings


def _validate_submission_artifact(workspace: Path, artifact: Any, label: str, expected_schema: str | None = None) -> tuple[Path | None, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    if not isinstance(artifact, dict):
        return None, [_finding("P1", f"{label}_NOT_OBJECT", "artifact must be object")]
    unknown = sorted(set(artifact) - ALLOWED_ARTIFACT_FIELDS)
    findings.extend(_finding("P0", f"{label}_UNKNOWN_FIELD", field) for field in unknown)
    for field in ("path", "sha256", "kind"):
        if field not in artifact:
            findings.append(_finding("P1", f"{label}_MISSING_FIELD", field))
    if not _is_hash(artifact.get("sha256")):
        findings.append(_finding("P0", f"{label}_HASH_INVALID", str(artifact.get("sha256"))))
    if expected_schema is not None and artifact.get("schema") != expected_schema:
        findings.append(_finding("P0", f"{label}_SCHEMA_MISMATCH", f"expected={expected_schema}:actual={artifact.get('schema')}"))
    path, path_findings = _resolve_workspace_artifact(workspace, artifact.get("path"), label)
    findings.extend(path_findings)
    if path is not None and _is_hash(artifact.get("sha256")):
        actual_hash = _sha256_file(path)
        if actual_hash != artifact["sha256"]:
            findings.append(_finding("P0", f"{label}_HASH_MISMATCH", str(path)))
    return path, findings


def _validate_local_schema_instance(instance: Any, schema_name: str) -> list[dict[str, str]]:
    schema_root = Path(__file__).resolve().parents[1] / "schemas"
    schema_path = schema_root / schema_name
    if not schema_path.is_file():
        return [_finding("P0", "LOCAL_SCHEMA_MISSING", schema_name)]
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource
    except ImportError as error:
        return [_finding("P1", "CAPABILITY_SCHEMA_RUNTIME_MISSING", str(error))]
    try:
        schema = _load_json(schema_path)
        registry = Registry()
        for local_path in sorted(schema_root.glob("*.json")):
            local_schema = _load_json(local_path)
            resource = Resource.from_contents(local_schema)
            schema_id = local_schema.get("$id") if isinstance(local_schema, dict) else None
            if schema_id:
                registry = registry.with_resource(schema_id, resource)
            registry = registry.with_resource(local_path.as_uri(), resource)
        validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(instance), key=lambda item: tuple(str(part) for part in item.absolute_path))
    except (RuntimeError, ValueError) as error:
        return [_finding("P0", "LOCAL_SCHEMA_INVALID", f"{schema_name}:{error}")]
    return [
        _finding("P0", "CAPABILITY_SCHEMA_VALIDATION_FAILED", f"/{'/'.join(str(part) for part in error.absolute_path)}:{error.message}")
        for error in errors[:100]
    ]


def _capability_submission_binding(workspace: Path, submission: dict[str, Any]) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    artifacts = submission.get("output_artifacts")
    if not isinstance(artifacts, list):
        return None, [_finding("P0", "CAPABILITY_OUTPUT_REQUIRED", "output_artifacts must contain one capability report")]
    matching = [artifact for artifact in artifacts if isinstance(artifact, dict) and artifact.get("schema") == "capability-report.schema.json"]
    if len(matching) != 1:
        return None, [_finding("P0", "CAPABILITY_OUTPUT_COUNT_INVALID", f"expected=1:actual={len(matching)}")]
    artifact = matching[0]
    path, path_findings = _resolve_workspace_artifact(workspace, artifact.get("path"), "CAPABILITY_REPORT")
    findings.extend(path_findings)
    if path is None:
        return None, findings
    try:
        report = _load_json(path)
    except RuntimeError as error:
        findings.append(_finding("P0", "CAPABILITY_REPORT_INVALID_JSON", str(error)))
        return None, findings
    if not isinstance(report, dict):
        findings.append(_finding("P0", "CAPABILITY_REPORT_NOT_OBJECT", str(path)))
        return None, findings
    findings.extend(_validate_local_schema_instance(report, "capability-report.schema.json"))
    findings.extend(_validate_capability_report(report, None))
    submission_status = submission.get("status")
    if report.get("status") != submission_status:
        findings.append(_finding("P0", "CAPABILITY_SUBMISSION_STATUS_MISMATCH", f"report={report.get('status')}:submission={submission_status}"))
    if report.get("certification_ceiling") != report.get("status"):
        findings.append(_finding("P0", "CAPABILITY_CEILING_STATUS_MISMATCH", f"ceiling={report.get('certification_ceiling')}:status={report.get('status')}"))
    if report.get("status") == "PASS" and report.get("mandatory_ready") is not True:
        findings.append(_finding("P0", "CAPABILITY_PASS_WITHOUT_MANDATORY_READY", str(path)))
    if findings:
        return None, findings
    binding = {
        "path": str(path),
        "sha256": _sha256_file(path),
        "probe_id": str(report["probe_id"]),
        "fingerprint": str(report["fingerprint"]),
        "ttl_expires_at": str(report["ttl_expires_at"]),
        "status": str(report["status"]),
        "bound_at": _timestamp(),
    }
    if _is_hash(artifact.get("sha256")) and artifact["sha256"] != binding["sha256"]:
        findings.append(_finding("P0", "CAPABILITY_ARTIFACT_HASH_MISMATCH", str(path)))
        return None, findings
    return binding, findings


def validate_submission(
    workspace: Path | str,
    submission: dict[str, Any],
    registry: dict[str, Any],
    *,
    quarantine_invalid: bool = False,
) -> list[dict[str, str]]:
    paths = ensure_workspace(workspace)
    root = paths["root"]
    findings: list[dict[str, str]] = []
    if not isinstance(submission, dict):
        return [_finding("P0", "SUBMISSION_NOT_OBJECT", "submission must be object")]
    findings.extend(_finding("P0", "SUBMISSION_UNKNOWN_FIELD", field) for field in sorted(set(submission) - ALLOWED_SUBMISSION_FIELDS))
    required = ("schema_version", "run_id", "gate_id", "attempt_id", "producer", "actor_context_id", "input_artifacts", "output_artifacts", "dependency_hashes", "tool_fingerprint", "status", "findings", "generated_at")
    for field in required:
        if field not in submission:
            findings.append(_finding("P1", "SUBMISSION_MISSING_FIELD", field))
    if submission.get("schema_version") != "1.0":
        findings.append(_finding("P0", "SUBMISSION_SCHEMA_VERSION_INVALID", str(submission.get("schema_version"))))
    for field in ("run_id", "gate_id", "attempt_id", "producer", "actor_context_id", "tool_fingerprint"):
        if field in submission and (not isinstance(submission[field], str) or not submission[field].strip()):
            findings.append(_finding("P1", "SUBMISSION_STRING_INVALID", field))
    try:
        _parse_timestamp(str(submission.get("generated_at")))
    except (TypeError, ValueError):
        findings.append(_finding("P1", "SUBMISSION_TIMESTAMP_INVALID", str(submission.get("generated_at"))))
    gate_by_id = {gate.get("gate_id"): gate for gate in _registry_gates(registry) if isinstance(gate, dict)}
    gate_id = submission.get("gate_id")
    gate = gate_by_id.get(gate_id)
    if gate is None:
        findings.append(_finding("P0", "SUBMISSION_GATE_UNKNOWN", str(gate_id)))
    try:
        state = rebuild_state(root, registry)
    except RuntimeError as error:
        findings.append(_finding("P0", "SUBMISSION_STATE_UNAVAILABLE", str(error)))
        state = None
    if state is not None:
        if submission.get("run_id") != state["run_id"]:
            findings.append(_finding("P0", "SUBMISSION_RUN_ID_MISMATCH", str(submission.get("run_id"))))
        if gate is not None:
            next_gate = state.get("next_gate")
            if gate_id != next_gate:
                findings.append(_finding("P1", "SUBMISSION_GATE_NOT_NEXT", f"expected={next_gate}:actual={gate_id}"))
            gate_state = state["gates"].get(gate_id, {})
            if gate_state.get("status") in TERMINAL_STATUSES:
                findings.append(_finding("P1", "SUBMISSION_GATE_ALREADY_TERMINAL", str(gate_id)))
            for dependency in gate.get("dependencies", []):
                dependency_state = state["gates"].get(dependency, {})
                dependency_status = dependency_state.get("status")
                if dependency_status not in {"PASS", "SKIPPED"}:
                    findings.append(_finding("P0", "SUBMISSION_DEPENDENCY_NOT_COMPLETE", f"{gate_id}:{dependency}"))
                if dependency_status == "PASS":
                    expected_hash = dependency_state.get("receipt_sha256")
                    actual_hash = (submission.get("dependency_hashes") or {}).get(dependency) if isinstance(submission.get("dependency_hashes"), dict) else None
                    if not _is_hash(expected_hash) or actual_hash != expected_hash:
                        findings.append(_finding("P0", "SUBMISSION_DEPENDENCY_HASH_MISMATCH", f"{dependency}:expected={expected_hash}:actual={actual_hash}"))
    dependency_hashes = submission.get("dependency_hashes")
    if not isinstance(dependency_hashes, dict):
        findings.append(_finding("P1", "SUBMISSION_DEPENDENCY_HASHES_INVALID", "must be object"))
    else:
        for dependency, value in dependency_hashes.items():
            if not _is_hash(value):
                findings.append(_finding("P0", "SUBMISSION_DEPENDENCY_HASH_INVALID", str(dependency)))
    input_artifacts = submission.get("input_artifacts")
    output_artifacts = submission.get("output_artifacts")
    if not isinstance(input_artifacts, list) or not isinstance(output_artifacts, list):
        findings.append(_finding("P1", "SUBMISSION_ARTIFACT_LIST_INVALID", "input_artifacts/output_artifacts must be arrays"))
        input_artifacts = input_artifacts if isinstance(input_artifacts, list) else []
        output_artifacts = output_artifacts if isinstance(output_artifacts, list) else []
    expected_schema = gate.get("output_schema") if gate is not None else None
    artifact_paths: set[str] = set()
    for artifact in input_artifacts:
        path, artifact_findings = _validate_submission_artifact(root, artifact, "INPUT_ARTIFACT")
        findings.extend(artifact_findings)
        if path is not None:
            normalized = os.path.normcase(str(path))
            if normalized in artifact_paths:
                findings.append(_finding("P1", "SUBMISSION_ARTIFACT_DUPLICATE_PATH", str(path)))
            artifact_paths.add(normalized)
    output_paths: list[Path] = []
    for artifact in output_artifacts:
        path, artifact_findings = _validate_submission_artifact(root, artifact, "OUTPUT_ARTIFACT", expected_schema)
        findings.extend(artifact_findings)
        if path is not None:
            output_paths.append(path)
            normalized = os.path.normcase(str(path))
            if normalized in artifact_paths:
                findings.append(_finding("P0", "SUBMISSION_INPUT_OUTPUT_COLLISION", str(path)))
            if normalized in {os.path.normcase(str(item)) for item in output_paths[:-1]}:
                findings.append(_finding("P1", "SUBMISSION_ARTIFACT_DUPLICATE_PATH", str(path)))
            artifact_paths.add(normalized)
        if submission.get("status") == "PASS" and isinstance(artifact, dict) and artifact.get("immutable") is not True:
            findings.append(_finding("P1", "OUTPUT_ARTIFACT_NOT_IMMUTABLE", str(artifact.get("path"))))
    status = submission.get("status")
    if status == "PASS" and not output_artifacts:
        findings.append(_finding("P0", "PASS_OUTPUT_ARTIFACT_REQUIRED", str(gate_id)))
    if gate_id == "G1_CAPABILITY_SECURITY" and status in {"PASS", "UNVERIFIED"}:
        _, capability_findings = _capability_submission_binding(root, submission)
        findings.extend(capability_findings)
    if gate_id in CAPABILITY_TTL_GATES:
        metadata = submission.get("metadata") if isinstance(submission.get("metadata"), dict) else {}
        capability_override = metadata.get("capability_report_path") if isinstance(metadata.get("capability_report_path"), str) else None
        findings.extend(validate_capability_ttl(root, registry, str(gate_id), capability_report_path=capability_override, submission=submission))
    if status == "SKIPPED":
        metadata = submission.get("metadata")
        if not isinstance(metadata, dict) or not isinstance(metadata.get("skip_reason"), str) or not metadata.get("skip_reason") or not isinstance(metadata.get("predicate"), str) or not metadata.get("predicate"):
            findings.append(_finding("P0", "SKIP_METADATA_REQUIRED", str(gate_id)))
        elif gate is not None:
            policy = gate.get("skip_policy", {})
            predicate = metadata["predicate"]
            allowed = policy.get("mode") == "PREDICATE" and predicate == policy.get("predicate")
            allowed = allowed or (policy.get("mode") == "PROFILE_EXCLUDED" and predicate == "PROFILE_NOT_TARGET" and state is not None and state.get("active_profile") in policy.get("excluded_profiles", []))
            if not allowed:
                findings.append(_finding("P0", "SKIP_NOT_ALLOWED", str(gate_id)))
    if status == "PASS" and isinstance(submission.get("findings"), list):
        for finding in submission["findings"]:
            if isinstance(finding, dict) and finding.get("severity") in {"P0", "P1"}:
                findings.append(_finding("P0", "CRITICAL_FINDING_ON_PASS", str(finding.get("code", "unknown"))))
    metadata = submission.get("metadata")
    if gate is not None and str(gate_id).startswith("G15_"):
        actor_kind = metadata.get("actor_kind") if isinstance(metadata, dict) else None
        producer = str(submission.get("producer", "")).casefold()
        if actor_kind == "AGENT" or "agent" in producer:
            findings.append(_finding("P0", "RELEASE_CERTIFICATE_AGENT_SUBMISSION_FORBIDDEN", str(gate_id)))
    if gate is not None and gate.get("independent_reviewer_required"):
        reviewer_context = submission.get("review_context_id")
        if not isinstance(reviewer_context, str) or not reviewer_context.strip() or reviewer_context == submission.get("actor_context_id"):
            findings.append(_finding("P0", "INDEPENDENT_REVIEWER_REQUIRED", str(gate_id)))
    if quarantine_invalid:
        for path in output_paths:
            if any(finding.get("code") in {"OUTPUT_ARTIFACT_HASH_MISMATCH", "ARTIFACT_REPARSE_POINT", "ARTIFACT_OUTSIDE_WORKSPACE"} for finding in findings):
                quarantine_artifact(root, path, "submission-validation-failure")
    return findings


def quarantine_artifact(workspace: Path | str, path: Path | str, reason: str) -> Path:
    paths = ensure_workspace(workspace)
    source = Path(path).absolute()
    if not source.exists() or not source.is_file() or _is_reparse(source):
        raise RuntimeError(f"QUARANTINE_SOURCE_INVALID:{source}")
    _assert_safe_ancestors(source)
    if not _path_is_inside(source, paths["root"]):
        raise RuntimeError(f"QUARANTINE_SOURCE_OUTSIDE_WORKSPACE:{source}")
    target = paths["quarantine"] / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}-{uuid.uuid4().hex}-{source.name}"
    shutil.move(str(source), str(target))
    receipt = {
        "schema_version": "1.0",
        "operation": "QUARANTINE",
        "reason": reason,
        "source_path": str(source),
        "quarantine_path": str(target),
        "sha256": _sha256_file(target),
        "generated_at": _timestamp(),
    }
    _write_json_new(paths["receipts"] / f"quarantine-{uuid.uuid4().hex}.json", receipt)
    return target


def _read_recovery_journal(paths: dict[str, Path]) -> list[dict[str, Any]]:
    if not paths["journal"].exists():
        return []
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(paths["journal"].read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            raise RuntimeError(f"RECOVERY_BLANK_JOURNAL_LINE:{line_number}")
        event = _decode_json(line, f"recovery-journal:{line_number}")
        if not isinstance(event, dict):
            raise RuntimeError(f"RECOVERY_EVENT_NOT_OBJECT:{line_number}")
        events.append(event)
    _validate_event_chain(events)
    return events


def _quarantine_event_record(paths: dict[str, Path], source: Path, reason: str) -> Path:
    if not source.exists() or not source.is_file() or _is_reparse(source):
        raise RuntimeError(f"RECOVERY_QUARANTINE_SOURCE_INVALID:{source}")
    _assert_safe_ancestors(source)
    if not _path_is_inside(source, paths["root"]):
        raise RuntimeError(f"RECOVERY_QUARANTINE_SOURCE_OUTSIDE_WORKSPACE:{source}")
    target = paths["quarantine"] / f"event-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}-{uuid.uuid4().hex}-{source.name}"
    shutil.move(str(source), str(target))
    return target


def recover_workspace(workspace: Path | str, registry: dict[str, Any]) -> dict[str, Any]:
    paths = ensure_workspace(workspace)
    with _workspace_lock(paths):
        journal_events = _read_recovery_journal(paths)
        actual_files = {item.name: item for item in _event_record_files(paths)}
        quarantined: list[str] = []
        restored_count = 0
        promoted_count = 0
        expected_names = {_event_record_name(event): event for event in journal_events}

        manifest = _load_run_manifest(paths)
        manifest_run_id = manifest.get("run_id") if isinstance(manifest, dict) else None

        orphan_paths = {source for name, source in actual_files.items() if name not in expected_names}
        while True:
            next_revision = len(journal_events) + 1
            candidates: list[tuple[Path, dict[str, Any]]] = []
            for source in sorted(orphan_paths, key=lambda item: item.name):
                try:
                    record = _load_json(source)
                    if not isinstance(record, dict):
                        raise RuntimeError("EVENT_RECORD_NOT_OBJECT")
                    _validate_event_shape(record)
                    if event_digest(record) != record.get("event_sha256"):
                        raise RuntimeError("EVENT_RECORD_HASH_MISMATCH")
                    if _event_record_name(record) != source.name:
                        raise RuntimeError("EVENT_RECORD_FILENAME_MISMATCH")
                except RuntimeError as error:
                    target = _quarantine_event_record(paths, source, f"recovery-invalid-record:{error}")
                    quarantined.append(str(target))
                    orphan_paths.remove(source)
                    continue
                revision = record.get("state_revision")
                if not isinstance(revision, int):
                    target = _quarantine_event_record(paths, source, "recovery-invalid-sequence")
                    quarantined.append(str(target))
                    orphan_paths.remove(source)
                    continue
                if revision == next_revision:
                    candidates.append((source, record))
                elif revision <= len(journal_events):
                    expected = journal_events[revision - 1]
                    if expected.get("event_id") == record.get("event_id"):
                        if canonical_json(expected) != canonical_json(record):
                            raise RuntimeError(f"EVENT_RECORD_JOURNAL_MISMATCH:{source.name}")
                    else:
                        target = _quarantine_event_record(paths, source, "recovery-duplicate-sequence")
                        quarantined.append(str(target))
                        orphan_paths.remove(source)
                else:
                    target = _quarantine_event_record(paths, source, "recovery-future-sequence")
                    quarantined.append(str(target))
                    orphan_paths.remove(source)
            if not candidates:
                break
            if len(candidates) > 1:
                raise RuntimeError("RECOVERY_MULTIPLE_NEXT_RECORDS")
            source, candidate = candidates[0]
            expected_previous = journal_events[-1]["event_sha256"] if journal_events else ZERO_HASH
            if candidate.get("previous_event_sha256") != expected_previous:
                target = _quarantine_event_record(paths, source, "recovery-previous-hash-mismatch")
                quarantined.append(str(target))
                orphan_paths.remove(source)
                continue
            if journal_events and candidate.get("run_id") != journal_events[0].get("run_id"):
                raise RuntimeError("RECOVERY_RECORD_RUN_ID_CONFLICT")
            if not journal_events and isinstance(manifest_run_id, str) and candidate.get("run_id") != manifest_run_id:
                raise RuntimeError("RECOVERY_RECORD_MANIFEST_RUN_ID_MISMATCH")
            _append_journal_line(paths, candidate)
            journal_events.append(candidate)
            orphan_paths.remove(source)
            promoted_count += 1

        expected_names = {_event_record_name(event): event for event in journal_events}
        actual_files = {item.name: item for item in _event_record_files(paths)}
        missing_names = sorted(set(expected_names) - set(actual_files))
        for name in missing_names:
            _write_json_new(paths["events"] / name, expected_names[name])
            restored_count += 1

        actual_files = {item.name: item for item in _event_record_files(paths)}
        for name, expected in expected_names.items():
            source = actual_files.get(name)
            if source is None:
                raise RuntimeError(f"EVENT_RECORD_MISSING:{name}")
            try:
                record = _load_json(source)
                if not isinstance(record, dict):
                    raise RuntimeError("EVENT_RECORD_NOT_OBJECT")
                _validate_event_shape(record)
            except RuntimeError as error:
                raise RuntimeError(f"EVENT_RECORD_INVALID:{name}:{error}") from error
            if canonical_json(record) != canonical_json(expected):
                raise RuntimeError(f"EVENT_RECORD_JOURNAL_MISMATCH:{name}")

        for source in sorted((item for item in _event_record_files(paths) if item.name not in expected_names), key=lambda item: item.name):
            target = _quarantine_event_record(paths, source, "recovery-unmatched-record")
            quarantined.append(str(target))

        _validate_event_records(paths, journal_events)
        journal_hash = hashlib.sha256(paths["journal"].read_bytes()).hexdigest() if paths["journal"].exists() else ZERO_HASH
        recovery_receipt = {
            "schema_version": "1.0",
            "operation": "RECOVERY",
            "status": "PASS",
            "journal_sha256": journal_hash,
            "restored_count": restored_count,
            "promoted_count": promoted_count,
            "quarantined_count": len(quarantined),
            "quarantined_paths": quarantined,
            "generated_at": _timestamp(),
        }
        receipt_path = paths["receipts"] / f"recovery-{uuid.uuid4().hex}.json"
        _write_json_new(receipt_path, recovery_receipt)
        state = rebuild_state(paths["root"], registry)
        manifest = _load_run_manifest(paths)
        if isinstance(manifest, dict):
            if manifest.get("capability_binding") != state.get("capability_binding"):
                if state.get("capability_binding") is None:
                    manifest.pop("capability_binding", None)
                else:
                    manifest["capability_binding"] = state["capability_binding"]
                _write_json_atomic(paths["run_manifest"], manifest)
        _write_json_atomic(paths["state"], state)
    recovery_receipt["receipt_path"] = str(receipt_path)
    recovery_receipt["state_revision"] = state["state_revision"]
    return recovery_receipt


def rebuild_state(workspace: Path | str, registry: dict[str, Any]) -> dict[str, Any]:
    paths = ensure_workspace(workspace)
    if any(key in registry for key in ("schema_version", "profiles", "default_profile")):
        registry_findings = validate_registry(registry)
        if any(finding.get("severity") == "P0" for finding in registry_findings):
            raise RuntimeError("REGISTRY_INVALID:" + ";".join(finding["code"] for finding in registry_findings))
    events = _read_events(paths)
    gates = _registry_gates(registry)
    manifest = _load_run_manifest(paths)
    profile = _profile_for(registry, events, manifest)
    gate_states = {gate["gate_id"]: _initial_gate_state(gate) for gate in gates}
    run_id = events[0]["run_id"] if events else str((manifest or {}).get("run_id", registry.get("run_id", "uninitialized")))
    source_snapshot_hash = str((manifest or {}).get("source_snapshot_hash", ZERO_HASH))
    job_contract_hash = str((manifest or {}).get("job_contract_hash", ZERO_HASH))
    fingerprints = {
        "skill_sha256": ZERO_HASH,
        "schema_bundle_sha256": ZERO_HASH,
        "gate_registry_sha256": ZERO_HASH,
        "script_fingerprint": "unbound",
        "runtime_fingerprint": "unbound",
        "office_fingerprint": "unbound",
        "font_fingerprint": "unbound",
        "artifact_tool_fingerprint": "unbound",
        "asr_runtime_fingerprint": None,
    }
    if manifest and isinstance(manifest.get("fingerprints"), dict):
        fingerprints.update(manifest["fingerprints"])
    projection_fault = False
    for event in events:
        metadata = event.get("metadata")
        if isinstance(metadata, dict):
            if isinstance(metadata.get("source_snapshot_hash"), str):
                source_snapshot_hash = metadata["source_snapshot_hash"]
            if isinstance(metadata.get("job_contract_hash"), str):
                job_contract_hash = metadata["job_contract_hash"]
            if isinstance(metadata.get("fingerprints"), dict):
                fingerprints.update(metadata["fingerprints"])
        gate_id = event["gate_id"]
        if gate_id not in gate_states:
            gate_states[gate_id] = {
                "status": "QUARANTINED",
                "attempts": 0,
                "invalidation_keys": [],
                "receipt_path": None,
                "receipt_sha256": None,
                "reason": "GATE_NOT_IN_REGISTRY",
            }
            projection_fault = True
        gate_state = gate_states[gate_id]
        if event["status"] == "STARTED":
            gate_state["attempts"] += 1
            gate_state["status"] = "RUNNING"
        elif event["status"] == "RECOVERED":
            metadata = event.get("metadata")
            if not isinstance(metadata, dict) or not metadata.get("lease_takeover_only"):
                gate_state["status"] = "PENDING"
                gate_state["reason"] = event["reason"]
        else:
            gate_state["status"] = event["status"]
            gate_state["reason"] = event["reason"]
        outputs = event.get("output_bindings") or []
        if outputs:
            first_output = outputs[0]
            gate_state["receipt_path"] = first_output.get("path")
            gate_state["receipt_sha256"] = first_output.get("sha256")
    active_gate_ids = [gate["gate_id"] for gate in gates if _is_gate_in_profile(gate, profile)]
    active_statuses = [gate_states[gate_id]["status"] for gate_id in active_gate_ids]
    if not events:
        status = "INITIALIZED"
    elif projection_fault or any(value in {"BLOCKED", "QUARANTINED"} for value in active_statuses):
        status = "BLOCKED"
    elif any(value == "UNVERIFIED" for value in active_statuses):
        status = "UNVERIFIED"
    elif any(value == "STALE" for value in active_statuses):
        status = "STALE"
    elif all(value in COMPLETED_STATUSES for value in active_statuses):
        status = "PASS"
    else:
        status = "RUNNING"
    capability_binding = _capability_binding(paths["root"])
    next_gate = _next_gate(gates, gate_states, profile)
    state = {
        "schema_version": "1.0",
        "run_id": run_id,
        "pipeline_version": str(registry.get("pipeline_version", "6.2.0")),
        "state_revision": len(events),
        "status": status,
        "active_profile": profile,
        "source_snapshot_hash": source_snapshot_hash,
        "job_contract_hash": job_contract_hash,
        "fingerprints": fingerprints,
        "capability_binding": capability_binding,
        "gates": gate_states,
        "lease": _load_json(paths["lease"]) if paths["lease"].exists() else None,
        "last_event_sha256": events[-1]["event_sha256"] if events else None,
        "next_gate": next_gate,
    }
    return state


def validate_state(workspace: Path | str, state: dict[str, Any], registry: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    try:
        rebuilt = rebuild_state(workspace, registry)
    except RuntimeError as error:
        return [{"severity": "P0", "code": "STATE_REPLAY_FAILED", "detail": str(error)}]
    if state.get("state_revision") != rebuilt["state_revision"]:
        findings.append({"severity": "P1", "code": "STATE_REVISION_MISMATCH", "detail": f"state={state.get('state_revision')} rebuilt={rebuilt['state_revision']}"})
    if state.get("last_event_sha256") != rebuilt["last_event_sha256"]:
        findings.append({"severity": "P0", "code": "STATE_LAST_EVENT_HASH_MISMATCH", "detail": "snapshot does not match journal"})
    if state.get("run_id") != rebuilt["run_id"]:
        findings.append({"severity": "P1", "code": "STATE_RUN_ID_MISMATCH", "detail": "snapshot does not match journal"})
    if state.get("gates") != rebuilt["gates"]:
        findings.append({"severity": "P1", "code": "STATE_GATE_PROJECTION_MISMATCH", "detail": "gate projection differs from journal replay"})
    if state.get("capability_binding") != rebuilt.get("capability_binding"):
        findings.append({"severity": "P1", "code": "STATE_CAPABILITY_BINDING_MISMATCH", "detail": "capability binding differs from journal replay"})
    return findings


def _append_event_locked(paths: dict[str, Path], event: dict[str, Any], expected_revision: int) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise RuntimeError("EVENT_MUST_BE_OBJECT")
    events = _read_events(paths)
    current_revision = len(events)
    if expected_revision != current_revision:
        raise RuntimeError(f"STATE_REVISION_CONFLICT:expected={expected_revision}:actual={current_revision}")
    if current_revision and event.get("run_id") != events[0]["run_id"]:
        raise RuntimeError("EVENT_RUN_ID_MISMATCH")
    event_id = str(event.get("event_id") or uuid.uuid4().hex)
    if any(existing.get("event_id") == event_id for existing in events):
        raise RuntimeError(f"EVENT_ID_DUPLICATE:{event_id}")
    generated_at = event.get("generated_at") or _timestamp()
    normalized = dict(event)
    normalized.update(
        {
            "schema_version": "1.0",
            "event_id": event_id,
            "run_id": str(event.get("run_id") or (events[0]["run_id"] if events else uuid.uuid4().hex)),
            "state_revision": current_revision + 1,
            "previous_event_sha256": events[-1]["event_sha256"] if events else ZERO_HASH,
            "attempt_id": str(event.get("attempt_id") or uuid.uuid4().hex),
            "actor_id": str(event.get("actor_id") or "system"),
            "actor_kind": str(event.get("actor_kind") or "SYSTEM"),
            "context_id": str(event.get("context_id") or "system"),
            "status": str(event.get("status") or "STARTED"),
            "input_bindings": list(event.get("input_bindings") or []),
            "output_bindings": list(event.get("output_bindings") or []),
            "generated_at": generated_at,
            "reason": str(event.get("reason") or "unspecified"),
        }
    )
    normalized.pop("event_sha256", None)
    normalized["event_sha256"] = event_digest(normalized)
    _validate_event_shape(normalized)
    record_path = paths["events"] / _event_record_name(normalized)
    _append_journal_line(paths, normalized)
    _write_json_new(record_path, normalized)
    return normalized


def _append_journal_line(paths: dict[str, Path], event: dict[str, Any]) -> None:
    line = (canonical_json(event) + "\n").encode("utf-8")
    descriptor = os.open(paths["journal"], os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        with os.fdopen(descriptor, "ab", closefd=True) as stream:
            stream.write(line)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        raise


def append_event(workspace: Path | str, event: dict[str, Any], expected_revision: int) -> dict[str, Any]:
    paths = ensure_workspace(workspace)
    with _workspace_lock(paths):
        return _append_event_locked(paths, event, expected_revision)


def _read_lease(paths: dict[str, Path]) -> dict[str, Any] | None:
    if not paths["lease"].exists():
        return None
    lease = _load_json(paths["lease"])
    if not isinstance(lease, dict):
        raise RuntimeError("LEASE_RECORD_INVALID")
    for key in ("owner_id", "token", "acquired_at", "expires_at"):
        if not isinstance(lease.get(key), str) or not lease[key]:
            raise RuntimeError(f"LEASE_RECORD_INVALID:{key}")
    _parse_timestamp(lease["acquired_at"])
    _parse_timestamp(lease["expires_at"])
    return lease


def _require_lease(workspace: Path | str, owner_id: str, token: str | None) -> dict[str, Any]:
    paths = ensure_workspace(workspace)
    lease = _read_lease(paths)
    if lease is None:
        raise RuntimeError("LEASE_REQUIRED")
    if lease.get("owner_id") != owner_id or not token or lease.get("token") != token:
        raise RuntimeError("LEASE_TOKEN_MISMATCH")
    if _parse_timestamp(str(lease["expires_at"])) <= _now():
        raise RuntimeError("LEASE_EXPIRED_RECOVERY_REQUIRED")
    return lease


def acquire_lease(workspace: Path | str, owner_id: str, duration_seconds: int = 300, recover_expired: bool = False) -> dict[str, Any]:
    if not owner_id:
        raise RuntimeError("LEASE_OWNER_REQUIRED")
    if duration_seconds < 30:
        raise RuntimeError("LEASE_DURATION_TOO_SHORT")
    paths = ensure_workspace(workspace)
    with _workspace_lock(paths):
        existing: dict[str, Any] | None = None
        if paths["lease"].exists():
            existing = _load_json(paths["lease"])
            expires_at = _parse_timestamp(str(existing.get("expires_at")))
            if expires_at > _now():
                raise RuntimeError(f"LEASE_HELD:{existing.get('owner_id', 'unknown')}")
            if not recover_expired:
                raise RuntimeError("LEASE_EXPIRED_RECOVERY_REQUIRED")
        acquired = _now()
        lease = {
            "owner_id": owner_id,
            "token": uuid.uuid4().hex,
            "acquired_at": _timestamp(acquired),
            "expires_at": _timestamp(acquired + timedelta(seconds=duration_seconds)),
        }
        _write_json_atomic(paths["lease"], lease)
        return lease


def release_lease(workspace: Path | str, owner_id: str, token: str) -> None:
    paths = ensure_workspace(workspace)
    with _workspace_lock(paths):
        if not paths["lease"].exists():
            return
        lease = _load_json(paths["lease"])
        if lease.get("owner_id") != owner_id or lease.get("token") != token:
            raise RuntimeError("LEASE_TOKEN_MISMATCH")
        paths["lease"].unlink()


def write_snapshot(workspace: Path | str, registry: dict[str, Any]) -> dict[str, Any]:
    paths = ensure_workspace(workspace)
    state = rebuild_state(workspace, registry)
    if paths["lease"].exists():
        state["lease"] = _load_json(paths["lease"])
    _write_json_atomic(paths["state"], state)
    return state


def read_snapshot(workspace: Path | str) -> dict[str, Any]:
    paths = ensure_workspace(workspace)
    return _load_json(paths["state"])


def load_json_file(path: Path | str) -> Any:
    return _load_json(Path(path))


def _registry_hash(registry: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(registry).encode("utf-8")).hexdigest()


def _require_hash(value: Any, label: str) -> str:
    if not _is_hash(value):
        raise RuntimeError(f"{label}_INVALID")
    return str(value)


def _normalize_fingerprints(payload: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    supplied = payload.get("fingerprints", {})
    if not isinstance(supplied, dict):
        raise RuntimeError("FINGERPRINTS_INVALID")
    fingerprints = {
        "skill_sha256": _require_hash(supplied.get("skill_sha256"), "SKILL_FINGERPRINT"),
        "schema_bundle_sha256": _require_hash(supplied.get("schema_bundle_sha256"), "SCHEMA_BUNDLE_FINGERPRINT"),
        "gate_registry_sha256": _registry_hash(registry),
        "script_fingerprint": str(supplied.get("script_fingerprint", "unbound")),
        "runtime_fingerprint": str(supplied.get("runtime_fingerprint", "unbound")),
        "office_fingerprint": str(supplied.get("office_fingerprint", "unbound")),
        "font_fingerprint": str(supplied.get("font_fingerprint", "unbound")),
        "artifact_tool_fingerprint": str(supplied.get("artifact_tool_fingerprint", "unbound")),
        "asr_runtime_fingerprint": supplied.get("asr_runtime_fingerprint"),
    }
    if any(not value.strip() for key, value in fingerprints.items() if key != "asr_runtime_fingerprint" and isinstance(value, str)):
        raise RuntimeError("FINGERPRINT_VALUE_EMPTY")
    if fingerprints["asr_runtime_fingerprint"] is not None and not isinstance(fingerprints["asr_runtime_fingerprint"], str):
        raise RuntimeError("ASR_FINGERPRINT_INVALID")
    return fingerprints


def _normalize_capability_binding(workspace: Path | str, payload: dict[str, Any]) -> dict[str, Any] | None:
    supplied = payload.get("capability_binding")
    if supplied is not None and not isinstance(supplied, dict):
        raise RuntimeError("CAPABILITY_BINDING_INVALID")
    report_path = supplied.get("path") if isinstance(supplied, dict) else None
    report_path = report_path or payload.get("capability_report_path")
    if not report_path:
        candidate = workspace_paths(workspace)["root"] / "capability-report.json"
        if candidate.is_file():
            report_path = str(candidate)
    if not report_path:
        return None
    binding = _build_capability_binding(workspace, str(report_path))
    if isinstance(supplied, dict):
        for key in ("sha256", "probe_id", "fingerprint", "ttl_expires_at", "status"):
            if key in supplied and supplied[key] != binding[key]:
                raise RuntimeError(f"CAPABILITY_BINDING_{key.upper()}_MISMATCH")
    return binding


def initialize_run(workspace: Path | str, registry: dict[str, Any], payload: dict[str, Any], owner_id: str, lease_duration_seconds: int) -> dict[str, Any]:
    paths = ensure_workspace(workspace)
    registry_findings = validate_registry(registry)
    if any(finding.get("severity") == "P0" for finding in registry_findings):
        raise RuntimeError("REGISTRY_INVALID:" + ";".join(finding["code"] for finding in registry_findings))
    if paths["journal"].exists() or paths["run_manifest"].exists():
        raise RuntimeError("RUN_ALREADY_INITIALIZED")
    if not isinstance(payload, dict):
        raise RuntimeError("INIT_PAYLOAD_MUST_BE_OBJECT")
    run_id = payload.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise RuntimeError("RUN_ID_REQUIRED")
    profile = payload.get("active_profile", registry.get("default_profile"))
    if profile not in PROFILES or profile not in registry.get("profiles", []):
        raise RuntimeError("ACTIVE_PROFILE_INVALID")
    source_snapshot_hash = _require_hash(payload.get("source_snapshot_hash"), "SOURCE_SNAPSHOT_HASH")
    job_contract_hash = _require_hash(payload.get("job_contract_hash"), "JOB_CONTRACT_HASH")
    fingerprints = _normalize_fingerprints(payload, registry)
    capability_binding = _normalize_capability_binding(paths["root"], payload)
    job_contract_path = payload.get("job_contract_path")
    if job_contract_path:
        candidate = Path(str(job_contract_path)).expanduser()
        if not candidate.is_absolute():
            candidate = paths["root"] / candidate
        candidate = Path(os.path.abspath(str(candidate)))
        if not candidate.is_file() or _is_reparse(candidate):
            raise RuntimeError(f"JOB_CONTRACT_PATH_INVALID:{candidate}")
        _assert_safe_ancestors(candidate)
        if _sha256_file(candidate) != job_contract_hash:
            raise RuntimeError("JOB_CONTRACT_PATH_HASH_MISMATCH")
        job_contract_binding_path = str(candidate)
    else:
        job_contract_binding_path = f"sha256://job-contract/{job_contract_hash}"
    lease = acquire_lease(workspace, owner_id, lease_duration_seconds)
    manifest = {
        "schema_version": "1.0",
        "run_id": run_id,
        "active_profile": profile,
        "source_snapshot_hash": source_snapshot_hash,
        "job_contract_hash": job_contract_hash,
        "fingerprints": fingerprints,
        "registry_sha256": _registry_hash(registry),
        "created_at": _timestamp(),
    }
    if capability_binding is not None:
        manifest["capability_binding"] = capability_binding
    try:
        _write_json_new(paths["run_manifest"], manifest)
        event = append_event(
            workspace,
            {
                "run_id": run_id,
                "gate_id": "G0_JOB_CONTRACT",
                "status": "PASS",
                "actor_id": owner_id,
                "actor_kind": "MANAGER",
                "context_id": owner_id,
                "reason": "run initialized with validated job contract",
                "output_bindings": [{
                    "path": job_contract_binding_path,
                    "sha256": job_contract_hash,
                    "schema": "job-contract.schema.json",
                }],
                "metadata": {
                    "active_profile": profile,
                    "source_snapshot_hash": source_snapshot_hash,
                    "job_contract_hash": job_contract_hash,
                    "fingerprints": fingerprints,
                },
            },
            expected_revision=0,
        )
        state = write_snapshot(workspace, registry)
        state["lease"] = lease
        return state | {"event": event}
    except BaseException:
        try:
            release_lease(workspace, owner_id, lease["token"])
        finally:
            paths["run_manifest"].unlink(missing_ok=True)
        raise


def _auto_skip_profile_exclusions(workspace: Path | str, registry: dict[str, Any], owner_id: str, lease_token: str) -> dict[str, Any]:
    max_skips = len(_registry_gates(registry)) + 1
    for _ in range(max_skips):
        _require_lease(workspace, owner_id, lease_token)
        state = rebuild_state(workspace, registry)
        gate_id = state.get("next_gate")
        if not gate_id:
            return state
        gate = next((item for item in _registry_gates(registry) if item.get("gate_id") == gate_id), None)
        if gate is None or _is_gate_in_profile(gate, state["active_profile"]):
            return state
        if not _gate_is_skippable(gate, state["active_profile"]):
            raise RuntimeError(f"GATE_NOT_AVAILABLE_FOR_PROFILE:{gate_id}")
        submission = {
            "schema_version": "1.0",
            "run_id": state["run_id"],
            "gate_id": gate_id,
            "attempt_id": uuid.uuid4().hex,
            "producer": "orchestrator",
            "actor_context_id": owner_id,
            "input_artifacts": [],
            "output_artifacts": [],
            "dependency_hashes": {
                dependency: state["gates"][dependency]["receipt_sha256"]
                for dependency in gate.get("dependencies", [])
                if state["gates"].get(dependency, {}).get("receipt_sha256")
            },
            "tool_fingerprint": "orchestrator",
            "status": "SKIPPED",
            "findings": [],
            "generated_at": _timestamp(),
            "metadata": {"skip_reason": gate["skip_policy"]["reason"], "predicate": "PROFILE_NOT_TARGET"},
        }
        findings = validate_submission(workspace, submission, registry)
        if findings:
            raise RuntimeError("AUTO_SKIP_INVALID:" + ";".join(finding["code"] for finding in findings))
        append_event(
            workspace,
            {
                "run_id": state["run_id"],
                "gate_id": gate_id,
                "attempt_id": submission["attempt_id"],
                "actor_id": owner_id,
                "actor_kind": "SYSTEM",
                "context_id": owner_id,
                "status": "SKIPPED",
                "reason": submission["metadata"]["skip_reason"],
                "metadata": submission["metadata"],
            },
            expected_revision=state["state_revision"],
        )
    raise RuntimeError("PROFILE_SKIP_LOOP")


def _dependency_hashes(state: dict[str, Any], gate: dict[str, Any]) -> dict[str, str]:
    return {
        dependency: state["gates"][dependency]["receipt_sha256"]
        for dependency in gate.get("dependencies", [])
        if state["gates"].get(dependency, {}).get("receipt_sha256")
    }


def _submission_event(workspace: Path | str, submission: dict[str, Any]) -> dict[str, Any]:
    state = rebuild_state(workspace, load_json_file(Path(workspace) / "control" / "registry.json")) if False else None
    metadata = submission.get("metadata") if isinstance(submission.get("metadata"), dict) else {}
    actor_kind = metadata.get("actor_kind") or ("VALIDATOR" if submission.get("review_context_id") else "SPECIALIST")
    if actor_kind not in ACTOR_KINDS:
        actor_kind = "SPECIALIST"
    return {
        "run_id": submission["run_id"],
        "gate_id": submission["gate_id"],
        "attempt_id": submission["attempt_id"],
        "actor_id": submission["producer"],
        "actor_kind": actor_kind,
        "context_id": submission["actor_context_id"],
        "status": submission["status"],
        "reason": metadata.get("reason") or f"gate submission {submission['status']}",
        "input_bindings": [
            {key: artifact[key] for key in ("path", "sha256", "schema") if key in artifact}
            for artifact in submission.get("input_artifacts", [])
        ],
        "output_bindings": [
            {key: artifact[key] for key in ("path", "sha256", "schema") if key in artifact}
            for artifact in submission.get("output_artifacts", [])
        ],
        "metadata": metadata,
    }


def _capability_unverified_only(findings: list[dict[str, str]]) -> bool:
    return bool(findings) and all(
        finding.get("severity") == "P1" and finding.get("code") in CAPABILITY_UNVERIFIED_CODES
        for finding in findings
    )


def submit_gate(workspace: Path | str, registry: dict[str, Any], submission: dict[str, Any], owner_id: str, lease_token: str) -> dict[str, Any]:
    _require_lease(workspace, owner_id, lease_token)
    _auto_skip_profile_exclusions(workspace, registry, owner_id, lease_token)
    findings = validate_submission(workspace, submission, registry, quarantine_invalid=True)
    if findings:
        if submission.get("status") == "UNVERIFIED" and _capability_unverified_only(findings):
            state = rebuild_state(workspace, registry)
            enriched = dict(submission)
            metadata = dict(submission.get("metadata") or {})
            metadata["validation_findings"] = findings
            enriched["metadata"] = metadata
            _require_lease(workspace, owner_id, lease_token)
            event = append_event(workspace, _submission_event(workspace, enriched), expected_revision=state["state_revision"])
            result_state = write_snapshot(workspace, registry)
            return result_state | {"event": event, "findings": findings}
        return {"status": "BLOCKED", "findings": findings}
    state = rebuild_state(workspace, registry)
    _require_lease(workspace, owner_id, lease_token)
    gate_id = submission.get("gate_id")
    event_submission = submission
    capability_binding = None
    if gate_id == "G1_CAPABILITY_SECURITY" and submission.get("status") in {"PASS", "UNVERIFIED"}:
        capability_binding, binding_findings = _capability_submission_binding(ensure_workspace(workspace)["root"], submission)
        if binding_findings:
            return {"status": "BLOCKED", "findings": binding_findings}
        existing = _capability_binding(workspace)
        if existing:
            identity_keys = ("path", "sha256", "probe_id", "fingerprint", "ttl_expires_at", "status")
            if not all(existing.get(key) == capability_binding.get(key) for key in identity_keys):
                return {"status": "BLOCKED", "findings": [_finding("P0", "CAPABILITY_BINDING_CONFLICT", "G1 report differs from existing binding")]}
        enriched = dict(submission)
        metadata = dict(submission.get("metadata") or {})
        metadata["capability_binding"] = capability_binding
        enriched["metadata"] = metadata
        event_submission = enriched
    event = append_event(workspace, _submission_event(workspace, event_submission), expected_revision=state["state_revision"])
    if capability_binding:
        _cache_capability_binding(workspace, capability_binding)
    result_state = write_snapshot(workspace, registry)
    return result_state | {"event": event}


def skip_gate(workspace: Path | str, registry: dict[str, Any], payload: dict[str, Any], owner_id: str, lease_token: str) -> dict[str, Any]:
    state = _auto_skip_profile_exclusions(workspace, registry, owner_id, lease_token)
    gate_id = payload.get("gate_id", state.get("next_gate"))
    gate = next((item for item in _registry_gates(registry) if item.get("gate_id") == gate_id), None)
    if gate is None:
        raise RuntimeError("SKIP_GATE_UNKNOWN")
    submission = {
        "schema_version": "1.0",
        "run_id": state["run_id"],
        "gate_id": gate_id,
        "attempt_id": str(payload.get("attempt_id") or uuid.uuid4().hex),
        "producer": str(payload.get("producer") or owner_id),
        "actor_context_id": owner_id,
        "input_artifacts": list(payload.get("input_artifacts") or []),
        "output_artifacts": [],
        "dependency_hashes": payload.get("dependency_hashes") or _dependency_hashes(state, gate),
        "tool_fingerprint": str(payload.get("tool_fingerprint") or "orchestrator"),
        "status": "SKIPPED",
        "findings": [],
        "generated_at": str(payload.get("generated_at") or _timestamp()),
        "metadata": {
            "skip_reason": str(payload.get("skip_reason") or payload.get("reason") or "approved registry skip"),
            "predicate": str(payload.get("predicate") or "PROFILE_NOT_TARGET"),
        },
    }
    result = submit_gate(workspace, registry, submission, owner_id, lease_token)
    if result.get("status") == "BLOCKED":
        raise RuntimeError("SKIP_NOT_ALLOWED:" + ";".join(finding["code"] for finding in result["findings"]))
    return result


def invalidate_gates(workspace: Path | str, registry: dict[str, Any], payload: dict[str, Any], owner_id: str, lease_token: str) -> dict[str, Any]:
    _require_lease(workspace, owner_id, lease_token)
    state = rebuild_state(workspace, registry)
    requested_gate = payload.get("gate_id")
    requested_keys = set(payload.get("invalidation_keys") or [])
    gate_by_id = {gate["gate_id"]: gate for gate in _registry_gates(registry)}
    if requested_gate not in gate_by_id and not requested_keys:
        raise RuntimeError("INVALIDATION_TARGET_REQUIRED")
    affected: set[str] = set()
    if requested_gate in gate_by_id:
        affected.add(str(requested_gate))
    if requested_keys:
        affected.update(gate_id for gate_id, gate in gate_by_id.items() if requested_keys.intersection(gate.get("invalidation_keys", [])))
    changed = True
    while changed:
        changed = False
        for gate_id, gate in gate_by_id.items():
            if gate_id not in affected and any(dependency in affected for dependency in gate.get("dependencies", [])):
                affected.add(gate_id)
                changed = True
    invalidated = []
    for gate in _registry_gates(registry):
        gate_id = gate["gate_id"]
        if gate_id not in affected or state["gates"].get(gate_id, {}).get("status") == "STALE":
            continue
        current = rebuild_state(workspace, registry)
        append_event(
            workspace,
            {
                "run_id": current["run_id"],
                "gate_id": gate_id,
                "actor_id": owner_id,
                "actor_kind": "MANAGER",
                "context_id": owner_id,
                "status": "STALE",
                "reason": str(payload.get("reason") or "dependency invalidated"),
                "metadata": {"invalidation_keys": sorted(requested_keys), "root_gate_id": requested_gate},
            },
            expected_revision=current["state_revision"],
        )
        invalidated.append(gate_id)
    return write_snapshot(workspace, registry) | {"invalidated_gates": invalidated}


def recover_run(workspace: Path | str, registry: dict[str, Any], owner_id: str, lease_token: str | None, lease_duration_seconds: int, recover_expired: bool) -> dict[str, Any]:
    paths = ensure_workspace(workspace)
    current_lease = _read_lease(paths)
    lease_taken_over = False
    if current_lease is not None:
        expires = _parse_timestamp(current_lease["expires_at"])
        if expires > _now():
            if current_lease.get("owner_id") != owner_id:
                raise RuntimeError("LEASE_HELD:" + str(current_lease.get("owner_id")))
            if not lease_token or current_lease.get("token") != lease_token:
                raise RuntimeError("LEASE_TOKEN_MISMATCH")
            lease = current_lease
        else:
            lease = acquire_lease(workspace, owner_id, lease_duration_seconds, recover_expired=recover_expired)
            lease_taken_over = True
    else:
        lease = acquire_lease(workspace, owner_id, lease_duration_seconds)
    recovery = recover_workspace(workspace, registry)
    state = rebuild_state(workspace, registry)
    recoverable = next((gate_id for gate_id, gate_state in state["gates"].items() if gate_state.get("status") in {"RUNNING", "STALE", "QUARANTINED"} and gate_id in {item["gate_id"] for item in _registry_gates(registry) if _is_gate_in_profile(item, state["active_profile"])}), None)
    event = None
    if recoverable and state["state_revision"] > 0:
        event = append_event(
            workspace,
            {
                "run_id": state["run_id"],
                "gate_id": recoverable,
                "actor_id": owner_id,
                "actor_kind": "SYSTEM",
                "context_id": owner_id,
                "status": "RECOVERED",
                "reason": "recovery receipt accepted; gate returned to pending",
                "metadata": {
                    "recovery_receipt_path": recovery.get("receipt_path"),
                    "lease_taken_over": lease_taken_over,
                    "promoted_count": recovery.get("promoted_count", 0),
                    "restored_count": recovery.get("restored_count", 0),
                    "quarantined_count": recovery.get("quarantined_count", 0),
                },
            },
            expected_revision=state["state_revision"],
        )
    elif lease_taken_over and state["state_revision"] > 0:
        active_gates = [item["gate_id"] for item in _registry_gates(registry) if _is_gate_in_profile(item, state["active_profile"])]
        anchor_gate = state.get("next_gate") or (active_gates[-1] if active_gates else "G0_JOB_CONTRACT")
        event = append_event(
            workspace,
            {
                "run_id": state["run_id"],
                "gate_id": anchor_gate,
                "actor_id": owner_id,
                "actor_kind": "SYSTEM",
                "context_id": owner_id,
                "status": "RECOVERED",
                "reason": "expired lease taken over; pipeline state unchanged",
                "metadata": {
                    "lease_taken_over": True,
                    "lease_takeover_only": True,
                    "recovery_receipt_path": recovery.get("receipt_path"),
                },
            },
            expected_revision=state["state_revision"],
        )
    final_state = write_snapshot(workspace, registry)
    return {"recovery": recovery, "lease": lease, "lease_taken_over": lease_taken_over, "state": final_state, "event": event}


def _load_payload(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    payload = load_json_file(path)
    if not isinstance(payload, dict):
        raise RuntimeError("PAYLOAD_MUST_BE_OBJECT")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Make Slide Pro G0-G15 orchestrator")
    parser.add_argument("--action", required=True, choices=["init", "status", "next", "submit", "skip", "invalidate", "recover"])
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--payload", type=str)
    parser.add_argument("--owner-id", default="make-slide-pro-manager")
    parser.add_argument("--lease-token")
    parser.add_argument("--lease-duration-seconds", type=int, default=300)
    parser.add_argument("--recover-expired", action="store_true")
    args = parser.parse_args(argv)
    try:
        registry = load_json_file(args.registry)
        if not isinstance(registry, dict):
            raise RuntimeError("REGISTRY_MUST_BE_OBJECT")
        registry_findings = validate_registry(registry, args.registry.parent.parent.parent / "schemas")
        if any(finding.get("severity") == "P0" for finding in registry_findings):
            raise RuntimeError("REGISTRY_INVALID:" + ";".join(finding["code"] for finding in registry_findings))
        payload = _load_payload(args.payload)
        if args.action == "init":
            result = initialize_run(args.workspace, registry, payload, args.owner_id, args.lease_duration_seconds)
        elif args.action == "status":
            result = rebuild_state(args.workspace, registry)
        elif args.action == "next":
            _require_lease(args.workspace, args.owner_id, args.lease_token)
            result = _auto_skip_profile_exclusions(args.workspace, registry, args.owner_id, str(args.lease_token))
        elif args.action == "submit":
            result = submit_gate(args.workspace, registry, payload, args.owner_id, str(args.lease_token or ""))
        elif args.action == "skip":
            result = skip_gate(args.workspace, registry, payload, args.owner_id, str(args.lease_token or ""))
        elif args.action == "invalidate":
            result = invalidate_gates(args.workspace, registry, payload, args.owner_id, str(args.lease_token or ""))
        else:
            result = recover_run(args.workspace, registry, args.owner_id, args.lease_token, args.lease_duration_seconds, args.recover_expired)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if isinstance(result, dict) and result.get("status") == "BLOCKED":
            return 2
        if isinstance(result, dict) and result.get("status") == "UNVERIFIED":
            return 3
        return 0
    except RuntimeError as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}, ensure_ascii=False), file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
