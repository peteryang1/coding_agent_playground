# Test 1 SFT Retry Validation

Date: 2026-05-20

Task ID: `M1-SFT-RETRY-VALIDATE-TEST1`

Owner: `intern_code_test_1`

Scope: validate the proposed/run SFT retry against `evidence/test_1_sft_retry_gate.md`. This file records pre-run validation now and defines the post-run checks to apply after `intern_code_dev_4` records retry run evidence.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_sft_retry_validation.md`

## Sources Reviewed

- Retry gate: `evidence/test_1_sft_retry_gate.md`
- Prior failed smoke: `evidence/dev_4_sft_smoke_run.md`
- Config fix package: `evidence/dev_4_sft_config_fix_plan.md`
- Tiny-data config template: `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`
- Resource plan: `evidence/dev_2_gpu_retry_resource_plan.md`
- Data mitigation: `evidence/dev_3_sft_data_mitigation.md`
- Base path support: `evidence/dev_1_sft_base_path_support.md`
- Failure review: `evidence/dev_1_sft_failure_review.md`
- Task registry: `task_registry.md`

## Current Retry State

Current state: proposed retry package is available; no retry run has been recorded yet.

No `evidence/dev_4_sft_retry_run.md` file exists in the PM worktree at validation time, and no post-run artifacts were provided to test_1 for this assignment. Therefore this validation can only pass or block the pre-run package. It cannot mark the SFT retry itself complete, and it cannot allow mini-swe yet.

## Pre-Run Validation Summary

Result: **PRE-RUN PASS WITH RESOURCE PENDING**

The proposed retry package satisfies the config/data/base-model parts of `test_1_sft_retry_gate.md`, but a fresh GPU endpoint or current retry `nodes.json` is not active yet. PM can use this as test_1 pre-run gate evidence, but actual launch still requires dev_2 resource execution and dev_4 run evidence.

Mini-swe status: **BLOCKED** until a retry run produces a checkpoint/model or served endpoint and test_1 post-run validation passes.

## Task And Evidence Checks

Pass:

- Task registry contains `M1-SFT-RETRY-VALIDATE-TEST1`.
- Retry gate exists at `evidence/test_1_sft_retry_gate.md`.
- Config package exists at `evidence/dev_4_sft_config_fix_plan.md`.
- Resource plan exists at `evidence/dev_2_gpu_retry_resource_plan.md`.
- Data mitigation evidence exists at `evidence/dev_3_sft_data_mitigation.md`.
- Proposed dev_4 retry command names a unique run-id pattern:
  `milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_maxsteps2_<UTC>`.
- Proposed command is explicitly `DRY_RUN=0`.
- Proposed config path is explicit:
  `/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`.
- Proposed dataset path is explicit:
  `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Proposed base model path is explicit:
  `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.

Open:

- No fresh retry GPU endpoint is active yet.
- No current retry `nodes.json` has been produced by dev_2 yet.

## Dataset Checks

Result: **PASS for proposed original 10-example dataset**

Evidence:

- `dev_3_sft_input_handoff.md` records `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- SHA-256:
  `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`
- Count: 10 rows.
- Format: `coding_agent_playground_sft_v1`.
- Complete-process validation: 10 checked, 10 valid, 0 invalid.

Data mitigation note:

- `dev_3_sft_data_mitigation.md` also provides a repeated smoke-only artifact:
  `/root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/train.jsonl`
- Expanded count: 160.
- SHA-256:
  `f79d1e5843541faeb9789e4c4b24b10f1e10f60002af24173a9d039bcb370d87`
- Current dev_4 proposed command uses the original 10-example dataset, not the repeated artifact.
- This is acceptable for the proposed TP=8/DP=1 config because data parallel size should be 1; the repeated artifact remains a fallback if PM/dev_4 choose a data-side mitigation later.

Gate assertion:

```text
dataset_ok_for_proposed_retry=true
dataset_path=/root/workspace/cleaned_m1_sft_10/train.jsonl
dataset_sha256=5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
```

## Base Model Checks

Result: **PASS by evidence**

Accepted clean-base candidate:

```text
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

Evidence from `dev_1_sft_base_path_support.md`:

- Complete HF-style Qwen3 8B model layout.
- Contains `config.json`, tokenizer files, `model.safetensors.index.json`, and 5 safetensor shards.
- Config: `model_type=qwen3`, `architectures=['Qwen3ForCausalLM']`, `num_hidden_layers=36`, `hidden_size=4096`, `vocab_size=151936`.
- No training/adapter marker files found.

Gate assertion:

```text
base_model_ok_for_proposed_retry=true
base_model=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
clean_base_classification=clean-base candidate
```

## Config Checks

Result: **PASS for proposed tiny-data-safe config package**

Config template:

```text
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
```

Relevant config values:

```yaml
per_device_train_batch_size: 1
gradient_accumulation_steps: 1
max_steps: 2
warmup_steps: 0
save_steps: 1
logging_steps: 1
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
context_parallel_size: 1
sequence_parallel: false
```

Data-parallel safety reasoning:

- Expected single-node GPU count: 8.
- Tensor model parallel size: 8.
- Pipeline model parallel size: 1.
- Context parallel size: 1.
- Expected data parallel size: 1.
- Dataset examples: 10.
- With DP=1, the 10-example dataset is not split across 8 data-parallel ranks.
- This directly avoids the previous DP=8 tiny-data `steps_in_epoch=0` failure.

Scheduler safety reasoning:

- `max_steps=2`.
- `warmup_steps=0`.
- Required invariant: `lr_warmup_steps < lr_decay_steps`.
- Proposed relation: `0 < 2`.
- This directly avoids the previous TP=8/max_steps=1 scheduler assertion shape.

Checkpoint/metrics safety:

- `save_steps=1`, compatible with `max_steps=2`.
- `logging_steps=1`, compatible with `max_steps=2`.
- `save_total_limit=2`.
- `save_only_model=true` and `save_hf_model=true` are present.

Gate assertion:

```text
config_ok_for_pre_run=true
avoids_prior_dp8_failure=true
avoids_prior_tp8_scheduler_shape=true
expected_dp=1
warmup_less_than_decay=true
save_steps_within_smoke=true
```

## Resource Checks

Result: **PLAN PASS, EXECUTION PENDING**

Resource plan evidence:

- `dev_2_gpu_retry_resource_plan.md`
- Prior H200 allocation is recorded as STOPPED / Completed.
- Prior endpoint `ssh -p 39314 root@10.100.20.37` must be treated as released and unavailable.
- Plan requires a fresh single-node 8xH200 LTP job after PM gate.
- Plan requires endpoint verification with `nvidia-smi`.
- Plan requires output preservation under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.

Gate assertion:

```text
resource_plan_ok=true
fresh_resource_active=false
launch_authorized_by_test1=false
```

Interpretation:

The resource plan satisfies the planning part of the retry gate, but there is no current endpoint for dev_4 to run against. PM should not treat this as a runnable SFT retry until dev_2 creates and records a fresh endpoint or current retry `nodes.json`.

## Proposed Retry Command Check

Result: **PASS for command shape, pending concrete endpoint**

Proposed command from dev_4:

```bash
cd /root/workspace/coding_agent_playground
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_maxsteps2_$(date -u +%Y%m%dT%H%M%SZ) \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Checks:

- `DRY_RUN=0`: pass.
- Unique `RUN_ID`: pass by timestamped pattern.
- `CONFIG_TEMPLATE`: pass, points to the new tiny-data-safe template.
- `DATASET_JSONL`: pass, points to the validated 10-example file.
- `BASE_MODEL`: pass, points to clean-base candidate from dev_1 evidence.
- `OUTPUT_ROOT`: pass, durable `/mnt/3fs` path.
- `LLAMAFACTORY_DIR`: pass if materialized on the fresh endpoint by dev_4 setup.

Open item:

- The command cannot be run yet without a fresh GPU endpoint/node.

## Post-Run Validation Status

Result: **NOT RUN / PENDING**

No post-run validation can be completed yet because no `dev_4_sft_retry_run.md` or retry run artifacts exist.

Required post-run evidence after dev_4 runs:

- exact endpoint and run ID,
- exact command and exit status,
- run manifest path,
- copied runtime config path,
- stdout/stderr log path,
- checkpoint/model path or explicit absence,
- `trainer_state.json` and/or `all_results.json` path,
- first failing exception if failed,
- GPU cleanup/resource state.

Required log assertions:

- Must not contain:
  - `ZeroDivisionError: division by zero`
  - `steps_in_epoch`
  - `self.state.epoch = epoch + (...) / steps_in_epoch`
  - `optimizer_param_scheduler.py`
  - `assert self.lr_warmup_steps < self.lr_decay_steps`
  - `Cannot open data/sft/dataset_info.json`
- PASS must show at least one training step and a checkpoint/model or usable metrics.

## Mini-swe Decision

Current result: **mini-swe must not proceed yet**

Reason:

- There is no retry-produced checkpoint/model.
- There is no retry `trainer_state.json`, `all_results.json`, or accepted model endpoint.
- `M1-EVAL-SMOKE-TEST2` remains blocked by absent SFT checkpoint/endpoint.

PM can allow mini-swe only after:

1. dev_2 provides a fresh endpoint/current retry resource evidence.
2. dev_4 runs the retry and records durable run evidence.
3. test_1 post-run validation confirms PASS against `test_1_sft_retry_gate.md`.
4. A mini-swe-usable checkpoint/model path or served endpoint exists.

## Overall Validation Result

```text
task_id: M1-SFT-RETRY-VALIDATE-TEST1
pre_run_validation: PASS_WITH_RESOURCE_PENDING
post_run_validation: PENDING_NO_RUN_EVIDENCE
mini_swe_can_proceed: false
blocking_reason: no retry run artifact/checkpoint/model yet
```

## Completion Marker

This file completes the pre-run validation portion of `M1-SFT-RETRY-VALIDATE-TEST1`.

The task should remain open or marked `pre-run-pass/post-run-pending` in `task_registry.md` until dev_4 produces retry run evidence and test_1 records the post-run PASS/FAIL result.
