# Test 1 S22 NCCL/NVLink Retry Gate

Task ID: `M1-S22-NCCL-GATE-TEST1`
Owner: `intern_code_test_1`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_nccl_retry_gate.md`
Status timestamp: `2026-05-21T10:29:17Z`

## Result

`GATE_DEFINED_WAITING_NCCL_MITIGATION_PACKAGES`

No SFT, GPU command, LTP action, eval, or dry-run launch was run by `intern_code_test_1`.

## Basis

This gate is based on the final post-run gate for `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`:

- Prior runtime final result: `BLOCKED_FINAL_RUNTIME`.
- Fresh blocker: `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.
- Failure signature: CUDA/NCCL `Invalid access of peer GPU memory over nvlink or a hardware error`, torch elastic local rank 5 `SIGABRT`, before checkpoint save.
- The prior run passed these gates: PM authorization, `/home/xu.yang` CephFS storage, 24GiB capacity probe, PR39 diagnostics, PR41 single-process preprocessing, ShareGPT conversion 10/10, training startup reached, old-failure absence, and stop proof.
- The prior run failed checkpoint/model acceptance: no checkpoint/model, no `trainer_state.json`, no `all_results.json`, and no accepted replacement artifact.
- Eval handoff remains blocked.

## Required Pre-Run Evidence Before PM Retry Authorization

A future retry is blocked until all of the following are present in durable evidence and reviewed by PM-required owners:

1. NCCL/NVLink mitigation package
   - Required evidence: `evidence/dev_4_s22_nccl_mitigation.md` or PM-named replacement.
   - Must cite `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.
   - Must propose exact mitigation for the peer GPU memory / NVLink / NCCL blocker.
   - Must state whether the next attempt requires a different H200 node, adjusted NCCL/NVL/launcher settings, a minimal hardware/NCCL preflight, or a combination.
   - Must list exact future command/config/env changes.
   - Must preserve PR39 diagnostics and PR41 single-process preprocessing.
   - Must not run LTP/SFT/GPU/eval/dry-run.

2. Resource plan
   - Required evidence: `evidence/dev_2_s22_nccl_resource_plan.md` or PM-named replacement.
   - Must confirm no active Milestone GPU is held.
   - Must confirm prior frame `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z` is stopped/released.
   - Must recommend different-node or NCCL/hardware-preflight resource shape.
   - Must include submit/status/stop templates only; no submit without fresh PM authorization.
   - Must keep capacity probes, logs, checkpoints, run metadata, temporary converted datasets, and intermediates under `/home/xu.yang/coding_agent_playground/outputs`.

3. Data confirmation
   - Required evidence: `evidence/dev_3_s22_nccl_data_confirm.md` or PM-named replacement.
   - Must cite that ShareGPT conversion reached 10/10 in the post-PR41 run.
   - Must confirm the data artifact remains `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
   - Must preserve sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`, row count 10, and `messages[*].from/value` schema.
   - Must state whether data is implicated in the NCCL/NVLink blocker. Current test_1 expectation: data is not implicated unless new evidence shows otherwise.
   - Future staging/intermediates must remain under `/home/xu.yang` unless explicitly justified as existing required input paths.

4. Independent review
   - Required evidence: `evidence/dev_1_s22_nccl_review.md` or PM-named replacement.
   - Must review dev_4 mitigation, dev_2 resource plan, dev_3 data confirmation, and this test_1 gate.
   - Must output `PASS_FOR_PM_RETRY` or exact blockers.
   - Must not run remote experiments/SFT/GPU/eval.

5. Fresh PM authorization
   - Required evidence: a new PM authorization file naming the retry task, owner, allowed attempt count, allowed resource shape, and whether any hardware/NCCL preflight is authorized.
   - No LTP/SFT/GPU/eval retry is allowed without this fresh PM authorization.

## Required Runtime Contract For Any Later Authorized Retry

Any future authorized retry must preserve these already-passing constraints:

### PR39 Diagnostics

Required durable artifacts:

- `train_stdout_stderr.log`
- `train_xtrace.log`
- `early_exit_diagnostics.txt`
- `exit_status.txt`
- `preflight.json`
- generated runtime config copy
- `run_manifest.json`

Artifacts must be listed with path, size, and checksum or equivalent integrity proof. The wrapper must continue to record ERR/EXIT diagnostics and exit status.

### PR41 Preprocessing

Required proof:

- Runtime source includes PR #41 or an approved successor containing the same preprocessing behavior.
- Generated config records `dataset: coding_agent_m1_sft_10_sharegpt`.
- Generated config records `preprocessing_num_workers: null` or PM/test-accepted single-process equivalent.
- Generated config records `dataloader_num_workers: 0`.
- Run manifest records `preflight.preprocessing_num_workers` as the generated config value.
- Log does not show `Converting format of dataset (num_proc=4): 0/10`.
- ShareGPT conversion reaches 10/10 or any new data-side failure is separately identified.

### `/home/xu.yang` Storage

All generated outputs and intermediates must be under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Required covered paths:

- launch logs
- xtrace
- diagnostics
- exit status
- preflight
- generated runtime config
- run manifest
- temporary converted datasets
- caches/intermediates controlled by the run
- checkpoints/model artifacts
- run metadata
- capacity probes

Any non-`/home/xu.yang` path must be an existing required input path with explicit durable justification. Otherwise the retry gate fails.

### Data Contract

Required proof:

- Dataset name: `coding_agent_m1_sft_10_sharegpt`.
- Source artifact: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Source sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Row count: 10.
- ShareGPT mapping: `messages[*].from/value`.

## Post-Run PASS Criteria

A future runtime can pass test_1 post-run gate only if all criteria below are met:

1. NCCL/NVLink blocker resolved or absent
   - No `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.
   - No `Invalid access of peer GPU memory over nvlink or a hardware error`.
   - No NCCL watchdog abort causing local rank SIGABRT.
   - No torch elastic local-rank hardware/NVLink abort before checkpoint save.
   - Any hardware/NCCL preflight required by PM/dev_4/dev_2/dev_1 passes and is recorded durably.

2. Checkpoint/model acceptance
   - Complete checkpoint/model exists under `/home/xu.yang/coding_agent_playground/outputs`.
   - File listing, sizes, and checksum or equivalent integrity proof are recorded.
   - Required downstream model/tokenizer/config artifacts are present.
   - `trainer_state.json` is present.
   - `all_results.json` is present.
   - Any missing `trainer_state.json` or `all_results.json` requires explicit PM/test accepted replacement before eval handoff.

3. PR39 diagnostics complete
   - stdout/stderr, xtrace, diagnostics, exit status, preflight, config, and manifest are present.
   - Manifest/config/preflight agree on dataset, output root, preprocessing workers, checkpoint dir, log path, xtrace path, and diagnostics path.

4. PR41 preprocessing preserved
   - `preprocessing_num_workers: null` or accepted single-process equivalent is recorded in generated config and manifest.
   - `num_proc=4` SyncManager EOF does not recur.

5. Storage and stop proof
   - `/home/xu.yang` output/intermediate rule passes.
   - LTP stop/release proof is recorded.
   - Endpoint is refused or otherwise unreachable after stop.
   - Artifact preservation on CephFS is recorded.

6. Old failure absence
   - No `KeyError: 'from'`.
   - No missing/wrong `dataset_info`.
   - No wrong dataset name.
   - No `datasets.map(num_proc=4)` / SyncManager EOFError.
   - No ENOSPC / safetensors no-space.
   - No early wrapper exit before diagnostics.
   - No checkpoint-save failure.

## Eval Handoff Criteria

`EVAL_HANDOFF_PASS` is allowed only if:

- post-run gate passes;
- checkpoint/model acceptance passes;
- `trainer_state.json` and `all_results.json` are present, or explicit PM/test accepted replacements exist;
- stop proof passes;
- PM separately gates eval or a served endpoint/model handoff.

Otherwise record `EVAL_HANDOFF_BLOCKED` with exact blockers.

## Current Blockers

Current no-execution gate status is blocked pending required owner packages and PM authorization:

- `BLOCKED_WAITING_DEV4_NCCL_MITIGATION`
- `BLOCKED_WAITING_DEV2_RESOURCE_PLAN`
- `BLOCKED_WAITING_DEV3_DATA_CONFIRM`
- `BLOCKED_WAITING_DEV1_REVIEW`
- `BLOCKED_WAITING_FRESH_PM_AUTHORIZATION`

Eval handoff remains blocked because the latest runtime has no checkpoint/model, no `trainer_state.json`, and no `all_results.json`.

## Completion Marker

```yaml
task_id: M1-S22-NCCL-GATE-TEST1
owner: intern_code_test_1
result: GATE_DEFINED_WAITING_NCCL_MITIGATION_PACKAGES
runtime_blocker_to_resolve: BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY
fresh_pm_authorization_required: true
pr39_diagnostics_required: true
pr41_preprocessing_num_workers_required: null
home_xu_yang_outputs_required: true
checkpoint_model_required: true
trainer_state_required: true
all_results_required: true
stop_proof_required: true
old_failure_absence_required: true
eval_handoff_allowed_now: false
sft_gpu_eval_executed_by_test1: false
```
