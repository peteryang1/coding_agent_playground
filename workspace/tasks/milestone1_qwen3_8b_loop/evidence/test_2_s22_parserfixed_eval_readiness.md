# Test 2 S22 Parser-Fixed Mini-SWE Eval Readiness Gate

Timestamp: 2026-05-21T11:46:52Z

## Task Attachment

Task id: `M1-S22-PARSERFIXED-EVAL-READINESS-TEST2`

Owner: `intern_code_test_2`

Upstream runtime task: `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`

Scope: prepare a no-execution mini-swe eval readiness gate for a possible future checkpoint/model or served endpoint from dev_2 evidence.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s22_parserfixed_eval_readiness.md`

Status path: `workspace/interns/intern_code_test_2/status.md`

Execution rule: do not run eval and do not use GPU. mini-swe may run only after PM explicitly gates a complete checkpoint/model or served endpoint.

Current completion marker: `READY_PACKAGE_BLOCKED_NO_MODEL`

## Runtime Evidence Watched

Watched dev_2 evidence:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md
```

Current dev_2 evidence state:

```text
runtime_status: AUTHORIZED_PRE_SUBMIT
LTP submit: not recorded
GPU command: not run
NCCL preflight: not run
SFT: not run
eval authorization: false
checkpoint/model: absent
served endpoint: absent
```

dev_2 storage contract:

```text
output_root: /home/xu.yang/coding_agent_playground/outputs
generated artifacts, preflight, health_status, temporary converted datasets, logs, checkpoints, run metadata, trainer outputs, and intermediates must be under output_root
```

Existing required runtime input exceptions from dev_2 evidence:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source_dataset_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dependency archives/wheels if needed: /mnt/3fs/data/ai4ai/deps
```

Interpretation: no eval-ready artifact exists yet. test_2 should continue watching for either a complete checkpoint/model plus serving handoff or a served endpoint in dev_2 evidence.

## Current Blocker

Status: `READY_PACKAGE_BLOCKED_NO_MODEL`

Current blocker:

- No checkpoint/model exists in `evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md`.
- No served endpoint or model id exists.
- No `trainer_state.json` or `all_results.json` exists.
- PM has not gated any parser-fixed runtime artifact for mini-swe eval.

No mini-swe eval was run for this readiness package.

## Accepted Future Form A: Served Endpoint

Required PM-gated handoff fields:

```text
source_runtime_task: M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2
run_id: <parserfixed-preflight-sft-run-id>
preflight_status: PASS
sft_status: <PASS or PM-accepted model-producing status>
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

Required PM-gated handoff fields:

```text
source_runtime_task: M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2
run_id: <parserfixed-preflight-sft-run-id>
preflight_status: PASS
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

## Required `/home/xu.yang` Eval Output Paths

Default eval root for any future PM-authorized mini-swe run:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2
```

Required generated eval paths:

```text
logs: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/logs
predictions: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/output/preds.json
results: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/output/results.json, if scoring runs
metrics: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/output/metrics_readiness.json
run metadata: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/metadata
trajectories: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/output/trajectories
temporary datasets/intermediates: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/tmp
HF_HOME: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/hf_home
HF_DATASETS_CACHE: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/hf_datasets_cache
UV_CACHE_DIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/uv_cache
APPTAINER_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/apptainer_cache
SINGULARITY_CACHEDIR: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/singularity_cache
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

export PARSERFIXED_RUN_ID="<parserfixed-preflight-sft-run-id>"
export SFT_CHECKPOINT_PATH="<optional-complete-checkpoint-path-for-provenance>"
export MODEL_NAME="<served-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"

EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2
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
  "task_id": "M1-S22-PARSERFIXED-EVAL-READINESS-TEST2",
  "owner": "intern_code_test_2",
  "source_runtime_task": "M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2",
  "parserfixed_run_id": "$PARSERFIXED_RUN_ID",
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

## Conditions For PM To Authorize Eval Later

PM can authorize mini-swe eval only after durable evidence shows all applicable items:

- `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2` has completed or produced a PM-accepted checkpoint/model handoff.
- A complete checkpoint/model or served endpoint exists.
- If checkpoint form: config, tokenizer, weights/adapters, `trainer_state.json` and `all_results.json` or PM-approved replacements are present.
- If checkpoint form: a serving handoff exposes the model as a reachable endpoint.
- If endpoint form: `/models` or equivalent health check passes and a simple completion works.
- PM explicitly names the checkpoint/model or endpoint as eval-approved.
- Future mini-swe generated logs, predictions, results, metrics, run metadata, temporary datasets, caches, and intermediates are under `/home/xu.yang`.
- Existing required input exceptions are documented for any non-`/home/xu.yang` source/config inputs.

## Outputs To Verify After Future Authorized Eval

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/output/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/output/metrics_readiness.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/output/results.json, if scoring runs
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/output/trajectories/*.json or per-instance trajectory files
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/logs/mini_swe_stdout_stderr.log
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_parserfixed_eval_readiness_test2/metadata/run_metadata.json
```

Prediction fields:

```text
instance_id
model_name_or_path
model_patch
```

## Current Result

Result: `READY_PACKAGE_BLOCKED_NO_MODEL`

Reason: eval readiness is prepared for `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`, but dev_2 evidence currently has no LTP submit, no GPU/NCCL preflight, no SFT run, no checkpoint/model, and no served endpoint. No eval or GPU work was performed by test_2.
