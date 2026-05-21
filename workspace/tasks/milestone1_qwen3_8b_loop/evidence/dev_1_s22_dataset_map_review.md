# M1-S22-DATASET-MAP-REVIEW-DEV1

Owner: `intern_code_dev_1`
Task: `M1-S22-DATASET-MAP-REVIEW-DEV1`
Evidence date: 2026-05-21
Execution boundary: no remote experiments, SFT, GPU, or eval run by dev_1.

## Result

`BLOCKED_MISSING_DEV4_DEV3_PACKAGES`

dev_1 can confirm the new runtime blocker facts from durable evidence, but cannot issue `PASS_FOR_PM_RETRY` until the assigned no-execution fix inputs exist:

- Missing: `evidence/dev_4_s22_dataset_map_singleproc_fix.md`
- Missing: `evidence/dev_3_s22_dataset_map_data_confirm.md`

## Inputs Reviewed

- `evidence/dev_2_s22_postpatch_sft_runtime.md`
- `evidence/gpu_s22_postpatch_runtime_tracking.md`
- `evidence/pm_s22_dataset_map_eof_gate.md`
- `evidence/test_1_s22_postpatch_sft_runtime_gate.md`
- `task_registry.md`

Checked for package inputs:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_dataset_map_singleproc_fix.md: MISSING
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_3_s22_dataset_map_data_confirm.md: MISSING
```

## Confirmed Runtime Facts

The current blocker is a fresh post-PR39 runtime blocker, not a recurrence of the older failures.

Confirmed from dev_2/test_1/PM evidence:

- PM authorized exactly one post-PR39 SFT smoke attempt for `intern_code_dev_2`.
- PR #39 merge commit used for runtime: `4a6c2968e1290d30415460b464eee638110958bc`.
- LTP frame: `xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z`.
- Endpoint during run: `ssh -p 38445 root@10.100.24.11`.
- LTP final state: `STOPPED (Completed)`.
- Endpoint refused connection after stop.
- Eval was not run.
- Runtime artifacts are preserved under `/home/xu.yang/coding_agent_playground/outputs` on CephFS.
- `/home/xu.yang` resolved to `/mnt/cephfs/home/xu.yang`.
- Capacity probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/...` wrote and cleaned `25769803776` bytes.
- PR39 diagnostics worked and produced:
  - `preflight.json`
  - `config/qwen3_8b_sft.yaml`
  - `run_manifest.json`
  - `logs/train_stdout_stderr.log`
  - `logs/train_xtrace.log`
  - `early_exit_diagnostics.txt`
  - `exit_status.txt`
- Run manifest records:
  - `dataset_name: coding_agent_m1_sft_10_sharegpt`
  - train sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`
  - PR39 merge commit
  - save policy and preflight log/xtrace/diagnostic paths.
- Generated config records:
  - `dataset: coding_agent_m1_sft_10_sharegpt`
  - `output_dir` under `/home/xu.yang/coding_agent_playground/outputs`
  - `max_steps: 2`
  - `save_steps: 2`
  - `save_total_limit: 1`
  - `tensor_model_parallel_size: 8`

## Current Failure Signature

The authorized post-PR39 run failed before training and before checkpoint save:

```text
EXIT_STATUS=1
Failure point: LLamaFactory dataset conversion
Log signature: Converting format of dataset (num_proc=4): 0/10
Traceback path: datasets.arrow_dataset.map -> multiprocess.managers.Manager.start -> reader.recv -> EOFError
Exact blocker: BLOCKED_POSTPATCH_RUNTIME_DATASET_MAP_EOF
```

Artifact result:

```text
checkpoint files: absent
complete checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
```

Old failure signatures are absent in durable evidence:

- `KeyError: 'from'`: not observed.
- Missing dataset_info / wrong dataset name: not observed.
- ENOSPC / safetensors no-space checkpoint failure: not observed.
- Checkpoint save failure: not reached.
- Training step progress: not reached.

## Expected Review Criteria When Packages Exist

dev_4 single-process preprocessing package must show, without running SFT/GPU/eval:

- The future config/launcher forces single-process dataset preprocessing for the 10-row smoke, for example `preprocessing_num_workers: 1` or an accepted equivalent that avoids `datasets.map(num_proc=4)`.
- PR #39 diagnostics remain preserved: stdout/stderr log, xtrace, ERR/EXIT diagnostics, preflight JSON, runtime config copy, run manifest, and exit status.
- `/home/xu.yang/coding_agent_playground/outputs` remains the default for outputs, logs, checkpoints, run metadata, temporary converted datasets, capacity probes, and intermediates.
- Dataset name remains `coding_agent_m1_sft_10_sharegpt`.
- Exact future command/config path and expected post-run PASS/FAIL artifacts are recorded.

dev_3 data confirmation must show, without running SFT/GPU/eval:

- Source artifact remains `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Source sha256 remains `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Row count remains `10`.
- ShareGPT schema remains `messages[*].from/value` with provenance fields preserved.
- The new `SyncManager EOFError` is not evidence of content/schema corruption, or it records an exact data-side blocker if dev_3 finds one.
- Any future staging/copy/temp dataset path uses `/home/xu.yang` or records an explicit required-path exception.

## Current Blockers

No `PASS_FOR_PM_RETRY` from dev_1 yet.

Exact blockers:

1. `MISSING_DEV4_SINGLEPROC_FIX_PACKAGE`: `evidence/dev_4_s22_dataset_map_singleproc_fix.md` is absent, so dev_1 cannot verify the proposed config/launcher change to single-process dataset preprocessing.
2. `MISSING_DEV3_DATA_CONFIRMATION`: `evidence/dev_3_s22_dataset_map_data_confirm.md` is absent, so dev_1 cannot verify whether the ShareGPT data artifact needs no content/schema change for this blocker.

## Completion Marker

```yaml
task_id: M1-S22-DATASET-MAP-REVIEW-DEV1
owner: intern_code_dev_1
result: BLOCKED_MISSING_DEV4_DEV3_PACKAGES
runtime_blocker_confirmed: BLOCKED_POSTPATCH_RUNTIME_DATASET_MAP_EOF
old_keyerror_from_absent: true
enospc_absent: true
checkpoint_model_present: false
trainer_state_present: false
all_results_present: false
ltp_stopped_completed: true
endpoint_refused_after_stop: true
missing_inputs:
  - evidence/dev_4_s22_dataset_map_singleproc_fix.md
  - evidence/dev_3_s22_dataset_map_data_confirm.md
no_remote_experiments_sft_gpu_eval_by_dev1: true
```
