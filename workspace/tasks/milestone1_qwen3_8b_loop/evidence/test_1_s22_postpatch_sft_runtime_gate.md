# Test 1 S22 Post-Patch SFT Runtime Gate

Task under gate: `M1-S22-POSTPATCH-SFT-RUNTIME-DEV2`
Owner under gate: `intern_code_dev_2`
Test owner: `intern_code_test_1`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_postpatch_sft_runtime_gate.md`
Status timestamp: `2026-05-21T09:36:00Z`

## Result

`BLOCKED_FINAL_RUNTIME`

No SFT, GPU command, LTP action, or eval was run by `intern_code_test_1`.

## Inputs Checked

- PM authorization exists: `evidence/pm_s22_postpatch_runtime_authorization.md`.
- Task registry authorizes exactly one owner run for `intern_code_dev_2` after PR #39 merge commit `4a6c2968e1290d30415460b464eee638110958bc`.
- Required dev_2 runtime evidence is present:
  - `evidence/dev_2_s22_postpatch_sft_runtime.md`
  - `evidence/gpu_s22_postpatch_runtime_tracking.md`

## Post-Run Findings

### Authorization And Attempt Accounting

PASS.

- Runtime task id: `M1-S22-POSTPATCH-SFT-RUNTIME-DEV2`.
- Authorized owner: `intern_code_dev_2`.
- PR #39 merge commit: `4a6c2968e1290d30415460b464eee638110958bc`.
- Evidence records exactly one authorized SFT smoke attempt started and completed.
- Evidence records no additional retry and no eval run.

### Storage Rule

PASS.

- Required output root: `/home/xu.yang/coding_agent_playground/outputs`.
- Worker proof records `/home/xu.yang` resolving to `/mnt/cephfs/home/xu.yang`, with `findmnt` showing `fuse.ceph-fuse`.
- Capacity probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/...` wrote 4 x 6.0G files, verified `25769803776` bytes, then cleaned up.
- Runtime paths for run dir, stdout/stderr log, xtrace, diagnostics, manifest, runtime config, exit status, and checkpoint root are under `/home/xu.yang/coding_agent_playground/outputs`.
- Existing non-`/home/xu.yang` paths are recorded as required read-only inputs: base model under `/mnt/3fs`, dependency archives/wheels under `/mnt/3fs`, and source dataset under `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- After stop, artifacts are preserved and visible via `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs`.

### Data/Config/Runtime Contract

PASS until runtime execution.

- Dataset name: `coding_agent_m1_sft_10_sharegpt`.
- Accepted source artifact sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Dataset rows: 10.
- `dataset_info` entry maps ShareGPT `messages` with `from`/`value` tags.
- Generated config records `dataset: coding_agent_m1_sft_10_sharegpt`, `max_steps: 2`, `save_steps: 2`, `save_total_limit: 1`, `tensor_model_parallel_size: 8`, and output dir under `/home/xu.yang/coding_agent_playground/outputs`.
- Run manifest records PR #39 merge commit, dataset name, source sha256, save settings, and preflight log/xtrace/diagnostic paths.

### PR #39 Diagnostics Completeness

PASS.

dev_2 evidence records these durable PR #39 wrapper artifacts:

```text
preflight.json
config/qwen3_8b_sft.yaml
early_exit_diagnostics.txt
logs/train_stdout_stderr.log
exit_status.txt
run_manifest.json
logs/train_xtrace.log
```

Artifact hashes are recorded for preflight, manifest, runtime config, stdout/stderr log, xtrace, diagnostics, and exit status. This satisfies the post-PR39 observability gate: stdout/stderr, xtrace, ERR diagnostics, preflight, runtime config, manifest, and exit status were produced before/around the failure.

### Runtime Result

FAIL: fresh exact runtime blocker.

- `EXIT_STATUS=1`.
- Failure occurred before training/checkpoint save during LLamaFactory dataset conversion.
- Log signature recorded by dev_2: `Converting format of dataset (num_proc=4): 0/10`.
- Rank 0 traceback path: `datasets.arrow_dataset.map -> multiprocess.managers.Manager.start -> reader.recv -> EOFError`.
- Torch elastic root cause: `ChildFailedError` from local rank 0 / llamafactory launcher, exit code 1.
- PR39 diagnostics recorded `DIAGNOSTIC_REASON=ERR_TRAP`, `ERROR_EXIT=1`, `ERROR_LINE=209`.
- Exact blocker: `BLOCKED_POSTPATCH_RUNTIME_DATASET_MAP_EOF`.

### Checkpoint/Model Acceptance

FAIL.

- Checkpoint root: `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z`.
- Checkpoint files: absent.
- Complete checkpoint/model: absent.
- `trainer_state.json`: absent.
- `all_results.json`: absent.
- No replacement acceptance artifact is present.

### Old Failure Absence

PASS for old-signature absence.

- `KeyError: 'from'`: not observed.
- Missing `dataset_info` / wrong dataset name: not observed.
- Old scheduler signature failure: not observed in dev_2 evidence.
- DP/TP zero-step or old DP=8/TP=8 mismatch failure: not observed.
- ENOSPC / safetensors no-space checkpoint failure: not observed.
- Checkpoint save failure: not reached.

### Stop Proof And Endpoint

PASS.

- Stop command was issued for frame `xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z`.
- Post-stop status: `STOPPED (Completed)`.
- Completion timestamp: `2026-05-21 09:33:57`.
- Endpoint `ssh -p 38445 root@10.100.24.11` refused connection after STOPPED.
- GPU tracking records all 8 H200 idle after the failed attempt and before stop.

## Eval Handoff

`EVAL_HANDOFF_BLOCKED`

Eval handoff is blocked because there is no complete checkpoint/model, no `trainer_state.json`, and no `all_results.json`. The post-run blocker is not an eval-side issue; it is the SFT runtime blocker `BLOCKED_POSTPATCH_RUNTIME_DATASET_MAP_EOF`.

## Next Gate Recommendation

Before PM authorizes any further SFT attempt, require a no-execution config/runtime fix gate for the dataset conversion multiprocessing failure:

- Preserve PR39 diagnostics: stdout/stderr log, xtrace, ERR/EXIT diagnostics, preflight JSON, runtime config copy, run manifest, and exit status.
- Preserve `/home/xu.yang/coding_agent_playground/outputs` for all outputs, logs, checkpoints, run metadata, capacity probes, temporary converted datasets, and intermediates.
- Preserve dataset name `coding_agent_m1_sft_10_sharegpt`, ShareGPT `messages/from/value` mapping, source artifact sha256, and row count 10.
- Change preprocessing for the 10-row smoke to avoid `datasets.map(num_proc=4)` multiprocessing manager failure, for example by setting LLamaFactory preprocessing workers to single-process (`preprocessing_num_workers: 1` or an accepted equivalent).
- Have dev_1/test_1 re-gate the no-execution fix before PM authorizes another runtime attempt.
- Post-run PASS for any later attempt still requires complete checkpoint/model, `trainer_state.json`, `all_results.json` or PM-accepted replacement, stop proof, and absence of old and new failure signatures.

## Gate To Apply After dev_2 Evidence Lands

The post-run gate must verify all of the following from durable evidence only:

1. One-run authorization and provenance
   - Task id is `M1-S22-POSTPATCH-SFT-RUNTIME-DEV2`.
   - Runtime evidence names the PM authorization file and PR #39 merge commit.
   - Exactly one post-PR39 SFT smoke attempt is documented.
   - LTP job/frame id, node id, endpoint, `nodes.json`, submit/status/ssh/stop commands, and post-stop status are recorded.

2. `/home/xu.yang` storage rule
   - SFT output root is `/home/xu.yang/coding_agent_playground/outputs`.
   - Logs, xtrace, diagnostics, preflight JSON, runtime config, run manifest, checkpoints, run metadata, temporary converted datasets, capacity probes, and intermediates are under `/home/xu.yang`.
   - Any non-`/home/xu.yang` path is either an existing required input path with explicit justification, or the gate fails.

3. Data/config/runtime contract
   - Dataset name is `coding_agent_m1_sft_10_sharegpt`.
   - Accepted source artifact is `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl` with sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
   - Runtime config preserves the ShareGPT `messages/from/value` mapping.
   - Base model path, exact command, env, config path, dataset_info entry, run id, output root, run dir, checkpoint dir, log file, xtrace file, diagnostic file, and manifest path are recorded.

4. PR #39 diagnostics completeness
   - Durable stdout/stderr log exists and includes early startup lines.
   - Xtrace file exists or evidence states the configured xtrace mode and exact reason if disabled.
   - ERR/EXIT diagnostics file exists and records exit status and key environment/path state.
   - Preflight JSON, runtime config copy, and run manifest exist and agree on dataset name, output root, tmpdir, log, xtrace, diagnostic, checkpoint, and config paths.

5. Checkpoint/model acceptance
   - PASS requires a complete checkpoint/model artifact suitable for eval handoff, with path, file listing, sizes, and checksum or equivalent durable integrity proof.
   - `trainer_state.json` and `all_results.json` must be present, or dev_2 must provide an explicit accepted replacement approved by PM/test gate.
   - Any partial checkpoint, missing model file, missing trainer state/results, failed save, ENOSPC, early exit, or endpoint refusal is a runtime blocker.

6. Old failure absence
   - No `KeyError: 'from'`.
   - No missing `dataset_info` / wrong dataset name.
   - No old scheduler signature failure.
   - No DP/TP zero-step or old DP=8/TP=8 mismatch failure.
   - No checkpoint ENOSPC or write failure.

7. Eval handoff decision
   - `EVAL_HANDOFF_ALLOWED` only if checkpoint/model acceptance passes, trainer_state/all_results are present or PM-accepted replacement exists, stop proof is recorded, and test_1 post-run gate result is PASS.
   - Otherwise record `EVAL_HANDOFF_BLOCKED` with the exact blocker.

## Current Blocker

`BLOCKED_POSTPATCH_RUNTIME_DATASET_MAP_EOF`: the authorized post-PR39 SFT smoke produced the required PR39 diagnostics and preserved `/home/xu.yang` artifacts, but failed with `EXIT_STATUS=1` during `datasets.map(num_proc=4)` / `SyncManager` startup before training and checkpoint creation. No checkpoint/model, `trainer_state.json`, or `all_results.json` exists, so eval handoff is blocked.

## Completion Marker

```yaml
task_under_gate: M1-S22-POSTPATCH-SFT-RUNTIME-DEV2
test_owner: intern_code_test_1
result: BLOCKED_FINAL_RUNTIME
runtime_blocker: BLOCKED_POSTPATCH_RUNTIME_DATASET_MAP_EOF
exit_status: 1
pr39_diagnostics_complete: true
home_xu_yang_outputs_preserved: true
checkpoint_model_present: false
trainer_state_present: false
all_results_present: false
old_keyerror_from_absent: true
enospc_absent: true
ltp_stopped_completed: true
endpoint_refused_after_stop: true
eval_handoff_allowed: false
next_gate_recommendation: no_execution_config_fix_for_single_process_dataset_conversion_then_dev1_test1_regate
home_xu_yang_required: true
sft_gpu_eval_executed_by_test1: false
```
