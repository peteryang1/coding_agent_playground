#!/usr/bin/env python3
"""Run resumable Codex rollouts for repository coding tasks.

Input tasks are JSONL records. Required fields:
  - repo: fastapi, scikit-learn, or rich
  - task_id: stable identifier unique within the repo
  - prompt: instruction passed to Codex

Optional fields are preserved in per-run metadata. The harness writes one
trajectory directory per task and can be rerun safely; completed trajectories
are skipped unless --force is set.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


REPOS: dict[str, dict[str, str]] = {
    "fastapi": {"full_id": "fastapi/fastapi", "path": "/root/workspace/fastapi"},
    "scikit-learn": {
        "full_id": "scikit-learn/scikit-learn",
        "path": "/root/workspace/scikit-learn",
    },
    "rich": {"full_id": "Textualize/rich", "path": "/root/workspace/rich"},
}

DEFAULT_OUTPUT_ROOT = Path("/root/workspace/rollouts")
DEFAULT_TIMEOUT_SECONDS = 60 * 60
DEFAULT_CODEX_CMD = "/usr/local/bin/codex"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            for field in ("repo", "task_id", "prompt"):
                if not record.get(field):
                    raise SystemExit(f"{path}:{lineno}: missing required field {field!r}")
            if record["repo"] not in REPOS:
                raise SystemExit(
                    f"{path}:{lineno}: repo must be one of {sorted(REPOS)}, got {record['repo']!r}"
                )
            records.append(record)
    return records


def repo_git_metadata(repo_path: Path) -> dict[str, str]:
    def git(args: list[str]) -> str:
        return subprocess.check_output(
            ["git", "-C", str(repo_path), *args],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()

    metadata = {
        "path": str(repo_path),
        "head": git(["rev-parse", "HEAD"]),
        "branch": git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "status_short": git(["status", "--short"]),
    }
    try:
        metadata["remote_origin"] = git(["remote", "get-url", "origin"])
    except subprocess.CalledProcessError:
        metadata["remote_origin"] = ""
    return metadata


def repo_path(repo: str) -> Path:
    return Path(REPOS[repo]["path"])


def repo_full_id(repo: str) -> str:
    return REPOS[repo]["full_id"]


def filesystem_safe(value: str) -> str:
    return "".join(char if char.isalnum() or char in "._-" else "_" for char in value)


def trajectory_id(repo: str, task_id: str) -> str:
    return f"{filesystem_safe(repo)}__{filesystem_safe(task_id)}"


def normalized_status(status: str) -> str:
    if status == "passed":
        return "success"
    if status in {"failed", "skipped_existing"}:
        return "failed"
    if status == "timeout":
        return "partial"
    if status == "dry_run":
        return "invalid"
    return "invalid"


def run_preflight(codex_cmd: str) -> int:
    checks: list[dict[str, Any]] = []
    status = 0

    codex_binary = shlex.split(codex_cmd)[0] if codex_cmd.strip() else "codex"
    codex_path = shutil_which(codex_binary)
    checks.append({"name": "codex_command", "command": codex_cmd, "path": codex_path})
    if not codex_path:
        status = 2

    for repo in REPOS:
        path = repo_path(repo)
        item: dict[str, Any] = {"name": f"repo:{repo}", "path": str(path), "exists": path.is_dir()}
        if path.is_dir():
            try:
                item.update(repo_git_metadata(path))
                item["clean"] = item["status_short"] == ""
            except subprocess.CalledProcessError as exc:
                item["error"] = exc.output
                status = 2
        else:
            status = 2
        checks.append(item)

    print(json.dumps({"checked_at": utc_now(), "status": status, "checks": checks}, indent=2))
    return status


def shutil_which(command: str) -> str | None:
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / command
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def build_codex_command(codex_cmd: str, prompt: str, output_file: Path) -> list[str]:
    parts = shlex.split(codex_cmd)
    if not parts:
        raise SystemExit("CODEX command cannot be empty")
    # Default command template targets Codex CLI in non-interactive mode.
    # Override with --codex-cmd when local CLI flags differ.
    return [
        *parts,
        "exec",
        "--json",
        "--output-last-message",
        str(output_file),
        prompt,
    ]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def load_jsonl_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def ensure_artifact_files(
    stdout_file: Path,
    stderr_file: Path,
    last_message_file: Path,
    dry_run: bool,
) -> None:
    if dry_run:
        stdout_file.write_text("", encoding="utf-8")
        stderr_file.write_text("", encoding="utf-8")
        last_message_file.write_text("DRY RUN: Codex was not executed.\n", encoding="utf-8")
        return
    for path in (stdout_file, stderr_file, last_message_file):
        path.touch(exist_ok=True)


def write_raw_trajectory(
    path: Path,
    record: dict[str, Any],
    metadata: dict[str, Any],
    result: dict[str, Any],
    dry_run: bool,
) -> None:
    timestamp = result.get("finished_at") or utc_now()
    events = [
        {
            "type": "message",
            "role": "user",
            "content": str(record["prompt"]),
            "timestamp": metadata["started_at"],
        }
    ]
    if dry_run:
        events.append(
            {
                "type": "message",
                "role": "assistant",
                "content": "DRY RUN: Codex was not executed; artifact files are placeholders.",
                "timestamp": timestamp,
            }
        )
    else:
        last_message = Path(result["last_message"]).read_text(encoding="utf-8", errors="replace")
        events.append(
            {
                "type": "message",
                "role": "assistant",
                "content": last_message,
                "timestamp": timestamp,
            }
        )
    raw = {
        "trajectory_id": metadata["trajectory_id"],
        "repo": metadata["repo_full_id"],
        "repo_slug": metadata["repo"],
        "repo_path": metadata["repo_metadata"]["path"],
        "repo_commit": metadata["repo_metadata"]["head"],
        "task_id": metadata["task_id"],
        "prompt": str(record["prompt"]),
        "events": events,
        "final": {
            "status": normalized_status(result["status"]),
            "raw_status": result["status"],
            "summary": result.get("summary", ""),
            "changed_files": [],
            "tests": [],
        },
    }
    write_json(path, raw)


def run_one(
    record: dict[str, Any],
    output_root: Path,
    codex_cmd: str,
    timeout_seconds: int,
    force: bool,
    dry_run: bool,
) -> dict[str, Any]:
    repo = record["repo"]
    task_id = str(record["task_id"])
    stable_trajectory_id = trajectory_id(repo, task_id)
    path_for_repo = repo_path(repo)
    run_dir = output_root / repo / task_id
    done_file = run_dir / "done.json"
    if done_file.exists() and not force:
        previous = json.loads(done_file.read_text(encoding="utf-8"))
        return {
            "trajectory_id": stable_trajectory_id,
            "repo": repo,
            "repo_full_id": repo_full_id(repo),
            "task_id": task_id,
            "status": "skipped_existing",
            "previous_status": previous.get("status"),
            "normalized_status": previous.get(
                "normalized_status", normalized_status(str(previous.get("status", "")))
            ),
            "run_dir": str(run_dir),
            "raw_trajectory": str(run_dir / "raw_trajectory.json"),
        }

    run_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = run_dir / "prompt.md"
    stdout_file = run_dir / "stdout.jsonl"
    stderr_file = run_dir / "stderr.log"
    last_message_file = run_dir / "last_message.md"
    meta_file = run_dir / "metadata.json"
    raw_trajectory_file = run_dir / "raw_trajectory.json"

    prompt_file.write_text(str(record["prompt"]).rstrip() + "\n", encoding="utf-8")
    metadata = {
        "trajectory_id": stable_trajectory_id,
        "repo": repo,
        "repo_full_id": repo_full_id(repo),
        "task_id": task_id,
        "record": record,
        "repo_metadata": repo_git_metadata(path_for_repo),
        "run_dir": str(run_dir),
        "started_at": utc_now(),
        "codex_cmd": codex_cmd,
        "timeout_seconds": timeout_seconds,
        "dry_run": dry_run,
    }
    write_json(meta_file, metadata)

    if dry_run:
        ensure_artifact_files(stdout_file, stderr_file, last_message_file, dry_run=True)
        result = {
            "trajectory_id": stable_trajectory_id,
            "repo": repo,
            "repo_full_id": repo_full_id(repo),
            "task_id": task_id,
            "status": "dry_run",
            "normalized_status": normalized_status("dry_run"),
            "returncode": 0,
            "run_dir": str(run_dir),
            "finished_at": utc_now(),
            "stdout": str(stdout_file),
            "stderr": str(stderr_file),
            "last_message": str(last_message_file),
            "raw_trajectory": str(raw_trajectory_file),
        }
        write_raw_trajectory(raw_trajectory_file, record, metadata, result, dry_run=True)
        write_json(done_file, result)
        return result

    command = build_codex_command(codex_cmd, str(record["prompt"]), last_message_file)
    started = time.monotonic()
    try:
        with stdout_file.open("w", encoding="utf-8") as stdout, stderr_file.open(
            "w", encoding="utf-8"
        ) as stderr:
            proc = subprocess.run(
                command,
                cwd=str(path_for_repo),
                stdout=stdout,
                stderr=stderr,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
        status = "passed" if proc.returncode == 0 else "failed"
        returncode = proc.returncode
    except subprocess.TimeoutExpired:
        status = "timeout"
        returncode = 124

    ensure_artifact_files(stdout_file, stderr_file, last_message_file, dry_run=False)
    result = {
        "trajectory_id": stable_trajectory_id,
        "repo": repo,
        "repo_full_id": repo_full_id(repo),
        "task_id": task_id,
        "status": status,
        "normalized_status": normalized_status(status),
        "returncode": returncode,
        "run_dir": str(run_dir),
        "duration_seconds": round(time.monotonic() - started, 3),
        "finished_at": utc_now(),
        "stdout": str(stdout_file),
        "stderr": str(stderr_file),
        "last_message": str(last_message_file),
        "raw_trajectory": str(raw_trajectory_file),
    }
    write_raw_trajectory(raw_trajectory_file, record, metadata, result, dry_run=False)
    write_json(done_file, result)
    return result


def summarize(results: list[dict[str, Any]], summary_type: str) -> dict[str, Any]:
    by_repo: dict[str, dict[str, int]] = {}
    totals: dict[str, int] = {}
    for result in results:
        repo = result.get("repo_full_id") or result["repo"]
        status = result["status"]
        by_repo.setdefault(repo, {})
        by_repo[repo][status] = by_repo[repo].get(status, 0) + 1
        totals[status] = totals.get(status, 0) + 1
    return {
        "summary_type": summary_type,
        "generated_at": utc_now(),
        "total": len(results),
        "by_repo": by_repo,
        "totals": totals,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, help="JSONL task records")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--codex-cmd", default=os.environ.get("CODEX_CMD", DEFAULT_CODEX_CMD))
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--limit-per-repo", type=int, default=100)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args(argv)

    if args.preflight:
        return run_preflight(args.codex_cmd)

    if not args.tasks:
        raise SystemExit("--tasks is required unless --preflight is set")

    records = load_jsonl(args.tasks)
    selected: list[dict[str, Any]] = []
    counts = {repo: 0 for repo in REPOS}
    for record in records:
        repo = record["repo"]
        if counts[repo] >= args.limit_per_repo:
            continue
        counts[repo] += 1
        selected.append(record)

    manifest_path = args.output_root / "manifest.jsonl"
    results: list[dict[str, Any]] = []
    for record in selected:
        result = run_one(
            record=record,
            output_root=args.output_root,
            codex_cmd=args.codex_cmd,
            timeout_seconds=args.timeout_seconds,
            force=args.force,
            dry_run=args.dry_run,
        )
        results.append(result)
        append_jsonl(manifest_path, result)
        print(json.dumps(result, sort_keys=True), flush=True)

    last_run_summary = summarize(results, "last_run")
    manifest_summary = summarize(load_jsonl_records(manifest_path), "manifest")
    write_json(args.output_root / "last_run_summary.json", last_run_summary)
    write_json(args.output_root / "manifest_summary.json", manifest_summary)
    # Backward-compatible name; semantics are cumulative and reconcile with manifest.jsonl.
    write_json(args.output_root / "summary.json", manifest_summary)
    print(json.dumps(last_run_summary, indent=2, sort_keys=True))

    failure_statuses = {"failed", "timeout"}
    return 1 if any(result["status"] in failure_statuses for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
