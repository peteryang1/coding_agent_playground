# Dev 2 GPU / nodes.json Support Evidence

## Scope

- Date: 2026-05-20
- Intern: `intern_code_dev_2`
- PM assignment: independently check current GPU allocation, `nodes.json`, and compute workflow evidence for Milestone 1.
- Constraint followed: read-only checks only; did not modify remote state and did not start training.
- Corrected final workspace checked: `ssh -p 31787 root@10.100.194.40`.

## Checked Commands And Paths

Entry-host GPU check:

```bash
ssh -p 31787 root@10.100.194.40 'hostname; command -v nvidia-smi || true; nvidia-smi 2>&1 || true; echo CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES-}'
```

Result:

```text
hostname lg-cmc-b7r201-k10u23-cpu-000158
command -v nvidia-smi: empty
nvidia-smi: zsh:1: command not found: nvidia-smi
CUDA_VISIBLE_DEVICES=
```

`nodes.json` search:

```bash
ssh -p 31787 root@10.100.194.40 'find /root/workspace -maxdepth 6 -name nodes.json -type f -print 2>/dev/null | sort'
ssh -p 31787 root@10.100.194.40 'find /mnt/3fs/data/ai4ai/outputs -maxdepth 4 -name nodes.json -type f -print 2>/dev/null | sort'
```

Result:

```text
/root/workspace: no nodes.json found
/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json
```

Milestone/output path search:

```bash
ssh -p 31787 root@10.100.194.40 'find /mnt/3fs/data/ai4ai/outputs /root/workspace -maxdepth 5 \( -iname "*milestone*" -o -iname "*coding_agent*" -o -iname "*qwen3_8b*" \) -print 2>/dev/null | sort'
```

Relevant result:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_smoke_cmd_20260520
/root/workspace/coding_agent_playground
/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft.yaml
/root/workspace/coding_agent_playground/docs/training/qwen3_8b_sft_pipeline.md
/root/workspace/coding_agent_playground/scripts/train_qwen3_8b_sft.sh
```

Workflow evidence paths checked:

```text
/root/workspace/axrd/ai4ai/statics/skills/developer/dskill_multinode_training/reference/nodes-json.md
/root/workspace/axrd/ai4ai/statics/skills/developer/dskill_multinode_training/SKILL.md
/root/workspace/axrd/ai4ai/setup/ltp/ltp_gpu_worker.yaml
/root/workspace/tools/ltp_configs/gpu_sft_worker.yaml
/root/workspace/coding_agent_playground/scripts/train_qwen3_8b_sft.sh
/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft.yaml
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/run_manifest.json
/root/workspace/cleaned_m1_sft_10/train.jsonl
```

Note: GPU worker YAML files contain sensitive parameter values. I checked their workflow shape but did not copy secrets into this evidence file.

## Current nodes.json Status

- Current Milestone 1 `nodes.json`: **not found**.
- Corrected final workspace entry host does not expose GPUs and has no `nvidia-smi`.
- Historical `nodes.json` exists at:

```text
/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json
```

Historical file summary:

```text
node_count 4
node 0: user=root ip=10.100.2.9 port=38222 node_rank=0
node 1: user=root ip=10.100.16.37 port=34905 node_rank=1
node 2: user=root ip=10.100.0.49 port=23657 node_rank=2
node 3: user=root ip=10.100.14.71 port=39767 node_rank=3
```

Classification: historical/non-milestone. Do not use it for Milestone 1 SFT without explicit compute/PM confirmation.

## Compute Workflow Evidence

Axrd `nodes-json.md` says `nodes.json` is the source of truth for multi-node GPU workspaces: node count, rank, IP, user, and SSH port. It also says worker SSH must use each node's recorded port and workspace paths must be identical when scripts reference workspace-local files.

Axrd `dskill_multinode_training` rules relevant to SFT:

- Shared training state should live on `/mnt/3fs/...`.
- Pod-local paths are only for ephemeral runtime material.
- Configs, data, code, and env files must be on shared storage or propagated to every worker before launch.
- SSH does not inherit arbitrary shell env; required env vars must be passed explicitly.
- For LLamaFactory/MCA SFT, use the task-specific SFT launcher plus multi-node torchrun/SSH guidance.

GPU route templates found:

- `/root/workspace/axrd/ai4ai/setup/ltp/ltp_gpu_worker.yaml`: single taskrole, 1 instance, 8 GPUs, H200 virtual cluster; installs/mounts shared storage and then sleeps for interactive use.
- `/root/workspace/tools/ltp_configs/gpu_sft_worker.yaml`: taskrole with 2 instances, 8 GPUs each, H200 virtual cluster; includes SSH plugin and writes runtime node/network env.

These templates indicate an available compute workflow pattern, not a currently allocated Milestone 1 GPU node.

## SFT Readiness Context

Existing SFT command manifest:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/run_manifest.json
```

Manifest confirms:

```text
run_id milestone1_qwen3_8b_sft_smoke_cmd_20260520
dataset /root/workspace/cleaned_m1_sft_10/train.jsonl
dataset_sha256 f91d0b096537564f136576dd7f3bb5f54750aafb524c7f890be621d557ddd0c2
repo_root /root/workspace/coding_agent_playground
trainer LLamaFactory full SFT with MCA
output_dir /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_smoke_cmd_20260520
```

Dataset exists:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
```

SFT scripts/configs exist:

```text
/root/workspace/coding_agent_playground/scripts/train_qwen3_8b_sft.sh
/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft.yaml
```

## Available GPU Route

No current live GPU route is verified for Milestone 1. The available route is procedural:

1. Ask compute manager/PM to allocate an H200 GPU worker using the established LTP GPU worker template.
2. For single-node smoke, one 8-GPU node is sufficient after verifying `nvidia-smi` on that node.
3. For multi-node smoke/full run, require a fresh Milestone 1 `nodes.json`; use its `node_rank`, `ip`, `user`, and `port` fields and keep dataset/config/output on `/mnt/3fs`.
4. Do not route dev_4 to the historical `ws_20260512.../nodes.json` unless PM/supervisor explicitly accepts reuse of that old allocation.

## Recommendation For dev_4 SFT Smoke

Recommended next routing:

1. Route dev_4 to request or receive a current GPU allocation from compute manager, preferably a single H200 8-GPU node for the first SFT smoke.
2. Require dev_4 to record either:
   - direct GPU node SSH endpoint plus `nvidia-smi` output, or
   - current Milestone 1 `nodes.json` path and parsed node list.
3. Once a GPU node is available, run only the existing SFT smoke command path using:
   - dataset `/root/workspace/cleaned_m1_sft_10/train.jsonl`;
   - repo `/root/workspace/coding_agent_playground`;
   - output root `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`;
   - shared artifacts under `/mnt/3fs`.
4. If no GPU allocation can be issued immediately, dev_4 should keep SFT status blocked on "missing current GPU node / Milestone 1 nodes.json"; PM/compute should own routing to the next available H200 job.

Current decision: SFT smoke is not launchable from `ssh -p 31787 root@10.100.194.40` alone because that host has no visible GPU and no current Milestone 1 `nodes.json`.
