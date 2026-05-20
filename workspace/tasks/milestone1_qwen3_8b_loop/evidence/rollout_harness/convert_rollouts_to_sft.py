#!/usr/bin/env python3
"""Convert Codex rollout artifacts into coding_agent_playground_sft_v1 JSONL."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORMAT_VERSION = "coding_agent_playground_sft_v1"
ALLOWED_ROLES = {"system", "user", "assistant", "tool"}
KEEP_STATUSES = {"success", "partial"}
STATUS_MAP = {
    "passed": "success",
    "success": "success",
    "partial": "partial",
    "failed": "failed",
    "timeout": "failed",
    "dry_run": "invalid",
    "invalid": "invalid",
}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?([A-Za-z0-9_\-./+=]{16,})"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-./+=]{16,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
]
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return value


def clean_text(value: Any) -> str:
    text = str(value or "")
    text = ANSI_RE.sub("", text)
    text = CONTROL_RE.sub("", text)
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(lambda match: match.group(0).split(match.group(2))[0] + "<REDACTED_TOKEN>" if len(match.groups()) >= 2 else "<REDACTED_TOKEN>", text)
    return text.strip()


def normalize_status(raw: Any) -> str:
    return STATUS_MAP.get(str(raw or "").strip().lower(), "invalid")


def normalize_role(raw: Any) -> str:
    role = str(raw or "").strip().lower()
    if role in {"developer", "system_prompt"}:
        return "system"
    if role in {"human", "prompt", "task"}:
        return "user"
    if role in {"agent", "model", "assistant_message"}:
        return "assistant"
    if role in ALLOWED_ROLES:
        return role
    return "tool"


def discover_raw_paths(root: Path) -> list[Path]:
    manifest = root / "manifest.jsonl"
    paths: list[Path] = []
    if manifest.exists():
        for line_no, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line)
            raw_path = Path(record.get("raw_trajectory") or "")
            if not raw_path.is_absolute():
                raw_path = root / raw_path
            if not raw_path.exists():
                raise FileNotFoundError(f"{manifest}:{line_no}: missing raw_trajectory {raw_path}")
            paths.append(raw_path)
    else:
        paths = sorted(root.glob("*/*/raw_trajectory.json"))
    return sorted(paths)


def build_record(raw_path: Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    run_dir = raw_path.parent
    raw = load_json(raw_path)
    done = load_json(run_dir / "done.json") if (run_dir / "done.json").exists() else {}
    metadata = load_json(run_dir / "metadata.json") if (run_dir / "metadata.json").exists() else {}

    trajectory_id = clean_text(raw.get("trajectory_id") or done.get("trajectory_id") or metadata.get("trajectory_id") or run_dir.name)
    task_id = clean_text(raw.get("task_id") or done.get("task_id") or metadata.get("task_id") or run_dir.name)
    repo = clean_text(raw.get("repo") or done.get("repo_full_id") or metadata.get("repo_full_id") or raw.get("repo_slug"))
    final = raw.get("final") if isinstance(raw.get("final"), dict) else {}
    status = normalize_status(final.get("status") or done.get("normalized_status") or done.get("status"))
    dry_run = bool(metadata.get("dry_run")) or str(done.get("status")) == "dry_run"

    reject_reason = ""
    events = raw.get("events") if isinstance(raw.get("events"), list) else []
    messages: list[dict[str, str]] = []
    for event in events:
        if not isinstance(event, dict) or event.get("type") != "message":
            continue
        role = normalize_role(event.get("role"))
        content = clean_text(event.get("content"))
        if content:
            messages.append({"role": role, "content": content})

    roles = {message["role"] for message in messages}
    if dry_run:
        reject_reason = "dry_run_placeholder"
    elif status not in KEEP_STATUSES:
        reject_reason = f"status_{status}"
    elif "user" not in roles:
        reject_reason = "missing_user_message"
    elif "assistant" not in roles:
        reject_reason = "missing_assistant_message"
    elif not trajectory_id:
        reject_reason = "missing_trajectory_id"

    source = {
        "rollout_owner": "intern_code_dev_2",
        "generator": "codex",
        "captured_at": clean_text(done.get("finished_at") or metadata.get("started_at") or utc_now()),
        "raw_path": str(raw_path),
        "run_dir": str(run_dir),
    }
    base = {
        "format_version": FORMAT_VERSION,
        "example_id": trajectory_id,
        "repo": repo,
        "repo_path": clean_text(raw.get("repo_path") or metadata.get("repo_path")),
        "trajectory_id": trajectory_id,
        "task_id": task_id,
        "source": source,
        "messages": messages,
        "metadata": {
            "repo_commit": clean_text(raw.get("repo_commit") or metadata.get("repo_commit")),
            "status": status,
            "raw_status": clean_text(final.get("raw_status") or done.get("status")),
            "tests": final.get("tests") if isinstance(final.get("tests"), list) else [],
            "changed_files": final.get("changed_files") if isinstance(final.get("changed_files"), list) else [],
            "duration_seconds": done.get("duration_seconds"),
        },
        "artifacts": {
            "last_message": str(run_dir / "last_message.md"),
            "stdout": str(run_dir / "stdout.jsonl"),
            "stderr": str(run_dir / "stderr.log"),
        },
    }
    if reject_reason:
        return None, {
            "trajectory_id": trajectory_id,
            "task_id": task_id,
            "repo": repo,
            "raw_path": str(raw_path),
            "drop_reason": reject_reason,
            "status": status,
        }
    return base, None


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def convert(root: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_paths = discover_raw_paths(root)
    kept: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen_examples: set[str] = set()
    errors: list[dict[str, str]] = []

    for raw_path in raw_paths:
        try:
            record, rejection = build_record(raw_path)
            if record is not None:
                example_id = record["example_id"]
                if example_id in seen_examples:
                    raise ValueError(f"duplicate example_id {example_id}")
                seen_examples.add(example_id)
                kept.append(record)
            elif rejection is not None:
                rejected.append(rejection)
        except Exception as exc:  # noqa: BLE001 - conversion evidence should record all parse failures.
            errors.append({"raw_path": str(raw_path), "error": str(exc)})

    train_path = output_dir / "train.jsonl"
    rejected_path = output_dir / "rejected.jsonl"
    summary_path = output_dir / "conversion_summary.json"
    write_jsonl(train_path, kept)
    write_jsonl(rejected_path, rejected)
    summary = {
        "format_version": FORMAT_VERSION,
        "input_root": str(root),
        "output_dir": str(output_dir),
        "input_count": len(raw_paths),
        "kept_count": len(kept),
        "dropped_count": len(rejected),
        "error_count": len(errors),
        "per_repo_kept": Counter(row["repo"] for row in kept),
        "per_repo_dropped": Counter(row["repo"] for row in rejected),
        "status_counts": Counter(row["metadata"]["status"] for row in kept),
        "drop_reasons": Counter(row["drop_reason"] for row in rejected),
        "errors": errors,
        "train_path": str(train_path),
        "rejected_path": str(rejected_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True, default=dict) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    summary = convert(args.input_root, args.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True, default=dict))
    return 0 if summary["error_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
