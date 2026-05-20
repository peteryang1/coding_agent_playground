#!/usr/bin/env bash
set -euo pipefail

# Launch or inspect the Milestone 1 300-run rollout plan.
#
# Defaults target the corrected final workspace:
#   ssh -p 31787 root@10.100.194.40
#
# Modes:
#   preflight  - validate Codex/repo readiness
#   prepare    - validate and split tasks_300.jsonl into repo batches
#   launch     - run repo batches sequentially; reruns resume from done.json
#   status     - print manifest/summary and per-repo completion counts
#
# Environment overrides:
#   TASKS_FILE=/root/workspace/rollout_harness/tasks_300.jsonl
#   OUTPUT_ROOT=/root/workspace/rollouts_m1_300
#   CODEX_CMD=/usr/local/bin/codex
#   EXPECT_PER_REPO=100
#   TIMEOUT_SECONDS=3600
#   DRY_RUN=0

MODE="${1:-status}"
HARNESS="${HARNESS:-/root/workspace/rollout_harness/run_codex_rollouts.py}"
TASKS_FILE="${TASKS_FILE:-/root/workspace/rollout_harness/tasks_300.jsonl}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/root/workspace/rollouts_m1_300}"
CODEX_CMD="${CODEX_CMD:-/usr/local/bin/codex}"
EXPECT_PER_REPO="${EXPECT_PER_REPO:-100}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-3600}"
DRY_RUN="${DRY_RUN:-0}"
BATCH_DIR="${BATCH_DIR:-/root/workspace/rollout_harness/tasks_300_by_repo}"
LOG_DIR="${LOG_DIR:-${OUTPUT_ROOT}/_launcher_logs}"

repos=(fastapi scikit-learn rich)

run_preflight() {
  python3 "$HARNESS" --codex-cmd "$CODEX_CMD" --preflight
}

prepare_batches() {
  TASKS_FILE="$TASKS_FILE" BATCH_DIR="$BATCH_DIR" EXPECT_PER_REPO="$EXPECT_PER_REPO" python3 - <<'PY'
import json
import os
from pathlib import Path

tasks_file = Path(os.environ["TASKS_FILE"])
batch_dir = Path(os.environ["BATCH_DIR"])
expected = int(os.environ["EXPECT_PER_REPO"])
repo_aliases = {
    "fastapi": "fastapi",
    "fastapi/fastapi": "fastapi",
    "scikit-learn": "scikit-learn",
    "scikit-learn/scikit-learn": "scikit-learn",
    "rich": "rich",
    "Textualize/rich": "rich",
}
repos = ("fastapi", "scikit-learn", "rich")

if not tasks_file.exists():
    raise SystemExit(f"missing tasks file: {tasks_file}")

rows = []
counts = {repo: 0 for repo in repos}
seen = set()
for lineno, line in enumerate(tasks_file.read_text(encoding="utf-8").splitlines(), 1):
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        continue
    record = json.loads(stripped)
    for field in ("repo", "task_id", "prompt"):
        if not record.get(field):
            raise SystemExit(f"{tasks_file}:{lineno}: missing {field}")
    repo = repo_aliases.get(str(record.get("repo_key") or record["repo"]))
    if repo not in counts:
        raise SystemExit(f"{tasks_file}:{lineno}: unsupported repo {record['repo']!r}")
    record["repo"] = repo
    key = (repo, str(record["task_id"]))
    if key in seen:
        raise SystemExit(f"{tasks_file}:{lineno}: duplicate repo/task_id {key}")
    seen.add(key)
    counts[repo] += 1
    rows.append(record)

problems = [f"{repo}={count}, expected >= {expected}" for repo, count in counts.items() if count < expected]
if problems:
    raise SystemExit("insufficient tasks: " + "; ".join(problems))

batch_dir.mkdir(parents=True, exist_ok=True)
for repo in repos:
    path = batch_dir / f"{repo}.jsonl"
    selected = [record for record in rows if record["repo"] == repo][:expected]
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in selected), encoding="utf-8")
    print(f"{repo}: wrote {len(selected)} tasks to {path}")
print(f"total selected: {expected * len(repos)}")
PY
}

launch_batches() {
  mkdir -p "$LOG_DIR"
  run_preflight
  prepare_batches
  for repo in "${repos[@]}"; do
    batch_file="${BATCH_DIR}/${repo}.jsonl"
    log_file="${LOG_DIR}/${repo}_$(date -u +%Y%m%dT%H%M%SZ).log"
    cmd=(
      python3 "$HARNESS"
      --tasks "$batch_file"
      --output-root "$OUTPUT_ROOT"
      --limit-per-repo "$EXPECT_PER_REPO"
      --timeout-seconds "$TIMEOUT_SECONDS"
      --codex-cmd "$CODEX_CMD"
    )
    if [[ "$DRY_RUN" == "1" ]]; then
      cmd+=(--dry-run)
    fi
    printf 'launching %s batch, log=%s\n' "$repo" "$log_file"
    "${cmd[@]}" 2>&1 | tee "$log_file"
  done
}

print_status() {
  OUTPUT_ROOT="$OUTPUT_ROOT" python3 - <<'PY'
import json
import os
from pathlib import Path

root = Path(os.environ["OUTPUT_ROOT"])
print(f"output_root {root}")
for name in ("summary.json", "manifest_summary.json", "last_run_summary.json"):
    path = root / name
    if path.exists():
        print(f"{name} {path.read_text(encoding='utf-8').strip()}")
    else:
        print(f"{name} missing")

manifest = root / "manifest.jsonl"
if manifest.exists():
    rows = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()]
    statuses = sorted({row.get("status") for row in rows})
    print("manifest_count", len(rows), {status: sum(1 for row in rows if row.get("status") == status) for status in statuses})
else:
    print("manifest_count 0")

for repo in ("fastapi", "scikit-learn", "rich"):
    repo_dir = root / repo
    done = sorted(repo_dir.glob("*/done.json")) if repo_dir.exists() else []
    counts = {}
    for path in done:
        try:
            status = json.loads(path.read_text(encoding="utf-8")).get("status", "unknown")
        except Exception:
            status = "unreadable"
        counts[status] = counts.get(status, 0) + 1
    print(f"{repo}_done {len(done)} {counts}")
PY
}

case "$MODE" in
  preflight)
    run_preflight
    ;;
  prepare)
    prepare_batches
    ;;
  launch|resume)
    launch_batches
    ;;
  status)
    print_status
    ;;
  *)
    echo "usage: $0 {preflight|prepare|launch|resume|status}" >&2
    exit 2
    ;;
esac
