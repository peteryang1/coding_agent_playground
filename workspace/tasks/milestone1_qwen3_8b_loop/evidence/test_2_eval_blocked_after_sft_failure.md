# Test 2 Eval Blocked After SFT Failure

Task ID: `M1-EVAL-BLOCKED-TEST2`
Owner: `intern_code_test_2`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_eval_blocked_after_sft_failure.md`
Timestamp: `2026-05-20T10:35:27Z`

## Task Attachment

- Registry entry: `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- Scope: convert current post-SFT-failure state into explicit eval blocker evidence and define exact unblock condition for mini-swe.
- Acceptance criteria: cite PR #18/#23 SFT blocked-with-final-evidence, explain why mini-swe cannot run without checkpoint/served endpoint, list accepted future model forms, and name next fields/files to verify when endpoint exists.
- Completion marker: blocked-with-final-evidence for the current no-model state. If a future eval PR is opened, it must cite task id `M1-EVAL-BLOCKED-TEST2`, owner `intern_code_test_2`, this evidence path, acceptance criteria, and completion marker.

## SFT Final Evidence Cited

PR #18:

- URL: `https://github.com/peteryang1/coding_agent_playground/pull/18`
- State: merged
- `mergedAt`: `2026-05-20T10:18:04Z`
- Merge commit: `1c3a3e23921dd3fc91b340f9b67f83c747d42948`
- Task: `M1-SFT-SMOKE-DEV4`
- Durable evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_smoke_run.md`
- Completion marker recorded in task registry: blocked-with-final-evidence.

PR #23:

- URL: `https://github.com/peteryang1/coding_agent_playground/pull/23`
- State: merged
- `mergedAt`: `2026-05-20T10:20:28Z`
- Merge commit: `3ccabb573aecccdb71fe8d296643e6816b3ed22e`
- Title: `【milestone1_qwen3_8b_loop】【intern_code_dev_4】Record PR 18 completion`
- Body records task `M1-SFT-SMOKE-DEV4`, owner `intern_code_dev_4`, durable evidence `evidence/dev_4_sft_smoke_run.md`, and completion marker blocked-with-final-evidence.

SFT failure facts from `dev_4_sft_smoke_run.md`:

- Attempt 2 reached training with 10 examples, clean-base Qwen3 config, 8 distributed H200 tasks, and total optimization steps = 2, then failed with `ZeroDivisionError` from `steps_in_epoch=0`.
- Attempt 3 bounded TP=8/max_steps=1 retry failed Megatron scheduler assertion `lr_warmup_steps < lr_decay_steps`.
- No checkpoint directory with model files was produced.
- No `trainer_state.json` was produced.
- No `all_results.json` was produced.
- Dev_4 final recommendation: no further retry without a new PM-approved MCA/Megatron tiny-data config fix and resource plan.

## Why Mini-SWE Cannot Run Now

mini-swe-agent evaluates a callable model, not a training attempt. The current SFT smoke produced command/log/manifest evidence but produced no model artifact that can be loaded or served.

Current missing prerequisite:

```text
No SFT checkpoint/model directory
No final exported model path
No served endpoint model name
No OpenAI-compatible endpoint/base URL for the SFT smoke model
```

Therefore, running mini-swe now would either:

- evaluate the wrong model, such as a base model or historical checkpoint not produced by the current SFT smoke;
- fail before predictions because `--model` cannot resolve to a served model;
- produce non-actionable infrastructure/auth errors instead of Milestone 1 SFT-eval evidence.

This blocks mini-swe smoke execution. The prepared mini-swe backend remains ready at the command/config level in `evidence/test_2_eval_validation.md`, but execution is blocked until an accepted model form exists.

## Exact Unblock Condition

`M1-EVAL-BLOCKED-TEST2` unblocks only when one of the following accepted model forms is provided in durable evidence.

Accepted form A: served endpoint for the SFT smoke model.

Required fields:

```text
SFT_SMOKE_MODEL=<mini-swe/litellm-compatible model string>
OPENAI_BASE_URL=<OpenAI-compatible endpoint ending at or compatible with /v1>
OPENAI_API_KEY=<token, or explicit note that dummy token is accepted>
SFT_SMOKE_CHECKPOINT_PATH=<optional checkpoint/model path for provenance>
```

Accepted form B: raw checkpoint/model path plus serving instructions.

Required fields:

```text
SFT_SMOKE_CHECKPOINT_PATH=<readable HF-compatible checkpoint/model directory>
config.json exists
tokenizer_config.json or tokenizer.json exists
model weights exist (*.safetensors or pytorch_model*.bin)
serving command or endpoint handoff exists
served model string exists after serving
OPENAI_BASE_URL and auth/env values exist after serving
```

Raw checkpoint path alone is not enough for mini-swe because mini-swe-agent calls a model API through its model backend. The checkpoint must first be served or otherwise exposed as a mini-swe/litellm-compatible model string.

## Accepted Future Model Forms

Preferred:

- OpenAI-compatible endpoint serving the actual SFT smoke checkpoint.
- Model string usable by mini-swe-agent/litellm, for example `hosted_vllm/<served-model-name>` or another documented litellm-compatible identifier.
- Provenance includes the exact SFT run id, checkpoint/model path, serving command, endpoint URL, and model string.

Acceptable for a later PM-approved fallback:

- Historical or warm-start checkpoint served through the same endpoint mechanism, only if PM/supervisor explicitly records that this is not current clean-base SFT smoke output.
- Must be labeled in metrics/report as fallback or warm-start, not as current SFT smoke output.

Not accepted:

- A raw path with no serving endpoint.
- A base model path if the task is to evaluate SFT output.
- Historical mini-swe outputs under `/root/workspace/swe-bench-related/output` that predate this SFT smoke.
- A public model name not tied to the produced SFT smoke or an explicit PM-approved fallback.

## Next Fields And Files To Verify When Endpoint Exists

I will verify these fields before running mini-swe:

```text
task id: M1-EVAL-SMOKE-TEST2 or follow-up eval task id
owner: intern_code_test_2
SFT source PR(s): #18 and #23, plus any future retry PR
SFT run id
checkpoint/model path
checkpoint config/tokenizer/weights presence
served model name
OPENAI_BASE_URL
OPENAI_API_KEY presence or explicit no-auth note
mini-swe backend: singularity
mini-swe checkout sha and dirty provenance
runtime config path
output root
```

Files/paths to verify:

```text
/root/workspace/swe-bench-related/mini-swe-agent
/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/preds.json
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json
<checkpoint-path>/config.json
<checkpoint-path>/tokenizer_config.json or <checkpoint-path>/tokenizer.json
<checkpoint-path>/*.safetensors or <checkpoint-path>/pytorch_model*.bin
```

Prediction/result fields to verify after mini-swe run:

```text
instance_id
model_name_or_path
model_patch
trajectory path(s)
prediction path
results_json_path, if SWE-bench scoring runs
logs_path
total_instances
instances_submitted
instances_completed
instances_resolved
resolution_rate
status: passed, failed, blocked, or predictions_only
```

## Current Completion Marker

Blocked-with-final-evidence for current post-SFT-failure state.

Reason: PR #18/#23 establish that the SFT smoke is complete as blocked-with-final-evidence and produced no checkpoint/model/served endpoint. mini-swe execution cannot start without an accepted future model form above. The next unblock event is a future SFT retry/fallback evidence package that provides a served endpoint or a checkpoint plus serving handoff.
