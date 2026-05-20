# dev_2 GPU Retry Resource Plan

Task ID: `M1-GPU-RETRY-RESOURCE-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-20T10:35:31Z

## Scope

Prepare the LTP resource plan for any next Milestone 1 Qwen3-8B SFT retry.

This is a **no-submit plan**:

- Do not start a new LTP job until PM gates the dev_4 config fix and test_1 retry gate.
- Do not reuse stale or unrelated H200 jobs.
- Do not peer_send PM routine status.

## Acceptance Criteria

- Include LTP submit/status/stop command templates.
- Define node requirements.
- Define expected duration.
- Define stop conditions.
- Define output preservation path.
- Define owner split.
- Prove no stale H200 allocation remains active for the previous run.

## Current Stale Allocation Proof

Checked at 2026-05-20T10:35:31Z.

Commands:

```text
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 20 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 20 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state STOPPED --vc h200agentic --limit 20 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state STOPPED --vc h200 --limit 20 --json
```

Previous Milestone 1 SFT frame:

```text
frame: xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
state: STOPPED
subState: Completed
executionType: STOP
submitted: 2026-05-20 09:21:31
started: 2026-05-20 09:21:58
completed: 2026-05-20 09:53:21
endpoint: ssh -p 39314 root@10.100.20.37
task state: STOPPED
```

Conclusion:

```text
No stale H200 allocation remains active for the previous Milestone 1 SFT run.
The prior approved endpoint ssh -p 39314 root@10.100.20.37 must be treated as released and unavailable.
```

Current unrelated RUNNING H200 allocations visible under user `xu.yang`:

```text
h200agentic:
  xu.yang~ltp-axis-eval-platform-a71e4142
  endpoint: ssh -p 38116 root@10.100.22.25
  submitted: 2026-05-11 15:55:58
  started: 2026-05-11 15:57:02
  gpu: 8

h200:
  xu.yang~ltp-axis-eval-platform-6493743e
  xu.yang~ltp-axis-eval-platform-2de3c892
  gpu: 8 each
```

These are **not** Milestone 1 retry resources:

- names do not include `coding-agent-playground-m1-qwen3-8b`;
- they predate this retry planning task;
- they must not be reused or stopped by dev_2 for this task without a new PM gate.

## LTP Command Templates

LTP helper:

```text
/work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py
```

Submit template, for use only after PM gates dev_4 config fix and test_1 retry gate:

```bash
RETRY_ID="$(date -u +%Y%m%dT%H%M%SZ)"
LTP_YAML="/root/workspace/tools/ltp_configs/coding_agent_playground_m1_qwen3_8b_retry_${RETRY_ID}.yaml"

# Prepare YAML from the approved single-node H200 worker template.
# Required edits before submit:
# - unique job name: coding-agent-playground-m1-qwen3-8b-retry-${RETRY_ID}
# - vc: h200agentic preferred, h200 only if PM explicitly approves
# - instances: 1
# - gpu per instance: 8
# - command ends in sleep infinity, not training
# - no secrets copied into evidence

python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Status template:

```bash
FRAME="xu.yang~coding-agent-playground-m1-qwen3-8b-retry-<UTC_ID>"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh "${FRAME}"
```

Endpoint verification template after a submitted job reaches RUNNING:

```bash
ssh -p <PORT> root@<IP> '
  date -u +%Y-%m-%dT%H:%M:%SZ
  hostname
  command -v nvidia-smi
  nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits || true
  test -d /root/workspace/coding_agent_playground
  test -f /root/workspace/cleaned_m1_sft_10/train.jsonl
  test -d /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
  test -w /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
'
```

Stop template:

```bash
FRAME="xu.yang~coding-agent-playground-m1-qwen3-8b-retry-<UTC_ID>"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"

for i in 1 2 3 4 5 6; do
  date -u +%Y-%m-%dT%H:%M:%SZ
  python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}" || true
  ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p <PORT> root@<IP> 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; nvidia-smi -L' || echo 'ssh endpoint unavailable'
  sleep 20
done
```

Stop proof must include:

```text
stop command/action
frame id
timestamp UTC
post-stop LTP status
endpoint proof: unavailable, connection refused/closed, or job STOPPED/SUCCEEDED/FAILED
artifact preservation note
```

## Node Requirements

Preferred shape:

```text
single node
vc: h200agentic preferred
gpu: 8 x NVIDIA H200
cpu: around 184
memory: around 2,048,000 MB
shm: around 262,144 MB
infiniband: enabled
mounts:
  /mnt/3fs
  /mnt/3fs2
  /mnt/cephfs as fuse.ceph-fuse
workspace:
  /root/workspace/coding_agent_playground
  /root/workspace/cleaned_m1_sft_10/train.jsonl
nodes:
  /root/workspace/coding_agent_playground/nodes.json
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_nodes.json
output root:
  /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

Training should not be embedded in the LTP bootstrap command. The worker should boot, mount filesystems, expose SSH, verify GPU idleness, write nodes JSON, and then sleep. dev_4 owns launching SFT after PM/test gate.

## Expected Duration

Plan for a short retry window:

```text
allocation/boot: 5-15 minutes
dev_4 setup verification: 5-10 minutes
SFT retry run: 10-30 minutes expected for one bounded smoke
post-run artifact validation: 5-10 minutes
resource hard review: 60 minutes after allocation unless PM records a shorter or bounded longer window
```

Recommended hard stop/review:

```text
Stop after dev_4 completion/failure/no-retry, 15 minutes idle without owner progress, route unhealthy, or PM-specified hard time.
```

## Stop Conditions

Stop/release the retry LTP job when any condition is true:

1. dev_4 records retry completion with no further same-node work required.
2. dev_4 records retry failure and recommends no more same-node retry.
3. test_1 retry gate blocks or fails and PM does not authorize same-node follow-up.
4. No active SFT process and no owner progress for 15 minutes after route handoff.
5. GPU route becomes unhealthy, non-idle before handoff, unreachable unexpectedly, or diverges from approved endpoint.
6. PM hard stop/review time triggers without a bounded extension.

Do not stop while active dev_4 SFT torchrun/python GPU work or fresh retry artifacts are progressing, unless PM explicitly orders stop.

## Output Preservation

All retry artifacts should stay under:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

Recommended retry paths:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/latest_dev4_sft_retry_run_id.txt
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RETRY_RUN_ID>/run_manifest.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RETRY_RUN_ID>/config/qwen3_8b_sft.yaml
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RETRY_RUN_ID>/logs/train_stdout_stderr.log
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RETRY_RUN_ID>/
```

LTP stop must release compute only; it must not delete `/mnt/3fs` outputs.

## Owner Split

```text
PM:
  gates dev_4 config fix and test_1 retry gate before any submit
  sets hard stop/review time
  decides whether a retry allocation should be created

intern_code_dev_2:
  owns LTP resource submit/status/ssh/stop only after PM gate
  writes retry resource evidence, endpoint/nodes evidence, lifecycle watch, and stop proof
  does not run SFT

intern_code_dev_4:
  owns SFT retry command/config/run artifacts
  writes completion/failure/no-more-retry recommendation

intern_code_test_1:
  owns retry gate validation criteria before PM allows a new LTP allocation
  validates SFT retry evidence after dev_4 runs, if assigned by PM
```

## Readiness / Blockers

Current state:

```text
ready_to_submit: no
reason: PM has not yet gated dev_4 config fix and test_1 retry gate.
previous_resource_active: no
previous_resource_state: STOPPED / Completed
new_resource_active: no Milestone 1 retry resource submitted by dev_2
```

Next action after PM gate:

```text
Prepare a unique single-node H200 LTP YAML, submit it, verify endpoint idleness and staged paths, write fresh retry nodes JSON, and hand route to dev_4. Start lifecycle watch immediately after allocation.
```
