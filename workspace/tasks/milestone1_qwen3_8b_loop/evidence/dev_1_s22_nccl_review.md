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

## Standby Review Template for M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2

Standby status: `COMPLETED_WITH_PREFLIGHT_BLOCKER`

PM has authorized `intern_code_dev_2` for `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`: one fresh 8 x H200 allocation, NCCL/NVLink preflight first, and exactly one SFT smoke only if preflight passes. dev_1 did not run LTP/GPU/preflight/SFT/eval.

Known gate inputs before dev_2 evidence lands:

```text
PR #43 merged at 2026-05-21T10:47:20Z, merge commit 2c867d3226f7ebb4962b5b173235639df8f1f9be.
PR #44 merged at 2026-05-21T10:50:28Z, merge commit 6dcdc6730debeb2fb875baaec6667cb64d09867d.
PM authorization evidence: evidence/pm_s22_nccl_preflight_sft_authorization.md.
Required dev_2 evidence: evidence/dev_2_s22_nccl_preflight_sft_runtime.md.
Required GPU tracking: evidence/gpu_s22_nccl_preflight_sft_tracking.md.
No eval authorized.
```

When dev_2 evidence lands, dev_1 will update this evidence and status to `PASS_FOR_PM_NEXT_GATE` or an exact blocker by checking the following:

1. Authorization and merge provenance
   - Task id is `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`.
   - Runtime owner is `intern_code_dev_2`.
   - PR #43 and PR #44 merge facts are cited.
   - Evidence cites PM authorization path.
   - Attempt count obeys PM authorization: preflight first; SFT starts only if preflight passes; no eval.

2. Different-node/resource proof
   - Fresh LTP frame/job/node/endpoint are recorded.
   - New physical node is different from failed node `lg-cmc-b7r202-p07u16-h200-000708`, or a PM/resource-owner exception is explicitly justified.
   - Prior post-PR41 frame remains stopped.
   - No unrelated active Milestone GPU is held after stop.

3. `/home/xu.yang` paths
   - `/home/xu.yang` resolves to CephFS.
   - Capacity probe runs under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>`.
   - Preflight artifacts are under `/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>`.
   - SFT run dir, logs, xtrace, diagnostics, manifest, runtime config, checkpoints, tmp/intermediates, nodes JSON, and run metadata are under `/home/xu.yang/coding_agent_playground/outputs`.
   - Non-`/home/xu.yang` paths are limited to justified read-only inputs: base model, dependency archives/wheels, and accepted source dataset.

4. NCCL/NVLink preflight result
   - Preflight captures hostname, `nvidia-smi -L`, topology, NVLink status, and ECC/PCI/NVLink/performance diagnostics.
   - 8-rank NCCL or PyTorch all-reduce preflight result is recorded if used.
   - PASS requires no NCCL/CUDA invalid peer memory, SIGABRT, Xid, missing/unhealthy GPU, or NVLink link error.
   - If preflight fails, SFT must not run; evidence must record exact preflight blocker and stop proof.

5. SFT command/env if run
   - SFT runs only after preflight PASS.
   - Command preserves PR39 diagnostics and PR41 preprocessing:
     - `DATASET_NAME=coding_agent_m1_sft_10_sharegpt`
     - `preprocessing_num_workers: null`
     - `dataloader_num_workers: 0`
     - `OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs`
   - NCCL/CUDA env additions from mitigation are recorded, especially `NCCL_DEBUG=INFO`, `NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL`, `NCCL_ASYNC_ERROR_HANDLING=1`, `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`, and `CUDA_DEVICE_MAX_CONNECTIONS=1`.
   - Any `NCCL_P2P_DISABLE=1` use must have explicit PM/dev_1/test_1 acceptance because dev_4 marked it fallback-only.

6. SFT post-run artifacts or exact blocker
   - PASS_FOR_PM_NEXT_GATE requires a complete checkpoint/model and `trainer_state.json` plus `all_results.json`, or PM/test accepted replacement artifacts.
   - If no checkpoint/model exists, evidence must record exact blocker with logs, exit status, diagnostics, node status, and whether old signatures returned.
   - Old blockers to check absent: `KeyError: from`, wrong/missing dataset_info, `datasets.map(num_proc=4)` SyncManager EOFError, ENOSPC/safetensors no-space, early wrapper diagnostics gap, and the prior NCCL/NVLink peer-memory signature.

7. Stop proof
   - Stop command/action is recorded after preflight failure, SFT completion/failure, idle/health limit, or checkpoint.
   - Final LTP state and completed timestamp are recorded.
   - Endpoint refused proof after stop is recorded.
   - Artifact preservation under `/home/xu.yang/coding_agent_playground/outputs` is recorded.

Template output decisions:

```text
PASS_FOR_PM_NEXT_GATE: preflight passes, SFT either produces accepted checkpoint/model artifacts or reaches a PM/test-defined next gate with complete evidence and no launch-blocking inconsistency.
BLOCKER_PREFLIGHT_FAILED: preflight fails and SFT is correctly not run.
BLOCKER_SFT_RUNTIME_<signature>: SFT runs after preflight pass but fails with exact blocker.
BLOCKER_AUTHORIZATION_OR_PROVENANCE: task id, PR43/PR44 merge facts, PM authorization, attempt count, or no-eval boundary is inconsistent.
BLOCKER_STORAGE_PATH: required outputs/preflight/intermediates are outside /home/xu.yang without accepted exception.
BLOCKER_STOP_PROOF: final stop/release/endpoint-refused proof is missing.
```

## Final Gate Review for M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2

Review result: `BLOCKER_PREFLIGHT_FAILED_NO_SFT_RUN_HEALTH_SIGNATURE_AMBIGUOUS`

dev_2 final evidence is present:

- `evidence/dev_2_s22_nccl_preflight_sft_runtime.md`
- `evidence/gpu_s22_nccl_preflight_sft_tracking.md`

dev_1 did not run remote experiments, SFT, GPU, or eval.

### Runtime/Authorization Review

- PASS: task id is `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`.
- PASS: runtime owner is `intern_code_dev_2`.
- PASS: PM authorization path is cited: `evidence/pm_s22_nccl_preflight_sft_authorization.md`.
- PASS: authorization boundary was followed: preflight first, SFT only if preflight passes, no eval.
- PASS: SFT was not run because preflight wrote a FAIL marker.

### Node and Resource Review

- PASS: fresh node is `lg-cmc-b7r401-a04u26-h200-000769`.
- PASS: fresh endpoint was `ssh -p 27402 root@10.100.24.11`.
- PASS: different-node check passed against failed node `lg-cmc-b7r202-p07u16-h200-000708`.
- PASS: allocation stopped after preflight failure.
- PASS: final LTP state is `STOPPED (Completed)`, completed `2026-05-21 11:02:09`.
- PASS: endpoint refused after stop.

### Storage and Artifact Review

- PASS: `/home/xu.yang` was linked to `/mnt/cephfs/home/xu.yang`.
- PASS: preflight artifacts are preserved under `/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z`.
- PASS: preserved CephFS path is `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z`.
- PASS: capacity probe passed and cleaned: 4 x 6GiB writes, `25769803776` bytes verified.
- PASS: topology and NVLink evidence were captured; evidence records `NV18` between GPU pairs and NVLink status links 0-17 at 26.562 GB/s per GPU.

### Preflight Review

- PASS: 8 x NVIDIA H200 visible and idle before/after preflight.
- PASS: `all_reduce_perf` was unavailable, and dev_2 used an acceptable torchrun 8-rank NCCL all-reduce substitute.
- PASS: torch NCCL all-reduce exited 0:
  - `TORCHRUN_EXIT=0`
  - start `2026-05-21T10:59:18Z`
  - end `2026-05-21T10:59:31Z`
- PASS: NCCL env was recorded:
  - `NCCL_DEBUG=INFO`
  - `NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL`
  - `NCCL_ASYNC_ERROR_HANDLING=1`
  - `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`
  - `CUDA_DEVICE_MAX_CONNECTIONS=1`
  - `NCCL_P2P_DISABLE` unset.
- BLOCKER: final preflight marker is `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.

dev_1 interpretation of the blocker:

```text
The blocker is not a failed torch NCCL all-reduce, capacity probe, different-node gate, /home/xu.yang path, or stop proof. Those checks pass by durable evidence.

The blocker is the preflight health parser/result: a broad recursive scan of the preflight directory matched evidence/command/process/generic NVRM text and wrote PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE. Because the PM authorization allowed SFT only if preflight passes, dev_2 correctly did not run SFT.
```

### Conditional SFT Review

- PASS: SFT was not run.
- PASS: no eval was run.
- EXPECTED: no checkpoint/model exists because SFT was not run.
- EXPECTED: `trainer_state.json` absent because SFT was not run.
- EXPECTED: `all_results.json` absent because SFT was not run.

### Exact Current Blocker

`BLOCKER_PREFLIGHT_FAILED_NO_SFT_RUN_HEALTH_SIGNATURE_AMBIGUOUS`

This is a preflight gate/parser blocker, not an SFT runtime blocker. The durable FAIL marker must be respected, but the evidence also shows the concrete torch NCCL preflight succeeded and that the failure was caused by broad health-signature matching over command/process/generic text.

### Recommended Next PM Gate/Fix

Recommended next task/gate: no-execution preflight parser refinement before any new GPU authorization.

Acceptance criteria for the next fix:

- Narrow the health scan to actionable failure sources only, such as dedicated `nvidia-smi` health outputs, torch/NCCL preflight stderr/stdout, dmesg/Xid logs if intentionally captured, and explicit return codes.
- Do not recursively scan generated command text, process-list text, shell scripts, or prior evidence copies for generic strings like `hardware error`, `SIGABRT`, `fatal`, or `NVRM`.
- Distinguish historical/generic NVRM/NVLink initialization text from actionable current GPU fault patterns.
- Preserve fail-fast behavior for actual NCCL/CUDA invalid peer memory, Xid, ECC, missing GPU, NVLink link failure, nonzero torchrun preflight exit, or inability to write `/home/xu.yang` artifacts.
- Produce a structured preflight summary with separate fields:
  - `capacity_probe_status`
  - `torch_nccl_allreduce_status`
  - `nvidia_smi_health_status`
  - `nvlink_status`
  - `parser_health_status`
  - `overall_preflight_result`
- Continue to require fresh PM authorization before any new LTP/GPU/preflight/SFT attempt.

## Completion Marker

```yaml
task_id: M1-S22-NCCL-REVIEW-DEV1
owner: intern_code_dev_1
result: BLOCKER_PREFLIGHT_FAILED_NO_SFT_RUN_HEALTH_SIGNATURE_AMBIGUOUS
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
standby_template_for: M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2
standby_status: COMPLETED_WITH_PREFLIGHT_BLOCKER
preflight_runtime_task: M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2
preflight_node: lg-cmc-b7r401-a04u26-h200-000769
preflight_endpoint: ssh -p 27402 root@10.100.24.11
different_node_check_passed: true
capacity_probe_passed_and_cleaned: true
torch_8rank_nccl_allreduce_exit_0: true
preflight_marker: PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
sft_run: false
eval_run: false
stop_proof_passed: true
next_pm_gate_recommendation: refine_no_execution_preflight_health_parser_before_new_gpu_authorization
```
