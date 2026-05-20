# GPU Resource Tracking

## Resource Management Rule

Effective 2026-05-20, coding_agent_playground interns must learn and use the LTP workflow directly for GPU resources.

- PM owns organization, gate decisions, durable tracking, and escalation decisions.
- PM does not submit LTP jobs, run training, run eval, or stop jobs directly.
- Dev/test owners must execute LTP submit/status/ssh/stop operations for their assigned work and write durable evidence.
- Do not route routine GPU requests through axrd interns. If an external compute owner already created a resource, transfer lifecycle tracking to a coding_agent_playground owner immediately.
- Every GPU node must have owner, purpose, job id/frame, node endpoint, start time, expected end time, stop conditions, and final stop proof.
- A GPU node must not sit idle. Stop when the assigned smoke finishes, fails irrecoverably, or exceeds the idle/timeout condition below.

## Active Resource: Milestone 1 SFT Smoke H200

Status: active, approved for short SFT smoke only.

Resource:

```text
LTP frame: xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
endpoint: ssh -p 39314 root@10.100.20.37
hostname: lg-cmc-b7r202-o09u26-h200-000667
vc: h200agentic
gpu: 8 x NVIDIA H200
nodes.json: workspace/tasks/milestone1_qwen3_8b_loop/evidence/compute_gpu_route_nodes.json
```

Owners:

```text
Lifecycle / LTP / stop-proof owner: intern_code_dev_2
Workload / SFT smoke owner: intern_code_dev_4
PM gate owner: intern_code_pm
```

Purpose:

```text
Run exactly one short Qwen3-8B SFT smoke for Milestone 1 using the clean-base candidate and 10-example SFT dataset.
No mini-swe eval should run on this node unless PM explicitly assigns a separate eval task.
```

Start time:

```text
Submitted fixed job: 2026-05-20T09:21:30Z, inferred from job name.
Route decision evidence written: 2026-05-20T09:24:29Z.
PM dispatch to dev_4: 2026-05-20T09:30Z range.
```

Expected end time:

```text
Target: 2026-05-20T10:30:00Z or earlier.
Hard stop/review: if no active SFT command is running and no owner progress is recorded for 15 minutes, dev_2 must stop the job or write a durable reason for one more short extension.
```

Stop conditions:

1. Dev_4 records a completed SFT smoke with checkpoint/model artifacts, logs, metrics, and manifest path.
2. Dev_4 records an SFT smoke failure that does not require immediate retry on the same node.
3. PR #14 conflict blocks dev_4 long enough that the GPU node is idle for 15 minutes after this tracking record.
4. GPU route becomes unhealthy, non-idle, or diverges from the approved endpoint.
5. PM explicitly gates that no further SFT attempt should run on this node.

Stop proof requirement:

Dev_2 must write stop evidence to this file or `evidence/dev_2_gpu_lifecycle.md` including:

```text
stop command or LTP API action
job/frame id
timestamp UTC
post-stop LTP status
proof that ssh endpoint is no longer running or job state is STOPPED/SUCCEEDED/FAILED
whether outputs were preserved under /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

Current stop proof:

```text
PENDING. Node is intentionally active for dev_4 SFT smoke.
```

Lifecycle monitor evidence:

```text
evidence/dev_2_gpu_lifecycle.md
```

Latest PM-observed lifecycle state:

```text
2026-05-20T09:35Z: dev_2 reports LTP RUNNING / AttemptRunning, all 8 H200 GPUs idle, no compute processes, no training process, and only milestone1_nodes.json as recent artifact. dev_2 is continuing the short idle watch and will stop if no SFT/progress appears inside the 15-minute idle window.
```

## dev_2 Lifecycle Monitor - 2026-05-20T09:35Z

Owner: `intern_code_dev_2`

PM resource rule update accepted:

- coding_agent_playground owns LTP lifecycle directly.
- Do not route GPU requests through axrd interns.
- dev_2 is lifecycle/stop-proof owner for `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130`.
- Do not run SFT.

Checked commands:

```text
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 39314 root@10.100.20.37 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; nvidia-smi --query-gpu=index,name,memory.used,utilization.gpu --format=csv,noheader,nounits; nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits || true; find /mnt/3fs/data/ai4ai/outputs/coding_agent_playground -maxdepth 3 -type f -mmin -30 2>/dev/null | head -50'
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 39314 root@10.100.20.37 'ps -eo pid,etime,pcpu,pmem,args --sort=-pcpu | head -30; find /mnt/3fs/data/ai4ai/outputs/coding_agent_playground -maxdepth 5 -type f -mmin -20 -printf "%TY-%Tm-%TdT%TH:%TM:%TS %p\n" 2>/dev/null | sort | tail -50'
```

Observed:

```text
local_utc: 2026-05-20T09:35:32Z
remote_utc: 2026-05-20T09:35:31Z
ltp_state: RUNNING / AttemptRunning
endpoint: ssh -p 39314 root@10.100.20.37
hostname: lg-cmc-b7r202-o09u26-h200-000667
gpu_state: all 8 x NVIDIA H200 at 0% utilization, about 1MB memory used per GPU
compute_processes: none reported by nvidia-smi
top_cpu_processes: only runtime, sshd, ceph/3fs fuse, sleep infinity, and monitor commands; no SFT/training process
recent_output_artifacts: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_nodes.json only
dev_4_evidence: latest visible dev_4 record still says no SFT launch was attempted during PR conflict-resolution work
```

Current lifecycle decision:

- Keep watching briefly because the node was just assigned for dev_4 SFT smoke.
- If no active SFT command or owner progress appears by the 15-minute idle/progress window, stop the LTP job and write stop proof here.
- Latest hard stop remains `2026-05-20T10:30:00Z` unless a bounded extension is recorded first.
