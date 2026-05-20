# GPU Retry Resource Tracking

Task ID: `M1-GPU-RETRY-SUBMIT-DEV2`

Lifecycle owner: `intern_code_dev_2`

Workload owner: `intern_code_dev_4`

PM/test gate owner: `intern_code_pm` / `intern_code_test_1`

## Active Retry Resource

Status: active, LTP worker submitted and staged; no SFT run by dev_2.

```text
frame: xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
job: coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
vc: h200agentic
node id: lg-cmc-b7r202-r05u16-h200-000747
endpoint: ssh -p 23121 root@10.100.22.53
submitted: 2026-05-20 11:06:15
started: 2026-05-20 11:06:20
expected_end_or_review: 2026-05-20T12:06:20Z unless PM records a bounded extension
```

## Verification Summary

LTP:

```text
state: RUNNING / AttemptRunning
execType: START
task index: 0
task state: RUNNING
container ip: 10.100.22.53
ports: ssh=23121, http=19076
scheduled node: lg-cmc-b7r202-r05u16-h200-000747
```

Endpoint:

```text
timestamp_utc: 2026-05-20T11:10:12Z
hostname: lg-cmc-b7r202-r05u16-h200-000747
gpu: 8 x NVIDIA H200, 143771 MiB each
gpu memory: 1 MiB used per GPU
gpu utilization: 0% on all 8 GPUs
compute processes: none
/mnt/cephfs: fuse.ceph-fuse
output root: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground writable
```

Staged paths:

```text
/root/workspace/coding_agent_playground
/root/workspace/cleaned_m1_sft_10/train.jsonl
/root/workspace/coding_agent_playground/nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_nodes.json
```

Nodes JSON:

```json
{"node_count":1,"nodes":[{"ip":"10.100.22.53","port":"23121","user":"root","node_rank":0}]}
```

## Commands Of Record

Submit:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z.yaml
```

Status:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
```

SSH:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
ssh -p 23121 root@10.100.22.53
```

Stop:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
```

## Stop Conditions

Stop/release when any condition is true:

1. dev_4 records SFT retry completion and no more same-node retry is needed.
2. dev_4 records SFT retry failure/no-retry.
3. test_1 retry gate blocks/fails and PM does not authorize same-node follow-up.
4. No active SFT process and no owner progress for 15 minutes after handoff.
5. GPU route becomes unhealthy, non-idle before handoff, or endpoint becomes unexpectedly unreachable.
6. `2026-05-20T12:06:20Z` hard review triggers without bounded extension.

Do not stop during active dev_4 SFT torchrun/python GPU work or fresh retry artifact progress unless PM explicitly orders stop.

## Output Preservation

Preserve outputs under:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

Current retry route artifact:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_nodes.json
```

LTP stop must release compute only and must not delete shared `/mnt/3fs` artifacts.

## Stop Proof

```text
SUPERSEDED. Resource was active at initial handoff time. See "Final Stop Proof - 2026-05-20T11:22Z" below for completed release proof. dev_2 did not run SFT.
```

## Monitor Update - 2026-05-20T11:19Z

PM resource update applied:

```text
dev_4 pre-run gate passed.
Exactly one SFT retry started on endpoint ssh -p 23121 root@10.100.22.53 around 2026-05-20T11:18Z.
Do not stop while active dev_4 torchrun/python GPU work or fresh retry artifacts are progressing.
Continue monitoring; write stop proof after dev_4/test_1 outcome or PM stop order.
```

Commands checked:

```text
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 23121 root@10.100.22.53 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader,nounits; nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits || true; ps -eo pid,etime,pcpu,pmem,args | egrep "(llamafactory|train_qwen3|torchrun|deepspeed|accelerate|python.*train|sft)" | grep -v egrep || true; cat /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/latest_dev4_sft_retry_run_id.txt 2>/dev/null || true; find /mnt/3fs/data/ai4ai/outputs/coding_agent_playground -maxdepth 5 -type f -mmin -20 -printf "%TY-%Tm-%TdT%TH:%TM:%TS %p\n" 2>/dev/null | sort | tail -80'
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 23121 root@10.100.22.53 '<read latest retry run exit_status, manifest, log tail, and output file list>'
```

Observed:

```text
local_utc: 2026-05-20T11:19:56Z
remote_utc: 2026-05-20T11:19:54Z
ltp_state: RUNNING / AttemptRunning
endpoint: ssh -p 23121 root@10.100.22.53
hostname: lg-cmc-b7r202-r05u16-h200-000747
gpu_state: all 8 H200 GPUs at 0% utilization and about 1 MiB used
compute_processes: none reported by nvidia-smi
training_processes: none visible at sample time
latest_retry_run_id: milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z
fresh_artifacts:
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/latest_dev4_sft_retry_run_id.txt
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/config/qwen3_8b_sft.yaml
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/run_manifest.json
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/exit_status.txt
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/logs/train_stdout_stderr.log
exit_status: EXIT_STATUS=1, END_UTC=2026-05-20T11:19:30Z
log_tail_key_error: KeyError: 'from'
torchrun_result: ChildFailedError, exitcode 1, local_rank 0
checkpoint_files_seen: none in training_summary/sft_output/<run_id> at sample time
```

Lifecycle decision:

```text
Do not stop yet. Although no training process was visible at 2026-05-20T11:19Z and the run wrote EXIT_STATUS=1, fresh retry artifacts were just written and PM instructed stop proof only after dev_4/test_1 outcome or PM stop order. Continue monitoring per stop conditions.
```

## Final Stop Proof - 2026-05-20T11:22Z

Stop reason:

```text
PM stop order for M1-GPU-RETRY-SUBMIT-DEV2.
dev_4 one authorized SFT retry finished with EXIT_STATUS=1, no checkpoint/model/trainer_state/all_results, failure KeyError: 'from' during LLamaFactory dataset conversion, and dev_4 recommended stopping immediately.
```

Pre-stop proof:

```text
timestamp_utc: 2026-05-20T11:22:47Z
frame: xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
ltp_state_before_stop: RUNNING / AttemptRunning
endpoint_before_stop: ssh -p 23121 root@10.100.22.53 reachable
hostname: lg-cmc-b7r202-r05u16-h200-000747
gpu_state_before_stop: all 8 H200 GPUs at 0% utilization and about 1 MiB memory used
compute_processes: none reported by nvidia-smi
latest_retry_run_id: milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z
retry_exit_status: EXIT_STATUS=1, END_UTC=2026-05-20T11:19:30Z
preserved_files_seen:
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/config/qwen3_8b_sft.yaml
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/exit_status.txt
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/logs/train_stdout_stderr.log
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/run_manifest.json
```

Stop command/action:

```text
timestamp_utc: 2026-05-20T11:22:47Z to 2026-05-20T11:23:07Z
command:
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z

result:
STOP signal sent to xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
{
  "status": 202,
  "message": "Execute job xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z successfully."
}
```

Post-stop status:

```text
2026-05-20T11:23:07Z:
  State: STOPPING (AttemptDeleting)
  ExecType: STOP
  TaskRole idx=0 state=STOPPING
  endpoint: still briefly reachable; GPUs idle

2026-05-20T11:23:28Z:
  State: STOPPING (AttemptDeleting)
  endpoint probe: ssh connect to host 10.100.22.53 port 23121: Connection refused

2026-05-20T11:23:48Z:
  State: STOPPED (Completed)
  ExecType: STOP
  Completed: 2026-05-20 11:23:29
  TaskRole idx=0 state=STOPPED
  endpoint probe: ssh connect to host 10.100.22.53 port 23121: Connection refused

2026-05-20T11:24:08Z, 2026-05-20T11:24:28Z, 2026-05-20T11:24:48Z:
  State remains STOPPED (Completed)
  Completed remains 2026-05-20 11:23:29
  endpoint remains unavailable with Connection refused
```

Artifact preservation:

```text
Outputs preserved under /mnt/3fs/data/ai4ai/outputs/coding_agent_playground.
The LTP stop released compute only and did not delete shared /mnt/3fs artifacts.
```

Final lifecycle state:

```text
COMPLETE. Retry resource released at LTP completed timestamp 2026-05-20 11:23:29. dev_2 did not run SFT.
```
