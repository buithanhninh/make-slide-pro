from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path


SKILL_ROOT = (
    Path(os.environ["MAKE_SLIDE_PRO_ROOT"])
    if os.environ.get("MAKE_SLIDE_PRO_ROOT")
    else Path(__file__).resolve().parents[1]
)


def run_pwsh(script: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["pwsh", "-NoLogo", "-NoProfile", "-File", str(SKILL_ROOT / "scripts" / script), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


class SkillPackageTests(unittest.TestCase):
    def _write_job_contract(self, path: Path, **overrides: object) -> dict[str, object]:
        payload: dict[str, object] = {
            "schema_version": "1.0",
            "primary_operation": "CREATE",
            "modifiers": ["CERTIFY"],
            "audience": "Board of Directors",
            "purpose": "Support a decision",
            "audience_action": "Approve the recommended plan",
            "output_language": "vi-VN",
            "duration_minutes": 20,
            "slide_count_policy": "CONTENT_DRIVEN",
            "preservation_mode": "LOCKED",
            "sequence_change_allowed": False,
            "visual_style": "MODERN_REFINED",
            "motion_level": "NARRATIVE",
            "confidentiality": "CONFIDENTIAL",
            "external_sourcing_allowed": False,
            "content_change_budget": {
                "max_semantic_change": "EQUIVALENT_ONLY",
                "allow_derivation": False,
                "allow_reorder": False,
                "omission_policy": "NONE",
                "p0_p1_omission_allowed": False,
            },
            "output_contract": {
                "format": "PPTX",
                "editable": True,
                "versioned": True,
                "source_notes": "REQUIRED",
                "evidence_package": "FULL",
            },
            "certification_mode": "CERTIFIED",
        }
        payload.update(overrides)
        path.write_text(json.dumps(payload), encoding="utf-8")
        return payload

    def test_required_entrypoints_exist(self) -> None:
        required = [
            "SKILL.md",
            "agents/openai.yaml",
            "scripts/preflight.ps1",
            "scripts/inventory-inputs.ps1",
            "scripts/inspect-archive.ps1",
            "scripts/route-job.ps1",
            "scripts/audit-native-layout.ps1",
            "scripts/audit-motion.ps1",
            "scripts/audit-images.py",
            "scripts/audit-images.ps1",
            "scripts/audit-contrast.py",
            "scripts/audit-contrast.ps1",
            "scripts/audit-icon-consistency.mjs",
            "scripts/audit-visual-coverage.mjs",
            "scripts/compare-content.ps1",
            "scripts/reconcile-content.py",
            "scripts/validate-data.py",
            "scripts/validate-json.py",
            "scripts/validate-job-contract.py",
            "scripts/validate-slide-blueprints.py",
            "scripts/render-pdf.ps1",
            "scripts/ensure-faster-whisper.ps1",
            "scripts/certify-release.ps1",
            "scripts/safe_io.py",
            "scripts/safe-io.mjs",
            "schemas/evidence-graph.schema.json",
            "schemas/narrative-graph.schema.json",
            "schemas/slide-blueprint.schema.json",
            "schemas/visual-asset.schema.json",
            "schemas/motion-storyboard.schema.json",
            "schemas/routing-decision.schema.json",
            "schemas/qa-finding.schema.json",
            "schemas/evidence-receipt.schema.json",
            "schemas/visual-assets-evidence-receipt.schema.json",
            "schemas/release-certificate.schema.json",
            "schemas/native-layout-report.schema.json",
            "schemas/native-visual-coverage-report.schema.json",
            "references/certified-pipeline.md",
            "references/intake-and-routing.md",
            "references/content-to-slide.md",
            "references/modern-refined-visual-system.md",
            "references/motion-system.md",
            "references/qa-and-certification.md",
            "references/script-contracts.md",
            "assets/style-presets/modern-refined.tokens.json",
            "assets/style-presets/lucide-semantic-registry.json",
            "assets/authoring-starter/make-slide-pro-starter.mjs",
        ]
        missing = [item for item in required if not (SKILL_ROOT / item).exists()]
        self.assertEqual([], missing)

    def test_skill_contract_contains_non_negotiable_rules(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        required_phrases = [
            "@oai/artifact-tool",
            "python-pptx",
            "PASS",
            "UNVERIFIED",
            "BLOCKED",
            "static",
            "motion",
            "source",
            "slide blueprint",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, skill)

    def test_inventory_detects_signature_mismatch_and_hashes_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fake = root / "fake.pptx"
            fake.write_text("plain text pretending to be pptx", encoding="utf-8")
            output = root / "inventory.json"
            result = run_pwsh(
                "inventory-inputs.ps1",
                "-InputPath",
                str(root),
                "-OutputPath",
                str(output),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertEqual(1, len(payload["sources"]))
            source = payload["sources"][0]
            self.assertEqual(64, len(source["sha256"]))
            self.assertTrue(source["extension_mismatch"])
            self.assertEqual("TEXT", source["detected_format"])

    def test_inventory_rejects_output_path_equal_to_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "source.txt"
            source.write_text("immutable source", encoding="utf-8")
            result = run_pwsh(
                "inventory-inputs.ps1",
                "-InputPath",
                str(source),
                "-OutputPath",
                str(source),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual("immutable source", source.read_text(encoding="utf-8"))

    def test_inventory_excludes_report_inside_source_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "source.txt").write_text("source", encoding="utf-8")
            output = root / "inventory.json"
            result = run_pwsh(
                "inventory-inputs.ps1",
                "-InputPath",
                str(root),
                "-OutputPath",
                str(output),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertEqual(1, payload["source_count"])
            self.assertNotIn(str(output), {source["path"] for source in payload["sources"]})

    def test_inventory_blocks_empty_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "empty.txt"
            source.write_bytes(b"")
            output = root / "inventory.json"
            result = run_pwsh(
                "inventory-inputs.ps1",
                "-InputPath",
                str(source),
                "-OutputPath",
                str(output),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertEqual("BLOCKED", payload["status"])
            self.assertIn("EMPTY_FILE", payload["sources"][0]["risk_flags"])

    def test_inventory_enforces_file_and_byte_resource_limits_before_hashing(self) -> None:
        cases = [
            (
                "file-count",
                {"a.txt": b"a", "b.txt": b"b", "c.txt": b"c"},
                ["-MaximumFiles", "2"],
                "SOURCE_FILE_COUNT_LIMIT_EXCEEDED",
            ),
            (
                "total-bytes",
                {"a.txt": b"12345", "b.txt": b"67890"},
                ["-MaximumTotalBytes", "8"],
                "SOURCE_TOTAL_BYTES_LIMIT_EXCEEDED",
            ),
            (
                "single-file-bytes",
                {"large.txt": b"12345"},
                ["-MaximumFileBytes", "4"],
                "SOURCE_FILE_BYTES_LIMIT_EXCEEDED",
            ),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for index, (case_name, files, limit_arguments, expected_error) in enumerate(cases):
                with self.subTest(case=case_name):
                    source_directory = root / f"sources-{index}"
                    source_directory.mkdir()
                    for name, content in files.items():
                        (source_directory / name).write_bytes(content)
                    output = root / f"inventory-{index}.json"
                    result = run_pwsh(
                        "inventory-inputs.ps1",
                        "-InputPath", str(source_directory),
                        "-OutputPath", str(output),
                        *limit_arguments,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    payload = json.loads(output.read_text(encoding="utf-8-sig"))
                    self.assertEqual("BLOCKED", payload["status"])
                    self.assertTrue(
                        any(expected_error in item for item in payload["errors"]),
                        payload,
                    )

    def test_inspect_input_rejects_output_path_equal_to_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.txt"
            source.write_text("immutable source", encoding="utf-8")
            result = run_pwsh(
                "inspect-input.ps1",
                "-InputPath",
                str(source),
                "-OutputPath",
                str(source),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual("immutable source", source.read_text(encoding="utf-8"))

    def test_large_file_signature_probe_does_not_overflow_int32(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "large.bin"
            with source.open("wb") as stream:
                stream.seek((2 * 1024 * 1024 * 1024) + 1)
                stream.write(b"x")
            common = SKILL_ROOT / "scripts" / "common.ps1"
            command = (
                f". '{common}'; "
                f"$bytes = Get-FilePrefixBytes -Path '{source}' -Count 4096; "
                "Write-Output $bytes.Length"
            )
            result = subprocess.run(
                ["pwsh", "-NoLogo", "-NoProfile", "-Command", command],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("4096", result.stdout.strip())

    def test_mutable_writer_rejects_existing_reparse_target(self) -> None:
        if os.name != "nt":
            self.skipTest("Windows junction coverage")
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            target = root / "target"
            junction = root / "mutable-state.json"
            target.mkdir()
            sentinel = target / "sentinel.txt"
            sentinel.write_text("keep", encoding="utf-8")
            result = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode != 0:
                self.skipTest(f"junction unavailable: {result.stderr or result.stdout}")
            try:
                common = SKILL_ROOT / "scripts" / "common.ps1"
                command = (
                    f". '{common}'; "
                    f"Write-JsonFileMutable -Value ([ordered]@{{status='PASS'}}) -Path '{junction}'"
                )
                write_result = subprocess.run(
                    ["pwsh", "-NoLogo", "-NoProfile", "-Command", command],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertNotEqual(0, write_result.returncode)
                self.assertIn(
                    "PATH_REPARSE_POINT_NOT_ALLOWED:",
                    write_result.stdout + write_result.stderr,
                )
                self.assertEqual("keep", sentinel.read_text(encoding="utf-8"))
            finally:
                if junction.exists():
                    junction.rmdir()

    def test_asr_probe_returns_fail_closed_receipt_instead_of_runtime_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            result = run_pwsh(
                "ensure-faster-whisper.ps1",
                "-CacheRoot",
                str(root),
                "-PythonPath",
                sys.executable,
                "-ProbeOnly",
            )
            self.assertIn(result.returncode, {0, 3}, result.stderr)
            receipt_path = root / "asr" / "install-receipt.json"
            self.assertTrue(receipt_path.exists())
            receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
            self.assertIn(receipt["status"], {"PASS", "UNVERIFIED"})

    def test_asr_probe_selects_cuda_only_when_ctranslate2_verifies_it(self) -> None:
        probe_path = SKILL_ROOT / "scripts" / "probe-asr-runtime.py"
        specification = importlib.util.spec_from_file_location("make_slide_pro_probe_asr", probe_path)
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        module.probe_nvidia = lambda: {"available": True, "path": "nvidia-smi", "devices": ["GPU"]}
        module.supported_compute_types = lambda device="cpu": ["int8"] if device == "cpu" else []
        original_argv = sys.argv
        try:
            sys.argv = [str(probe_path)]
            stream = io.StringIO()
            with redirect_stdout(stream):
                module.main()
            payload = json.loads(stream.getvalue())
        finally:
            sys.argv = original_argv
        self.assertEqual("cpu", payload["selected_device"])
        self.assertEqual("int8", payload["selected_compute_type"])
        self.assertFalse(payload["cuda_verified"])

    def test_asr_probe_selects_only_reported_cpu_compute_type(self) -> None:
        probe_path = SKILL_ROOT / "scripts" / "probe-asr-runtime.py"
        specification = importlib.util.spec_from_file_location("make_slide_pro_probe_asr_cpu", probe_path)
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        module.probe_nvidia = lambda: {"available": False, "path": None, "devices": []}
        module.supported_compute_types = lambda device="cpu": ["float32"] if device == "cpu" else []
        original_argv = sys.argv
        try:
            sys.argv = [str(probe_path)]
            stream = io.StringIO()
            with redirect_stdout(stream):
                module.main()
            payload = json.loads(stream.getvalue())
        finally:
            sys.argv = original_argv
        self.assertEqual("cpu", payload["selected_device"])
        self.assertEqual("float32", payload["selected_compute_type"])
        self.assertIn("float32", payload["ctranslate2"]["cpu_compute_types"])

    def test_asr_probe_marks_runtime_unready_without_suitable_compute_type(self) -> None:
        probe_path = SKILL_ROOT / "scripts" / "probe-asr-runtime.py"
        specification = importlib.util.spec_from_file_location("make_slide_pro_probe_asr_empty", probe_path)
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        module.probe_nvidia = lambda: {"available": True, "path": "nvidia-smi", "devices": ["GPU"]}
        module.supported_compute_types = lambda device="cpu": []
        original_find_spec = module.importlib.util.find_spec
        original_argv = sys.argv
        try:
            module.importlib.util.find_spec = lambda _name: object()
            sys.argv = [str(probe_path)]
            stream = io.StringIO()
            with redirect_stdout(stream):
                exit_code = module.main()
            payload = json.loads(stream.getvalue())
        finally:
            module.importlib.util.find_spec = original_find_spec
            sys.argv = original_argv
        self.assertEqual(3, exit_code)
        self.assertIsNone(payload["selected_device"])
        self.assertIsNone(payload["selected_compute_type"])
        self.assertFalse(payload["ready"])

    def test_asr_probe_refreshes_existing_report_with_safe_writer(self) -> None:
        probe_path = SKILL_ROOT / "scripts" / "probe-asr-runtime.py"
        specification = importlib.util.spec_from_file_location("make_slide_pro_probe_asr_writer", probe_path)
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        module.probe_nvidia = lambda: {"available": False, "path": None, "devices": []}
        module.supported_compute_types = lambda device="cpu": ["int8"] if device == "cpu" else []
        original_find_spec = module.importlib.util.find_spec
        original_argv = sys.argv
        try:
            module.importlib.util.find_spec = lambda _name: object()
            with tempfile.TemporaryDirectory() as temporary_directory:
                output_path = Path(temporary_directory) / "capability-report.json"
                for _ in range(2):
                    sys.argv = [str(probe_path), "--output", str(output_path)]
                    stream = io.StringIO()
                    with redirect_stdout(stream):
                        exit_code = module.main()
                    self.assertEqual(0, exit_code)
                    self.assertEqual("PASS", json.loads(stream.getvalue()).get("status"))
                report = json.loads(output_path.read_text(encoding="utf-8"))
                self.assertEqual("cpu", report["selected_device"])
                self.assertEqual("int8", report["selected_compute_type"])
        finally:
            module.importlib.util.find_spec = original_find_spec
            sys.argv = original_argv

    def test_asr_probe_fails_closed_when_output_target_is_not_regular_file(self) -> None:
        probe_path = SKILL_ROOT / "scripts" / "probe-asr-runtime.py"
        specification = importlib.util.spec_from_file_location("make_slide_pro_probe_asr_bad_output", probe_path)
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        module.probe_nvidia = lambda: {"available": False, "path": None, "devices": []}
        module.supported_compute_types = lambda device="cpu": ["int8"] if device == "cpu" else []
        original_argv = sys.argv
        try:
            with tempfile.TemporaryDirectory() as temporary_directory:
                output_path = Path(temporary_directory) / "existing-directory"
                output_path.mkdir()
                sys.argv = [str(probe_path), "--output", str(output_path)]
                stream = io.StringIO()
                try:
                    with redirect_stdout(stream):
                        exit_code = module.main()
                except Exception as error:
                    self.fail(f"probe raised instead of fail-closed: {error}")
                payload = json.loads(stream.getvalue())
                self.assertEqual(3, exit_code)
                self.assertEqual("UNVERIFIED", payload["status"])
                self.assertIn("ASR_PROBE_OUTPUT_WRITE_FAILED", payload["error"])
        finally:
            sys.argv = original_argv

    def test_preflight_keeps_cpu_default_until_asr_runtime_verifies_cuda(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            (fake_bin / "nvidia-smi.cmd").write_text("@exit /b 0\n", encoding="utf-8")
            output = root / "preflight.json"
            environment = os.environ.copy()
            environment["PATH"] = str(fake_bin) + os.pathsep + environment.get("PATH", "")
            result = subprocess.run(
                [
                    "pwsh",
                    "-NoLogo",
                    "-NoProfile",
                    "-File",
                    str(SKILL_ROOT / "scripts" / "preflight.ps1"),
                    "-OutputPath",
                    str(output),
                    "-TargetPath",
                    str(root),
                    "-Mode",
                    "AUDIT",
                ],
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertIn(result.returncode, {0, 3}, result.stderr)
            self.assertTrue(output.exists(), result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertIn(payload["status"], {"PASS", "UNVERIFIED"})
            self.assertEqual(payload["certification_ceiling"], payload["status"])
            self.assertEqual("GPU_CANDIDATE", payload["profile"])
            self.assertTrue(payload["hardware"]["nvidia_smi"]["available"])
            self.assertFalse(payload["hardware"]["cuda_verified"])
            self.assertEqual("cpu", payload["hardware"]["selected_asr_device"])
            self.assertEqual("int8", payload["hardware"]["selected_asr_compute_type"])

    def test_asr_installer_refuses_concurrent_cache_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_root = Path(temporary_directory)
            environment = os.environ.copy()
            environment["MAKE_SLIDE_PRO_TEST_ASR_CACHE"] = str(cache_root)
            holder_script = (
                "$cache=[IO.Path]::GetFullPath($env:MAKE_SLIDE_PRO_TEST_ASR_CACHE).TrimEnd('\\','/').ToLowerInvariant();"
                "$bytes=[Text.Encoding]::UTF8.GetBytes($cache);"
                "$sha=[Security.Cryptography.SHA256]::Create();"
                "$hash=[Convert]::ToHexString($sha.ComputeHash($bytes)).ToLowerInvariant();"
                "$mutex=[Threading.Mutex]::new($false,('Local\\MakeSlidePro-ASR-' + $hash));"
                "$null=$mutex.WaitOne();"
                "[Console]::Out.WriteLine('LOCKED');[Console]::Out.Flush();"
                "Start-Sleep -Seconds 30"
            )
            holder = subprocess.Popen(
                ["pwsh", "-NoLogo", "-NoProfile", "-Command", holder_script],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
            )
            try:
                self.assertEqual("LOCKED", holder.stdout.readline().strip())
                result = run_pwsh(
                    "ensure-faster-whisper.ps1",
                    "-CacheRoot",
                    str(cache_root),
                    "-PythonPath",
                    sys.executable,
                    "-ProbeOnly",
                    "-LockTimeoutSeconds",
                    "0",
                )
                self.assertEqual(3, result.returncode, result.stderr)
                receipt_path = cache_root / "asr" / "install-receipt.json"
                self.assertFalse(receipt_path.exists())
                receipt = json.loads(result.stdout)
                self.assertEqual("UNVERIFIED", receipt["status"])
                self.assertEqual("ASR_INSTALL_BUSY", receipt["reason"])
            finally:
                holder.terminate()
                try:
                    holder.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    holder.kill()
                    holder.wait(timeout=5)
                if holder.stdout:
                    holder.stdout.close()
                if holder.stderr:
                    holder.stderr.close()

    def test_asr_installer_rejects_reparse_asr_directory_before_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            cache_root = root / "cache"
            target = root / "target"
            cache_root.mkdir()
            target.mkdir()
            junction = cache_root / "asr"
            create = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            if create.returncode != 0:
                self.skipTest(f"junction unavailable: {create.stderr or create.stdout}")
            try:
                result = run_pwsh(
                    "ensure-faster-whisper.ps1",
                    "-CacheRoot",
                    str(cache_root),
                    "-PythonPath",
                    sys.executable,
                    "-ProbeOnly",
                )
                self.assertEqual(2, result.returncode, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual("BLOCKED", payload["status"])
                self.assertEqual("ASR_CACHE_PATH_UNSAFE", payload["reason"])
                self.assertIn("REPARSE_POINT_NOT_ALLOWED", payload["error"])
                self.assertEqual([], list(target.iterdir()))
            finally:
                if junction.exists():
                    junction.rmdir()

    def test_asr_installer_rolls_back_failed_published_runtime(self) -> None:
        script = (SKILL_ROOT / "scripts" / "ensure-faster-whisper.ps1").read_text(encoding="utf-8")
        self.assertIn("ASR_POST_INSTALL_PROBE_FAILED", script)
        self.assertIn("Remove-Item -LiteralPath $venv -Recurse -Force", script)
        self.assertIn("Move-Item -LiteralPath $backup -Destination $venv", script)
        self.assertIn("rollback_restored", script)

    def test_asr_success_commits_receipt_before_backup_cleanup(self) -> None:
        script = (SKILL_ROOT / "scripts" / "ensure-faster-whisper.ps1").read_text(encoding="utf-8")
        success_block_start = script.index("if ($probeExit -ne 0) { throw 'ASR_POST_INSTALL_PROBE_FAILED' }")
        success_block_end = script.index("} catch {", success_block_start)
        success_block = script[success_block_start:success_block_end]
        self.assertLess(success_block.index("Write-Receipt -Value $receipt"), success_block.index("Remove-Item -LiteralPath $backup"))
        self.assertIn("backup_cleanup_pending", success_block)

    def test_transcription_rejects_source_output_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "audio.mp3"
            source.write_bytes(b"audio")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "transcribe-media.py"),
                    "--input",
                    str(source),
                    "--output",
                    str(source),
                    "--dry-run",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode)
            self.assertEqual(b"audio", source.read_bytes())

    def test_transcription_rejects_glossary_output_collision_and_invalid_beam(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "audio.mp3"
            glossary = root / "glossary.txt"
            source.write_bytes(b"audio")
            glossary.write_text("Sunhouse", encoding="utf-8")
            collision = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "transcribe-media.py"),
                    "--input", str(source), "--glossary", str(glossary),
                    "--output", str(glossary), "--dry-run",
                ],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(2, collision.returncode, collision.stderr)
            self.assertEqual("Sunhouse", glossary.read_text(encoding="utf-8"))

            output = root / "transcript.json"
            invalid_beam = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "transcribe-media.py"),
                    "--input", str(source), "--output", str(output),
                    "--beam-size", "0", "--dry-run",
                ],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(2, invalid_beam.returncode, invalid_beam.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", payload["status"])
            self.assertEqual("INVALID_BEAM_SIZE", payload["error"])

    def test_python_audits_reject_source_output_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.json"
            other = root / "other.json"
            source.write_text("{}", encoding="utf-8")
            other.write_text("{}", encoding="utf-8")
            cases = [
                ("audit-images.py", ["--assets", str(source), "--output", str(source)]),
                ("audit-contrast.py", ["--manifest", str(source), "--output", str(source)]),
                ("validate-data.py", ["--input", str(source), "--output", str(source)]),
                ("validate-json.py", ["--input", str(source), "--schema", "release-input", "--output", str(source)]),
                ("reconcile-content.py", ["--content-atoms", str(source), "--data-ledger", str(other), "--output", str(source)]),
                ("validate-slide-blueprints.py", ["--blueprints", str(source), "--content-atoms", str(other), "--output", str(source)]),
            ]
            for script, arguments in cases:
                with self.subTest(script=script):
                    source.write_text("{}", encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(SKILL_ROOT / "scripts" / script), *arguments],
                        text=True, capture_output=True, check=False,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    self.assertEqual("{}", source.read_text(encoding="utf-8"))

    def test_python_audit_rejects_existing_output_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "ledger.json"
            output = root / "report.json"
            source.write_text('{"metrics":[]}', encoding="utf-8")
            output.write_text("sentinel", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SKILL_ROOT / "scripts" / "validate-data.py"),
                 "--input", str(source), "--output", str(output)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual("sentinel", output.read_text(encoding="utf-8"))

    def test_image_audit_rejects_nan_ppi_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "assets.json"
            output = root / "report.json"
            source.write_text('{"assets":[]}', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SKILL_ROOT / "scripts" / "audit-images.py"),
                 "--assets", str(source), "--output", str(output), "--minimum-ppi", "NaN"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", payload["status"])
            self.assertEqual("INVALID_PPI_THRESHOLD", payload["error"])

    def test_inventory_detects_flac_ogg_and_raw_aac_signatures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "sample.flac").write_bytes(b"fLaC" + b"\x00" * 16)
            (root / "sample.ogg").write_bytes(b"OggS" + b"\x00" * 16)
            (root / "sample.aac").write_bytes(b"\xff\xf1" + b"\x00" * 16)
            (root / "sample.mp3").write_bytes(b"\xff\xfb" + b"\x00" * 16)
            output = root / "inventory.json"
            result = run_pwsh("inventory-inputs.ps1", "-InputPath", str(root), "-OutputPath", str(output))
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            formats = {Path(source["path"]).suffix: source["detected_format"] for source in payload["sources"]}
            self.assertEqual({".aac": "AAC", ".flac": "FLAC", ".mp3": "MP3", ".ogg": "OGG"}, formats)

    def test_inventory_detects_empty_zip_signature_as_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "empty.zip"
            source.write_bytes(b"PK\x05\x06" + b"\x00" * 18)
            output = root / "inventory.json"
            result = run_pwsh("inventory-inputs.ps1", "-InputPath", str(source), "-OutputPath", str(output))
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertEqual("ZIP", payload["sources"][0]["detected_format"])
            self.assertEqual("PRIMARY_CONTENT", payload["sources"][0]["role"])

    def test_inspect_input_routes_pdf_to_pdf_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.pdf"
            source.write_bytes(b"%PDF-1.7\n%%EOF\n")
            output = root / "inspect.json"
            result = run_pwsh("inspect-input.ps1", "-InputPath", str(source), "-OutputPath", str(output))
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertEqual("PDF", payload["adapter"])
            self.assertEqual("S3_FLAT_OR_REPORT", payload["maturity_hint"])

    def test_inspect_input_routes_aac_to_audio_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.aac"
            source.write_bytes(b"\xff\xf1" + b"\x00" * 16)
            output = root / "inspect.json"
            result = run_pwsh("inspect-input.ps1", "-InputPath", str(source), "-OutputPath", str(output))
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertEqual("AUDIO", payload["adapter"])
            self.assertEqual("S0_MEDIA", payload["maturity_hint"])

    def test_router_classifies_pdf_as_s3_report_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "PDF",
                                "extension": ".pdf",
                                "role": "PRIMARY_CONTENT",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath",
                str(inventory_path),
                "-RequestedOperation",
                "auto",
                "-OutputPath",
                str(route_path),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("REPORT_OR_FLAT_SOURCE", route["input_class"])
            self.assertEqual("S3", route["maturity"])
            self.assertEqual("PDF_RECONSTRUCTION", route["visual_route"])
            self.assertEqual("PDF", route["required_adapters"][0]["adapter"])

    def test_router_recognizes_archive_source_and_required_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "ZIP",
                                "extension": ".zip",
                                "role": "PRIMARY_CONTENT",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath",
                str(inventory_path),
                "-RequestedOperation",
                "auto",
                "-OutputPath",
                str(route_path),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("ARCHIVE_SOURCE", route["input_class"])
            self.assertEqual("ARCHIVE_EXTRACTION", route["visual_route"])
            self.assertIn("EXTRACT_ARCHIVE", route["modifiers"])
            self.assertEqual("ARCHIVE", route["required_adapters"][0]["adapter"])

    def test_router_distinguishes_existing_deck_from_raw_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "PPTX",
                                "extension": ".pptx",
                                "role": "PREVIOUS_DECK",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath",
                str(inventory_path),
                "-RequestedOperation",
                "auto",
                "-OutputPath",
                str(route_path),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("EDITABLE_DECK", route["input_class"])
            self.assertEqual("REDESIGN", route["primary_operation"])
            self.assertEqual("S4", route["maturity"])

    def test_router_rejects_incompatible_motion_request_for_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "PDF",
                                "extension": ".pdf",
                                "role": "PRIMARY_CONTENT",
                                "path": str(root / "source.pdf"),
                                "sha256": "a" * 64,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath",
                str(inventory_path),
                "-RequestedOperation",
                "motion",
                "-OutputPath",
                str(route_path),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("BLOCKED", route["status"])
            self.assertIn("OPERATION_REQUIRES_DECK", route["blocking_reasons"])

    def test_router_does_not_pass_macro_source_or_unverified_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            cases = [
                ("macro", "PASS", ["MACRO_ENABLED"], "MACRO_SOURCE_REQUIRES_EXPLICIT_SAFE_HANDLING"),
                ("unverified", "UNVERIFIED", [], "INVENTORY_NOT_CERTIFIED"),
            ]
            for label, status, risk_flags, expected_reason in cases:
                with self.subTest(label=label):
                    inventory_path = root / f"inventory-{label}.json"
                    route_path = root / f"route-{label}.json"
                    inventory_path.write_text(
                        json.dumps(
                            {
                                "schema_version": "1.0",
                                "status": status,
                                "sources": [
                                    {
                                        "source_id": "source-001",
                                        "detected_format": "PPTM",
                                        "extension": ".pptm",
                                        "role": "PREVIOUS_DECK",
                                        "path": str(root / "source.pptm"),
                                        "sha256": "a" * 64,
                                        "risk_flags": risk_flags,
                                    }
                                ],
                            }
                        ),
                        encoding="utf-8",
                    )
                    result = run_pwsh(
                        "route-job.ps1",
                        "-InventoryPath",
                        str(inventory_path),
                        "-RequestedOperation",
                        "auto",
                        "-OutputPath",
                        str(route_path),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    route = json.loads(route_path.read_text(encoding="utf-8-sig"))
                    self.assertEqual("BLOCKED", route["status"])
                    self.assertIn(expected_reason, route["blocking_reasons"])

    def test_router_blocks_duplicate_source_ids_and_signature_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "PDF",
                                "role": "PRIMARY_CONTENT",
                                "risk_flags": ["SIGNATURE_EXTENSION_MISMATCH"],
                            },
                            {
                                "source_id": "source-001",
                                "detected_format": "TEXT",
                                "role": "PRIMARY_CONTENT",
                                "risk_flags": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath",
                str(inventory_path),
                "-OutputPath",
                str(route_path),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertIn("DUPLICATE_SOURCE_ID:source-001", route["blocking_reasons"])
            self.assertIn("SIGNATURE_EXTENSION_MISMATCH", route["blocking_reasons"])

    def test_router_blocks_multiple_data_authorities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {"source_id": "source-001", "detected_format": "XLSX", "role": "DATA_AUTHORITY"},
                            {"source_id": "source-002", "detected_format": "CSV", "role": "DATA_AUTHORITY"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath",
                str(inventory_path),
                "-OutputPath",
                str(route_path),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertIn("MULTIPLE_DATA_AUTHORITIES_REQUIRE_RECONCILIATION", route["blocking_reasons"])

    def test_router_marks_deck_plus_supporting_sources_for_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "PPTX",
                                "role": "PREVIOUS_DECK",
                                "risk_flags": [],
                            },
                            {
                                "source_id": "source-002",
                                "detected_format": "PDF",
                                "role": "SUPPORTING_EVIDENCE",
                                "risk_flags": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath",
                str(inventory_path),
                "-OutputPath",
                str(route_path),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("EDITABLE_DECK", route["input_class"])
            self.assertIn("RECONCILE_SOURCES", route["modifiers"])

    def test_router_writes_blocked_receipt_for_invalid_job_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            contract_path = root / "job-contract.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "TEXT",
                                "role": "PRIMARY_CONTENT",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            contract_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "primary_operation": "CREATE",
                        "modifiers": "CERTIFY",
                        "preservation_mode": "LOCKED",
                        "certification_mode": "CERTIFIED",
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath", str(inventory_path),
                "-JobContractPath", str(contract_path),
                "-OutputPath", str(route_path),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertTrue(route_path.exists())
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("BLOCKED", route["status"])
            self.assertTrue(
                any("ROUTE_JOB_CONTRACT_MODIFIERS_INVALID" in item for item in route["blocking_reasons"]),
                route,
            )

    def test_router_rejects_invalid_job_contract_routing_enums_with_schema_valid_fallback(self) -> None:
        cases = [
            ("primary_operation", "DECORATE", "ROUTE_JOB_CONTRACT_OPERATION_INVALID:DECORATE"),
            ("modifiers", ["CERTIFY", "SPARKLE"], "ROUTE_JOB_CONTRACT_MODIFIER_INVALID:SPARKLE"),
            ("preservation_mode", "LOOSE", "ROUTE_JOB_CONTRACT_PRESERVATION_INVALID:LOOSE"),
            ("certification_mode", "PERFECT", "ROUTE_JOB_CONTRACT_CERTIFICATION_INVALID:PERFECT"),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "TEXT",
                                "role": "PRIMARY_CONTENT",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            for index, (field, value, expected_reason) in enumerate(cases):
                with self.subTest(field=field):
                    contract_path = root / f"job-contract-{index}.json"
                    route_path = root / f"route-{index}.json"
                    validation_path = root / f"route-validation-{index}.json"
                    self._write_job_contract(contract_path, **{field: value})
                    result = run_pwsh(
                        "route-job.ps1",
                        "-InventoryPath", str(inventory_path),
                        "-JobContractPath", str(contract_path),
                        "-OutputPath", str(route_path),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    route = json.loads(route_path.read_text(encoding="utf-8-sig"))
                    self.assertEqual("BLOCKED", route["status"])
                    self.assertTrue(
                        any(expected_reason in item for item in route["blocking_reasons"]),
                        route,
                    )
                    validation = subprocess.run(
                        [
                            sys.executable,
                            str(SKILL_ROOT / "scripts" / "validate-json.py"),
                            "--input", str(route_path),
                            "--schema", "routing-decision",
                            "--output", str(validation_path),
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(0, validation.returncode, validation.stderr)

    def test_router_writes_schema_valid_fallback_when_job_contract_is_missing_or_collides(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "TEXT",
                                "role": "PRIMARY_CONTENT",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            cases = [
                (root / "missing-contract.json", "ROUTE_JOB_CONTRACT_MISSING"),
                (inventory_path, "ROUTE_JOB_CONTRACT_COLLIDES_WITH_INVENTORY"),
            ]
            for index, (contract_path, expected_reason) in enumerate(cases):
                with self.subTest(reason=expected_reason):
                    route_path = root / f"route-{index}.json"
                    validation_path = root / f"validation-{index}.json"
                    result = run_pwsh(
                        "route-job.ps1",
                        "-InventoryPath", str(inventory_path),
                        "-JobContractPath", str(contract_path),
                        "-OutputPath", str(route_path),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    route = json.loads(route_path.read_text(encoding="utf-8-sig"))
                    self.assertEqual("BLOCKED", route["status"])
                    self.assertTrue(any(expected_reason in item for item in route["blocking_reasons"]), route)
                    validation = subprocess.run(
                        [
                            sys.executable,
                            str(SKILL_ROOT / "scripts" / "validate-json.py"),
                            "--input", str(route_path),
                            "--schema", "routing-decision",
                            "--output", str(validation_path),
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(0, validation.returncode, validation.stderr)

    def test_router_contract_modifiers_require_matching_source_families(self) -> None:
        cases = [
            ("REPAIR", ["TEXT"], "MODIFIER_REPAIR_REQUIRES_DECK"),
            ("UPDATE_DATA", ["PPTX"], "MODIFIER_UPDATE_DATA_REQUIRES_DATA"),
            ("UPDATE_DATA", ["XLSX"], "MODIFIER_UPDATE_DATA_REQUIRES_DECK"),
            ("TRANSCRIBE_MEDIA", ["TEXT"], "MODIFIER_TRANSCRIBE_MEDIA_REQUIRES_AUDIO_OR_VIDEO"),
            ("EXTRACT_ARCHIVE", ["TEXT"], "MODIFIER_EXTRACT_ARCHIVE_REQUIRES_ARCHIVE"),
            ("RECONCILE_SOURCES", ["TEXT"], "MODIFIER_RECONCILE_SOURCES_REQUIRES_MULTIPLE_SOURCES"),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for index, (modifier, formats, expected_reason) in enumerate(cases):
                with self.subTest(modifier=modifier, formats=formats):
                    inventory_path = root / f"inventory-{index}.json"
                    contract_path = root / f"job-contract-{index}.json"
                    route_path = root / f"route-{index}.json"
                    inventory_path.write_text(
                        json.dumps(
                            {
                                "schema_version": "1.0",
                                "status": "PASS",
                                "sources": [
                                    {
                                        "source_id": f"source-{source_index + 1:03d}",
                                        "detected_format": source_format,
                                        "role": "PRIMARY_CONTENT",
                                    }
                                    for source_index, source_format in enumerate(formats)
                                ],
                            }
                        ),
                        encoding="utf-8",
                    )
                    self._write_job_contract(
                        contract_path,
                        primary_operation="AUDIT",
                        modifiers=[modifier],
                        preservation_mode="CONTROLLED",
                        certification_mode="STANDARD",
                    )
                    result = run_pwsh(
                        "route-job.ps1",
                        "-InventoryPath", str(inventory_path),
                        "-JobContractPath", str(contract_path),
                        "-OutputPath", str(route_path),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    route = json.loads(route_path.read_text(encoding="utf-8-sig"))
                    self.assertEqual("BLOCKED", route["status"])
                    self.assertIn(expected_reason, route["blocking_reasons"])

    def test_router_does_not_inject_undeclared_modifiers_when_contract_is_present(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            contract_path = root / "job-contract.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {"source_id": "source-001", "detected_format": "PPTX", "role": "PREVIOUS_DECK"},
                            {"source_id": "source-002", "detected_format": "XLSX", "role": "DATA_AUTHORITY"},
                            {"source_id": "source-003", "detected_format": "MP3", "role": "MEDIA_ASSET"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            self._write_job_contract(
                contract_path,
                primary_operation="AUDIT",
                modifiers=[],
                preservation_mode="CONTROLLED",
                certification_mode="STANDARD",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath", str(inventory_path),
                "-JobContractPath", str(contract_path),
                "-OutputPath", str(route_path),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertEqual([], route["modifiers"])

    def test_release_certification_blocks_major_findings(self) -> None:
        result, certificate = self._certify(
            findings=[{"severity": "P1", "code": "FONT_SUBSTITUTION"}]
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])

    def test_release_certification_passes_complete_evidence(self) -> None:
        result, certificate = self._certify(findings=[])
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("PASS", certificate["status"])
        self.assertEqual("FINAL_RELEASE_MOTION", certificate["certification_profile"])

    def test_static_ready_profile_passes_without_motion_gates(self) -> None:
        result, certificate = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("PASS", certificate["status"])
        self.assertEqual("STATIC_READY_FOR_MOTION", certificate["certification_profile"])
        self.assertNotIn("motion", certificate["required_domains"])
        self.assertNotIn("motion_verified", certificate["required_evidence"])
        self.assertNotIn("static_motion_equivalent", certificate["required_evidence"])

    def test_release_certification_marks_missing_capability_unverified(self) -> None:
        result, certificate = self._certify(
            findings=[], mandatory_capabilities_verified=False
        )
        self.assertEqual(3, result.returncode, result.stderr)
        self.assertEqual("UNVERIFIED", certificate["status"])

    def test_release_certification_marks_missing_render_evidence_unverified(self) -> None:
        result, certificate = self._certify(
            findings=[], evidence_overrides={"all_slides_rendered": False}
        )
        self.assertEqual(3, result.returncode, result.stderr)
        self.assertEqual("UNVERIFIED", certificate["status"])
        self.assertIn("MISSING_OR_FAILED_EVIDENCE:all_slides_rendered", certificate["failed_requirements"])

    def test_release_certification_blocks_critical_finding_even_when_capability_missing(self) -> None:
        result, certificate = self._certify(
            findings=[{"severity": "P1", "code": "LAYOUT_OVERFLOW", "detail": "slide-2"}],
            mandatory_capabilities_verified=False,
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])

    def test_release_certification_blocks_missing_required_domain(self) -> None:
        result, certificate = self._certify(findings=[], omit_domain="motion")
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("MISSING_DOMAIN_SCORE:motion", certificate["failed_requirements"])

    def test_release_certification_blocks_source_hash_change(self) -> None:
        result, certificate = self._certify(findings=[], source_hash_unchanged=False)
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("SOURCE_HASH_CHANGED", certificate["failed_requirements"])

    def test_release_certification_rejects_lowered_quality_threshold(self) -> None:
        result, certificate = self._certify(
            findings=[],
            minimum_quality_score=0,
            minimum_domain_score=0,
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("CERTIFICATION_THRESHOLD_CANNOT_BE_LOWERED", certificate["failed_requirements"])

    def test_release_certification_binds_source_hash_to_source_path(self) -> None:
        result, certificate = self._certify(
            findings=[],
            source_hash_before_override="a" * 64,
            source_hash_after_override="a" * 64,
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("SOURCE_HASH_MISMATCH", certificate["failed_requirements"])

    def test_release_certificate_binds_source_and_output_hashes(self) -> None:
        _, certificate = self._certify(findings=[])
        expected_source_hash = hashlib.sha256(b"immutable source").hexdigest()
        self.assertEqual(expected_source_hash, certificate["source_hash_before"])
        self.assertEqual(expected_source_hash, certificate["source_hash_after"])
        self.assertEqual(
            hashlib.sha256(Path(certificate["output_path"]).read_bytes()).hexdigest(),
            certificate["output_sha256"],
        )
        self.assertTrue(Path(certificate["output_path"]).exists())

    def test_release_certification_binds_multiple_sources_to_aggregate_hash(self) -> None:
        result, certificate = self._certify(
            findings=[], additional_source_contents=["second immutable source"]
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(2, len(certificate["source_bindings"]))
        self.assertEqual(certificate["source_hash_before"], certificate["source_hash_after"])
        self.assertEqual(
            "SOURCE_FILE_SHA256_OR_SET_V1",
            certificate["certification_rules"].get("source_hash_formula"),
        )

        blocked_result, blocked_certificate = self._certify(
            findings=[],
            additional_source_contents=["second immutable source"],
            source_hash_before_override="a" * 64,
            source_hash_after_override="a" * 64,
        )
        self.assertEqual(2, blocked_result.returncode, blocked_result.stderr)
        self.assertEqual("BLOCKED", blocked_certificate["status"])
        self.assertIn(
            "SOURCE_SET_HASH_MISMATCH",
            blocked_certificate["failed_requirements"],
        )

    def test_release_certification_requires_hashed_evidence_receipts(self) -> None:
        result, certificate = self._certify(findings=[], include_evidence_receipts=False)
        self.assertEqual(3, result.returncode, result.stderr)
        self.assertEqual("UNVERIFIED", certificate["status"])
        self.assertIn("EVIDENCE_RECEIPTS_MISSING", certificate["failed_requirements"])

    def test_release_certification_blocks_tampered_evidence_receipt(self) -> None:
        result, certificate = self._certify(
            findings=[], tamper_evidence_receipt="all_slides_rendered"
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn(
            "EVIDENCE_RECEIPT_HASH_MISMATCH:all_slides_rendered",
            certificate["failed_requirements"],
        )

    def test_release_certification_blocks_receipt_bound_to_different_deck(self) -> None:
        result, certificate = self._certify(
            findings=[], receipt_subject_hash_override="d" * 64
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn(
            "EVIDENCE_RECEIPT_SUBJECT_HASH_MISMATCH:all_slides_rendered",
            certificate["failed_requirements"],
        )

    def test_release_certification_blocks_reparse_bound_files(self) -> None:
        if os.name != "nt":
            self.skipTest("Windows junction coverage")
        cases = {
            "source": "SOURCE_REPARSE_POINT_NOT_ALLOWED:source-001",
            "output": "OUTPUT_REPARSE_POINT_NOT_ALLOWED",
            "receipt": "EVIDENCE_RECEIPT_REPARSE_POINT:all_slides_rendered",
        }
        for binding, expected_failure in cases.items():
            with self.subTest(binding=binding):
                result, certificate = self._certify(
                    findings=[], reparse_binding=binding
                )
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertEqual("BLOCKED", certificate["status"])
                self.assertIn(expected_failure, certificate["failed_requirements"])

    def test_release_certification_recalculates_quality_score(self) -> None:
        result, certificate = self._certify(
            findings=[], quality_score_override=100
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn(
            "QUALITY_SCORE_FORMULA_MISMATCH",
            certificate["failed_requirements"],
        )
        self.assertAlmostEqual(98.4, certificate["calculated_quality_score"], places=2)

    def test_release_certification_blocks_future_receipt_timestamp(self) -> None:
        result, certificate = self._certify(
            findings=[], receipt_generated_at_override="2999-01-01T00:00:00Z"
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn(
            "EVIDENCE_RECEIPT_TIMESTAMP_IN_FUTURE:all_slides_rendered",
            certificate["failed_requirements"],
        )

    def test_release_certification_blocks_receipt_older_than_output(self) -> None:
        result, certificate = self._certify(
            findings=[], receipt_generated_at_override="2000-01-01T00:00:00Z"
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn(
            "EVIDENCE_RECEIPT_TIMESTAMP_PREDATES_OUTPUT:all_slides_rendered",
            certificate["failed_requirements"],
        )

    def test_release_certification_blocks_unknown_input_field(self) -> None:
        result, certificate = self._certify(
            findings=[], extra_input_fields={"trust_me": True}
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("UNKNOWN_RELEASE_FIELD:trust_me", certificate["failed_requirements"])

    def test_release_certification_blocks_unknown_domain_and_receipt_fields(self) -> None:
        _, domain_certificate = self._certify(
            findings=[], extra_domain_scores={"untrusted_domain": 100}
        )
        self.assertEqual("BLOCKED", domain_certificate["status"])
        self.assertIn(
            "UNKNOWN_DOMAIN_SCORE:untrusted_domain",
            domain_certificate["failed_requirements"],
        )

        _, receipt_certificate = self._certify(
            findings=[], extra_receipt_fields={"all_slides_rendered": {"unexpected": True}}
        )
        self.assertEqual("BLOCKED", receipt_certificate["status"])
        self.assertIn(
            "UNKNOWN_EVIDENCE_RECEIPT_FIELD:all_slides_rendered:unexpected",
            receipt_certificate["failed_requirements"],
        )

        _, source_binding_certificate = self._certify(
            findings=[], extra_source_binding_fields={"unexpected": True}
        )
        self.assertEqual("BLOCKED", source_binding_certificate["status"])
        self.assertIn(
            "UNKNOWN_SOURCE_BINDING_FIELD:source-001:unexpected",
            source_binding_certificate["failed_requirements"],
        )

        _, receipt_binding_certificate = self._certify(
            findings=[], extra_receipt_binding_fields={"all_slides_rendered": {"unexpected": True}}
        )
        self.assertEqual("BLOCKED", receipt_binding_certificate["status"])
        self.assertIn(
            "UNKNOWN_EVIDENCE_RECEIPT_BINDING_FIELD:all_slides_rendered:unexpected",
            receipt_binding_certificate["failed_requirements"],
        )

        _, receipt_check_certificate = self._certify(
            findings=[], extra_receipt_check_fields={"all_slides_rendered": {"unexpected": True}}
        )
        self.assertEqual("BLOCKED", receipt_check_certificate["status"])
        self.assertIn(
            "UNKNOWN_EVIDENCE_RECEIPT_CHECK_FIELD:all_slides_rendered:unexpected",
            receipt_check_certificate["failed_requirements"],
        )

    def test_release_certification_requires_native_visual_binding(self) -> None:
        result, certificate = self._certify(
            findings=[], omit_visual_native_metadata=True
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn(
            "NATIVE_VISUAL_BINDING_MISSING",
            certificate["failed_requirements"],
        )

    def test_release_certification_rejects_extra_receipt_key(self) -> None:
        result, certificate = self._certify(
            findings=[], extra_receipt_name="unexpected_receipt"
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn(
            "UNKNOWN_EVIDENCE_RECEIPT:unexpected_receipt",
            certificate["failed_requirements"],
        )

    def test_release_certification_does_not_reuse_receipt_subject_path(self) -> None:
        result, certificate = self._certify(
            findings=[],
            extra_receipt_fields={"all_slides_reviewed": {"subject_path": ""}},
        )
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertEqual(
            "",
            certificate["evidence_receipts"]["all_slides_reviewed"]["subject_path"],
        )

    def test_release_certification_rejects_forged_native_report_contract(self) -> None:
        cases = [
            (
                "coverage-schema",
                {"schema_version": "0.9"},
                None,
                "NATIVE_VISUAL_COVERAGE_SCHEMA_VERSION_INVALID:visual_assets_verified",
            ),
            (
                "coverage-slide-count",
                {"slide_count": 2},
                None,
                "NATIVE_VISUAL_COVERAGE_SLIDE_COUNT_MISMATCH:visual_assets_verified",
            ),
            (
                "layout-duplicate-slides",
                None,
                {
                    "slide_count": 2,
                    "slides": [
                        {"slide": 1, "shape_count": 0, "objects": []},
                        {"slide": 1, "shape_count": 0, "objects": []},
                    ],
                },
                "NATIVE_LAYOUT_REPORT_SLIDE_SEQUENCE_INVALID:visual_assets_verified",
            ),
            (
                "layout-critical-finding",
                None,
                {
                    "findings": [
                        {
                            "severity": "P1",
                            "code": "TEXT_OVERFLOW",
                            "detail": "overflow",
                        }
                    ]
                },
                "NATIVE_LAYOUT_REPORT_CRITICAL_FINDINGS:visual_assets_verified",
            ),
            (
                "coverage-malformed-finding",
                {"findings": [{"severity": "P2"}]},
                None,
                "NATIVE_VISUAL_COVERAGE_FINDINGS_INVALID:visual_assets_verified",
            ),
            (
                "layout-malformed-finding",
                None,
                {"findings": [{"severity": "P2"}]},
                "NATIVE_LAYOUT_REPORT_FINDINGS_INVALID:visual_assets_verified",
            ),
            (
                "layout-deck-hash",
                None,
                {"deck_sha256": "0" * 64},
                "NATIVE_LAYOUT_REPORT_DECK_HASH_MISMATCH:visual_assets_verified",
            ),
            (
                "blueprint-hash",
                {"blueprints_sha256": "0" * 64},
                None,
                "NATIVE_VISUAL_COVERAGE_BLUEPRINT_HASH_MISMATCH:visual_assets_verified",
            ),
        ]
        for case_name, coverage_overrides, layout_overrides, expected_failure in cases:
            with self.subTest(case=case_name):
                result, certificate = self._certify(
                    findings=[],
                    native_coverage_overrides=coverage_overrides,
                    native_layout_overrides=layout_overrides,
                )
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertEqual("BLOCKED", certificate["status"])
                self.assertIn(expected_failure, certificate["failed_requirements"])

    def test_release_certification_rechecks_bindings_before_certificate_write(self) -> None:
        content = (SKILL_ROOT / "scripts" / "certify-release.ps1").read_text(
            encoding="utf-8"
        )
        for marker in (
            "SOURCE_CHANGED_DURING_CERTIFICATION:",
            "OUTPUT_CHANGED_DURING_CERTIFICATION",
            "EVIDENCE_RECEIPT_CHANGED_DURING_CERTIFICATION:",
        ):
            self.assertIn(marker, content)
        recheck_index = content.index("SOURCE_CHANGED_DURING_CERTIFICATION:")
        write_index = content.index("Write-JsonFileNew -Value $certificate")
        self.assertLess(recheck_index, write_index)

    def test_release_certification_blocks_non_presentation_output(self) -> None:
        result, certificate = self._certify(findings=[], deck_bytes_override=b"plain text")
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertTrue(
            any(
                requirement.startswith("OUTPUT_FORMAT_NOT_PRESENTATION:")
                for requirement in certificate["failed_requirements"]
            )
        )

    def test_release_certification_rejects_null_findings(self) -> None:
        result, certificate = self._certify(findings=None)
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("INVALID_RELEASE_FIELD:findings", certificate["failed_requirements"])

    def test_release_certification_rejects_malformed_noncritical_finding(self) -> None:
        result, certificate = self._certify(findings=[{"severity": "P2"}])
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("MALFORMED_FINDING_RECORD", certificate["failed_requirements"])

    def test_release_certification_rejects_nan_threshold(self) -> None:
        result, certificate = self._certify(findings=[], minimum_quality_score="NaN")
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("INVALID_CERTIFICATION_THRESHOLD", certificate["failed_requirements"])

    def test_release_certification_blocks_output_hash_mismatch(self) -> None:
        result, certificate = self._certify(findings=[], output_hash_override="c" * 64)
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual("BLOCKED", certificate["status"])
        self.assertIn("OUTPUT_HASH_MISMATCH", certificate["failed_requirements"])

    def test_release_certification_writes_blocked_certificate_for_malformed_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            input_path = root / "release-input.json"
            output_path = root / "release-certificate.json"
            input_path.write_text("{not-json", encoding="utf-8")
            result = run_pwsh(
                "certify-release.ps1",
                "-InputPath",
                str(input_path),
                "-OutputPath",
                str(output_path),
            )
            self.assertEqual(2, result.returncode)
            certificate = json.loads(output_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("BLOCKED", certificate["status"])
            self.assertEqual("1.0", certificate["schema_version"])
            self.assertIn("RELEASE_INPUT_UNREADABLE", certificate["failed_requirements"][0])

    def test_blueprint_validator_blocks_empty_blueprint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            blueprint_path = root / "blueprints.json"
            content_path = root / "content.json"
            output_path = root / "blueprint-report.json"
            blueprint_path.write_text(json.dumps({"slides": []}), encoding="utf-8")
            content_path.write_text(json.dumps({"atoms": []}), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-slide-blueprints.py"),
                    "--blueprints",
                    str(blueprint_path),
                    "--content-atoms",
                    str(content_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(any(item["code"] == "EMPTY_BLUEPRINT" for item in report["findings"]))

    def test_blueprint_validator_blocks_non_contiguous_or_out_of_order_sequence(self) -> None:
        cases = {
            "gap": [1, 3],
            "out-of-order": [2, 1],
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            content_path = root / "content.json"
            content_path.write_text(json.dumps({"schema_version": "1.0", "atoms": []}), encoding="utf-8")
            for case_name, slide_numbers in cases.items():
                with self.subTest(case=case_name):
                    blueprint_path = root / f"blueprints-{case_name}.json"
                    output_path = root / f"blueprint-report-{case_name}.json"
                    blueprint_path.write_text(
                        json.dumps(
                            {
                                "schema_version": "1.0",
                                "deck_id": "sequence-test",
                                "slides": [
                                    {
                                        "slide_id": f"slide-{index + 1:03d}",
                                        "slide_number": slide_number,
                                        "role": "TITLE" if index == 0 else "CLOSING",
                                        "assertion_title": f"Slide {slide_number}",
                                        "primary_claim": f"Claim {slide_number}",
                                        "source_atoms": [],
                                        "visual_job": "SET_CONTEXT" if index == 0 else "CLOSE",
                                    }
                                    for index, slide_number in enumerate(slide_numbers)
                                ],
                            }
                        ),
                        encoding="utf-8",
                    )
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(SKILL_ROOT / "scripts" / "validate-slide-blueprints.py"),
                            "--blueprints",
                            str(blueprint_path),
                            "--content-atoms",
                            str(content_path),
                            "--output",
                            str(output_path),
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    report = json.loads(output_path.read_text(encoding="utf-8"))
                    self.assertTrue(any(item["code"] == "BLUEPRINT_SLIDE_SEQUENCE_INVALID" for item in report["findings"]))

    def test_archive_inspection_blocks_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            archive_path = root / "unsafe.zip"
            report_path = root / "archive-report.json"
            extraction_path = root / "extract"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../outside.txt", "blocked")
            result = run_pwsh(
                "inspect-archive.ps1",
                "-ArchivePath",
                str(archive_path),
                "-OutputPath",
                str(report_path),
                "-ExtractionDirectory",
                str(extraction_path),
                "-Extract",
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("BLOCKED", report["status"])
            self.assertTrue(any(item["code"] == "ARCHIVE_PATH_TRAVERSAL" for item in report["risks"]))
            self.assertFalse((root / "outside.txt").exists())
            self.assertFalse(extraction_path.exists())

    def test_archive_inspection_extracts_safe_zip(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            archive_path = root / "safe.zip"
            report_path = root / "archive-report.json"
            extraction_path = root / "extract"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("content/brief.txt", "slide brief")
            result = run_pwsh(
                "inspect-archive.ps1",
                "-ArchivePath",
                str(archive_path),
                "-OutputPath",
                str(report_path),
                "-ExtractionDirectory",
                str(extraction_path),
                "-Extract",
            )
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("PASS", report["status"])
            extracted = extraction_path / "content" / "brief.txt"
            self.assertEqual("slide brief", extracted.read_text(encoding="utf-8"))
            self.assertTrue(any(item["kind"] == "ARCHIVE_MEMBER" for item in report["artifacts"]))

    def test_apply_motion_rejects_certificate_for_different_static_deck(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            static_deck = root / "static.pptx"
            output_deck = root / "motion.pptx"
            storyboard = root / "storyboard.json"
            certificate = root / "static-certificate.json"
            report = root / "motion-report.json"
            static_deck.write_bytes(b"not-a-real-deck")
            storyboard.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": True,
                        "slides": [{"slide": 1, "transition": "fade_smoothly", "beats": []}],
                    }
                ),
                encoding="utf-8",
            )
            certificate.write_text(
                json.dumps({"status": "PASS", "output_sha256": "0" * 64}),
                encoding="utf-8",
            )
            result = run_pwsh(
                "apply-motion.ps1",
                "-InputPath",
                str(static_deck),
                "-OutputPath",
                str(output_deck),
                "-StoryboardPath",
                str(storyboard),
                "-StaticCertificationPath",
                str(certificate),
                "-ReportPath",
                str(report),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(report.read_text(encoding="utf-8-sig"))
            self.assertEqual("STATIC_CERTIFICATE_DECK_HASH_MISMATCH", payload["error"])
            self.assertFalse(output_deck.exists())

    def test_apply_motion_rejects_forged_static_quality_contract(self) -> None:
        _, certified = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        static_deck = Path(str(certified["output_path"]))
        cases = [
            (
                "source-formula",
                lambda payload: payload["certification_rules"].__setitem__(
                    "source_hash_formula", "FORGED"
                ),
                "STATIC_CERTIFICATE_POLICY_MISMATCH:source_hash_formula",
            ),
            (
                "formula",
                lambda payload: payload["certification_rules"].__setitem__(
                    "quality_score_formula", "FORGED"
                ),
                "STATIC_CERTIFICATE_POLICY_MISMATCH:quality_score_formula",
            ),
            (
                "calculated-score",
                lambda payload: payload.__setitem__("calculated_quality_score", 100),
                "STATIC_CERTIFICATE_QUALITY_SCORE_MISMATCH",
            ),
            (
                "source-set-hash",
                lambda payload: (
                    payload.__setitem__("source_hash_before", "b" * 64),
                    payload.__setitem__("source_hash_after", "b" * 64),
                ),
                "STATIC_CERTIFICATE_SOURCE_SET_HASH_MISMATCH",
            ),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            storyboard = root / "storyboard.json"
            storyboard.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": True,
                        "slides": [{"slide": 1, "transition": "fade_smoothly", "beats": []}],
                    }
                ),
                encoding="utf-8",
            )
            for index, (case_name, tamper, expected_error) in enumerate(cases):
                with self.subTest(case=case_name):
                    payload = json.loads(json.dumps(certified))
                    tamper(payload)
                    certificate = root / f"certificate-{index}.json"
                    output_deck = root / f"motion-{index}.pptx"
                    report = root / f"motion-report-{index}.json"
                    certificate.write_text(json.dumps(payload), encoding="utf-8")
                    result = run_pwsh(
                        "apply-motion.ps1",
                        "-InputPath",
                        str(static_deck),
                        "-OutputPath",
                        str(output_deck),
                        "-StoryboardPath",
                        str(storyboard),
                        "-StaticCertificationPath",
                        str(certificate),
                        "-ReportPath",
                        str(report),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    motion_report = json.loads(report.read_text(encoding="utf-8-sig"))
                    self.assertEqual(expected_error, motion_report["error"])
                    self.assertFalse(output_deck.exists())

    def test_apply_motion_rejects_future_static_receipt(self) -> None:
        _, certified = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        static_deck = Path(str(certified["output_path"]))
        receipt_binding = certified["evidence_receipts"]["all_slides_rendered"]
        receipt_path = Path(str(receipt_binding["path"]))
        receipt_payload = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt_payload["generated_at"] = "2999-01-01T00:00:00Z"
        receipt_path.write_text(json.dumps(receipt_payload), encoding="utf-8")
        receipt_binding["sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            certificate = root / "static-certificate.json"
            storyboard = root / "storyboard.json"
            output_deck = root / "motion.pptx"
            report = root / "motion-report.json"
            certificate.write_text(json.dumps(certified), encoding="utf-8")
            storyboard.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": True,
                        "slides": [{"slide": 1, "transition": "fade_smoothly", "beats": []}],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "apply-motion.ps1",
                "-InputPath", str(static_deck),
                "-OutputPath", str(output_deck),
                "-StoryboardPath", str(storyboard),
                "-StaticCertificationPath", str(certificate),
                "-ReportPath", str(report),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            motion_report = json.loads(report.read_text(encoding="utf-8-sig"))
            self.assertEqual(
                "STATIC_CERTIFICATE_RECEIPT_TIMESTAMP_IN_FUTURE:all_slides_rendered",
                motion_report["error"],
            )
            self.assertFalse(output_deck.exists())

    def test_apply_motion_rejects_static_receipt_older_than_deck(self) -> None:
        _, certified = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        static_deck = Path(str(certified["output_path"]))
        receipt_binding = certified["evidence_receipts"]["all_slides_rendered"]
        receipt_path = Path(str(receipt_binding["path"]))
        receipt_payload = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt_payload["generated_at"] = "2000-01-01T00:00:00Z"
        receipt_path.write_text(json.dumps(receipt_payload), encoding="utf-8")
        receipt_binding["sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            certificate = root / "static-certificate.json"
            storyboard = root / "storyboard.json"
            output_deck = root / "motion.pptx"
            report = root / "motion-report.json"
            certificate.write_text(json.dumps(certified), encoding="utf-8")
            storyboard.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": True,
                        "slides": [{"slide": 1, "transition": "fade_smoothly", "beats": []}],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "apply-motion.ps1",
                "-InputPath", str(static_deck),
                "-OutputPath", str(output_deck),
                "-StoryboardPath", str(storyboard),
                "-StaticCertificationPath", str(certificate),
                "-ReportPath", str(report),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            motion_report = json.loads(report.read_text(encoding="utf-8-sig"))
            self.assertEqual(
                "STATIC_CERTIFICATE_RECEIPT_TIMESTAMP_PREDATES_DECK:all_slides_rendered",
                motion_report["error"],
            )
            self.assertFalse(output_deck.exists())

    def test_compare_renders_blocks_empty_render_sets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline = root / "baseline"
            candidate = root / "candidate"
            baseline.mkdir()
            candidate.mkdir()
            output = root / "render-report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "compare-renders.py"),
                    "--baseline-dir",
                    str(baseline),
                    "--candidate-dir",
                    str(candidate),
                    "--output",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertTrue(any(item["code"] == "RENDER_SET_EMPTY" for item in payload["findings"]))

    def test_compare_renders_rejects_nan_threshold_and_nested_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline = root / "baseline"
            candidate = root / "candidate"
            baseline.mkdir()
            candidate.mkdir()
            output = root / "render-report.json"
            invalid_threshold = subprocess.run(
                [sys.executable, str(SKILL_ROOT / "scripts" / "compare-renders.py"),
                 "--baseline-dir", str(baseline), "--candidate-dir", str(candidate),
                 "--output", str(output), "--max-different-ratio", "NaN"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(2, invalid_threshold.returncode, invalid_threshold.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("INVALID_RENDER_THRESHOLD", payload["error"])

            nested_output = baseline / "report.json"
            nested = subprocess.run(
                [sys.executable, str(SKILL_ROOT / "scripts" / "compare-renders.py"),
                 "--baseline-dir", str(baseline), "--candidate-dir", str(candidate),
                 "--output", str(nested_output)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(2, nested.returncode, nested.stderr)
            self.assertFalse(nested_output.exists())

    def test_node_audits_reject_source_output_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.json"
            other = root / "other.json"
            source.write_text("{}", encoding="utf-8")
            other.write_text("{}", encoding="utf-8")
            cases = [
                ("audit-icon-consistency.mjs", ["--assets", str(source), "--registry", str(other), "--output", str(source)]),
                ("audit-visual-coverage.mjs", ["--blueprints", str(source), "--assets", str(other), "--output", str(source)]),
            ]
            for script, arguments in cases:
                with self.subTest(script=script):
                    source.write_text("{}", encoding="utf-8")
                    result = subprocess.run(
                        ["node", str(SKILL_ROOT / "scripts" / script), *arguments],
                        text=True, capture_output=True, check=False,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    self.assertEqual("{}", source.read_text(encoding="utf-8"))

    def test_visual_coverage_requires_native_shape_binding_for_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            blueprints = root / "blueprints.json"
            assets = root / "assets.json"
            layout = root / "layout.json"
            deck = root / "deck.pptx"
            deck.write_bytes(b"native-deck")
            deck_hash = hashlib.sha256(deck.read_bytes()).hexdigest()
            blueprints.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "deck_id": "test-deck",
                        "slides": [
                            {
                                "slide_id": "slide-001",
                                "slide_number": 1,
                                "role": "INSIGHT",
                                "visual_anchor": {
                                    "kind": "PHOTO",
                                    "asset_or_object_ids": ["asset-001"],
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            assets.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "assets": [
                            {
                                "asset_id": "asset-001",
                                "slide_number": 1,
                                "kind": "PHOTO",
                                "role": "CONTEXT",
                                "native_object_name": "asset-001",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            layout.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "deck_path": str(deck),
                        "deck_sha256": deck_hash,
                        "deck_sha256_before": deck_hash,
                        "deck_sha256_after": deck_hash,
                        "slide_count": 1,
                        "slide_size_points": {"width": 960, "height": 540},
                        "findings": [],
                        "slides": [
                            {
                                "slide": 1,
                                "shape_count": 1,
                                "objects": [{"name": "different-object"}],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            output = root / "coverage.json"
            result = subprocess.run(
                [
                    "node",
                    str(SKILL_ROOT / "scripts" / "audit-visual-coverage.mjs"),
                    "--blueprints", str(blueprints),
                    "--assets", str(assets),
                    "--layout-report", str(layout),
                    "--require-native-bindings",
                    "--output", str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", payload["status"])
            self.assertEqual(
                hashlib.sha256(layout.read_bytes()).hexdigest(),
                payload["native_layout_report_sha256"],
            )
            self.assertEqual(
                hashlib.sha256(blueprints.read_bytes()).hexdigest(),
                payload["blueprints_sha256"],
            )
            self.assertEqual(
                hashlib.sha256(assets.read_bytes()).hexdigest(),
                payload["assets_sha256"],
            )
            self.assertTrue(
                any(
                    item["code"] == "VISUAL_ANCHOR_NATIVE_OBJECT_MISSING"
                    for item in payload["findings"]
                )
            )

    def test_visual_coverage_marks_missing_native_report_unverified(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            blueprints = root / "blueprints.json"
            assets = root / "assets.json"
            output = root / "coverage.json"
            blueprints.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "deck_id": "test-deck",
                        "slides": [
                            {
                                "slide_id": "slide-001",
                                "slide_number": 1,
                                "role": "TITLE",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            assets.write_text(
                json.dumps({"schema_version": "1.0", "assets": []}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    "node",
                    str(SKILL_ROOT / "scripts" / "audit-visual-coverage.mjs"),
                    "--blueprints", str(blueprints),
                    "--assets", str(assets),
                    "--require-native-bindings",
                    "--output", str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(3, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("UNVERIFIED", payload["status"])
            self.assertTrue(
                any(
                    item["code"] == "NATIVE_LAYOUT_REPORT_MISSING"
                    for item in payload["findings"]
                )
            )

    def test_visual_coverage_rejects_unversioned_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            blueprints = root / "blueprints.json"
            assets = root / "assets.json"
            output = root / "coverage.json"
            blueprints.write_text(
                json.dumps(
                    {
                        "slides": [
                            {
                                "slide_id": "slide-001",
                                "slide_number": 1,
                                "role": "TITLE",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            assets.write_text(json.dumps({"assets": []}), encoding="utf-8")
            result = subprocess.run(
                [
                    "node",
                    str(SKILL_ROOT / "scripts" / "audit-visual-coverage.mjs"),
                    "--blueprints", str(blueprints),
                    "--assets", str(assets),
                    "--output", str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", payload["status"])
            codes = {finding["code"] for finding in payload["findings"]}
            self.assertIn("BLUEPRINT_SCHEMA_VERSION_INVALID", codes)
            self.assertIn("VISUAL_ASSETS_SCHEMA_VERSION_INVALID", codes)

    def test_visual_coverage_rejects_duplicate_slide_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            blueprints = root / "blueprints.json"
            assets = root / "assets.json"
            output = root / "coverage.json"
            blueprints.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "deck_id": "test-deck",
                        "slides": [
                            {"slide_id": "slide-001", "slide_number": 1, "role": "TITLE"},
                            {"slide_id": "slide-002", "slide_number": 1, "role": "CLOSING"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            assets.write_text(
                json.dumps({"schema_version": "1.0", "assets": []}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    "node",
                    str(SKILL_ROOT / "scripts" / "audit-visual-coverage.mjs"),
                    "--blueprints", str(blueprints),
                    "--assets", str(assets),
                    "--output", str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertTrue(
                any(
                    finding["code"] == "BLUEPRINT_SLIDE_SEQUENCE_INVALID"
                    for finding in payload["findings"]
                )
            )

    def test_visual_coverage_accepts_consistent_native_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            deck = root / "deck.pptx"
            blueprints = root / "blueprints.json"
            assets = root / "assets.json"
            layout = root / "layout.json"
            output = root / "coverage.json"
            deck.write_bytes(b"native-deck")
            deck_hash = hashlib.sha256(deck.read_bytes()).hexdigest()
            blueprints.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "deck_id": "test-deck",
                        "slides": [
                            {"slide_id": "slide-001", "slide_number": 1, "role": "TITLE"},
                            {
                                "slide_id": "slide-002",
                                "slide_number": 2,
                                "role": "INSIGHT",
                                "visual_anchor": {
                                    "kind": "PHOTO",
                                    "asset_or_object_ids": ["asset-002"],
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            assets.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "assets": [
                            {
                                "asset_id": "asset-002",
                                "slide_number": 2,
                                "kind": "PHOTO",
                                "role": "CONTEXT",
                                "native_object_name": "asset-002",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            layout.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "deck_path": str(deck),
                        "deck_sha256": deck_hash,
                        "deck_sha256_before": deck_hash,
                        "deck_sha256_after": deck_hash,
                        "slide_count": 2,
                        "slide_size_points": {"width": 960, "height": 540},
                        "findings": [],
                        "slides": [
                            {"slide": 1, "shape_count": 0, "objects": []},
                            {
                                "slide": 2,
                                "shape_count": 1,
                                "objects": [{"name": "asset-002"}],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    "node",
                    str(SKILL_ROOT / "scripts" / "audit-visual-coverage.mjs"),
                    "--blueprints", str(blueprints),
                    "--assets", str(assets),
                    "--layout-report", str(layout),
                    "--require-native-bindings",
                    "--output", str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("PASS", payload["status"])
            self.assertIs(payload["native_bindings_required"], True)
            self.assertIs(payload["native_bindings_verified"], True)
            self.assertEqual(deck_hash, payload["native_deck_sha256"])

    def test_visual_coverage_rejects_inconsistent_native_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            deck = root / "deck.pptx"
            blueprints = root / "blueprints.json"
            assets = root / "assets.json"
            deck.write_bytes(b"native-deck")
            deck_hash = hashlib.sha256(deck.read_bytes()).hexdigest()
            blueprints_payload = {
                "schema_version": "1.0",
                "deck_id": "test-deck",
                "slides": [
                    {"slide_id": "slide-001", "slide_number": 1, "role": "TITLE"},
                    {
                        "slide_id": "slide-002",
                        "slide_number": 2,
                        "role": "INSIGHT",
                        "visual_anchor": {
                            "kind": "PHOTO",
                            "asset_or_object_ids": ["asset-002"],
                        },
                    },
                ],
            }
            assets_payload = {
                "schema_version": "1.0",
                "assets": [
                    {
                        "asset_id": "asset-002",
                        "slide_number": 2,
                        "kind": "PHOTO",
                        "role": "CONTEXT",
                        "native_object_name": "asset-002",
                    }
                ],
            }
            layout_payload = {
                "schema_version": "1.0",
                "status": "PASS",
                "deck_path": str(deck),
                "deck_sha256": deck_hash,
                "deck_sha256_before": deck_hash,
                "deck_sha256_after": deck_hash,
                "slide_count": 2,
                "slide_size_points": {"width": 960, "height": 540},
                "findings": [],
                "slides": [
                    {"slide": 1, "shape_count": 0, "objects": []},
                    {
                        "slide": 2,
                        "shape_count": 1,
                        "objects": [{"name": "asset-002"}],
                    },
                ],
            }

            def clone(value: object) -> object:
                return json.loads(json.dumps(value))

            cases: list[tuple[str, dict[str, object], dict[str, object], str]] = []
            invalid_layout = clone(layout_payload)
            invalid_layout["deck_sha256"] = "b" * 64
            cases.append(("deck-hash-field", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_DECK_HASH_INVALID"))
            invalid_layout = clone(layout_payload)
            invalid_layout["deck_path"] = ""
            cases.append(("deck-path", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_DECK_PATH_INVALID"))
            invalid_layout = clone(layout_payload)
            invalid_layout["deck_sha256"] = "b" * 64
            invalid_layout["deck_sha256_before"] = "b" * 64
            invalid_layout["deck_sha256_after"] = "b" * 64
            cases.append(("actual-deck-hash", invalid_layout, clone(assets_payload), "NATIVE_DECK_HASH_MISMATCH"))
            invalid_layout = clone(layout_payload)
            invalid_layout["slide_count"] = 3
            invalid_layout["slides"].append({"slide": 3, "shape_count": 0, "objects": []})
            cases.append(("blueprint-layout-count", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_BLUEPRINT_SLIDE_COUNT_MISMATCH"))
            invalid_layout = clone(layout_payload)
            del invalid_layout["slides"][0]["objects"]
            cases.append(("objects-array", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_OBJECTS_INVALID"))
            invalid_layout = clone(layout_payload)
            invalid_layout["slides"][1]["shape_count"] = 2
            cases.append(("shape-count", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_SHAPE_COUNT_MISMATCH"))
            invalid_layout = clone(layout_payload)
            invalid_layout["slides"][1]["shape_count"] = 2
            invalid_layout["slides"][1]["objects"].append({"name": "ASSET-002"})
            cases.append(("duplicate-object", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_OBJECT_NAME_DUPLICATE"))
            invalid_layout = clone(layout_payload)
            invalid_layout["slides"][1]["shape_count"] = 2
            invalid_layout["slides"][1]["objects"].append({"name": "   "})
            cases.append(("blank-object", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_OBJECT_NAME_INVALID"))
            invalid_layout = clone(layout_payload)
            invalid_layout["findings"] = [None]
            cases.append(("finding-record", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_FINDING_RECORD_INVALID"))
            invalid_layout = clone(layout_payload)
            invalid_layout["findings"] = [{"severity": "P2"}]
            cases.append(("finding-fields", invalid_layout, clone(assets_payload), "NATIVE_LAYOUT_FINDING_RECORD_INVALID"))
            invalid_assets = clone(assets_payload)
            invalid_assets["assets"].append(
                {
                    "asset_id": "asset-out-of-range",
                    "slide_number": 99,
                    "kind": "PHOTO",
                    "role": "CONTEXT",
                }
            )
            cases.append(("asset-slide-range", clone(layout_payload), invalid_assets, "VISUAL_ASSET_SLIDE_NUMBER_INVALID"))

            blueprints.write_text(json.dumps(blueprints_payload), encoding="utf-8")
            for index, (case_name, candidate_layout, candidate_assets, expected_code) in enumerate(cases):
                with self.subTest(case=case_name):
                    layout = root / f"layout-{index}.json"
                    assets_case = root / f"assets-{index}.json"
                    output = root / f"coverage-{index}.json"
                    layout.write_text(json.dumps(candidate_layout), encoding="utf-8")
                    assets_case.write_text(json.dumps(candidate_assets), encoding="utf-8")
                    result = subprocess.run(
                        [
                            "node",
                            str(SKILL_ROOT / "scripts" / "audit-visual-coverage.mjs"),
                            "--blueprints", str(blueprints),
                            "--assets", str(assets_case),
                            "--layout-report", str(layout),
                            "--require-native-bindings",
                            "--output", str(output),
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    payload = json.loads(output.read_text(encoding="utf-8"))
                    self.assertEqual("BLOCKED", payload["status"])
                    self.assertTrue(
                        any(finding["code"] == expected_code for finding in payload["findings"]),
                        payload,
                    )

    def test_python_and_node_safe_io_reject_reparse_output_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            target = root / "target"
            junction = root / "junction"
            target.mkdir()
            create = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                text=True, capture_output=True, check=False,
            )
            if create.returncode != 0:
                self.skipTest(f"Junction unavailable: {create.stderr}")
            try:
                ledger = root / "ledger.json"
                assets = root / "assets.json"
                registry = root / "registry.json"
                ledger.write_text('{"metrics":[]}', encoding="utf-8")
                assets.write_text('{"assets":[]}', encoding="utf-8")
                registry.write_text('{"icons":{}}', encoding="utf-8")

                python_output = junction / "python-report.json"
                python_result = subprocess.run(
                    [
                        sys.executable,
                        str(SKILL_ROOT / "scripts" / "validate-data.py"),
                        "--input", str(ledger),
                        "--output", str(python_output),
                    ],
                    text=True, capture_output=True, check=False,
                )

                node_output = junction / "node-report.json"
                node_result = subprocess.run(
                    [
                        "node",
                        str(SKILL_ROOT / "scripts" / "audit-icon-consistency.mjs"),
                        "--assets", str(assets),
                        "--registry", str(registry),
                        "--output", str(node_output),
                    ],
                    text=True, capture_output=True, check=False,
                )
                cases = [
                    ("python", python_result, target / "python-report.json"),
                    ("node", node_result, target / "node-report.json"),
                ]
                for runtime, result, resolved_output in cases:
                    with self.subTest(runtime=runtime):
                        self.assertEqual(2, result.returncode, result.stderr)
                        self.assertFalse(resolved_output.exists())
            finally:
                if junction.exists():
                    junction.rmdir()

    def test_python_and_node_json_consumers_reject_reparse_input_ancestors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            target = root / "target"
            junction = root / "junction"
            target.mkdir()
            create = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            if create.returncode != 0:
                self.skipTest(f"Junction unavailable: {create.stderr}")
            try:
                ledger = target / "ledger.json"
                registry = root / "registry.json"
                ledger.write_text('{"metrics":[]}', encoding="utf-8")
                registry.write_text('{"icons":{},"semantic_registry":{}}', encoding="utf-8")
                cases = [
                    (
                        "python",
                        [
                            sys.executable,
                            str(SKILL_ROOT / "scripts" / "validate-data.py"),
                            "--input",
                            str(junction / "ledger.json"),
                            "--output",
                            str(root / "python-report.json"),
                        ],
                        root / "python-report.json",
                    ),
                    (
                        "node",
                        [
                            "node",
                            str(SKILL_ROOT / "scripts" / "audit-icon-consistency.mjs"),
                            "--assets",
                            str(junction / "ledger.json"),
                            "--registry",
                            str(registry),
                            "--output",
                            str(root / "node-report.json"),
                        ],
                        root / "node-report.json",
                    ),
                ]
                for runtime, command, output_path in cases:
                    with self.subTest(runtime=runtime):
                        result = subprocess.run(command, text=True, capture_output=True, check=False)
                        self.assertEqual(2, result.returncode, result.stderr)
                        if output_path.exists():
                            payload = json.loads(output_path.read_text(encoding="utf-8-sig"))
                            self.assertEqual("BLOCKED", payload["status"])
            finally:
                if junction.exists():
                    junction.rmdir()

    def test_python_and_node_json_consumers_block_ambiguous_or_malformed_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry = root / "registry.json"
            registry.write_text('{"icons":{},"semantic_registry":{}}', encoding="utf-8")
            cases = [
                (
                    "python-duplicate",
                    '{"metrics":[],"metrics":[]}',
                    [sys.executable, str(SKILL_ROOT / "scripts" / "validate-data.py")],
                    ["--input", "{input}", "--output", "{output}"],
                ),
                (
                    "python-malformed",
                    '{"metrics":[}',
                    [sys.executable, str(SKILL_ROOT / "scripts" / "validate-data.py")],
                    ["--input", "{input}", "--output", "{output}"],
                ),
                (
                    "node-duplicate",
                    '{"assets":[],"assets":[]}',
                    ["node", str(SKILL_ROOT / "scripts" / "audit-icon-consistency.mjs")],
                    ["--assets", "{input}", "--registry", str(registry), "--output", "{output}"],
                ),
                (
                    "node-malformed",
                    '{"assets":[}',
                    ["node", str(SKILL_ROOT / "scripts" / "audit-icon-consistency.mjs")],
                    ["--assets", "{input}", "--registry", str(registry), "--output", "{output}"],
                ),
            ]
            for index, (case_name, content, command, arguments) in enumerate(cases):
                with self.subTest(case=case_name):
                    input_path = root / f"input-{index}.json"
                    output_path = root / f"output-{index}.json"
                    input_path.write_text(content, encoding="utf-8")
                    rendered_arguments = [
                        value.format(input=str(input_path), output=str(output_path))
                        for value in arguments
                    ]
                    result = subprocess.run(
                        [*command, *rendered_arguments],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    payload = json.loads(output_path.read_text(encoding="utf-8-sig"))
                    self.assertEqual("BLOCKED", payload["status"])

    def test_json_readers_reject_files_larger_than_64_mib_before_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            oversized = root / "oversized.json"
            with oversized.open("wb") as stream:
                stream.truncate(64 * 1024 * 1024 + 1)
            python_environment = os.environ.copy()
            python_environment["PYTHONPATH"] = str(SKILL_ROOT / "scripts")
            commands = [
                (
                    "python",
                    [
                        sys.executable,
                        "-c",
                        f"from safe_io import load_json_strict; load_json_strict(r'{oversized}')",
                    ],
                    python_environment,
                ),
                (
                    "node",
                    [
                        "node",
                        "--input-type=module",
                        "-e",
                        (
                            f"import {{ loadJsonStrict }} from '{(SKILL_ROOT / 'scripts' / 'safe-io.mjs').as_uri()}';"
                            f"await loadJsonStrict({json.dumps(str(oversized))});"
                        ),
                    ],
                    None,
                ),
                (
                    "powershell",
                    [
                        "pwsh",
                        "-NoLogo",
                        "-NoProfile",
                        "-Command",
                        f". '{SKILL_ROOT / 'scripts' / 'common.ps1'}'; Read-JsonFile -Path '{oversized}'",
                    ],
                    None,
                ),
            ]
            for runtime, command, environment in commands:
                with self.subTest(runtime=runtime):
                    result = subprocess.run(
                        command,
                        text=True,
                        capture_output=True,
                        check=False,
                        env=environment,
                    )
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("JSON_INPUT_TOO_LARGE", result.stdout + result.stderr)

    def test_release_certificate_schema_requires_gate_evidence_and_domains(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            input_path = root / "certificate.json"
            output_path = root / "schema-report.json"
            input_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "generated_at": "2026-08-26T00:00:00+00:00",
                        "status": "PASS",
                        "quality_score": 98,
                        "domain_scores": {},
                        "findings": [],
                        "failed_requirements": [],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-json.py"),
                    "--input",
                    str(input_path),
                    "--schema",
                    "release-certificate.schema.json",
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertGreater(report["error_count"], 0)

    def test_release_schemas_require_bound_receipts_and_reject_unknown_fields(self) -> None:
        release_input_schema = json.loads(
            (SKILL_ROOT / "schemas" / "release-input.schema.json").read_text(encoding="utf-8")
        )
        self.assertIn("source_bindings", release_input_schema["required"])
        self.assertIn("evidence_receipts", release_input_schema["required"])
        self.assertFalse(release_input_schema["additionalProperties"])
        self.assertFalse(release_input_schema["properties"]["domain_scores"]["additionalProperties"])

        certificate_schema = json.loads(
            (SKILL_ROOT / "schemas" / "release-certificate.schema.json").read_text(encoding="utf-8")
        )
        for field in [
            "source_bindings",
            "output_detected_format",
            "evidence_receipts",
            "blocking_requirements",
            "unverified_requirements",
        ]:
            self.assertIn(field, certificate_schema["required"])

    def test_generated_release_certificate_validates_against_schema(self) -> None:
        _, certificate = self._certify(findings=[])
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            certificate_path = root / "certificate.json"
            report_path = root / "schema-report.json"
            certificate_path.write_text(json.dumps(certificate), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-json.py"),
                    "--input", str(certificate_path),
                    "--schema", "release-certificate",
                    "--output", str(report_path),
                ],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual("PASS", report["status"])

    def test_generated_static_certificate_validates_against_schema(self) -> None:
        _, certificate = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            certificate_path = root / "certificate.json"
            report_path = root / "schema-report.json"
            certificate_path.write_text(json.dumps(certificate), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-json.py"),
                    "--input", str(certificate_path),
                    "--schema", "release-certificate",
                    "--output", str(report_path),
                ],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual("PASS", report["status"])

    def test_generated_native_reports_validate_against_schemas(self) -> None:
        _, certificate = self._certify(findings=[])
        coverage_path = Path(
            certificate["evidence_receipts"]["visual_assets_verified"]["metadata"]
            ["native_visual_coverage_report_path"]
        )
        coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
        layout_path = Path(coverage["native_layout_report_path"])
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for index, (artifact, schema_name) in enumerate(
                (
                    (layout_path, "native-layout-report"),
                    (coverage_path, "native-visual-coverage-report"),
                )
            ):
                report_path = root / f"schema-report-{index}.json"
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SKILL_ROOT / "scripts" / "validate-json.py"),
                        "--input", str(artifact),
                        "--schema", schema_name,
                        "--output", str(report_path),
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr or result.stdout)
                report = json.loads(report_path.read_text(encoding="utf-8"))
                self.assertEqual("PASS", report["status"])

    def test_pass_certificate_schema_rejects_semantic_contradictions(self) -> None:
        _, certificate = self._certify(findings=[])
        cases = [
            (
                "critical-finding",
                lambda payload: payload["findings"].append(
                    {"severity": "P1", "code": "UNRESOLVED_ISSUE", "detail": "must block"}
                ),
            ),
            (
                "receipt-not-pass",
                lambda payload: payload["evidence_receipts"]["all_slides_rendered"].update(
                    {"status": "UNVERIFIED", "check_count": 0}
                ),
            ),
            (
                "missing-source-binding",
                lambda payload: payload.__setitem__("source_bindings", []),
            ),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for index, (case_name, tamper) in enumerate(cases):
                with self.subTest(case=case_name):
                    payload = json.loads(json.dumps(certificate))
                    tamper(payload)
                    certificate_path = root / f"certificate-{index}.json"
                    report_path = root / f"schema-report-{index}.json"
                    certificate_path.write_text(json.dumps(payload), encoding="utf-8")
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(SKILL_ROOT / "scripts" / "validate-json.py"),
                            "--input", str(certificate_path),
                            "--schema", "release-certificate",
                            "--output", str(report_path),
                        ],
                        text=True, capture_output=True, check=False,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    report = json.loads(report_path.read_text(encoding="utf-8"))
                    self.assertEqual("BLOCKED", report["status"])
                    self.assertGreater(report["error_count"], 0)

    def test_run_pipeline_records_source_hash_and_gate_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_path = root / "source.txt"
            job_contract_path = root / "job-contract.json"
            workspace = root / "run"
            source_path.write_text("Source-backed strategy content", encoding="utf-8")
            self._write_job_contract(job_contract_path)
            result = run_pwsh(
                "run-pipeline.ps1",
                "-InputPath",
                str(source_path),
                "-JobContractPath",
                str(job_contract_path),
                "-Workspace",
                str(workspace),
                "-SkipPreflight",
            )
            self.assertEqual(3, result.returncode, result.stderr)
            manifest = json.loads((workspace / "run-manifest.json").read_text(encoding="utf-8-sig"))
            self.assertTrue(manifest["source_hash_unchanged"])
            self.assertEqual(manifest["source_hash_before"], manifest["source_hash_after"])
            self.assertEqual("INTAKE_UNVERIFIED", manifest["state"])
            self.assertEqual("INTAKE_BOOTSTRAP_ONLY", manifest["pipeline_scope"])
            self.assertEqual("G3_FORMAT_ADAPTERS", manifest["next_gate"])
            self.assertFalse(manifest["release_certified"])
            expected_job_contract_hash = hashlib.sha256(job_contract_path.read_bytes()).hexdigest()
            self.assertEqual(expected_job_contract_hash, manifest["job_contract_hash_before"])
            self.assertEqual(expected_job_contract_hash, manifest["job_contract_hash_after"])
            self.assertTrue(manifest["job_contract_hash_unchanged"])
            self.assertEqual(
                [
                    "G0_JOB_CONTRACT",
                    "G1_CAPABILITY",
                    "G2_SOURCE_INVENTORY",
                    "G2_ROUTING_DECISION",
                ],
                [checkpoint["stage"] for checkpoint in manifest["job_contract_hash_checkpoints"]],
            )
            self.assertEqual(
                [
                    "G0_JOB_CONTRACT",
                    "G1_CAPABILITY",
                    "G2_SOURCE_INVENTORY",
                    "G2_SOURCE_INVENTORY_SCHEMA",
                    "G2_ROUTING_DECISION",
                    "G2_ROUTING_DECISION_SCHEMA",
                ],
                [gate["gate"] for gate in manifest["gates"]],
            )
            self.assertTrue(all(gate["status"] == "PASS" for gate in manifest["gates"] if gate["gate"] != "G1_CAPABILITY"))
            self.assertEqual("UNVERIFIED", manifest["gates"][1]["status"])
            self.assertEqual("PASS", json.loads((workspace / "job-contract-validation.json").read_text(encoding="utf-8"))["status"])
            routing_schema_report = json.loads(
                (workspace / "routing-decision.validation.json").read_text(encoding="utf-8")
            )
            self.assertEqual("PASS", routing_schema_report["status"])
            inventory_schema_report = json.loads(
                (workspace / "source-inventory.validation.json").read_text(encoding="utf-8")
            )
            self.assertEqual("PASS", inventory_schema_report["status"])
            inventory_hash = hashlib.sha256((workspace / "source-inventory.json").read_bytes()).hexdigest()
            routing_hash = hashlib.sha256((workspace / "routing-decision.json").read_bytes()).hexdigest()
            self.assertEqual(inventory_hash, manifest["inventory_hash_before_routing"])
            self.assertEqual(inventory_hash, manifest["inventory_hash_after_routing"])
            self.assertTrue(manifest["inventory_hash_unchanged"])
            self.assertEqual(routing_hash, manifest["routing_hash_before_validation"])
            self.assertEqual(routing_hash, manifest["routing_hash_after_validation"])
            self.assertTrue(manifest["routing_hash_unchanged"])

    def test_run_pipeline_records_deterministic_aggregate_hash_for_multiple_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_directory = root / "sources"
            source_directory.mkdir()
            (source_directory / "a.txt").write_text("alpha", encoding="utf-8")
            (source_directory / "b.txt").write_text("beta", encoding="utf-8")
            job_contract_path = root / "job-contract.json"
            workspace = root / "run"
            self._write_job_contract(job_contract_path)
            result = run_pwsh(
                "run-pipeline.ps1",
                "-InputPath", str(source_directory),
                "-JobContractPath", str(job_contract_path),
                "-Workspace", str(workspace),
                "-SkipPreflight",
            )
            self.assertEqual(3, result.returncode, result.stderr)
            manifest = json.loads((workspace / "run-manifest.json").read_text(encoding="utf-8-sig"))
            self.assertEqual(2, len(manifest["source_hashes_before"]))
            canonical_records = []
            for source in manifest["source_hashes_before"]:
                canonical_records.append(
                    f'{source["source_id"]}\x1f{os.path.normcase(str(Path(source["path"]).resolve()))}\x1f{source["sha256"]}'
                )
            expected = hashlib.sha256("\n".join(sorted(canonical_records)).encode("utf-8")).hexdigest()
            self.assertEqual(expected, manifest["source_hash_before"])
            self.assertEqual(expected, manifest["source_hash_after"])
            self.assertEqual("SOURCE_FILE_SHA256_OR_SET_V1", manifest["source_hash_formula"])
            self.assertTrue(manifest["job_contract_hash_unchanged"])
            inventory = json.loads((workspace / "source-inventory.json").read_text(encoding="utf-8-sig"))
            self.assertEqual(len(inventory["sources"]), inventory["source_count"])

    def test_run_pipeline_binds_routing_to_job_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_path = root / "source.txt"
            job_contract_path = root / "job-contract.json"
            workspace = root / "run"
            source_path.write_text("Audit this source without rewriting it.", encoding="utf-8")
            self._write_job_contract(
                job_contract_path,
                primary_operation="AUDIT",
                modifiers=[],
                preservation_mode="CONTROLLED",
                certification_mode="STANDARD",
            )
            result = run_pwsh(
                "run-pipeline.ps1",
                "-InputPath", str(source_path),
                "-JobContractPath", str(job_contract_path),
                "-Workspace", str(workspace),
                "-SkipPreflight",
            )
            self.assertEqual(3, result.returncode, result.stderr)
            route = json.loads((workspace / "routing-decision.json").read_text(encoding="utf-8-sig"))
            contract_hash = hashlib.sha256(job_contract_path.read_bytes()).hexdigest()
            self.assertEqual("AUDIT", route["primary_operation"])
            self.assertEqual("CONTROLLED", route["preservation_mode"])
            self.assertEqual("STANDARD", route["certification_mode"])
            self.assertEqual(str(job_contract_path.resolve()), route["job_contract_path"])
            self.assertEqual(contract_hash, route["job_contract_sha256"])
            route_validation_path = root / "routing-validation.json"
            route_validation = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-json.py"),
                    "--input", str(workspace / "routing-decision.json"),
                    "--schema", "routing-decision",
                    "--output", str(route_validation_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, route_validation.returncode, route_validation.stderr)

    def test_run_pipeline_blocks_requested_operation_conflicting_with_job_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_path = root / "source.txt"
            job_contract_path = root / "job-contract.json"
            workspace = root / "run"
            source_path.write_text("Create a new deck.", encoding="utf-8")
            self._write_job_contract(job_contract_path, primary_operation="CREATE")
            result = run_pwsh(
                "run-pipeline.ps1",
                "-InputPath", str(source_path),
                "-JobContractPath", str(job_contract_path),
                "-Workspace", str(workspace),
                "-RequestedOperation", "audit",
                "-SkipPreflight",
            )
            self.assertEqual(2, result.returncode, result.stderr)
            manifest = json.loads((workspace / "run-manifest.json").read_text(encoding="utf-8-sig"))
            self.assertEqual("BLOCKED", manifest["state"])
            self.assertEqual(
                "REQUESTED_OPERATION_JOB_CONTRACT_MISMATCH:requested=AUDIT;contract=CREATE",
                manifest["error"],
            )
            self.assertFalse((workspace / "source-inventory.json").exists())

    def test_run_pipeline_never_records_pass_for_malformed_gate_artifact(self) -> None:
        malformed_python = """\
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output", required=True)
args = parser.parse_args()
Path(args.output).write_text("[]", encoding="utf-8")
print("[]")
raise SystemExit(0)
"""
        malformed_powershell = """\
param(
  [string]$InputPath,
  [string]$InventoryPath,
  [string]$JobContractPath,
  [string]$RequestedOperation,
  [string]$OutputPath,
  [string]$TargetPath,
  [string]$Mode
)
[System.IO.File]::WriteAllText($OutputPath, '[]', [System.Text.UTF8Encoding]::new($false))
Write-Output '[]'
exit 0
"""
        cases = [
            ("G0_JOB_CONTRACT", "validate-job-contract.py", malformed_python, False),
            ("G1_CAPABILITY", "preflight.ps1", malformed_powershell, False),
            ("G2_SOURCE_INVENTORY", "inventory-inputs.ps1", malformed_powershell, True),
            ("G2_ROUTING_DECISION", "route-job.ps1", malformed_powershell, True),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for index, (gate_name, script_name, script_content, skip_preflight) in enumerate(cases):
                with self.subTest(gate=gate_name):
                    skill_copy = root / f"skill-{index}"
                    shutil.copytree(SKILL_ROOT, skill_copy)
                    (skill_copy / "scripts" / script_name).write_text(script_content, encoding="utf-8")
                    source_path = root / f"source-{index}.txt"
                    contract_path = root / f"job-contract-{index}.json"
                    workspace = root / f"run-{index}"
                    source_path.write_text("Source-backed strategy content", encoding="utf-8")
                    self._write_job_contract(contract_path)
                    command = [
                        "pwsh", "-NoLogo", "-NoProfile", "-File",
                        str(skill_copy / "scripts" / "run-pipeline.ps1"),
                        "-InputPath", str(source_path),
                        "-JobContractPath", str(contract_path),
                        "-Workspace", str(workspace),
                    ]
                    if skip_preflight:
                        command.append("-SkipPreflight")
                    environment = os.environ.copy()
                    environment["RUNTIME_PYTHON"] = sys.executable
                    result = subprocess.run(
                        command,
                        text=True,
                        capture_output=True,
                        check=False,
                        env=environment,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    manifest = json.loads((workspace / "run-manifest.json").read_text(encoding="utf-8-sig"))
                    receipts = [item for item in manifest["gates"] if item["gate"] == gate_name]
                    self.assertEqual(1, len(receipts), manifest)
                    self.assertEqual("BLOCKED", receipts[0]["status"], receipts[0])
                    self.assertNotEqual(0, receipts[0]["exit_code"], receipts[0])
                    self.assertIn("ARTIFACT_VALIDATION_FAILED", receipts[0]["reason"])

    def test_run_pipeline_blocks_route_that_changes_contract_modifiers(self) -> None:
        wrapper = """\
param(
  [Parameter(Mandatory = $true)][string]$InventoryPath,
  [string]$JobContractPath,
  [string]$RequestedOperation = 'auto',
  [Parameter(Mandatory = $true)][string]$OutputPath
)
& (Join-Path $PSScriptRoot 'route-job-real.ps1') -InventoryPath $InventoryPath -JobContractPath $JobContractPath -RequestedOperation $RequestedOperation -OutputPath $OutputPath | Out-Null
$payload = Get-Content -LiteralPath $OutputPath -Raw | ConvertFrom-Json
$payload.modifiers = @('CERTIFY')
[System.IO.File]::WriteAllText($OutputPath, ($payload | ConvertTo-Json -Depth 20), [System.Text.UTF8Encoding]::new($false))
$payload | ConvertTo-Json -Depth 20
exit 0
"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_copy = root / "skill"
            shutil.copytree(SKILL_ROOT, skill_copy)
            scripts = skill_copy / "scripts"
            (scripts / "route-job.ps1").rename(scripts / "route-job-real.ps1")
            (scripts / "route-job.ps1").write_text(wrapper, encoding="utf-8")
            source_path = root / "source.txt"
            contract_path = root / "job-contract.json"
            workspace = root / "run"
            source_path.write_text("Audit source without changing it.", encoding="utf-8")
            self._write_job_contract(
                contract_path,
                primary_operation="AUDIT",
                modifiers=[],
                preservation_mode="CONTROLLED",
                certification_mode="STANDARD",
            )
            environment = os.environ.copy()
            environment["RUNTIME_PYTHON"] = sys.executable
            result = subprocess.run(
                [
                    "pwsh", "-NoLogo", "-NoProfile", "-File",
                    str(scripts / "run-pipeline.ps1"),
                    "-InputPath", str(source_path),
                    "-JobContractPath", str(contract_path),
                    "-Workspace", str(workspace),
                    "-SkipPreflight",
                ],
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            manifest = json.loads((workspace / "run-manifest.json").read_text(encoding="utf-8-sig"))
            route_receipt = next(item for item in manifest["gates"] if item["gate"] == "G2_ROUTING_DECISION")
            self.assertEqual("BLOCKED", route_receipt["status"])
            self.assertIn("ROUTE_JOB_CONTRACT_MODIFIERS_MISMATCH", route_receipt["reason"])

    def test_run_pipeline_rejects_runtime_python_script_without_executing_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_path = root / "source.txt"
            contract_path = root / "job-contract.json"
            workspace = root / "run"
            fake_python = root / "python.ps1"
            marker_path = root / "executed.txt"
            source_path.write_text("Source-backed strategy content", encoding="utf-8")
            self._write_job_contract(contract_path)
            fake_python.write_text(
                "param([Parameter(ValueFromRemainingArguments=$true)][object[]]$Remaining)\n"
                f"[System.IO.File]::WriteAllText('{marker_path}', 'executed')\n"
                "exit 0\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment["RUNTIME_PYTHON"] = str(fake_python)
            result = subprocess.run(
                [
                    "pwsh", "-NoLogo", "-NoProfile", "-File",
                    str(SKILL_ROOT / "scripts" / "run-pipeline.ps1"),
                    "-InputPath", str(source_path),
                    "-JobContractPath", str(contract_path),
                    "-Workspace", str(workspace),
                    "-SkipPreflight",
                ],
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertFalse(marker_path.exists())
            manifest = json.loads((workspace / "run-manifest.json").read_text(encoding="utf-8-sig"))
            self.assertEqual("BLOCKED", manifest["state"])
            self.assertIn("RUNTIME_PYTHON_NOT_APPLICATION", manifest["error"])

    def test_validate_job_contract_blocks_reversed_target_range(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            contract_path = root / "job-contract.json"
            output_path = root / "validation.json"
            self._write_job_contract(
                contract_path,
                slide_count_policy="TARGET_RANGE",
                target_slide_range=[20, 10],
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-job-contract.py"),
                    "--input", str(contract_path),
                    "--output", str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", report["status"])
            self.assertTrue(any(item["code"] == "TARGET_SLIDE_RANGE_REVERSED" for item in report["findings"]))

    def test_validate_job_contract_blocks_semantic_contradictions(self) -> None:
        cases = [
            (
                "locked-derivation",
                {
                    "content_change_budget": {
                        "max_semantic_change": "EQUIVALENT_ONLY",
                        "allow_derivation": True,
                        "allow_reorder": False,
                        "omission_policy": "NONE",
                        "p0_p1_omission_allowed": False,
                    }
                },
                "LOCKED_PRESERVATION_ALLOWS_DERIVATION",
            ),
            (
                "locked-sequence-change",
                {
                    "sequence_change_allowed": True,
                },
                "LOCKED_PRESERVATION_ALLOWS_SEQUENCE_CHANGE",
            ),
            (
                "motion-none",
                {"primary_operation": "MOTION", "motion_level": "NONE"},
                "MOTION_OPERATION_WITHOUT_MOTION",
            ),
            (
                "editable-pdf",
                {
                    "output_contract": {
                        "format": "PDF",
                        "editable": True,
                        "versioned": True,
                        "source_notes": "REQUIRED",
                        "evidence_package": "FULL",
                    }
                },
                "PDF_OUTPUT_CANNOT_BE_EDITABLE",
            ),
            (
                "certified-summary-evidence",
                {
                    "output_contract": {
                        "format": "PPTX",
                        "editable": True,
                        "versioned": True,
                        "source_notes": "REQUIRED",
                        "evidence_package": "SUMMARY",
                    }
                },
                "CERTIFIED_EVIDENCE_PACKAGE_NOT_FULL",
            ),
            (
                "certified-notes-optional",
                {
                    "output_contract": {
                        "format": "PPTX",
                        "editable": True,
                        "versioned": True,
                        "source_notes": "OPTIONAL",
                        "evidence_package": "FULL",
                    }
                },
                "CERTIFIED_SOURCE_NOTES_NOT_REQUIRED",
            ),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for index, (case_name, overrides, expected_code) in enumerate(cases):
                with self.subTest(case=case_name):
                    contract_path = root / f"contract-{index}.json"
                    output_path = root / f"validation-{index}.json"
                    self._write_job_contract(contract_path, **overrides)
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(SKILL_ROOT / "scripts" / "validate-job-contract.py"),
                            "--input", str(contract_path),
                            "--output", str(output_path),
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    report = json.loads(output_path.read_text(encoding="utf-8"))
                    self.assertEqual("BLOCKED", report["status"])
                    self.assertTrue(
                        any(item["code"] == expected_code for item in report["findings"]),
                        report,
                    )

    def test_job_contract_schema_requires_explicit_duration_and_modifiers(self) -> None:
        schema = json.loads(
            (SKILL_ROOT / "schemas" / "job-contract.schema.json").read_text(encoding="utf-8")
        )
        required = set(schema["required"])
        self.assertIn("duration_minutes", required)
        self.assertIn("modifiers", required)
        content_driven_rule = [
            rule
            for rule in schema["allOf"]
            if rule.get("if", {}).get("properties", {}).get("slide_count_policy", {}).get("const")
            == "CONTENT_DRIVEN"
        ]
        self.assertEqual(1, len(content_driven_rule))

    def test_reconcile_content_blocks_metric_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            atoms_path = root / "canonical-content.json"
            data_path = root / "data-ledger.json"
            output_path = root / "reconciliation.json"
            atoms_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "atoms": [
                            {
                                "atom_id": "atom-001",
                                "type": "METRIC",
                                "source_id": "source-001",
                                "locator": {"slide": 3},
                                "verbatim": "Doanh thu 10 triệu USD",
                                "normalized": {
                                    "metric_key": "revenue",
                                    "value": 10,
                                    "unit": "USD_MILLION",
                                    "period": "2030",
                                    "actual_or_forecast": "TARGET",
                                },
                                "priority": "P0",
                                "confidence": "VERIFIED",
                                "must_preserve": True,
                                "destination": "VISIBLE_SLIDE",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            data_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "metrics": [
                            {
                                "metric_id": "metric-001",
                                "metric_key": "revenue",
                                "value": 12,
                                "unit": "USD_MILLION",
                                "period": "2030",
                                "source_id": "source-002",
                                "locator": {"sheet": "Plan", "cell": "B4"},
                                "verification_status": "VERIFIED",
                                "actual_or_forecast": "TARGET",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "reconcile-content.py"),
                    "--content-atoms",
                    str(atoms_path),
                    "--data-ledger",
                    str(data_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", payload["status"])
            self.assertTrue(any(item["code"] == "CONTENT_METRIC_CONFLICT" for item in payload["findings"]))

    def test_reconcile_content_does_not_match_actual_to_forecast(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            atoms_path = root / "canonical-content.json"
            data_path = root / "data-ledger.json"
            output_path = root / "reconciliation.json"
            atoms_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "atoms": [
                            {
                                "atom_id": "atom-actual",
                                "type": "METRIC",
                                "source_id": "source-001",
                                "locator": {"slide": 2},
                                "verbatim": "Doanh thu thực tế 10 triệu USD",
                                "normalized": {
                                    "metric_key": "revenue",
                                    "value": 10,
                                    "unit": "USD_MILLION",
                                    "period": "2030",
                                    "actual_or_forecast": "ACTUAL",
                                },
                                "priority": "P0",
                                "confidence": "VERIFIED",
                                "must_preserve": True,
                                "destination": "VISIBLE_SLIDE",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            data_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "metrics": [
                            {
                                "metric_id": "metric-forecast",
                                "metric_key": "revenue",
                                "value": 10,
                                "unit": "USD_MILLION",
                                "period": "2030",
                                "source_id": "source-002",
                                "locator": {"sheet": "Plan", "cell": "B4"},
                                "verification_status": "VERIFIED",
                                "actual_or_forecast": "FORECAST",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "reconcile-content.py"),
                    "--content-atoms",
                    str(atoms_path),
                    "--data-ledger",
                    str(data_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(any(item["code"] == "CANONICAL_METRIC_NOT_IN_DATA_LEDGER" for item in payload["findings"]))

    def test_blueprint_validation_blocks_missing_p0_p1_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            atoms_path = root / "canonical-content.json"
            blueprint_path = root / "slide-blueprints.json"
            output_path = root / "blueprint-report.json"
            atoms_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "atoms": [
                            {
                                "atom_id": "atom-critical",
                                "type": "CLAIM",
                                "source_id": "source-001",
                                "locator": {"paragraph": 1},
                                "verbatim": "Critical claim",
                                "priority": "P1",
                                "confidence": "VERIFIED",
                                "must_preserve": True,
                                "destination": "VISIBLE_SLIDE",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            blueprint_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "slides": [
                            {
                                "slide_id": "slide-001",
                                "slide_number": 1,
                                "role": "TITLE",
                                "assertion_title": "Opening",
                                "primary_claim": "Opening",
                                "source_atoms": [],
                                "visual_job": "SET_CONTEXT",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-slide-blueprints.py"),
                    "--blueprints",
                    str(blueprint_path),
                    "--content-atoms",
                    str(atoms_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(any(item["code"] == "CRITICAL_ATOM_NOT_COVERED" for item in payload["findings"]))

    def test_image_audit_blocks_generated_visual_used_as_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            assets_path = root / "visual-assets.json"
            output_path = root / "image-report.json"
            assets_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "assets": [
                            {
                                "asset_id": "asset-001",
                                "slide_number": 4,
                                "kind": "IMAGE",
                                "role": "EVIDENCE",
                                "source_type": "AI_GENERATED",
                                "provenance": {"generator": "imagegen"},
                                "usage": {"display_width_inches": 5, "display_height_inches": 3},
                                "pixel_width": 1600,
                                "pixel_height": 900,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "audit-images.py"),
                    "--assets",
                    str(assets_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(any(item["code"] == "GENERATED_ASSET_USED_AS_EVIDENCE" for item in payload["findings"]))

    def test_image_audit_blocks_visual_asset_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            asset_path = root / "asset.png"
            asset_path.write_bytes(b"asset-bytes")
            assets_path = root / "visual-assets.json"
            output_path = root / "image-report.json"
            assets_path.write_text(
                json.dumps(
                    [
                        {
                            "asset_id": "asset-002",
                            "slide_number": 2,
                            "kind": "PHOTO",
                            "role": "EVIDENCE",
                            "source_type": "USER_PROVIDED",
                            "provenance": {"kind": "SOURCE_FILE"},
                            "usage": {
                                "display_width_inches": 5,
                                "display_height_inches": 3,
                                "alt_text": "Source photo",
                            },
                            "pixel_width": 1600,
                            "pixel_height": 900,
                            "path": str(asset_path),
                            "sha256": "0" * 64,
                        }
                    ]
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "audit-images.py"),
                    "--assets",
                    str(assets_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(any(item["code"] == "VISUAL_ASSET_HASH_MISMATCH" for item in payload["findings"]))

    def test_image_audit_blocks_declared_pixel_dimension_mismatch(self) -> None:
        from PIL import Image

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            asset_path = root / "asset.png"
            Image.new("RGB", (320, 180), color=(12, 34, 56)).save(asset_path)
            assets_path = root / "visual-assets.json"
            output_path = root / "image-report.json"
            assets_path.write_text(
                json.dumps(
                    [
                        {
                            "asset_id": "asset-003",
                            "slide_number": 3,
                            "kind": "PHOTO",
                            "role": "DECORATIVE",
                            "source_type": "USER_PROVIDED",
                            "provenance": {"kind": "SOURCE_FILE"},
                            "usage": {
                                "display_width_inches": 5,
                                "display_height_inches": 3,
                            },
                            "pixel_width": 1600,
                            "pixel_height": 900,
                            "path": str(asset_path),
                            "sha256": hashlib.sha256(asset_path.read_bytes()).hexdigest(),
                        }
                    ]
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "audit-images.py"),
                    "--assets",
                    str(assets_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(
                any(
                    item["code"] == "IMAGE_PIXEL_DIMENSIONS_MISMATCH"
                    for item in payload["findings"]
                )
            )

    def test_contrast_audit_accepts_list_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            manifest_path = root / "contrast.json"
            output_path = root / "contrast-report.json"
            manifest_path.write_text(
                json.dumps(
                    [
                        {
                            "slide_number": 1,
                            "object_id": "title",
                            "kind": "TEXT",
                            "foreground": "#FFFFFF",
                            "background": "#07172E",
                            "font_size": 32,
                            "bold": True,
                        }
                    ]
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "audit-contrast.py"),
                    "--manifest",
                    str(manifest_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("PASS", payload["status"])
            self.assertEqual(1, payload["item_count"])

    def test_native_audits_reject_deck_output_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            deck = root / "source.pptx"
            original = b"immutable-deck"
            cases = [
                ("audit-motion.ps1", []),
                ("audit-typography.ps1", []),
                ("audit-native-layout.ps1", []),
            ]
            for script, extra_arguments in cases:
                with self.subTest(script=script):
                    deck.write_bytes(original)
                    result = run_pwsh(
                        script,
                        "-DeckPath", str(deck),
                        "-OutputPath", str(deck),
                        *extra_arguments,
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    self.assertEqual(original, deck.read_bytes())

    def test_render_native_rejects_invalid_dimensions_and_existing_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            deck = root / "source.pptx"
            deck.write_bytes(b"immutable-deck")
            invalid_output = root.parent / f"renders-{root.name}"
            try:
                result = run_pwsh(
                    "render-native.ps1",
                    "-DeckPath", str(deck),
                    "-OutputDirectory", str(invalid_output),
                    "-Width", "0",
                    "-Height", "1080",
                )
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertFalse(invalid_output.exists())

                invalid_output.mkdir()
                sentinel = invalid_output / "slide-999.png"
                sentinel.write_bytes(b"stale")
                result = run_pwsh(
                    "render-native.ps1",
                    "-DeckPath", str(deck),
                    "-OutputDirectory", str(invalid_output),
                )
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertEqual(b"stale", sentinel.read_bytes())
            finally:
                if invalid_output.exists():
                    for child in invalid_output.iterdir():
                        child.unlink()
                    invalid_output.rmdir()

    def test_render_pdf_rejects_existing_output_without_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            deck = root / "source.pptx"
            output = root / "output.pdf"
            deck.write_bytes(b"immutable-deck")
            output.write_bytes(b"sentinel")
            result = run_pwsh(
                "render-pdf.ps1",
                "-DeckPath", str(deck),
                "-OutputPath", str(output),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual(b"sentinel", output.read_bytes())

    def test_render_scripts_reject_source_under_reparse_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            target = root / "target"
            junction = root / "junction"
            target.mkdir()
            create = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            if create.returncode != 0:
                self.skipTest(f"Junction unavailable: {create.stderr}")
            try:
                deck = target / "source.pptx"
                deck.write_bytes(b"immutable-deck")
                render_output = root / "renders"
                pdf_output = root / "output.pdf"
                cases = [
                    (
                        "render-native.ps1",
                        [
                            "-DeckPath", str(junction / "source.pptx"),
                            "-OutputDirectory", str(render_output),
                            "-Width", "1920",
                        ],
                    ),
                    (
                        "render-pdf.ps1",
                        [
                            "-DeckPath", str(junction / "source.pptx"),
                            "-OutputPath", str(pdf_output),
                        ],
                    ),
                ]
                for script, arguments in cases:
                    with self.subTest(script=script):
                        result = run_pwsh(script, *arguments)
                        self.assertEqual(2, result.returncode, result.stderr)
                        self.assertIn("PATH_REPARSE_POINT_NOT_ALLOWED", result.stderr)
                self.assertEqual(b"immutable-deck", deck.read_bytes())
                self.assertFalse(render_output.exists())
                self.assertFalse(pdf_output.exists())
            finally:
                if junction.exists():
                    junction.rmdir()

    def test_archive_inspection_rejects_existing_report_without_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            archive_path = root / "safe.zip"
            report_path = root / "archive-report.json"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("content/brief.txt", "slide brief")
            report_path.write_text("sentinel", encoding="utf-8")
            result = run_pwsh(
                "inspect-archive.ps1",
                "-ArchivePath", str(archive_path),
                "-OutputPath", str(report_path),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual("sentinel", report_path.read_text(encoding="utf-8"))

    def test_compare_content_blocks_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline = root / "baseline.json"
            candidate = root / "candidate.json"
            output = root / "report.json"
            atom = {
                "atom_id": "atom-001",
                "verbatim": "US revenue reaches 100M",
                "normalized": "US revenue reaches 100M",
                "priority": "P1",
                "destination": "slide-2",
            }
            baseline.write_text(json.dumps({"atoms": [atom]}), encoding="utf-8")
            candidate.write_text(json.dumps({"atoms": [atom, atom]}), encoding="utf-8")
            result = run_pwsh(
                "compare-content.ps1",
                "-BaselinePath", str(baseline),
                "-CandidatePath", str(candidate),
                "-OutputPath", str(output),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8-sig"))
            self.assertTrue(any(item["code"] == "CANDIDATE_DUPLICATE_KEY" for item in payload["findings"]))

    def test_run_pipeline_rejects_existing_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.txt"
            job_contract_path = root / "job-contract.json"
            workspace = root / "run"
            source.write_text("source", encoding="utf-8")
            self._write_job_contract(job_contract_path)
            workspace.mkdir()
            sentinel = workspace / "sentinel.txt"
            sentinel.write_text("keep", encoding="utf-8")
            result = run_pwsh(
                "run-pipeline.ps1",
                "-InputPath", str(source),
                "-JobContractPath", str(job_contract_path),
                "-Workspace", str(workspace),
                "-SkipPreflight",
            )
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual("keep", sentinel.read_text(encoding="utf-8"))

    def test_apply_motion_rejects_duplicate_storyboard_slides_before_copy(self) -> None:
        _, certificate_payload = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            static_deck = Path(str(certificate_payload["output_path"]))
            certificate = root / "static-certificate.json"
            storyboard = root / "storyboard.json"
            output = root / "motion.pptx"
            report = root / "motion-report.json"
            certificate.write_text(json.dumps(certificate_payload), encoding="utf-8")
            storyboard.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": True,
                        "slides": [
                            {"slide": 1, "transition": "fade_smoothly", "beats": []},
                            {"slide": 1, "transition": "none", "beats": []},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "apply-motion.ps1",
                "-InputPath", str(static_deck),
                "-OutputPath", str(output),
                "-StoryboardPath", str(storyboard),
                "-StaticCertificationPath", str(certificate),
                "-ReportPath", str(report),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(report.read_text(encoding="utf-8-sig"))
            self.assertTrue(payload["error"].startswith("STORYBOARD_DUPLICATE_SLIDE"))
            self.assertFalse(output.exists())

    def test_apply_motion_rejects_unversioned_or_unknown_storyboard_contract(self) -> None:
        _, certificate_payload = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            static_deck = Path(str(certificate_payload["output_path"]))
            certificate = root / "static-certificate.json"
            certificate.write_text(json.dumps(certificate_payload), encoding="utf-8")
            cases = [
                (
                    "missing-version",
                    {
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": True,
                        "slides": [{"slide": 1, "transition": "none", "beats": []}],
                    },
                    "STORYBOARD_SCHEMA_VERSION_INVALID",
                ),
                (
                    "unknown-field",
                    {
                        "schema_version": "1.0",
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": True,
                        "unexpected": True,
                        "slides": [{"slide": 1, "transition": "none", "beats": []}],
                    },
                    "STORYBOARD_UNKNOWN_PROPERTY:unexpected",
                ),
                (
                    "schema-runtime-mismatch",
                    {
                        "schema_version": "1.0",
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": True,
                        "deck_id": "unused-but-previously-accepted",
                        "slides": [{"slide": 1, "transition": "none", "beats": []}],
                    },
                    "STORYBOARD_UNKNOWN_PROPERTY:deck_id",
                ),
            ]
            for case_name, storyboard_payload, expected_error in cases:
                with self.subTest(case=case_name):
                    storyboard = root / f"storyboard-{case_name}.json"
                    output = root / f"motion-{case_name}.pptx"
                    report = root / f"motion-report-{case_name}.json"
                    storyboard.write_text(json.dumps(storyboard_payload), encoding="utf-8")
                    result = run_pwsh(
                        "apply-motion.ps1",
                        "-InputPath", str(static_deck),
                        "-OutputPath", str(output),
                        "-StoryboardPath", str(storyboard),
                        "-StaticCertificationPath", str(certificate),
                        "-ReportPath", str(report),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    payload = json.loads(report.read_text(encoding="utf-8-sig"))
                    self.assertEqual(expected_error, payload["error"])
                    self.assertFalse(output.exists())

    def test_apply_motion_rejects_inherited_untracked_effects_before_copy(self) -> None:
        _, certificate_payload = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        schema = json.loads(
            (SKILL_ROOT / "schemas" / "motion-storyboard.schema.json").read_text(encoding="utf-8")
        )
        self.assertTrue(schema["properties"]["replace_existing"].get("const"))
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            static_deck = Path(str(certificate_payload["output_path"]))
            certificate = root / "static-certificate.json"
            storyboard = root / "storyboard.json"
            output = root / "motion.pptx"
            report = root / "motion-report.json"
            certificate.write_text(json.dumps(certificate_payload), encoding="utf-8")
            storyboard.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "click_controlled": True,
                        "auto_advance_allowed": False,
                        "replace_existing": False,
                        "slides": [{"slide": 1, "transition": "none", "beats": []}],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "apply-motion.ps1",
                "-InputPath", str(static_deck),
                "-OutputPath", str(output),
                "-StoryboardPath", str(storyboard),
                "-StaticCertificationPath", str(certificate),
                "-ReportPath", str(report),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            payload = json.loads(report.read_text(encoding="utf-8-sig"))
            self.assertEqual("STORYBOARD_REPLACE_EXISTING_MUST_BE_TRUE", payload["error"])
            self.assertFalse(output.exists())

    def test_apply_motion_requires_explicit_timing_and_narrative_purpose_before_copy(self) -> None:
        _, certificate_payload = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        schema = json.loads(
            (SKILL_ROOT / "schemas" / "motion-storyboard.schema.json").read_text(encoding="utf-8")
        )
        beat_schema = schema["properties"]["slides"]["items"]["properties"]["beats"]["items"]
        self.assertEqual(
            {"shape_names", "effect", "trigger", "duration", "delay", "narrative_purpose"},
            set(beat_schema["required"]),
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            static_deck = Path(str(certificate_payload["output_path"]))
            certificate = root / "static-certificate.json"
            certificate.write_text(json.dumps(certificate_payload), encoding="utf-8")
            complete_beat = {
                "shape_names": ["Shape 1"],
                "effect": "fade",
                "trigger": "on_click",
                "duration": 0.45,
                "delay": 0.0,
                "narrative_purpose": "Reveal recommendation after context.",
            }
            cases = [
                ("duration", "STORYBOARD_BEAT_PROPERTY_MISSING:duration:slide=1"),
                ("delay", "STORYBOARD_BEAT_PROPERTY_MISSING:delay:slide=1"),
                (
                    "narrative_purpose",
                    "STORYBOARD_BEAT_PROPERTY_MISSING:narrative_purpose:slide=1",
                ),
            ]
            for missing_field, expected_error in cases:
                with self.subTest(field=missing_field):
                    beat = dict(complete_beat)
                    beat.pop(missing_field)
                    storyboard = root / f"storyboard-missing-{missing_field}.json"
                    output = root / f"motion-missing-{missing_field}.pptx"
                    report = root / f"motion-report-missing-{missing_field}.json"
                    storyboard.write_text(
                        json.dumps(
                            {
                                "schema_version": "1.0",
                                "click_controlled": True,
                                "auto_advance_allowed": False,
                                "replace_existing": True,
                                "slides": [
                                    {
                                        "slide": 1,
                                        "transition": "fade_smoothly",
                                        "beats": [beat],
                                    }
                                ],
                            }
                        ),
                        encoding="utf-8",
                    )
                    result = run_pwsh(
                        "apply-motion.ps1",
                        "-InputPath", str(static_deck),
                        "-OutputPath", str(output),
                        "-StoryboardPath", str(storyboard),
                        "-StaticCertificationPath", str(certificate),
                        "-ReportPath", str(report),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    payload = json.loads(report.read_text(encoding="utf-8-sig"))
                    self.assertEqual(expected_error, payload["error"])
                    self.assertFalse(output.exists())

    def test_apply_motion_revalidates_static_evidence_after_powerpoint_save(self) -> None:
        content = (SKILL_ROOT / "scripts" / "apply-motion.ps1").read_text(
            encoding="utf-8"
        )
        first_validation = content.index("Assert-StaticCertificate -Certificate")
        second_validation = content.find(
            "Assert-StaticCertificate -Certificate", first_validation + 1
        )
        close_index = content.index("$presentation.Close()")
        report_index = content.index("$report = [ordered]@{", close_index)
        self.assertGreater(second_validation, close_index)
        self.assertLess(second_validation, report_index)

    def test_powerpoint_scripts_disable_macros_before_open(self) -> None:
        scripts = [
            "render-native.ps1",
            "render-pdf.ps1",
            "audit-motion.ps1",
            "audit-typography.ps1",
            "audit-native-layout.ps1",
            "apply-motion.ps1",
        ]
        common = (SKILL_ROOT / "scripts" / "common.ps1").read_text(encoding="utf-8")
        self.assertIn("function Set-PowerPointSafeAutomation", common)
        self.assertIn("$Application.AutomationSecurity = 3", common)
        for script in scripts:
            with self.subTest(script=script):
                content = (SKILL_ROOT / "scripts" / script).read_text(encoding="utf-8")
                security_index = content.index("Set-PowerPointSafeAutomation -Application $powerPoint")
                open_index = content.index("Presentations.Open")
                self.assertLess(security_index, open_index)

    def test_immutable_json_entrypoints_reject_existing_output_without_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.txt"
            source.write_text("source", encoding="utf-8")
            inventory = root / "inventory-input.json"
            inventory.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "path": str(source),
                                "detected_format": "TEXT",
                                "role": "PRIMARY_CONTENT",
                                "risk_flags": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            cases = [
                ("inspect-input.ps1", ["-InputPath", str(source)]),
                ("inventory-inputs.ps1", ["-InputPath", str(source)]),
                ("route-job.ps1", ["-InventoryPath", str(inventory)]),
                ("preflight.ps1", ["-TargetPath", str(root), "-Mode", "AUDIT"]),
            ]
            for index, (script, arguments) in enumerate(cases):
                with self.subTest(script=script):
                    output = root / f"sentinel-{index}.json"
                    output.write_text("sentinel", encoding="utf-8")
                    result = run_pwsh(script, *arguments, "-OutputPath", str(output))
                    self.assertEqual(2, result.returncode, result.stderr)
                    self.assertEqual("sentinel", output.read_text(encoding="utf-8"))

    def test_only_private_mutable_state_uses_overwriting_json_writer(self) -> None:
        offenders: list[str] = []
        for script_path in (SKILL_ROOT / "scripts").glob("*.ps1"):
            if script_path.name == "common.ps1":
                continue
            content = script_path.read_text(encoding="utf-8")
            if "Write-JsonFile -" in content:
                offenders.append(script_path.name)
        self.assertEqual([], offenders)

    def test_mutable_state_uses_explicit_writer_and_common_writers_check_parents(self) -> None:
        common = (SKILL_ROOT / "scripts" / "common.ps1").read_text(encoding="utf-8")
        self.assertIn("function Write-JsonFileMutable", common)
        self.assertGreaterEqual(common.count("Assert-NoReparseAncestors -Path $parent"), 2)
        for script_name in ("ensure-faster-whisper.ps1", "run-pipeline.ps1"):
            content = (SKILL_ROOT / "scripts" / script_name).read_text(encoding="utf-8")
            self.assertIn("Write-JsonFileMutable", content)
            self.assertNotIn("Write-JsonFile -", content)

    def test_archive_blocks_ads_control_names_and_prefix_collisions(self) -> None:
        cases = [
            (
                "ads",
                [("content/brief.txt:payload", "bad")],
                "ARCHIVE_INVALID_MEMBER_NAME",
            ),
            (
                "control",
                [("content/bad\x01name.txt", "bad")],
                "ARCHIVE_INVALID_MEMBER_NAME",
            ),
            (
                "prefix",
                [("content/node", "file"), ("content/node/child.txt", "child")],
                "ARCHIVE_MEMBER_PREFIX_COLLISION",
            ),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for case_name, members, expected_code in cases:
                with self.subTest(case=case_name):
                    archive_path = root / f"{case_name}.zip"
                    report_path = root / f"{case_name}-report.json"
                    with zipfile.ZipFile(archive_path, "w") as archive:
                        for name, value in members:
                            archive.writestr(name, value)
                    result = run_pwsh(
                        "inspect-archive.ps1",
                        "-ArchivePath", str(archive_path),
                        "-OutputPath", str(report_path),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
                    self.assertEqual("BLOCKED", report["status"])
                    self.assertTrue(any(item["code"] == expected_code for item in report["risks"]))

    def test_apply_motion_rejects_forged_static_certificate_contract(self) -> None:
        _, certificate_payload = self._certify(
            findings=[], certification_profile="STATIC_READY_FOR_MOTION"
        )
        tamper_cases = [
            (
                "missing-required-evidence",
                lambda payload: (
                    payload.__setitem__("required_evidence", ["source_hash_unchanged"]),
                    payload.__setitem__("evidence_receipts", {}),
                ),
                "STATIC_CERTIFICATE_REQUIRED_EVIDENCE_MISMATCH",
            ),
            (
                "receipt-subject-hash",
                lambda payload: payload["evidence_receipts"]["all_slides_rendered"].__setitem__(
                    "subject_sha256", "0" * 64
                ),
                "STATIC_CERTIFICATE_RECEIPT_SUBJECT_HASH_MISMATCH",
            ),
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            static_deck = Path(str(certificate_payload["output_path"]))
            for index, (case_name, tamper, expected_error) in enumerate(tamper_cases):
                with self.subTest(case=case_name):
                    payload = json.loads(json.dumps(certificate_payload))
                    tamper(payload)
                    certificate = root / f"certificate-{index}.json"
                    storyboard = root / f"storyboard-{index}.json"
                    output = root / f"motion-{index}.pptx"
                    report = root / f"motion-report-{index}.json"
                    certificate.write_text(json.dumps(payload), encoding="utf-8")
                    storyboard.write_text(
                        json.dumps(
                            {
                                "schema_version": "1.0",
                                "click_controlled": True,
                                "auto_advance_allowed": False,
                                "replace_existing": True,
                                "slides": [
                                    {"slide": 1, "transition": "fade_smoothly", "beats": []},
                                ],
                            }
                        ),
                        encoding="utf-8",
                    )
                    result = run_pwsh(
                        "apply-motion.ps1",
                        "-InputPath", str(static_deck),
                        "-OutputPath", str(output),
                        "-StoryboardPath", str(storyboard),
                        "-StaticCertificationPath", str(certificate),
                        "-ReportPath", str(report),
                    )
                    self.assertEqual(2, result.returncode, result.stderr)
                    failure = json.loads(report.read_text(encoding="utf-8-sig"))
                    self.assertTrue(failure["error"].startswith(expected_error), failure["error"])
                    self.assertFalse(output.exists())

    def test_router_blocks_inventory_without_explicit_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path = root / "inventory.json"
            route_path = root / "route.json"
            inventory_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "sources": [
                            {
                                "source_id": "source-001",
                                "detected_format": "TEXT",
                                "role": "PRIMARY_CONTENT",
                                "risk_flags": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = run_pwsh(
                "route-job.ps1",
                "-InventoryPath",
                str(inventory_path),
                "-OutputPath",
                str(route_path),
            )
            self.assertEqual(2, result.returncode, result.stderr)
            route = json.loads(route_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("BLOCKED", route["status"])
            self.assertIn("INVENTORY_STATUS_MISSING", route["blocking_reasons"])

    def test_validate_data_empty_ledger_requires_canonical_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            ledger_path = root / "data-ledger.json"
            output_path = root / "data-report.json"
            ledger_path.write_text(
                json.dumps({"schema_version": "1.0", "metrics": []}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-data.py"),
                    "--input",
                    str(ledger_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(3, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("UNVERIFIED", report["status"])
            self.assertTrue(
                any(
                    finding["code"] == "EMPTY_DATA_LEDGER_CONTEXT_REQUIRED"
                    for finding in report["findings"]
                ),
                report,
            )

    def test_validate_data_certifies_empty_ledger_only_for_metric_free_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            ledger_path = root / "data-ledger.json"
            content_path = root / "canonical-content.json"
            output_path = root / "data-report.json"
            ledger_path.write_text(
                json.dumps({"schema_version": "1.0", "metrics": []}),
                encoding="utf-8",
            )
            content_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "atoms": [
                            {
                                "atom_id": "atom-001",
                                "type": "CLAIM",
                                "source_id": "source-001",
                                "locator": {"paragraph": 1},
                                "verbatim": "Strategy remains focused.",
                                "priority": "P1",
                                "confidence": "VERIFIED",
                                "must_preserve": True,
                                "destination": "VISIBLE_SLIDE",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-data.py"),
                    "--input",
                    str(ledger_path),
                    "--content-atoms",
                    str(content_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("PASS", report["status"])
            self.assertEqual(0, report["expected_metric_count"])

    def test_validate_data_blocks_empty_ledger_when_content_contains_metric(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            ledger_path = root / "data-ledger.json"
            content_path = root / "canonical-content.json"
            output_path = root / "data-report.json"
            ledger_path.write_text(
                json.dumps({"schema_version": "1.0", "metrics": []}),
                encoding="utf-8",
            )
            content_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "atoms": [
                            {
                                "atom_id": "atom-metric",
                                "type": "METRIC",
                                "source_id": "source-001",
                                "locator": {"paragraph": 1},
                                "verbatim": "Revenue reaches 100 million USD.",
                                "normalized": {
                                    "metric_key": "revenue",
                                    "value": 100,
                                    "unit": "USD_MILLION",
                                    "period": "2030",
                                    "actual_or_forecast": "TARGET",
                                },
                                "priority": "P0",
                                "confidence": "VERIFIED",
                                "must_preserve": True,
                                "destination": "VISIBLE_SLIDE",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-data.py"),
                    "--input",
                    str(ledger_path),
                    "--content-atoms",
                    str(content_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", report["status"])
            self.assertTrue(
                any(
                    finding["code"] == "EXPECTED_METRICS_MISSING"
                    for finding in report["findings"]
                ),
                report,
            )

    def test_validate_data_blocks_semantically_invalid_metric_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            ledger_path = root / "data-ledger.json"
            output_path = root / "data-report.json"
            ledger_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "metrics": [
                            {
                                "metric_id": "metric-001",
                                "metric_key": "   ",
                                "value": True,
                                "unit": "USD",
                                "period": "2030",
                                "source_id": "source-001",
                                "locator": {},
                                "verification_status": "VERIFIED",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-data.py"),
                    "--input",
                    str(ledger_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            codes = {finding["code"] for finding in report["findings"]}
            self.assertIn("METRIC_FIELD_INVALID", codes)
            self.assertIn("METRIC_ACTUAL_OR_FORECAST_MISSING", codes)

    def test_reconciliation_does_not_pass_unverified_metric_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            content_path = root / "canonical-content.json"
            ledger_path = root / "data-ledger.json"
            output_path = root / "reconciliation.json"
            content_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "status": "PASS",
                        "atoms": [
                            {
                                "atom_id": "atom-metric",
                                "type": "METRIC",
                                "source_id": "source-001",
                                "locator": {"paragraph": 1},
                                "verbatim": "Revenue reaches 100 million USD.",
                                "normalized": {
                                    "metric_key": "revenue",
                                    "value": 100,
                                    "unit": "USD_MILLION",
                                    "period": "2030",
                                    "actual_or_forecast": "TARGET",
                                },
                                "priority": "P0",
                                "confidence": "VERIFIED",
                                "must_preserve": True,
                                "destination": "VISIBLE_SLIDE",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            ledger_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "metrics": [
                            {
                                "metric_id": "metric-001",
                                "metric_key": "revenue",
                                "value": 100,
                                "unit": "USD_MILLION",
                                "period": "2030",
                                "denominator": None,
                                "source_id": "source-002",
                                "locator": {"sheet": "Plan", "cell": "B4"},
                                "verification_status": "UNVERIFIED",
                                "actual_or_forecast": "TARGET",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "reconcile-content.py"),
                    "--content-atoms",
                    str(content_path),
                    "--data-ledger",
                    str(ledger_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(3, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("UNVERIFIED", report["status"])
            self.assertTrue(
                any(
                    finding["code"] == "MATCHED_METRIC_NOT_VERIFIED"
                    for finding in report["findings"]
                ),
                report,
            )

    def test_reconciliation_blocks_empty_canonical_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            content_path = root / "canonical-content.json"
            ledger_path = root / "data-ledger.json"
            output_path = root / "reconciliation.json"
            content_path.write_text(
                json.dumps({"schema_version": "1.0", "status": "PASS", "atoms": []}),
                encoding="utf-8",
            )
            ledger_path.write_text(
                json.dumps({"schema_version": "1.0", "metrics": []}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "reconcile-content.py"),
                    "--content-atoms",
                    str(content_path),
                    "--data-ledger",
                    str(ledger_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", report["status"])
            self.assertTrue(
                any(
                    finding["code"] == "CANONICAL_CONTENT_EMPTY"
                    for finding in report["findings"]
                ),
                report,
            )

    def test_blueprint_validation_blocks_empty_canonical_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            content_path = root / "canonical-content.json"
            blueprint_path = root / "slide-blueprints.json"
            output_path = root / "blueprint-report.json"
            content_path.write_text(
                json.dumps({"schema_version": "1.0", "status": "PASS", "atoms": []}),
                encoding="utf-8",
            )
            blueprint_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "deck_id": "deck-001",
                        "slides": [
                            {
                                "slide_id": "slide-001",
                                "slide_number": 1,
                                "role": "TITLE",
                                "assertion_title": "Opening",
                                "primary_claim": "Opening",
                                "source_atoms": [],
                                "visual_job": "SET_CONTEXT",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-slide-blueprints.py"),
                    "--blueprints",
                    str(blueprint_path),
                    "--content-atoms",
                    str(content_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(
                any(
                    finding["code"] == "CANONICAL_CONTENT_EMPTY"
                    for finding in report["findings"]
                ),
                report,
            )

    def test_contrast_audit_blocks_empty_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            manifest_path = root / "contrast-manifest.json"
            output_path = root / "contrast-report.json"
            manifest_path.write_text(
                json.dumps({"schema_version": "1.0", "items": []}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "audit-contrast.py"),
                    "--manifest",
                    str(manifest_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", report["status"])
            self.assertTrue(
                any(
                    finding["code"] == "CONTRAST_MANIFEST_EMPTY"
                    for finding in report["findings"]
                ),
                report,
            )

    def test_visual_coverage_blocks_empty_blueprint_set(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            blueprints_path = root / "slide-blueprints.json"
            assets_path = root / "visual-assets.json"
            output_path = root / "coverage-report.json"
            blueprints_path.write_text(
                json.dumps({"schema_version": "1.0", "deck_id": "deck-001", "slides": []}),
                encoding="utf-8",
            )
            assets_path.write_text(
                json.dumps({"schema_version": "1.0", "assets": []}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    "node",
                    str(SKILL_ROOT / "scripts" / "audit-visual-coverage.mjs"),
                    "--blueprints",
                    str(blueprints_path),
                    "--assets",
                    str(assets_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(
                any(
                    finding["code"] == "EMPTY_BLUEPRINT"
                    for finding in report["findings"]
                ),
                report,
            )

    def test_preflight_certification_requires_python_and_jsonschema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            fake_python = fake_bin / "python.cmd"
            fake_python.write_text(
                "@echo off\r\necho 3.11.0\r\necho False\r\necho False\r\necho False\r\n",
                encoding="utf-8",
            )
            output_path = root / "preflight.json"
            environment = os.environ.copy()
            environment["PATH"] = str(fake_bin)
            pwsh_path = subprocess.run(
                ["where.exe", "pwsh"],
                text=True,
                capture_output=True,
                check=True,
            ).stdout.splitlines()[0]
            result = subprocess.run(
                [
                    pwsh_path,
                    "-NoLogo",
                    "-NoProfile",
                    "-File",
                    str(SKILL_ROOT / "scripts" / "preflight.ps1"),
                    "-OutputPath",
                    str(output_path),
                    "-TargetPath",
                    str(root),
                    "-Mode",
                    "CERTIFY",
                ],
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(3, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("UNVERIFIED", report["status"])
            self.assertTrue(
                any(
                    issue["code"] == "JSONSCHEMA_RUNTIME_MISSING"
                    for issue in report["issues"]
                ),
                report,
            )

    def test_preflight_requires_artifact_tool_import_not_directory_presence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            fake_node = fake_bin / "node.cmd"
            fake_node.write_text("@echo off\r\nexit /b 1\r\n", encoding="utf-8")
            runtime_modules = root / "node_modules"
            (runtime_modules / "@oai" / "artifact-tool").mkdir(parents=True)
            output_path = root / "preflight.json"
            environment = os.environ.copy()
            environment["RUNTIME_NODE"] = str(fake_node)
            environment["RUNTIME_NODE_MODULES"] = str(runtime_modules)
            environment["RUNTIME_BIN_DIR"] = str(fake_bin)
            result = subprocess.run(
                [
                    "pwsh",
                    "-NoLogo",
                    "-NoProfile",
                    "-File",
                    str(SKILL_ROOT / "scripts" / "preflight.ps1"),
                    "-OutputPath",
                    str(output_path),
                    "-TargetPath",
                    str(root),
                    "-Mode",
                    "CREATE",
                ],
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(3, result.returncode, result.stderr)
            report = json.loads(output_path.read_text(encoding="utf-8-sig"))
            self.assertEqual("UNVERIFIED", report["status"])
            self.assertFalse(report["runtimes"]["artifact_tool"]["importable"])
            self.assertTrue(
                any(
                    issue["code"] == "ARTIFACT_TOOL_IMPORT_FAILED"
                    for issue in report["issues"]
                ),
                report,
            )

    def test_pipeline_logs_use_create_new_safe_text_writer(self) -> None:
        common = (SKILL_ROOT / "scripts" / "common.ps1").read_text(encoding="utf-8")
        pipeline = (SKILL_ROOT / "scripts" / "run-pipeline.ps1").read_text(encoding="utf-8")
        self.assertIn("function Write-TextFileNew", common)
        self.assertNotIn("Out-File", pipeline)
        self.assertGreaterEqual(pipeline.count("Write-TextFileNew"), 3)

        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "existing.txt"
            target.write_text("sentinel", encoding="utf-8")
            command = (
                f". '{SKILL_ROOT / 'scripts' / 'common.ps1'}'; "
                f"Write-TextFileNew -Text 'replacement' -Path '{target}'"
            )
            result = subprocess.run(
                ["pwsh", "-NoLogo", "-NoProfile", "-Command", command],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("sentinel", target.read_text(encoding="utf-8"))

    def test_critical_intermediate_schemas_reject_unknown_fields(self) -> None:
        schema_expectations = {
            "adapter-result.schema.json": [(), ("properties", "coverage"), ("properties", "artifacts", "items")],
            "canonical-content.schema.json": [()],
            "content-atom.schema.json": [()],
            "copy-difference-log.schema.json": [(), ("properties", "changes", "items")],
            "data-ledger.schema.json": [(), ("properties", "metrics", "items")],
            "job-contract.schema.json": [()],
            "motion-storyboard.schema.json": [(), ("properties", "slides", "items"), ("properties", "slides", "items", "properties", "beats", "items")],
            "routing-decision.schema.json": [(), ("properties", "required_adapters", "items")],
            "qa-finding.schema.json": [()],
            "slide-blueprint.schema.json": [(), ("properties", "slides", "items"), ("properties", "slides", "items", "properties", "visual_anchor")],
            "source-manifest.schema.json": [(), ("properties", "sources", "items")],
            "contrast-manifest.schema.json": [(), ("properties", "items", "items")],
            "content-coverage-matrix.schema.json": [(), ("properties", "rows", "items")],
            "evidence-graph.schema.json": [(), ("properties", "nodes", "items"), ("properties", "edges", "items"), ("properties", "conflicts", "items")],
            "narrative-graph.schema.json": [(), ("properties", "candidates", "items"), ("properties", "question_chain", "items"), ("properties", "sections", "items")],
            "source-slide-map.schema.json": [(), ("properties", "mappings", "items")],
            "visual-assets.schema.json": [()],
            "visual-asset.schema.json": [(), ("properties", "provenance"), ("properties", "usage")],
        }
        for schema_name, paths in schema_expectations.items():
            with self.subTest(schema=schema_name):
                schema = json.loads(
                    (SKILL_ROOT / "schemas" / schema_name).read_text(encoding="utf-8")
                )
                for path_parts in paths:
                    node = schema
                    for part in path_parts:
                        node = node[part]
                    self.assertIs(
                        False,
                        node.get("additionalProperties"),
                        f"{schema_name}:{'/'.join(path_parts) or '$'}",
                    )

    def test_copy_difference_schema_allows_approved_omission_with_meaning_loss(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            log_path = root / "copy-difference-log.json"
            report_path = root / "validation.json"
            log_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "changes": [
                            {
                                "change_id": "change-001",
                                "atom_id": "atom-001",
                                "slide_id": "slide-001",
                                "transformation": "OMIT_WITH_APPROVAL",
                                "before": "Low-priority detail",
                                "after": None,
                                "meaning_preserved": False,
                                "review_status": "APPROVED",
                                "rationale": "Omit approved P2 detail to reduce density.",
                                "approval": {
                                    "approver": "owner@example.com",
                                    "scope": "atom-001",
                                    "reason": "P2 content not required in executive view.",
                                    "expiry": "2030-01-01T00:00:00Z",
                                    "impact": "No impact to P0/P1 meaning.",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-json.py"),
                    "--input", str(log_path),
                    "--schema", "copy-difference-log",
                    "--output", str(report_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual("PASS", report["status"])

    def test_data_and_contrast_schemas_reject_empty_certification_inputs(self) -> None:
        data_schema = json.loads(
            (SKILL_ROOT / "schemas" / "data-ledger.schema.json").read_text(encoding="utf-8")
        )
        contrast_schema = json.loads(
            (SKILL_ROOT / "schemas" / "contrast-manifest.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(0, data_schema["properties"]["metrics"].get("minItems", 0))
        self.assertEqual(1, contrast_schema["properties"]["items"]["minItems"])
        metric_required = set(data_schema["properties"]["metrics"]["items"]["required"])
        self.assertIn("denominator", metric_required)
        self.assertIn("actual_or_forecast", metric_required)

    def test_generated_inventory_and_archive_reports_validate_against_schemas(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.txt"
            source.write_text("source", encoding="utf-8")
            inventory = root / "source-inventory.json"
            inventory_result = run_pwsh(
                "inventory-inputs.ps1",
                "-InputPath", str(source),
                "-OutputPath", str(inventory),
            )
            self.assertEqual(0, inventory_result.returncode, inventory_result.stderr)
            inventory_validation = root / "source-inventory-validation.json"
            inventory_schema_result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-json.py"),
                    "--input", str(inventory),
                    "--schema", "source-manifest",
                    "--output", str(inventory_validation),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, inventory_schema_result.returncode, inventory_schema_result.stderr)

            archive = root / "source.zip"
            with zipfile.ZipFile(archive, "w") as package:
                package.writestr("content/source.txt", "source")
            archive_report = root / "archive-report.json"
            archive_result = run_pwsh(
                "inspect-archive.ps1",
                "-ArchivePath", str(archive),
                "-OutputPath", str(archive_report),
            )
            self.assertEqual(0, archive_result.returncode, archive_result.stderr)
            archive_validation = root / "archive-validation.json"
            archive_schema_result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "validate-json.py"),
                    "--input", str(archive_report),
                    "--schema", "adapter-result",
                    "--output", str(archive_validation),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, archive_schema_result.returncode, archive_schema_result.stderr)

    def _certify(
        self,
        *,
        findings: list[dict[str, str]] | None,
        mandatory_capabilities_verified: bool = True,
        source_hash_unchanged: bool = True,
        omit_domain: str | None = None,
        evidence_overrides: dict[str, bool] | None = None,
        output_hash_override: str | None = None,
        minimum_quality_score: float | str | None = None,
        minimum_domain_score: float | str | None = None,
        source_hash_before_override: str | None = None,
        source_hash_after_override: str | None = None,
        include_evidence_receipts: bool = True,
        tamper_evidence_receipt: str | None = None,
        deck_bytes_override: bytes | None = None,
        certification_profile: str = "FINAL_RELEASE_MOTION",
        receipt_subject_hash_override: str | None = None,
        quality_score_override: float | None = None,
        receipt_generated_at_override: str | None = None,
        reparse_binding: str | None = None,
        extra_domain_scores: dict[str, float] | None = None,
        extra_receipt_fields: dict[str, dict[str, object]] | None = None,
        extra_source_binding_fields: dict[str, object] | None = None,
        extra_receipt_binding_fields: dict[str, dict[str, object]] | None = None,
        extra_receipt_check_fields: dict[str, dict[str, object]] | None = None,
        omit_visual_native_metadata: bool = False,
        additional_source_contents: list[str] | None = None,
        extra_input_fields: dict[str, object] | None = None,
        extra_receipt_name: str | None = None,
        native_coverage_overrides: dict[str, object] | None = None,
        native_layout_overrides: dict[str, object] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        input_path = root / "release-input.json"
        output_path = root / "release-certificate.json"
        deck_path = root / "final.pptx"
        source_path = root / "source.txt"
        if reparse_binding not in {None, "source", "output", "receipt"}:
            raise ValueError(f"unsupported reparse binding: {reparse_binding}")

        def bind_directory_through_junction(name: str) -> Path:
            target = root / f"{name}-target"
            junction = root / f"{name}-junction"
            target.mkdir()
            result = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode != 0:
                self.skipTest(f"junction unavailable: {result.stderr or result.stdout}")
            self.addCleanup(lambda: junction.rmdir() if junction.exists() else None)
            return junction

        if reparse_binding == "output":
            deck_path = bind_directory_through_junction("output") / "final.pptx"
        if reparse_binding == "source":
            source_path = bind_directory_through_junction("source") / "source.txt"
        if deck_bytes_override is not None:
            deck_path.write_bytes(deck_bytes_override)
        else:
            with zipfile.ZipFile(deck_path, "w") as archive:
                archive.writestr(
                    "[Content_Types].xml",
                    '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/></Types>',
                )
                archive.writestr(
                    "_rels/.rels",
                    '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>',
                )
                archive.writestr(
                    "ppt/presentation.xml",
                    '<?xml version="1.0" encoding="UTF-8"?><p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>',
                )
        source_path.write_text("immutable source", encoding="utf-8")
        source_records = [
            {
                "source_id": "source-001",
                "path": source_path,
                "sha256": hashlib.sha256(b"immutable source").hexdigest(),
            }
        ]
        for index, content in enumerate(additional_source_contents or [], start=2):
            additional_source = root / f"source-{index:03d}.txt"
            additional_source.write_text(content, encoding="utf-8")
            source_records.append(
                {
                    "source_id": f"source-{index:03d}",
                    "path": additional_source,
                    "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                }
            )
        source_hash = source_records[0]["sha256"]

        def source_set_hash(records: list[dict[str, object]]) -> str:
            if len(records) == 1:
                return str(records[0]["sha256"])
            canonical_records = []
            for record in records:
                normalized_path = os.path.normcase(str(Path(str(record["path"])).resolve()))
                canonical_records.append(
                    f'{record["source_id"]}\x1f{normalized_path}\x1f{record["sha256"]}'
                )
            return hashlib.sha256("\n".join(sorted(canonical_records)).encode("utf-8")).hexdigest()
        domain_scores = {
            "source_integrity": 100,
            "content_fidelity": 99,
            "data_accuracy": 99,
            "narrative_logic": 98,
            "visual_design": 98,
            "layout_typography": 98,
            "charts_tables": 98,
            "images_icons": 98,
            "motion": 98,
            "native_compatibility": 98,
        }
        if omit_domain:
            domain_scores.pop(omit_domain)
        if certification_profile in {"STATIC_READY_FOR_MOTION", "FINAL_RELEASE_STATIC"}:
            domain_scores.pop("motion", None)
        if extra_domain_scores:
            domain_scores.update(extra_domain_scores)
        evidence = {
                    "source_hash_unchanged": source_hash_unchanged,
                    "mandatory_capabilities_verified": mandatory_capabilities_verified,
                    "all_slides_rendered": True,
                    "all_slides_reviewed": True,
                    "all_data_validated": True,
                    "all_changes_documented": True,
                    "blueprint_coverage_verified": True,
                    "visual_assets_verified": True,
                    "contrast_verified": True,
                    "icon_consistency_verified": True,
                    "motion_verified": True,
                    "source_traceability_verified": True,
                    "static_motion_equivalent": True,
                    "fresh_powerpoint_open": True,
        }
        evidence.update(evidence_overrides or {})
        if certification_profile in {"STATIC_READY_FOR_MOTION", "FINAL_RELEASE_STATIC"}:
            evidence.pop("motion_verified", None)
            evidence.pop("static_motion_equivalent", None)
        deck_hash = hashlib.sha256(deck_path.read_bytes()).hexdigest()
        native_blueprints_path = root / "slide-blueprints.json"
        native_blueprints_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "deck_id": "test-deck",
                    "slides": [{"slide_id": "slide-001", "slide_number": 1}],
                }
            ),
            encoding="utf-8",
        )
        native_assets_path = root / "visual-assets.json"
        native_assets_path.write_text(
            json.dumps({"schema_version": "1.0", "assets": []}),
            encoding="utf-8",
        )
        native_layout_report_path = root / "native-layout-report.json"
        native_layout_payload = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "PASS",
            "deck_path": str(deck_path),
            "deck_sha256": deck_hash,
            "deck_sha256_before": deck_hash,
            "deck_sha256_after": deck_hash,
            "slide_count": 1,
            "slide_size_points": {"width": 960, "height": 540},
            "slides": [{"slide": 1, "shape_count": 0, "objects": []}],
            "findings": [],
        }
        native_layout_payload.update(native_layout_overrides or {})
        native_layout_report_path.write_text(
            json.dumps(native_layout_payload),
            encoding="utf-8",
        )
        native_layout_report_hash = hashlib.sha256(native_layout_report_path.read_bytes()).hexdigest()
        native_visual_coverage_report_path = root / "native-visual-coverage-report.json"
        native_coverage_payload = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "PASS",
            "blueprints_path": str(native_blueprints_path),
            "blueprints_sha256": hashlib.sha256(native_blueprints_path.read_bytes()).hexdigest(),
            "assets_path": str(native_assets_path),
            "assets_sha256": hashlib.sha256(native_assets_path.read_bytes()).hexdigest(),
            "native_bindings_required": True,
            "native_layout_report_path": str(native_layout_report_path),
            "native_layout_report_sha256": native_layout_report_hash,
            "native_deck_path": str(deck_path),
            "native_deck_sha256": deck_hash,
            "native_bindings_verified": True,
            "slide_count": 1,
            "findings": [],
        }
        native_coverage_payload.update(native_coverage_overrides or {})
        native_visual_coverage_report_path.write_text(
            json.dumps(native_coverage_payload),
            encoding="utf-8",
        )
        native_visual_coverage_report_hash = hashlib.sha256(native_visual_coverage_report_path.read_bytes()).hexdigest()
        evidence_receipts: dict[str, dict[str, str]] = {}
        if include_evidence_receipts:
            if reparse_binding == "receipt":
                evidence_directory = bind_directory_through_junction("evidence")
            else:
                evidence_directory = root / "evidence"
                evidence_directory.mkdir()
            for evidence_name in evidence:
                if evidence_name == "source_hash_unchanged":
                    continue
                receipt_path = evidence_directory / f"{evidence_name}.json"
                receipt_path.write_text(
                    json.dumps(
                        {
                            "schema_version": "1.0",
                            "generated_at": (
                                receipt_generated_at_override
                                if receipt_generated_at_override
                                and evidence_name == "all_slides_rendered"
                                else datetime.now(timezone.utc).isoformat()
                            ),
                            "status": "PASS",
                            "evidence_name": evidence_name,
                            "subject_path": str(deck_path),
                            "subject_sha256": (
                                receipt_subject_hash_override
                                if receipt_subject_hash_override
                                and evidence_name == "all_slides_rendered"
                                else deck_hash
                            ),
                            "producer": "make-slide-pro-test-harness",
                            "checks": [
                                {
                                    "check_id": evidence_name,
                                    "status": "PASS",
                                    **(extra_receipt_check_fields or {}).get(evidence_name, {}),
                                }
                            ],
                            **(
                                {
                                    "metadata": {
                                        "native_bindings_verified": True,
                                        "native_visual_coverage_report_path": str(native_visual_coverage_report_path),
                                        "native_visual_coverage_report_sha256": native_visual_coverage_report_hash,
                                        "native_visual_coverage_deck_sha256": deck_hash,
                                    }
                                }
                                if evidence_name == "visual_assets_verified"
                                and not omit_visual_native_metadata
                                else {}
                            ),
                        }
                    ),
                    encoding="utf-8",
                )
                receipt_binding = {
                    "path": str(receipt_path),
                    "sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
                }
                receipt_binding.update(
                    (extra_receipt_binding_fields or {}).get(evidence_name, {})
                )
                evidence_receipts[evidence_name] = receipt_binding
            if extra_receipt_name:
                evidence_receipts[extra_receipt_name] = dict(
                    next(iter(evidence_receipts.values()))
                )
            for evidence_name, extra_fields in (extra_receipt_fields or {}).items():
                receipt_path = Path(evidence_receipts[evidence_name]["path"])
                receipt_payload = json.loads(receipt_path.read_text(encoding="utf-8"))
                receipt_payload.update(extra_fields)
                receipt_path.write_text(json.dumps(receipt_payload), encoding="utf-8")
                evidence_receipts[evidence_name]["sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
            if tamper_evidence_receipt:
                tampered_path = Path(evidence_receipts[tamper_evidence_receipt]["path"])
                tampered_path.write_text('{"status":"PASS","tampered":true}', encoding="utf-8")
        calculated_source_set_hash = source_set_hash(source_records)
        source_hash_before = source_hash_before_override or calculated_source_set_hash
        source_hash_after = source_hash_after_override or (calculated_source_set_hash if source_hash_unchanged else "c" * 64)
        source_bindings = []
        for index, record in enumerate(source_records):
            source_binding = {
                "source_id": record["source_id"],
                "path": str(record["path"]),
                "sha256_before": record["sha256"],
                "sha256_after": record["sha256"] if source_hash_unchanged else "c" * 64,
            }
            if index == 0:
                source_binding.update(extra_source_binding_fields or {})
            source_bindings.append(source_binding)
        input_path.write_text(
            json.dumps(
                {
                    **evidence,
                    "certification_profile": certification_profile,
                    "source_bindings": source_bindings,
                    "source_hash_before": source_hash_before,
                    "source_hash_after": source_hash_after,
                    "output_path": str(deck_path),
                    "output_sha256": output_hash_override or deck_hash,
                    "quality_score": 98.4 if quality_score_override is None else quality_score_override,
                    "domain_scores": domain_scores,
                    "findings": findings,
                    **({"evidence_receipts": evidence_receipts} if include_evidence_receipts else {}),
                    **(extra_input_fields or {}),
                }
            ),
            encoding="utf-8",
        )
        arguments = ["-InputPath", str(input_path), "-OutputPath", str(output_path)]
        if minimum_quality_score is not None:
            arguments.extend(["-MinimumQualityScore", str(minimum_quality_score)])
        if minimum_domain_score is not None:
            arguments.extend(["-MinimumDomainScore", str(minimum_domain_score)])
        result = run_pwsh("certify-release.ps1", *arguments)
        certificate = json.loads(output_path.read_text(encoding="utf-8-sig"))
        return result, certificate


if __name__ == "__main__":
    unittest.main()
