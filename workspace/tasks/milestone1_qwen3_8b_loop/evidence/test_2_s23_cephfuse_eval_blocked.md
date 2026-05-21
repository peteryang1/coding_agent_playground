# Test 2 S23 Ceph-Fuse Mini-SWE Eval Blocked Readiness

Timestamp: 2026-05-21T13:05:27Z

## Task Attachment

Task id: `M1-S23-CEPHFUSE-EVAL-BLOCKED-TEST2`

Owner: `intern_code_test_2`

Upstream runtime task: `M1-S23-PARSERPATCH-PREFLIGHT-SFT-RUNTIME-DEV2`

Scope: refresh mini-swe eval blocked/readiness evidence after parser-patch runtime failed before transfer, preflight, and SFT.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s23_cephfuse_eval_blocked.md`

Status path: `workspace/interns/intern_code_test_2/status.md`

Execution rule: do not run eval/GPU/SFT. mini-swe remains blocked until PM gates a complete checkpoint/model or served endpoint.

Completion marker: `BLOCKED_CEPHFUSE_BOOTSTRAP_NO_MODEL`

## Runtime Evidence Read

Source runtime evidence:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_parserpatch_preflight_sft_runtime.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_parserpatch_preflight_sft_tracking.md
```

Key final runtime facts:

```text
runtime status: BLOCKED_LTP_BOOTSTRAP_CEPH_FUSE_MISSING_NO_PREFLIGHT_NO_SFT
tracking outcome: FAILED_COMPLETED_BOOTSTRAP_NO_GPU_RUNTIME
frame: xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
LTP state: FAILED (Completed)
exit_code: 220 Failed
originUserExitCode: 127
node from events: lg-cmc-b7r202-q04u06-h200-000725
endpoint: ssh -p 36822 root@10.100.22.31
```

Ceph-fuse bootstrap blocker:

```text
exact log: /usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found
root cause: LTP image/spec lacked ceph-fuse at bootstrap, so /home/xu.yang/CephFS output root could not be mounted/proved.
```

Execution boundary from dev_2 evidence:

```text
remote source transfer: not performed because job never reached usable RUNNING endpoint.
remote post-transfer verification: not performed.
preflight: not run.
health_status.json/txt: absent because preflight did not run.
capacity/topology/NVLink/NCCL all-reduce: not run.
conditional SFT: not run because preflight did not run and sft_allowed was never true.
checkpoint/model: absent.
trainer_state.json: absent.
all_results.json: absent.
eval: not authorized and not run.
```

Release proof:

```text
post-stop terminal state: FAILED (Completed)
endpoint proof: connection refused
running coding-agent-playground jobs: No jobs found
no LTP retry or second allocation was submitted
```

## Eval Decision

Status: `BLOCKED_CEPHFUSE_BOOTSTRAP_NO_MODEL`

mini-swe eval remains blocked because no accepted model form exists:

- runtime failed during LTP bootstrap before transfer;
- no preflight ran;
- no SFT ran;
- no checkpoint/model exists;
- no `trainer_state.json` exists;
- no `all_results.json` exists;
- no served endpoint or model id exists;
- PM has not gated any model/endpoint for eval.

No eval/GPU/SFT was run by test_2 for this task.

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
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2
```

Required future generated eval paths:

```text
logs: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/logs
predictions: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/output/preds.json
results: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/output/results.json, if scoring runs
metrics: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/output/metrics_readiness.json
run metadata: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/metadata
trajectories: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/output/trajectories
temporary datasets/intermediates: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/tmp
HF_HOME: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/hf_home
HF_DATASETS_CACHE: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/hf_datasets_cache
UV_CACHE_DIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/uv_cache
APPTAINER_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/apptainer_cache
SINGULARITY_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2/singularity_cache
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

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_eval_blocked_test2
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
  "task_id": "M1-S23-CEPHFUSE-EVAL-BLOCKED-TEST2",
  "owner": "intern_code_test_2",
  "source_runtime_task": "<future model-producing runtime task>",
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

## PM Authorization Condition

PM can authorize mini-swe eval only after durable evidence shows all applicable conditions:

- A future runtime or PM-approved replacement produces a complete checkpoint/model or served endpoint.
- If checkpoint form: config, tokenizer, weights/adapters, `trainer_state.json`, and `all_results.json` or PM-approved replacements are present.
- If checkpoint form: a serving handoff exposes the model as a reachable endpoint.
- If endpoint form: health check and simple completion proof pass.
- PM explicitly names the checkpoint/model path or served endpoint as eval-approved for mini-swe.
- Future mini-swe generated logs, predictions, results, metrics, run metadata, temporary datasets, caches, and intermediates are under `/home/xu.yang`.
- Any non-`/home/xu.yang` source/config input has an existing-required-path justification.

## Current Result

Result: `BLOCKED_CEPHFUSE_BOOTSTRAP_NO_MODEL`

Reason: parser-patch runtime failed during LTP bootstrap with `ceph-fuse: command not found`, before transfer, preflight, SFT, or eval. No checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or model id exists. No eval/GPU/SFT was performed by test_2.
