# Test 2 S23 PR59 Mini-SWE Eval Ready Reblock

Task ID: `M1-S23-PR59-EVAL-READY-REBLOCK-TEST2`

Owner: `intern_code_test_2`

Updated: 2026-05-21T16:59:51Z

Scope: keep mini-swe eval blocked but ready for the first PM-gated checkpoint/model or served endpoint after PR59. No eval, GPU, SFT, dry-run, remote transfer, or remote command was run by test_2.

## Source Evidence Read

- `evidence/dev_2_s23_pr59_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr59_preflight_sft_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

Upstream runtime task: `M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2`, owner `intern_code_dev_2`.

## Current State

PR59 runtime produced no eval-usable model target.

```text
PR #59 merge commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
source bundle sha256: 2f272f210b67ed45b4a7b05592881c8c036fb34de2660645d6f96af76adf4d85
mcore_adapter bundle sha256: ec0ace00eeca1f4d60710deea59621c868860e34827a5b645122f64f043170e7
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
transfer/import/preflight: PASS
SFT_ALLOWED: true
conditional SFT: ran exactly once
SFT exit status: 127
final blocker: BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized, not run
```

Current test_2 marker:

```text
READY_REBLOCKED_NO_PR59_MODEL
```

## Accepted Future Model Forms

Accepted form A, served endpoint:

```text
OPENAI_BASE_URL or equivalent endpoint URL reachable from the corrected mini-swe runner
OPENAI_API_KEY or explicit no-auth instruction
MODEL_NAME or exact served model id
serving provenance: upstream task id, checkpoint/model source, source commit, serving command/config, endpoint health log
health check: endpoint responds to a minimal completion request before mini-swe
PM authorization: PM explicitly names this endpoint/model id as eval-approved
```

Accepted form B, complete checkpoint/model plus serving handoff:

```text
SFT_CHECKPOINT_PATH or MODEL_PATH exists and is complete
required model files: config/tokenizer files plus weights or adapter files required by the serving stack
trainer_state.json present, or PM documents an explicit replacement provenance record
all_results.json present, or PM documents an explicit replacement metrics record
source/runtime provenance: source commit, bundle checksum, file list, data checksum, mcore_adapter checksum, transfer command, post-transfer verification, and no-remote-project-code/dependency-network proof
serving handoff: exact serving command/config, resolved model id, port/base URL, logs, and health check
PM authorization: PM explicitly gates this checkpoint/model or resulting endpoint for eval
```

Rejected current forms:

```text
No checkpoint/model path.
No checkpoint files.
No trainer_state.json.
No all_results.json.
No served endpoint/model id.
The stopped LTP SSH endpoint is not an inference endpoint.
```

## Eval Output And Intermediate Paths

All future mini-swe generated logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates must remain under `/home/xu.yang`.

Planned eval root:

```text
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2
LOG_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/logs
PREDICTIONS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/predictions
RESULTS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/results
METRICS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/metrics
RUN_METADATA_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/run_metadata
INTERMEDIATES_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/intermediates
TMPDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/tmp
HF_HOME=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/hf_home
HF_DATASETS_CACHE=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/hf_datasets
UV_CACHE_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/uv
APPTAINER_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/apptainer
SINGULARITY_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/singularity
```

Expected output files after a future PM-authorized smoke:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/predictions/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/results/results.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/metrics/metrics.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/run_metadata/run_metadata.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/logs/mini_swe_smoke.log
```

Existing required-path exceptions:

```text
/root/workspace/swe-bench-related/mini-swe-agent
  justification: required mini-swe source checkout on the corrected final workspace.

/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
  justification: required existing SWE-bench/mini-swe config path on the corrected final workspace.
```

## Command Template

Do not run this command until PM explicitly gates a checkpoint/model or served endpoint for eval.

```bash
ssh -p 31787 root@10.100.194.40 '
  set -euo pipefail
  export EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2
  export LOG_DIR=$EVAL_ROOT/logs
  export PREDICTIONS_DIR=$EVAL_ROOT/predictions
  export RESULTS_DIR=$EVAL_ROOT/results
  export METRICS_DIR=$EVAL_ROOT/metrics
  export RUN_METADATA_DIR=$EVAL_ROOT/run_metadata
  export INTERMEDIATES_DIR=$EVAL_ROOT/intermediates
  export TMPDIR=$EVAL_ROOT/tmp
  export HF_HOME=$EVAL_ROOT/cache/hf_home
  export HF_DATASETS_CACHE=$EVAL_ROOT/cache/hf_datasets
  export UV_CACHE_DIR=$EVAL_ROOT/cache/uv
  export APPTAINER_CACHEDIR=$EVAL_ROOT/cache/apptainer
  export SINGULARITY_CACHEDIR=$EVAL_ROOT/cache/singularity
  export OPENAI_BASE_URL=<PM_GATED_ENDPOINT_BASE_URL>
  export OPENAI_API_KEY=<PM_GATED_API_KEY_OR_DUMMY_IF_NO_AUTH>
  export MODEL_NAME=<PM_GATED_MODEL_ID>
  mkdir -p "$LOG_DIR" "$PREDICTIONS_DIR" "$RESULTS_DIR" "$METRICS_DIR" "$RUN_METADATA_DIR" "$INTERMEDIATES_DIR" "$TMPDIR" "$HF_HOME" "$HF_DATASETS_CACHE" "$UV_CACHE_DIR" "$APPTAINER_CACHEDIR" "$SINGULARITY_CACHEDIR"
  cd /root/workspace/swe-bench-related/mini-swe-agent
  git rev-parse HEAD | tee "$RUN_METADATA_DIR/mini_swe_git_head.txt"
  git status --short | tee "$RUN_METADATA_DIR/mini_swe_git_status.txt"
  uv run --with datasets mini-extra swebench \
    --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
    --split test \
    --subset verified \
    --workers 1 \
    --instances <PM_GATED_SMOKE_INSTANCE_ID_OR_LIST> \
    --model "$MODEL_NAME" \
    --output "$RESULTS_DIR/results.json" \
    --predictions-path "$PREDICTIONS_DIR/preds.json" \
    2>&1 | tee "$LOG_DIR/mini_swe_smoke.log"
'
```

## Metrics And PASS Criteria

Before execution:

```text
PM eval authorization explicitly names checkpoint/model or endpoint.
Model target matches accepted form A or form B.
All eval output/cache/temp paths resolve under /home/xu.yang.
mini-swe source git head/status is captured.
Endpoint health check or checkpoint serving handoff passes before mini-swe.
```

Smoke PASS:

```text
mini-swe command exits 0
predictions file exists and is non-empty
results file exists when SWE-bench scoring is requested
metrics/run metadata records model id, source task, source commit, checkpoint or endpoint, mini-swe git head/status, instance ids, start/end UTC, exit status, and artifact paths
no generated eval artifact is outside /home/xu.yang
no unauthorized remote project code/dependency clone/fetch/download is recorded for the eval handoff
```

Smoke FAIL:

```text
record command, environment, model target, instance id/list, log path, predictions/results/metrics presence or absence, exit status, and first actionable error
```

## Exact Unblock Condition

PM may unblock test_2 mini-swe execution only when all of the following are true:

1. A future runtime or PM-approved replacement evidence names a complete checkpoint/model path or a live served endpoint/model id.
2. The upstream evidence includes local/provided-workspace source packaging, exact commit/file list/checksums, transfer command, remote destination, post-transfer verification, and no-remote-project-code/dependency-network proof.
3. For checkpoint/model form, required config/tokenizer/weight or adapter files are complete, and `trainer_state.json` plus `all_results.json` are present or explicitly replaced by PM-approved provenance/metrics records.
4. For served endpoint form, endpoint/base URL is reachable, exact model id is provided, auth requirements are known, and a minimal completion health check passes.
5. PM explicitly states that the named checkpoint/model or endpoint is eval-approved for mini-swe.
6. All generated eval logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates are written under `/home/xu.yang`; any non-`/home/xu.yang` input paths are recorded with justification.

Until then, mini-swe remains ready-blocked and no eval/GPU/SFT/remote commands should be run by test_2.
