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
PENDING. Resource is currently active and staged for the PM-assigned retry. dev_2 did not run SFT.
```
