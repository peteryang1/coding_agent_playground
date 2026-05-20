#!/usr/bin/env python3
"""Validate Milestone 1 trajectories for the required complete coding process."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_MARKERS = {
    "requirements_understanding": [r"requirement", r"goal", r"task"],
    "localization": [r"file", r"located", r"inspected", r"source"],
    "code_inspection": [r"inspected", r"checked", r"reviewed", r"read"],
    "edit_attempt": [r"changed file", r"modified", r"edited", r"patch", r"change"],
    "test_attempt": [r"test", r"pytest", r"check", r"validation"],
    "observation": [r"result", r"passed", r"failed", r"error", r"observed"],
    "final_summary": [r"changed files", r"tests", r"blocker"],
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} did not contain an object")
    return value


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def validate_run(run_dir: Path) -> dict[str, Any]:
    done_path = run_dir / "done.json"
    raw_path = run_dir / "raw_trajectory.json"
    last_path = run_dir / "last_message.md"
    done = load_json(done_path)
    raw = load_json(raw_path)
    last_message = last_path.read_text(encoding="utf-8", errors="replace") if last_path.exists() else ""
    events = raw.get("events") if isinstance(raw.get("events"), list) else []
    event_text = "\n".join(str(event.get("content", "")) for event in events if isinstance(event, dict))
    text = f"{event_text}\n{last_message}"

    missing = [name for name, patterns in REQUIRED_MARKERS.items() if not has_any(text, patterns)]
    final = raw.get("final") if isinstance(raw.get("final"), dict) else {}
    changed_files = final.get("changed_files") if isinstance(final.get("changed_files"), list) else []
    tests = final.get("tests") if isinstance(final.get("tests"), list) else []
    if not changed_files and not has_any(text, [r"changed files?:\s*(?!none|n/a)", r"modified", r"edited", r"patch"]):
        missing.append("evidence_of_changed_files_or_patch_attempt")
    if not tests and not has_any(text, [r"pytest", r"test command", r"tests? run", r"validation command", r"check attempted"]):
        missing.append("evidence_of_test_or_check_attempt")

    status = str(done.get("normalized_status") or final.get("status") or done.get("status") or "invalid")
    return {
        "run_dir": str(run_dir),
        "trajectory_id": done.get("trajectory_id") or raw.get("trajectory_id"),
        "repo": done.get("repo_full_id") or raw.get("repo"),
        "task_id": done.get("task_id") or raw.get("task_id"),
        "status": status,
        "missing": sorted(set(missing)),
        "valid_complete_process": status in {"success", "partial"} and not missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run_dirs = sorted(path.parent for path in args.input_root.glob("*/*/done.json"))
    results = [validate_run(path) for path in run_dirs]
    summary = {
        "input_root": str(args.input_root),
        "checked_count": len(results),
        "valid_count": sum(1 for result in results if result["valid_complete_process"]),
        "invalid_count": sum(1 for result in results if not result["valid_complete_process"]),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["invalid_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
