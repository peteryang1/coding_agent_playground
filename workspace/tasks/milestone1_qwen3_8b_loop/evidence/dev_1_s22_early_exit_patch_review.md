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

Status: `BLOCKER_MANIFEST_ENV_CAPTURE`

The PR #39 wrapper patch is directionally correct and addresses most of the Session 22 early-exit diagnostics gap:

- PASS: stdout/stderr logging is moved near the top of `scripts/train_qwen3_8b_sft.sh` through `LOG_FILE=${RUN_DIR}/logs/train_stdout_stderr.log` and `exec > >(tee -a "${LOG_FILE}") 2>&1`.
- PASS: xtrace is captured in `${RUN_DIR}/logs/train_xtrace.log` through `BASH_XTRACEFD=9` and `set -x` when `SFT_XTRACE` is enabled.
- PASS: ERR/EXIT diagnostics are added through `trap on_err ERR`, `trap on_exit EXIT`, `${RUN_DIR}/early_exit_diagnostics.txt`, and `${RUN_DIR}/exit_status.txt`.
- PASS: preflight evidence is generated before fragile launch work at `${RUN_DIR}/preflight.json`, including config/data existence, checksums, output paths, log path, and xtrace path.
- PASS: runtime config generation happens before launch and rewrites `model_name_or_path`, `output_dir`, and top-level `dataset` when `DATASET_NAME` is set.
- PASS: the checked config contains `dataset: coding_agent_m1_sft_10_sharegpt`.
- PASS: the checked config and wrapper default outputs preserve `/home/xu.yang/coding_agent_playground/outputs` for logs, run metadata, tmp, and checkpoint/output roots.
- PASS: `scripts/write_sft_run_manifest.py` now reads the generated runtime config and records actual checkpoint policy fields including `save_steps`, `save_total_limit`, `save_only_model`, `save_hf_model`, and `output_dir`.

## Blocking Issue

PR #39 does not currently guarantee that the run manifest records the resolved dataset/output preflight variables.

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

Because `DATASET_NAME`, `OUTPUT_ROOT`, `RUN_DIR`, and `CHECKPOINT_DIR` are shell variables but are not exported or passed as manifest arguments before `python3 scripts/write_sft_run_manifest.py`, child process environment reads can be unset. This means the manifest can fail the acceptance requirement to durably record `DATASET_NAME=coding_agent_m1_sft_10_sharegpt` and the resolved `/home/xu.yang` output root, even though the runtime config rewrite itself is correct.

Required fix before `PASS_FOR_PM_RETRY`:

- Export the resolved manifest preflight variables before invoking `write_sft_run_manifest.py`, for example `export DATASET_NAME OUTPUT_ROOT RUN_DIR CHECKPOINT_DIR TMPDIR LOG_FILE XTRACE_FILE DIAG_FILE`, or pass them explicitly as manifest CLI arguments and stop relying on unexported shell variables.
- Re-check that the generated manifest will record `dataset_name: coding_agent_m1_sft_10_sharegpt` and `/home/xu.yang/coding_agent_playground/outputs` paths.

## PR Scope Review

PR #39 diff includes the required wrapper/config/manifest patch plus broader historical durable evidence files:

- Required functional files:
  - `configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml`
  - `scripts/train_qwen3_8b_sft.sh`
  - `scripts/write_sft_run_manifest.py`
- Broader durable/history files include dev_4 status/evidence, older SFT retry evidence, test evidence updates, history, task knowledge, and task registry updates.

dev_1 scope judgment: the broader historical evidence diff is acceptable as a PM scope note, not the launch blocker I am raising. It is not ideal for a focused patch PR, but it is limited to milestone durable evidence/history/status files plus the required functional patch. I do not see unrelated application/runtime code outside the required wrapper/config/manifest files. PM may still require scope cleanup as a process decision, but my technical blocker is the manifest environment capture gap above.

## Result

`BLOCKER_MANIFEST_ENV_CAPTURE`

No `PASS_FOR_PM_RETRY` from dev_1 yet. PR #39 should not be used to authorize the next retry until the manifest preflight variable capture is fixed or PM explicitly waives manifest recording of `DATASET_NAME` and resolved `/home/xu.yang` output root.
