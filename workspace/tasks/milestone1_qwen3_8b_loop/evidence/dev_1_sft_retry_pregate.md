# Dev 1 SFT Retry Pregate Review

Owner: `intern_code_dev_1`
Task ID: `M1-SFT-RETRY-PREGATE-DEV1`
Date: 2026-05-20
Scope: independent pre-run sanity review of PR #26/#27 config fix, test_1 retry gate, dev_2 resource plan, and dev_3 data gate. No remote experiments were run.

## Sources Reviewed

- PR #26: `https://github.com/peteryang1/coding_agent_playground/pull/26`
- PR #27: `https://github.com/peteryang1/coding_agent_playground/pull/27`
- `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`
- `scripts/train_qwen3_8b_sft.sh`
- `evidence/dev_4_sft_config_fix_plan.md`
- `evidence/test_1_sft_retry_gate.md`
- `evidence/dev_2_gpu_retry_resource_plan.md`
- `evidence/dev_3_sft_data_mitigation.md`
- `task_registry.md`
- `assignments.md`
- `status.md`

## PR #26 / #27 Mapping

PR #26:

- Task ID: `M1-SFT-CONFIG-FIX-DEV4`
- Owner: `intern_code_dev_4`
- State: merged.
- `mergedAt`: `2026-05-20T10:44:55Z`
- Merge commit: `6a704f842c992f83a8d86167dfe870fa6ff72440`
- Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_config_fix_plan.md`
- Completion marker in registry: ready-for-retry.

PR #27:

- Task ID: `M1-SFT-CONFIG-FIX-DEV4`
- Owner: `intern_code_dev_4`
- State: merged.
- `mergedAt`: `2026-05-20T10:47:11Z`
- Merge commit: `9052693e5e3e03a0c9340a01f443164fdb03162d`
- Purpose: completion record for PR #26.
- Completion marker in registry: ready-for-retry.

Mapping verdict: pass. PR #26/#27 cite task id, owner, acceptance criteria, durable evidence, and completion marker.

## Config Fix Sanity

Config reviewed:

```text
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
```

Relevant values:

```text
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
context_parallel_size: 1
per_device_train_batch_size: 1
gradient_accumulation_steps: 1
max_steps: 2
warmup_steps: 0
save_steps: 1
logging_steps: 1
dataloader_num_workers: 0
```

Sanity check:

- Addresses prior DP=8/drop-last tiny-data failure by using TP=8 on one 8-GPU node, implying DP=1 for the single-node retry.
- Addresses prior one-step scheduler assertion by setting `max_steps=2` and `warmup_steps=0`, satisfying the intended relation `0 < 2`.
- `save_steps=1` and `logging_steps=1` are compatible with a two-step smoke and can produce early artifacts.
- Static template `output_dir` is not a launch collision blocker because `scripts/train_qwen3_8b_sft.sh` rewrites `output_dir:` in the runtime config to `${OUTPUT_ROOT}/training_summary/sft_output/${RUN_ID}`.
- The template default `model_name_or_path: Qwen/Qwen3-8B` is not a blocker because the same wrapper rewrites `model_name_or_path:` from `BASE_MODEL`.

Config verdict: pass for pre-run sanity, assuming dev_4 uses the PR #26 command shape with unique `RUN_ID`, `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`, and the approved dataset path.

## Test Gate Sanity

Evidence reviewed:

```text
evidence/test_1_sft_retry_gate.md
```

Verdict: pass.

Reasons:

- It explicitly names prior failures to avoid: MCA trainer `steps_in_epoch` division-by-zero and Megatron scheduler assertion `lr_warmup_steps < lr_decay_steps`.
- It requires task IDs, paths, exact command, base model validation, dataset checksum/schema checks, GPU endpoint/nodes proof, tiny-data-safe config reasoning, scheduler safety, output path, logs, and PASS/FAIL artifacts.
- It rejects placeholders, stale/broken base model paths, CPU/login-host runs, old baseline config, `max_steps=1`, repeated prior signatures, and no-checkpoint/no-metrics outcomes.
- It keeps mini-swe blocked until a retry produces a checkpoint/model or served endpoint and passes validation.

## Resource Plan Sanity

Evidence reviewed:

```text
evidence/dev_2_gpu_retry_resource_plan.md
```

Verdict: pass for planning, not yet executable.

Reasons:

- It records no stale previous H200 allocation remains active; previous frame is `STOPPED / Completed`.
- It forbids reuse of unrelated H200 jobs.
- It defines submit/status/ssh/stop templates, single-node 8xH200 requirements, expected duration, stop conditions, output preservation, and owner split.
- It correctly says no LTP job was submitted yet.

Non-blocking outdated note:

- The resource plan says `ready_to_submit: no` because PM had not yet gated config/test evidence at the time it was written. Later milestone status records PR #26/#27 merged and the test gate present. This is an expected timestamp drift, not a technical contradiction. Actual submit still requires PM authorization and the current owner execution task `M1-GPU-RETRY-SUBMIT-DEV2`.

## Data Gate Sanity

Evidence reviewed:

```text
evidence/dev_3_sft_data_mitigation.md
```

Existing data evidence:

- Original dataset: `/root/workspace/cleaned_m1_sft_10/train.jsonl`
- Original sha256: `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`
- Original count: 10.
- Mitigation artifact: `/root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/train.jsonl`
- Mitigation sha256: `f79d1e5843541faeb9789e4c4b24b10f1e10f60002af24173a9d039bcb370d87`
- Mitigation count: 160 repeated smoke rows.

Milestone status and assignments state the first retry data decision:

```text
Use original /root/workspace/cleaned_m1_sft_10/train.jsonl for the first attempt.
Use repeated x16 data only if dev_3/test_1 records a concrete blocker or PM explicitly changes the gate.
```

Launch-blocking inconsistency:

- `task_registry.md` has `M1-SFT-RETRY-DATA-GATE-DEV3` open.
- Required evidence path `evidence/dev_3_sft_retry_data_gate.md` is absent at review time.
- `assignments.md` says dev_3 owns `M1-SFT-RETRY-DATA-GATE-DEV3` and must write checksum/schema/limits to `evidence/dev_3_sft_retry_data_gate.md`.

Data verdict: **blocker until resolved**. The technical dataset decision appears coherent, but the explicit task/evidence gate is missing. Before launch, either:

1. dev_3 writes `evidence/dev_3_sft_retry_data_gate.md` confirming the original 10-example dataset for first retry with checksum/schema/limits; or
2. PM records an explicit waiver that `dev_3_sft_data_mitigation.md` plus PM status/assignments is sufficient for the first retry data gate.

## Overall Pregate Verdict

Current verdict: **BLOCKED on data-gate process evidence, not on config/resource/test technical consistency.**

No launch-blocking inconsistency found in:

- PR #26/#27 task mapping.
- Tiny-data-safe config values.
- Wrapper behavior for `BASE_MODEL` and runtime `output_dir`.
- Test_1 retry gate.
- Dev_2 no-submit resource plan.

Launch-blocking issue:

- Missing `evidence/dev_3_sft_retry_data_gate.md` while `M1-SFT-RETRY-DATA-GATE-DEV3` is open and explicitly required by the owner split.

## Recommendation For PM Gate

Concise recommendation:

```text
Do not authorize dev_2 resource submit / dev_4 retry launch until the dev_3 retry data gate is closed or explicitly waived. After that, the package is pregate-consistent for a first retry using PR #26 config, original 10-example dataset, clean-base path, and a fresh dev_2-owned H200 endpoint.
```

Expected launch package after data-gate resolution:

```text
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground
RUN_ID=<unique milestone1 retry id>
DRY_RUN=0
```

Completion marker: complete-with-blocker. This review identifies one launch blocker and does not run remote experiments.
