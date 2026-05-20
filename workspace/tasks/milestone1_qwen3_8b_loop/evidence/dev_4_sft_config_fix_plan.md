# Dev 4 SFT Config Fix Plan

Owner: `intern_code_dev_4`  
Task ID: `M1-SFT-CONFIG-FIX-DEV4`  
Status: proposed config package, no GPU run authorized or attempted  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_config_fix_plan.md`

## Task Contract

- Scope: produce the next SFT unblock package after `M1-SFT-SMOKE-DEV4` was marked blocked-with-final-evidence.
- Acceptance criteria: cite prior run ids, root causes, proposed config diff/command, expected artifacts, rollback/stop conditions, and whether a fresh GPU run is justified.
- Completion marker for this package: ready-for-PM-gate once this evidence and the task-attached PR are present. No GPU execution is authorized until PM gates this package plus test/resource plans.

## Prior Runs Reviewed

Evidence source: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_smoke_run.md`.

| Run ID | Command Shape | Exit | Root Cause |
|--------|---------------|------|------------|
| `milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T093916Z` | baseline clean-base command | `1` | dataset registration missing at `data/sft/dataset_info.json`; fixed before later attempts |
| `milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z` | baseline DP=8, TP=1, 10 examples | `1` | MCA trainer/drop-last made per-rank effective epoch length zero, ending in `ZeroDivisionError` at `steps_in_epoch` |
| `milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z` | bounded TP=8, DP=1, `max_steps=1` | `1` | Megatron scheduler rejected the one-step schedule with `assert self.lr_warmup_steps < self.lr_decay_steps` |

## Root Cause Summary

- The base model, dataset, output root, LLamaFactory/MCA dependencies, and H200 route were usable.
- DP=8 is unsafe for the 10-example smoke data because MCA/drop-last can leave each data-parallel rank with zero trainable steps.
- TP=8 / DP=1 fixes the data-parallel zero-step issue, because tensor parallelism uses all 8 GPUs without splitting the 10 examples across 8 data-parallel workers.
- The failed TP=8 retry made the schedule too short: `max_steps=1` can collapse Megatron warmup/decay step accounting so the scheduler assertion fails.

## Proposed Patch

Add a dedicated tiny-data smoke template:

```text
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
```

Key differences from `configs/train/qwen3_8b_sft.yaml`:

```diff
- save_steps: 150
+ save_steps: 1
- per_device_train_batch_size: 1
- gradient_accumulation_steps: 4
- num_train_epochs: 2.0
- warmup_ratio: 0.03
- tensor_model_parallel_size: 1
+ per_device_train_batch_size: 1
+ gradient_accumulation_steps: 1
+ max_steps: 2
+ warmup_steps: 0
+ tensor_model_parallel_size: 8
```

Rationale:

- `tensor_model_parallel_size: 8` keeps `DP=1` on the single 8xH200 node and avoids the prior DP=8 zero-step failure.
- `max_steps: 2` gives Megatron at least two decay steps and avoids the prior one-step scheduler shape.
- `warmup_steps: 0` removes warmup/decay equality risk.
- `save_steps: 1` creates an early artifact opportunity for smoke verification.
- `gradient_accumulation_steps: 1` keeps the two-step smoke bounded and fast.

## Proposed No-Launch Command

This command is for PM-gated future execution only. Do not run it until PM also gates the test/resource plans.

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

Required pre-run checks:

```bash
nvidia-smi
test -f /root/workspace/cleaned_m1_sft_10/train.jsonl
test -f /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6/config.json
test -d /root/workspace/coding_agent_playground/code/LLamaFactory
test -w /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

## Expected Artifacts

For `RUN_ID=milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_maxsteps2_<UTC>`:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/run_manifest.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/trainer_state.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/all_results.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/checkpoint-*/
```

PASS for this retry should require either a checkpoint/model artifact or a clear new failure after passing the two previous failure points:

- no `steps_in_epoch=0` / division-by-zero failure;
- no `lr_warmup_steps < lr_decay_steps` assertion;
- durable logs and manifest exist.

## Rollback / Stop Conditions

- Stop immediately if pre-run checks fail.
- Stop after the first completed two-step smoke attempt, whether pass or fail.
- Stop if logs show either previous failure class again.
- Stop if H200 memory remains allocated after the command exits and hand lifecycle cleanup to `M1-GPU-RETRY-RESOURCE-DEV2`.
- Roll back by using the existing baseline template `configs/train/qwen3_8b_sft.yaml`; this package does not modify the baseline template.

## Fresh GPU Run Justification

A fresh GPU run is justified only after PM gates this package, the test gate, and the resource plan. The prior blocker is config-level, not data/base/resource availability:

- Data/base/deps/output were usable in the previous run.
- The proposed config directly targets the two observed failures.
- A CPU or dry-run check cannot validate MCA/Megatron scheduler/runtime behavior for TP=8.

No GPU run was performed for this package.

## Local No-GPU Validation

Validation command run locally on the dev worktree with `DRY_RUN=1`:

```bash
RUN_ID=local_config_fix_dryrun \
CONFIG_TEMPLATE=$PWD/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml \
DATASET_JSONL=$PWD/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_smoke_run.md \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=$PWD/../debug/sft_config_fix_dryrun \
DRY_RUN=1 \
bash scripts/train_qwen3_8b_sft.sh
```

Result:

```text
DRY_RUN=1; not launching training.
Runtime config: ../debug/sft_config_fix_dryrun/runs/train/local_config_fix_dryrun/config/qwen3_8b_sft.yaml
Run manifest: ../debug/sft_config_fix_dryrun/runs/train/local_config_fix_dryrun/run_manifest.json
```

Runtime config spot-check:

```text
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
save_steps: 1
gradient_accumulation_steps: 1
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
```
