# Test 2 Session 21 Mini-SWE Eval Package

Task ID: `M1-S21-EVAL-PACKAGE-TEST2`  
Owner: `intern_code_test_2`  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s21_eval_package.md`  
Timestamp: `2026-05-21T07:21:38Z`

## Task Attachment

- Registry: `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- Scope: prepare mini-swe smoke package for the SFT checkpoint or served endpoint produced by Session 21 runtime task `M1-S21-RUNTIME-DEV2`.
- Acceptance criteria: evidence names accepted checkpoint/endpoint forms, env vars, command template, predictions/results/metrics paths, provenance fields, and current blocker until checkpoint exists.
- PR rule: no eval PR until model/endpoint exists. Any future PR must cite task id `M1-S21-EVAL-PACKAGE-TEST2`, owner `intern_code_test_2`, this evidence path, acceptance criteria, and completion marker.
- Execution rule: do not run eval until PM gates a checkpoint or served endpoint.

## Current Blocker

Status: `BLOCKED`

Reason: `M1-S21-RUNTIME-DEV2` has not produced a checkpoint/model or served endpoint. Current task registry state says `M1-S21-RUNTIME-DEV2` is blocked-pre-submit: PM runtime authorization is not recorded and no fresh Session 21 LTP frame/node/endpoint/nodes.json exists.

No mini-swe eval was run for this package.

## Accepted Runtime Outputs

Accepted form A: served endpoint from Session 21 SFT runtime.

```text
S21_SFT_RUN_ID=<run id from M1-S21-RUNTIME-DEV2>
S21_SFT_MODEL=<mini-swe/litellm-compatible served model id>
OPENAI_BASE_URL=<OpenAI-compatible base URL, usually ending in /v1>
OPENAI_API_KEY=<token, or explicit durable no-auth/dummy-token note>
S21_SFT_CHECKPOINT_PATH=<optional checkpoint/model path for provenance>
S21_SERVING_OWNER=<owner of serving process>
S21_SERVING_COMMAND_OR_MANIFEST=<durable command/manifest/path>
```

Accepted form B: checkpoint/model path plus serving handoff.

```text
S21_SFT_RUN_ID=<run id from M1-S21-RUNTIME-DEV2>
S21_SFT_CHECKPOINT_PATH=<readable HF-compatible checkpoint/model directory>
config.json exists
tokenizer_config.json or tokenizer.json exists
model weights exist (*.safetensors or pytorch_model*.bin)
serving command or manifest exists
S21_SFT_MODEL=<model id exposed after serving>
OPENAI_BASE_URL=<served OpenAI-compatible /v1 endpoint>
OPENAI_API_KEY=<token/no-auth note>
```

Not accepted:

- Raw checkpoint path without a serving endpoint/handoff.
- Base Qwen3-8B or historical checkpoint unless PM explicitly records a fallback decision.
- Any endpoint/model id not tied to `M1-S21-RUNTIME-DEV2` output or PM-approved fallback.
- Historical mini-swe predictions from prior sessions.

## Pre-Run Env And Config Checks

Run these only after PM gates a Session 21 checkpoint or endpoint.

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
test -d /root/workspace/swe-bench-related/mini-swe-agent
test -d /root/workspace/swe-bench-related/SWE-bench
test -f /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
command -v uv
command -v singularity
singularity --version
uv run --with datasets mini-extra swebench --help >/tmp/m1_s21_mini_swe_help.out
test -n "${S21_SFT_RUN_ID:-}"
test -n "${S21_SFT_MODEL:-}"
test -n "${OPENAI_BASE_URL:-}"
python3 - <<PY
import os
for key in [
    "S21_SFT_RUN_ID",
    "S21_SFT_MODEL",
    "OPENAI_BASE_URL",
    "S21_SFT_CHECKPOINT_PATH",
    "S21_SERVING_OWNER",
    "S21_SERVING_COMMAND_OR_MANIFEST",
]:
    print(f"{key}={os.environ.get(key, '')}")
print("OPENAI_API_KEY_present=", bool(os.environ.get("OPENAI_API_KEY")))
PY'
```

If checkpoint path is part of the handoff:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
test -n "${S21_SFT_CHECKPOINT_PATH:-}"
test -d "$S21_SFT_CHECKPOINT_PATH"
test -f "$S21_SFT_CHECKPOINT_PATH/config.json"
test -f "$S21_SFT_CHECKPOINT_PATH/tokenizer_config.json" || test -f "$S21_SFT_CHECKPOINT_PATH/tokenizer.json"
find "$S21_SFT_CHECKPOINT_PATH" -maxdepth 1 \( -name "*.safetensors" -o -name "pytorch_model*.bin" \) | head -1 | grep -q .'
```

Endpoint reachability check:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
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

## Command Template

Two-instance Session 21 mini-swe smoke:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
export S21_SFT_RUN_ID="<s21-runtime-run-id>"
export S21_SFT_MODEL="<served-litellm-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"
export S21_SFT_CHECKPOINT_PATH="<optional-checkpoint-path-for-provenance>"
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s21_eval_package_test2
OUT="$EVAL_ROOT/output/qwen3_8b_s21_eval_smoke"
export TMPDIR="$EVAL_ROOT/tmp"
export HF_HOME="$EVAL_ROOT/hf_home"
export HF_DATASETS_CACHE="$EVAL_ROOT/hf_datasets_cache"
export UV_CACHE_DIR="$EVAL_ROOT/uv_cache"
export APPTAINER_CACHEDIR="$EVAL_ROOT/apptainer_cache"
mkdir -p "$OUT"
uv run --with datasets mini-extra swebench \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --slice 0:2 \
  --model "$S21_SFT_MODEL" \
  --environment-class singularity \
  --workers 1 \
  --output "$OUT"'
```

Single-instance debug fallback:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
export S21_SFT_MODEL="<served-litellm-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s21_eval_package_test2
OUT="$EVAL_ROOT/output/qwen3_8b_s21_eval_smoke"
export TMPDIR="$EVAL_ROOT/tmp"
export HF_HOME="$EVAL_ROOT/hf_home"
export HF_DATASETS_CACHE="$EVAL_ROOT/hf_datasets_cache"
export UV_CACHE_DIR="$EVAL_ROOT/uv_cache"
export APPTAINER_CACHEDIR="$EVAL_ROOT/apptainer_cache"
mkdir -p "$OUT"
uv run --with datasets mini-extra swebench-single \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --instance 0 \
  --model "$S21_SFT_MODEL" \
  --environment-class singularity \
  --exit-immediately \
  --output "$OUT/single_instance_0.traj.json"'
```

## Predictions / Results / Metrics Paths

Storage rule effective immediately:

- Default all future mini-swe eval logs, predictions, metrics, run metadata, temporary datasets, caches, and intermediates to CephFS under `/home/xu.yang`.
- Current default eval root for this task: `/home/xu.yang/milestone1_qwen3_8b_loop/m1_s21_eval_package_test2`.
- Existing required path exception: `/root/workspace/swe-bench-related/mini-swe-agent` remains the required mini-swe source checkout for command execution.
- Existing required path exception: `/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml` remains the required mini-swe/SWE-bench config path.
- Exception justification: those `/root/workspace/...` paths are pre-existing required source/config inputs on the corrected final workspace; generated eval artifacts, logs, predictions, metrics, metadata, temporary datasets, and caches must not default there.

Expected output root:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s21_eval_package_test2/output/qwen3_8b_s21_eval_smoke
```

Verify after run:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s21_eval_package_test2/output/qwen3_8b_s21_eval_smoke/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s21_eval_package_test2/output/qwen3_8b_s21_eval_smoke/metrics_readiness.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s21_eval_package_test2/output/qwen3_8b_s21_eval_smoke/results.json, if SWE-bench scoring runs
trajectory JSON files under output root or per-instance subdirectories
mini-swe logs with no infrastructure/auth/Singularity traceback
```

Prediction fields:

```text
instance_id
model_name_or_path
model_patch
```

Metrics schema:

```json
{
  "task_id": "M1-S21-EVAL-PACKAGE-TEST2",
  "s21_sft_run_id": "<S21_SFT_RUN_ID>",
  "model_name_or_path": "<S21_SFT_MODEL>",
  "checkpoint_path": "<S21_SFT_CHECKPOINT_PATH or empty>",
  "agent": "mini-swe-agent",
  "backend": "singularity",
  "benchmark": "SWE-bench lite dev slice 0:2",
  "total_instances": 2,
  "instances_submitted": 2,
  "instances_completed": 0,
  "instances_resolved": 0,
  "resolution_rate": 0.0,
  "predictions_path": "<path>",
  "results_json_path": "<path or empty>",
  "logs_path": "<path>",
  "status": "<PASS|FAIL|BLOCKED|PREDICTIONS_ONLY>",
  "blockers": []
}
```

## Provenance Fields

Record these with any eventual run:

```text
task_id: M1-S21-EVAL-PACKAGE-TEST2
owner: intern_code_test_2
runtime_source_task: M1-S21-RUNTIME-DEV2
runtime_owner: intern_code_dev_2
S21_SFT_RUN_ID
S21_SFT_CHECKPOINT_PATH
S21_SFT_MODEL
OPENAI_BASE_URL
serving owner/command/manifest
mini-swe checkout path
mini-swe git sha
mini-swe dirty files/diff provenance
runtime config path
backend: singularity
dataset subset/split/slice
output root
```

Known mini-swe provenance from prior checks:

```text
path: /root/workspace/swe-bench-related/mini-swe-agent
git sha previously observed: 0e47fb4
dirty files previously observed:
  M src/minisweagent/environments/apptainer.py
  ?? uv.lock
```

Before execution, re-check the mini-swe git sha and dirty state and record the exact current values.

## PASS / FAIL / BLOCKED Criteria

PASS:

- PM-gated Session 21 checkpoint or served endpoint exists.
- Pre-run env/config and endpoint checks pass.
- mini-swe two-instance command exits without infrastructure/auth/dataset/Singularity traceback.
- Predictions file exists and contains records for the smoke slice.
- Each prediction has `instance_id`, `model_name_or_path`, and `model_patch`.
- Metrics JSON is written with paths and status `PASS`, or `PREDICTIONS_ONLY` if scoring is explicitly deferred.

FAIL:

- PM-gated endpoint/model exists but mini-swe cannot produce predictions because of model/API/config failure.
- Dataset loading, Singularity, or mini-swe infrastructure fails after pre-run checks.
- Predictions are missing or malformed.
- Metrics JSON is missing after an attempted run.

BLOCKED:

- No PM-gated checkpoint/model/served endpoint exists.
- Raw checkpoint exists but no serving handoff exists.
- Endpoint is unreachable from corrected final workspace.
- Required env vars/model id are absent.
- Checkpoint path lacks config/tokenizer/weights.

## Current Result

Status: `POST_RUN_BLOCKED`

Reason: `M1-S21-RUNTIME-DEV2` produced final runtime evidence, but it did not produce a complete checkpoint/model or served endpoint. This package is ready for use once PM gates a future Session 21 model artifact or endpoint, but eval must not run before that gate.

## 2026-05-21T07:46:12Z - PM Eval Gate Update / POST_RUN_BLOCKED

Source evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s21_sft_runtime.md` for runtime task `M1-S21-RUNTIME-DEV2`.

Runtime facts now gating eval:

- `EXIT_STATUS=1`.
- The SFT run reached data loading, ShareGPT conversion, training progress, and attempted `checkpoint-1` save.
- The checkpoint save failed during safetensors serialization with `No space left on device (os error 28)`.
- Partial `checkpoint-1` artifacts exist, but they are not a complete checkpoint/model and must not be used for eval.
- `trainer_state.json` is absent.
- `all_results.json` is absent.
- No eval-approved model id, complete checkpoint path, or served endpoint exists.

Eval decision:

- Status is `POST_RUN_BLOCKED`.
- Do not run mini-swe against partial `checkpoint-1`.
- Do not run mini-swe until PM gates either a complete checkpoint/model plus serving handoff, or a reachable served endpoint.

Why partial `checkpoint-1` is rejected:

- The save failed before full serialization completed.
- Required run completion files are absent (`trainer_state.json`, `all_results.json`).
- There is no PM-approved eval handoff naming this partial directory as a valid model.
- There is no served endpoint/model id backed by this checkpoint.

Exact unblock condition:

- Future runtime evidence must provide one accepted model form:
  - a reachable OpenAI-compatible endpoint with `OPENAI_BASE_URL`, optional `OPENAI_API_KEY`, concrete `MODEL_NAME`, health check result, serving owner, and serving command/manifest; or
  - a complete checkpoint/model directory with config, tokenizer, full weights, provenance, and an explicit serving handoff that exposes it through a reachable endpoint.
- Future runtime evidence should also include completion/provenance fields when available: run id, checkpoint path, base model, adapter/full-model status, `trainer_state.json`, `all_results.json` or accepted replacement metrics, disk/output path note, and PM gate approval.

Fields/files to verify once a model exists:

- Endpoint: `OPENAI_BASE_URL`, `OPENAI_API_KEY` if required, `MODEL_NAME`, health response, simple completion response, serving owner/command/log path.
- Checkpoint: config files, tokenizer files, complete weight shards or adapter files, shard index if present, no interrupted save marker, readable path on corrected final workspace.
- Runtime completion: `trainer_state.json`, `all_results.json` or PM-approved replacement metrics, final exit status, run id, source task id.
- Eval outputs: `preds.json`, `metrics_readiness.json`, optional `results.json`, per-instance trajectory/log files, and prediction fields `instance_id`, `model_name_or_path`, `model_patch`.

## 2026-05-21T08:06:07Z - Storage Rule Update

Supervisor storage rule now applies to this task:

- Future mini-swe eval logs, predictions, metrics, run metadata, temporary datasets, caches, and intermediates default to CephFS under `/home/xu.yang`.
- Updated command templates now use `/home/xu.yang/milestone1_qwen3_8b_loop/m1_s21_eval_package_test2` as the task eval root.
- Updated command templates set `TMPDIR`, `HF_HOME`, `HF_DATASETS_CACHE`, `UV_CACHE_DIR`, and `APPTAINER_CACHEDIR` under that CephFS eval root.
- Existing required path exception: use `/root/workspace/swe-bench-related/mini-swe-agent` only for the pre-existing mini-swe source checkout.
- Existing required path exception: use `/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml` only for the pre-existing runtime config.
- Exception justification: these `/root/workspace/...` paths are required source/config inputs on the corrected final workspace; generated eval artifacts and temporary data must default to CephFS.

Execution status remains `POST_RUN_BLOCKED`: no PM-gated complete checkpoint/model or served endpoint exists, partial `checkpoint-1` remains rejected, and no eval was run.
