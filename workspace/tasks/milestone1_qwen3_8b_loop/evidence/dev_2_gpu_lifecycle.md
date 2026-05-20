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

## Monitor 2 - Active Training and Bounded Retry Observation

Timestamp: 2026-05-20T09:41Z to 2026-05-20T09:49Z

PM updates applied:

- dev_4 SFT smoke became active on `ssh -p 39314 root@10.100.20.37`.
- First real SFT attempt failed after training start due `DP=8/drop_last` causing 0 steps on 10 examples.
- dev_4 performed one bounded retry on the same node with `TP=8/DP=1/max_steps=1`.
- Treat resource as intentionally active during the bounded retry; do not stop while real SFT work/artifacts are progressing.

Observed active training at 2026-05-20T09:41Z:

```text
ltp_state: RUNNING / AttemptRunning
gpu_state: all 8 H200 GPUs using about 17156 MiB each; GPUs 5-6 at 5% util, others 0% at sampling instant
compute_processes: 8 x /usr/bin/python3 using about 17146 MiB each
training_processes:
  /usr/local/bin/llamafactory-cli train .../runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/config/qwen3_8b_sft.yaml
  /usr/local/bin/torchrun --nnodes 1 --node_rank 0 --nproc_per_node 8 ...
  8 x LLamaFactory launcher.py worker processes
active_artifacts:
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/run_manifest.json
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/config/qwen3_8b_sft.yaml
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/logs/train_stdout_stderr.log
```

Observed bounded retry artifacts at 2026-05-20T09:45Z and 2026-05-20T09:49Z:

```text
latest_dev4_sft_run_id: milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z
retry_artifacts:
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z/run_manifest.json
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z/config/qwen3_8b_sft.yaml
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z/logs/train_stdout_stderr.log
gpu_state_at_0949: all 8 H200 GPUs back to 0% util and about 1MB memory used
training_process_at_0949: none visible
```

Lifecycle decision before stop:

```text
Did not stop during active training or active retry artifact progress.
Stop became authorized only after PM resource gate reported dev_4's real SFT smoke plus bounded retry both failed and recommended no further GPU use.
```

## Stop Proof - 2026-05-20T09:52Z

Stop reason:

```text
PM RESOURCE GATE: dev_4 reported the real SFT smoke plus one bounded retry both failed and recommended no further GPU use.
```

Pre-stop check:

```text
timestamp_utc: 2026-05-20T09:52:39Z
ltp_state_before_stop: RUNNING / AttemptRunning
endpoint_before_stop: ssh -p 39314 root@10.100.20.37 reachable
remote_utc: 2026-05-20T09:52:37Z
hostname: lg-cmc-b7r202-o09u26-h200-000667
gpu_state_before_stop: all 8 H200 GPUs at 0% util and about 1MB memory used
latest_dev4_sft_run_id: milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z
preserved_run_manifests:
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T093916Z/run_manifest.json
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z/run_manifest.json
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z/run_manifest.json
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/run_manifest.json
```

Stop command/action:

```text
timestamp_utc: 2026-05-20T09:52:39Z to 2026-05-20T09:52:59Z
command:
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130

result:
STOP signal sent to xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
{
  "status": 202,
  "message": "Execute job xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130 successfully."
}
```

Post-stop status:

```text
2026-05-20T09:52:59Z:
  State: STOPPING (AttemptDeleting)
  ExecType: STOP
  TaskRole idx=0 state=STOPPING
  endpoint: still briefly reachable; all 8 GPUs at 0% util and about 1MB memory used

2026-05-20T09:53:19Z:
  State: STOPPING (AttemptDeleting)
  endpoint: Connection closed by 10.100.20.37 port 39314

2026-05-20T09:53:40Z:
  State: STOPPED (Completed)
  ExecType: STOP
  Completed: 2026-05-20 09:53:21
  TaskRole idx=0 state=STOPPED
  endpoint: ssh connect to host 10.100.20.37 port 39314: Connection refused

2026-05-20T09:54:20Z:
  State: STOPPED (Completed)
  Completed: 2026-05-20 09:53:21
  endpoint: Connection refused

2026-05-20T09:54:40Z:
  State: STOPPED (Completed)
  Completed: 2026-05-20 09:53:21
  endpoint: Connection refused
```

Artifact preservation note:

```text
Outputs were preserved under /mnt/3fs/data/ai4ai/outputs/coding_agent_playground before stopping the LTP job. The stop action released the GPU job only; it did not delete shared /mnt/3fs artifacts.
```

Final lifecycle state:

```text
Resource released. Stop proof complete.
```
