# Qwen3-8B SFT Pipeline

This is the Milestone 1 training contract for converting cleaned coding-agent
trajectories into a Qwen3-8B SFT run.

## Inputs

- Base model: `Qwen/Qwen3-8B` by default, override with `BASE_MODEL`.
- Dataset: ShareGPT-style JSONL at `data/sft/milestone1_coding_agent_sft.jsonl`
  by default, override with `DATASET_JSONL`.
- LLamaFactory config template: `configs/train/qwen3_8b_sft.yaml`.
- Final workspace host: `ssh -p 31787 root@10.100.194.40`.
- Shared output root: `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.

## GPU Workflow

1. Start from the final workspace machine and confirm the run is on an allocated
   GPU node:
   ```bash
   ssh -p 31787 root@10.100.194.40
   command -v nvidia-smi && nvidia-smi
   ```
2. If the shell is a CPU/login node, do not launch training there. Obtain the
   allocated GPU workspace or `nodes.json` from the compute workflow first.
3. Materialize LLamaFactory and mcore_adapter in the workspace:
   ```bash
   mkdir -p code
   tar -xf /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz -C code
   rsync -a /mnt/3fs/data/ai4ai/deps/mcore_adapter/ code/mcore_adapter/
   ```
4. Install cluster dependencies with system Python:
   ```bash
   pip install --break-system-packages -e code/LLamaFactory/ --no-deps
   pip install --break-system-packages peft accelerate datasets 'trl<=0.24.0,>=0.18.0'
   pip install --break-system-packages /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
   pip install --break-system-packages -e code/mcore_adapter/ --no-deps
   python3 -c "import flash_attn, mcore_adapter; print('gpu deps ok')"
   llamafactory-cli version
   ```
5. Register the dataset in the workspace-local LLamaFactory
   `data/sft/dataset_info.json` or recipe-local `dataset_info.json`:
   ```json
   {
     "milestone1_coding_agent_sft": {
       "file_name": "/absolute/path/to/data/sft/milestone1_coding_agent_sft.jsonl",
       "formatting": "sharegpt",
       "columns": {"messages": "conversations"},
       "tags": {
         "role_tag": "role",
         "content_tag": "content",
         "user_tag": "user",
         "assistant_tag": "assistant",
         "system_tag": "system"
       }
     }
   }
   ```

## Command Templates

Dry-run locally or on the final machine:

```bash
DRY_RUN=1 bash scripts/train_qwen3_8b_sft.sh
```

Single-node launch on an allocated 8-GPU node:

```bash
DRY_RUN=0 \
DATASET_JSONL=/root/workspace/coding_agent_playground/data/sft/milestone1_coding_agent_sft.jsonl \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
bash scripts/train_qwen3_8b_sft.sh
```

Multi-node launch should use `nodes.json` as the source of truth for
`MASTER_ADDR`, `MASTER_PORT`, `NNODES`, and `NODE_RANK`. Keep configs, dataset,
and checkpoint output on `/mnt/3fs`, or rsync the exact runtime config to every
worker before launching.

Required environment defaults are set by the script:

```bash
USE_MCA=1
FORCE_TORCHRUN=1
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
TORCH_NCCL_AVOID_RECORD_STREAMS=1
NCCL_DEBUG=WARN
DISABLE_VERSION_CHECK=1
NVTE_FLASH_ATTN=1
NVTE_FUSED_ATTN=0
NVTE_UNFUSED_ATTN=0
```

## Checkpoint Layout

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/
  runs/train/<run_id>/
    config/qwen3_8b_sft.yaml
    logs/
    metrics.json
    run_manifest.json
  training_summary/
    sft_output/<run_id>/
      checkpoint-*/
      runs/
      trainer_state.json
    model -> durable final or best exported model
    pinned_checkpoints/
    checkpoint_registry.json
```

Pin any evaluated intermediate checkpoint before resuming if it is the best
candidate so far; rolling retention can delete older `checkpoint-*` directories.

## Run Manifest

`scripts/train_qwen3_8b_sft.sh` writes
`runs/train/<run_id>/run_manifest.json` before launch. The manifest records:

- run id, creation timestamp, git commit, base model, trainer backend;
- dataset path and SHA-256 when the dataset file exists;
- runtime config path and SHA-256;
- checkpoint/output/log locations;
- MCA/NCCL/TransformerEngine environment variables;
- exact launch command.

## Current GPU Blocker

As of 2026-05-20, `ssh -p 31787 root@10.100.194.40` reaches the corrected final
workspace and `/mnt/3fs/data/ai4ai/deps`, but `nvidia-smi` is not present on
that entry host. Full SFT launch requires an allocated GPU node or a
milestone-specific `nodes.json`. Any earlier `20087/root@10.100.193.54` probe
is scratch-only and must not be used as the final workspace assumption.
