"""
scripts/sync_to_vps.py
Make Slide Pro V8.6.0 - Auto Synchronization Engine to Remote VPS.
Transfers code updates from local workstation (D:\\Make Slide PPT)
to remote VPS (hmu-vm-makeslidepro:/home/ubuntu/makeslidepro), reloads systemd,
and supports live auto-sync via --watch.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Set

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "__pycache__",
    ".pytest_cache",
    ".git*",
    "venv",
    "env",
    "*.db",
    "*.sqlite*",
    "*.pptx",
    "*.pdf",
    "*.log",
    "Du_An_Outputs",
    "Du An",
    "Du_An",
    "output",
    "*.docx",
    "workspace_proof",
    "scratch",
    ".idea",
    ".vscode",
    ".system_generated",
    "macc_v8_benchmark_summary.json",
    "temp_*",
]


def should_exclude(rel_path_str: str) -> bool:
    parts = rel_path_str.replace("\\", "/").split("/")
    for p in parts:
        for pat in EXCLUDE_PATTERNS:
            if fnmatch.fnmatch(p, pat):
                return True
    for pat in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(rel_path_str, pat):
            return True
    return False


def collect_project_files() -> List[Path]:
    included: List[Path] = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        rel_root = os.path.relpath(root, PROJECT_ROOT)
        if rel_root != "." and should_exclude(rel_root):
            dirs[:] = []
            continue

        for f in files:
            full_path = Path(root) / f
            rel_file = os.path.relpath(full_path, PROJECT_ROOT)
            if not should_exclude(rel_file):
                included.append(full_path)
    return included


def get_file_mtimes() -> Dict[str, float]:
    mtimes: Dict[str, float] = {}
    for path in collect_project_files():
        try:
            rel = str(path.relative_to(PROJECT_ROOT))
            mtimes[rel] = path.stat().st_mtime
        except OSError:
            pass
    return mtimes


def create_archive(files: List[Path], output_tar: Path) -> int:
    with tarfile.open(output_tar, "w:gz") as tar:
        for f in files:
            rel = f.relative_to(PROJECT_ROOT)
            tar.add(str(f), arcname=rel.as_posix())
    return len(files)


def run_cmd(cmd: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout
    )


def sync_to_vps(vps_host: str = "hmu-vm-makeslidepro", remote_dir: str = "/home/ubuntu/makeslidepro", restart_service: bool = True) -> bool:
    t0 = time.time()
    print(f"\n================================================================================")
    print(f"   MAKE SLIDE PRO V8.6.0 - SYNCING CODE TO VPS [{vps_host}]")
    print(f"================================================================================")

    files = collect_project_files()
    print(f"[*] Packaging {len(files)} source files...")

    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp_tar_path = Path(tmp.name)

    try:
        create_archive(files, tmp_tar_path)
        tar_size_kb = tmp_tar_path.stat().st_size / 1024
        print(f"    ✔ Archive created: {tar_size_kb:.1f} KB")

        # 1. SCP Archive to VPS /tmp
        print(f"[*] Transferring archive to {vps_host}:/tmp/makeslidepro_update.tar.gz...")
        scp_cmd = ["scp", "-o", "ConnectTimeout=10", str(tmp_tar_path), f"{vps_host}:/tmp/makeslidepro_update.tar.gz"]
        res_scp = run_cmd(scp_cmd, timeout=30)
        if res_scp.returncode != 0:
            print(f"[!] SCP Error: {res_scp.stderr}")
            return False
        print("    ✔ Transfer complete.")

        # 2. Extract and Reload on VPS
        print(f"[*] Unpacking archive to {remote_dir} & synchronizing environment...")
        remote_script = f"""
set -e
mkdir -p {remote_dir}
tar -xzf /tmp/makeslidepro_update.tar.gz -C {remote_dir}
rm -f /tmp/makeslidepro_update.tar.gz

# Ensure AI_MODEL=testing and AI_PROVIDER=9router in .env
if [ -f {remote_dir}/.env ]; then
    sed -i 's/^AI_MODEL=.*/AI_MODEL=testing/' {remote_dir}/.env
    sed -i 's|^AI_BASE_URL=.*|AI_BASE_URL=https://9router.caqa.io.vn/v1|' {remote_dir}/.env
    sed -i 's/^AI_PROVIDER=.*/AI_PROVIDER=9router/' {remote_dir}/.env
fi

# Ensure correct file permissions
chown -R ubuntu:ubuntu {remote_dir} 2>/dev/null || true
"""
        if restart_service:
            remote_script += f"""
# Restart systemd daemon
sudo systemctl restart makeslidepro.service
sleep 2

# Verify health
IS_ACTIVE=$(sudo systemctl is-active makeslidepro.service || true)
HTTP_CODE=$(curl -s -o /dev/null -w "%{{http_code}}" http://127.0.0.1:3218/ || true)
echo "SERVICE_STATUS=$IS_ACTIVE"
echo "LOCAL_HTTP_STATUS=$HTTP_CODE"
"""

        script_bytes = remote_script.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        ssh_cmd = ["ssh", "-o", "ConnectTimeout=10", vps_host, "bash -s"]
        proc = subprocess.run(
            ssh_cmd,
            input=script_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=40
        )

        stdout_text = proc.stdout.decode("utf-8", errors="replace")
        stderr_text = proc.stderr.decode("utf-8", errors="replace")

        if proc.returncode != 0:
            print(f"[!] Remote execution error:\n{stderr_text}")
            return False

        print(stdout_text)
        elapsed = time.time() - t0
        print(f"✔ SYNCHRONIZATION COMPLETED in {elapsed:.2f}s!")
        return True

    finally:
        if tmp_tar_path.exists():
            tmp_tar_path.unlink()


def watch_and_sync(vps_host: str = "hmu-vm-makeslidepro", remote_dir: str = "/home/ubuntu/makeslidepro", interval: float = 1.5):
    print(f"\n================================================================================")
    print(f"   MAKE SLIDE PRO V8.6.0 - LIVE WATCH AUTO-SYNC TO VPS ACTIVATED")
    print(f"   Target: {vps_host}:{remote_dir}")
    print(f"   Watching: {PROJECT_ROOT}")
    print(f"   Press CTRL+C to stop auto-sync.")
    print(f"================================================================================\n")

    # Initial sync
    sync_to_vps(vps_host, remote_dir)
    last_mtimes = get_file_mtimes()

    try:
        while True:
            time.sleep(interval)
            current_mtimes = get_file_mtimes()

            changed_files: List[str] = []
            for f_rel, mtime in current_mtimes.items():
                if f_rel not in last_mtimes or mtime > last_mtimes[f_rel]:
                    changed_files.append(f_rel)

            deleted_files = [f_rel for f_rel in last_mtimes if f_rel not in current_mtimes]

            if changed_files or deleted_files:
                sample = changed_files[:3] + ([f"deleted:{d}" for d in deleted_files[:2]])
                print(f"\n[⚡ Change Detected] {len(changed_files)} changed, {len(deleted_files)} deleted (e.g. {sample}).")
                print("   Debouncing 1.0s before triggering sync...")
                time.sleep(1.0)
                sync_to_vps(vps_host, remote_dir)
                last_mtimes = get_file_mtimes()

    except KeyboardInterrupt:
        print("\n[*] Live Watch Auto-Sync stopped by user.")


def main():
    parser = argparse.ArgumentParser(description="Auto-sync Make Slide Pro V8.6.0 to VPS")
    parser.add_argument("--watch", "-w", action="store_true", help="Continuously watch for file changes and auto-sync in real time")
    parser.add_argument("--vps-host", default="hmu-vm-makeslidepro", help="SSH Host name in ~/.ssh/config")
    parser.add_argument("--remote-dir", default="/home/ubuntu/makeslidepro", help="Remote directory path on VPS")
    parser.add_argument("--no-restart", action="store_true", help="Do not restart makeslidepro.service on VPS")
    args = parser.parse_args()

    if args.watch:
        watch_and_sync(vps_host=args.vps_host, remote_dir=args.remote_dir)
    else:
        success = sync_to_vps(
            vps_host=args.vps_host,
            remote_dir=args.remote_dir,
            restart_service=not args.no_restart
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
