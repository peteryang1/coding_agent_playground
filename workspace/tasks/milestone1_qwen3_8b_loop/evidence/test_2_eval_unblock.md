# Test 2 Mini-SWE Eval Unblock

Task ID: `M1-EVAL-UNBLOCK-TEST2`  
Owner: `intern_code_test_2`  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_eval_unblock.md`  
Timestamp: `2026-05-20T11:04:50Z`

## Task Attachment

- Registry: `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- Scope: prepare and, once a checkpoint/served endpoint exists, run or gate the mini-swe smoke unblock path.
- Acceptance criteria: evidence must name accepted endpoint/checkpoint+serving handoff, env vars/model id, command, predictions/results path, metrics, and PASS/FAIL or explicit blocker.
- PR rule: no eval PR until model/endpoint exists. Any future PR must cite task id `M1-EVAL-UNBLOCK-TEST2`, owner `intern_code_test_2`, this evidence path, acceptance criteria, and completion marker.
- Completion marker: blocked until dev_4 produces checkpoint or served endpoint; then mark PASS/FAIL/blocked-with-final-evidence after gate execution.

## Current State

Blocked. Dev_4 has not yet provided a mini-swe-usable SFT checkpoint/model or served endpoint for the retry path.

Current upstream state from task registry:

- `M1-SFT-SMOKE-DEV4`: blocked-with-final-evidence; PR #18 and PR #23 are merged, but no checkpoint/model was produced.
- `M1-SFT-CONFIG-FIX-DEV4`: ready-for-retry; PR #26 and PR #27 are merged with a tiny-data-safe config package, but no retry run output exists yet.
- `M1-SFT-RETRY-RUN-DEV4`: open; dev_4 waits for a fresh endpoint/node before executing retry and recording output.
- `M1-EVAL-UNBLOCK-TEST2`: open; blocked until checkpoint or served endpoint exists.

## Accepted Endpoint / Checkpoint + Serving Handoff

Accepted endpoint form:

```text
SFT_SMOKE_MODEL=<litellm/mini-swe compatible model id>
OPENAI_BASE_URL=<OpenAI-compatible base URL, typically ending in /v1>
OPENAI_API_KEY=<token, or explicit durable note that dummy token is accepted>
SFT_SMOKE_CHECKPOINT_PATH=<optional durable checkpoint/model path for provenance>
SFT_SMOKE_RUN_ID=<SFT retry run id>
```

Accepted checkpoint+serving handoff form:

```text
SFT_SMOKE_CHECKPOINT_PATH=<readable HF-compatible checkpoint/model directory>
SFT_SMOKE_RUN_ID=<SFT retry run id>
serving_command=<exact command or durable handoff that serves the checkpoint>
SFT_SMOKE_MODEL=<model id exposed by the serving process>
OPENAI_BASE_URL=<served OpenAI-compatible /v1 endpoint>
OPENAI_API_KEY=<token/no-auth note>
```

Checkpoint-only is not accepted for mini-swe execution. It must be served first because mini-swe-agent calls a model API through its backend.

## Required Pre-Run Env/Config Gate

Run only after dev_4 provides endpoint or checkpoint+serving handoff:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
test -d /root/workspace/swe-bench-related/mini-swe-agent
test -d /root/workspace/swe-bench-related/SWE-bench
test -f /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
command -v uv
command -v singularity
singularity --version
uv run --with datasets mini-extra swebench --help >/tmp/m1_eval_unblock_help.out
test -n "${SFT_SMOKE_MODEL:-}"
test -n "${OPENAI_BASE_URL:-}"
python3 - <<PY
import os
print("SFT_SMOKE_RUN_ID=", os.environ.get("SFT_SMOKE_RUN_ID", ""))
print("SFT_SMOKE_MODEL=", os.environ.get("SFT_SMOKE_MODEL", ""))
print("OPENAI_BASE_URL=", os.environ.get("OPENAI_BASE_URL", ""))
print("OPENAI_API_KEY_present=", bool(os.environ.get("OPENAI_API_KEY")))
print("SFT_SMOKE_CHECKPOINT_PATH=", os.environ.get("SFT_SMOKE_CHECKPOINT_PATH", ""))
PY'
```

If a checkpoint path is part of the handoff:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
test -n "${SFT_SMOKE_CHECKPOINT_PATH:-}"
test -d "$SFT_SMOKE_CHECKPOINT_PATH"
test -f "$SFT_SMOKE_CHECKPOINT_PATH/config.json"
test -f "$SFT_SMOKE_CHECKPOINT_PATH/tokenizer_config.json" || test -f "$SFT_SMOKE_CHECKPOINT_PATH/tokenizer.json"
find "$SFT_SMOKE_CHECKPOINT_PATH" -maxdepth 1 \( -name "*.safetensors" -o -name "pytorch_model*.bin" \) | head -1 | grep -q .'
```

Endpoint reachability check:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
test -n "${OPENAI_BASE_URL:-}"
python3 - <<PY
import os, urllib.request
base = os.environ["OPENAI_BASE_URL"].rstrip("/")
req = urllib.request.Request(base + "/models")
if os.environ.get("OPENAI_API_KEY"):
    req.add_header("Authorization", "Bearer " + os.environ["OPENAI_API_KEY"])
with urllib.request.urlopen(req, timeout=15) as r:
    print(r.status)
    print(r.read(4096).decode("utf-8", errors="replace"))
PY'
```

## Mini-SWE Command

Two-instance unblock smoke:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
export SFT_SMOKE_RUN_ID="<sft-retry-run-id>"
export SFT_SMOKE_MODEL="<served-litellm-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"
export SFT_SMOKE_CHECKPOINT_PATH="<optional-checkpoint-path-for-provenance>"
OUT=/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
mkdir -p "$OUT"
uv run --with datasets mini-extra swebench \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --slice 0:2 \
  --model "$SFT_SMOKE_MODEL" \
  --environment-class singularity \
  --workers 1 \
  --output "$OUT"'
```

Single-instance debug fallback:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
export SFT_SMOKE_MODEL="<served-litellm-model-id>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-no-auth>"
OUT=/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
mkdir -p "$OUT"
uv run --with datasets mini-extra swebench-single \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --instance 0 \
  --model "$SFT_SMOKE_MODEL" \
  --environment-class singularity \
  --exit-immediately \
  --output "$OUT/single_instance_0.traj.json"'
```

## Prediction / Result / Metrics Paths

Expected output root:

```text
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
```

Verify:

```text
trajectory JSON files under output root or per-instance subdirectories
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/preds.json or equivalent prediction file
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json
results.json or equivalent SWE-bench result file if local scoring runs
mini-swe logs with no infrastructure/auth/Singularity traceback
```

Prediction fields:

```text
instance_id
model_name_or_path
model_patch
```

Metrics fields:

```json
{
  "task_id": "M1-EVAL-UNBLOCK-TEST2",
  "sft_run_id": "<SFT_SMOKE_RUN_ID>",
  "model_name_or_path": "<SFT_SMOKE_MODEL>",
  "checkpoint_path": "<SFT_SMOKE_CHECKPOINT_PATH or empty>",
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

## PASS / FAIL / BLOCKER Criteria

PASS:

- Dev_4 provides accepted endpoint or checkpoint+serving handoff.
- Env/config gate passes on corrected final workspace.
- Endpoint `/models` or equivalent health/model check is reachable.
- mini-swe two-instance command exits without infrastructure/auth/dataset/Singularity traceback.
- Prediction file exists and contains two records for the smoke slice.
- Every prediction has `instance_id`, `model_name_or_path`, and `model_patch`.
- Metrics/readiness JSON is written with artifact paths and status `PASS` or `PREDICTIONS_ONLY` if SWE-bench scoring is explicitly deferred.

FAIL:

- Provided endpoint/model id exists but mini-swe cannot produce predictions due to model/API/config failure.
- Singularity or dataset startup fails after pre-run gate appeared valid.
- Predictions file is missing or malformed.
- Metrics/readiness JSON is missing after an attempted run.

BLOCKED:

- No checkpoint/model/served endpoint exists.
- Raw checkpoint is provided without serving handoff.
- Endpoint is unreachable from corrected final workspace.
- Required env vars or model id are absent.
- Checkpoint path lacks config/tokenizer/weights.

## Current Result

Status: `BLOCKED`

Reason: no checkpoint/model/served endpoint from the SFT retry exists yet. The unblock command/gate is ready and will be executed only after dev_4 records an accepted endpoint or checkpoint+serving handoff.
