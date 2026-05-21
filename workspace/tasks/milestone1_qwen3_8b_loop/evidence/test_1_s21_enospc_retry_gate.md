# Test 1 Session 21 ENOSPC Retry Gate

Date: 2026-05-21

Task ID: `M1-S21-ENOSPC-GATE-TEST1`

Owner: `intern_code_test_1`

Scope: define the no-execution retry gate after the Session 21 safetensors ENOSPC checkpoint-save blocker. This gate defines what evidence must exist before PM can authorize any additional SFT runtime and what post-run evidence is required for PASS/FAIL.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s21_enospc_retry_gate.md`

## Current Result

Result: **PASS_FOR_PM_RETRY**

No SFT, GPU, or eval command was run by test_1.

Current final blocker from `M1-S21-LAUNCH-GATE-TEST1`:

```text
POST_RUN_RESULT: BLOCKED_FINAL_RUNTIME
runtime_exit_status: 1
runtime_blocker: SAFETENSORS_ENOSPC_DURING_CHECKPOINT_SAVE
```

The prior Session 21 runtime cleared the data-format blocker and prior tiny-data/scheduler failures, but failed while saving `checkpoint-1` with:

```text
safetensors_rust.SafetensorError: Error while serializing: I/O error: No space left on device (os error 28)
```

The partial `checkpoint-1` is not an accepted checkpoint/model and must not be used for mini-swe.

## Sources Reviewed

- `task_registry.md`
- `task_knowledge.md`
- `history_log.md`
- `evidence/test_1_s21_launch_gate.md`
- `evidence/dev_2_s21_sft_runtime.md`
- `evidence/gpu_s21_resource_tracking.md`
- `evidence/dev_3_s21_datasetinfo_package.md`
- `evidence/dev_3_sft_dataformat_artifact.md`
- `evidence/dev_4_s21_enospc_config_fix.md`
- `evidence/dev_2_s21_enospc_resource_plan.md`
- `evidence/dev_3_s21_enospc_data_confirm.md`
- `evidence/dev_1_s21_enospc_review.md`

## Prior Runtime Facts Required For Any Retry

Any ENOSPC-fixed retry package must cite these accepted prior facts:

```text
run_id=milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
exit_status=1
final_blocker=safetensors ENOSPC during checkpoint-1 serialization
checkpoint_status=partial checkpoint-1 only
trainer_state_json=absent
all_results_json=absent
ltp_frame=xu.yang~coding-agent-playground-m1-s21-qwen3-8b-runtime-20260521T072638Z
ltp_final_state=STOPPED (Completed)
endpoint_after_stop=ssh -p 16126 root@10.100.16.54 refused connection
```

Accepted prior PASS facts:

- Dataset info/data-format passed.
- Runtime used dataset entry `coding_agent_m1_sft_10_sharegpt`.
- Runtime config contained `dataset: coding_agent_m1_sft_10_sharegpt`.
- Dataset path was `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Dataset sha256 was `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- ShareGPT conversion completed `10/10`.
- Training reached total optimization steps `2` and step progress `1/2`.
- No `KeyError: 'from'`.
- No missing `dataset_info.json` signature.
- No `ZeroDivisionError` / `steps_in_epoch`.
- No Megatron scheduler warmup assertion.

## Required Pre-Run Inputs

PM should not authorize another runtime until all of these task-specific packages exist and pass owner gates.

### Config / Save Strategy Fix

Required owner evidence:

```text
evidence/dev_4_s21_enospc_config_fix.md
task_id=M1-S21-ENOSPC-CONFIG-FIX-DEV4
```

Required content:

- exact failed run id and ENOSPC signature;
- explicit fix type, for example:
  - output/checkpoint path changed to a capacity-verified path;
  - checkpoint save behavior changed for smoke, such as disabling full-model save if PM accepts that;
  - save strategy changed so the smoke still produces a PM-accepted model/checkpoint artifact;
- exact config/script file paths changed or exact no-code command/config override;
- exact expected artifact paths after retry;
- statement preserving:
  - dataset entry `coding_agent_m1_sft_10_sharegpt`;
  - dataset sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`;
  - base model `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`;
  - TP=8/DP=1, `max_steps=2`, `warmup_steps=0`;
- clear rollback/stop conditions.

Pre-run BLOCKER if:

- there is no concrete ENOSPC fix;
- the fix changes data format without dev_3 confirmation;
- the fix removes all acceptable checkpoint/model output without defining an accepted replacement;
- the fix relies on partial `checkpoint-1`.

### Resource / Capacity Plan

Required owner evidence:

```text
evidence/dev_2_s21_enospc_resource_plan.md
task_id=M1-S21-ENOSPC-RESOURCE-DEV2
```

Required content:

- capacity/root-cause assessment for the checkpoint output path used by the failed run;
- proposed output/checkpoint path and why it has sufficient capacity;
- pre-run capacity commands and expected thresholds;
- LTP submit/status/stop templates;
- no active stale Session 21 GPU proof;
- statement that no LTP submit occurs until PM authorization;
- stop proof requirements.

Pre-run BLOCKER if:

- output capacity is not checked;
- proposed output path is still likely to hit ENOSPC;
- no stop/cleanup proof contract exists;
- stale GPU or output state is ambiguous.

### Data Confirmation

Required owner evidence:

```text
evidence/dev_3_s21_enospc_data_confirm.md
task_id=M1-S21-ENOSPC-DATA-CONFIRM-DEV3
```

Required content:

- confirm the retry keeps dataset entry `coding_agent_m1_sft_10_sharegpt`;
- confirm dataset path `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`;
- confirm sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`;
- confirm row count `10`;
- confirm no data-side change is needed for ENOSPC;
- list any data-side blocker if found.

Pre-run BLOCKER if:

- dataset entry/path/checksum changes without a new data package;
- old OpenAI `role/content` dataset is reintroduced;
- data confirmation is absent.

### Independent Review

Required owner evidence:

```text
evidence/dev_1_s21_enospc_review.md
task_id=M1-S21-ENOSPC-REVIEW-DEV1
```

Required content:

- review dev_4 config/save fix;
- review dev_2 resource/capacity plan;
- review dev_3 data confirmation;
- review this test gate;
- state `PASS_FOR_PM_RETRY` or exact blockers.

Pre-run BLOCKER if review is absent or identifies unresolved blockers.

## Required Retry Command / Config

Any proposed retry command must preserve the accepted Session 21 data/config path unless a new PM-approved task changes it.

Required command properties:

```text
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
DRY_RUN=0
RUN_ID=<new unique ENOSPC-fixed run id>
OUTPUT_ROOT=<capacity-verified durable output root under /home/xu.yang unless an existing-required-path justification is recorded>
```

Required generated runtime config properties:

```yaml
dataset: coding_agent_m1_sft_10_sharegpt
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
```

The generated config must show the ENOSPC fix, such as changed output/checkpoint path or accepted save behavior change.

## Required `/home/xu.yang` Storage Rule

Supervisor storage rule applied on 2026-05-21:

```text
SFT launch outputs, stdout/stderr logs, checkpoints/model artifacts, run metadata, temporary converted datasets, staging copies, capacity probes, and related intermediates must use CephFS /home/xu.yang.
Any non-/home/xu.yang path must include an explicit existing-required-path justification before PM authorization.
If a proposed retry uses a non-/home/xu.yang path without that justification, this gate FAILs/blocks pre-run.
```

Allowed non-`/home/xu.yang` inputs only if justified by existing-required-path evidence:

- base model path `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`, if model loading requires the existing mounted model location;
- canonical source dataset path `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, if the owner explicitly states it is the accepted source artifact and records any temporary conversion/staging under `/home/xu.yang`.

Pre-run BLOCKER if any future package places these under `/mnt/3fs`, `/mnt/3fs2`, `/tmp`, `/root/workspace`, or another non-`/home/xu.yang` path without explicit existing-required-path justification:

- `OUTPUT_ROOT`;
- checkpoint/model output directory;
- run directory and run metadata;
- stdout/stderr and training logs;
- generated runtime config copies;
- temporary converted datasets, staging copies, and preprocessing intermediates;
- capacity probe files used to prove ENOSPC mitigation.

## Required Absence Of Old Failures

A retry FAILs if logs contain any old blocker signature:

```text
KeyError: 'from'
Cannot open data/sft/dataset_info.json
ValueError: Cannot open data/sft/dataset_info.json
ZeroDivisionError: division by zero
steps_in_epoch
optimizer_param_scheduler.py
assert self.lr_warmup_steps < self.lr_decay_steps
safetensors_rust.SafetensorError: Error while serializing: I/O error: No space left on device
No space left on device
```

The ENOSPC signature must be absent for the retry to pass.

## Checkpoint / Model Acceptance

Post-run PASS requires one of the accepted completion forms below.

### Preferred Acceptance

Required:

- exit status `0`;
- complete checkpoint/model path;
- complete model weights, not a partial write;
- tokenizer/config files needed by downstream loading;
- `trainer_state.json` present;
- `all_results.json` present;
- run manifest present;
- generated runtime config present;
- stdout/stderr log present;
- stop proof present.

### Accepted Replacement, If PM Pre-Approves

If dev_4 proposes a smoke-specific save strategy that intentionally does not emit both `trainer_state.json` and `all_results.json`, the pre-run package must define an accepted replacement before runtime. Replacement evidence must include:

- exact files that replace `trainer_state.json` / `all_results.json`;
- why they prove training reached the intended smoke endpoint;
- exact metrics or state fields retained;
- PM acceptance recorded before runtime.

Without pre-approved replacement evidence, missing `trainer_state.json` or missing `all_results.json` is a post-run BLOCKER.

## Stop Proof Requirements

Every retry must record:

- LTP frame/job id;
- endpoint/node id;
- stop command/action;
- stop timestamp UTC;
- post-stop LTP status;
- endpoint proof after stop;
- artifact preservation note;
- statement that the chosen `/home/xu.yang` output root was not deleted, plus preservation/justification for any existing required non-`/home/xu.yang` source path used by the run.

Missing stop proof is a post-run BLOCKER even if training produced a checkpoint.

## PASS Criteria

Pre-run `PASS_FOR_PM_RETRY` requires:

- prior data-format PASS cited;
- corrected dataset entry `coding_agent_m1_sft_10_sharegpt` retained;
- dev_4 ENOSPC config/save-strategy fix present and concrete;
- dev_2 resource/capacity plan present and concrete;
- dev_3 data confirmation present and PASS;
- dev_1 review present and `PASS_FOR_PM_RETRY`;
- proposed command/config preserve accepted data/base/tiny-data-safe settings;
- output/checkpoint path or save behavior is explicitly fixed for ENOSPC;
- SFT launch outputs, logs, checkpoints/model artifacts, run metadata, temporary converted datasets/staging copies, and capacity probes are under `/home/xu.yang`, or every non-`/home/xu.yang` path has explicit existing-required-path justification;
- no SFT/GPU/eval has been run before PM authorization.

Post-run PASS requires:

- old failure signatures absent;
- ENOSPC absent;
- complete accepted checkpoint/model or pre-approved replacement exists;
- `trainer_state.json` and `all_results.json` exist, unless replacement was pre-approved;
- exit status and logs are consistent;
- stop proof complete;
- checkpoint/model is explicitly accepted for mini-swe handoff.

## FAIL / BLOCKER Criteria

Pre-run BLOCKER if any required owner package is missing or unresolved.

Post-run BLOCKER if:

- ENOSPC repeats;
- only partial checkpoint exists;
- `trainer_state.json` is absent without pre-approved replacement;
- `all_results.json` is absent without pre-approved replacement;
- exit status is nonzero without a complete accepted checkpoint/model and exact new blocker;
- old data-format/tiny-data/scheduler failures reappear;
- stop proof is missing;
- endpoint/resource state is ambiguous.

## Current Application

Current application result: **PASS_FOR_PM_RETRY**

Current accepted facts:

- Session 21 data-format path passed.
- Dataset entry is `coding_agent_m1_sft_10_sharegpt`.
- Dataset sha256 is `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Prior runtime reached ShareGPT conversion `10/10` and step `1/2`.
- Prior runtime failed with safetensors ENOSPC during checkpoint save.
- Partial `checkpoint-1` is not accepted.
- No `trainer_state.json` or `all_results.json` exists from the failed run.
- Prior LTP frame was stopped and endpoint refused connection after stop.

Current input refresh findings:

- `evidence/dev_4_s21_enospc_config_fix.md` now exists and is concrete for save-strategy direction (`save_steps: 2`, `save_total_limit: 1`, fresh run id, preserve `coding_agent_m1_sft_10_sharegpt`). The current package supersedes the earlier `/mnt/3fs` output-root recommendation and points future outputs/logs/checkpoints/run metadata/tmp/intermediates/probes to `/home/xu.yang/coding_agent_playground/outputs`; non-`/home/xu.yang` paths are limited to recorded existing-required input/audit exceptions.
- `evidence/dev_2_s21_enospc_resource_plan.md` now exists and contains no-submit resource/capacity planning, LTP templates, probe commands, and `/home/xu.yang/coding_agent_playground` defaults for future SFT intermediates, output roots, checkpoint dirs, logs, run metadata, stop proof, and runtime evidence. `/mnt/3fs` is exception-only for historical failed-run evidence, small compatibility metadata mirrors, and existing required read-only inputs with written justification.
- `evidence/dev_3_s21_enospc_data_confirm.md` now exists and passes the data-contract portion: keep `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`, row count `10`, dataset entry `coding_agent_m1_sft_10_sharegpt`, and `messages[*].from/value`; no data-side ENOSPC blocker found. Future temporary converted datasets or staging copies still must be under `/home/xu.yang` unless explicitly justified.
- `evidence/dev_1_s21_enospc_review.md` now outputs `PASS_FOR_PM_RETRY` and records that all required ENOSPC input packages are present, reviewed, and refreshed for the `/home/xu.yang` CephFS storage rule. It finds no remaining pre-run blocker in durable evidence.

Final pre-run gate result:

- `PASS_FOR_PM_RETRY`: from the test_1 no-execution gate perspective, PM may decide whether to authorize one ENOSPC-fixed Session 21 retry.
- This PASS does not execute or itself authorize SFT/GPU/eval. PM authorization is still required before any LTP submit or retry execution.
- The retry must keep `/home/xu.yang` CephFS as the default for SFT launch outputs, logs, checkpoints/model artifacts, run metadata, temporary converted datasets/staging copies, capacity probes, and related intermediates.
- Non-`/home/xu.yang` paths remain allowed only for recorded existing-required input/audit/compatibility exceptions, such as the base model, historical failed-run evidence, existing source dataset, and small metadata mirrors.
- Runtime owner must still record fresh endpoint/node proof, `/home/xu.yang` mount/path proof, capacity probe result, exact generated config, complete checkpoint/model acceptance, `trainer_state.json`/`all_results.json` or pre-approved replacement, old-failure absence, exit status/logs, and stop proof.

Completion marker:

```text
task_id: M1-S21-ENOSPC-GATE-TEST1
gate_definition: COMPLETE
pre_run_status: PASS_FOR_PM_RETRY
post_run_status: PENDING_NO_RETRY_RUNTIME
sft_gpu_eval_executed_by_test1: false
mini_swe_can_proceed: false
```
