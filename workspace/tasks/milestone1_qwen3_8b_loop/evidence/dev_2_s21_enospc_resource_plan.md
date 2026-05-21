# dev_2 Session 21 ENOSPC Resource / Capacity Plan

Task ID: `M1-S21-ENOSPC-RESOURCE-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T07:51:35Z

Storage rule updated: 2026-05-21T08:00:00Z

Scope: no-submit resource/capacity plan for the Session 21 safetensors ENOSPC checkpoint-save blocker.

Execution boundary:

```text
No LTP submit was performed for this task.
No GPU was allocated.
No SFT was run.
No eval was run.
Fresh PM authorization is required before any LTP submit or retry execution.
```

## Supervisor Storage Rule

Effective immediately for future `M1-S21-ENOSPC-RESOURCE-DEV2` LTP/GPU owner work:

```text
Default storage root for SFT intermediates, capacity probes, output roots, checkpoint dirs, logs, run metadata, stop proof, and runtime evidence on future LTP/GPU nodes:
/home/xu.yang/coding_agent_playground
```

Default future paths:

```text
output_root: /home/xu.yang/coding_agent_playground/outputs
run_metadata_root: /home/xu.yang/coding_agent_playground/outputs/runs/train
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output
logs_root: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs
capacity_probe_root: /home/xu.yang/coding_agent_playground/outputs/capacity_probes
stop_proof_root: /home/xu.yang/coding_agent_playground/outputs/resource_tracking
nodes_json: /home/xu.yang/coding_agent_playground/outputs/milestone1_s21_nodes.json
```

Exception rule:

```text
Use /mnt/3fs only for existing required paths or explicit PM/test/eval compatibility mirrors, and record the justification next to each exception. Do not default future probes/checkpoints/logs/metadata to /mnt/3fs.
```

Existing required path exceptions and justification:

```text
1. Historical failed-run evidence remains under /mnt/3fs/data/ai4ai/outputs/coding_agent_playground because that is where the already-run Session 21 artifacts were written and referenced by PM/test evidence.
2. If downstream PM/test/eval tooling still requires a /mnt/3fs handoff path, mirror small metadata files only, such as nodes.json, run_manifest.json, exit_status.txt, and stop proof summaries. Justification: compatibility with existing milestone evidence paths. Do not mirror large checkpoints by default unless PM explicitly requires it.
3. Base model and dependency paths under /mnt/3fs/data/ai4ai are existing required read-only inputs, not future output/checkpoint/probe targets.
```

## Source Failure

Failed run:

```text
run_id: milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
run_dir: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
checkpoint_root: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
exit_status: 1
```

Runtime reached real training and checkpoint save:

```text
ShareGPT conversion: 10/10
Total optimization steps: 2
Step progress: 1/2
Loss observed: 2.0884
Partial checkpoint directory: checkpoint-1
```

Failure signature:

```text
safetensors_rust.SafetensorError: Error while serializing: I/O error: No space left on device (os error 28)
```

## Checks Performed

Commands checked from the PM worktree host against durable `/mnt/3fs` artifacts:

```bash
RUN_ID=milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
OUT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
CKPT="${OUT}/training_summary/sft_output/${RUN_ID}"
RUN="${OUT}/runs/train/${RUN_ID}"

date -u +%Y-%m-%dT%H:%M:%SZ
df -h /mnt/3fs "${OUT}" "${CKPT}"
df -i /mnt/3fs "${OUT}" "${CKPT}"
du -sh "${RUN}" "${CKPT}"
find "${CKPT}" -maxdepth 2 -type f -printf '%s %p\n' | sort -nr | head -20
grep -n "No space left on device\\|safetensors\\|checkpoint-1\\|EXIT_STATUS" "${RUN}/logs/train_stdout_stderr.log" | tail -40
cat "${RUN}/exit_status.txt"
```

Observed at 2026-05-21T07:51:35Z:

```text
/mnt/3fs filesystem: hf3fs.stage
size: 950T
used: 900T
available: 51T
use%: 95%
inode reporting: 0/0/0, not useful for capacity diagnosis on hf3fs
run_dir size: 920K
checkpoint_root size: 9.4G
exit_status: EXIT_STATUS=1
```

Partial checkpoint files:

```text
checkpoint-1/model0_0.safetensors: 4,999,854,216 bytes
checkpoint-1/model0_1.safetensors: 4,983,069,208 bytes
checkpoint-1/model0_2.safetensors: 32,522,240 bytes
checkpoint-1/config.json: 1,538 bytes
trainer_log.jsonl: 161 bytes
```

## Capacity Diagnosis

Current conclusion: **not proven to be global `/mnt/3fs` free-space exhaustion**.

Reasoning:

```text
df shows 51T available on /mnt/3fs at the durable artifact path after the failure.
The failed checkpoint root contains only 9.4G of partial output.
The safetensors write failed while serializing model shards into checkpoint-1, after two approximately 5G shards and one small shard were written.
```

Most likely resource/capacity classes to rule out before retry:

```text
1. Path-specific hf3fs quota, object limit, file count limit, or write policy not visible through normal df.
2. Transient hf3fs ENOSPC / backend allocation failure while writing large safetensors.
3. Checkpoint save behavior writing multiple full HF shards into a crowded /mnt/3fs output tree.
4. Local temporary or staging behavior inside safetensors/MCA that reports ENOSPC while final path is on /mnt/3fs.
```

The ENOSPC was triggered at the configured checkpoint path:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/checkpoint-1
```

Do not hand the partial `checkpoint-1` to eval.

## Recommended Safe Output Strategy

Preferred resource-side retry plan after PM/test/config gate:

```text
Keep future SFT intermediates, probes, logs, run metadata, checkpoints, and stop proof under CephFS /home/xu.yang/coding_agent_playground by default.
Use a new, empty, unique run id and checkpoint directory.
Before training, run explicit write/capacity probes in the exact intended checkpoint parent.
Do not reuse or append to the failed checkpoint directory.
Do not delete the failed partial checkpoint unless PM explicitly authorizes cleanup.
Mirror only small compatibility metadata to existing required /mnt/3fs paths if PM/test/eval requires them.
```

Recommended output root:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Recommended retry run id pattern:

```text
milestone1_qwen3_8b_s21_enospcfix_sharegpt_tp8_<UTC>
```

Recommended checkpoint directory:

```text
/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
```

Compatibility mirror, only if PM/test/eval requires existing `/mnt/3fs` evidence paths:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/run_manifest.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/exit_status.txt
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/logs/stop_proof_summary.txt
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_s21_nodes.json
```

Compatibility mirror caveat:

```text
These /mnt/3fs paths are exceptions for existing milestone evidence consumers. The authoritative future SFT outputs/checkpoints/logs/probes should remain under /home/xu.yang unless PM explicitly authorizes a different path.
```

## Required Capacity Checks Before Any Retry

Run these on the future allocated node before launching SFT:

```bash
set -euo pipefail
RUN_ID="milestone1_qwen3_8b_s21_enospcfix_sharegpt_tp8_$(date -u +%Y%m%dT%H%M%SZ)"
OUT=/home/xu.yang/coding_agent_playground/outputs
CKPT="${OUT}/training_summary/sft_output/${RUN_ID}"
PROBE="${OUT}/capacity_probes/${RUN_ID}"
MIRROR=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground

date -u +%Y-%m-%dT%H:%M:%SZ
findmnt -n -o FSTYPE,SOURCE -T /home/xu.yang
df -h /home/xu.yang "${OUT}" || true
df -i /home/xu.yang "${OUT}" || true
mkdir -p "${CKPT}" "${PROBE}"
test -w "${OUT}"
test -w "${CKPT}"
test -w "${PROBE}"

# Existing required path exception check, metadata mirror only if PM/test/eval requires it.
findmnt -n -o FSTYPE,SOURCE -T /mnt/3fs || true
test -d "${MIRROR}" && test -w "${MIRROR}" || true
```

Recommended large-write probe:

```bash
# Use real writes, not sparse files. Remove probe files after checks pass.
for i in 0 1 2 3; do
  dd if=/dev/zero of="${PROBE}/probe_${i}.bin" bs=1G count=6 status=progress conv=fsync
done
sync
ls -lh "${PROBE}"
rm -f "${PROBE}"/probe_*.bin
rmdir "${PROBE}" || true
```

Rationale:

```text
The failed checkpoint reached about 9.4G before ENOSPC. A 24G real-write probe in the future default CephFS output tree is a minimal resource-side check that the next run can write more than the observed failure point before occupying GPU for training.
```

If PM/test wants stronger proof before GPU launch, use:

```bash
for i in 0 1 2 3 4 5; do
  dd if=/dev/zero of="${PROBE}/probe_${i}.bin" bs=1G count=8 status=progress conv=fsync
done
sync
rm -f "${PROBE}"/probe_*.bin
rmdir "${PROBE}" || true
```

This writes 48G, closer to a plausible full-model checkpoint budget for Qwen3-8B HF shards plus overhead. Run it under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes`, not `/mnt/3fs`, unless PM explicitly requests a `/mnt/3fs` compatibility probe.

## Cleanup Plan

No cleanup was performed for this planning task.

Before any retry, PM should decide whether to preserve or remove failed partial output:

```text
Preserve for evidence:
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
```

Recommended default:

```text
Do not delete the failed partial checkpoint until test_1/PM finish auditing the ENOSPC evidence.
Use a fresh RUN_ID and fresh checkpoint path for any retry.
```

Optional cleanup after PM approval:

```bash
FAILED_RUN_ID=milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
FAILED_CKPT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/${FAILED_RUN_ID}
du -sh "${FAILED_CKPT}"
# PM-approved only:
# rm -rf "${FAILED_CKPT}/checkpoint-1"
```

## LTP Resource Template

No LTP submit is authorized from this task.

Future submit template after PM authorization only:

```bash
RUNTIME_ID="$(date -u +%Y%m%dT%H%M%SZ)"
JOB_NAME="coding-agent-playground-m1-s21-enospcfix-qwen3-8b-runtime-${RUNTIME_ID}"
FRAME="xu.yang~${JOB_NAME}"
LTP_YAML="/tmp/${JOB_NAME}.yaml"

# Build from known-good single-node H200 worker shape:
# - defaults.virtualCluster: h200agentic
# - taskrole.instances: 1
# - resourcePerInstance.gpu: 8
# - resourcePerInstance.cpu: 184
# - resourcePerInstance.memoryMB: 2048000
# - extraContainerOptions.shmMB: 262144
# - infiniband: true
# - command ends in sleep infinity, not SFT

python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Status template:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py events "${FRAME}" | tail -40
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh "${FRAME}"
```

Stop template:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"
for i in 1 2 3 4 5 6; do
  date -u +%Y-%m-%dT%H:%M:%SZ
  python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}" || true
  ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 -p <PORT> root@<IP> 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; nvidia-smi -L' || echo 'ssh endpoint unavailable'
  sleep 20
done
```

Stop conditions for any PM-authorized retry:

```text
1. Complete checkpoint/model is produced and artifact presence is verified.
2. Runtime fails with no PM-authorized same-node retry.
3. Capacity probe fails before launch.
4. Node becomes unhealthy or endpoint disappears unexpectedly.
5. 15 minutes idle without progress after launch.
6. 60 minute max runtime unless PM records a bounded extension.
```

## Runtime Handoff Requirements

Before SFT launch on any future node, dev_2 must record:

```text
LTP frame/job id
node hostname
ssh endpoint
nodes.json path and content
/home/xu.yang mount/path proof
CephFS output path write proof
capacity probe command and result
exact output/checkpoint path
any /mnt/3fs exception mirror path and justification, if used
exact SFT command/config from dev_4/test_1 gate
stop proof plan
```

## Current Completion Marker

```text
task_id: M1-S21-ENOSPC-RESOURCE-DEV2
owner: intern_code_dev_2
status: complete-for-plan
evidence: evidence/dev_2_s21_enospc_resource_plan.md
ltp_submitted: false
gpu_occupied: false
sft_run: false
eval_run: false
remaining_gate: PM authorization plus dev_4 config/save fix, dev_3 data confirmation, dev_1 review, and test_1 ENOSPC retry gate before any retry.
storage_rule: future LTP/GPU owner SFT intermediates, capacity probes, output roots, checkpoint dirs, logs, run metadata, stop proof, and evidence default to CephFS /home/xu.yang/coding_agent_playground; /mnt/3fs is exception-only for existing required paths with written justification.
```
