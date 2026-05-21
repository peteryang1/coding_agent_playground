# Dev 4 S22 Dataset Map Single-Process Fix

Task ID: `M1-S22-DATASET-MAP-SINGLEPROC-FIX-DEV4`

Owner: `intern_code_dev_4`

Created: 2026-05-21

Scope: no-execution config/launcher patch package for the post-PR39 SFT blocker where the one authorized run failed during `datasets.map(num_proc=4)` with a multiprocessing `SyncManager` EOFError before training or checkpoint creation.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_dataset_map_singleproc_fix.md`

Completion marker: ready-for-review after PR opens; ready-for-runtime-gate only after PM/dev_1/test_1 gate. This task does not authorize LTP/SFT/GPU/eval or dry-run launch.

## Inputs Reviewed

Primary runtime evidence:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_postpatch_sft_runtime.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_postpatch_runtime_tracking.md
```

Key facts from dev_2 post-PR39 run:

```text
PR #39 diagnostics worked: preflight.json, generated config, run_manifest.json, stdout/stderr log, xtrace log, early_exit_diagnostics.txt, and exit_status.txt were produced under /home/xu.yang/coding_agent_playground/outputs.
run_id: milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
source git commit: 4a6c2968e1290d30415460b464eee638110958bc
source dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
output root: /home/xu.yang/coding_agent_playground/outputs
exit_status: EXIT_STATUS=1
failure signature: datasets.arrow_dataset.map -> multiprocess.managers.Manager.start -> reader.recv -> EOFError
log signature: Converting format of dataset (num_proc=4): 0/10
checkpoint/model/trainer_state/all_results: absent
LTP state: STOPPED (Completed); endpoint refused after stop
no eval run
```

Known non-regressions from the same evidence:

```text
KeyError: 'from': not observed
No space left on device / safetensors ENOSPC: not observed
checkpoint save failure: not reached
training step progress: not reached
```

## Diagnosis

The new blocker is not a data schema failure, storage-capacity failure, or PR39 observability failure. The run reached LLamaFactory dataset conversion and failed in the multiprocessing conversion layer before any training step or checkpoint save.

The active ShareGPT smoke config had:

```yaml
preprocessing_num_workers: 4
```

LLamaFactory passes this value to Hugging Face Datasets as `num_proc`. The reviewed LLamaFactory archive defines `preprocessing_num_workers` as `int | None`, default `None`, and passes it into dataset loading/mapping. For this 10-row smoke, multiprocessing gives no useful throughput benefit and introduces the observed `SyncManager` failure surface.

Preferred fix: force the 10-row ShareGPT smoke to use in-process dataset preprocessing by setting:

```yaml
preprocessing_num_workers: null
```

This should make the generated runtime config avoid `num_proc=4`; expected future log should no longer show `Converting format of dataset (num_proc=4)`.

## Patch Scope

Files patched in PR package:

```text
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_dataset_map_singleproc_fix.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md
workspace/interns/intern_code_dev_4/status.md
```

Config diff intent:

```yaml
# Keep the 10-row smoke preprocessing in-process. The post-PR39 runtime failed
# in datasets.map(num_proc=4) / SyncManager EOFError before training.
preprocessing_num_workers: null
dataloader_num_workers: 0
```

Launcher diff intent:

```text
scripts/train_qwen3_8b_sft.sh preserves PR39 diagnostics and adds PREPROCESSING_NUM_WORKERS as an optional runtime override. If set, it rewrites the generated runtime config's preprocessing_num_workers field before manifest creation and launch.
```

Manifest diff intent:

```text
scripts/write_sft_run_manifest.py records preprocessing_num_workers in preflight from the generated runtime config and records PREPROCESSING_NUM_WORKERS from the environment, so future runtime evidence can prove whether the generated config requested single-process preprocessing.
```

## Expected Future Runtime Evidence

If PM later authorizes a runtime, expected generated config proof should include:

```text
dataset: coding_agent_m1_sft_10_sharegpt
preprocessing_num_workers: null
dataloader_num_workers: 0
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
```

Expected manifest proof should include:

```text
preflight.dataset_name: coding_agent_m1_sft_10_sharegpt
preflight.preprocessing_num_workers: null
preflight.output_root: /home/xu.yang/coding_agent_playground/outputs
artifacts.run_dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>
artifacts.checkpoint_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
```

Expected log signature:

```text
The previous `Converting format of dataset (num_proc=4)` signature should be absent.
The run may either reach training/checkpoint behavior or expose a new blocker, but it should not use four dataset preprocessing worker processes for the 10-row smoke.
```

## Runtime Boundary

```text
No LTP/SFT/GPU/eval or dry-run launch was run by dev_4 for this task.
No new runtime is authorized by this package.
Future runtime requires PM gate plus dev_1/test_1/resource review.
```
