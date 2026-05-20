# dev_2 GPU Lifecycle Evidence

## Scope

PM resource rule update accepted on 2026-05-20 UTC.

`intern_code_dev_2` is lifecycle/stop-proof owner for:

```text
LTP frame: xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
endpoint: ssh -p 39314 root@10.100.20.37
purpose: short Milestone 1 Qwen3-8B SFT smoke only
```

Rules:

- coding_agent_playground owns LTP lifecycle directly.
- Do not route GPU requests through axrd interns.
- Do not run SFT from dev_2.
- Stop after dev_4 SFT completion/failure, idle 15 minutes without progress, or `2026-05-20T10:30:00Z` unless a bounded extension reason is recorded.

## Monitor 1 - 2026-05-20T09:35Z

Commands checked:

```text
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 39314 root@10.100.20.37 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; nvidia-smi --query-gpu=index,name,memory.used,utilization.gpu --format=csv,noheader,nounits; nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits || true; find /mnt/3fs/data/ai4ai/outputs/coding_agent_playground -maxdepth 3 -type f -mmin -30 2>/dev/null | head -50'
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 39314 root@10.100.20.37 'ps -eo pid,etime,pcpu,pmem,args --sort=-pcpu | head -30; find /mnt/3fs/data/ai4ai/outputs/coding_agent_playground -maxdepth 5 -type f -mmin -20 -printf "%TY-%Tm-%TdT%TH:%TM:%TS %p\n" 2>/dev/null | sort | tail -50'
```

Findings:

```text
local_utc: 2026-05-20T09:35:32Z
remote_utc: 2026-05-20T09:35:31Z
ltp_state: RUNNING / AttemptRunning
hostname: lg-cmc-b7r202-o09u26-h200-000667
gpu_state: all 8 H200 GPUs idle at 0% util and about 1MB memory used
compute_processes: none
training_process: none visible
recent_artifacts: only /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_nodes.json
dev_4_progress: latest visible evidence records PR conflict work and says no SFT launch was attempted
```

Decision:

```text
Continue short watch. If still no active SFT/progress inside the 15-minute idle window, stop the LTP job and record stop proof.
```
