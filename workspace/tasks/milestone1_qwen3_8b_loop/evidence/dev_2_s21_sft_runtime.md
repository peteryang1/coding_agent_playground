# dev_2 Session 21 SFT Runtime Plan / Blocker

Task ID: `M1-S21-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T07:12:51Z

## Scope

Act as replacement resource/runtime owner for the Session 21 ShareGPT-fixed SFT smoke path.

Current state: **blocked with final runtime evidence after the one PM-authorized SFT smoke**.

dev_2 must not submit LTP or run SFT until PM gate confirms:

1. dev_3 package exists and is accepted;
2. test_1 launch gate exists and passes;
3. dev_1 launch review exists and passes;
4. PM explicitly authorizes runtime execution.

No eval was performed. One PM-authorized LTP submit and one SFT smoke were performed later in this file; the LTP worker was stopped and released after final runtime failure evidence was captured.

## Required Inputs Status

Checked at 2026-05-21T07:12:51Z.

```text
evidence/dev_3_s21_datasetinfo_package.md: missing
evidence/test_1_s21_launch_gate.md: missing
evidence/dev_1_s21_launch_review.md: missing
```

Runtime blocker:

```text
BLOCKED_PRE_SUBMIT: Missing Session 21 dev_3 dataset_info package, test_1 launch gate, and dev_1 launch review. Fresh PM authorization is required before LTP submit or SFT execution.
```

Refreshed at 2026-05-21T07:16:34Z after PM gate refresh notice.

```text
evidence/dev_3_s21_datasetinfo_package.md: present; dataset_info package PASS
evidence/test_1_s21_launch_gate.md: present; DATASET_INFO PASS / LAUNCH WIRING BLOCKED
evidence/dev_1_s21_launch_review.md: present; refreshed review says runtime remains BLOCKED until command wiring, PM auth, and fresh endpoint exist
```

Current runtime blocker:

```text
BLOCKED_PRE_SUBMIT: Current inputs now exist, and the accepted dataset_info entry is coding_agent_m1_sft_10_sharegpt. Runtime remains blocked because PM runtime authorization is not recorded and no fresh Session 21 LTP frame/node/endpoint/nodes.json exists. The intended command below has been refreshed to use the accepted dataset entry before any future PM-gated submit/run.
```

## No Active Retry GPU Proof

Refreshed at 2026-05-21T07:21:17Z.

Commands:

```text
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 50 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 50 --json
```

Visible RUNNING H200 jobs:

```text
h200agentic:
  xu.yang~ltp-axis-eval-platform-a71e4142
h200:
  xu.yang~ltp-axis-eval-platform-6493743e
  xu.yang~ltp-axis-eval-platform-2de3c892
```

Conclusion:

```text
No active coding_agent_playground / Milestone 1 / Session 21 retry GPU allocation is running.
Visible running H200 jobs are unrelated ltp-axis-eval-platform jobs and must not be reused or stopped for this task without a new PM gate.
```

## Base Model

Path:

```text
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

Verification command:

```text
ssh -p 31787 root@10.100.194.40 'test -f /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6/config.json && echo base_ok'
```

Result:

```text
base_ok
```

## ShareGPT Artifact

Accepted artifact path:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Verification command:

```text
ssh -p 31787 root@10.100.194.40 'sha256sum /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl /root/workspace/cleaned_m1_sft_10_sharegpt/conversion_summary.json; wc -l /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl; head -1 /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl | cut -c1-500'
```

Result:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2  /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
825f2116168e76158f344768293eff2957ca6217d69ad9a56608275830457ec1  /root/workspace/cleaned_m1_sft_10_sharegpt/conversion_summary.json
10 /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sample includes format_version=coding_agent_playground_sft_v1_sharegpt_messages and messages with from/value keys
```

## Expected Dataset Info Entry

Session 21 dev_3 package is present at `evidence/dev_3_s21_datasetinfo_package.md` and is accepted by `evidence/test_1_s21_launch_gate.md` for the ShareGPT `messages[*].from/value` mapping.

Expected entry name:

```text
coding_agent_m1_sft_10_sharegpt
```

Expected LLamaFactory `dataset_info.json` entry:

```json
{
  "coding_agent_m1_sft_10_sharegpt": {
    "file_name": "/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl",
    "formatting": "sharegpt",
    "columns": {
      "messages": "messages"
    },
    "tags": {
      "role_tag": "from",
      "content_tag": "value",
      "user_tag": "human",
      "assistant_tag": "gpt",
      "system_tag": "system",
      "observation_tag": "tool"
    }
  }
}
```

Expected patch locations after runtime node staging:

```text
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
```

Rationale:

```text
The previous retry failed with KeyError: 'from' because OpenAI role/content messages were parsed by ShareGPT defaults. The accepted ShareGPT artifact uses messages[*].from/value, so the runtime must point LLamaFactory at that artifact and register matching tags.
```

## Intended LTP Node Shape

```text
single node
virtual cluster: h200agentic preferred
gpu: 8 x NVIDIA H200
cpu: around 184
memory: around 2,048,000 MB
shm: around 262,144 MB
infiniband: enabled
worker behavior: bootstrap environment, mount filesystems, expose SSH, write nodes JSON, sleep infinity
```

Required staged paths on runtime node:

```text
/root/workspace/coding_agent_playground
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
/root/workspace/coding_agent_playground/nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_s21_nodes.json
```

## Intended LTP Commands

Submit command template, after fresh PM gate only:

```bash
RUNTIME_ID="$(date -u +%Y%m%dT%H%M%SZ)"
JOB_NAME="coding-agent-playground-m1-s21-qwen3-8b-runtime-${RUNTIME_ID}"
LTP_YAML="/tmp/${JOB_NAME}.yaml"

# Build YAML from known-good single-node h200agentic worker config:
# - name: ${JOB_NAME}
# - defaults.virtualCluster: h200agentic unless PM approves h200
# - taskrole.instances: 1
# - resourcePerInstance.gpu: 8
# - command ends in sleep infinity, not SFT
# - no secrets copied into evidence

python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Status/SSH templates:

```bash
FRAME="xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-<UTC_ID>"

python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py events "${FRAME}" | tail -40
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh "${FRAME}"
```

Stop template:

```bash
FRAME="xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-<UTC_ID>"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"

for i in 1 2 3 4 5 6; do
  date -u +%Y-%m-%dT%H:%M:%SZ
  python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}" || true
  ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p <PORT> root@<IP> 'date -u +%Y-%m-%dT%H:%M:%SZ; hostname; nvidia-smi -L' || echo 'ssh endpoint unavailable'
  sleep 20
done
```

## Staging Template After PM-Gated Allocation

```bash
ssh -p 31787 root@10.100.194.40 'tar -C /root/workspace -cf - coding_agent_playground cleaned_m1_sft_10_sharegpt' \
  | ssh -p <PORT> root@<IP> 'mkdir -p /root/workspace && tar -C /root/workspace -xf -'

ssh -p <PORT> root@<IP> 'cat > /root/workspace/coding_agent_playground/nodes.json <<EOF
{"node_count":1,"nodes":[{"ip":"<IP>","port":"<PORT>","user":"root","node_rank":0}]}
EOF
cp /root/workspace/coding_agent_playground/nodes.json /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_s21_nodes.json'
```

## Exact SFT Command Template

Run only after PM gate, LTP allocation, staging, dataset_info patch, and endpoint verification:

```bash
ssh -p <PORT> root@<IP>
cd /root/workspace/coding_agent_playground

mkdir -p code/LLamaFactory code/mcore_adapter
tar -xf /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz -C code/LLamaFactory --strip-components=1
rsync -a /mnt/3fs/data/ai4ai/deps/mcore_adapter/ code/mcore_adapter/

pip install --break-system-packages -e code/LLamaFactory/ --no-deps
pip install --break-system-packages peft accelerate datasets 'trl<=0.24.0,>=0.18.0'
pip install --break-system-packages /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
pip install --break-system-packages -e code/mcore_adapter/ --no-deps

# Patch dataset_info.json using the PM-gated dev_3 Session 21 entry before running.

DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_s21_qwen3_8b_sft_sharegpt_$(date -u +%Y%m%dT%H%M%SZ) \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

If the existing script does not honor `DATASET_NAME`, runtime must patch the generated config or script to use the PM-gated dataset entry before execution and record the exact diff/command in this evidence. The generated runtime config must contain:

```text
dataset: coding_agent_m1_sft_10_sharegpt
```

## Expected Output Path

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

Expected runtime artifacts:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/run_manifest.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/exit_status.txt
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/trainer_state.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/all_results.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/checkpoint-*/
```

Target outcome after PM-gated execution:

```text
checkpoint/model produced, or fresh exact runtime blocker with logs, command, node status, owner, and next fix.
```

## Runtime Limits And Stop Proof Requirements

Max runtime after allocation:

```text
60 minutes from LTP started timestamp unless PM records a bounded extension
15 minutes idle without active torchrun/python GPU work or fresh artifact progress after route handoff
```

Stop conditions:

1. SFT completes and checkpoint/model/trainer_state/all_results are verified.
2. SFT fails and no PM-authorized same-node retry remains.
3. test_1/PM gates a stop.
4. Node becomes unhealthy, endpoint unreachable unexpectedly, or GPU state diverges from intended route.
5. Idle limit or hard runtime limit triggers without bounded extension.

Stop proof must include:

```text
stop command/action
frame id
timestamp UTC
post-stop LTP status
endpoint proof
artifact preservation note
```

Output preservation:

```text
Do not delete /mnt/3fs/data/ai4ai/outputs/coding_agent_playground.
LTP stop releases compute only.
```

## Current Decision

```text
ready_to_submit: no
ready_to_run_sft: no
blocker: PM runtime authorization is not recorded and no fresh Session 21 LTP frame/node/endpoint/nodes.json exists. Current dev_3 package, test_1 gate, and dev_1 review files exist; dataset_info is accepted as coding_agent_m1_sft_10_sharegpt. The previous dataset-name mismatch has been corrected in this intended command template, but a PM-gated launch still requires final generated config proof and fresh endpoint proof.
fresh_PM_authorization_required_before_submit: yes
```

## Gate Refresh - 2026-05-21T07:16:34Z

Checked current durable files:

```text
sed -n '60,115p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_3_s21_datasetinfo_package.md
sed -n '340,390p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s21_launch_gate.md
sed -n '1,360p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s21_launch_review.md
```

Refresh result:

```text
ready_to_submit: no
ready_to_run_sft: no
dataset_info_package: present/pass
test_1_gate: present; dataset_info pass; launch wiring was blocked on stale dev_2 dataset name and no PM authorization
dev_1_review: present; confirms data package/test gate pass, but runtime blocked until dev_2 wiring is corrected, PM authorization is recorded, fresh endpoint exists, and post-run evidence exists
intended_dataset_name: coding_agent_m1_sft_10_sharegpt
intended_dataset_jsonl: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
intended_dataset_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remaining_blocker: PM runtime authorization is not recorded; no fresh Session 21 LTP job/frame/node/endpoint/nodes.json exists; final generated runtime config cannot be proven until a PM-gated node is allocated and staged.
execution_performed_by_dev2: none
ltp_submitted_by_dev2_for_session21: no
sft_run_by_dev2_for_session21: no
```

## PM-Authorized Runtime Execution - 2026-05-21

Authorization source:

```text
PM authorized intern_code_dev_2 to submit one fresh Session 21 LTP job and run one ShareGPT-fixed Qwen3-8B SFT smoke only for task M1-S21-RUNTIME-DEV2.
```

Successful LTP submit:

```bash
RUNTIME_ID=20260521T072638Z
JOB_NAME=coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
FRAME=xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
LTP_YAML=/tmp/coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z.yaml
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Submit result:

```text
status: 202
message: Update job coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z for user xu.yang successfully.
```

Note: an earlier JSON-form submit for the same intended job returned HTTP 400 `InvalidProtocolError` and did not allocate a resource. The successful allocation was the YAML submit above.

LTP job/node:

```text
frame: xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
job: coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
vc: h200agentic
submitted: 2026-05-21 07:27:00
started: 2026-05-21 07:27:06
node hostname: lg-cmc-b7r202-i08u06-h200-000556
endpoint: ssh -p 16126 root@10.100.16.54
gpu: 8 x NVIDIA H200
```

Node proof at first usable poll:

```text
2026-05-21T07:27:28Z
lg-cmc-b7r202-i08u06-h200-000556
0..7 NVIDIA H200, 0% util, 1 MiB memory each
```

Mount/output proof:

```text
2026-05-21T07:28:34Z
/mnt/cephfs: fuse.ceph-fuse
/mnt/3fs: fuse.hf3fs
/mnt/3fs2: fuse.hf3fs
output_dir_present
output_writable
```

Staged inputs:

```text
/root/workspace/coding_agent_playground
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Nodes JSON path/content:

```text
/root/workspace/coding_agent_playground/nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_s21_nodes.json
{"node_count":1,"nodes":[{"ip":"10.100.16.54","port":"16126","user":"root","node_rank":0,"hostname":"lg-cmc-b7r202-i08u06-h200-000556"}]}
```

Dataset info staged on worker:

```text
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
entry: coding_agent_m1_sft_10_sharegpt
file_name: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
formatting: sharegpt
columns.messages: messages
tags.role_tag: from
tags.content_tag: value
tags.user_tag: human
tags.assistant_tag: gpt
tags.system_tag: system
tags.observation_tag: tool
```

Exact runtime command:

```bash
cd /root/workspace/coding_agent_playground
CONFIG_TEMPLATE=/tmp/qwen3_8b_sft_s21_sharegpt.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Generated runtime config path:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z/config/qwen3_8b_sft.yaml
sha256: 2ec57cce6e73aba4393ee09f8338629146473cb6ea38d54180a5c64d07dd5e0b
```

Generated config proof:

```yaml
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset_dir: data/sft
dataset: coding_agent_m1_sft_10_sharegpt
output_dir: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
```

Run artifacts:

```text
run_id: milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
run_manifest: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z/run_manifest.json
config: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z/config/qwen3_8b_sft.yaml
stdout_stderr_log: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z/logs/train_stdout_stderr.log
exit_status: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z/exit_status.txt
checkpoint_root: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
```

Exit status:

```text
EXIT_STATUS=1
END_UTC=2026-05-21T07:35:26Z
CORRECTION_UTC=2026-05-21T07:36:15Z
CORRECTION_REASON=wrapper initially wrote 0 after failed subprocess; log contains ChildFailedError/CalledProcessError and safetensors No space left on device
```

Runtime result:

```text
SFT failed after real training progress. Data-format blocker is cleared for this run: logs show dataset load, ShareGPT format conversion 10/10, Total optimization steps = 2, step 1/2 loss, and checkpoint-1 save began. No `KeyError: 'from'`, missing dataset_info, ZeroDivisionError, or scheduler assertion signature was found.
```

Failure signature:

```text
safetensors_rust.SafetensorError: Error while serializing: I/O error: No space left on device (os error 28)
torch.distributed.elastic.multiprocessing.errors.ChildFailedError
subprocess.CalledProcessError: torchrun ... returned non-zero exit status 1
```

Artifact presence:

```text
present checkpoint root
present checkpoint-1 partial files:
  checkpoint-1/config.json
  checkpoint-1/model0_0.safetensors 4999854216 bytes
  checkpoint-1/model0_1.safetensors 4983069208 bytes
  checkpoint-1/model0_2.safetensors 32522240 bytes
absent checkpoint-2
absent trainer_state.json
absent all_results.json
```

Checkpoint/model status:

```text
No complete accepted checkpoint/model is available. checkpoint-1 is partial because serialization failed with ENOSPC before full save completion. Do not hand this partial checkpoint to eval.
```

Fresh exact runtime blocker:

```text
BLOCKED_FINAL_RUNTIME: ShareGPT-fixed data path and corrected dataset_info/config reached training and checkpoint save, but model save failed with safetensors ENOSPC during checkpoint-1 serialization. Next fix should address checkpoint output capacity/path or disable/full-model save behavior for this tiny smoke before authorizing another run. No same-node retry is authorized or available; node was released.
```

Stop proof:

```bash
FRAME=xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"
```

Stop action/result:

```text
stop_sent_utc: 2026-05-21T07:36:31Z
post_stop_state: STOPPED (Completed)
completed: 2026-05-21 07:37:02
endpoint proof: ssh -p 16126 root@10.100.16.54 refused connection after stop
artifact preservation: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground was not deleted; run/log/partial checkpoint artifacts remain under the paths above.
```
