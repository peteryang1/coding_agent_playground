# Dev 4 SFT Retry Run Evidence

Task ID: `M1-SFT-RETRY-RUN-DEV4`
Owner: `intern_code_dev_4`
Status: blocked-with-final-evidence after exactly one retry attempt
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_retry_run.md`

## Assignment

PM assigned dev_4 to run exactly one Qwen3-8B SFT retry after dev_2 provided a fresh endpoint/node.

Constraints:

- Use merged config: `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`.
- Use PM-approved original data unless dev_3/test_1 records a blocker: `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Do not perform extra retries without a new PM gate.
- Do not peer-send routine status to PM.

## Gate Inputs Used

PM authorization:

```text
task: M1-SFT-RETRY-AUTH-PM
PR #29 mergedAt: 2026-05-20T11:02:32Z
merge commit: c14fa045b210a74fc243f2d2690a2523cc7ec2db
```

Fresh dev_2 endpoint evidence:

```text
source: /work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_gpu_retry_submit.md
tracking: /work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_retry_resource_tracking.md
endpoint: ssh -p 23121 root@10.100.22.53
node: lg-cmc-b7r202-r05u16-h200-000747
frame: xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
hard review: 2026-05-20T12:06:20Z
```

## Pre-Run Verification

Pre-run verification was executed on `ssh -p 23121 root@10.100.22.53`.

Result summary:

```text
timestamp_utc: 2026-05-20T11:18:05Z
hostname: lg-cmc-b7r202-r05u16-h200-000747
gpu: 8 x NVIDIA H200, 143771 MiB each
gpu memory before launch: 1 MiB used per GPU
gpu utilization before launch: 0% on all 8 GPUs
dataset: /root/workspace/cleaned_m1_sft_10/train.jsonl
dataset sha256: 5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
dataset rows: 10
dataset schema: coding_agent_playground_sft_v1
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
base shape: qwen3, 36 layers, hidden size 4096, vocab size 151936
config gate: TP=8, gradient_accumulation_steps=1, max_steps=2, warmup_steps=0, save_steps=1
nodes.json: /root/workspace/coding_agent_playground/nodes.json -> 10.100.22.53:23121 rank 0
LLamaFactory: 0.9.5.dev0
dependency gate: flash_attn and mcore_adapter import OK
```

Remote staging repair before launch:

```text
copied config to /root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
materialized /root/workspace/coding_agent_playground/code/LLamaFactory from /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz
installed mcore_adapter-0.9.0, flash_attn-2.8.3, trl 0.24.0, peft 0.18.1, and editable LLamaFactory
registered dataset under code/LLamaFactory/data/sft/dataset_info.json
```

This staging repair happened before the SFT command and is not counted as a retry attempt.

## One Retry Attempt

Run ID:

```text
milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z
```

Exact command:

```bash
cd /root/workspace/coding_agent_playground
RUN_ID=milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
RUN_DIR=${OUTPUT_ROOT}/runs/train/${RUN_ID}
mkdir -p ${RUN_DIR}/logs
printf "%s\n" "$RUN_ID" > ${OUTPUT_ROOT}/latest_dev4_sft_retry_run_id.txt
export CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
export DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl
export BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
export OUTPUT_ROOT=${OUTPUT_ROOT}
export LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory
export RUN_ID=${RUN_ID}
export DRY_RUN=0
{
  echo "RUN_ID=${RUN_ID}"
  echo "START_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "COMMAND=CONFIG_TEMPLATE=${CONFIG_TEMPLATE} DATASET_JSONL=${DATASET_JSONL} BASE_MODEL=${BASE_MODEL} OUTPUT_ROOT=${OUTPUT_ROOT} LLAMAFACTORY_DIR=${LLAMAFACTORY_DIR} RUN_ID=${RUN_ID} DRY_RUN=0 bash scripts/train_qwen3_8b_sft.sh"
  bash scripts/train_qwen3_8b_sft.sh
} 2>&1 | tee ${RUN_DIR}/logs/train_stdout_stderr.log
status=${PIPESTATUS[0]}
echo "EXIT_STATUS=${status}" | tee ${RUN_DIR}/exit_status.txt
echo "END_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a ${RUN_DIR}/exit_status.txt
exit ${status}
```

Exit status:

```text
EXIT_STATUS=1
END_UTC=2026-05-20T11:19:30Z
```

## Artifacts

Present:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/latest_dev4_sft_retry_run_id.txt
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/run_manifest.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/config/qwen3_8b_sft.yaml
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/logs/train_stdout_stderr.log
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/exit_status.txt
```

Absent:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/trainer_state.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/all_results.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/checkpoint-*
model files under /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/
```

Post-run GPU/process check:

```text
timestamp_utc: 2026-05-20T11:19:47Z
gpu memory after exit: 1 MiB used per GPU
gpu utilization after exit: 0% on all 8 GPUs
active torchrun/llamafactory/launcher.py workload: none visible
endpoint recheck at 2026-05-20T11:23:57Z: ssh -p 23121 root@10.100.22.53 refused connection
```

## Failure

Failure signature:

```text
KeyError: 'from'
```

Log context:

```text
Loading dataset milestone1_coding_agent_sft.jsonl...
Generating train split: 10 examples
Converting format of dataset (num_proc=4)
File "/root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/data/converter.py", line 151, in __call__
  and messages[0][self.dataset_attr.role_tag] == self.dataset_attr.system_tag
KeyError: 'from'
```

Interpretation:

- The retry reached LLamaFactory distributed launch and dataset conversion.
- The previous DP=8 `steps_in_epoch=0` failure and TP=8 one-step scheduler assertion were not re-hit before this failure.
- The current blocker is data registration/format mapping: the PM-approved JSONL uses OpenAI-style `messages` with role/content fields, while the runtime LLamaFactory dataset registration used ShareGPT defaults that expect `from`/`value`.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` was produced.

## Resource Recommendation

dev_4 recommends dev_2 stop the active H200 resource immediately.

Reason:

- The single authorized retry has completed with exit status 1.
- No extra retry is authorized without a new PM gate.
- The failure is a data-format/LLamaFactory registration issue, not a live resource issue.
- Post-run GPU state was idle before the endpoint later refused SSH; output artifacts are preserved under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.

## Stop / No-Extra-Retry Rule

- Exactly one retry attempt was performed.
- No second training command was launched.
- A future retry requires explicit PM authorization and should fix the LLamaFactory dataset registration for OpenAI-style role/content messages or produce a PM-approved ShareGPT-format training JSONL.
