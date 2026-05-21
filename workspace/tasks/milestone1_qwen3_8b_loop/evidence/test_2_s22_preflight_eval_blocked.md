# Test 2 S22 Preflight-Failed Mini-SWE Eval Blocked Readiness

Timestamp: 2026-05-21T11:14:22Z

## Task Attachment

Task id: `M1-S22-PREFLIGHT-EVAL-BLOCKED-TEST2`

Owner: `intern_code_test_2`

Upstream runtime task: `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`

Scope: refresh mini-swe eval blocked/readiness evidence after NCCL/NVLink preflight failed before SFT.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s22_preflight_eval_blocked.md`

Status path: `workspace/interns/intern_code_test_2/status.md`

Execution rule: do not run eval/SFT/GPU/dry-run. mini-swe remains blocked until PM gates a complete checkpoint/model or served endpoint.

Completion marker: `BLOCKED_PREFLIGHT_FAILED_NO_MODEL`

## Runtime Evidence Read

Source runtime evidence:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_nccl_preflight_sft_runtime.md
```

Relevant runtime facts:

```text
preflight_result: PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
conditional_sft: NOT_RUN
reason: PM contract required SFT only if preflight passes; preflight wrote FAIL marker.
checkpoint/model: absent, because SFT was not run.
trainer_state.json: absent, because SFT was not run.
all_results.json: absent, because SFT was not run.
eval: not authorized and not run.
```

Allocation/stop facts:

```text
frame: xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
node: lg-cmc-b7r401-a04u26-h200-000769
endpoint: ssh -p 27402 root@10.100.24.11
state after stop: STOPPED (Completed)
endpoint proof after stop: connection refused
```

Preflight artifacts were preserved under:

```text
/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
```

## Eval Decision

Status: `BLOCKED_PREFLIGHT_FAILED_NO_MODEL`

mini-swe eval remains blocked because no accepted model form exists:

- SFT was not run after preflight failed.
- No checkpoint/model exists.
- No `trainer_state.json` exists.
- No `all_results.json` exists.
- No model id exists.
- No served endpoint exists.
- PM has not gated any model/endpoint for eval.

No mini-swe eval was run for this task.

## Accepted Future Model Forms

Future eval may proceed only after PM explicitly gates one of these accepted forms.

### Form A: Served Endpoint

Required handoff:

```text
source_runtime_task: <future PM-gated runtime task>
run_id: <future model-producing run id>
OPENAI_BASE_URL: <reachable OpenAI-compatible /v1 endpoint>
OPENAI_API_KEY: <token or explicit no-auth marker>
MODEL_NAME: <served model id>
model_source: <checkpoint/model path, registry id, or serving manifest>
serving_owner: <owner>
serving_command_or_manifest: <durable command/manifest path>
serving_log_path: <durable log path>
health_check: PASS
simple_completion_check: PASS
PM_eval_gate: <explicit approval reference>
```

### Form B: Checkpoint/Model Plus Serving Handoff

Required handoff:

```text
source_runtime_task: <future PM-gated runtime task>
run_id: <future model-producing run id>
SFT_CHECKPOINT_PATH: <readable complete checkpoint/model directory>
BASE_MODEL: <base model path/id>
model_type: <full model | adapter | merged model>
config_present: PASS
tokenizer_present: PASS
weights_present: PASS
trainer_state_json: <present or PM-approved replacement completion proof>
all_results_json: <present or PM-approved replacement metrics>
serving_handoff: <command/manifest exposing checkpoint through endpoint>
OPENAI_BASE_URL: <reachable OpenAI-compatible /v1 endpoint>
MODEL_NAME: <served model id>
PM_eval_gate: <explicit approval reference>
```

Raw checkpoint-only input is not sufficient. mini-swe needs a reachable served model target.

## Required `/home/xu.yang` Eval Storage

Default eval root for any future authorized run:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2
```

Required future generated paths:

```text
logs: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/logs
predictions: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/output/preds.json
results: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/output/results.json, if scoring runs
metrics: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/output/metrics_readiness.json
run metadata: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/metadata
trajectories: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/output/trajectories
temporary datasets/intermediates: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/tmp
HF_HOME: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/hf_home
HF_DATASETS_CACHE: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/hf_datasets_cache
UV_CACHE_DIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/uv_cache
APPTAINER_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/apptainer_cache
SINGULARITY_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/singularity_cache
```

Existing required input exceptions:

```text
mini-swe source: /root/workspace/swe-bench-related/mini-swe-agent
mini-swe/SWE-bench config: /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
```

Exception justification: these `/root/workspace/...` paths are existing source/config inputs on the corrected final workspace. Generated eval logs, predictions, results, metrics, run metadata, temporary datasets, caches, and intermediates must default to `/home/xu.yang`.

## Mini-SWE Smoke Command Template

Use only after PM explicitly gates a model/endpoint.

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent

export FUTURE_MODEL_RUN_ID="<pm-gated-model-run-id>"
export SFT_CHECKPOINT_PATH="<optional-complete-checkpoint-path-for-provenance>"
export MODEL_NAME="<served-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2
OUT="$EVAL_ROOT/output"
LOGS="$EVAL_ROOT/logs"
META="$EVAL_ROOT/metadata"
export TMPDIR="$EVAL_ROOT/tmp"
export HF_HOME="$EVAL_ROOT/hf_home"
export HF_DATASETS_CACHE="$EVAL_ROOT/hf_datasets_cache"
export UV_CACHE_DIR="$EVAL_ROOT/uv_cache"
export APPTAINER_CACHEDIR="$EVAL_ROOT/apptainer_cache"
export SINGULARITY_CACHEDIR="$EVAL_ROOT/singularity_cache"
mkdir -p "$OUT/trajectories" "$LOGS" "$META" "$TMPDIR" "$HF_HOME" "$HF_DATASETS_CACHE" "$UV_CACHE_DIR" "$APPTAINER_CACHEDIR" "$SINGULARITY_CACHEDIR"

cat > "$META/run_metadata.json" <<JSON
{
  "task_id": "M1-S22-PREFLIGHT-EVAL-BLOCKED-TEST2",
  "owner": "intern_code_test_2",
  "source_runtime_task": "M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2",
  "future_model_run_id": "$FUTURE_MODEL_RUN_ID",
  "model_name": "$MODEL_NAME",
  "checkpoint_path": "$SFT_CHECKPOINT_PATH",
  "openai_base_url": "$OPENAI_BASE_URL",
  "eval_root": "$EVAL_ROOT",
  "backend": "singularity",
  "slice": "lite/dev/0:2"
}
JSON

uv run --with datasets mini-extra swebench \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --slice 0:2 \
  --model "$MODEL_NAME" \
  --environment-class singularity \
  --workers 1 \
  --output "$OUT" \
  > "$LOGS/mini_swe_stdout_stderr.log" 2>&1
'
```

## Outputs To Verify After Future Authorized Eval

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/output/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/output/metrics_readiness.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/output/results.json, if scoring runs
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/output/trajectories/*.json or per-instance trajectory files
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/logs/mini_swe_stdout_stderr.log
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_preflight_eval_blocked_test2/metadata/run_metadata.json
```

Prediction fields:

```text
instance_id
model_name_or_path
model_patch
```

## Current Result

Result: `BLOCKED_PREFLIGHT_FAILED_NO_MODEL`

Reason: NCCL/NVLink preflight failed before SFT, so SFT was not run and no checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or model id exists. mini-swe eval remains blocked until PM gates a future model/endpoint. No eval/SFT/GPU/dry-run was performed by test_2.
