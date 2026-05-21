# Dev 4 Session 21 ENOSPC Config / Save-Strategy Fix Package

Task ID: `M1-S21-ENOSPC-CONFIG-FIX-DEV4`

Owner: `intern_code_dev_4`

Created: 2026-05-21T07:54:22Z

Scope: no-execution fix package for the Session 21 Qwen3-8B SFT smoke checkpoint-save blocker.

Execution boundary:

```text
No SFT command was run.
No GPU command was run.
No eval command was run.
This package is a proposed config/save-strategy and output-path fix only.
```

## Session 26 Storage Rule Refresh

Supervisor storage rule now applies to this task:

```text
Future SFT launch outputs, logs, checkpoints, run metadata, temporary converted datasets, and intermediates default to CephFS under /home/xu.yang.
Use /mnt/3fs only for existing required paths, with explicit justification in evidence.
```

This refresh supersedes the Session 25 recommendation that used `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground` as the future output root.

Required-path exceptions that remain valid:

```text
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
  Justification: PM/dev_1 selected clean Qwen3-8B base model candidate; it is an existing required input path, not a new launch output.

/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
  Justification: historical failed-run evidence already exists there; preserve for audit only and do not reuse for future outputs.
```

The ShareGPT training data path remains an existing staged input path:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Future temporary converted datasets or copied training intermediates should be written under the CephFS run tree, not under `/mnt/3fs`.

## Source Failure

Failed run:

```text
run_id: milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
run_dir: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
checkpoint_root: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
exit_status: 1
```

Evidence reviewed:

```text
evidence/dev_2_s21_sft_runtime.md
evidence/gpu_s21_resource_tracking.md
evidence/dev_2_s21_enospc_resource_plan.md
evidence/dev_3_s21_enospc_data_confirm.md
evidence/test_1_s21_enospc_retry_gate.md
```

Positive runtime facts:

```text
dataset entry: coding_agent_m1_sft_10_sharegpt
dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
ShareGPT conversion: 10/10
Total optimization steps: 2
Step progress: 1/2
```

Failure signature:

```text
safetensors_rust.SafetensorError: Error while serializing: I/O error: No space left on device (os error 28)
```

Partial checkpoint files recorded by dev_2:

```text
checkpoint-1/model0_0.safetensors: 4,999,854,216 bytes
checkpoint-1/model0_1.safetensors: 4,983,069,208 bytes
checkpoint-1/model0_2.safetensors: 32,522,240 bytes
checkpoint-1/config.json: 1,538 bytes
```

Conclusion:

```text
The data-format blocker is cleared for this run. The failure moved to checkpoint serialization capacity/path behavior. The partial checkpoint-1 is not an accepted model/checkpoint and must not be used for mini-swe eval.
```

## Dataset Contract To Preserve

The retry must keep the accepted ShareGPT dataset entry:

```text
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
```

Required generated runtime config property:

```yaml
dataset: coding_agent_m1_sft_10_sharegpt
```

Required `dataset_info.json` entry shape:

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

Do not switch back to the old OpenAI-style `role/content` JSONL for this ENOSPC fix. dev_3's data confirmation records no data-side change is needed.

## Recommended Fix

Primary recommendation: **capacity-verified durable output path plus one final save only**.

Rationale:

- The failed config saved at `save_steps: 1` in a `max_steps: 2` smoke, so it attempted a large full-model checkpoint after the first step.
- The checkpoint write failed after about 9.4G of partial safetensors under `checkpoint-1`.
- The milestone still needs a complete model/checkpoint for mini-swe, so a metrics-only smoke with all saving disabled is not the primary fix.
- The next authorized retry should avoid the step-1 intermediate save and write exactly one complete model checkpoint to a fresh capacity-proven directory.

Config changes for the next retry template:

```yaml
### dataset
dataset: coding_agent_m1_sft_10_sharegpt

### output
logging_steps: 1
save_steps: 2
save_total_limit: 1
overwrite_output_dir: false
save_only_model: true
save_hf_model: true

### train
max_steps: 2
warmup_steps: 0

### megatron parallelism
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
context_parallel_size: 1
sequence_parallel: false
```

Operational output-path requirement:

```text
Use a new unique RUN_ID and a new empty CHECKPOINT_DIR.
Do not reuse or append to milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z.
Do not delete the failed partial checkpoint unless PM explicitly approves cleanup.
```

Preferred durable output root, superseding the prior `/mnt/3fs` recommendation:

```text
/home/xu.yang/coding_agent_playground/outputs
```

CephFS run tree:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>
/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>
```

`/mnt/3fs` and `/mnt/3fs2` are not recommended future output roots for this retry. Use them only for the required-path exceptions listed above or after a new PM/supervisor storage decision.

## Exact Future Command Template

This is a no-execution command package. Run only after PM retry authorization, fresh endpoint, capacity proof, and test/review gates.

```bash
RUN_ID="milestone1_qwen3_8b_s21_enospcfix_sharegpt_tp8_$(date -u +%Y%m%dT%H%M%SZ)"
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
CHECKPOINT_DIR="${OUTPUT_ROOT}/training_summary/sft_output/${RUN_ID}"
TMPDIR="${OUTPUT_ROOT}/tmp/${RUN_ID}"

CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT="${OUTPUT_ROOT}" \
CHECKPOINT_DIR="${CHECKPOINT_DIR}" \
TMPDIR="${TMPDIR}" \
RUN_ID="${RUN_ID}" \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Expected generated runtime config proof:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
```

Required config assertions:

```text
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
save_steps: 2
save_total_limit: 1
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
```

## Required Capacity Evidence Before Launch

dev_2's resource plan should be treated as a pre-run gate input. The retry launcher should not proceed unless the future node records capacity proof for the exact output tree.

Minimum required commands on the future allocated node:

```bash
set -euo pipefail
RUN_ID="milestone1_qwen3_8b_s21_enospcfix_sharegpt_tp8_<UTC>"
OUT=/home/xu.yang/coding_agent_playground/outputs
CKPT="${OUT}/training_summary/sft_output/${RUN_ID}"
PROBE="${OUT}/capacity_probes/${RUN_ID}"
TMP="${OUT}/tmp/${RUN_ID}"

date -u +%Y-%m-%dT%H:%M:%SZ
findmnt -n -o FSTYPE,SOURCE -T /home/xu.yang
df -h /home/xu.yang "${OUT}"
df -i /home/xu.yang "${OUT}" || true
mkdir -p "${CKPT}" "${PROBE}" "${TMP}"
test -w "${OUT}"
test -w "${CKPT}"
test -w "${PROBE}"
test -w "${TMP}"

for i in 0 1 2 3; do
  dd if=/dev/zero of="${PROBE}/probe_${i}.bin" bs=1G count=6 status=progress conv=fsync
done
sync
ls -lh "${PROBE}"
rm -f "${PROBE}"/probe_*.bin
rmdir "${PROBE}" || true
```

Capacity gate:

```text
The 24G real-write probe must pass in the CephFS output tree before SFT launch. If PM/test require stronger proof, use the dev_2 48G probe variant before launch, but target /home/xu.yang rather than /mnt/3fs.
```

## Files / PR Needed

No code or config was patched by this task. If PM wants a repository PR before retry, use task id `M1-S21-ENOSPC-CONFIG-FIX-DEV4` and include these scoped changes:

```text
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
```

Required content:

```yaml
dataset: coding_agent_m1_sft_10_sharegpt
save_steps: 2
save_total_limit: 1
overwrite_output_dir: false
save_only_model: true
save_hf_model: true
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
```

Recommended script hardening for the same PR or a follow-up task:

```text
scripts/train_qwen3_8b_sft.sh
```

Change requested:

```text
If DATASET_NAME is set, rewrite the top-level `dataset:` field in the runtime config to DATASET_NAME. Current script rewrites model_name_or_path and output_dir only, so dev_2 had to rely on a temporary config template for the accepted ShareGPT dataset entry.
```

Recommended manifest hardening:

```text
scripts/write_sft_run_manifest.py
```

Change requested:

```text
Record save_steps/save_total_limit/save_only_model/save_hf_model/CHECKPOINT_DIR from the actual runtime config instead of static manifest defaults that still describe save_steps=150 and save_total_limit=4.
```

## Fallback Option

Fallback if PM accepts a training-only smoke without an eval-usable model:

```yaml
save_strategy: "no"
save_only_model: false
save_hf_model: false
```

This fallback is not recommended as the primary milestone path because mini-swe remains blocked without a complete checkpoint/model or served endpoint.

## Rollback / Stop Conditions

Do not launch if any of these are true:

```text
capacity probe fails
generated config does not contain dataset: coding_agent_m1_sft_10_sharegpt
generated config saves at step 1 again
generated config uses the failed run id or failed checkpoint directory
dataset checksum differs from 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
PM retry authorization is absent
```

Stop after launch if:

```text
ENOSPC recurs
old data-format errors recur, including KeyError: 'from' or missing dataset_info
ZeroDivisionError / steps_in_epoch recurs
Megatron warmup scheduler assertion recurs
node endpoint becomes unhealthy
runtime exceeds the PM/test bounded window
```

## Current Completion Marker

```text
Complete-for-plan: M1-S21-ENOSPC-CONFIG-FIX-DEV4 records a no-execution fix package. Recommended primary fix is a capacity-verified durable output path with a fresh RUN_ID plus save_steps=2/save_total_limit=1 so the max_steps=2 smoke avoids the step-1 full checkpoint save and still targets one complete eval-usable checkpoint/model. Dataset entry coding_agent_m1_sft_10_sharegpt is preserved. No SFT/GPU/eval command was run.
```

Session 26 storage-rule refresh:

```text
Superseded output root: /mnt/3fs/data/ai4ai/outputs/coding_agent_playground
Current output root recommendation: /home/xu.yang/coding_agent_playground/outputs
Future logs/checkpoints/run metadata/tmp converted datasets/intermediates must default under /home/xu.yang. /mnt/3fs remains allowed only for existing required input/audit paths with the justifications recorded above.
```
