# Test 2 Session 23 Parser-Patch Mini-SWE Eval Readiness

Timestamp: 2026-05-21T12:26:41Z

## Task Attachment

Task id: `M1-S23-PARSERPATCH-EVAL-READY-TEST2`

Owner: `intern_code_test_2`

Scope: keep mini-swe eval readiness current for a future parser-patch SFT checkpoint path or served endpoint.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s23_parserpatch_eval_ready.md`

Status path: `workspace/interns/intern_code_test_2/status.md`

Execution rule: do not run eval/GPU/SFT/dry-run. mini-swe may run only after PM explicitly gates a complete checkpoint/model or served endpoint.

Current completion marker: `READY_PACKAGE_BLOCKED_NO_MODEL`

## Current Blocker

Status: `READY_PACKAGE_BLOCKED_NO_MODEL`

Current known state:

- No Session 23 parser-patch checkpoint/model has been handed to test_2.
- No `trainer_state.json` has been handed to test_2.
- No `all_results.json` has been handed to test_2.
- No served endpoint has been handed to test_2.
- No model id has been handed to test_2.
- PM has not authorized mini-swe eval for a Session 23 parser-patch artifact.

No eval/GPU/SFT/dry-run was performed for this readiness package.

## Accepted Future Form A: Served Endpoint

Required PM-gated handoff:

```text
source_runtime_task: <future Session 23 parser-patch SFT runtime task>
run_id: <future parser-patch model-producing run id>
OPENAI_BASE_URL: <reachable OpenAI-compatible /v1 endpoint>
OPENAI_API_KEY: <token or explicit no-auth marker>
MODEL_NAME: <served model id>
model_source: <checkpoint/model path, registry id, or serving manifest>
serving_owner: <owner>
serving_command_or_manifest: <durable command/manifest path>
serving_log_path: <durable log path under /home/xu.yang or justified existing-required path>
health_check: PASS
simple_completion_check: PASS
PM_eval_gate: <explicit approval reference>
```

Endpoint preflight before eval:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
test -n "${OPENAI_BASE_URL:?missing OPENAI_BASE_URL}"
test -n "${MODEL_NAME:?missing MODEL_NAME}"
python3 - <<PY
import os, urllib.request
base = os.environ["OPENAI_BASE_URL"].rstrip("/")
req = urllib.request.Request(base + "/models")
if os.environ.get("OPENAI_API_KEY"):
    req.add_header("Authorization", "Bearer " + os.environ["OPENAI_API_KEY"])
with urllib.request.urlopen(req, timeout=15) as r:
    print("status=", r.status)
    print(r.read(4096).decode("utf-8", errors="replace"))
PY'
```

## Accepted Future Form B: Checkpoint/Model Plus Serving Handoff

Required PM-gated handoff:

```text
source_runtime_task: <future Session 23 parser-patch SFT runtime task>
run_id: <future parser-patch model-producing run id>
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

Checkpoint preflight before eval:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
test -n "${SFT_CHECKPOINT_PATH:?missing SFT_CHECKPOINT_PATH}"
test -d "$SFT_CHECKPOINT_PATH"
find "$SFT_CHECKPOINT_PATH" -maxdepth 1 -type f | sort
test -f "$SFT_CHECKPOINT_PATH/config.json"
find "$SFT_CHECKPOINT_PATH" -maxdepth 1 \( -name "tokenizer*" -o -name "special_tokens_map.json" \) | grep -q .
find "$SFT_CHECKPOINT_PATH" -maxdepth 1 \( -name "*.safetensors" -o -name "pytorch_model*.bin" -o -name "adapter_model*" \) | grep -q .
'
```

Raw checkpoint-only input is not sufficient. mini-swe needs a reachable served model target.

## Required `/home/xu.yang` Eval Storage

Default eval root for any future PM-authorized Session 23 parser-patch mini-swe run:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2
```

Required generated eval paths:

```text
logs: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/logs
predictions: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/output/preds.json
results: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/output/results.json, if scoring runs
metrics: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/output/metrics_readiness.json
run metadata: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/metadata
trajectories: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/output/trajectories
temporary datasets/intermediates: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/tmp
HF_HOME: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/hf_home
HF_DATASETS_CACHE: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/hf_datasets_cache
UV_CACHE_DIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/uv_cache
APPTAINER_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/apptainer_cache
SINGULARITY_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/singularity_cache
```

Existing required eval input exceptions:

```text
mini-swe source: /root/workspace/swe-bench-related/mini-swe-agent
mini-swe/SWE-bench config: /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
```

Exception justification: those `/root/workspace/...` paths are existing source/config inputs on the corrected final workspace. Generated eval logs, predictions, results, metrics, run metadata, temporary datasets, caches, and intermediates must default to `/home/xu.yang`.

## Mini-SWE Smoke Command Template

Use only after PM explicitly gates a complete checkpoint/model or served endpoint.

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent

export S23_PARSERPATCH_RUN_ID="<s23-parserpatch-model-run-id>"
export SFT_CHECKPOINT_PATH="<optional-complete-checkpoint-path-for-provenance>"
export MODEL_NAME="<served-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2
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
  "task_id": "M1-S23-PARSERPATCH-EVAL-READY-TEST2",
  "owner": "intern_code_test_2",
  "source_runtime_task": "<future Session 23 parser-patch SFT runtime task>",
  "s23_parserpatch_run_id": "$S23_PARSERPATCH_RUN_ID",
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

## Exact PM Authorization Condition

PM can authorize mini-swe eval only after durable evidence names an eval-approved model target and all applicable conditions are met:

- A future Session 23 parser-patch runtime or PM-approved replacement produces a complete checkpoint/model or served endpoint.
- If checkpoint form: config, tokenizer, weights/adapters, `trainer_state.json`, and `all_results.json` or PM-approved replacements are present.
- If checkpoint form: a serving handoff exposes the model as a reachable endpoint.
- If endpoint form: health check and simple completion proof pass.
- PM explicitly names the checkpoint/model path or served endpoint as eval-approved for mini-swe.
- Future mini-swe generated logs, predictions, results, metrics, run metadata, temporary datasets, caches, and intermediates are under `/home/xu.yang`.
- Any non-`/home/xu.yang` source/config input has an existing-required-path justification.

## Outputs To Verify After Future Authorized Eval

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/output/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/output/metrics_readiness.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/output/results.json, if scoring runs
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/output/trajectories/*.json or per-instance trajectory files
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/logs/mini_swe_stdout_stderr.log
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_parserpatch_eval_ready_test2/metadata/run_metadata.json
```

Prediction fields:

```text
instance_id
model_name_or_path
model_patch
```

## Current Result

Result: `READY_PACKAGE_BLOCKED_NO_MODEL`

Reason: Session 23 parser-patch eval readiness is prepared, but no checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or model id has been handed to test_2. No eval/GPU/SFT/dry-run was performed.
