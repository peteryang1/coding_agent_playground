# Dev 1 Session 21 ENOSPC Review

Owner: `intern_code_dev_1`  
Task ID: `M1-S21-ENOSPC-REVIEW-DEV1`  
Date: 2026-05-21  
Scope: refreshed independent no-execution review of ENOSPC config/resource/data/test-gate packages before any next retry, including the supervisor storage rule requiring SFT/eval intermediates under CephFS `/home/xu.yang` unless a required-path exception is recorded. No remote experiments, SFT, GPU, or eval were run.

## Sources Reviewed

Commands/files checked from the PM worktree:

```text
sed -n '1,420p' evidence/dev_4_s21_enospc_config_fix.md
sed -n '1,440p' evidence/dev_2_s21_enospc_resource_plan.md
sed -n '1,260p' evidence/dev_3_s21_enospc_data_confirm.md
sed -n '1,420p' evidence/test_1_s21_enospc_retry_gate.md
```

## Current Result

```text
review_status: PASS_FOR_PM_RETRY
pass_for_pm_retry: true
```

All required ENOSPC input packages are now present and have been refreshed for the `/home/xu.yang` CephFS storage rule. I found no remaining pre-run blocker in the durable evidence.

PM still must explicitly authorize any LTP/GPU/SFT retry. This review does not authorize execution by itself.

## Runtime Failure Facts

Prior failed runtime:

```text
run_id: milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z
exit_status: EXIT_STATUS=1
failure: safetensors_rust.SafetensorError: Error while serializing: I/O error: No space left on device (os error 28)
```

Accepted prior PASS facts:

- ShareGPT dataset and dataset_info were accepted.
- Runtime used dataset entry `coding_agent_m1_sft_10_sharegpt`.
- Runtime reached ShareGPT conversion `10/10`.
- Runtime reached total optimization steps `2` and step progress `1/2`.
- Prior failure signatures were absent: `KeyError: 'from'`, missing `dataset_info`, `ZeroDivisionError`, and scheduler warmup assertion.

Final blocker from that run:

- Checkpoint save failed during safetensors serialization.
- Only partial `checkpoint-1` exists.
- No complete checkpoint/model exists.
- `trainer_state.json` and `all_results.json` are absent.
- Partial checkpoint must not be used for eval.

## Package Review

### dev_4 Config / Save Fix

Reviewed path:

```text
evidence/dev_4_s21_enospc_config_fix.md
```

Status: **PASS**

Findings:

- Cites the failed run and ENOSPC signature.
- Preserves dataset entry `coding_agent_m1_sft_10_sharegpt`.
- Preserves accepted data path and checksum.
- Proposes avoiding the step-1 full checkpoint by using `save_steps: 2`, `save_total_limit: 1`, `max_steps: 2`.
- Requires a fresh `RUN_ID` and empty checkpoint directory.
- Defines rollback/stop conditions.
- Defines script/manifest hardening recommendations.

Storage-rule review:

- Supersedes the earlier `/mnt/3fs` output-root recommendation.
- Sets future `OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs`.
- Sets future `CHECKPOINT_DIR=${OUTPUT_ROOT}/training_summary/sft_output/${RUN_ID}`.
- Sets future `TMPDIR=${OUTPUT_ROOT}/tmp/${RUN_ID}`.
- Expects generated config proof under `/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml`.
- Uses `/mnt/3fs` only for recorded existing required paths: base model and historical failed-run evidence.

### dev_2 Resource / Capacity Plan

Reviewed path:

```text
evidence/dev_2_s21_enospc_resource_plan.md
```

Status: **PASS**

Findings:

- Diagnoses ENOSPC as not proven to be global `/mnt/3fs` free-space exhaustion.
- Defines no-submit LTP/resource plan and stop templates.
- Requires PM authorization before any LTP submit or retry.
- Defines capacity probes before launch.
- Requires fresh run id and fresh checkpoint path.

Storage-rule review:

- Default future storage root is `/home/xu.yang/coding_agent_playground`.
- Defines:
  - `output_root: /home/xu.yang/coding_agent_playground/outputs`
  - `run_metadata_root: /home/xu.yang/coding_agent_playground/outputs/runs/train`
  - `checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output`
  - `logs_root: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs`
  - `capacity_probe_root: /home/xu.yang/coding_agent_playground/outputs/capacity_probes`
  - `stop_proof_root: /home/xu.yang/coding_agent_playground/outputs/resource_tracking`
  - `nodes_json: /home/xu.yang/coding_agent_playground/outputs/milestone1_s21_nodes.json`
- Allows `/mnt/3fs` only for existing failed-run evidence, small compatibility metadata mirrors, and existing read-only inputs, with written justification.
- Capacity probes target `/home/xu.yang/coding_agent_playground/outputs/capacity_probes`.

### dev_3 Data Confirmation

Reviewed path:

```text
evidence/dev_3_s21_enospc_data_confirm.md
```

Status: **PASS**

Findings:

- Confirms no data-side change is needed for ENOSPC.
- Keeps dataset path `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Keeps sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Keeps row count `10`.
- Keeps dataset entry `coding_agent_m1_sft_10_sharegpt`.
- Confirms future temporary converted datasets, staging copies, SFT intermediates, and eval intermediates default to `/home/xu.yang`.
- Records an acceptable exception for the existing `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl` source artifact because it predates the storage rule and is treated as a stable source artifact.

### test_1 ENOSPC Retry Gate

Reviewed path:

```text
evidence/test_1_s21_enospc_retry_gate.md
```

Status: **PASS AFTER THIS DEV_1 REFRESH**

Findings:

- Gate is defined.
- Requires prior data-format PASS.
- Requires corrected dataset entry `coding_agent_m1_sft_10_sharegpt`.
- Requires dev_4 config/save fix, dev_2 resource/capacity plan, dev_3 data confirmation, and dev_1 review.
- Requires `/home/xu.yang` storage for launch outputs, stdout/stderr logs, checkpoints/model artifacts, run metadata, temporary converted datasets, staging copies, capacity probes, and related intermediates.
- Allows non-`/home/xu.yang` paths only with explicit existing-required-path justification.
- Current application said `BLOCKED_WAITING_DEV1_REFRESH`; this file now supplies that dev_1 refresh with `PASS_FOR_PM_RETRY`.

## Storage Rule Coverage

| Category | Current coverage | Status |
|---|---|---|
| Launch outputs | dev_4/dev_2 set `/home/xu.yang/coding_agent_playground/outputs` | PASS |
| Logs | dev_2 sets logs under `/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs`; test_1 requires `/home/xu.yang` | PASS |
| Checkpoints/model artifacts | dev_4/dev_2 set checkpoint root under `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output` | PASS |
| Run metadata / generated configs | dev_4/dev_2 set run metadata under `/home/xu.yang/coding_agent_playground/outputs/runs/train` | PASS |
| Capacity probes | dev_4/dev_2 set probes under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes` | PASS |
| Temp/staging data | dev_3/test_1 require future temp/staging/intermediate data under `/home/xu.yang`; existing source artifact exception is documented | PASS |
| Eval intermediates | dev_3/test_1 require eval intermediates under `/home/xu.yang` when eval becomes unblocked | PASS |
| Non-`/home/xu.yang` paths | base model, historical failed-run artifacts, existing source dataset, and small compatibility mirrors have written justifications | PASS |

## PASS_FOR_PM_RETRY Conditions

This review considers the pre-run package ready for PM retry decision because:

- ENOSPC cause is well characterized as checkpoint-save safetensors ENOSPC after data/config issues were cleared.
- dev_4 provides a concrete save-strategy/output-path fix.
- dev_2 provides a concrete no-submit capacity/resource plan.
- dev_3 confirms data contract should not change.
- test_1 defines the retry gate and storage rule.
- `/home/xu.yang` CephFS storage rule is now represented across the relevant packages.
- No evidence shows SFT/GPU/eval was run by these no-execution package tasks.

## Remaining Execution Requirements After PM Authorization

If PM authorizes retry, runtime owner must still record:

- fresh LTP frame/job id;
- node hostname and SSH endpoint;
- `/home/xu.yang` mount/path proof;
- capacity probe command/result under `/home/xu.yang`;
- exact generated config showing `dataset: coding_agent_m1_sft_10_sharegpt`, `save_steps: 2`, `save_total_limit: 1`, `max_steps: 2`, `warmup_steps: 0`, TP=8;
- exact output/checkpoint/log/run metadata paths under `/home/xu.yang`;
- exit status, logs, checkpoint/model presence, `trainer_state.json`, `all_results.json`;
- stop proof and artifact preservation note.

## Recommendation

```text
PASS_FOR_PM_RETRY. PM can decide whether to authorize one ENOSPC-fixed Session 21 retry. The retry should use the accepted ShareGPT dataset entry coding_agent_m1_sft_10_sharegpt, the save_steps=2/save_total_limit=1 final-save strategy, and CephFS /home/xu.yang/coding_agent_playground/outputs for future SFT/eval intermediates. Existing /mnt/3fs paths should remain audit/input exceptions only unless PM records a new exception.
```

## Completion Marker

PASS_FOR_PM_RETRY: all required ENOSPC input packages are present and reviewed; prior `/home/xu.yang` storage blockers are resolved in the current durable evidence. No remote experiments, SFT, GPU, or eval were run.
