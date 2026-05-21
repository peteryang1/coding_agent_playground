# M1-S22-EARLY-EXIT-PATCH-REVIEW-DEV1

Owner: `intern_code_dev_1`
Task: `M1-S22-EARLY-EXIT-PATCH-REVIEW-DEV1`
Evidence date: 2026-05-21
Execution boundary: no remote experiments, SFT, GPU, or eval run by dev_1.

## Reviewed Inputs

- PR #39: `https://github.com/peteryang1/coding_agent_playground/pull/39`
- GitHub metadata checked with `gh pr view 39 --repo peteryang1/coding_agent_playground --json ...`
  - State: open
  - Draft: false
  - Mergeable: `MERGEABLE`
  - Merge state: `CLEAN`
  - Head: `intern_code_dev_4/M1-S22-EARLY-EXIT-FIX-DEV4`
  - Base: `main`
- Local review branch: `origin/pr-39`, fetched from `pull/39/head`
- Functional files reviewed:
  - `scripts/train_qwen3_8b_sft.sh`
  - `scripts/write_sft_run_manifest.py`
  - `configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml`
- Static no-execution checks run locally:
  - `git show origin/pr-39:scripts/train_qwen3_8b_sft.sh | bash -n`
  - Python `compile()` against `origin/pr-39:scripts/write_sft_run_manifest.py`
  - Result: syntax checks pass.

## Acceptance Review

Status: `PASS_FOR_PM_RETRY`

The PR #39 wrapper patch is directionally correct and addresses most of the Session 22 early-exit diagnostics gap:

- PASS: stdout/stderr logging is moved near the top of `scripts/train_qwen3_8b_sft.sh` through `LOG_FILE=${RUN_DIR}/logs/train_stdout_stderr.log` and `exec > >(tee -a "${LOG_FILE}") 2>&1`.
- PASS: xtrace is captured in `${RUN_DIR}/logs/train_xtrace.log` through `BASH_XTRACEFD=9` and `set -x` when `SFT_XTRACE` is enabled.
- PASS: ERR/EXIT diagnostics are added through `trap on_err ERR`, `trap on_exit EXIT`, `${RUN_DIR}/early_exit_diagnostics.txt`, and `${RUN_DIR}/exit_status.txt`.
- PASS: preflight evidence is generated before fragile launch work at `${RUN_DIR}/preflight.json`, including config/data existence, checksums, output paths, log path, and xtrace path.
- PASS: runtime config generation happens before launch and rewrites `model_name_or_path`, `output_dir`, and top-level `dataset` when `DATASET_NAME` is set.
- PASS: the checked config contains `dataset: coding_agent_m1_sft_10_sharegpt`.
- PASS: the checked config and wrapper default outputs preserve `/home/xu.yang/coding_agent_playground/outputs` for logs, run metadata, tmp, and checkpoint/output roots.
- PASS: `scripts/write_sft_run_manifest.py` now reads the generated runtime config and records actual checkpoint policy fields including `save_steps`, `save_total_limit`, `save_only_model`, `save_hf_model`, and `output_dir`.

## Prior Blocking Issue

Prior dev_1 finding: PR #39 did not guarantee that the run manifest records the resolved dataset/output preflight variables.

Observed wrapper lines from `origin/pr-39:scripts/train_qwen3_8b_sft.sh`:

- `DATASET_NAME="${DATASET_NAME:-}"`
- `OUTPUT_ROOT="${OUTPUT_ROOT:-/home/xu.yang/coding_agent_playground/outputs}"`
- `RUN_DIR="${RUN_DIR:-${OUTPUT_ROOT}/runs/train/${RUN_ID}}"`
- `CHECKPOINT_DIR="${CHECKPOINT_DIR:-${OUTPUT_ROOT}/training_summary/sft_output/${RUN_ID}}"`
- `TMPDIR="${TMPDIR:-${OUTPUT_ROOT}/tmp/${RUN_ID}}"`
- only `TMPDIR` and later launcher-specific variables are exported before manifest generation.

Observed manifest code from `origin/pr-39:scripts/write_sft_run_manifest.py`:

- `preflight.output_root = os.environ.get("OUTPUT_ROOT")`
- `preflight.tmpdir = os.environ.get("TMPDIR")`
- `preflight.dataset_name = os.environ.get("DATASET_NAME")`

At the previous PR head, `DATASET_NAME`, `OUTPUT_ROOT`, `RUN_DIR`, and `CHECKPOINT_DIR` were shell variables but were not exported or passed as manifest arguments before `python3 scripts/write_sft_run_manifest.py`, so child process environment reads could be unset.

Required fix before `PASS_FOR_PM_RETRY` was:

- Export the resolved manifest preflight variables before invoking `write_sft_run_manifest.py`, for example `export DATASET_NAME OUTPUT_ROOT RUN_DIR CHECKPOINT_DIR TMPDIR LOG_FILE XTRACE_FILE DIAG_FILE`, or pass them explicitly as manifest CLI arguments and stop relying on unexported shell variables.
- Re-check that the generated manifest will record `dataset_name: coding_agent_m1_sft_10_sharegpt` and `/home/xu.yang/coding_agent_playground/outputs` paths.

## Re-gate Review: PR #39 `f81c7da`

PM requested re-gate after dev_4 updated PR #39 to commit `f81c7da217bcad90b68cd2ce327ac637bb4134d5` (`Address PR39 manifest gate blockers`).

Current PR metadata:

- URL: `https://github.com/peteryang1/coding_agent_playground/pull/39`
- State: open
- Draft: false
- Mergeable: `MERGEABLE`
- Merge state: `CLEAN`
- Head commit reviewed: `f81c7da217bcad90b68cd2ce327ac637bb4134d5`

Static no-execution checks re-run locally:

- `git show origin/pr-39:scripts/train_qwen3_8b_sft.sh | bash -n`
- Python `compile()` against `origin/pr-39:scripts/write_sft_run_manifest.py`
- Result: syntax checks pass.

The prior `BLOCKER_MANIFEST_ENV_CAPTURE` is resolved:

- PASS: `scripts/train_qwen3_8b_sft.sh` now exports the resolved variables before manifest generation:
  - `DATASET_NAME`
  - `OUTPUT_ROOT`
  - `RUN_DIR`
  - `CHECKPOINT_DIR`
  - `TMPDIR`
  - `LOG_FILE`
  - `XTRACE_FILE`
  - `DIAG_FILE`
- PASS: the wrapper also passes those resolved values explicitly to `scripts/write_sft_run_manifest.py`:
  - `--dataset-name "${DATASET_NAME}"`
  - `--output-root "${OUTPUT_ROOT}"`
  - `--tmpdir "${TMPDIR}"`
  - `--log-file "${LOG_FILE}"`
  - `--xtrace-file "${XTRACE_FILE}"`
  - `--diag-file "${DIAG_FILE}"`
- PASS: `scripts/write_sft_run_manifest.py` now accepts those CLI arguments and records them in `manifest["preflight"]`, using CLI values before environment fallback.
- PASS: future manifest preflight should record `dataset_name: coding_agent_m1_sft_10_sharegpt` when launched with the PM-approved `DATASET_NAME`, and should record `/home/xu.yang/coding_agent_playground/outputs`-derived `output_root`, `run_dir`, `checkpoint_dir`, `tmpdir`, log, xtrace, and diagnostics paths.
- PASS: checked config still contains `dataset: coding_agent_m1_sft_10_sharegpt` and `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/...`.

## Archival Scope Re-check

dev_4 added an explicit archival justification in `evidence/dev_4_s22_early_exit_fix.md`:

- PR #39 keeps durable history/status/task knowledge evidence records required by PM process and conflict-resolution gates for this same task.
- Splitting them out now would require a second task/PR or remove provenance showing how PR #39 became mergeable after resolving conflicts against current main.
- dev_4 states implementation scope remains limited to `scripts/train_qwen3_8b_sft.sh`, `scripts/write_sft_run_manifest.py`, the config file, and directly required task/status/history/knowledge/evidence records for `M1-S22-EARLY-EXIT-FIX-DEV4`.
- dev_4 states no unrelated runtime evidence, checkpoint artifact, GPU result, or eval result is added by PR #39.

dev_1 scope judgment after re-check: archival justification is acceptable and is not a dev_1 blocker. The PR remains broader than an ideal focused functional patch, but the broader files are durable milestone records/history/status. I do not see unrelated runtime application code outside the required wrapper/config/manifest files.

## PR Scope Review

PR #39 diff includes the required wrapper/config/manifest patch plus broader historical durable evidence files:

- Required functional files:
  - `configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml`
  - `scripts/train_qwen3_8b_sft.sh`
  - `scripts/write_sft_run_manifest.py`
- Broader durable/history files include dev_4 status/evidence, older SFT retry evidence, test evidence updates, history, task knowledge, and task registry updates.

dev_1 scope judgment: the broader historical evidence diff is acceptable as a PM scope note, not the launch blocker I am raising. It is not ideal for a focused patch PR, but it is limited to milestone durable evidence/history/status files plus the required functional patch. I do not see unrelated application/runtime code outside the required wrapper/config/manifest files. PM may still require scope cleanup as a process decision, but my technical blocker is the manifest environment capture gap above.

## Result

`PASS_FOR_PM_RETRY`

dev_1 finds no remaining blocker in the current PR #39 head for the reviewed acceptance criteria. The prior manifest preflight capture blocker is fixed at commit `f81c7da`, and the broader historical evidence diff is acceptable as an archival scope note rather than a dev_1 blocker. PM/test/resource gates and explicit PM retry authorization are still separate from this dev_1 no-execution review.
