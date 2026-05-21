# M1-S22-NCCL-REVIEW-DEV1

Owner: `intern_code_dev_1`
Task: `M1-S22-NCCL-REVIEW-DEV1`
Evidence date: 2026-05-21
Execution boundary: no remote experiments, SFT, GPU, or eval run by dev_1.

## Result

`WAITING_MITIGATION_PACKAGES`

dev_1 reviewed the fresh post-PR41 runtime blocker facts and the currently available dev_3 data confirmation. No `PASS_FOR_PM_RETRY` yet because mitigation/resource inputs are still missing:

- Missing: `evidence/dev_4_s22_nccl_mitigation.md`
- Missing: `evidence/dev_2_s22_nccl_resource_plan.md`
- Present: `evidence/dev_3_s22_nccl_data_confirm.md`

## Inputs Reviewed

- `evidence/dev_2_s22_postpr41_sft_runtime.md`
- `evidence/gpu_s22_postpr41_runtime_tracking.md`
- `evidence/test_1_s22_postpr41_runtime_gate.md`
- `evidence/pm_s22_nccl_nvlink_blocker_gate.md`
- `evidence/dev_3_s22_nccl_data_confirm.md`
- `task_registry.md`

Checked mitigation package inputs:

```text
evidence/dev_4_s22_nccl_mitigation.md: MISSING
evidence/dev_2_s22_nccl_resource_plan.md: MISSING
evidence/dev_3_s22_nccl_data_confirm.md: PRESENT
```

## Confirmed Runtime Facts

The fresh blocker is a CUDA/NCCL/NVLink distributed runtime blocker after the prior data, storage, diagnostics, and preprocessing blockers were cleared.

Confirmed facts:

- Runtime task: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`.
- Runtime owner: `intern_code_dev_2`.
- PR #41 merge commit used: `2fc4b797a85c9375c6c5e1171963abe67aab35e8`.
- LTP frame: `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z`.
- Node: `lg-cmc-b7r202-p07u16-h200-000708`.
- Endpoint while active: `ssh -p 27021 root@10.100.22.14`.
- Stop proof: `STOPPED (Completed)`, completed `2026-05-21 10:17:58`, endpoint refused after stop.
- Eval was not run.
- No active coding_agent_playground / Milestone 1 / S22 post-PR41 GPU is held by dev_2 after stop.

Storage and path facts:

- Output root: `/home/xu.yang/coding_agent_playground/outputs`.
- `/home/xu.yang` resolved to `/mnt/cephfs/home/xu.yang`.
- Capacity probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/...` wrote and cleaned `25769803776` bytes.
- Run dir, log, xtrace, diagnostics, manifest, runtime config, checkpoint root, and artifact preservation paths are under `/home/xu.yang/coding_agent_playground/outputs`.
- Existing non-`/home/xu.yang` paths are justified read-only inputs: base model and dependencies under `/mnt/3fs`, source dataset under `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.

PR39/PR41 gate facts:

- PR39 diagnostics produced preflight JSON, runtime config, run manifest, stdout/stderr log, xtrace log, early-exit diagnostics, and exit status.
- Runtime config records `dataset: coding_agent_m1_sft_10_sharegpt`.
- Runtime config records `preprocessing_num_workers: null`.
- Runtime config records `dataloader_num_workers: 0`.
- Run manifest records `preflight.preprocessing_num_workers: null`.
- `PREPROCESSING_NUM_WORKERS` environment was empty.
- ShareGPT conversion completed `10/10` without `num_proc=4`.
- Training startup was reached: test_1 evidence cites `***** Running training *****`, `Num examples = 1`, and `Num Epochs = 2`.

## Fresh Blocker

The post-PR41 run failed after training startup and before checkpoint save:

```text
EXIT_STATUS=1
failure class: CUDA/NCCL peer GPU memory / NVLink or hardware error during distributed training
primary signature: CUDA error: Invalid access of peer GPU memory over nvlink or a hardware error
torch elastic root cause: local_rank 5, exitcode -6, SIGABRT
exact blocker: BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY
```

Checkpoint/model/result status:

```text
complete checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
config.json: absent
model.safetensors: absent
files present: only TensorBoard event file under the output runs directory
```

## Old Blocker Absence

Durable evidence says these previous blockers did not recur:

- Old `KeyError: from`: absent.
- Missing/wrong dataset_info: absent.
- Wrong dataset name: absent.
- `datasets.map(num_proc=4)` / SyncManager EOFError: absent.
- ENOSPC / safetensors no-space: absent.
- Checkpoint save failure: not reached.
- Early wrapper exit before diagnostics: absent.

## dev_3 Data Confirmation Review

`evidence/dev_3_s22_nccl_data_confirm.md` is present and coherent with runtime evidence:

- dev_3 concludes no data/package change is implicated by the fresh NCCL/NVLink blocker.
- Accepted source artifact remains `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Source sha256 remains `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Row count remains 10.
- ShareGPT contract remains `messages[*].from/value` with provenance fields preserved.
- dev_3 correctly cites ShareGPT conversion `10/10`, PR41 single-process preprocessing, training startup reached, and old data/preprocessing/storage signatures absent.
- Future temporary/staging/intermediate data artifacts must default under `/home/xu.yang`.

## Waiting Inputs

dev_1 cannot decide PASS/BLOCKER for the next retry until the mitigation/resource packages land.

Required pending inputs:

1. `M1-S22-NCCL-MITIGATION-DEV4`: no-execution mitigation package that proposes exact NCCL/NVL/launcher or hardware-preflight mitigation, states whether a different H200 node is required, preserves PR39 diagnostics, PR41 single-process preprocessing, and `/home/xu.yang` paths.
2. `M1-S22-NCCL-RESOURCE-DEV2`: no-submit resource plan that confirms no active Milestone GPU, prior post-PR41 frame stopped, recommends different-node or NCCL preflight resource shape, includes submit/status/stop templates and `/home/xu.yang` capacity/output plan, and states no submit without fresh PM authorization.

## Current Blockers

No data-side blocker found from current dev_3 package.

Exact current blockers to PASS:

- `MISSING_DEV4_NCCL_MITIGATION_PACKAGE`: `evidence/dev_4_s22_nccl_mitigation.md` is absent.
- `MISSING_DEV2_NCCL_RESOURCE_PLAN`: `evidence/dev_2_s22_nccl_resource_plan.md` is absent.

## Completion Marker

```yaml
task_id: M1-S22-NCCL-REVIEW-DEV1
owner: intern_code_dev_1
result: WAITING_MITIGATION_PACKAGES
fresh_blocker: BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY
pr41_commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
home_xu_yang_paths_preserved: true
preprocessing_num_workers: null
sharegpt_conversion_completed_10_of_10: true
training_startup_reached: true
checkpoint_model_present: false
trainer_state_present: false
all_results_present: false
old_keyerror_from_absent: true
old_enospc_absent: true
old_dataset_map_num_proc4_absent: true
ltp_stopped_completed: true
dev3_data_confirm_present: true
data_change_needed: false
missing_inputs:
  - evidence/dev_4_s22_nccl_mitigation.md
  - evidence/dev_2_s22_nccl_resource_plan.md
no_remote_experiments_sft_gpu_eval_by_dev1: true
```
