# Dev 4 SFT Smoke Run Evidence

Owner: intern_code_dev_4  
Session: 13  
Timestamp: 2026-05-20T09:46:00Z  
Task ID: M1-SFT-SMOKE-DEV4
Scope: short Qwen3-8B clean-base SFT smoke only. No mini-swe was run.

## PM Authorization / Resource Rule

- PM task registry entry: `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`, task id `M1-SFT-SMOKE-DEV4`.
- Approved GPU endpoint: `ssh -p 39314 root@10.100.20.37`
- Approved local `nodes.json`: `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/compute_gpu_route_nodes.json`
- GPU-staged `nodes.json`:
  - `/root/workspace/coding_agent_playground/nodes.json`
  - `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_nodes.json`
- SFT workload owner: dev_4.
- LTP lifecycle/stop proof owner: dev_2.
- Resource decision from this run: dev_2 should stop the H200 allocation immediately. A further retry is not recommended without a PM-approved config change for MCA/Megatron tiny-data smoke.

## Precheck

Command:

```bash
ssh -p 39314 root@10.100.20.37 'nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader'
```

Result:

```text
0..7, NVIDIA H200, 1 MiB used, 143771 MiB total
```

Other verified paths:

```text
/root/workspace/coding_agent_playground
/root/workspace/cleaned_m1_sft_10/train.jsonl
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
/root/workspace/coding_agent_playground/nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_nodes.json
```

Dataset:

```text
10 /root/workspace/cleaned_m1_sft_10/train.jsonl
sha256 5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
```

Dependency setup performed on the approved GPU endpoint:

```bash
cd /root/workspace/coding_agent_playground
mkdir -p code/LLamaFactory
tar -xf /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz -C code/LLamaFactory --strip-components=1
python3 -m pip install --break-system-packages hatchling editables
python3 -m pip install --break-system-packages \
  /mnt/3fs/data/ai4ai/deps/mcore_adapter-0.9.0-py3-none-any.whl \
  /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl \
  'trl>=0.18.0,<=0.24.0' peft -e code/LLamaFactory --no-build-isolation
```

Verified:

```text
llamafactory 0.9.5.dev0
trl 0.24.0
peft 0.18.1
flash_attn 2.8.3
mcore_adapter import OK
/usr/local/bin/llamafactory-cli
```

Dataset registration added on the GPU endpoint:

```text
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
```

## Attempt 1: Baseline Command

Run ID:

```text
milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T093916Z
```

Command:

```bash
cd /root/workspace/coding_agent_playground
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T093916Z \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Exit status: `1`

Paths:

```text
manifest: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T093916Z/run_manifest.json
config: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T093916Z/config/qwen3_8b_sft.yaml
log: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T093916Z/logs/train_stdout_stderr.log
checkpoint/model path: none
trainer_state/all_results: none
```

Failure:

```text
ValueError: Cannot open data/sft/dataset_info.json
```

Action taken: registered the dataset in `code/LLamaFactory/data/sft/dataset_info.json`.

## Attempt 2: Baseline After Dataset Registration

Run ID:

```text
milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z
```

Command:

```bash
cd /root/workspace/coding_agent_playground
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Exit status: `1`

Paths:

```text
manifest: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/run_manifest.json
config: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/config/qwen3_8b_sft.yaml
log: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/logs/train_stdout_stderr.log
tensorboard event: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/runs/May20_17-40-20_lg-cmc-b7r202-o09u26-h200-000667/events.out.tfevents.1779270124.lg-cmc-b7r202-o09u26-h200-000667.50764.0
checkpoint/model path: none
trainer_state/all_results: none
```

Progress before failure:

```text
Loaded 10 examples.
Loaded clean-base Qwen3 config from /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6.
Initialized 8 distributed tasks on H200.
Entered training with total optimization steps = 2.
```

Failure:

```text
ZeroDivisionError: division by zero
mcore_adapter/trainer/trainer.py: self.state.epoch = epoch + (...) / steps_in_epoch
```

Interpretation: MCA trainer forces `drop_last=True`; with 10 examples and the baseline DP=8 layout, the tiny smoke dataset yields zero effective steps per epoch on ranks.

## Attempt 3: Bounded Retry With TP=8 Tiny-Data Config

Run ID:

```text
milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z
```

Bounded retry rationale: keep the same clean base/data/output, but use TP=8, DP=1 and `max_steps=1` so the 10-example dataset is not split across data-parallel workers.

Command:

```bash
cd /root/workspace/coding_agent_playground
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Exit status: `1`

Paths:

```text
manifest: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z/run_manifest.json
config: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z/config/qwen3_8b_sft.yaml
log: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z/logs/train_stdout_stderr.log
checkpoint/model path: none
trainer_state/all_results: none
```

Progress before failure:

```text
Loaded 10 examples.
Initialized tensor model parallel with size 8.
Loaded clean-base Qwen3 config.
```

Failure:

```text
AssertionError
megatron/core/optimizer_param_scheduler.py: assert self.lr_warmup_steps < self.lr_decay_steps
```

Interpretation: this MCA/Megatron stack rejects the 1-step bounded smoke scheduler. A successful tiny-data retry likely needs a deliberate training-config change such as more scheduler decay steps, zero warmup handling, or a non-MCA/alternate smoke mode, which requires PM-approved scope because the assigned command was the clean-base LLamaFactory/MCA path.

## Final State

- No checkpoint directory with model files was produced.
- No `trainer_state.json` or `all_results.json` was produced.
- GPU process cleanup verified after attempts:

```text
nvidia-smi memory.used: 1 MiB on GPUs 0-7
no torchrun/llamafactory/launcher.py process remains
```

## Blockers

- The approved GPU route, base model, dataset, output root, and dependencies are usable.
- Current blocker is MCA/Megatron tiny-data smoke configuration:
  - baseline DP=8 with 10 examples fails with `ZeroDivisionError` from `steps_in_epoch=0`;
  - bounded TP=8/max_steps=1 retry fails scheduler assertion `lr_warmup_steps < lr_decay_steps`.

## Resource Recommendation

Dev_2 should stop the active H200 allocation immediately and record stop proof. Dev_4 does not need the GPU held open after this evidence because the remaining issue is config-level, not live resource access.

If PM later approves another retry, recommended bounded retry shape is a config-only run with enough optimization steps for Megatron scheduler validity and tiny-data-safe batching, for example TP=8, DP=1, `max_steps>=2`, and explicit `warmup_steps=0` or equivalent scheduler settings after confirming LLamaFactory/MCA accepts them.
