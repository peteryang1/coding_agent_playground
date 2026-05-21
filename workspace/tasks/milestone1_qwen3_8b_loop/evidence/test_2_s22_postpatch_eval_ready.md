# Test 2 S22 Post-Patch Mini-SWE Eval Readiness

Timestamp: 2026-05-21T08:55:45Z

## Task Attachment

Task id: `M1-S22-POSTPATCH-EVAL-READY-TEST2`

Owner: `intern_code_test_2`

Scope: refresh mini-swe eval readiness for a future post-patch checkpoint path or served endpoint, with all future eval intermediates and outputs defaulting to CephFS `/home/xu.yang`.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s22_postpatch_eval_ready.md`

Status path: `workspace/interns/intern_code_test_2/status.md`

Execution rule: do not run eval until PM gates a complete model/checkpoint or served endpoint.

Completion marker for current state: `READY_PACKAGE_BLOCKED_NO_MODEL`.

## Current Blocker

Status: `READY_PACKAGE_BLOCKED_NO_MODEL`

mini-swe eval remains blocked because there is currently no PM-gated post-patch checkpoint/model or served endpoint. The latest durable S22 eval blocker evidence records no checkpoint/model, no model id, no `trainer_state.json`, no `all_results.json`, and no served endpoint after the Session 22 early-exit runtime failure.

This file is a readiness package only. No mini-swe eval was run.

## Accepted Model Forms

Future eval may proceed only after PM gates one of these forms.

### Form A: Served Endpoint

Required handoff fields:

```text
task_id/source_runtime_task=<runtime task id that produced the model>
run_id=<post-patch SFT run id>
OPENAI_BASE_URL=<reachable OpenAI-compatible endpoint ending in /v1>
OPENAI_API_KEY=<token or explicit no-auth marker>
MODEL_NAME=<served model id>
checkpoint_or_model_source=<source checkpoint/model path or model registry id>
serving_owner=<owner>
serving_command_or_manifest=<path or command>
serving_log_path=<durable log path>
health_check=/models or equivalent PASS
simple_completion_check=PASS
PM_eval_gate=<approval reference>
```

Pre-run endpoint checks:

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

### Form B: Checkpoint/Model Path Plus Serving Handoff

Required handoff fields:

```text
task_id/source_runtime_task=<runtime task id that produced the checkpoint>
run_id=<post-patch SFT run id>
SFT_CHECKPOINT_PATH=<readable complete checkpoint/model directory>
BASE_MODEL=<base model path/id>
model_type=<full model | adapter | merged model>
config_present=PASS
tokenizer_present=PASS
weights_present=PASS
trainer_state_json=<present or PM-approved replacement>
all_results_json=<present or PM-approved replacement>
serving_handoff=<command/manifest that exposes checkpoint through endpoint>
OPENAI_BASE_URL=<reachable OpenAI-compatible endpoint ending in /v1>
MODEL_NAME=<served model id>
PM_eval_gate=<approval reference>
```

Pre-run checkpoint checks:

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

Raw checkpoint-only input is not sufficient for mini-swe. It must have a serving handoff and reachable model endpoint before eval.

## Required Environment

Corrected final workspace:

```text
ssh -p 31787 root@10.100.194.40
```

Known required source/config inputs:

```text
mini-swe source: /root/workspace/swe-bench-related/mini-swe-agent
mini-swe/SWE-bench config: /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
```

Existing required path exception justification:

- `/root/workspace/swe-bench-related/mini-swe-agent` is the existing required mini-swe source checkout on the corrected final workspace.
- `/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml` is the existing required config input.
- Generated eval outputs, logs, metadata, caches, temporary datasets, and intermediates must not default to `/root/workspace`; they must default to `/home/xu.yang`.

Before any authorized eval, re-check:

```text
mini-swe checkout exists
mini-swe git sha
mini-swe dirty files/diff provenance
uv available
singularity/apptainer available
OPENAI_BASE_URL/MODEL_NAME reachable, if endpoint form
SFT_CHECKPOINT_PATH readable and complete, if checkpoint form
PM gate approval exists
```

## `/home/xu.yang` Eval Storage Rule

All future mini-swe eval generated files for this task default to:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2
```

Required future paths:

```text
eval root: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2
logs: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/logs
predictions: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/preds.json
results: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/results.json, if scoring runs
metrics: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/metrics_readiness.json
run metadata: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/metadata
trajectories: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/trajectories
temporary datasets/intermediates: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/tmp
HF_HOME: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/hf_home
HF_DATASETS_CACHE: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/hf_datasets_cache
UV_CACHE_DIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/uv_cache
APPTAINER_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/apptainer_cache
SINGULARITY_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/singularity_cache
```

Any future non-`/home/xu.yang` generated output or intermediate is a blocker unless an existing-required-path justification is written before execution.

## Command Template

Two-instance mini-swe smoke template for a PM-gated post-patch model endpoint:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent

export POSTPATCH_RUN_ID="<postpatch-sft-run-id>"
export SFT_CHECKPOINT_PATH="<optional-complete-checkpoint-path-for-provenance>"
export MODEL_NAME="<served-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2
OUT="$EVAL_ROOT/output"
LOGS="$EVAL_ROOT/logs"
META="$EVAL_ROOT/metadata"
export TMPDIR="$EVAL_ROOT/tmp"
export HF_HOME="$EVAL_ROOT/hf_home"
export HF_DATASETS_CACHE="$EVAL_ROOT/hf_datasets_cache"
export UV_CACHE_DIR="$EVAL_ROOT/uv_cache"
export APPTAINER_CACHEDIR="$EVAL_ROOT/apptainer_cache"
export SINGULARITY_CACHEDIR="$EVAL_ROOT/singularity_cache"
mkdir -p "$OUT" "$LOGS" "$META" "$TMPDIR" "$HF_HOME" "$HF_DATASETS_CACHE" "$UV_CACHE_DIR" "$APPTAINER_CACHEDIR" "$SINGULARITY_CACHEDIR"

cat > "$META/run_metadata.json" <<JSON
{
  "task_id": "M1-S22-POSTPATCH-EVAL-READY-TEST2",
  "owner": "intern_code_test_2",
  "postpatch_run_id": "$POSTPATCH_RUN_ID",
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

Single-instance debug fallback, only after PM gates a model/endpoint:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent

export MODEL_NAME="<served-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2
OUT="$EVAL_ROOT/output"
LOGS="$EVAL_ROOT/logs"
export TMPDIR="$EVAL_ROOT/tmp"
export HF_HOME="$EVAL_ROOT/hf_home"
export HF_DATASETS_CACHE="$EVAL_ROOT/hf_datasets_cache"
export UV_CACHE_DIR="$EVAL_ROOT/uv_cache"
export APPTAINER_CACHEDIR="$EVAL_ROOT/apptainer_cache"
export SINGULARITY_CACHEDIR="$EVAL_ROOT/singularity_cache"
mkdir -p "$OUT/trajectories" "$LOGS" "$TMPDIR" "$HF_HOME" "$HF_DATASETS_CACHE" "$UV_CACHE_DIR" "$APPTAINER_CACHEDIR" "$SINGULARITY_CACHEDIR"

uv run --with datasets mini-extra swebench-single \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --instance 0 \
  --model "$MODEL_NAME" \
  --environment-class singularity \
  --exit-immediately \
  --output "$OUT/trajectories/single_instance_0.traj.json" \
  > "$LOGS/mini_swe_single_stdout_stderr.log" 2>&1
'
```

## Outputs To Verify After Authorized Eval

Required generated files under `/home/xu.yang`:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/metrics_readiness.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/results.json, if SWE-bench scoring runs
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/trajectories/*.json or per-instance trajectory files
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/logs/mini_swe_stdout_stderr.log
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/metadata/run_metadata.json
```

Prediction fields:

```text
instance_id
model_name_or_path
model_patch
```

Metrics readiness schema:

```json
{
  "task_id": "M1-S22-POSTPATCH-EVAL-READY-TEST2",
  "owner": "intern_code_test_2",
  "postpatch_run_id": "<run id>",
  "model_name_or_path": "<MODEL_NAME>",
  "checkpoint_path": "<SFT_CHECKPOINT_PATH or empty>",
  "agent": "mini-swe-agent",
  "backend": "singularity",
  "benchmark": "SWE-bench lite dev slice 0:2",
  "eval_root": "/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2",
  "predictions_path": "/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/output/preds.json",
  "results_json_path": "<path or empty>",
  "logs_path": "/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpatch_eval_ready_test2/logs/mini_swe_stdout_stderr.log",
  "total_instances": 2,
  "instances_submitted": 2,
  "instances_completed": 0,
  "instances_resolved": 0,
  "resolution_rate": 0.0,
  "status": "<PASS|FAIL|BLOCKED|PREDICTIONS_ONLY>",
  "blockers": []
}
```

## PASS / FAIL / BLOCKED Criteria

PASS:

- PM-gated post-patch checkpoint/model or served endpoint exists.
- Endpoint/model pre-run checks pass.
- Required `/home/xu.yang` eval root and cache/temp paths are used.
- mini-swe smoke exits without infrastructure/auth/dataset/Singularity traceback.
- Predictions exist for the smoke slice.
- Prediction records include `instance_id`, `model_name_or_path`, and `model_patch`.
- Metrics readiness JSON is written under `/home/xu.yang`.

FAIL:

- PM-gated model exists, but mini-swe cannot produce predictions because of model/API/config failure.
- mini-swe, dataset loading, Singularity/Apptainer, or scoring fails after pre-run checks.
- Predictions are missing or malformed after attempted eval.
- Metrics readiness file is missing after attempted eval.
- Generated logs/predictions/results/metrics/metadata/intermediates are written outside `/home/xu.yang` without prior existing-required-path justification.

BLOCKED:

- No PM-gated complete checkpoint/model or served endpoint exists.
- Only a raw checkpoint exists with no serving handoff.
- Endpoint is unreachable from corrected final workspace.
- Required model env vars are absent.
- Checkpoint path lacks config/tokenizer/complete weights or accepted adapter files.
- PM gate approval is absent.

## Current Result

Result: `READY_PACKAGE_BLOCKED_NO_MODEL`

Reason: post-patch mini-swe readiness is refreshed, but there is no PM-gated complete checkpoint/model or served endpoint yet. Eval remains blocked. No eval was run.
