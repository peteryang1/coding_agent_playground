# M1-S22-NCCL-REVIEW-DEV1

Owner: `intern_code_dev_1`
Task: `M1-S22-NCCL-REVIEW-DEV1`
Evidence date: 2026-05-21
Execution boundary: no remote experiments, SFT, GPU, or eval run by dev_1.

## Result

`PASS_FOR_PM_RETRY`

dev_1 refreshed the review after dev_4 mitigation and dev_2 resource packages landed. No remaining dev_1 blocker found for PM to decide the next NCCL/NVLink mitigation retry gate.

This pass does not itself authorize LTP/SFT/GPU/eval. Any future preflight or SFT runtime still requires explicit PM authorization and the applicable test/resource gates.

## Inputs Reviewed

- `evidence/dev_2_s22_postpr41_sft_runtime.md`
- `evidence/gpu_s22_postpr41_runtime_tracking.md`
- `evidence/test_1_s22_postpr41_runtime_gate.md`
- `evidence/pm_s22_nccl_nvlink_blocker_gate.md`
- `evidence/dev_4_s22_nccl_mitigation.md`
- `evidence/dev_2_s22_nccl_resource_plan.md`
- `evidence/dev_3_s22_nccl_data_confirm.md`
- PR #43: `https://github.com/peteryang1/coding_agent_playground/pull/43`
- `task_registry.md`

PR #43 metadata checked:

```text
state: OPEN
draft: false
mergeable: MERGEABLE
merge_state: CLEAN
head: intern_code_dev_4/M1-S22-NCCL-MITIGATION-DEV4
head_commit: 5f4d14a12aa8044a429d1110757ed631a7bc9833
title: M1-S22-NCCL-MITIGATION-DEV4
body execution boundary: No LTP/SFT/GPU/eval or dry-run launch was performed.
```

Static no-execution checks run locally against PR #43 script snapshots:

```text
bash -n scripts/train_qwen3_8b_sft.sh
python py_compile scripts/write_sft_run_manifest.py
result: syntax_ok
```

## Runtime Facts Confirmed

The fresh blocker is a CUDA/NCCL/NVLink distributed runtime blocker after prior data, storage, diagnostics, and preprocessing blockers were cleared.

Confirmed facts:

- Runtime task: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`.
- Runtime owner: `intern_code_dev_2`.
- PR #41 merge commit used: `2fc4b797a85c9375c6c5e1171963abe67aab35e8`.
- LTP frame: `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z`.
- Failed node: `lg-cmc-b7r202-p07u16-h200-000708`.
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

PR39/PR41 facts:

- PR39 diagnostics produced preflight JSON, runtime config, run manifest, stdout/stderr log, xtrace log, early-exit diagnostics, and exit status.
- Runtime config records `dataset: coding_agent_m1_sft_10_sharegpt`.
- Runtime config records `preprocessing_num_workers: null`.
- Runtime config records `dataloader_num_workers: 0`.
- Run manifest records `preflight.preprocessing_num_workers: null`.
- `PREPROCESSING_NUM_WORKERS` environment was empty.
- ShareGPT conversion completed `10/10` without `num_proc=4`.
- Training startup was reached.

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

Old blockers did not recur:

- `KeyError: from`: absent.
- Missing/wrong dataset_info: absent.
- Wrong dataset name: absent.
- `datasets.map(num_proc=4)` / SyncManager EOFError: absent.
- ENOSPC / safetensors no-space: absent.
- Checkpoint save failure: not reached.
- Early wrapper exit before diagnostics: absent.

## dev_4 Mitigation Review

`evidence/dev_4_s22_nccl_mitigation.md` and PR #43 are coherent:

- PASS: cites the post-PR41 runtime blocker and local rank 5 SIGABRT.
- PASS: classifies the issue as hardware or distributed-backend sensitive, not data-format, storage, PR39 diagnostics, or PR41 preprocessing.
- PASS: recommends a fresh H200 allocation, preferably a different physical node than `lg-cmc-b7r202-p07u16-h200-000708`.
- PASS: explicitly says not to reuse stopped endpoint `ssh -p 27021 root@10.100.22.14`.
- PASS: defines a bounded hardware/NCCL preflight before SFT, with artifacts under `/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>`.
- PASS: preflight captures `hostname`, `nvidia-smi -L`, topology, NVLink status, ECC/PCI/NVLink/performance query, and an 8-rank NCCL all-reduce preflight when available.
- PASS: preflight pass/fail criteria are explicit, including failure on NCCL/CUDA invalid peer memory, SIGABRT, Xid, NVLink link error, missing/unhealthy GPU, or failure to write `/home/xu.yang` artifacts.
- PASS: preserves PR39 diagnostics, PR41 `preprocessing_num_workers: null`, ShareGPT dataset name, source dataset, base model, and `/home/xu.yang` output root.
- PASS: proposes future NCCL/CUDA env additions for a PM-gated retry: `NCCL_DEBUG=INFO`, `NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL`, `NCCL_ASYNC_ERROR_HANDLING=1`, `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`, and `CUDA_DEVICE_MAX_CONNECTIONS=1`.
- PASS: treats `NCCL_P2P_DISABLE=1` as fallback only with explicit PM/dev_1/test_1 acceptance, not default.
- PASS: records no LTP/SFT/GPU/eval or dry-run launch by dev_4.

PR #43 scope note:

- PR #43 currently contains the dev_4 mitigation evidence/status/history/task records only; it does not make additional runtime code changes beyond already merged PR39/PR41 code. That is acceptable for this no-execution mitigation package because the proposed mitigation is resource/preflight/env driven.

## dev_2 Resource Plan Review

`evidence/dev_2_s22_nccl_resource_plan.md` is coherent:

- PASS: records no-submit/no-GPU/no-SFT/no-eval/no-dry-run boundary.
- PASS: confirms prior frame `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z` is `STOPPED (Completed)`.
- PASS: confirms prior endpoint refused after STOPPED state.
- PASS: records no active coding_agent_playground / Milestone 1 / S22 NCCL retry GPU held by dev_2.
- PASS: recommends a fresh single-node 8 x H200 allocation on a different physical node than `lg-cmc-b7r202-p07u16-h200-000708`.
- PASS: includes H200 resource shape and LTP submit/status/ssh/stop templates as templates only.
- PASS: preserves `/home/xu.yang/coding_agent_playground/outputs` for run dir, checkpoint dir, tmpdir, capacity probe, nodes JSON, logs, metadata, and intermediates.
- PASS: preserves required read-only exceptions for base model, dependencies, and source dataset.
- PASS: includes capacity probe template and stop proof requirements.
- PASS: states no submit without fresh PM authorization.

## dev_3 Data Confirmation Review

`evidence/dev_3_s22_nccl_data_confirm.md` remains coherent:

- PASS: confirms no ShareGPT data/package change is implicated by the NCCL/NVLink blocker.
- PASS: keeps accepted source artifact `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- PASS: source sha256 remains `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- PASS: row count remains 10.
- PASS: ShareGPT contract remains `messages[*].from/value` with provenance fields preserved.
- PASS: correctly cites ShareGPT conversion `10/10`, PR41 single-process preprocessing, training startup reached, and old data/preprocessing/storage signatures absent.
- PASS: future temporary/staging/intermediate data artifacts must default under `/home/xu.yang`.

## Current Blockers

None from dev_1 no-execution review.

Remaining non-dev_1 conditions before any actual run:

- PM must explicitly authorize any LTP/GPU/NCCL preflight/SFT runtime.
- Test/resource gates must decide whether PR #43 and the resource plan are sufficient for launch.
- Future runtime must still pass post-run acceptance: complete checkpoint/model, `trainer_state.json`, `all_results.json` or PM-accepted replacements, stop proof, and absence/resolution of old and NCCL/NVLink failure signatures.

## Completion Marker

```yaml
task_id: M1-S22-NCCL-REVIEW-DEV1
owner: intern_code_dev_1
result: PASS_FOR_PM_RETRY
fresh_blocker: BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY
pr41_commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
pr43_head: 5f4d14a12aa8044a429d1110757ed631a7bc9833
pr43_mergeable_clean: true
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
dev4_mitigation_present: true
dev2_resource_plan_present: true
dev3_data_confirm_present: true
different_h200_node_recommended: true
nccl_preflight_required_before_sft: true
data_change_needed: false
missing_inputs: []
no_remote_experiments_sft_gpu_eval_by_dev1: true
```
