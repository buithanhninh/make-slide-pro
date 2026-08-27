from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = SKILL_ROOT / "schemas"
REGISTRY_PATH = SKILL_ROOT / "assets" / "pipeline" / "gate-registry.json"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))


class V62ControlPlaneTests(unittest.TestCase):
    def test_v62_control_plane_entrypoints_exist(self) -> None:
        required = [
            "scripts/orchestrator_core.py",
            "scripts/validate-orchestrator-state.py",
            "scripts/rebuild-orchestrator-state.py",
            "scripts/orchestrate-gates.ps1",
            "schemas/gate-registry.schema.json",
            "schemas/orchestrator-event.schema.json",
            "schemas/orchestrator-state.schema.json",
            "schemas/gate-submission.schema.json",
            "schemas/approval-record.schema.json",
            "schemas/run-policy.schema.json",
            "schemas/prototype-review.schema.json",
            "schemas/capability-report.schema.json",
            "schemas/quality-assessment.schema.json",
            "assets/pipeline/gate-registry.json",
            "tests/corpus/manifest.json",
        ]
        missing = [item for item in required if not (SKILL_ROOT / item).is_file()]
        self.assertEqual([], missing)

    def test_registry_contains_complete_profile_aware_dag(self) -> None:
        payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        self.assertEqual("1.0", payload["schema_version"])
        gate_ids = [gate["gate_id"] for gate in payload["gates"]]
        self.assertEqual(
            [
                "G0_JOB_CONTRACT",
                "G1_CAPABILITY_SECURITY",
                "G2_SOURCE_INVENTORY",
                "G3_FORMAT_ADAPTERS",
                "G4_CANONICAL_EVIDENCE",
                "G5_RECONCILIATION",
                "G6_FIDELITY_COVERAGE",
                "G7_NARRATIVE_ARCHITECTURE",
                "G8_SLIDE_BLUEPRINT",
                "G9_ART_DIRECTION",
                "G10_REPRESENTATIVE_PROTOTYPE",
                "G11_STATIC_PRODUCTION",
                "G12_STATIC_CERTIFICATION",
                "G13_NATIVE_MOTION",
                "G14_STATIC_QA",
                "G14_MOTION_QA",
                "G15_STATIC_RELEASE",
                "G15_MOTION_RELEASE",
            ],
            gate_ids,
        )

    def test_append_event_chains_and_rejects_stale_revision(self) -> None:
        from orchestrator_core import append_event, rebuild_state

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            first = append_event(
                workspace,
                {
                    "run_id": "run-001",
                    "gate_id": "G0_JOB_CONTRACT",
                    "status": "PASS",
                    "actor_id": "manager",
                    "actor_kind": "MANAGER",
                    "context_id": "ctx-manager",
                    "reason": "contract accepted",
                },
                expected_revision=0,
            )
            self.assertEqual(1, first["state_revision"])
            self.assertRegex(first["event_sha256"], r"^[0-9a-f]{64}$")
            with self.assertRaisesRegex(RuntimeError, "STATE_REVISION_CONFLICT"):
                append_event(
                    workspace,
                    {
                        "run_id": "run-001",
                        "gate_id": "G1_CAPABILITY_SECURITY",
                        "status": "PASS",
                        "actor_id": "manager",
                        "actor_kind": "MANAGER",
                        "context_id": "ctx-manager",
                        "reason": "stale writer",
                    },
                    expected_revision=0,
                )
            state = rebuild_state(workspace, {"gates": []})
            self.assertEqual(1, state["state_revision"])
            self.assertEqual("PASS", state["gates"]["G0_JOB_CONTRACT"]["status"])

    def test_event_hash_changes_when_payload_changes(self) -> None:
        from orchestrator_core import canonical_json, event_digest

        payload = {"b": 2, "a": 1}
        self.assertEqual(canonical_json(payload), '{"a":1,"b":2}')
        first = event_digest(payload)
        changed = event_digest({"a": 1, "b": 3})
        self.assertNotEqual(first, changed)
        self.assertEqual(64, len(first))

    def test_rebuilt_state_uses_schema_compatible_nullable_lease(self) -> None:
        from orchestrator_core import rebuild_state

        with tempfile.TemporaryDirectory() as temporary:
            state = rebuild_state(Path(temporary), json.loads(REGISTRY_PATH.read_text(encoding="utf-8")))
        self.assertIsNone(state["lease"])
        schema = json.loads((SCHEMAS / "orchestrator-state.schema.json").read_text(encoding="utf-8"))
        self.assertIn("anyOf", schema["properties"]["lease"])

    def test_registry_semantic_validator_rejects_bad_dag(self) -> None:
        from orchestrator_core import validate_registry

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        registry["gates"][1]["dependencies"] = ["G1_CAPABILITY_SECURITY"]
        findings = validate_registry(registry)
        codes = {finding["code"] for finding in findings}
        self.assertIn("REGISTRY_CYCLE", codes)

    def test_submission_validator_rejects_artifact_outside_workspace(self) -> None:
        from orchestrator_core import validate_submission

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            outside = workspace.parent / "outside-artifact.txt"
            outside.write_text("not inside", encoding="utf-8")
            submission = {
                "schema_version": "1.0",
                "run_id": "run-001",
                "gate_id": "G1_CAPABILITY_SECURITY",
                "attempt_id": "attempt-001",
                "producer": "test",
                "actor_context_id": "ctx",
                "input_artifacts": [],
                "output_artifacts": [{
                    "path": str(outside),
                    "sha256": hashlib.sha256(b"not inside").hexdigest(),
                    "kind": "report",
                }],
                "dependency_hashes": {},
                "tool_fingerprint": "tool-v1",
                "status": "PASS",
                "findings": [],
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
            findings = validate_submission(workspace, submission, json.loads(REGISTRY_PATH.read_text(encoding="utf-8")))
        self.assertIn("ARTIFACT_OUTSIDE_WORKSPACE", {finding["code"] for finding in findings})

    def test_orchestrator_cli_initializes_and_advances_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "run"
            init_payload = workspace.parent / "init.json"
            init_payload.write_text(json.dumps({
                "run_id": "run-cli-001",
                "active_profile": "FINAL_RELEASE_STATIC",
                "source_snapshot_hash": "a" * 64,
                "job_contract_hash": "b" * 64,
                "fingerprints": {
                    "skill_sha256": "c" * 64,
                    "schema_bundle_sha256": "d" * 64,
                    "gate_registry_sha256": "e" * 64,
                    "script_fingerprint": "script-v1",
                    "runtime_fingerprint": "runtime-v1",
                    "office_fingerprint": "office-v1",
                    "font_fingerprint": "font-v1",
                    "artifact_tool_fingerprint": "artifact-v1",
                    "asr_runtime_fingerprint": None,
                },
            }), encoding="utf-8")
            wrapper = SKILL_ROOT / "scripts" / "orchestrate-gates.ps1"
            init = subprocess.run(
                ["pwsh", "-NoLogo", "-NoProfile", "-File", str(wrapper), "-Action", "init", "-Workspace", str(workspace), "-RegistryPath", str(REGISTRY_PATH), "-PayloadPath", str(init_payload)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, init.returncode, init.stderr)
            initialized = json.loads(init.stdout)
            self.assertEqual("G1_CAPABILITY_SECURITY", initialized["next_gate"])
            token = initialized["lease"]["token"]
            next_result = subprocess.run(
                ["pwsh", "-NoLogo", "-NoProfile", "-File", str(wrapper), "-Action", "next", "-Workspace", str(workspace), "-RegistryPath", str(REGISTRY_PATH), "-OwnerId", "make-slide-pro-manager", "-LeaseToken", token],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, next_result.returncode, next_result.stderr)
            self.assertEqual("G1_CAPABILITY_SECURITY", json.loads(next_result.stdout)["next_gate"])

    def test_recovery_quarantines_orphan_event_record(self) -> None:
        from orchestrator_core import append_event, recover_workspace

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            append_event(workspace, {
                "run_id": "run-recover-001",
                "gate_id": "G0_JOB_CONTRACT",
                "status": "PASS",
                "actor_id": "manager",
                "actor_kind": "MANAGER",
                "context_id": "ctx",
                "reason": "accepted",
            }, expected_revision=0)
            orphan = workspace / "events" / "99999999999999999999-orphan.json"
            orphan.write_text(json.dumps({"event_id": "orphan"}), encoding="utf-8")
            result = recover_workspace(workspace, json.loads(REGISTRY_PATH.read_text(encoding="utf-8")))
            self.assertEqual(1, result["quarantined_count"])
            self.assertTrue(any((workspace / "quarantine").iterdir()))


class V62HardeningTests(unittest.TestCase):
    def test_lease_held_blocks_second_init(self) -> None:
        from orchestrator_core import initialize_run, acquire_lease

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "run"
            payload = {
                "run_id": "run-lease-001",
                "active_profile": "FINAL_RELEASE_STATIC",
                "source_snapshot_hash": "a" * 64,
                "job_contract_hash": "b" * 64,
                "fingerprints": {
                    "skill_sha256": "c" * 64,
                    "schema_bundle_sha256": "d" * 64,
                    "gate_registry_sha256": "e" * 64,
                    "script_fingerprint": "s", "runtime_fingerprint": "r",
                    "office_fingerprint": "o", "font_fingerprint": "f",
                    "artifact_tool_fingerprint": "at", "asr_runtime_fingerprint": None,
                },
            }
            initialize_run(workspace, registry, payload, "owner-a", 300)
            with self.assertRaisesRegex(RuntimeError, "RUN_ALREADY_INITIALIZED|LEASE_HELD"):
                initialize_run(workspace, registry, {**payload, "run_id": "run-lease-002"}, "owner-b", 300)

    def test_stale_gate_re_entry_after_invalidation(self) -> None:
        from orchestrator_core import (
            initialize_run, append_event, rebuild_state,
            invalidate_gates, _require_lease,
        )

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "run"
            payload = {
                "run_id": "run-stale-001",
                "active_profile": "FINAL_RELEASE_STATIC",
                "source_snapshot_hash": "a" * 64,
                "job_contract_hash": "b" * 64,
                "fingerprints": {
                    "skill_sha256": "c" * 64, "schema_bundle_sha256": "d" * 64,
                    "gate_registry_sha256": "e" * 64, "script_fingerprint": "s",
                    "runtime_fingerprint": "r", "office_fingerprint": "o",
                    "font_fingerprint": "f", "artifact_tool_fingerprint": "at",
                    "asr_runtime_fingerprint": None,
                },
            }
            state = initialize_run(workspace, registry, payload, "owner", 300)
            token = state["lease"]["token"]
            current = rebuild_state(workspace, registry)
            next_gate = current["next_gate"]
            self.assertIsNotNone(next_gate)
            append_event(workspace, {
                "run_id": current["run_id"], "gate_id": next_gate,
                "status": "PASS", "actor_id": "owner", "actor_kind": "SPECIALIST",
                "context_id": "owner", "reason": "completed",
            }, expected_revision=current["state_revision"])
            before = rebuild_state(workspace, registry)
            self.assertEqual("PASS", before["gates"][next_gate]["status"])
            result = invalidate_gates(workspace, registry, {
                "gate_id": next_gate, "reason": "test invalidation",
            }, "owner", token)
            self.assertIn(next_gate, result["invalidated_gates"])
            after = rebuild_state(workspace, registry)
            self.assertEqual("STALE", after["gates"][next_gate]["status"])

    def test_expired_lease_recovery_returns_new_token(self) -> None:
        from orchestrator_core import acquire_lease, release_lease, _now, _timestamp
        from datetime import timedelta

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            lease = acquire_lease(workspace, "owner-a", 30)
            lease_path = Path(workspace) / "control" / "lease.json"
            expired = json.loads(lease_path.read_text(encoding="utf-8"))
            expired["expires_at"] = _timestamp(_now() - timedelta(seconds=10))
            lease_path.write_text(json.dumps(expired), encoding="utf-8")
            new_lease = acquire_lease(workspace, "owner-b", 300, recover_expired=True)
            self.assertNotEqual(lease["token"], new_lease["token"])
            self.assertEqual("owner-b", new_lease["owner_id"])

    def test_duplicate_event_id_rejected(self) -> None:
        from orchestrator_core import append_event

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            first = append_event(workspace, {
                "run_id": "run-dup-001", "gate_id": "G0_JOB_CONTRACT",
                "status": "PASS", "actor_id": "mgr", "actor_kind": "MANAGER",
                "context_id": "mgr", "reason": "ok",
            }, expected_revision=0)
            with self.assertRaisesRegex(RuntimeError, "EVENT_ID_DUPLICATE"):
                append_event(workspace, {
                    "run_id": "run-dup-001", "gate_id": "G1_CAPABILITY_SECURITY",
                    "event_id": first["event_id"],
                    "status": "PASS", "actor_id": "mgr", "actor_kind": "MANAGER",
                    "context_id": "mgr", "reason": "dup",
                }, expected_revision=1)

    def test_submission_rejects_critical_finding_on_pass(self) -> None:
        from orchestrator_core import validate_submission

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            submission = {
                "schema_version": "1.0", "run_id": "run-crit-001",
                "gate_id": "G0_JOB_CONTRACT", "attempt_id": "att-001",
                "producer": "test", "actor_context_id": "ctx",
                "input_artifacts": [], "output_artifacts": [{
                    "path": str(workspace / "dummy.json"), "sha256": "a" * 64,
                    "kind": "report", "immutable": True,
                }],
                "dependency_hashes": {}, "tool_fingerprint": "t",
                "status": "PASS",
                "findings": [{"severity": "P0", "code": "DATA_MISMATCH"}],
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
            findings = validate_submission(workspace, submission, registry)
            codes = {f["code"] for f in findings}
            self.assertIn("CRITICAL_FINDING_ON_PASS", codes)

    def test_registry_validator_checks_g10_dependencies(self) -> None:
        from orchestrator_core import validate_registry

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        for gate in registry["gates"]:
            if gate["gate_id"] == "G10_REPRESENTATIVE_PROTOTYPE":
                gate["dependencies"] = ["G8_SLIDE_BLUEPRINT"]
                break
        findings = validate_registry(registry)
        codes = {f["code"] for f in findings}
        self.assertIn("REGISTRY_G10_DEPENDENCIES_INVALID", codes)


class V62HardeningExtendedTests(unittest.TestCase):
    def test_capability_ttl_expired_returns_findings(self) -> None:
        from orchestrator_core import validate_capability_ttl, ensure_workspace, _timestamp, _write_json_new

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "run"
            paths = ensure_workspace(workspace)
            expired = _timestamp(datetime.now(timezone.utc) - timedelta(minutes=10))
            report = {
                "schema_version": "1.0",
                "generated_at": _timestamp(datetime.now(timezone.utc) - timedelta(minutes=70)),
                "status": "PASS",
                "probe_id": "testprobe001",
                "capabilities": {"powerpoint": {"available": True, "evidence": "test"}},
                "fingerprint": "a" * 64,
                "ttl_expires_at": expired,
                "target_path": str(workspace),
                "mode": "AUDIT",
                "profile": "CPU_ONLY",
                "mandatory_ready": True,
                "certification_ceiling": "PASS",
                "office": {"powerpoint": {"available": True, "version": "16"}, "word": {"available": False}, "excel": {"available": False}},
                "runtimes": {"node": {"available": False, "path": None}, "node_modules": {"available": False, "path": None}, "bin_dir": {"available": False, "path": None}, "python": {"available": True, "path": "python"}, "python_probe": {"available": True, "version": "3.11", "faster_whisper": False, "pytesseract": False, "jsonschema": True}, "artifact_tool": {"available": False, "directory_present": False, "importable": False, "path": None, "runtime_modules": None, "error": "n/a"}, "ffmpeg": {"available": False, "path": None}, "ffprobe": {"available": False, "path": None}, "tesseract": {"available": False, "path": None}},
                "hardware": {"nvidia_smi": {"available": False, "path": None}, "cuda_verified": False, "selected_asr_device": "cpu", "selected_asr_compute_type": "int8", "asr_selection_source": "SAFE_DEFAULT"},
                "disk": {"root": "C:\\", "free_bytes": 10000000000, "free_gb": 9.31},
                "issues": [],
            }
            report_path = paths["artifacts"] / "capability-report.json"
            _write_json_new(report_path, report)
            findings = validate_capability_ttl(workspace, registry, "G11_STATIC_PRODUCTION", capability_report_path=report_path)
            codes = {f["code"] for f in findings}
            self.assertIn("CAPABILITY_TTL_EXPIRED", codes)

    def test_wal_journal_first_recovery_promotes_orphan_record(self) -> None:
        from orchestrator_core import append_event, recover_workspace, rebuild_state

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            first = append_event(workspace, {
                "run_id": "run-wal-001", "gate_id": "G0_JOB_CONTRACT",
                "status": "PASS", "actor_id": "mgr", "actor_kind": "MANAGER",
                "context_id": "mgr", "reason": "ok",
            }, expected_revision=0)
            journal_path = workspace / "events" / "events.ndjson"
            journal_lines = journal_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(1, len(journal_lines))
            journal_path.write_text(journal_lines[0] + "\n", encoding="utf-8")
            second = append_event(workspace, {
                "run_id": "run-wal-001", "gate_id": "G1_CAPABILITY_SECURITY",
                "status": "PASS", "actor_id": "mgr", "actor_kind": "MANAGER",
                "context_id": "mgr", "reason": "ok",
            }, expected_revision=1)
            journal_lines = journal_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(journal_lines))
            journal_path.write_text(journal_lines[0] + "\n", encoding="utf-8")
            result = recover_workspace(workspace, json.loads(REGISTRY_PATH.read_text(encoding="utf-8")))
            self.assertEqual(1, result["promoted_count"])
            state = rebuild_state(workspace, json.loads(REGISTRY_PATH.read_text(encoding="utf-8")))
            self.assertEqual(2, state["state_revision"])
            self.assertEqual("PASS", state["gates"]["G1_CAPABILITY_SECURITY"]["status"])

    def test_stale_gate_becomes_pending_after_recovery(self) -> None:
        from orchestrator_core import append_event, rebuild_state

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            append_event(workspace, {
                "run_id": "run-stale-r-001", "gate_id": "G0_JOB_CONTRACT",
                "status": "PASS", "actor_id": "mgr", "actor_kind": "MANAGER",
                "context_id": "mgr", "reason": "ok",
            }, expected_revision=0)
            append_event(workspace, {
                "run_id": "run-stale-r-001", "gate_id": "G1_CAPABILITY_SECURITY",
                "status": "STALE", "actor_id": "mgr", "actor_kind": "MANAGER",
                "context_id": "mgr", "reason": "invalidated",
            }, expected_revision=1)
            state = rebuild_state(workspace, registry)
            self.assertEqual("STALE", state["gates"]["G1_CAPABILITY_SECURITY"]["status"])
            self.assertEqual("STALE", state["status"])
            append_event(workspace, {
                "run_id": "run-stale-r-001", "gate_id": "G1_CAPABILITY_SECURITY",
                "status": "RECOVERED", "actor_id": "sys", "actor_kind": "SYSTEM",
                "context_id": "sys", "reason": "re-entry after invalidation",
            }, expected_revision=2)
            state = rebuild_state(workspace, registry)
            self.assertEqual("PENDING", state["gates"]["G1_CAPABILITY_SECURITY"]["status"])
            self.assertEqual("RUNNING", state["status"])

    def test_state_projection_pass_requires_all_active_completed(self) -> None:
        from orchestrator_core import append_event, rebuild_state

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            append_event(workspace, {
                "run_id": "run-proj-001", "gate_id": "G0_JOB_CONTRACT",
                "status": "PASS", "actor_id": "mgr", "actor_kind": "MANAGER",
                "context_id": "mgr", "reason": "ok",
            }, expected_revision=0)
            state = rebuild_state(workspace, registry)
            self.assertNotEqual("PASS", state["status"])
            self.assertEqual("RUNNING", state["status"])

    def test_lease_takeover_emits_recovered_event(self) -> None:
        from orchestrator_core import initialize_run, recover_run, _now, _timestamp

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "run"
            payload = {
                "run_id": "run-takeover-001",
                "active_profile": "FINAL_RELEASE_STATIC",
                "source_snapshot_hash": "a" * 64,
                "job_contract_hash": "b" * 64,
                "fingerprints": {
                    "skill_sha256": "c" * 64, "schema_bundle_sha256": "d" * 64,
                    "gate_registry_sha256": "e" * 64, "script_fingerprint": "s",
                    "runtime_fingerprint": "r", "office_fingerprint": "o",
                    "font_fingerprint": "f", "artifact_tool_fingerprint": "at",
                    "asr_runtime_fingerprint": None,
                },
            }
            state = initialize_run(workspace, registry, payload, "owner-a", 300)
            lease_path = workspace / "control" / "lease.json"
            expired = json.loads(lease_path.read_text(encoding="utf-8"))
            expired["expires_at"] = _timestamp(_now() - timedelta(seconds=10))
            lease_path.write_text(json.dumps(expired), encoding="utf-8")
            result = recover_run(workspace, registry, "owner-b", None, 300, recover_expired=True)
            self.assertTrue(result["lease_taken_over"])
            self.assertIsNotNone(result["event"])
            self.assertEqual("RECOVERED", result["event"]["status"])
            self.assertTrue(result["event"]["metadata"].get("lease_takeover_only"))

    def test_preflight_validates_against_strict_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "cap.json"
            subprocess.run(
                ["pwsh", "-NoLogo", "-NoProfile", "-File",
                 str(SKILL_ROOT / "scripts" / "preflight.ps1"),
                 "-OutputPath", str(output), "-TargetPath", str(root), "-Mode", "AUDIT"],
                text=True, capture_output=True, check=False,
            )
            if not output.exists():
                self.skipTest("preflight did not produce output")
            result = subprocess.run(
                ["python", str(SKILL_ROOT / "scripts" / "validate-json.py"),
                 "--input", str(output), "--schema", "capability-report"],
                text=True, capture_output=True, check=False,
            )
            self.assertIn(result.returncode, {0, 3}, result.stderr + result.stdout)
            if result.returncode == 0:
                payload = json.loads(result.stdout)
                self.assertEqual("PASS", payload["status"])
                self.assertEqual(0, payload["error_count"])


class V62SchemaContractTests(unittest.TestCase):
    def test_preflight_emits_v62_capability_schema_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "cap.json"
            result = subprocess.run(
                ["pwsh", "-NoLogo", "-NoProfile", "-File",
                 str(SKILL_ROOT / "scripts" / "preflight.ps1"),
                 "-OutputPath", str(output), "-TargetPath", str(root), "-Mode", "AUDIT"],
                text=True, capture_output=True, check=False,
            )
            self.assertIn(result.returncode, {0, 3}, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertIn("probe_id", payload)
            self.assertIn("fingerprint", payload)
            self.assertIn("ttl_expires_at", payload)
            self.assertIn("capabilities", payload)
            self.assertIsInstance(payload["capabilities"], dict)
            self.assertGreater(len(payload["capabilities"]), 0)
            for name, entry in payload["capabilities"].items():
                self.assertIn("available", entry)
                self.assertIn("evidence", entry)

    def test_schema_bundle_declares_strict_control_plane_contracts(self) -> None:
        for filename in (
            "gate-registry.schema.json",
            "orchestrator-event.schema.json",
            "orchestrator-state.schema.json",
            "gate-submission.schema.json",
            "approval-record.schema.json",
            "run-policy.schema.json",
            "prototype-review.schema.json",
            "capability-report.schema.json",
            "quality-assessment.schema.json",
        ):
            payload = json.loads((SCHEMAS / filename).read_text(encoding="utf-8"))
            self.assertEqual("https://json-schema.org/draft/2020-12/schema", payload["$schema"])
            self.assertFalse(payload["additionalProperties"])

    def test_legacy_release_profile_is_not_in_v62_contract(self) -> None:
        release_schema = json.loads((SCHEMAS / "release-input.schema.json").read_text(encoding="utf-8"))
        profiles = release_schema["properties"]["certification_profile"]["enum"]
        self.assertNotIn("FINAL_RELEASE", profiles)
        self.assertIn("FINAL_RELEASE_STATIC", profiles)
        self.assertIn("FINAL_RELEASE_MOTION", profiles)


if __name__ == "__main__":
    unittest.main()
