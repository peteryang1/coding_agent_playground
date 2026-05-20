# dev_3 Data Pipeline Evidence

Owner: `intern_code_dev_3`
Task: `milestone1_qwen3_8b_loop`
Area: trajectory schema discovery, normalization, cleaning, and conversion into `coding_agent_playground` data format.

## 2026-05-20 Status

- Assignment received from PM and acknowledged here per durable response rule.
- No routine `peer_send` status was sent to PM.
- PM critical address correction acknowledged: final workspace is `ssh -p 31787 root@10.100.194.40`.
- Earlier scratch-host artifacts are scratch-only and must not be treated as milestone evidence.
- Final workspace SSH check succeeded for `ssh -p 31787 root@10.100.194.40`.
- Final workspace repos exist:
  - `/root/workspace/fastapi` -> `https://github.com/fastapi/fastapi.git`
  - `/root/workspace/scikit-learn` -> `https://github.com/scikit-learn/scikit-learn.git`
  - `/root/workspace/rich` -> `https://github.com/Textualize/rich.git`
- Current valid rollout roots on the corrected machine:
  - `/root/workspace/rollouts_smoke_v3`: 3 raw trajectories, all `invalid` dry-run placeholders.
  - `/root/workspace/rollouts_nondry_new_machine_tiny`: 1 raw trajectory, `success`.
- Local `coding_agent_playground` tree does not contain an existing canonical trajectory data-format spec. I am defining a concrete `coding_agent_playground_sft_v1` JSONL contract below so dev_2 rollout and test_1 validation can target the same shape.

## Corrected-Machine Schema Discovery

Observed per-run files under both corrected-machine rollout roots:

- `metadata.json`: launcher metadata, including `codex_cmd`, `dry_run`, `record.prompt`, `repo_full_id`, `repo_metadata`, `run_dir`, `started_at`, `task_id`, `timeout_seconds`, and `trajectory_id`.
- `done.json`: run completion metadata, including `finished_at`, `normalized_status`, `raw_trajectory`, `repo_full_id`, `returncode`, `status`, `stdout`, `stderr`, `task_id`, and `trajectory_id`.
- `raw_trajectory.json`: compact training source with top-level `events`, `final`, `prompt`, `repo`, `repo_commit`, `repo_path`, `repo_slug`, `task_id`, and `trajectory_id`.
- `stdout.jsonl`: richer Codex event stream with records such as `thread.started`, `turn.started`, `item.started`, and `item.completed`; command outputs can be very large.
- `last_message.md`: final assistant message text.
- `stderr.log`: launcher stderr.

Observed `raw_trajectory.json` shape:

```json
{
  "events": [
    {"type": "message", "role": "user", "content": "...", "timestamp": "2026-05-20T06:21:31+00:00"},
    {"type": "message", "role": "assistant", "content": "...", "timestamp": "2026-05-20T06:21:47+00:00"}
  ],
  "final": {
    "changed_files": [],
    "raw_status": "passed",
    "status": "success",
    "summary": "",
    "tests": []
  },
  "prompt": "...",
  "repo": "fastapi/fastapi",
  "repo_commit": "f4cafbc467c225263ad3b5b0d4a7306b42ac855b",
  "repo_path": "/root/workspace/fastapi",
  "repo_slug": "fastapi",
  "task_id": "fastapi_new_machine_tiny_001",
  "trajectory_id": "fastapi__fastapi_new_machine_tiny_001"
}
```

Read-only conversion dry run results:

```json
[
  {
    "root": "/root/workspace/rollouts_smoke_v3",
    "raw_count": 3,
    "status_counts": {"invalid": 3},
    "errors": []
  },
  {
    "root": "/root/workspace/rollouts_nondry_new_machine_tiny",
    "raw_count": 1,
    "status_counts": {"success": 1},
    "errors": []
  }
]
```

Conversion decision:

- Use `raw_trajectory.json` as the primary SFT source because it is compact, already ordered, and has clean chat-style `events`.
- Use `done.json` and `metadata.json` to fill `source`, status, duration, paths, and launcher metadata.
- Use `stdout.jsonl` as optional diagnostic evidence only. It should not be included wholesale in SFT examples because command output can dominate context; if needed, retain only compact command summaries or final assistant messages.
- Treat `dry_run=true`, `done.status=dry_run`, or `final.status=invalid` placeholder trajectories as dropped from training with `quality.keep=false` and `drop_reason=dry_run_placeholder`.

## Proposed Output Format: `coding_agent_playground_sft_v1`

One JSON object per line. Each line is one cleaned training example derived from one assistant action or one full trajectory, depending on downstream trainer preference. Default for Qwen SFT should be one full trajectory per line to preserve planning context.

Required top-level fields:

```json
{
  "format_version": "coding_agent_playground_sft_v1",
  "example_id": "fastapi__000001",
  "repo": "fastapi/fastapi",
  "repo_path": "/root/workspace/fastapi",
  "trajectory_id": "fastapi__000001",
  "task_id": "fastapi__seed_000001",
  "source": {
    "rollout_owner": "intern_code_dev_2",
    "generator": "codex",
    "captured_at": "2026-05-20T00:00:00Z",
    "raw_path": "/root/workspace/rollouts/fastapi/000001.json"
  },
  "messages": [
    {"role": "system", "content": "You are Codex, a coding agent."},
    {"role": "user", "content": "Task prompt..."},
    {"role": "assistant", "content": "Reasoning-safe assistant response or action summary..."}
  ],
  "metadata": {
    "repo_commit": "git sha",
    "branch": "rollout branch if any",
    "status": "success",
    "tests": [{"command": "pytest ...", "exit_code": 0}],
    "changed_files": ["path/to/file.py"],
    "duration_seconds": 0
  }
}
```

Field requirements:

- `format_version`: exact string `coding_agent_playground_sft_v1`.
- `example_id`: globally unique, stable, filesystem-safe.
- `repo`: one of `fastapi/fastapi`, `scikit-learn/scikit-learn`, `Textualize/rich`.
- `trajectory_id`: stable ID from rollout harness; if absent, derive from repo slug plus raw file stem.
- `task_id`: original seed/task ID from dev_1/dev_2.
- `source.raw_path`: absolute path to immutable raw trajectory artifact.
- `messages`: non-empty list in chat format with roles limited to `system`, `user`, `assistant`, `tool`.
- `metadata.status`: normalized to `success`, `partial`, `failed`, or `invalid`.

Optional top-level fields:

- `quality`: object with `keep`, `drop_reason`, `score`, `checks`.
- `artifacts`: object with `patch`, `diff_path`, `log_path`, `final_answer`.
- `labels`: list of string tags such as `tests_passed`, `no_code_change`, `timeout`, `recovered`.

## Normalization Rules

- Preserve conversational order.
- Convert all known role aliases to canonical roles:
  - `developer`, `system_prompt` -> `system` only when content is instruction-level.
  - `human`, `prompt`, `task` -> `user`.
  - `agent`, `model`, `assistant_message` -> `assistant`.
  - command/tool observations -> `tool`.
- Keep tool outputs only when they are materially needed for the assistant response. Drop repeated command boilerplate and massive logs unless they explain the final code decision.
- Normalize paths relative to repo root inside message content where possible; keep absolute raw artifact paths only in `source`/`artifacts`.
- Normalize timestamps to UTC ISO-8601.
- Normalize test records to `{command, exit_code, status, log_path}`.
- Deduplicate repeated identical messages caused by resume/retry loops.
- Strip ANSI escape sequences, terminal control codes, tmux status lines, and progress spinners.
- Redact secrets/tokens/keys using fixed placeholders such as `<REDACTED_TOKEN>`.
- Enforce UTF-8 text and reject invalid JSON.

## Cleaning and Keep/Drop Policy

Keep examples when:

- A user task prompt exists.
- At least one assistant response/action exists.
- The trajectory has enough context to understand the code task.
- The final state is `success` or useful `partial` with clear debugging value.

Drop examples when:

- The trajectory is empty, malformed, or cannot be parsed.
- It only contains environment setup with no coding-relevant action.
- It contains unresolved credential material after redaction.
- It is dominated by repeated failed retries with no recoverable reasoning/action.
- It exceeds trainer context budget and cannot be losslessly summarized around relevant turns.

Mark as `partial` instead of dropping when:

- Tests fail but the code/debugging sequence is coherent and useful.
- The run times out after meaningful progress.
- The final patch is incomplete but includes reusable diagnosis.

## Expected Raw Input Contract for dev_2

To avoid reverse engineering later, rollout artifacts should include one raw JSON file per trajectory plus append-only logs:

```json
{
  "trajectory_id": "fastapi__000001",
  "repo": "fastapi/fastapi",
  "repo_path": "/root/workspace/fastapi",
  "repo_commit": "git sha before rollout",
  "task_id": "fastapi__seed_000001",
  "prompt": "task prompt",
  "events": [
    {"type": "message", "role": "user", "content": "...", "timestamp": "..."},
    {"type": "message", "role": "assistant", "content": "...", "timestamp": "..."},
    {"type": "tool_call", "name": "exec_command", "arguments": {}, "timestamp": "..."},
    {"type": "tool_result", "content": "...", "exit_code": 0, "timestamp": "..."}
  ],
  "final": {
    "status": "success",
    "summary": "...",
    "changed_files": [],
    "tests": []
  }
}
```

Minimum needed from dev_2 if schema differs:

- raw artifact root path;
- one stable trajectory ID per rollout;
- repo, repo commit, task prompt, ordered message/tool events;
- final status and test commands/results.

## Validation Plan for test_1

Small-sample validation should check:

- JSONL is parseable line by line.
- Required fields exist and have correct types.
- `example_id` and `trajectory_id` uniqueness.
- `messages` is non-empty and roles are allowed.
- no obvious secrets via regex checks for API keys/tokens/private keys.
- no ANSI escape/control characters.
- every kept example has `source.raw_path`.
- `metadata.status` is one of the normalized enum values.
- per-repo counts and drop counts reconcile with raw input count.

## Active Blockers / Dependencies

- No active schema blocker for the corrected-machine tiny/smoke roots: observed raw artifacts can be normalized into `coding_agent_playground_sft_v1`.
- Full-scale conversion still depends on upcoming non-dry rollout roots being populated with the same per-run artifact contract.
- No pre-existing `coding_agent_playground` canonical data format file was found in local or PM worktrees. The contract above is therefore a proposed v1 target and should be treated as the current dev_3 working spec unless PM provides a different canonical format.

## Session 3 Update - Converter and Validator Criteria

PM Session 3 assignment acknowledged here only. Final workspace remains:

```text
ssh -p 31787 root@10.100.194.40
```

Current corrected-machine artifact scan:

```json
[
  {
    "root": "/root/workspace/rollouts_smoke_v3",
    "exists": true,
    "raw_count": 3,
    "status_counts": {"invalid": 3},
    "repo_counts": {
      "Textualize/rich": 1,
      "fastapi/fastapi": 1,
      "scikit-learn/scikit-learn": 1
    },
    "manifest_lines": 3,
    "schema_errors": []
  },
  {
    "root": "/root/workspace/rollouts_nondry_new_machine_tiny",
    "exists": true,
    "raw_count": 1,
    "status_counts": {"success": 1},
    "repo_counts": {"fastapi/fastapi": 1},
    "manifest_lines": 1,
    "schema_errors": []
  },
  {
    "root": "/root/workspace/rollouts",
    "exists": false
  }
]
```

Converter requirements from available artifacts:

- Input root is a rollout directory containing `manifest.jsonl` plus per-run directories at `<root>/<repo_slug>/<task_id>/`.
- Each per-run directory must include `raw_trajectory.json`, `metadata.json`, `done.json`, `last_message.md`, `stdout.jsonl`, and `stderr.log`.
- Primary conversion source is `raw_trajectory.json`.
- `metadata.json` and `done.json` are joined by `trajectory_id`/`task_id` to fill source paths, launcher status, duration, timestamps, dry-run flag, and completion status.
- Output is JSONL in `coding_agent_playground_sft_v1`, one full trajectory per line.
- `example_id` is `trajectory_id` unless a duplicate is detected; duplicates must be rejected rather than silently renamed.
- `messages` are derived from `raw_trajectory.events` where `type == "message"`, preserving order and role/content.
- Optional command/tool detail may be summarized from `stdout.jsonl`, but raw command output must not be copied wholesale into SFT records.
- Examples with `metadata.dry_run == true`, `done.status == "dry_run"`, or `raw_trajectory.final.status == "invalid"` are emitted only to a reject manifest, not to the train JSONL.
- Successful and useful partial trajectories are eligible for train JSONL when they satisfy schema and cleaning checks.

Schema validator requirements:

- Validate root-level `manifest.jsonl` exists and is parseable.
- Validate manifest line count equals discovered `raw_trajectory.json` count, unless an explicit allowlist documents missing/in-progress runs.
- Validate every manifest path points to existing `raw_trajectory`, `stdout`, `stderr`, `last_message`, and `run_dir`.
- Validate every `raw_trajectory.json` has string `trajectory_id`, `task_id`, `repo`, `repo_commit`, `repo_path`, and `prompt`.
- Validate `events` is a non-empty list and at least one user message plus one assistant message exist for keep candidates.
- Validate message roles are limited to `system`, `user`, `assistant`, and `tool` after normalization.
- Validate `final.status` normalizes to one of `success`, `partial`, `failed`, or `invalid`.
- Validate no duplicate `trajectory_id`, `task_id` within a repo, or `example_id` in the output.
- Validate generated JSONL is parseable line by line and required fields match `coding_agent_playground_sft_v1`.
- Validate reject manifest reconciles all dropped examples with explicit `drop_reason`.

Cleaning requirements:

- Strip ANSI escape sequences and terminal control characters.
- Redact likely secrets, API keys, bearer tokens, private-key blocks, and environment values matching token-like patterns.
- Normalize timestamps to UTC ISO-8601.
- Normalize repo labels to full IDs: `fastapi/fastapi`, `scikit-learn/scikit-learn`, `Textualize/rich`.
- Preserve relative code paths in content where readable; keep absolute machine paths only in `source` and artifact metadata.
- Drop empty placeholder assistant messages and repeated duplicate turns.
- Cap or summarize oversized tool/command observations before any inclusion as `tool` messages.

Exact acceptance criteria for `/root/workspace/rollouts`:

- Directory exists on `ssh -p 31787 root@10.100.194.40`.
- Contains a root `manifest.jsonl` with one line per completed rollout.
- Contains `manifest_summary.json` or equivalent summary with total and per-repo counts.
- Contains per-run artifacts under `<repo_slug>/<task_id>/` for all selected repos.
- Every completed rollout has `metadata.json`, `done.json`, `raw_trajectory.json`, `stdout.jsonl`, `stderr.log`, and `last_message.md`.
- Every `raw_trajectory.json` matches the observed compact schema or a documented compatible extension.
- Manifest records and per-run raw trajectories agree on `trajectory_id`, `task_id`, `repo_full_id`/`repo`, and artifact paths.
- Dry-run artifacts are either absent from `/root/workspace/rollouts` or explicitly marked and excluded from training.
- Converter can produce:
  - `train.jsonl` containing only kept examples;
  - `rejected.jsonl` or reject manifest with every dropped trajectory and reason;
  - `conversion_summary.json` with input count, kept count, dropped count, per-repo counts, and status counts.
- Validator passes with zero parse errors, zero duplicate IDs, zero missing required fields, and zero unredacted secret-pattern hits.
- Counts reconcile: `input_count == kept_count + dropped_count`.
- At least one non-dry successful trajectory is present before this root is used as an end-to-end SFT smoke input; full milestone scale should target the PM/dev_2 assigned rollout count, not block converter work on all 300 being present.

Current blockers:

- `/root/workspace/rollouts` does not exist yet on the corrected final workspace, so exact acceptance can only be specified, not validated against final-scale root.
- Current non-dry tiny root has only one successful FastAPI trajectory. It is sufficient for converter smoke validation, but not sufficient for balanced multi-repo training data validation.

## Session 5 Conversion - `rollouts_m1_10`

PM Session 5 assignment acknowledged here only. I did not interrupt `/root/workspace/rollouts_m1_10` and did not send routine peer status to PM.

Current input root on final workspace:

```text
ssh -p 31787 root@10.100.194.40
/root/workspace/rollouts_m1_10
```

Current artifact scan before conversion:

```json
{
  "input_root": "/root/workspace/rollouts_m1_10",
  "raw_count": 10,
  "status_counts": {"success": 10},
  "repo_counts": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "manifest_total": 10,
  "manifest_status_counts": {"passed": 10},
  "schema_errors": []
}
```

Converter command used:

```bash
python3 /root/workspace/rollout_harness/convert_rollouts_to_sft.py \
  --input-root /root/workspace/rollouts_m1_10 \
  --output-dir /root/workspace/cleaned_m1_sft_m1_10_session5
```

Final `coding_agent_playground_sft_v1` paths:

```text
/root/workspace/cleaned_m1_sft_m1_10_session5/train.jsonl
/root/workspace/cleaned_m1_sft_m1_10_session5/rejected.jsonl
/root/workspace/cleaned_m1_sft_m1_10_session5/conversion_summary.json
```

Conversion summary:

```json
{
  "format_version": "coding_agent_playground_sft_v1",
  "input_count": 10,
  "kept_count": 10,
  "dropped_count": 0,
  "error_count": 0,
  "per_repo_kept": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {"success": 10},
  "train_path": "/root/workspace/cleaned_m1_sft_m1_10_session5/train.jsonl",
  "rejected_path": "/root/workspace/cleaned_m1_sft_m1_10_session5/rejected.jsonl"
}
```

Post-conversion JSONL validation:

```json
{
  "train_lines": 10,
  "rejected_lines": 0,
  "unique_ids": 10,
  "schema_errors": [],
  "per_repo": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {"success": 10}
}
```

Session 5 blocker / caution:

- `/root/workspace/rollouts_m1_10/complete_process_validation.json` currently records `checked_count=9`, `valid_count=9`, `invalid_count=0`, while the rollout manifest and raw artifacts now contain 10 successful trajectories. The missing validation entry is `fastapi__fastapi_complete_edit_004`. Converter output includes all 10 successful trajectories because `manifest_summary.json` and `raw_trajectory.json` show 10 passed/success records; the complete-process validation file should be regenerated or updated before treating all 10 as quality-gated final SFT input.

## Session 5 Post-Interrupt Final Cleaning Evidence

PM post-interrupt assignment acknowledged here only. I own the cleaning/conversion evidence for the final 10 complete-process trajectories.

Final cleaned `coding_agent_playground_sft_v1` paths on the final workspace:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
/root/workspace/cleaned_m1_sft_10/rejected.jsonl
/root/workspace/cleaned_m1_sft_10/conversion_summary.json
```

Source and quality-gate paths:

```text
/root/workspace/rollouts_m1_10
/root/workspace/rollouts_m1_10/complete_process_validation.json
```

Quality-gate status:

```json
{
  "checked_count": 10,
  "valid_count": 10,
  "invalid_count": 0
}
```

Final conversion summary:

```json
{
  "format_version": "coding_agent_playground_sft_v1",
  "input_count": 10,
  "kept_count": 10,
  "dropped_count": 0,
  "error_count": 0,
  "per_repo_kept": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {"success": 10},
  "train_path": "/root/workspace/cleaned_m1_sft_10/train.jsonl",
  "rejected_path": "/root/workspace/cleaned_m1_sft_10/rejected.jsonl"
}
```

Post-conversion validation:

```json
{
  "train_lines": 10,
  "rejected_lines": 0,
  "unique_ids": 10,
  "schema_errors": [],
  "per_repo": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {"success": 10}
}
```

Rejects:

- `rejected.jsonl` exists and has 0 non-empty lines.
- `conversion_summary.json` has `dropped_count=0`, `error_count=0`, and empty drop/error collections.

Current data-pipeline status:

- Final 10-trajectory cleaned SFT smoke dataset is ready at `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- The earlier Session 5 caution about `complete_process_validation.json` covering only 9 trajectories is resolved: the quality-gate file now records 10 checked, 10 valid, 0 invalid.

## PM Session 3 Continuation - Converter Implemented

PM added the standard-library converter:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/rollout_harness/convert_rollouts_to_sft.py
```

Remote deployment:

```text
/root/workspace/rollout_harness/convert_rollouts_to_sft.py
sha256 e126a1cff0914ec997c0539fb9978262bea1c1a226598dc62af17c5d5f62469b
```

Converter behavior:

- Reads a rollout root with `manifest.jsonl` or discovers `*/*/raw_trajectory.json`.
- Joins `raw_trajectory.json`, `done.json`, and `metadata.json`.
- Writes `train.jsonl`, `rejected.jsonl`, and `conversion_summary.json`.
- Keeps only non-dry `success` or useful `partial` examples.
- Drops dry-run/invalid/malformed examples with explicit `drop_reason`.
- Normalizes message roles, strips ANSI/control characters, redacts common token/private-key patterns, and rejects duplicate `example_id` values.

Smoke run against the live full-rollout root:

```text
input_root /root/workspace/rollouts_m1_300
output_dir /root/workspace/cleaned_m1_sft_smoke
input_count 3
kept_count 3
dropped_count 0
error_count 0
per_repo_kept fastapi/fastapi=3
status_counts success=3
train_path /root/workspace/cleaned_m1_sft_smoke/train.jsonl
```

Validation:

```text
validated_train_lines 3
unique_ids 3
```

This proves the cleaning path works on real non-dry Codex artifacts. It is not final training data yet because the rollout is still in progress and currently only has FastAPI examples in the converted smoke.

## PM Session 3 Continuation - Live Multi-Repo Conversion

After parallel scikit-learn and rich rollout roots began producing artifacts, PM converted all currently available non-dry roots and built a combined live SFT smoke dataset:

```text
/root/workspace/cleaned_m1_sft_main/train.jsonl
/root/workspace/cleaned_m1_sft_scikit/train.jsonl
/root/workspace/cleaned_m1_sft_rich/train.jsonl
/root/workspace/cleaned_m1_sft_live/train.jsonl
/root/workspace/cleaned_m1_sft_live/combined_summary.json
```

Combined summary:

```json
{
  "format_version": "coding_agent_playground_sft_v1",
  "kept_count": 7,
  "per_repo_kept": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 2,
    "Textualize/rich": 1
  },
  "status_counts": {"success": 7},
  "train_path": "/root/workspace/cleaned_m1_sft_live/train.jsonl"
}
```

Validation:

```text
validated_train_lines 7
unique_ids 7
per_repo fastapi/fastapi=4 scikit-learn/scikit-learn=2 Textualize/rich=1
```

This is still a smoke dataset, not final SFT input, because full 100-per-repo rollout is still running.

## Session 4 Scope Change - Quality Gate Before Cleaning

Supervisor changed the active rollout target to 10 total complete coding-process trajectories. The old 300 rollout roots are scratch-only and must not be used as final SFT input.

Active final input/output:

```text
/root/workspace/rollout_harness/tasks_m1_10.jsonl
/root/workspace/rollouts_m1_10
```

Before conversion to final SFT smoke data, each trajectory must pass:

```bash
python3 /root/workspace/rollout_harness/validate_complete_coding_trajectories.py \
  --input-root /root/workspace/rollouts_m1_10 \
  --output /root/workspace/rollouts_m1_10/complete_process_validation.json
```

Required complete-process evidence per accepted trajectory:

- requirements understanding;
- repo/file localization;
- code inspection;
- actual code edit or patch attempt;
- test/check attempt;
- observed result/error;
- final changed files/tests/blockers.

Only trajectories that pass this quality gate should be converted into the final `coding_agent_playground_sft_v1` smoke dataset for SFT.

## Session 5 Final 10-Trajectory Conversion

Final accepted rollout root:

```text
/root/workspace/rollouts_m1_10
```

Complete-process validation:

```text
checked_count 10
valid_count 10
invalid_count 0
```

Final cleaned SFT smoke dataset:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
/root/workspace/cleaned_m1_sft_10/rejected.jsonl
/root/workspace/cleaned_m1_sft_10/conversion_summary.json
```

Conversion summary:

```json
{
  "input_count": 10,
  "kept_count": 10,
  "dropped_count": 0,
  "error_count": 0,
  "per_repo_kept": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {"success": 10}
}
```

This is the current final SFT smoke input for Milestone 1 Session 5.

## Session 6 Re-Verification After Supervisor Correction

PM Session 6 assignment acknowledged here only. PM will assign/gate/collect/decide; dev_3 owns conversion/data-pipeline evidence for Milestone 1.

Corrected host:

```text
ssh -p 31787 root@10.100.194.40
```

Verified files:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
/root/workspace/cleaned_m1_sft_10/conversion_summary.json
/root/workspace/cleaned_m1_sft_10/rejected.jsonl
/root/workspace/rollouts_m1_10/complete_process_validation.json
```

Verification result:

```json
{
  "format_ok": true,
  "train_lines": 10,
  "unique_example_ids": 10,
  "unique_trajectory_ids": 10,
  "repo_split": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {"success": 10},
  "role_counts": {
    "user": 10,
    "assistant": 10
  },
  "message_count_min": 2,
  "message_count_max": 2,
  "rejected_lines": 0,
  "schema_errors": [],
  "cleaning_defects": []
}
```

`conversion_summary.json` agrees with the train/reject files:

```json
{
  "format_version": "coding_agent_playground_sft_v1",
  "input_count": 10,
  "kept_count": 10,
  "dropped_count": 0,
  "error_count": 0,
  "per_repo_kept": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {"success": 10},
  "train_path": "/root/workspace/cleaned_m1_sft_10/train.jsonl",
  "rejected_path": "/root/workspace/cleaned_m1_sft_10/rejected.jsonl"
}
```

Complete-process quality gate remains satisfied:

```json
{
  "checked_count": 10,
  "valid_count": 10,
  "invalid_count": 0
}
```

Cleaning defect check:

- No JSONL parse errors.
- No duplicate `example_id` or `trajectory_id`.
- No missing required `coding_agent_playground_sft_v1` top-level fields.
- All repos are in the expected set: `fastapi/fastapi`, `scikit-learn/scikit-learn`, `Textualize/rich`.
- Every kept example has at least one user message and one assistant message.
- No ANSI escape sequences or terminal control characters found in message content.
- No obvious unredacted API-key/token/bearer/private-key patterns found in message content.
- Every `source.raw_path` exists on the corrected host.

Current data-pipeline decision:

- `/root/workspace/cleaned_m1_sft_10/train.jsonl` is confirmed as valid `coding_agent_playground_sft_v1` 10-trajectory smoke SFT input.
- There are no current cleaning defects to route.
