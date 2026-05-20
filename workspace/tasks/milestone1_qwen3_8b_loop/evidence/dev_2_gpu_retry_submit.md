# dev_2 GPU Retry Submit Evidence

Task ID: `M1-GPU-RETRY-SUBMIT-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-20T11:04:52Z

## Scope

Submit or explicitly block a fresh LTP H200 job for the next Milestone 1 SFT retry using the merged resource plan.

Boundary:

- dev_2 did not run SFT.
- The LTP worker command ends in `sleep infinity`; it is a resource/SSH worker only.
- Routine status was recorded in durable evidence files, not peer-sent to PM.

## Pre-Submit Checks

Commands:

```text
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 20 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 20 --json
```

Findings:

```text
checked_at_utc: 2026-05-20T11:04:52Z
previous_frame: xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
previous_state: STOPPED / Completed
previous_completed: 2026-05-20 09:53:21
previous_endpoint: ssh -p 39314 root@10.100.20.37
```

Visible unrelated RUNNING H200 jobs:

```text
h200agentic:
  xu.yang~ltp-axis-eval-platform-a71e4142
h200:
  xu.yang~ltp-axis-eval-platform-6493743e
  xu.yang~ltp-axis-eval-platform-2de3c892
```

These unrelated jobs do not use the Milestone 1 retry name and were not reused or stopped.

## Submit Commands

First attempt:

```text
timestamp_utc: 2026-05-20T11:05:20Z
job_name: coding-agent-playground-m1-qwen3-8b-retry-20260520T110520Z
command:
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py config xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130 > /tmp/coding-agent-playground-m1-qwen3-8b-retry-20260520T110520Z.json
python3 <local-json-edit-script> /tmp/coding-agent-playground-m1-qwen3-8b-retry-20260520T110520Z.json coding-agent-playground-m1-qwen3-8b-retry-20260520T110520Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-qwen3-8b-retry-20260520T110520Z.json

result:
HTTP 400 InvalidProtocolError
No job created; status check returned NoJobError for xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110520Z.
```

Successful submit:

```text
timestamp_utc: 2026-05-20T11:06:15Z
job_name: coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
frame: xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
local_submit_file: /tmp/coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z.yaml
command:
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py config xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130 > /tmp/<retry>.json
python3 <local-json-to-yaml-edit-script> /tmp/<retry>.json /tmp/coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z.yaml coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z.yaml

result:
{
  "status": 202,
  "message": "Update job coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z for user xu.yang successfully."
}
```

Notes:

- Submit YAML was generated from the known-good previous single-node `h200agentic` worker shape.
- The evidence intentionally omits secret parameter values.
- The worker runs bootstrap plus `sleep infinity`; no SFT command is embedded.

## Status / SSH / Node

Status command:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py events xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
```

Status:

```text
state: RUNNING / AttemptRunning
execType: START
submitted: 2026-05-20 11:06:15
started: 2026-05-20 11:06:20
vc: h200agentic
task index: 0
task state: RUNNING
node id: lg-cmc-b7r202-r05u16-h200-000747
container ip: 10.100.22.53
ports: ssh=23121, http=19076
endpoint: ssh -p 23121 root@10.100.22.53
```

LTP scheduling event:

```text
Successfully assigned default/d2646ae5aebc5704072cb25e637d1bd1-taskrole-0 to lg-cmc-b7r202-r05u16-h200-000747
```

## Endpoint Verification

Command:

```text
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p 23121 root@10.100.22.53 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; command -v nvidia-smi; nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits; nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits || true; findmnt -n -o FSTYPE,SOURCE -T /mnt/cephfs 2>/dev/null || true; test -d /root/workspace/coding_agent_playground && echo repo_ok || echo repo_missing; test -f /root/workspace/cleaned_m1_sft_10/train.jsonl && echo data_ok || echo data_missing; test -w /mnt/3fs/data/ai4ai/outputs/coding_agent_playground && echo out_writable || echo out_not_writable'
```

Initial result at 2026-05-20T11:10:12Z:

```text
hostname: lg-cmc-b7r202-r05u16-h200-000747
nvidia-smi: /usr/bin/nvidia-smi
gpu: 8 x NVIDIA H200, 143771 MiB each, 1 MiB used each, 0% utilization
compute_processes: none
/mnt/cephfs: fuse.ceph-fuse
repo: missing initially
data: missing initially
output: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground writable
```

## Staging

Staging commands:

```text
ssh -o StrictHostKeyChecking=no -p 31787 root@10.100.194.40 'tar -C /root/workspace -cf - coding_agent_playground cleaned_m1_sft_10' | ssh -o StrictHostKeyChecking=no -p 23121 root@10.100.22.53 'mkdir -p /root/workspace && tar -C /root/workspace -xf -'
ssh -o StrictHostKeyChecking=no -p 23121 root@10.100.22.53 '<write /root/workspace/coding_agent_playground/nodes.json and copy it to /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_nodes.json; verify paths>'
```

Staging verification at 2026-05-20T11:10:53Z:

```text
hostname: lg-cmc-b7r202-r05u16-h200-000747
repo: /root/workspace/coding_agent_playground present
repo git short sha: dc7b268
data: /root/workspace/cleaned_m1_sft_10/train.jsonl present
data lines: 10
node json on GPU: /root/workspace/coding_agent_playground/nodes.json
node json on shared output: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_nodes.json
```

Nodes JSON:

```json
{"node_count":1,"nodes":[{"ip":"10.100.22.53","port":"23121","user":"root","node_rank":0}]}
```

## Expected End / Stop Conditions

Expected end / hard review:

```text
allocation_started: 2026-05-20 11:06:20
expected_end_or_review: 2026-05-20T12:06:20Z unless PM records a bounded extension
```

Stop conditions:

1. dev_4 records SFT retry completion and no more same-node retry is needed.
2. dev_4 records SFT retry failure/no-retry.
3. test_1 retry gate blocks or fails and PM does not authorize same-node follow-up.
4. No active SFT process and no owner progress for 15 minutes after route handoff.
5. GPU route becomes unhealthy, non-idle before handoff, or endpoint becomes unexpectedly unreachable.
6. `2026-05-20T12:06:20Z` hard review triggers without bounded extension.

Do not stop while active dev_4 SFT torchrun/python GPU work or fresh retry artifacts are progressing, unless PM explicitly orders stop.

## Output Preservation

Output root:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

Retry route artifacts:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_nodes.json
```

Expected dev_4 retry artifacts:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/latest_dev4_sft_retry_run_id.txt
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RETRY_RUN_ID>/
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RETRY_RUN_ID>/
```

Stopping LTP must not delete `/mnt/3fs` outputs.

## Stop Command Template

```bash
FRAME="xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"

for i in 1 2 3 4 5 6; do
  date -u +%Y-%m-%dT%H:%M:%SZ
  python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}" || true
  ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p 23121 root@10.100.22.53 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; nvidia-smi -L' || echo 'ssh endpoint unavailable'
  sleep 20
done
```

## Final Stop Proof

Current state:

```text
SUPERSEDED. Resource was active at initial handoff time. See "Final Stop Proof - 2026-05-20T11:22Z" below for completed release proof. dev_2 has not run SFT.
```

When stop is authorized, write:

```text
stop command/action
timestamp UTC
frame id
post-stop LTP status
endpoint proof
artifact preservation note
```

## Monitor Update - 2026-05-20T11:19Z

PM update: dev_4 pre-run gate passed and exactly one SFT retry started around 2026-05-20T11:18Z on:

```text
ssh -p 23121 root@10.100.22.53
```

Read-only monitor result:

```text
ltp_state: RUNNING / AttemptRunning
gpu_state: all 8 H200 GPUs at 0% util and about 1 MiB memory used
compute_processes: none at sample time
latest_retry_run_id: milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z
exit_status_file: EXIT_STATUS=1, END_UTC=2026-05-20T11:19:30Z
log_tail: KeyError: 'from' in LLamaFactory dataset conversion, followed by torchrun ChildFailedError exitcode 1
fresh_artifacts: run_manifest.json, config/qwen3_8b_sft.yaml, logs/train_stdout_stderr.log, exit_status.txt
```

Lifecycle action:

```text
No stop issued. Fresh retry artifacts had just been written and PM instructed dev_2 to stop only after dev_4/test_1 outcome or PM stop order.
```

## Final Stop Proof - 2026-05-20T11:22Z

Stop reason:

```text
PM stop order. dev_4 one authorized SFT retry finished with exit_status=1, no checkpoint/model/trainer_state/all_results, failure KeyError: 'from' during LLamaFactory dataset conversion, and dev_4 recommended stopping immediately.
```

Pre-stop:

```text
timestamp_utc: 2026-05-20T11:22:47Z
ltp_state: RUNNING / AttemptRunning
endpoint: ssh -p 23121 root@10.100.22.53 reachable
gpu_state: all 8 H200 GPUs idle at 0% util and about 1 MiB memory used
latest_retry_run_id: milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z
exit_status: EXIT_STATUS=1, END_UTC=2026-05-20T11:19:30Z
preserved_artifacts_seen: config/qwen3_8b_sft.yaml, exit_status.txt, logs/train_stdout_stderr.log, run_manifest.json
```

Stop command/action:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
```

Stop command result:

```text
STOP signal sent to xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
{
  "status": 202,
  "message": "Execute job xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z successfully."
}
```

Post-stop proof:

```text
2026-05-20T11:23:07Z: STOPPING / AttemptDeleting; endpoint still briefly reachable and GPU idle.
2026-05-20T11:23:28Z: STOPPING / AttemptDeleting; endpoint refused connection.
2026-05-20T11:23:48Z: STOPPED / Completed; completed 2026-05-20 11:23:29; endpoint refused connection.
2026-05-20T11:24:08Z: STOPPED / Completed; endpoint refused connection.
2026-05-20T11:24:28Z: STOPPED / Completed; endpoint refused connection.
2026-05-20T11:24:48Z: STOPPED / Completed; endpoint refused connection.
```

Artifact preservation:

```text
Outputs preserved under /mnt/3fs/data/ai4ai/outputs/coding_agent_playground.
The stop action released the LTP compute worker only and did not delete /mnt/3fs artifacts.
```

Final state:

```text
M1-GPU-RETRY-SUBMIT-DEV2 stop proof complete. Resource released. dev_2 did not run SFT.
```
