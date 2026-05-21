# Test 1 Session 22 Early-Exit Patch Gate

Date: 2026-05-21

Task ID: `M1-S22-EARLY-EXIT-PATCH-GATE-TEST1`

Owner: `intern_code_test_1`

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_early_exit_patch_gate.md`

Scope: no-execution test gate for PR #39 early-exit wrapper/logging patch before any owner self-merge or future retry authorization.

Execution boundary:

```text
No SFT command was run by test_1.
No GPU command was run by test_1.
No eval command was run by test_1.
No dry-run launch command was run by test_1.
No peer_send PM routine status was used.
```

## Sources Reviewed

- PR #39: `https://github.com/peteryang1/coding_agent_playground/pull/39`
- GitHub PR metadata via `gh pr view 39 --repo peteryang1/coding_agent_playground --json ...`
- PR branch fetched as `origin/pr/39`
- `scripts/train_qwen3_8b_sft.sh` from PR #39
- `scripts/write_sft_run_manifest.py` from PR #39
- `configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml` from PR #39
- `evidence/dev_4_s22_early_exit_fix.md`
- `evidence/test_1_s22_postrun_gate.md`
- `task_registry.md`

## PR Metadata

```text
PR: https://github.com/peteryang1/coding_agent_playground/pull/39
title: M1-S22-EARLY-EXIT-FIX-DEV4 wrapper diagnostics
state: OPEN
draft: false
base: main
head: intern_code_dev_4/M1-S22-EARLY-EXIT-FIX-DEV4
mergeable: MERGEABLE
merge_state_status: CLEAN
required_checks: none reported in reviewed metadata
```

PR body includes:

- task id `M1-S22-EARLY-EXIT-FIX-DEV4`;
- owner `intern_code_dev_4`;
- acceptance criteria;
- evidence paths;
- completion marker;
- no-execution boundary.

## Gate Result

Result: **PASS_FOR_PM_PATCH_GATE**

Technical patch result: **PASS_FOR_EARLY_EXIT_LOGGING_PATCH**

PR merge gate result: **PASS_WITH_ARCHIVAL_SCOPE_JUSTIFICATION**

Interpretation: the code/config patch in PR #39 satisfies the test_1 no-execution technical gate for early-exit diagnostics. The earlier scope blocker is resolved for test_1 because current dev_4 evidence at PR head `f81c7da217bcad90b68cd2ce327ac637bb4134d5` records an explicit archival justification for the broader historical evidence diff. Those historical files must be treated as archival/provenance only, not as current retry inputs; the current retry gate remains governed by the S22 `/home/xu.yang` post-patch criteria.

## Technical Patch Checks

### Durable stdout/stderr and xtrace

PASS.

`scripts/train_qwen3_8b_sft.sh` now:

- defaults `OUTPUT_ROOT` to `/home/xu.yang/coding_agent_playground/outputs`;
- creates `${RUN_DIR}/logs`, `${RUN_DIR}/config`, `${CHECKPOINT_DIR}`, and `${TMPDIR}`;
- redirects stdout/stderr through `tee -a "${RUN_DIR}/logs/train_stdout_stderr.log"`;
- opens xtrace file `${RUN_DIR}/logs/train_xtrace.log`;
- exports `BASH_XTRACEFD=9`;
- enables `set -x` when `SFT_XTRACE` is enabled.

Required output paths covered:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_xtrace.log
```

Gate note: a small shell prelude still runs before durable logging (`REPO_ROOT`, `RUN_ID`, path variable setup, and `mkdir -p`). This is acceptable for this gate because the patch moves durable capture to the first safe point where `RUN_DIR` is known and directories can exist. Future runtime evidence must show this path is not bypassed.

### ERR/EXIT diagnostics

PASS.

The patch adds:

- `write_status`;
- `write_diagnostics`;
- `on_err` trap;
- `on_exit` trap;
- artifact summary in diagnostics;
- exit status write for both ERR and non-ERR exits.

Required diagnostic paths covered:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/early_exit_diagnostics.txt
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/exit_status.txt
```

Expected future post-run evidence if early failure recurs:

- `ERROR_EXIT`;
- `ERROR_LINE`;
- `ERROR_COMMAND`;
- `RUN_ID`, `RUN_DIR`, `CHECKPOINT_DIR`, `OUTPUT_ROOT`, `TMPDIR`;
- artifact summary;
- durable `EXIT_STATUS=<nonzero>`.

### Preflight/config/manifest artifacts

PASS.

The patch writes:

- `preflight.json` before config rewrite/training;
- runtime config at `${RUN_DIR}/config/qwen3_8b_sft.yaml`;
- `run_manifest.json` before training launch.

`scripts/write_sft_run_manifest.py` now records:

- actual `save_steps`;
- actual `save_total_limit`;
- actual `save_only_model`;
- actual `save_hf_model`;
- actual `output_dir`;
- preflight fields for config/dataset existence, output root, run dir, checkpoint dir, tmpdir, `DATASET_NAME`, log path, xtrace path, and early-exit diagnostics path.

Required future pre-run artifact paths:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/preflight.json
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/run_manifest.json
```

### `/home/xu.yang` output rule

PASS.

The patch defaults:

```text
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
TMPDIR=/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>
CHECKPOINT_DIR=/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
```

The config template output path is also under `/home/xu.yang/coding_agent_playground/outputs`.

Non-`/home/xu.yang` paths remain accepted only as existing-required input/audit exceptions, for example:

- base model under `/mnt/3fs/data/ai4ai/models/...`;
- dependency archives/wheels under `/mnt/3fs`;
- existing source dataset path `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.

### ShareGPT dataset preservation

PASS.

The patch preserves:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset: coding_agent_m1_sft_10_sharegpt
ShareGPT messages/from/value contract inherited from prior dataset_info package
```

The wrapper rewrites top-level `dataset:` in the runtime config when `DATASET_NAME` is set, which addresses the prior dataset-name drift risk.

### Trainer handoff and trap preservation

PASS.

The patch no longer invokes `llamafactory-cli` via `exec`; it runs:

```text
llamafactory-cli train "${RUNTIME_CONFIG}"
```

This keeps traps active so trainer failures can still produce diagnostics and `exit_status.txt`.

## PR Scope / Historical Evidence Diff

Resolved for test_1 by current archival justification.

Reviewed PR file list includes the expected patch files:

```text
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_early_exit_fix.md
workspace/interns/intern_code_dev_4/status.md
workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
```

But PR #39 also includes older historical/session files not required for `M1-S22-EARLY-EXIT-FIX-DEV4`:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_sft_retry_pregate.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s21_enospc_config_fix.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s21_pr30_cleanup.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_retry_run.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_sft_retry_validation.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_eval_unblock.md
```

Scope risk reviewed:

- these files are historical evidence from older sessions and are not necessary to patch early-exit logging;
- some contain older `/mnt/3fs` output-path plans or older data paths from pre-S21/S22 flows, which can confuse the current `/home/xu.yang` gate if merged as fresh evidence;
- the PR touches other owner/test evidence files (`dev_1`, `test_1`, `test_2`) without this task owning those areas;
- the extra evidence changes increase merge/review surface without improving the wrapper patch.

Scope gate decision after PR head `f81c7da217bcad90b68cd2ce327ac637bb4134d5`:

```text
PASS_WITH_ARCHIVAL_SCOPE_JUSTIFICATION.
dev_4 evidence now states that the broader historical/status/task_knowledge records preserve PM-required provenance and conflict-resolution history for the same PR path.
The implementation scope remains the wrapper/config/manifest patch.
Older historical evidence files are archival only and must not override current S22 /home/xu.yang post-patch criteria.
```

Specific re-checks:

- PR head is `f81c7da217bcad90b68cd2ce327ac637bb4134d5`.
- GitHub metadata still reports PR #39 open, non-draft, `MERGEABLE` / `CLEAN`.
- `dev_1_sft_retry_pregate.md`, `test_1_sft_retry_validation.md`, and `test_2_eval_unblock.md` diffs are whitespace/trailing-newline only.
- The large dev_4 historical evidence additions are archival/provenance records from prior dev_4 tasks and current PR #39 conflict-resolution history.
- No runtime checkpoint artifact, GPU result, eval result, or new SFT execution evidence is added by PR #39.

## Manifest Environment Capture Re-Gate

PASS.

PR head `f81c7da217bcad90b68cd2ce327ac637bb4134d5` resolves the prior manifest env capture concern:

- `scripts/train_qwen3_8b_sft.sh` exports `DATASET_NAME`, `OUTPUT_ROOT`, `RUN_DIR`, `CHECKPOINT_DIR`, `TMPDIR`, `LOG_FILE`, `XTRACE_FILE`, and `DIAG_FILE`.
- The wrapper passes those values explicitly to `scripts/write_sft_run_manifest.py` with:
  - `--dataset-name`;
  - `--output-root`;
  - `--tmpdir`;
  - `--log-file`;
  - `--xtrace-file`;
  - `--diag-file`.
- `scripts/write_sft_run_manifest.py` accepts those arguments and records them in the manifest `preflight` object.
- Expected future manifest includes `dataset_name: coding_agent_m1_sft_10_sharegpt`, `/home/xu.yang/coding_agent_playground/outputs` output root, run dir, checkpoint dir, tmpdir, log path, xtrace path, and early-exit diagnostics path even if subprocess environment handling changes.

## Post-Run Artifact Criteria After Patch

Any future PM-authorized retry after this patch must produce enough evidence to distinguish wrapper/preflight failures from training/checkpoint failures.

Minimum required artifacts before training launch:

```text
logs/train_stdout_stderr.log
logs/train_xtrace.log
preflight.json
config/qwen3_8b_sft.yaml
run_manifest.json
exit_status.txt
early_exit_diagnostics.txt if nonzero before or during trainer handoff
```

Post-run PASS requires:

- exit status `0`, or PM-preapproved accepted replacement outcome;
- useful stdout/stderr boundary, not only `START_UTC`;
- xtrace present and nonempty;
- preflight JSON present;
- generated runtime config present and includes `dataset: coding_agent_m1_sft_10_sharegpt`, `save_steps: 2`, `save_total_limit: 1`, `max_steps: 2`, `warmup_steps: 0`, and `/home/xu.yang` output;
- run manifest present and checkpoint policy reflects runtime config, not stale static defaults;
- old failures absent:
  - `KeyError: 'from'`;
  - missing `dataset_info`;
  - `ZeroDivisionError` / `steps_in_epoch`;
  - scheduler warmup assertion;
  - `No space left on device`;
  - safetensors ENOSPC;
- complete checkpoint/model present and accepted, or preapproved replacement;
- `trainer_state.json` present unless PM preapproves replacement;
- `all_results.json` present unless PM preapproves replacement;
- stop proof present with LTP stopped/released and endpoint unavailable/refused.

## Completion Marker

```text
task_id: M1-S22-EARLY-EXIT-PATCH-GATE-TEST1
pr: https://github.com/peteryang1/coding_agent_playground/pull/39
pr_head: f81c7da217bcad90b68cd2ce327ac637bb4134d5
github_state: OPEN_NON_DRAFT_MERGEABLE_CLEAN
technical_patch_gate: PASS_FOR_EARLY_EXIT_LOGGING_PATCH
manifest_env_capture_gate: PASS
scope_gate: PASS_WITH_ARCHIVAL_SCOPE_JUSTIFICATION
next_pre_run_gate: PASS_FOR_PM_PATCH_GATE
home_xu_yang_required: true
sharegpt_dataset_preserved: true
post_run_artifact_criteria_defined: true
sft_gpu_eval_executed_by_test1: false
```
