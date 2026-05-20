# Dev 4 SFT Retry Run Evidence

Task ID: `M1-SFT-RETRY-RUN-DEV4`
Owner: `intern_code_dev_4`
Status: blocked waiting for fresh dev_2 endpoint/node
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_retry_run.md`

## Assignment

PM assigned dev_4 to run exactly one Qwen3-8B SFT retry after dev_2 provides a fresh endpoint/node.

Constraints:

- Use merged config: `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`.
- Use PM-approved original data unless dev_3/test_1 records a blocker: `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Do not run GPU before fresh endpoint/node exists.
- Do not perform extra retries without a new PM gate.
- Do not peer-send routine status to PM.

## Current Gate State

Current state: blocked before execution.

Reason:

- `M1-SFT-CONFIG-FIX-DEV4` is ready-for-retry via PR #26/#27.
- `M1-GPU-RETRY-RESOURCE-DEV2` is complete-for-plan only.
- Current registry still shows `M1-GPU-RETRY-SUBMIT-DEV2` open with no PR/evidence for a fresh submitted endpoint.
- No `evidence/dev_2_gpu_retry_submit.md` exists in this worktree.
- Registry still shows `M1-SFT-RETRY-AUTH-PM` open, so PM durable authorization record for actual retry execution is not yet merged in this worktree.

No GPU run was attempted for this evidence update.

## Required Inputs Before Launch

Dev_4 will require all of these before running:

```text
fresh endpoint: ssh -p <PORT> root@<IP>
fresh node/frame evidence from dev_2: evidence/dev_2_gpu_retry_submit.md
fresh nodes/tracking evidence: evidence/gpu_retry_resource_tracking.md or PM-approved equivalent
PM retry authorization task: M1-SFT-RETRY-AUTH-PM complete/merged or explicit durable PM gate
test_1 retry gate: no launch-blocking blocker recorded
dev_3 data gate: no blocker against original /root/workspace/cleaned_m1_sft_10/train.jsonl
```

Prior endpoint `ssh -p 39314 root@10.100.20.37` is released and must not be reused.

## Planned Base / Data / Config

Base model:

```text
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

Dataset:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
sha256 5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
count 10
schema coding_agent_playground_sft_v1
```

Config:

```text
/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
```

Key config properties:

```text
tensor_model_parallel_size: 8
gradient_accumulation_steps: 1
max_steps: 2
warmup_steps: 0
save_steps: 1
```

## Pre-Run Verification Commands

Run these only on the fresh endpoint:

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
hostname
command -v nvidia-smi
nvidia-smi -L
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader

cd /root/workspace/coding_agent_playground
test -f configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
test -f /root/workspace/cleaned_m1_sft_10/train.jsonl
sha256sum /root/workspace/cleaned_m1_sft_10/train.jsonl
test -f /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6/config.json
test -w /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
test -d /root/workspace/coding_agent_playground/code/LLamaFactory
```

Expected dataset checksum:

```text
5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
```

## Planned One-Shot Command

Run exactly once after all gates are satisfied:

```bash
cd /root/workspace/coding_agent_playground
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_$(date -u +%Y%m%dT%H%M%SZ) \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

## Required Result Fields

After execution, update this file with:

```text
endpoint
frame/job id
base model path
dataset path and checksum
config path and copied runtime config path
exact command
environment variables
run id
manifest path
log path
exit status
checkpoint/model path presence
trainer_state.json presence
all_results.json presence
resource stop/no-more-work recommendation
blocker if failed
```

Expected output paths for `<RUN_ID>`:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/run_manifest.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/trainer_state.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/all_results.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/checkpoint-*/
```

## Stop / No-Extra-Retry Rule

- Stop after exactly one retry attempt.
- If pre-run checks fail, do not start training.
- If the retry fails, record the blocker and recommend whether dev_2 should stop the resource.
- Do not alter config, switch dataset, or run another bounded retry without a fresh PM gate.
