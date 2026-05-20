# dev_2 GPU Retry Plan 2

Task ID: `M1-GPU-RETRY-PLAN2-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-20T12:03:52Z

## Scope

Prepare the next LTP resource plan only for a possible data-format-fixed SFT retry.

Boundary:

- Do not submit or occupy a GPU node without a fresh PM gate.
- Do not run SFT.
- Routine status/evidence goes to durable files only; no peer_send PM.

## Acceptance Criteria

- Node shape.
- Submit/status/stop command templates.
- Max runtime.
- Stop conditions.
- Output preservation path.
- Proof no retry GPU is active.

## Proof No Retry GPU Is Active

Checked at 2026-05-20T12:03:52Z.

Commands:

```text
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 50 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 50 --json
```

Prior retry frame:

```text
frame: xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
state: STOPPED
subState: Completed
execType: STOP
submitted: 2026-05-20 11:06:15
started: 2026-05-20 11:06:20
completed: 2026-05-20 11:23:29
prior endpoint: ssh -p 23121 root@10.100.22.53
task state: STOPPED
```

Current RUNNING H200/H200-agentic jobs visible under user `xu.yang`:

```text
h200agentic:
  xu.yang~ltp-axis-eval-platform-a71e4142

h200:
  xu.yang~ltp-axis-eval-platform-6493743e
  xu.yang~ltp-axis-eval-platform-2de3c892
```

Conclusion:

```text
No active coding_agent_playground / Milestone 1 / qwen3-8b retry GPU allocation exists.
The visible RUNNING H200 jobs are unrelated ltp-axis-eval-platform jobs and must not be reused or stopped for this task without a new PM gate.
```

## Node Shape

Preferred retry allocation:

```text
single node
virtual cluster: h200agentic preferred
gpu: 8 x NVIDIA H200
cpu: around 184
memory: around 2,048,000 MB
shm: around 262,144 MB
infiniband: enabled
container image: known-good previous retry worker image or PM-approved replacement
worker behavior: bootstrap environment, mount filesystems, expose SSH, write nodes JSON, sleep infinity
```

Required mounts/paths after allocation:

```text
/mnt/3fs
/mnt/3fs2
/mnt/cephfs as fuse.ceph-fuse
/root/workspace/coding_agent_playground
/root/workspace/cleaned_m1_sft_10/train.jsonl or PM-approved data-format-fixed replacement
/root/workspace/coding_agent_playground/nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_plan2_nodes.json
```

The LTP bootstrap must not embed SFT execution. dev_4 owns SFT command execution only after PM gate.

## Submit Command Template

Use only after fresh PM gate:

```bash
RETRY_ID="$(date -u +%Y%m%dT%H%M%SZ)"
JOB_NAME="coding-agent-playground-m1-qwen3-8b-retry2-${RETRY_ID}"
LTP_YAML="/tmp/${JOB_NAME}.yaml"

# Build YAML from known-good previous single-node h200agentic worker config.
# Required properties:
# - name: ${JOB_NAME}
# - defaults.virtualCluster: h200agentic unless PM approves h200
# - taskrole.instances: 1
# - resourcePerInstance.gpu: 8
# - command ends in sleep infinity, not SFT
# - no secrets copied into durable evidence

python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Expected submit result:

```text
HTTP 202
frame: xu.yang~coding-agent-playground-m1-qwen3-8b-retry2-<UTC_ID>
```

## Status / SSH Verification Template

```bash
FRAME="xu.yang~coding-agent-playground-m1-qwen3-8b-retry2-<UTC_ID>"

python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py events "${FRAME}" | tail -40
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh "${FRAME}"
```

Endpoint verification:

```bash
ssh -p <PORT> root@<IP> '
  date -u +%Y-%m-%dT%H:%M:%SZ
  hostname
  command -v nvidia-smi
  nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits || true
  findmnt -n -o FSTYPE,SOURCE -T /mnt/cephfs
  test -d /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
  test -w /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
'
```

Staging template after endpoint verification:

```bash
ssh -p 31787 root@10.100.194.40 'tar -C /root/workspace -cf - coding_agent_playground cleaned_m1_sft_10' \
  | ssh -p <PORT> root@<IP> 'mkdir -p /root/workspace && tar -C /root/workspace -xf -'

ssh -p <PORT> root@<IP> 'cat > /root/workspace/coding_agent_playground/nodes.json <<EOF
{"node_count":1,"nodes":[{"ip":"<IP>","port":"<PORT>","user":"root","node_rank":0}]}
EOF
cp /root/workspace/coding_agent_playground/nodes.json /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_plan2_nodes.json'
```

## Stop Command Template

```bash
FRAME="xu.yang~coding-agent-playground-m1-qwen3-8b-retry2-<UTC_ID>"

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
endpoint proof
artifact preservation note
```

## Max Runtime

Recommended runtime limit after allocation:

```text
max_runtime: 60 minutes from LTP started timestamp
idle_limit: 15 minutes without active dev_4 torchrun/python GPU work or fresh retry artifact progress
hard_review: PM-specified time if provided; otherwise allocation_start + 60 minutes
```

If data-format-fixed retry is expected to take longer, PM must record a bounded extension before hard review.

## Stop Conditions

Stop/release the plan2 LTP job when any condition is true:

1. dev_4 records data-format-fixed retry completion and no more same-node retry is needed.
2. dev_4 records retry failure/no-retry.
3. test_1 records retry gate failure/blocker and PM does not authorize same-node follow-up.
4. No active SFT process and no owner progress for 15 minutes after route handoff.
5. GPU route becomes unhealthy, non-idle before handoff, or endpoint becomes unexpectedly unreachable.
6. Max runtime/hard review triggers without bounded extension.
7. PM explicitly orders stop.

Do not stop while active dev_4 torchrun/python GPU work or fresh retry artifacts are progressing unless PM explicitly orders stop.

## Output Preservation

All outputs must be under:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

Expected plan2 artifacts:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_plan2_nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/latest_dev4_sft_retry_plan2_run_id.txt
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RETRY2_RUN_ID>/
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RETRY2_RUN_ID>/
```

LTP stop must release compute only and must not delete `/mnt/3fs` artifacts.

## Current Decision

```text
ready_to_submit: no
reason: PM assigned resource planning only; no fresh PM gate to submit/occupy a GPU node.
current_retry_gpu_active: no
next_action_if_PM_gates: submit a fresh single-node H200-agentic worker, verify/stage endpoint, write retry2 nodes JSON, and begin lifecycle tracking.
```
