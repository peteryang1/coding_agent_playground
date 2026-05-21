# Dev 4 S22 NCCL/NVLink Mitigation Package

Task ID: `M1-S22-NCCL-MITIGATION-DEV4`

Owner: `intern_code_dev_4`

Created: 2026-05-21

Scope: no-execution mitigation package for fresh post-PR41 runtime blocker `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.

Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_nccl_mitigation.md`

Completion marker: ready-for-review; future runtime remains blocked until PM/dev_1/test_1/dev_2 gates authorize a fresh resource and command.

## Inputs Reviewed

Primary evidence:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_postpr41_sft_runtime.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_postpr41_runtime_gate.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_postpr41_runtime_tracking.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/pm_s22_nccl_nvlink_blocker_gate.md
```

Post-PR41 runtime facts:

```text
runtime task: M1-S22-POSTPR41-SFT-RUNTIME-DEV2
node: lg-cmc-b7r202-p07u16-h200-000708
endpoint while active: ssh -p 27021 root@10.100.22.14
run_id: milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
code commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
output root: /home/xu.yang/coding_agent_playground/outputs
exit_status: EXIT_STATUS=1
stop proof: STOPPED (Completed), completed 2026-05-21 10:17:58, endpoint refused after stop
```

What was proven good:

```text
PR39 diagnostics: PASS; preflight/config/manifest/log/xtrace/diagnostics/exit_status were produced.
PR41 preprocessing: PASS; runtime config and manifest record preprocessing_num_workers: null.
Data: PASS; coding_agent_m1_sft_10_sharegpt, source sha256 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2, row count 10.
Dataset conversion: PASS; ShareGPT conversion completed 10/10 without num_proc=4.
Training startup: reached; log contains ***** Running training *****, Num examples = 1, Num Epochs = 2.
```

Fresh blocker:

```text
failure class: CUDA/NCCL peer GPU memory / NVLink or hardware error during distributed training
primary signature: ProcessGroupNCCL watchdog thread terminated with CUDA error: Invalid access of peer GPU memory over nvlink or a hardware error
torch elastic root cause: local_rank 5, exitcode -6, SIGABRT
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval handoff: blocked
```

Old blocker signatures absent:

```text
KeyError: from: absent
Wrong dataset_info or dataset name: absent
datasets.map(num_proc=4) / SyncManager EOFError: absent
ENOSPC / safetensors no-space: absent
checkpoint save failure: not reached
early wrapper exit before diagnostics: absent
```

## Diagnosis

This is not a data-format, storage, PR39 diagnostics, or PR41 preprocessing regression. The run reached distributed training startup on 8 H200 GPUs, then failed in NCCL/CUDA peer memory over NVLink on local rank 5 before checkpoint save.

The signature is hardware or distributed-backend sensitive. Because the failed node was stopped and because the error names peer GPU memory over NVLink or hardware error, the safest next package is not a same-node retry. A future attempt should require a fresh H200 allocation, preferably a different physical node, plus a bounded NCCL/NVLink preflight before any SFT launch.

## Mitigation Recommendation

Preferred mitigation: **different H200 node plus hardware/NCCL preflight**.

Rationale:

```text
- The failure names NVLink peer memory or hardware error and occurred on local_rank 5.
- PR39 and PR41 software/data mitigations were effective before this new point.
- A same-node retry cannot distinguish transient NCCL setup from a node-specific NVLink/peer-memory problem unless a hardware preflight is first run.
- A different H200 node lowers risk of repeating a node-local NVLink or GPU peer-memory fault.
```

Required future resource decision:

```text
Use a fresh H200 node that is not lg-cmc-b7r202-p07u16-h200-000708 if available.
Do not reuse endpoint ssh -p 27021 root@10.100.22.14; it is stopped and refused connection after stop.
If PM/resource owner can only allocate the same host class, require the preflight below before SFT.
```

## Future Hardware/NCCL Preflight Package

Run only after PM explicitly authorizes GPU/preflight work. This package itself does not authorize execution.

Preflight paths must stay under:

```text
/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>
```

Existing required input exceptions remain read-only only:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dependency_archives_wheels: /mnt/3fs/data/ai4ai/deps
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Recommended preflight commands for a future PM-gated node:

```bash
RUN_ID=<fresh-run-id>
OUT=/home/xu.yang/coding_agent_playground/outputs
PREFLIGHT_DIR="${OUT}/preflight/${RUN_ID}"
mkdir -p "${PREFLIGHT_DIR}"

hostname | tee "${PREFLIGHT_DIR}/hostname.txt"
nvidia-smi -L | tee "${PREFLIGHT_DIR}/nvidia_smi_L.txt"
nvidia-smi topo -m | tee "${PREFLIGHT_DIR}/nvidia_smi_topo_m.txt"
nvidia-smi nvlink -s | tee "${PREFLIGHT_DIR}/nvidia_smi_nvlink_s.txt"
nvidia-smi -q -d ECC,PCI,NVLINK,PERFORMANCE | tee "${PREFLIGHT_DIR}/nvidia_smi_q_ecc_pci_nvlink_performance.txt"

# If nccl-tests is present in the runtime image or staged by dev_2/resource owner:
NCCL_DEBUG=INFO \
NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL \
NCCL_ASYNC_ERROR_HANDLING=1 \
TORCH_NCCL_ASYNC_ERROR_HANDLING=1 \
CUDA_DEVICE_MAX_CONNECTIONS=1 \
torchrun --standalone --nproc_per_node=8 /path/to/nccl_or_torch_allreduce_preflight.py \
  2>&1 | tee "${PREFLIGHT_DIR}/torch_nccl_allreduce_preflight.log"
```

If a custom PyTorch preflight is used instead of nccl-tests, it should do all of the following:

```text
- initialize torch.distributed with backend=nccl across all 8 local ranks;
- set each local rank's CUDA device explicitly;
- run at least one all_reduce on a small tensor and one all_reduce on a moderately sized tensor;
- print rank, device, bus id if available, success/failure, and elapsed time;
- exit nonzero on any NCCL/CUDA exception;
- write stdout/stderr under /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>.
```

Preflight pass criteria before SFT:

```text
- nvidia-smi sees 8 H200 GPUs;
- no fresh ECC/Xid/NVLink replay or link error is reported in captured nvidia-smi output;
- topology/NVLink output is captured for audit;
- 8-rank NCCL all_reduce preflight exits 0;
- preflight artifacts are under /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>.
```

Preflight fail criteria:

```text
- any NCCL/CUDA invalid peer memory, unhandled system error, SIGABRT, Xid, or NVLink link error;
- missing or unhealthy GPU;
- failure to write preflight artifacts under /home/xu.yang;
- reuse of the stopped endpoint without PM/resource-owner justification.
```

## Future SFT Command / Env Changes

Preserve these already-proven requirements:

```text
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory
DRY_RUN=0
SFT_XTRACE=1
```

Preserve PR41 preprocessing in generated runtime config:

```text
preprocessing_num_workers: null
dataloader_num_workers: 0
```

Recommended NCCL/CUDA env additions for the next PM-gated SFT run after preflight passes:

```bash
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL
export NCCL_ASYNC_ERROR_HANDLING=1
export TORCH_NCCL_ASYNC_ERROR_HANDLING=1
export CUDA_DEVICE_MAX_CONNECTIONS=1
```

Rationale:

```text
NCCL_DEBUG and NCCL_DEBUG_SUBSYS improve future root-cause evidence.
NCCL_ASYNC_ERROR_HANDLING / TORCH_NCCL_ASYNC_ERROR_HANDLING make distributed failures surface more cleanly.
CUDA_DEVICE_MAX_CONNECTIONS=1 is a conservative Megatron-style setting often used to reduce communication scheduling variability.
```

Do not make `NCCL_P2P_DISABLE=1` the default SFT command. Treat it as a fallback only if PM/dev_1/test_1 explicitly accept a degraded NVLink-bypass diagnostic run:

```bash
export NCCL_P2P_DISABLE=1
```

Fallback risk:

```text
Disabling peer-to-peer communication may avoid an NVLink peer-memory path, but it also changes the distributed communication path and can mask a node/hardware issue. For this milestone, a different healthy H200 node plus NCCL preflight is the cleaner next runtime gate.
```

## Proposed Future Command Skeleton

Run only after fresh PM authorization and resource/test gates:

```bash
cd /root/workspace/coding_agent_playground
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL
export NCCL_ASYNC_ERROR_HANDLING=1
export TORCH_NCCL_ASYNC_ERROR_HANDLING=1
export CUDA_DEVICE_MAX_CONNECTIONS=1
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=<fresh-run-id> \
DRY_RUN=0 \
SFT_XTRACE=1 \
bash scripts/train_qwen3_8b_sft.sh
```

## Runtime Boundary

```text
No LTP/SFT/GPU/eval or dry-run launch was run by dev_4 for this task.
No peer_send PM was used.
This evidence package does not authorize runtime retry.
Future runtime requires PM gate plus resource/dev_1/test_1 gates.
```

## PR #43 Merge Completion

PM gate facts:

```text
PM gate evidence: workspace/tasks/milestone1_qwen3_8b_loop/evidence/pm_s22_pr43_gate.md on pm/session12-pr30-after-pr38-gate commit 5e4cfab
dev_1 evidence/dev_1_s22_nccl_review.md: PASS_FOR_PM_RETRY
test_1 evidence/test_1_s22_nccl_retry_gate.md: PASS_FOR_PM_RETRY
dev_2 resource plan: pass
dev_3 data confirmation: pass
GitHub PR #43 head: 5f4d14a12aa8044a429d1110757ed631a7bc9833
GitHub PR #43 pre-merge state: open, non-draft, MERGEABLE/CLEAN
Authorization scope: owner self-merge only
```

Merge evidence:

```text
PR #43: https://github.com/peteryang1/coding_agent_playground/pull/43
mergedAt: 2026-05-21T10:47:20Z
merge_commit: 2c867d3226f7ebb4962b5b173235639df8f1f9be
completion_marker: complete/ready-for-runtime-gate
```

Runtime boundary:

```text
This completion does not authorize LTP/SFT/GPU/NCCL preflight/eval/dry-run launch or runtime retry.
Future SFT/eval/preflight intermediates must remain under /home/xu.yang unless an existing required input path is explicitly justified.
No runtime command was run by dev_4 for completion.
```
