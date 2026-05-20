# Dev 2 Rollout Harness Evidence

## Assignment Acknowledgement

- Date: 2026-05-20
- Intern: `intern_code_dev_2`
- Owner area: Codex rollout harness for 100 trajectories per repo.
- Final workspace machine: `ssh -p 31787 root@10.100.194.40`.
- Target repos:
  - `/root/workspace/fastapi`
  - `/root/workspace/scikit-learn`
  - `/root/workspace/rich`
- Durable reporting rule acknowledged: routine confirmations/status/findings/blockers/test info are written here, task docs, PR comments, or PM-named evidence paths; no routine peer_send to PM.

## Harness Artifact

- Local evidence source: `evidence/rollout_harness/run_codex_rollouts.py`
- Session 4 10-total task input: `evidence/rollout_harness/tasks_m1_10.jsonl`
- 300-run launcher helper: `evidence/rollout_harness/launch_300_rollouts.sh`
- SFT conversion helper: `evidence/rollout_harness/convert_rollouts_to_sft.py`
- Complete-process validator: `evidence/rollout_harness/validate_complete_coding_trajectories.py`
- Sample smoke input: `evidence/rollout_harness/sample_tasks.jsonl`
- Remote install path: `/root/workspace/rollout_harness/run_codex_rollouts.py`
- Default output root: `/root/workspace/rollouts`
- Default Codex command on final workspace: `/usr/local/bin/codex`

## Harness Capabilities

- Accepts JSONL tasks with `repo`, `task_id`, and `prompt`.
- Caps selected tasks with `--limit-per-repo`, defaulting to 100 per repo.
- Writes one trajectory directory per task under `/root/workspace/rollouts/{repo}/{task_id}`.
- Writes `metadata.json`, `prompt.md`, `stdout.jsonl`, `stderr.log`, `last_message.md`, `raw_trajectory.json`, and `done.json` per task.
- Writes append-only `manifest.jsonl`, cumulative `manifest_summary.json`, cumulative backward-compatible `summary.json`, and `last_run_summary.json`.
- Supports resume by skipping trajectories with existing `done.json`.
- Supports `--force` reruns, `--dry-run` smoke runs, configurable `--timeout-seconds`, and configurable `--codex-cmd`/`CODEX_CMD`.
- Tracks failure accounting using statuses `passed`, `failed`, `timeout`, `skipped_existing`, and `dry_run`.
- Adds stable `trajectory_id` as `{repo_slug}__{task_id}` and full repo ids for dev_3:
  - `fastapi` -> `fastapi/fastapi`
  - `scikit-learn` -> `scikit-learn/scikit-learn`
  - `rich` -> `Textualize/rich`

## Artifact Contract

- Real run: `stdout.jsonl` and `stderr.log` capture Codex process output, `last_message.md` is produced by Codex `--output-last-message`, and `raw_trajectory.json` contains ordered user/assistant events plus final status.
- Dry run: Codex is not executed, but the same file set is created. `stdout.jsonl` and `stderr.log` are empty placeholders, `last_message.md` states that Codex was not executed, and `raw_trajectory.json` contains a user prompt event plus an assistant placeholder event.
- `raw_trajectory.json.final.status` uses dev_3-compatible normalized values: `success`, `partial`, `failed`, or `invalid`. Dry-run fixtures use `invalid` with `final.raw_status: dry_run`.
- `summary.json` is cumulative and reconciles with append-only `manifest.jsonl`; `last_run_summary.json` is the current invocation only.

## Current Findings

- Remote SSH is reachable.
- Repos exist and are clean at:
  - `/root/workspace/fastapi` at `f4cafbc467c225263ad3b5b0d4a7306b42ac855b` on `master`
  - `/root/workspace/scikit-learn` at `ffc6cdc20b8d5eb58e38042fd90a2aeecc33dfb8` on `main`
  - `/root/workspace/rich` at `46cebbb032f920eb096efbaf23cdc6fe9dd541f7` on `master`
- `python3`, `git`, and `timeout` exist on the remote machine.
- Harness was copied to `/root/workspace/rollout_harness/run_codex_rollouts.py`.
- `/usr/local/bin/codex` exists and is executable on the corrected final workspace.
- Smoke dry-run wrote expected files under `/root/workspace/rollouts_smoke_v3`.
- Tiny non-dry rollout on corrected final workspace wrote expected files under `/root/workspace/rollouts_nondry_new_machine_tiny` and returned `passed: 1`.

## Active Blockers

- No active dev_2 harness blocker on the corrected final workspace. PM generated the first 300-task input at `/root/workspace/rollout_harness/tasks_300.jsonl` and started the full rollout in the background.
- Session 3 run coordination note: PM-started direct full rollout is active at pid `1208139` using output root `/root/workspace/rollouts_m1_300`. Do not start a second real 300-run job against `/root/workspace/rollouts` while that pid is active.
- Session 5 update: no active dev_2 blocker for the 10-total rollout. `/root/workspace/rollouts_m1_10` reached 10 manifest entries, all `passed`; pid `1341184` is no longer running.

## Intended Full Run

PM-started direct run currently in progress:

```bash
ssh -p 31787 root@10.100.194.40
export CODEX_CMD=/usr/local/bin/codex
python3 /root/workspace/rollout_harness/run_codex_rollouts.py \
  --tasks /root/workspace/rollout_harness/tasks_300.jsonl \
  --output-root /root/workspace/rollouts_m1_300 \
  --limit-per-repo 100 \
  --timeout-seconds 3600
```

Prepared batched launcher for `/root/workspace/rollouts` after the active PM run is complete or explicitly stopped:

```bash
ssh -p 31787 root@10.100.194.40
mkdir -p /root/workspace/rollouts/_launcher_logs
nohup env \
  TASKS_FILE=/root/workspace/rollout_harness/tasks_300.jsonl \
  OUTPUT_ROOT=/root/workspace/rollouts \
  CODEX_CMD=/usr/local/bin/codex \
  EXPECT_PER_REPO=100 \
  TIMEOUT_SECONDS=3600 \
  /root/workspace/rollout_harness/launch_300_rollouts.sh launch \
  > /root/workspace/rollouts/_launcher_logs/launch_300_$(date -u +%Y%m%dT%H%M%SZ).log 2>&1 &
echo $! > /root/workspace/rollouts/_launcher_logs/launch_300.pid
```

Resume is the same launcher command; completed trajectories with existing `done.json` are skipped by the harness.

```bash
ssh -p 31787 root@10.100.194.40
TASKS_FILE=/root/workspace/rollout_harness/tasks_300.jsonl \
OUTPUT_ROOT=/root/workspace/rollouts \
CODEX_CMD=/usr/local/bin/codex \
EXPECT_PER_REPO=100 \
TIMEOUT_SECONDS=3600 \
/root/workspace/rollout_harness/launch_300_rollouts.sh resume
```

Status/failure accounting:

```bash
ssh -p 31787 root@10.100.194.40
OUTPUT_ROOT=/root/workspace/rollouts_m1_300 /root/workspace/rollout_harness/launch_300_rollouts.sh status
OUTPUT_ROOT=/root/workspace/rollouts /root/workspace/rollout_harness/launch_300_rollouts.sh status
```

## Validation Log

- 2026-05-20: Assignment accepted and personal `status.md` updated to Working for `milestone1_qwen3_8b_loop`.
- 2026-05-20: Initial harness implemented in evidence directory.
- 2026-05-20: Local `python3 -m py_compile` passed for `run_codex_rollouts.py`.
- 2026-05-20: Remote copy installed under `/root/workspace/rollout_harness`.
- 2026-05-20: Remote `python3 -m py_compile /root/workspace/rollout_harness/run_codex_rollouts.py` passed.
- 2026-05-20: Scratch host preflight confirmed repos are present and clean, but returned status 2 because `codex` was not found on PATH.
- 2026-05-20: Scratch host dry-run smoke with one sample task per repo passed and produced `/root/workspace/rollouts_smoke/{manifest.jsonl,summary.json}` plus per-task `metadata.json`, `prompt.md`, and `done.json`.
- 2026-05-20: Scratch host resume smoke rerun against existing `/root/workspace/rollouts_smoke` produced `skipped_existing: 3`, confirming completed trajectories are not rerun by default.
- 2026-05-20: Scratch host follow-up implementation used `/mnt/3fs/data/tools/codex`; corrected final workspace now uses `/usr/local/bin/codex`.
- 2026-05-20: Follow-up implementation made dry-run create the same per-task file set as real runs: `metadata.json`, `prompt.md`, `stdout.jsonl`, `stderr.log`, `last_message.md`, `raw_trajectory.json`, and `done.json`.
- 2026-05-20: Follow-up implementation changed summary semantics: `summary.json` and `manifest_summary.json` are cumulative over append-only `manifest.jsonl`; `last_run_summary.json` is current invocation only.
- 2026-05-20: Follow-up implementation added `trajectory_id`, `repo_full_id`, and dev_3-compatible `raw_trajectory.json` with full repo id, ordered events, repo commit, task id, prompt, and normalized final status.
- 2026-05-20: Scratch host preflight returned status 0 with Codex command path `/mnt/3fs/data/tools/codex`.
- 2026-05-20: Scratch host dry-run and resume smoke regenerated under `/root/workspace/rollouts_smoke_v2`; required file check passed for all three repos.
- 2026-05-20: PM corrected final workspace address to `ssh -p 31787 root@10.100.194.40`; earlier scratch-host outputs are scratch only.
- 2026-05-20: Verified corrected final workspace has clean repo clones at `/root/workspace/{fastapi,scikit-learn,rich}` with the same commits as earlier scratch checks.
- 2026-05-20: Verified local evidence harness and corrected final workspace harness have matching sha256 `43ae7d06e3fc9c380eb7e629858e728818110ea1c3e77ee19ddede05751b60fd`.
- 2026-05-20: Corrected final workspace preflight returned status 0 with Codex command path `/usr/local/bin/codex`.
- 2026-05-20: Corrected final workspace dry-run smoke exists at `/root/workspace/rollouts_smoke_v3`; all three repo task directories contain the full required artifact set.
- 2026-05-20: Corrected final workspace tiny non-dry rollout exists at `/root/workspace/rollouts_nondry_new_machine_tiny`; manifest summary is `passed: 1` for `fastapi/fastapi`.
- 2026-05-20: PM generated `/root/workspace/rollout_harness/tasks_300.jsonl` with 300 records, 100 per selected repo and 300 unique task ids.
- 2026-05-20: PM started full 300 rollout in the background on the corrected final workspace: pid file `/root/workspace/rollout_harness/rollouts_m1_300.pid`, log `/root/workspace/rollout_harness/rollouts_m1_300.log`, output root `/root/workspace/rollouts_m1_300`.
- 2026-05-20: Session 3 launcher wrapper created at `evidence/rollout_harness/launch_300_rollouts.sh` and deployed to `/root/workspace/rollout_harness/launch_300_rollouts.sh`.
- 2026-05-20: Launcher wrapper local/remote sha256 match: `f28d53a958ef6ff2ebaac1d9208a9c0f326423debab2d8d5fbd5fe6906019b23`.
- 2026-05-20: Launcher preflight on corrected final workspace returned status 0 with `/usr/local/bin/codex`.
- 2026-05-20: Launcher dry-run smoke against `sample_tasks.jsonl` passed using `/root/workspace/rollouts_launch_smoke`; manifest summary is `dry_run: 3` and per-repo done counts are 1 each.
- 2026-05-20: Actual `/root/workspace/rollout_harness/tasks_300.jsonl` validated and split into `/root/workspace/rollout_harness/tasks_300_by_repo/{fastapi,scikit-learn,rich}.jsonl`, 100 tasks each.
- 2026-05-20: Current PM-started full run status: pid `1208139` active; `/root/workspace/rollouts_m1_300` has `manifest_count 0` and done counts `fastapi=0`, `scikit-learn=0`, `rich=0`.
- 2026-05-20: Prepared `/root/workspace/rollouts_m1_300` launch/resume commands but did not start a second launcher to avoid colliding with the active PM-started full rollout.
- 2026-05-20: Remote launcher `status` mode reports output root `/root/workspace/rollouts_m1_300`; latest PM snapshot shows PID `1208139` alive, `manifest_count 1`, and `fastapi_done 1 {'passed': 1}`.
- 2026-05-20: PM observed remote `tasks_300.jsonl` now uses full repo IDs plus `repo_key`; launcher `prepare` was updated to accept slug, full repo ID, or `repo_key`, then redeployed. New launcher sha256 is `9348ec8468b3e1e707d1554c0d446c52195dd836b9a6aa12598190f7c1571505`.
- 2026-05-20: PM started independent parallel repo batches to avoid idle waiting on sequential rollout order:
  - scikit-learn: pid `/root/workspace/rollout_harness/rollouts_m1_300_scikit_learn.pid`, output root `/root/workspace/rollouts_m1_300_scikit_learn`;
  - rich: pid `/root/workspace/rollout_harness/rollouts_m1_300_rich.pid`, output root `/root/workspace/rollouts_m1_300_rich`.
- 2026-05-20: Latest PM rollout snapshot: main PID `1208139` alive with `manifest_count 3` and three FastAPI passes; scikit-learn PID `1270557` alive with no manifest yet; rich PID `1270562` alive with no manifest yet.
- 2026-05-20: PM deployed `convert_rollouts_to_sft.py` at `/root/workspace/rollout_harness/convert_rollouts_to_sft.py` for dev_3 handoff; converter smoke over `/root/workspace/rollouts_m1_300` kept 3/3 real FastAPI trajectories with zero errors.

## Session 4 Scope Change - 10 Total Complete Coding Trajectories

- Supervisor changed Milestone 1 rollout target from 300/100-per-repo to 10 total trajectories for an end-to-end smoke loop.
- Old outputs are scratch-only and must not be used as final success evidence:
  - `/root/workspace/rollouts_m1_300` stopped at 6 manifest entries;
  - `/root/workspace/rollouts_m1_300_scikit_learn` stopped at 7 manifest entries;
  - `/root/workspace/rollouts_m1_300_rich` stopped at 5 manifest entries.
- PM stopped/superseded old parent PIDs `1208139`, `1270557`, `1270562`; observed codex child PIDs `1326371`, `1326392`, `1329762`, `1329783`, `1333349`, and `1333370` are dead.
- Remote scratch markers:
  - `/root/workspace/rollout_harness/STOPPED_OLD_300_ROLLOUTS_AT.txt`;
  - `/root/workspace/rollout_harness/OLD_300_OUTPUTS_SCRATCH_ONLY.txt`.
- Active input: `/root/workspace/rollout_harness/tasks_m1_10.jsonl`, exactly 10 records with per-repo split `fastapi=4`, `scikit-learn=3`, `rich=3`.
- Active output root: `/root/workspace/rollouts_m1_10`.
- Active non-dry rollout PID: `1341184`.
- Active log: `/root/workspace/rollout_harness/rollouts_m1_10.log`.
- Acceptance: every final trajectory must pass `validate_complete_coding_trajectories.py` for complete coding process, including actual edit/patch attempt and test/check attempt.
- Latest validation snapshot: `/root/workspace/rollouts_m1_10` has 4 manifest entries, PID `1341184` is alive, and `/root/workspace/rollouts_m1_10/complete_process_validation.json` reports 4 checked, 4 valid, 0 invalid.
- Final Session 5 rollout result: `/root/workspace/rollouts_m1_10/manifest.jsonl` has 10 entries; rollout PID `1341184` is no longer alive after completion; complete-process validation reports 10 checked, 10 valid, 0 invalid.

## Session 5 10-Total Rollout Monitor

- 2026-05-20: Read-only monitor check; did not interrupt `/root/workspace/rollouts_m1_10`.
- PID file `/root/workspace/rollout_harness/rollouts_m1_10.pid` contains `1341184`; `ps -p 1341184` shows no running process.
- Log `/root/workspace/rollout_harness/rollouts_m1_10.log` ends with the 10th trajectory and last-run summary `passed: 10`.
- `/root/workspace/rollouts_m1_10/summary.json` and `manifest_summary.json` report total 10, `passed: 10`.
- Per-repo manifest counts: `fastapi=4`, `scikit-learn=3`, `rich=3`.
- Failure accounting: `failed=0`, `timeout=0`, non-passed manifest rows `0`.
- Done file count: `10`.
- Existing `/root/workspace/rollouts_m1_10/complete_process_validation.json` is stale at 9 checked, 9 valid, 0 invalid.
- Read-only validation rerun to `/tmp/rollouts_m1_10_complete_process_validation_session5.json` reports 10 checked, 10 valid, 0 invalid.

Rerun/failure strategy if any of the 10 fail or hang:

1. Do not interrupt a live rollout process. First verify liveness with `ps -p $(cat /root/workspace/rollout_harness/rollouts_m1_10.pid) -o pid,stat,etime,cmd` and inspect `/root/workspace/rollout_harness/rollouts_m1_10.log`.
2. If the process is alive but no log, manifest, or current task artifact changes for more than the agreed timeout window, record hang evidence before any intervention.
3. Preserve `/root/workspace/rollouts_m1_10` as immutable evidence. Rerun failed or hung replacements into a new root such as `/root/workspace/rollouts_m1_10_rerun_YYYYmmddTHHMMSSZ`.
4. Build replacement JSONL from failed/hung task IDs, or substitute unused same-repo tasks to preserve the 4/3/3 distribution. Avoid `--force` on the original root unless PM explicitly chooses overwrite.
5. Validate the rerun root with `validate_complete_coding_trajectories.py --input-root <rerun_root> --output <rerun_root>/complete_process_validation.json`.
6. Downstream handoff should include only `passed` trajectories that also pass complete-process validation.

## Preflight Snapshot

```json
{
  "checked_at": "2026-05-20T06:22:11+00:00",
  "status": 0,
  "codex_path": "/usr/local/bin/codex",
  "repos_clean": {
    "fastapi": true,
    "scikit-learn": true,
    "rich": true
  }
}
```

## Smoke Summary

```json
{
  "summary_type": "manifest",
  "total": 3,
  "totals": {
    "dry_run": 3
  },
  "by_repo": {
    "fastapi/fastapi": {
      "dry_run": 1
    },
    "scikit-learn/scikit-learn": {
      "dry_run": 1
    },
    "Textualize/rich": {
      "dry_run": 1
    }
  }
}
```

## Scratch Host Resume Smoke Summary

```json
{
  "total": 3,
  "totals": {
    "skipped_existing": 3
  },
  "by_repo": {
    "fastapi": {
      "skipped_existing": 1
    },
    "scikit-learn": {
      "skipped_existing": 1
    },
    "rich": {
      "skipped_existing": 1
    }
  }
}
```

## PM Verification - Harness v2 and Non-Dry Gate

- 2026-05-20: PM verified dev_2 harness v2 compiles locally and is deployed under `/root/workspace/rollout_harness/run_codex_rollouts.py`.
- 2026-05-20: PM verified `/root/workspace/rollouts_smoke_v2` includes `metadata.json`, `prompt.md`, `stdout.jsonl`, `stderr.log`, `last_message.md`, `done.json`, and `raw_trajectory.json` for each selected repo smoke task. This is now scratch-only evidence after the final workspace address correction.
- 2026-05-20: PM verified `raw_trajectory.json` includes stable `trajectory_id`, full repo ID, ordered message events, repo commit, task ID, and final status fields.
- 2026-05-20: PM verified `summary.json` has `summary_type: manifest` and reconciles with append-only `manifest.jsonl` for the v2 dry-run/resume smoke.
- 2026-05-20: Earlier PM non-dry check on the previous scratch host is scratch-only after address correction.
- 2026-05-20: Corrected final workspace has `/usr/local/bin/codex`; harness preflight passes there.
- 2026-05-20: Corrected final workspace tiny non-dry rollout passed for `fastapi/fastapi` with normalized status `success`; non-dry harness gate is closed for dev_2.

## Corrected Final Workspace Verification

Final workspace: `ssh -p 31787 root@10.100.194.40`

```text
hostname lg-cmc-b7r201-k10u23-cpu-000158
fastapi f4cafbc467c225263ad3b5b0d4a7306b42ac855b clean true
scikit-learn ffc6cdc20b8d5eb58e38042fd90a2aeecc33dfb8 clean true
rich 46cebbb032f920eb096efbaf23cdc6fe9dd541f7 clean true
codex /usr/local/bin/codex
harness_sha256 43ae7d06e3fc9c380eb7e629858e728818110ea1c3e77ee19ddede05751b60fd
```

Dry-run smoke on corrected final workspace:

```text
root /root/workspace/rollouts_smoke_v3
manifest_count 3
summary_type manifest
totals {'dry_run': 3}
required_files_missing []
raw repos fastapi/fastapi, scikit-learn/scikit-learn, Textualize/rich
final statuses invalid, invalid, invalid
```

Tiny non-dry rollout on corrected final workspace:

```text
root /root/workspace/rollouts_nondry_new_machine_tiny
manifest_count 1
summary_type manifest
totals {'passed': 1}
trajectory_id fastapi__fastapi_new_machine_tiny_001
repo fastapi/fastapi
final status success
required_files_missing []
last_message_size 270
stdout_size 125030
stderr_size 39
```

## Session 3 Launch Readiness

Launcher artifact:

```text
local /work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/rollout_harness/launch_300_rollouts.sh
remote /root/workspace/rollout_harness/launch_300_rollouts.sh
sha256 31f3fd95e07f76f66db871481761e1e3c54af8dae15e240865168c01611ad97f
```

Actual task split:

```text
fastapi: wrote 100 tasks to /root/workspace/rollout_harness/tasks_300_by_repo/fastapi.jsonl
scikit-learn: wrote 100 tasks to /root/workspace/rollout_harness/tasks_300_by_repo/scikit-learn.jsonl
rich: wrote 100 tasks to /root/workspace/rollout_harness/tasks_300_by_repo/rich.jsonl
total selected: 300
```

Launcher dry-run smoke:

```text
output_root /root/workspace/rollouts_launch_smoke
summary_type manifest
total 3
totals {'dry_run': 3}
fastapi_done 1 {'dry_run': 1}
scikit-learn_done 1 {'dry_run': 1}
rich_done 1 {'dry_run': 1}
```

Current full-run status:

```text
pm_pid 1208139 active
pm_output_root /root/workspace/rollouts_m1_300
pm_log /root/workspace/rollout_harness/rollouts_m1_300.log
summary.json missing
manifest_summary.json missing
last_run_summary.json missing
manifest_count 0
fastapi_done 0 {}
scikit-learn_done 0 {}
rich_done 0 {}
prepared_output_root /root/workspace/rollouts
prepared_manifest_count 0
```

## Scratch Host Follow-up Gate Self-Check

Command target: old scratch host `/root/workspace/rollouts_smoke_v2`

```text
manifest_count 6
summary manifest 6 {'dry_run': 3, 'skipped_existing': 3}
manifest_summary manifest 6 {'dry_run': 3, 'skipped_existing': 3}
last_run last_run 3 {'skipped_existing': 3}
summary_reconciles True
fastapi fastapi_smoke_001 missing [] trajectory fastapi__fastapi_smoke_001 raw_repo fastapi/fastapi events 2 final invalid meta_full fastapi/fastapi done_norm invalid
scikit-learn scikit_learn_smoke_001 missing [] trajectory scikit-learn__scikit_learn_smoke_001 raw_repo scikit-learn/scikit-learn events 2 final invalid meta_full scikit-learn/scikit-learn done_norm invalid
rich rich_smoke_001 missing [] trajectory rich__rich_smoke_001 raw_repo Textualize/rich events 2 final invalid meta_full Textualize/rich done_norm invalid
```
