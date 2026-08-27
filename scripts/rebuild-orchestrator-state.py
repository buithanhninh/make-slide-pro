from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator_core import load_json_file, write_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild Make Slide Pro state snapshot from append-only journal.")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    args = parser.parse_args()
    state = write_snapshot(args.workspace, load_json_file(args.registry))
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
