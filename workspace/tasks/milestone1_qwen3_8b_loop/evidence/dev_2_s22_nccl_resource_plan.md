# dev_2 S22 NCCL/NVLink Resource Plan

Task ID: `M1-S22-NCCL-RESOURCE-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T10:28:44Z

Scope: no-submit resource plan for a possible future retry after `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.

Execution boundary:

```text
ltp_submit_performed: false
gpu_occupied: false
sft_run: false
eval_run: false
dry_run: false
```

No fresh LTP submit, SFT, GPU command, eval, or dry-run is authorized by this plan. Any future resource action requires fresh PM authorization after the required gates listed below.

## Current Resource Closure

Fresh prior-frame status command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z
```

Fresh prior-frame status result:

```text
frame: xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z
state: STOPPED (Completed)
executionType: STOP
submitted: 2026-05-21 10:07:19
started: 2026-05-21 10:07:22
completed: 2026-05-21 10:17:58
exitCode: -210 Failed
task idx 0: STOPPED
former endpoint: ssh -p 27021 root@10.100.22.14
former node: lg-cmc-b7r202-p07u16-h200-000708
```

Endpoint proof from prior stop evidence:

```text
ssh -p 27021 root@10.100.22.14 refused connection after STOPPED state.
The endpoint is no longer usable and no active resource is held by this frame.
```

Fresh no-active-Milestone-GPU proof commands:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 100 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 100 --json
```

Visible RUNNING H200/H200-agentic jobs:

```text
h200agentic:
  xu.yang~ltp-axis-eval-platform-a71e4142, 8 GPUs, RUNNING
h200:
  xu.yang~ltp-axis-eval-platform-6493743e, 8 GPUs, RUNNING
  xu.yang~ltp-axis-eval-platform-2de3c892, 8 GPUs, RUNNING
```

Conclusion:

```text
No active coding_agent_playground / Milestone 1 / S22 NCCL retry GPU is held by intern_code_dev_2.
Visible RUNNING H200 jobs are unrelated ltp-axis-eval-platform allocations and must not be reused, modified, or stopped for this task.
```

## Blocker Basis

Source evidence:

```text
evidence/dev_2_s22_postpr41_sft_runtime.md
evidence/gpu_s22_postpr41_runtime_tracking.md
evidence/test_1_s22_postpr41_runtime_gate.md
```

Post-PR41 runtime facts to preserve:

```text
PR #41 merge commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
dataset: coding_agent_m1_sft_10_sharegpt
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
generated config: preprocessing_num_workers: null
ShareGPT conversion: completed 10/10
training startup: reached
checkpoint/model/trainer_state/all_results: absent
fresh blocker: CUDA/NCCL `Invalid access of peer GPU memory over nvlink or a hardware error`; local_rank 5 SIGABRT
old blockers absent: KeyError: from; ENOSPC; datasets.map(num_proc=4) SyncManager EOFError
```

Interpretation:

```text
The next resource attempt should not target data-format, storage capacity, or dataset-map multiprocessing. The fresh risk is node/distributed-backend/NVLink/NCCL health or launch environment.
```

## Recommended Resource Shape

Primary recommendation:

```text
Use a fresh single-node 8 x NVIDIA H200 allocation on a different physical node than lg-cmc-b7r202-p07u16-h200-000708.
Do not reuse the stopped post-PR41 node.
Prefer a node with all GPUs idle, no compute processes, clean NVLink/NCCL preflight, and working CephFS /home/xu.yang.
```

VC and SKU:

```text
virtualCluster: h200agentic or PM-approved h200
skuType: h200
instances: 1
gpu_per_node: 8
cpu_per_node: 184
memory_mb: 2048000
shm_mb: 262144
docker image: registry-tmp.zhilicon.com:5000/leejunjie/sglang-mcore:cu130-sgl0.5.9-mcore0.16
```

NCCL/NVL preflight recommendation for any future PM-authorized node before SFT:

```bash
hostname
nvidia-smi -L
nvidia-smi --query-gpu=index,name,uuid,utilization.gpu,memory.used --format=csv
nvidia-smi topo -m
nvidia-smi nvlink --status || true
pgrep -af 'torchrun|python|llamafactory|train_qwen3' || true
findmnt -T /mnt/cephfs
findmnt -T /home/xu.yang
df -h /home/xu.yang/coding_agent_playground/outputs
```

Acceptance expectation before SFT:

```text
8 H200 GPUs visible and idle;
no prior compute process;
NVLink/topology command returns without hardware error;
/home/xu.yang resolves to CephFS;
capacity probe under /home/xu.yang/coding_agent_playground/outputs/capacity_probes passes;
fresh nodes.json is written under both worker repo and /home/xu.yang output metadata.
```

## Output And Capacity Plan

Required root:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Future run layout template:

```text
RUN_ID=milestone1_qwen3_8b_s22_ncclfix_sharegpt_tp8_maxsteps2_<UTC>
run_dir=/home/xu.yang/coding_agent_playground/outputs/runs/train/${RUN_ID}
checkpoint_dir=/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/${RUN_ID}
tmpdir=/home/xu.yang/coding_agent_playground/outputs/tmp/${RUN_ID}
capacity_probe=/home/xu.yang/coding_agent_playground/outputs/capacity_probes/${RUN_ID}
nodes_json=/home/xu.yang/coding_agent_playground/outputs/milestone1_s22_nccl_nodes.json
```

Capacity probe template for a future authorized node:

```bash
RUN_ID=milestone1_qwen3_8b_s22_ncclfix_sharegpt_tp8_maxsteps2_<UTC>
OUT=/home/xu.yang/coding_agent_playground/outputs
PROBE="${OUT}/capacity_probes/${RUN_ID}"
mkdir -p "${PROBE}"
for i in 0 1 2 3; do
  dd if=/dev/zero of="${PROBE}/probe_${i}.bin" bs=1G count=6 status=progress conv=fsync
  ls -lh "${PROBE}/probe_${i}.bin"
done
sync
du -sb "${PROBE}"
rm -f "${PROBE}"/probe_*.bin
rmdir "${PROBE}"
```

Existing required input exceptions that may remain outside `/home/xu.yang`:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dependency_archives_wheels: /mnt/3fs/data/ai4ai/deps
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
justification: required read-only source/dependency inputs, not outputs/logs/checkpoints/probes/run metadata/intermediates.
```

## LTP Command Templates

No-submit boundary:

```text
The following commands are templates only. They must not be executed until PM explicitly authorizes a fresh runtime after all required gates pass.
```

Prepare YAML:

```bash
RUNTIME_ID=<UTC>
JOB_NAME=coding-agent-playground-m1-s22-nccl-qwen3-8b-runtime-${RUNTIME_ID}
FRAME=xu.yang~${JOB_NAME}
LTP_YAML=/tmp/${JOB_NAME}.yaml
# Render or copy the known-good single-node H200 YAML, changing only name and any PM-approved NCCL/preflight bootstrap additions.
```

Submit:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Wait/status/ssh:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait "${FRAME}" --state RUNNING --timeout 1800 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh "${FRAME}"
```

Stop:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait "${FRAME}" --timeout 600 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
```

Required stop conditions for any future authorized run:

```text
complete checkpoint/model plus trainer_state.json/all_results.json captured;
or final SFT failure with no authorized same-node retry;
or failed capacity/NCCL/NVL preflight;
or node idle/unhealthy without progress;
or PM/test stop order.
```

Stop proof must include:

```text
stop command/action;
UTC stop timestamp;
post-stop LTP state and completed timestamp;
endpoint refused proof;
artifact preservation note under /home/xu.yang/coding_agent_playground/outputs;
fresh no-active-Milestone-GPU proof.
```

## Inputs Required Before Fresh PM Authorization

Fresh PM authorization must not be requested or consumed until these inputs exist:

```text
1. dev_4 mitigation package for `M1-S22-NCCL-MITIGATION-DEV4`, including exact NCCL/NVL/launcher or hardware-preflight mitigation and whether it requires a different H200 node.
2. dev_3 data confirmation for `M1-S22-NCCL-DATA-CONFIRM-DEV3`, confirming the accepted ShareGPT data remains valid and no data change is required.
3. dev_1 review for `M1-S22-NCCL-REVIEW-DEV1`, with PASS_FOR_PM_RETRY or exact blockers.
4. test_1 gate for `M1-S22-NCCL-GATE-TEST1`, with PASS_FOR_PM_RETRY and post-run acceptance criteria.
5. PM explicit runtime authorization naming the owner, attempt count, allowed preflight commands, resource shape, run command/env/config, stop conditions, and evidence paths.
6. Confirmed no active coding_agent_playground/Milestone 1 GPU held immediately before submit.
```

Fresh run must preserve:

```text
PR39 diagnostics contract;
PR41 single-process preprocessing (`preprocessing_num_workers: null`);
dataset `coding_agent_m1_sft_10_sharegpt` and sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`;
all outputs/logs/checkpoints/run metadata/intermediates/capacity probes under /home/xu.yang/coding_agent_playground/outputs;
no eval unless separately authorized after checkpoint/model or accepted endpoint exists.
```

## Completion Marker

Complete for no-submit resource planning:

```text
task_id: M1-S22-NCCL-RESOURCE-DEV2
owner: intern_code_dev_2
status: complete-for-no-submit-resource-plan
ltp_submit_performed: false
gpu_occupied: false
sft_run: false
eval_run: false
dry_run: false
prior_postpr41_frame: STOPPED (Completed)
no_active_milestone_gpu_held_by_dev_2: true
fresh_pm_authorization_required_before_submit: true
```

