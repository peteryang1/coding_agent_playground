# Test 2 Eval Blocked After Retry Failure

Task ID: `M1-EVAL-BLOCKED-REFRESH-TEST2`  
Owner: `intern_code_test_2`  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_eval_blocked_after_retry_failure.md`  
Timestamp: `2026-05-20T12:03:49Z`

## Task Attachment

- Registry: `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- Scope: refresh mini-swe blocked/unblock evidence after the `KeyError: 'from'` SFT retry failure.
- Acceptance criteria: cite latest SFT retry failure/no-checkpoint facts, state why mini-swe cannot run, keep accepted future endpoint/checkpoint forms current, and list exact fields to validate once a checkpoint or served endpoint exists.
- PR rule: no eval PR until a model/endpoint exists. Any future PR must cite task id `M1-EVAL-BLOCKED-REFRESH-TEST2` or the active eval task id, owner `intern_code_test_2`, durable evidence path, acceptance criteria, and completion marker.
- Completion marker for this update: blocked-with-final-evidence for the current no-model/no-endpoint state.

## Latest SFT Retry Facts

Current task-registry facts for `M1-SFT-RETRY-RUN-DEV4`:

- PR #30 exists for the SFT retry evidence, but after PM PR #33 advanced `main`, GitHub reports `CONFLICTING` / `DIRTY`; dev_4 must refresh before PM gate.
- The retry ran once and failed with `KeyError: 'from'`.
- No checkpoint/model was produced.
- No `trainer_state.json` was produced.
- No `all_results.json` was produced.
- No further retry is authorized.

Current history facts:

- The authorized retry reached LLamaFactory distributed launch.
- The failure occurred during dataset conversion with `KeyError: 'from'`.
- The prior DP=8 `steps_in_epoch=0` and TP=8 one-step scheduler assertion were not the failure signatures for this retry.
- The current blocker is OpenAI-style `role`/`content` data being registered with ShareGPT defaults expecting `from`/`value`.

## Why Mini-SWE Cannot Run

mini-swe-agent requires a callable model target. For this milestone, the model target must be the SFT retry output or an explicitly accepted fallback served as an endpoint.

The latest SFT retry did not produce any mini-swe-usable model artifact:

```text
No retry checkpoint/model directory
No final exported model path
No served SFT endpoint
No SFT model id
No OpenAI-compatible base URL for the SFT retry model
```

Running mini-swe now would not test the milestone SFT retry. It would either evaluate the wrong model, fail before predictions because the model id/endpoint is absent, or produce infrastructure/auth errors unrelated to SFT quality. Therefore eval remains blocked.

## Accepted Future Endpoint / Checkpoint Forms

Accepted form A: served endpoint for the actual SFT retry output.

Required durable fields:

```text
SFT_RETRY_RUN_ID=<dev_4 retry run id>
SFT_SMOKE_MODEL=<mini-swe/litellm-compatible served model id>
OPENAI_BASE_URL=<OpenAI-compatible endpoint, typically ending in /v1>
OPENAI_API_KEY=<token, or explicit no-auth/dummy-token note>
SFT_SMOKE_CHECKPOINT_PATH=<checkpoint/model path for provenance, if available>
serving_owner=<owner who started/owns endpoint>
serving_command_or_manifest=<exact command/manifest/path>
```

Accepted form B: checkpoint/model path plus serving handoff.

Required durable fields:

```text
SFT_RETRY_RUN_ID=<dev_4 retry run id>
SFT_SMOKE_CHECKPOINT_PATH=<readable HF-compatible checkpoint/model directory>
config.json exists
tokenizer_config.json or tokenizer.json exists
model weights exist (*.safetensors or pytorch_model*.bin)
serving command or manifest exists
served model id exists after serving
OPENAI_BASE_URL exists after serving
OPENAI_API_KEY or no-auth note exists after serving
```

Not accepted:

- Raw checkpoint path with no serving endpoint/handoff.
- Base Qwen3-8B model when the requested target is SFT retry output.
- Historical mini-swe output or predictions from before this retry.
- Any endpoint/model id not tied to the SFT retry run id or an explicit PM-approved fallback.

## Fields To Validate When A Model Exists

Before mini-swe execution, test_2 will validate:

```text
task_id
owner
SFT retry PR id and merge/gate state
SFT_RETRY_RUN_ID
checkpoint/model path
checkpoint config/tokenizer/weights
served model id
OPENAI_BASE_URL
OPENAI_API_KEY presence or no-auth note
serving command/manifest
serving owner
mini-swe checkout sha
mini-swe dirty checkout provenance
runtime config path
backend: singularity
output root
```

Expected local paths on corrected final workspace:

```text
/root/workspace/swe-bench-related/mini-swe-agent
/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/preds.json
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json
```

Expected prediction fields after mini-swe run:

```text
instance_id
model_name_or_path
model_patch
```

Expected metrics fields:

```text
task_id
sft_retry_run_id
model_name_or_path
checkpoint_path
agent
backend
benchmark
total_instances
instances_submitted
instances_completed
instances_resolved
resolution_rate
predictions_path
results_json_path
logs_path
status
blockers
```

## Current Result

Status: `BLOCKED`

Reason: the latest SFT retry failed with `KeyError: 'from'` during LLamaFactory dataset conversion and produced no checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, model id, or eval-ready artifact. Mini-swe remains blocked until a later SFT retry or approved fallback provides an accepted endpoint or checkpoint+serving handoff.
