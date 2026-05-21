# M1-S22-DATASET-MAP-REVIEW-DEV1

Owner: `intern_code_dev_1`
Task: `M1-S22-DATASET-MAP-REVIEW-DEV1`
Evidence date: 2026-05-21
Execution boundary: no remote experiments, SFT, GPU, or eval run by dev_1.

## Result

`PASS_FOR_PM_RETRY`

dev_1 refreshed the review after PR #41, dev_4 single-process package, and dev_3 data confirmation became available. No remaining dev_1 blocker found for PM retry authorization.

`PASS_FOR_PM_RETRY` means dev_1 finds the PR #41 single-process preprocessing package and dev_3 data confirmation coherent for PM to decide on the next runtime gate. It does not itself authorize SFT/GPU/eval. Any future runtime still needs explicit PM authorization, resource readiness, and test gate approval.

## Inputs Reviewed

- `evidence/dev_2_s22_postpatch_sft_runtime.md`
- `evidence/gpu_s22_postpatch_runtime_tracking.md`
- `evidence/pm_s22_dataset_map_eof_gate.md`
- `evidence/test_1_s22_postpatch_sft_runtime_gate.md`
- `evidence/dev_4_s22_dataset_map_singleproc_fix.md`
- `evidence/dev_3_s22_dataset_map_data_confirm.md`
- PR #41: `https://github.com/peteryang1/coding_agent_playground/pull/41`
- `task_registry.md`

PR #41 metadata checked with `gh pr view 41 --repo peteryang1/coding_agent_playground --json ...`:

```text
state: OPEN
draft: false
mergeable: MERGEABLE
merge_state: CLEAN
head: intern_code_dev_4/M1-S22-DATASET-MAP-SINGLEPROC-FIX-DEV4
head_commit: fc0b6062664e3eb5283e89c22a152427ca47fc3c
title: M1-S22-DATASET-MAP-SINGLEPROC-FIX-DEV4
body execution boundary: No LTP/SFT/GPU/eval or dry-run launch was performed.
```

Static no-execution checks run locally:

```text
git show origin/pr-41:scripts/train_qwen3_8b_sft.sh | bash -n
python compile() of origin/pr-41:scripts/write_sft_run_manifest.py
result: syntax_ok
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
- PR39 diagnostics worked and produced `preflight.json`, generated config, run manifest, stdout/stderr log, xtrace log, early-exit diagnostics, and exit status.
- Run manifest records `dataset_name: coding_agent_m1_sft_10_sharegpt`, train sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`, PR39 merge commit, save policy, and preflight log/xtrace/diagnostic paths.
- Generated config records `dataset: coding_agent_m1_sft_10_sharegpt`, output dir under `/home/xu.yang/coding_agent_playground/outputs`, `max_steps: 2`, `save_steps: 2`, `save_total_limit: 1`, and `tensor_model_parallel_size: 8`.

## Runtime Failure Signature

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

## PR #41 Gate Review

Functional diff reviewed from `origin/main...origin/pr-41`:

```text
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
workspace/interns/intern_code_dev_4/status.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_dataset_map_singleproc_fix.md
workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
```

Gate findings:

- PASS: PR #41 cites task `M1-S22-DATASET-MAP-SINGLEPROC-FIX-DEV4`, owner `intern_code_dev_4`, acceptance criteria, evidence path, and completion marker.
- PASS: PR #41 is open, non-draft, and GitHub reports `MERGEABLE` / `CLEAN`.
- PASS: config forces single-process/in-process preprocessing for the 10-row ShareGPT smoke:
  - `preprocessing_num_workers: null`
  - `dataloader_num_workers: 0`
- PASS: config preserves dataset name `coding_agent_m1_sft_10_sharegpt`.
- PASS: config preserves `/home/xu.yang/coding_agent_playground/outputs` output path.
- PASS: wrapper preserves PR39 diagnostics: stdout/stderr log, xtrace file, ERR/EXIT diagnostics, preflight JSON, runtime config copy, run manifest, and exit status.
- PASS: wrapper preserves `/home/xu.yang/coding_agent_playground/outputs` defaults for output root, run dir, checkpoint dir, tmpdir, logs, xtrace, and diagnostics.
- PASS: wrapper supports optional `PREPROCESSING_NUM_WORKERS` override, but the reviewed template already sets `preprocessing_num_workers: null`; generated runtime config should keep null unless a future owner explicitly overrides it.
- PASS: manifest writer records `preflight.preprocessing_num_workers` from the generated runtime config and records `PREPROCESSING_NUM_WORKERS` from the environment, making future runtime proof auditable.
- PASS: dev_4 evidence states no LTP/SFT/GPU/eval or dry-run launch was run for the package.

## dev_3 Data Confirmation Review

- PASS: dev_3 confirms no ShareGPT content/schema change is needed for this blocker.
- PASS: source artifact remains `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- PASS: source sha256 remains `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- PASS: row count remains 10.
- PASS: ShareGPT contract remains `messages[*].from/value` with provenance fields preserved.
- PASS: future staging/copy/tmp data artifacts must use `/home/xu.yang` unless explicitly justified.

## Current Blockers

None from dev_1 no-execution review.

## Completion Marker

```yaml
task_id: M1-S22-DATASET-MAP-REVIEW-DEV1
owner: intern_code_dev_1
result: PASS_FOR_PM_RETRY
runtime_blocker_confirmed: BLOCKED_POSTPATCH_RUNTIME_DATASET_MAP_EOF
pr_41_head: fc0b6062664e3eb5283e89c22a152427ca47fc3c
pr_41_mergeable: true
single_process_preprocessing_forced: true
preprocessing_num_workers: null
dataloader_num_workers: 0
pr39_diagnostics_preserved: true
home_xu_yang_paths_preserved: true
dev3_data_confirmation_present: true
data_content_schema_change_needed: false
old_keyerror_from_absent: true
enospc_absent: true
checkpoint_model_present: false
trainer_state_present: false
all_results_present: false
ltp_stopped_completed: true
endpoint_refused_after_stop: true
missing_inputs: []
no_remote_experiments_sft_gpu_eval_by_dev1: true
```
