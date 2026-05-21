# Session 21 GPU Resource Tracking

Task ID: `M1-S21-RUNTIME-DEV2`

Lifecycle/runtime owner: `intern_code_dev_2`

Created: 2026-05-21T07:12:51Z

## Current State

```text
state: STOPPED_AFTER_FINAL_RUNTIME_FAILURE
active_session21_gpu: no
ltp_submitted_by_dev2_for_session21: yes
sft_run_by_dev2_for_session21: yes
eval_run_by_dev2_for_session21: no
```

Reason:

```text
PM authorized one runtime attempt. The attempt ran and failed during checkpoint save with safetensors ENOSPC; dev_2 stopped and released the LTP frame. No active Session 21 GPU remains.
```

Gate refresh at 2026-05-21T07:16:34Z:

```text
dev_3_s21_datasetinfo_package: present/pass
test_1_s21_launch_gate: present; DATASET_INFO PASS / LAUNCH WIRING BLOCKED in prior dev_2 evidence because DATASET_NAME was stale and PM auth absent
dev_1_s21_launch_review: present; confirms data package/test gate pass and blocks runtime until dev_2 wiring is corrected, PM auth is recorded, fresh endpoint exists, and post-run evidence exists
dev_2_runtime_wiring_refresh: evidence/dev_2_s21_sft_runtime.md now uses accepted dataset entry coding_agent_m1_sft_10_sharegpt in the intended command template
ready_to_submit: no
ready_to_run_sft: no
exact_remaining_blocker: no PM runtime authorization recorded; no fresh Session 21 LTP frame/node/endpoint/nodes.json exists; final generated config proof and endpoint proof can only be recorded after PM-gated allocation/staging.
```

## No Active Milestone 1 Runtime GPU Proof

Refreshed at 2026-05-21T07:21:17Z.

Commands:

```text
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 50 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 50 --json
```

Observed unrelated running H200 jobs:

```text
xu.yang~ltp-axis-eval-platform-a71e4142
xu.yang~ltp-axis-eval-platform-6493743e
xu.yang~ltp-axis-eval-platform-2de3c892
```

These jobs are not named for `coding-agent-playground`, `milestone1`, `m1`, or `s21`; do not reuse or stop them for this task without a new PM gate.

Conclusion:

```text
No active coding_agent_playground / Milestone 1 / Session 21 runtime GPU allocation is visible in RUNNING h200agentic or h200 LTP lists as of 2026-05-21T07:21:17Z.
```

## Intended Runtime Resource

After PM gate only:

```text
job name pattern: coding-agent-playground-m1-s21-qwen3-8b-runtime-<UTC_ID>
frame pattern: xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-<UTC_ID>
node shape: single-node 8 x NVIDIA H200
vc: h200agentic preferred
worker command: bootstrap + sleep infinity, no embedded SFT
expected output root: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
nodes path: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_s21_nodes.json
```

## Command Templates

Submit template, after explicit PM authorization only:

```text
RUNTIME_ID="$(date -u +%Y%m%dT%H%M%SZ)"
JOB_NAME="coding-agent-playground-m1-s21-qwen3-8b-runtime-${RUNTIME_ID}"
LTP_YAML="/tmp/${JOB_NAME}.yaml"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Status:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-<UTC_ID>
```

SSH:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-<UTC_ID>
ssh -p <PORT> root@<IP>
```

Stop:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-<UTC_ID>
```

## Runtime Watch Rules

Do not stop while active dev_2 SFT torchrun/python GPU work or fresh artifact progress is visible, unless PM explicitly orders stop.

Stop when:

1. checkpoint/model path is produced and artifacts are verified;
2. runtime failure is final for the PM-gated attempt;
3. PM/test gate orders stop;
4. endpoint/node becomes unhealthy;
5. 15 minute idle window or 60 minute max runtime triggers without bounded extension.

## Stop Proof Template

```text
stop reason:
stop command:
timestamp UTC:
frame id:
post-stop LTP status:
endpoint proof:
artifact preservation note:
```

## Artifact Preservation

Preserve:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
```

LTP stop must not delete shared `/mnt/3fs` outputs.

## Exact Intended Runtime Command

This command is recorded for PM gate review only. It must not be executed until PM explicitly authorizes runtime and a fresh LTP endpoint is allocated/staged.

```bash
ssh -p <PORT> root@<IP>
cd /root/workspace/coding_agent_playground

DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_s21_qwen3_8b_sft_sharegpt_$(date -u +%Y%m%dT%H%M%SZ) \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Generated config requirement before launch:

```text
dataset: coding_agent_m1_sft_10_sharegpt
```

## Active Allocation And Runtime - 2026-05-21

PM authorization:

```text
Task M1-S21-RUNTIME-DEV2 authorized dev_2 to submit one fresh Session 21 LTP job and run one ShareGPT-fixed Qwen3-8B SFT smoke. No eval was authorized.
```

Allocation:

```text
job: coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
frame: xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
submit_file: /tmp/coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z.yaml
submit_command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z.yaml
submit_result: 202 Accepted
started: 2026-05-21 07:27:06
node: lg-cmc-b7r202-i08u06-h200-000556
endpoint: ssh -p 16126 root@10.100.16.54
```

Node and output proof:

```text
2026-05-21T07:27:28Z: 8 x NVIDIA H200 visible and idle.
2026-05-21T07:28:34Z: /mnt/3fs mounted as fuse.hf3fs and /mnt/3fs/data/ai4ai/outputs/coding_agent_playground writable.
```

Nodes JSON:

```text
path_on_node: /root/workspace/coding_agent_playground/nodes.json
durable_path: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_s21_nodes.json
content: {"node_count":1,"nodes":[{"ip":"10.100.16.54","port":"16126","user":"root","node_rank":0,"hostname":"lg-cmc-b7r202-i08u06-h200-000556"}]}
```

Runtime:

```text
run_id: milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
started_utc: 2026-05-21T07:32:31Z
ended_utc: 2026-05-21T07:35:26Z
exit_status: 1
run_dir: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
log: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z/logs/train_stdout_stderr.log
config: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z/config/qwen3_8b_sft.yaml
checkpoint_root: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
```

Runtime command:

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

Runtime config proof:

```text
dataset: coding_agent_m1_sft_10_sharegpt
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
```

Training progress observed:

```text
dataset loaded: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
format conversion: 10/10
total optimization steps: 2
step progress: 1/2
loss: 2.0884
partial checkpoint save began: checkpoint-1/config.json and three model0_*.safetensors files
forbidden prior signatures absent: KeyError 'from', missing dataset_info, ZeroDivisionError, scheduler warmup assertion
```

Final runtime blocker:

```text
BLOCKED_FINAL_RUNTIME: SFT failed during checkpoint-1 safetensors serialization with ENOSPC: "No space left on device (os error 28)". This produced a partial checkpoint-1 only; trainer_state.json and all_results.json are absent. No checkpoint/model should be handed to eval.
```

Artifact presence:

```text
present:
  run_manifest.json
  config/qwen3_8b_sft.yaml
  logs/train_stdout_stderr.log
  exit_status.txt
  checkpoint_root/checkpoint-1/config.json
  checkpoint_root/checkpoint-1/model0_0.safetensors
  checkpoint_root/checkpoint-1/model0_1.safetensors
  checkpoint_root/checkpoint-1/model0_2.safetensors
  checkpoint_root/trainer_log.jsonl
absent:
  checkpoint-2
  trainer_state.json
  all_results.json
```

Stop proof:

```text
stop_reason: final SFT failure with no authorized same-node retry
stop_command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
stop_sent_utc: 2026-05-21T07:36:31Z
post_stop_ltp_status: STOPPED (Completed)
post_stop_completed: 2026-05-21 07:37:02
endpoint_proof: ssh -p 16126 root@10.100.16.54 refused connection after stop
artifact_preservation_note: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground artifacts were preserved; LTP stop only released compute.
```
