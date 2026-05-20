# Dev 2 GPU Route Acquisition Attempt

## Scope

- Date: 2026-05-20
- Intern: `intern_code_dev_2`
- PM assignment: move from GPU evidence to GPU route acquisition support.
- Constraint followed: did not run SFT, did not submit/stop/start/delete LTP jobs, and did not modify remote state.
- Corrected entry host: `ssh -p 31787 root@10.100.194.40`.

## Route Request Channel Attempted

Attempted direct intern route request to compute manager, not PM:

```bash
curl -sS -X POST http://localhost:33709/api/intern/peer/send \
  -H 'Content-Type: application/json' \
  -d '{"from_intern_name":"intern_code_dev_2","to_intern_name":"intern_compute_manager","to_project":"axrd","content":"Milestone 1 GPU route request ..."}'
```

Result:

```json
{"status": "undeliverable", "reason": "unconfirmed"}
```

Interpretation: compute manager route request was attempted but not delivered. No PM peer message was sent.

Local compute manager status evidence:

```bash
cat /work-agents/.feishu_registry/intern_compute_manager.json
sed -n '1,220p' /work-agents/intern_compute_manager/axrd/workspace/interns/intern_compute_manager/status.md
```

Result summary:

```text
registry has intern_compute_manager chat id
intern_compute_manager status: Idle
current task: empty
session: 15
```

## Current nodes.json Check

Commands:

```bash
ssh -p 31787 root@10.100.194.40 'find /root/workspace -maxdepth 6 -name nodes.json -type f -print 2>/dev/null | sort'
ssh -p 31787 root@10.100.194.40 'find /mnt/3fs/data/ai4ai/outputs -maxdepth 4 -name nodes.json -type f -print 2>/dev/null | sort'
```

Result:

```text
/root/workspace: no nodes.json found
/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json
```

Current Milestone 1 `nodes.json`: **does not exist**.

Historical `nodes.json` is not a valid current route without explicit PM/compute approval:

```text
/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json
node_count 4
node 0: root@10.100.2.9 -p 38222
node 1: root@10.100.16.37 -p 34905
node 2: root@10.100.0.49 -p 23657
node 3: root@10.100.14.71 -p 39767
```

## LTP Read-Only Route Discovery

Credential/capacity checks:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py whoami
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 20 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state WAITING --vc h200 --limit 20 --json
```

Result summary:

```text
whoami username xu.yang, application token true
RUNNING h200 jobs: 2
WAITING h200 jobs: 0
```

Running h200 candidate jobs discovered:

```text
xu.yang~ltp-axis-eval-platform-6493743e
state RUNNING
vc h200
totalGpuNumber 8
task 0 SSH: ssh -p 27094 root@10.100.10.20

xu.yang~ltp-axis-eval-platform-2de3c892
state RUNNING
vc h200
totalGpuNumber 8
task 0 SSH: ssh -p 31403 root@10.100.8.24
```

Read-only endpoint probes:

```bash
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 27094 root@10.100.10.20 \
  'hostname; command -v nvidia-smi || true; nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader 2>&1 || true; ls -ld /mnt/3fs/data/ai4ai/outputs/coding_agent_playground /root/workspace/coding_agent_playground /root/workspace/cleaned_m1_sft_10 2>&1 || true'

ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 31403 root@10.100.8.24 \
  'hostname; command -v nvidia-smi || true; nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader 2>&1 || true; ls -ld /mnt/3fs/data/ai4ai/outputs/coding_agent_playground /root/workspace/coding_agent_playground /root/workspace/cleaned_m1_sft_10 2>&1 || true'
```

Endpoint probe summary:

```text
ssh -p 27094 root@10.100.10.20
hostname lg-cmc-b7r201-n06u26-h200-000330
nvidia-smi present at /usr/bin/nvidia-smi
8 x NVIDIA H200 visible
memory used approximately 134590-134850 MiB per GPU
GPU utilization: GPUs 0-3 around 79-80%, GPUs 4-7 0%
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground exists
/root/workspace/coding_agent_playground missing
/root/workspace/cleaned_m1_sft_10 missing

ssh -p 31403 root@10.100.8.24
hostname lg-cmc-b7r201-l04u26-h200-000279
nvidia-smi present at /usr/bin/nvidia-smi
8 x NVIDIA H200 visible
memory used approximately 133836-134640 MiB per GPU
GPU utilization: GPUs 0-3 around 80-81%, GPUs 4-7 0%
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground exists
/root/workspace/coding_agent_playground missing
/root/workspace/cleaned_m1_sft_10 missing
```

Classification:

- These are live GPU endpoints, but **not confirmed Milestone 1 allocation**.
- Both appear already occupied or reserved: very high H200 memory usage on all GPUs and active utilization on GPUs 0-3.
- Both lack the local repo and cleaned dataset paths expected by dev_4's current SFT command.
- Do not route dev_4 to either endpoint unless compute manager/PM explicitly approves borrowing one and dev_4 stages repo/data there or uses shared `/mnt/3fs` paths.

## Compute Workflow Evidence Used

Read:

```text
/work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/SKILL.md
/work-agents/axrd/workspace/tasks/task003_manage_owned_ltp_machines/README.md
/work-agents/axrd/workspace/tasks/task010_gpu_lifecycle_multi_loop/README.md
/work-agents/intern_compute_manager/axrd/ai4ai/setup/gpu_leases.py
/work-agents/intern_compute_manager/axrd/tools/watch_gpus.sh
/root/workspace/axrd/ai4ai/statics/skills/developer/dskill_multinode_training/reference/nodes-json.md
/root/workspace/axrd/ai4ai/setup/ltp/ltp_gpu_worker.yaml
/root/workspace/tools/ltp_configs/gpu_sft_worker.yaml
```

Non-sensitive workflow conclusions:

- LTP skill supports read-only `whoami`, `list`, `status`, `ssh`, `config`, plus mutating `submit/launch/stop/start/delete`.
- I only used read-only commands.
- `task003_manage_owned_ltp_machines` identifies the corrected control host `ssh -p 31787 root@10.100.194.40` and `/root/workspace/axrd` as the compute management environment.
- `nodes.json` is source of truth for multi-node GPU rank/IP/port and must be current for the milestone.
- The GPU worker templates can create H200 8-GPU jobs, but submitting one would modify compute state. I did not submit.
- LTP config output contains sensitive parameter values, so this file records job/resource shape and endpoints only, not secret values.

## Allocation Blocker

Current blocker: no confirmed current Milestone 1 GPU allocation.

Details:

- Compute manager direct request via peer route was undeliverable with reason `unconfirmed`.
- No current Milestone 1 `nodes.json` exists under checked local/remote paths.
- Two live h200 candidate endpoints exist, but they are not approved for Milestone 1 and look occupied.
- Submitting a fresh LTP H200 worker is possible procedurally but was not performed because it would allocate resources/modify compute state and the assignment only asked for route acquisition support, not job submission.

## What dev_4 Should Use If Allocation Succeeds

Preferred single-node smoke route:

```text
ssh -p <ALLOCATED_SSH_PORT> root@<ALLOCATED_GPU_IP>
verify: nvidia-smi
stage or verify:
  /root/workspace/coding_agent_playground
  /root/workspace/cleaned_m1_sft_10/train.jsonl
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
run type: single-node 8 x H200 Qwen3-8B SFT smoke
```

If compute approves one of the discovered candidate endpoints, dev_4 can use only the approved endpoint:

```text
candidate A: ssh -p 27094 root@10.100.10.20
candidate B: ssh -p 31403 root@10.100.8.24
```

Before using either candidate, dev_4 must:

1. Get PM/compute approval that the endpoint is dedicated or safe to borrow.
2. Confirm GPU memory/process state is acceptable immediately before launch.
3. Stage `/root/workspace/coding_agent_playground` and `/root/workspace/cleaned_m1_sft_10/train.jsonl`, or adjust command paths to shared `/mnt/3fs` locations.
4. Keep outputs under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.

Preferred multi-node route:

```text
provide fresh Milestone 1 nodes.json
required fields per node: node_rank, ip, user, port
head node: node_rank 0
MASTER_ADDR: nodes[0].ip
NNODES: len(nodes)
```

Historical route not recommended:

```text
/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json
```

Do not use this historical nodes file unless PM/supervisor explicitly accepts it as the Milestone 1 route.

## Current Recommendation

Route recommendation for PM/dev_4:

1. Ask compute manager to either approve one of the two discovered live h200 endpoints for short SFT smoke or allocate a fresh single-node H200 worker.
2. Prefer fresh single-node H200 8-GPU allocation because the discovered endpoints show high memory occupancy and lack local SFT paths.
3. If fresh allocation is made, write the endpoint to durable evidence and optionally write a one-node Milestone 1 `nodes.json` so dev_4 has a stable route.
4. If no fresh allocation is available, keep SFT smoke blocked on "no approved current GPU route"; do not use the historical nodes.json by default.

## Route Acquired Update

Timestamp: 2026-05-20 UTC

Source:

```text
peer from axrd/intern_compute_manager
durable evidence:
  /work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/compute_gpu_route_decision.md
  /work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/compute_gpu_route_nodes.json
```

Approved fresh single-node H200 route for the requested short Qwen3-8B SFT smoke:

```text
ssh -p 39314 root@10.100.20.37
LTP frame: xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
hostname: lg-cmc-b7r202-o09u26-h200-000667
vc: h200agentic
gpu: 8 x NVIDIA H200
```

Compute manager verification:

```text
all 8 GPUs idle: 0% util, about 1MB memory used per card
no compute processes
/mnt/cephfs is fuse.ceph-fuse
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground is writable
```

Staged on GPU node:

```text
/root/workspace/coding_agent_playground
/root/workspace/cleaned_m1_sft_10/train.jsonl
/root/workspace/coding_agent_playground/nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_nodes.json
```

Updated route decision:

- The allocation blocker from the earlier route-attempt section is resolved for the short SFT smoke only.
- dev_4 should use `ssh -p 39314 root@10.100.20.37` and the staged `nodes.json` paths above.
- Do not use the earlier candidates `ssh -p 27094 root@10.100.10.20` or `ssh -p 31403 root@10.100.8.24`; compute manager reports both are occupied by Ray workers with about 133-135GB GPU memory used per card.
- I did not run SFT.
- After the short smoke, stop the LTP job or ask compute manager to stop it after use.
