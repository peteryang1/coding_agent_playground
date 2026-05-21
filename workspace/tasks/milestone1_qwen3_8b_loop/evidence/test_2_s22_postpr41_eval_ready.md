# Test 2 S22 Post-PR41 Mini-SWE Eval Handoff Readiness

Timestamp: 2026-05-21T10:10:13Z

## Task Attachment

Task id: `M1-S22-POSTPR41-EVAL-READY-TEST2`

Owner: `intern_code_test_2`

Upstream runtime task: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`

Scope: prepare the mini-swe eval handoff package for a future checkpoint/model or served endpoint produced by `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s22_postpr41_eval_ready.md`

Status path: `workspace/interns/intern_code_test_2/status.md`

Execution rule: do not run mini-swe/eval until PM explicitly gates a complete checkpoint/model or served endpoint from dev_2 evidence.

Current completion marker: `READY_PACKAGE_BLOCKED_NO_MODEL`

## Current Blocker

Status: `READY_PACKAGE_BLOCKED_NO_MODEL`

Current reason:

- `M1-S22-POSTPR41-SFT-RUNTIME-DEV2` has not yet provided a PM-gated complete checkpoint/model or served endpoint to test_2.
- mini-swe requires a model target. Without a complete checkpoint/model plus serving handoff, or a reachable served endpoint, any eval run would only test missing-model infrastructure behavior.
- No mini-swe eval command was run for this package.

Unblock condition:

```text
PM explicitly gates a complete checkpoint/model or served endpoint from dev_2 evidence for M1-S22-POSTPR41-SFT-RUNTIME-DEV2.
```

If dev_2 produces a checkpoint, test_2 is ready to gate/run only after PM explicit eval authorization.

## Accepted Form A: Served Endpoint

Required PM-gated handoff fields:

```text
source_runtime_task: M1-S22-POSTPR41-SFT-RUNTIME-DEV2
run_id: <postpr41-sft-run-id>
OPENAI_BASE_URL: <reachable OpenAI-compatible /v1 endpoint>
OPENAI_API_KEY: <token or explicit no-auth marker>
MODEL_NAME: <served model id>
model_source: <checkpoint/model path, registry id, or serving manifest>
serving_owner: <owner>
serving_command_or_manifest: <durable command/manifest path>
serving_log_path: <durable log path>
health_check: PASS for /models or equivalent
simple_completion_check: PASS
PM_eval_gate: <explicit approval reference>
```

Endpoint preflight:

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

## Accepted Form B: Checkpoint/Model Plus Serving Handoff

Required PM-gated handoff fields:

```text
source_runtime_task: M1-S22-POSTPR41-SFT-RUNTIME-DEV2
run_id: <postpr41-sft-run-id>
SFT_CHECKPOINT_PATH: <readable complete checkpoint/model directory>
BASE_MODEL: <base model path/id>
model_type: <full model | adapter | merged model>
config_present: PASS
tokenizer_present: PASS
weights_present: PASS
trainer_state_json: <present or PM-approved replacement completion proof>
all_results_json: <present or PM-approved replacement metrics>
serving_handoff: <command/manifest that exposes checkpoint through endpoint>
OPENAI_BASE_URL: <reachable OpenAI-compatible /v1 endpoint>
MODEL_NAME: <served model id>
PM_eval_gate: <explicit approval reference>
```

Checkpoint preflight:

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

Raw checkpoint-only input is not sufficient. A checkpoint path must either already be served or include a PM-gated serving handoff that exposes a reachable model endpoint for mini-swe.

## Required Workspace Inputs

Corrected final workspace:

```text
ssh -p 31787 root@10.100.194.40
```

Existing required inputs:

```text
mini-swe source: /root/workspace/swe-bench-related/mini-swe-agent
mini-swe/SWE-bench config: /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
```

Exception justification:

- `/root/workspace/swe-bench-related/mini-swe-agent` is the existing required mini-swe source checkout on the corrected final workspace.
- `/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml` is the existing required mini-swe/SWE-bench config input.
- Generated eval logs, predictions, results, metrics, run metadata, temporary datasets, caches, and intermediates must default to `/home/xu.yang`.

Before an authorized eval, verify:

```text
mini-swe source path exists
mini-swe git sha and dirty-state provenance recorded
uv available
singularity/apptainer available
PM eval gate exists
accepted model form A or B is complete
```

## Required `/home/xu.yang` Eval Storage

Default eval root:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2
```

Required generated paths:

```text
logs: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/logs
predictions: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/preds.json
results: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/results.json, if scoring runs
metrics: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/metrics_readiness.json
run metadata: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/metadata
trajectories: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/trajectories
temporary datasets/intermediates: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/tmp
HF_HOME: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/hf_home
HF_DATASETS_CACHE: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/hf_datasets_cache
UV_CACHE_DIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/uv_cache
APPTAINER_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/apptainer_cache
SINGULARITY_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/singularity_cache
```

Any future non-`/home/xu.yang` generated eval output or intermediate is a blocker unless an existing-required-path justification is written before execution.

## Mini-SWE Smoke Command Template

Use only after PM explicit eval authorization.

Two-instance smoke:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent

export POSTPR41_RUN_ID="<postpr41-sft-run-id>"
export SFT_CHECKPOINT_PATH="<optional-complete-checkpoint-path-for-provenance>"
export MODEL_NAME="<served-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2
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
  "task_id": "M1-S22-POSTPR41-EVAL-READY-TEST2",
  "owner": "intern_code_test_2",
  "source_runtime_task": "M1-S22-POSTPR41-SFT-RUNTIME-DEV2",
  "postpr41_run_id": "$POSTPR41_RUN_ID",
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

Single-instance debug fallback, also only after PM explicit eval authorization:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent

export MODEL_NAME="<served-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2
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

Expected files:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/metrics_readiness.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/results.json, if scoring runs
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/trajectories/*.json or per-instance trajectory files
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/logs/mini_swe_stdout_stderr.log
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/metadata/run_metadata.json
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
  "task_id": "M1-S22-POSTPR41-EVAL-READY-TEST2",
  "owner": "intern_code_test_2",
  "source_runtime_task": "M1-S22-POSTPR41-SFT-RUNTIME-DEV2",
  "postpr41_run_id": "<run id>",
  "model_name_or_path": "<MODEL_NAME>",
  "checkpoint_path": "<SFT_CHECKPOINT_PATH or empty>",
  "agent": "mini-swe-agent",
  "backend": "singularity",
  "benchmark": "SWE-bench lite dev slice 0:2",
  "eval_root": "/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2",
  "predictions_path": "/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/output/preds.json",
  "results_json_path": "<path or empty>",
  "logs_path": "/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_postpr41_eval_ready_test2/logs/mini_swe_stdout_stderr.log",
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

- PM-gated checkpoint/model or served endpoint from `M1-S22-POSTPR41-SFT-RUNTIME-DEV2` exists.
- Endpoint/checkpoint preflight checks pass.
- `/home/xu.yang` eval root, logs, predictions, results, metrics, metadata, caches, and intermediates are used.
- mini-swe two-instance smoke exits without infrastructure/auth/dataset/Singularity traceback.
- Predictions exist for the smoke slice and include `instance_id`, `model_name_or_path`, and `model_patch`.
- Metrics readiness JSON is written under `/home/xu.yang`.

FAIL:

- PM-gated model exists, but mini-swe cannot produce predictions because of model/API/config failure.
- mini-swe, dataset loading, Singularity/Apptainer, or scoring fails after pre-run checks.
- Predictions are missing or malformed after attempted eval.
- Metrics readiness file is missing after attempted eval.
- Generated eval files are written outside `/home/xu.yang` without prior existing-required-path justification.

BLOCKED:

- No PM-gated complete checkpoint/model or served endpoint exists.
- Raw checkpoint exists but lacks serving handoff.
- Endpoint is unreachable.
- Required model env vars are absent.
- Checkpoint lacks config/tokenizer/complete weights or accepted adapter files.
- PM explicit eval authorization is absent.

## Current Result

Result: `READY_PACKAGE_BLOCKED_NO_MODEL`

Reason: eval handoff is prepared for `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`, but dev_2 has not yet produced a PM-gated checkpoint/model or served endpoint. No mini-swe eval was run.
