# Test 1 S22 NCCL/NVLink Retry Gate

Task ID: `M1-S22-NCCL-GATE-TEST1`
Owner: `intern_code_test_1`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_nccl_retry_gate.md`
Status timestamp: `2026-05-21T10:41:00Z`

## Result

`PASS_FOR_PM_RETRY`

No SFT, GPU command, LTP action, eval, or dry-run launch was run by `intern_code_test_1`.

## Refresh Against Current Inputs

Inputs checked for this refresh:

- `evidence/dev_4_s22_nccl_mitigation.md`: present.
- `evidence/dev_2_s22_nccl_resource_plan.md`: present.
- `evidence/dev_3_s22_nccl_data_confirm.md`: present.
- `evidence/dev_1_s22_nccl_review.md`: present and refreshed to `PASS_FOR_PM_RETRY`.
- PR #43: `https://github.com/peteryang1/coding_agent_playground/pull/43`
  - state: `OPEN`
  - draft: `false`
  - mergeable: `MERGEABLE`
  - merge state: `CLEAN`
  - head: `5f4d14a12aa8044a429d1110757ed631a7bc9833`
  - task: `M1-S22-NCCL-MITIGATION-DEV4`

### dev_4 Mitigation Gate

PASS for test_1 no-execution review.

- Cites `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.
- Preserves the fact that PR39 diagnostics passed and PR41 `preprocessing_num_workers: null` passed.
- States the fresh blocker is hardware/distributed-backend sensitive, not data-format, storage, PR39 diagnostics, or PR41 preprocessing.
- Recommends a fresh H200 allocation, preferably a different physical node than `lg-cmc-b7r202-p07u16-h200-000708`.
- Requires hardware/NCCL preflight before SFT on any future PM-authorized node.
- Defines future preflight artifacts under `/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>`.
- Defines future SFT env additions for evidence and safer failure surfacing: `NCCL_DEBUG=INFO`, `NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL`, `NCCL_ASYNC_ERROR_HANDLING=1`, `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`, `CUDA_DEVICE_MAX_CONNECTIONS=1`.
- Does not make `NCCL_P2P_DISABLE=1` the default; treats it only as an explicitly accepted degraded diagnostic fallback.
- States no LTP/SFT/GPU/eval/dry-run was performed.

### PR #43 Gate

PASS for package scope/metadata.

- PR #43 body cites task id, owner, acceptance criteria, evidence path, and completion marker.
- GitHub reports open/non-draft `MERGEABLE`/`CLEAN`.
- Head commit is `5f4d14a12aa8044a429d1110757ed631a7bc9833`.
- PR #43 does not authorize SFT/GPU/eval/dry-run.
- PR #43 is a dev_4 mitigation package PR; it is not a runtime authorization.

### dev_2 Resource Plan Gate

PASS for no-submit resource planning.

- Confirms prior post-PR41 frame `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z` is `STOPPED (Completed)`.
- Confirms former endpoint `ssh -p 27021 root@10.100.22.14` refused connection after stop.
- Confirms no active coding_agent_playground / Milestone 1 / S22 NCCL retry GPU is held by `intern_code_dev_2`.
- Recommends a fresh single-node 8 x H200 allocation, preferably on a different physical node than `lg-cmc-b7r202-p07u16-h200-000708`.
- Includes no-submit LTP submit/status/ssh/stop templates only.
- Keeps future output, checkpoint, tmp, run metadata, nodes JSON, and capacity probe paths under `/home/xu.yang/coding_agent_playground/outputs`.
- States no submit/resource action without fresh PM authorization after required gates.

### dev_3 Data Confirmation Gate

PASS.

- Confirms no ShareGPT data/package change is implicated by the CUDA/NCCL/NVLink blocker.
- Preserves accepted source artifact `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Preserves sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Preserves row count 10 and ShareGPT `messages[*].from/value` contract.
- Cites ShareGPT conversion `10/10`, PR41 `preprocessing_num_workers: null`, and training startup reached.
- Requires future staging/copy/tmp data artifacts to use `/home/xu.yang` unless explicitly justified.
- States no SFT/GPU/LTP/dry-run/eval execution.

### dev_1 Review Gate

PASS.

Current `evidence/dev_1_s22_nccl_review.md` records `PASS_FOR_PM_RETRY`.

dev_1 reviewed dev_4 mitigation, dev_2 resource plan, dev_3 data confirmation, PR #43, and the prior runtime/test evidence. No remaining dev_1 blocker is reported. dev_1 also records that this review does not authorize LTP/SFT/GPU/eval; any future preflight or SFT runtime still requires explicit PM authorization.

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

Current no-execution gate status is `PASS_FOR_PM_RETRY`.

Cleared for test_1 no-execution gate:

- PR #43 package metadata/scope: PASS.
- dev_4 mitigation package: PASS.
- dev_2 resource plan: PASS.
- dev_3 data confirmation: PASS.
- dev_1 independent review: PASS.

Remaining before any actual execution:

- Fresh PM authorization is still required before any LTP/GPU/NCCL preflight/SFT runtime.
- Any future run must still satisfy post-run acceptance: NCCL/NVLink blocker absent/resolved, checkpoint/model present, `trainer_state.json` and `all_results.json` present or PM/test accepted replacements, PR39 diagnostics complete, PR41 preprocessing preserved, `/home/xu.yang` storage preserved, stop proof recorded, and old failure signatures absent.

Eval handoff remains blocked because the latest runtime has no checkpoint/model, no `trainer_state.json`, and no `all_results.json`.

## Completion Marker

```yaml
task_id: M1-S22-NCCL-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
runtime_blocker_to_resolve: BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY
fresh_pm_authorization_required: true
pr43_head: 5f4d14a12aa8044a429d1110757ed631a7bc9833
pr43_mergeable_clean: true
dev4_mitigation_gate: PASS
dev2_resource_plan_gate: PASS
dev3_data_confirm_gate: PASS
dev1_review_gate: PASS
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
