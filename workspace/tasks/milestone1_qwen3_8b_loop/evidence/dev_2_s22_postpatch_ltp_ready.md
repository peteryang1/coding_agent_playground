# dev_2 Session 22 Post-Patch LTP Readiness

Task ID: `M1-S22-POSTPATCH-LTP-READY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T08:56:37Z

Scope: refresh post-patch LTP readiness only. This task does not submit LTP, occupy GPU, run SFT, or run eval.

## Execution Boundary

```text
ltp_submit_performed: false
gpu_occupied: false
sft_run: false
eval_run: false
fresh_PM_authorization_required_before_submit: true
```

No job may be submitted for this post-patch path until PM explicitly authorizes a fresh runtime execution task after the post-patch gates.

## No Active Milestone GPU Proof

Checked at 2026-05-21T08:56:37Z.

Commands:

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 100 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 100 --json
```

Prior S22 runtime frame:

```text
frame: xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
state: STOPPED (Completed)
execType: STOP
submitted: 2026-05-21 08:20:48
started: 2026-05-21 08:20:53
completed: 2026-05-21 08:30:26
task idx 0: STOPPED
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
No active coding_agent_playground / Milestone 1 / S22 post-patch GPU allocation is running.
Visible RUNNING H200 jobs are unrelated ltp-axis-eval-platform allocations and must not be reused, modified, or stopped for this task.
```

## Intended H200 Shape

Use the previously proven single-node worker shape only after fresh PM authorization:

```text
virtualCluster: h200agentic preferred
instances: 1
gpu: 8 x NVIDIA H200
cpu: 184
memoryMB: 2048000
shmMB: 262144
infiniband: true
container image: registry-tmp.zhilicon.com:5000/leejunjie/sglang-mcore:cu130-sgl0.5.9-mcore0.16
worker command: bootstrap mounts/environment and sleep infinity; do not put SFT in LTP startup command
```

## Submit Template

Template only. Do not run without fresh PM authorization.

```bash
RUNTIME_ID="$(date -u +%Y%m%dT%H%M%SZ)"
JOB_NAME="coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-${RUNTIME_ID}"
FRAME="xu.yang~${JOB_NAME}"
LTP_YAML="/tmp/${JOB_NAME}.yaml"

# Build YAML from the known-good single-node h200agentic worker config:
# - defaults.virtualCluster: h200agentic
# - taskRoles.taskrole.instances: 1
# - resourcePerInstance.gpu: 8
# - resourcePerInstance.cpu: 184
# - resourcePerInstance.memoryMB: 2048000
# - extraContainerOptions.shmMB: 262144
# - extraContainerOptions.infiniband: true
# - command ends in sleep infinity

python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

JSON submit caveat:

```text
The prior S22 runtime JSON submit returned HTTP 400 InvalidProtocolError, while YAML submit succeeded. Use YAML for the next PM-authorized submit unless LTP tooling changes.
```

## Status / SSH Template

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py events "${FRAME}" | tail -80
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py logs "${FRAME}" | tail -160
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh "${FRAME}"
```

Expected SSH endpoint form:

```text
ssh -p <PORT> root@<IP>
```

## Stop Template

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"
for i in 1 2 3 4 5 6; do
  date -u +%Y-%m-%dT%H:%M:%SZ
  python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}" || true
  ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 -p <PORT> root@<IP> 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; nvidia-smi -L' || echo 'ssh endpoint unavailable'
  sleep 20
done
```

Stop after:

```text
complete checkpoint/model produced
SFT failure with no authorized same-node retry
failed capacity probe
idle/health limit
PM/test stop instruction
```

## Storage And Path Rules

Required default storage root for all future post-patch runtime outputs:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Expected path layout:

```text
output_root: /home/xu.yang/coding_agent_playground/outputs
capacity_probe_root: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>
run_metadata_root: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>
logs: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
runtime_config: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
exit_status: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/exit_status.txt
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
nodes_json: /home/xu.yang/coding_agent_playground/outputs/milestone1_s22_postpatch_nodes.json
stop_proof: /home/xu.yang/coding_agent_playground/outputs/resource_tracking/<RUN_ID>/stop_proof.txt
```

Existing required path exceptions:

```text
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dependency archives/wheels: /mnt/3fs/data/ai4ai/deps
source data input: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
justification: required read-only inputs or source artifact locations; not output/log/checkpoint/probe/run metadata targets.
```

## Capacity Probe Plan

Run only on a future PM-authorized node before SFT launch:

```bash
set -euo pipefail
RUN_ID="milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_$(date -u +%Y%m%dT%H%M%SZ)"
OUT=/home/xu.yang/coding_agent_playground/outputs
PROBE="${OUT}/capacity_probes/${RUN_ID}"
CKPT="${OUT}/training_summary/sft_output/${RUN_ID}"

date -u +%Y-%m-%dT%H:%M:%SZ
readlink -f /home/xu.yang || true
findmnt -n -o TARGET,FSTYPE,SOURCE -T /home/xu.yang
mkdir -p "${OUT}" "${PROBE}" "${CKPT}"
test -w "${OUT}"
test -w "${PROBE}"
test -w "${CKPT}"
df -h /home/xu.yang "${OUT}" "${PROBE}" "${CKPT}"
df -i /home/xu.yang "${OUT}" "${PROBE}" "${CKPT}" || true

for i in 0 1 2 3; do
  dd if=/dev/zero of="${PROBE}/probe_${i}.bin" bs=1G count=6 status=progress conv=fsync
  ls -lh "${PROBE}/probe_${i}.bin"
done
sync
du -sb "${PROBE}"
rm -f "${PROBE}"/probe_*.bin
rmdir "${PROBE}"
echo "PROBE_STATUS=PASS"
```

Minimum pass condition:

```text
24GiB real writes under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>, fsync completed, files verified, and probe files cleaned.
```

## Intended SFT Runtime Parameters

Use only after PM authorizes a runtime task:

```text
dataset: coding_agent_m1_sft_10_sharegpt
source dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
save_steps: 2
save_total_limit: 1
max_steps: 2
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
output root: /home/xu.yang/coding_agent_playground/outputs
```

## Completion Marker

```text
task_id: M1-S22-POSTPATCH-LTP-READY-DEV2
owner: intern_code_dev_2
status: complete-for-readiness
ltp_submit_performed: false
gpu_occupied: false
sft_run: false
eval_run: false
fresh_PM_authorization_required_before_submit: true
```
