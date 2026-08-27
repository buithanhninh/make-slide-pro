from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator_core import load_json_file, validate_state


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Make Slide Pro orchestrator snapshot against journal replay.")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--state", type=Path)
    args = parser.parse_args()
    registry = load_json_file(args.registry)
    state_path = args.state or (args.workspace / "control" / "state.json")
    state = load_json_file(state_path)
    findings = validate_state(args.workspace, state, registry)
    report = {
        "schema_version": "1.0",
        "status": "PASS" if not findings else "BLOCKED",
        "workspace": str(args.workspace.absolute()),
        "state_path": str(state_path.absolute()),
        "findings": findings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
