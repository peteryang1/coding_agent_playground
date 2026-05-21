# Test 2 S22 Parser-Fixed Mini-SWE Eval Blocked Readiness

Timestamp: 2026-05-21T12:02:15Z

## Task Attachment

Task id: `M1-S22-PARSERFIXED-EVAL-BLOCKED-TEST2`

Owner: `intern_code_test_2`

Upstream runtime task: `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`

Scope: refresh mini-swe eval blocked/readiness evidence after parser-fixed preflight failed before SFT and no checkpoint/model exists.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s22_parserfixed_eval_blocked.md`

Status path: `workspace/interns/intern_code_test_2/status.md`

Execution rule: do not run eval/GPU/SFT/dry-run. mini-swe remains blocked until PM gates a complete checkpoint/model or served endpoint.

Completion marker: `BLOCKED_PARSERFIXED_PREFLIGHT_NO_MODEL`

## Runtime Evidence Read

Source runtime evidence:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md
```

Key final evidence from dev_2:

```text
status: BLOCKED_PARSERFIXED_PREFLIGHT_FAILED_NO_SFT_RUN
structured preflight status: FAIL_HEALTH_SIGNATURE
sft_allowed: false
sft_allowed_if_pm_authorized: false
sft_skip_reason: FAIL_HEALTH_SIGNATURE
conditional SFT: NOT_RUN
checkpoint/model: absent, because SFT was not run.
trainer_state.json: absent, because SFT was not run.
all_results.json: absent, because SFT was not run.
eval: not authorized and not run.
```

Additional blocker details:

```text
health_status.txt:
  PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
  PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE
  ACTIONABLE_FAULT=true
  SFT_ALLOWED=false
  SFT_ALLOWED_IF_PM_AUTHORIZED=false
  SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
  TORCH_NCCL_ALLREDUCE_EXIT=0
  CAPACITY_PROBE_STATUS=PASS
  DIFFERENT_NODE_GATE=PASS
  HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
  REASON=actionable GPU/NCCL health signature found
```

Runtime lifecycle:

```text
frame: xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
endpoint: ssh -p 22662 root@10.100.22.14
node: lg-cmc-b7r202-p07u16-h200-000708
ltp_status: STOPPED (Completed)
ltp_completed: 2026-05-21 11:56:39
endpoint proof: connection refused after stop
```

Artifact preservation:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
preserved CephFS path: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
artifact cleanup: no cleanup of evidence artifacts was performed
```

## Eval Decision

Status: `BLOCKED_PARSERFIXED_PREFLIGHT_NO_MODEL`

mini-swe eval remains blocked because no accepted model form exists:

- parser-fixed preflight failed with `FAIL_HEALTH_SIGNATURE`;
- `sft_allowed=false`;
- SFT was not run;
- no checkpoint/model exists;
- no `trainer_state.json` exists;
- no `all_results.json` exists;
- no served endpoint or model id exists;
- LTP allocation is stopped and endpoint refuses connection;
- PM has not gated a model/endpoint for eval.

No mini-swe eval was run for this task.

## Accepted Future Model Forms

Future mini-swe eval may proceed only after PM explicitly gates one of these forms.

### Form A: Served Endpoint

Required PM-gated handoff:

```text
source_runtime_task: <future model-producing runtime task>
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

Required PM-gated handoff:

```text
source_runtime_task: <future model-producing runtime task>
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

Default eval root for any future PM-authorized mini-swe run:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2
```

Required future generated paths:

```text
logs: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/logs
predictions: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/output/preds.json
results: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/output/results.json, if scoring runs
metrics: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/output/metrics_readiness.json
run metadata: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/metadata
trajectories: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/output/trajectories
temporary datasets/intermediates: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/tmp
HF_HOME: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/hf_home
HF_DATASETS_CACHE: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/hf_datasets_cache
UV_CACHE_DIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/uv_cache
APPTAINER_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/apptainer_cache
SINGULARITY_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2/singularity_cache
```

Existing required eval input exceptions:

```text
mini-swe source: /root/workspace/swe-bench-related/mini-swe-agent
mini-swe/SWE-bench config: /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
```

Exception justification: those `/root/workspace/...` paths are existing source/config inputs on the corrected final workspace. Generated eval logs, predictions, results, metrics, run metadata, temporary datasets, caches, and intermediates must default to `/home/xu.yang`.

## Mini-SWE Smoke Template For Future PM Gate

Use only after PM explicitly gates a complete checkpoint/model or served endpoint.

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent

export FUTURE_MODEL_RUN_ID="<pm-gated-model-run-id>"
export SFT_CHECKPOINT_PATH="<optional-complete-checkpoint-path-for-provenance>"
export MODEL_NAME="<served-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_blocked_test2
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
  "task_id": "M1-S22-PARSERFIXED-EVAL-BLOCKED-TEST2",
  "owner": "intern_code_test_2",
  "source_runtime_task": "M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2",
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

## Current Result

Result: `BLOCKED_PARSERFIXED_PREFLIGHT_NO_MODEL`

Reason: parser-fixed preflight failed with `FAIL_HEALTH_SIGNATURE`; `sft_allowed=false`; SFT was not run; no checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or model id exists; LTP is stopped. mini-swe eval remains blocked until PM gates a future model/endpoint. No eval/GPU/SFT/dry-run was performed by test_2.
