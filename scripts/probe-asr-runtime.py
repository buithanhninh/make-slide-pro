from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


def module_version(distribution: str) -> str | None:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def probe_nvidia() -> dict[str, object]:
    command = shutil.which("nvidia-smi")
    if not command:
        return {"available": False, "path": None, "devices": []}
    try:
        result = subprocess.run(
            [command, "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        devices = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return {"available": result.returncode == 0 and bool(devices), "path": command, "devices": devices, "stderr": result.stderr.strip()}
    except (OSError, subprocess.SubprocessError) as error:
        return {"available": False, "path": command, "devices": [], "error": str(error)}


def supported_compute_types(device: str = "cpu") -> list[str]:
    if importlib.util.find_spec("ctranslate2") is None:
        return []
    try:
        import ctranslate2

        return sorted(str(item) for item in ctranslate2.get_supported_compute_types(device))
    except Exception:
        return []


def select_compute_type(supported: list[str], preferred: tuple[str, ...]) -> str | None:
    available = list(dict.fromkeys(str(item) for item in supported if str(item)))
    for compute_type in preferred:
        if compute_type in available:
            return compute_type
    return available[0] if available else None


def normalized_path(path: Path) -> Path:
    return Path(os.path.abspath(os.path.expanduser(os.fspath(path))))


def is_reparse_or_symlink(path: Path) -> bool:
    metadata = os.lstat(path)
    if stat.S_ISLNK(metadata.st_mode):
        return True
    attributes = getattr(metadata, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)
    return bool(attributes & reparse_flag)


def assert_no_reparse_components(path: Path) -> None:
    current = normalized_path(path)
    components: list[Path] = []
    while True:
        components.append(current)
        if current == current.parent:
            break
        current = current.parent
    for component in reversed(components):
        try:
            if is_reparse_or_symlink(component):
                raise ValueError(f"ASR_PROBE_OUTPUT_REPARSE_POINT_NOT_ALLOWED:{component}")
        except FileNotFoundError:
            continue


def assert_mutable_output(path: Path) -> Path:
    output = normalized_path(path)
    assert_no_reparse_components(output)
    if os.path.lexists(output):
        metadata = os.lstat(output)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError(f"ASR_PROBE_OUTPUT_NOT_REGULAR_FILE:{output}")
    return output


def write_json_mutable(payload: dict[str, object], path: Path) -> Path:
    output = normalized_path(path)
    assert_no_reparse_components(output.parent)
    output.parent.mkdir(parents=True, exist_ok=True)
    assert_no_reparse_components(output.parent)
    assert_mutable_output(output)
    text = json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        dir=output.parent,
        prefix=f".{output.name}.tmp-",
        text=True,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        assert_mutable_output(temporary_path)
        assert_mutable_output(output)
        os.replace(temporary_path, output)
        assert_mutable_output(output)
    finally:
        temporary_path.unlink(missing_ok=True)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe Make Slide Pro ASR runtime without downloading a model.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    nvidia = probe_nvidia()
    package_ready = importlib.util.find_spec("faster_whisper") is not None
    ctranslate2_ready = importlib.util.find_spec("ctranslate2") is not None
    av_ready = importlib.util.find_spec("av") is not None
    cpu_compute_types = supported_compute_types("cpu")
    cuda_compute_types = supported_compute_types("cuda")
    cuda_verified = bool(nvidia.get("available")) and bool(cuda_compute_types)
    cpu_compute_type = select_compute_type(cpu_compute_types, ("int8", "int8_float32", "float32", "int16", "bfloat16"))
    cuda_compute_type = select_compute_type(cuda_compute_types, ("float16", "int8_float16", "int8", "float32", "bfloat16"))
    if cuda_verified and cuda_compute_type:
        selected_device = "cuda"
        selected_compute_type = cuda_compute_type
    elif cpu_compute_type:
        selected_device = "cpu"
        selected_compute_type = cpu_compute_type
    else:
        selected_device = None
        selected_compute_type = None
    ready = package_ready and ctranslate2_ready and av_ready and selected_device is not None and selected_compute_type is not None
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "status": "PASS" if ready else "UNVERIFIED",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "faster_whisper": {"available": package_ready, "version": module_version("faster-whisper")},
        "ctranslate2": {
            "available": ctranslate2_ready,
            "version": module_version("ctranslate2"),
            "cpu_compute_types": cpu_compute_types,
            "cuda_compute_types": cuda_compute_types,
        },
        "av": {"version": module_version("av"), "available": av_ready},
        "onnxruntime": {"version": module_version("onnxruntime"), "available": importlib.util.find_spec("onnxruntime") is not None},
        "nvidia": nvidia,
        "cpu_compute_types": cpu_compute_types,
        "cuda_compute_types": cuda_compute_types,
        "cuda_verified": cuda_verified,
        "selected_device": selected_device,
        "selected_compute_type": selected_compute_type,
        "ready": ready,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        try:
            write_json_mutable(payload, args.output)
        except (OSError, ValueError, TypeError) as error:
            failure = {
                "schema_version": "1.0",
                "status": "UNVERIFIED",
                "ready": False,
                "requested_output_path": str(normalized_path(args.output)),
                "error": f"ASR_PROBE_OUTPUT_WRITE_FAILED:{error}",
            }
            print(json.dumps(failure, ensure_ascii=False, indent=2))
            return 3
    print(text)
    return 0 if payload["ready"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
