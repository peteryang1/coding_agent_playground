# Test 1 S22 Post-PR41 Runtime Gate

Task under gate: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`
Runtime owner: `intern_code_dev_2`
Test owner: `intern_code_test_1`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_postpr41_runtime_gate.md`
Status timestamp: `2026-05-21T10:20:00Z`

## Result

`BLOCKED_FINAL_RUNTIME`

No SFT, GPU command, LTP action, eval, or dry-run launch was run by `intern_code_test_1`.

## Inputs Checked

- PM authorization exists: `evidence/pm_s22_postpr41_runtime_authorization.md`.
- Authorized task: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`.
- Authorized owner: `intern_code_dev_2`.
- PR #41 merge commit required by PM: `2fc4b797a85c9375c6c5e1171963abe67aab35e8`.
- Required runtime evidence files are final:
  - `evidence/dev_2_s22_postpr41_sft_runtime.md`
  - `evidence/gpu_s22_postpr41_runtime_tracking.md`
- Final evidence records frame `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z`, endpoint `ssh -p 27021 root@10.100.22.14`, post-stop state `STOPPED (Completed)`, completed timestamp `2026-05-21 10:17:58`, and endpoint refused after stop.

## Final Post-Run Findings

### Authorization And Provenance

PASS.

- Task id: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`.
- Runtime owner: `intern_code_dev_2`.
- PR #41 merge commit: `2fc4b797a85c9375c6c5e1171963abe67aab35e8`.
- Evidence records exactly one authorized SFT smoke attempt.
- Evidence records no additional retry and no eval run.
- Frame: `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z`.
- Endpoint: `ssh -p 27021 root@10.100.22.14`.

### `/home/xu.yang` Storage

PASS.

- Required output root: `/home/xu.yang/coding_agent_playground/outputs`.
- CephFS proof: `/home/xu.yang` resolves to `/mnt/cephfs/home/xu.yang`; `findmnt` shows `/mnt/cephfs fuse.ceph-fuse ceph-fuse`.
- Capacity probe path: `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z`.
- Capacity probe result: `PASS_AND_CLEANED`, 4 x 6.0G real writes, `25769803776` bytes verified.
- Run dir, log, xtrace, diagnostics, manifest, runtime config, checkpoint root, and artifact preservation paths are under `/home/xu.yang/coding_agent_playground/outputs`.
- Existing non-`/home/xu.yang` paths are justified as read-only inputs: base model/dependencies under `/mnt/3fs` and source dataset under `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.

### PR39 Diagnostics

PASS.

dev_2 evidence records these durable artifacts with sizes and sha256 hashes:

```text
preflight.json
config/qwen3_8b_sft.yaml
run_manifest.json
logs/train_stdout_stderr.log
logs/train_xtrace.log
early_exit_diagnostics.txt
exit_status.txt
```

Wrapper diagnostics recorded `DIAGNOSTIC_REASON=ERR_TRAP` and `EXIT_STATUS=1`.

### PR41 Single-Process Preprocessing Proof

PASS.

- Runtime source commit is PR #41 merge commit `2fc4b797a85c9375c6c5e1171963abe67aab35e8`.
- Config template before launch records `preprocessing_num_workers: null` and `dataloader_num_workers: 0`.
- Runtime config records:
  - `dataset: coding_agent_m1_sft_10_sharegpt`
  - `preprocessing_num_workers: null`
  - `dataloader_num_workers: 0`
- Run manifest records `preflight.preprocessing_num_workers: null`.
- Runtime evidence records `PREPROCESSING_NUM_WORKERS: empty`.
- ShareGPT conversion completed `10/10` without `num_proc=4`.
- Previous `datasets.map(num_proc=4)` / SyncManager EOFError blocker was not reproduced.

### Data Contract

PASS.

- Dataset: `coding_agent_m1_sft_10_sharegpt`.
- Source artifact: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Source sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Row count: 10.
- `dataset_info` preserves ShareGPT mapping: `messages`, role tag `from`, content tag `value`, user `human`, assistant `gpt`.
- Training startup was reached: log contains `***** Running training *****`, `Num examples = 1`, and `Num Epochs = 2`.

### Runtime Result

FAIL: fresh exact runtime blocker.

- `EXIT_STATUS=1`.
- Failure class: CUDA/NCCL peer GPU memory / NVLink or hardware error during distributed training.
- Primary signature: `CUDA error: Invalid access of peer GPU memory over nvlink or a hardware error`.
- Torch elastic root cause: local rank 5, exit code `-6`, `SIGABRT`.
- No checkpoint save was reached.
- Exact blocker: `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.

### Checkpoint/Model Acceptance

FAIL.

- Checkpoint root: `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z`.
- Files present: only TensorBoard event file under `runs/May21_18-14-43_lg-cmc-b7r202-p07u16-h200-000708/`.
- Complete checkpoint/model: absent.
- `trainer_state.json`: absent.
- `all_results.json`: absent.
- `config.json`: absent.
- `model.safetensors`: absent.
- No PM-accepted replacement artifact is recorded.

### Old Failure Absence

PASS for old-signature absence.

- `KeyError: from`: absent.
- Missing/wrong `dataset_info`: absent.
- Wrong dataset name: absent.
- `datasets.map(num_proc=4)` / SyncManager EOFError: absent.
- ENOSPC / safetensors no-space: absent.
- Checkpoint-save failure: not reached.
- Early wrapper exit before diagnostics: absent.

### Stop Proof

PASS.

- Stop command recorded for frame `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z`.
- Stop issued: `2026-05-21T10:17:27Z`.
- Final state: `STOPPED (Completed)`.
- Completed timestamp: `2026-05-21 10:17:58`.
- Endpoint after stop: `ssh -p 27021 root@10.100.22.14` refused connection.
- Artifact preservation: `/home/xu.yang/coding_agent_playground/outputs` preserved on CephFS; shared mount path `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs` remains visible.
- No active coding_agent_playground / Milestone 1 / S22 post-PR41 GPU held by dev_2 after stop.

## Eval Handoff

`EVAL_HANDOFF_BLOCKED`

Eval handoff is blocked because there is no complete checkpoint/model, no `trainer_state.json`, no `all_results.json`, and no accepted replacement artifact. This is not a data-format, storage, PR39 diagnostics, or PR41 preprocessing blocker; it is a fresh runtime/node or distributed-backend blocker.

## Next Gate Recommendation

Before any further SFT runtime authorization, require a no-execution resource/runtime blocker review for `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`:

- Decide whether the next attempt should use a different H200 node, adjusted NCCL/NVL settings, or a minimal hardware/NCCL preflight.
- Preserve PR39 diagnostics and PR41 single-process preprocessing.
- Preserve `/home/xu.yang/coding_agent_playground/outputs` for all outputs/logs/checkpoints/run metadata/temp/intermediates.
- Require fresh PM authorization before any LTP/SFT/GPU retry.
- Post-run PASS still requires complete checkpoint/model, `trainer_state.json`, `all_results.json` or PM-accepted replacements, stop proof, and absence of old and new failure signatures.

## Post-Run Gate Checklist

Apply this checklist as soon as dev_2 final runtime evidence lands.

### 1. Authorization And Provenance

PASS requires:

- Task id remains `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`.
- Runtime source is merged main at PR #41 merge commit `2fc4b797a85c9375c6c5e1171963abe67aab35e8`.
- Evidence records exactly one PM-authorized owner run.
- No same-node retry, SFT rerun, GPU experiment, dry-run launch, or eval beyond the authorization.
- LTP job/frame id, node id, endpoint, `nodes.json`, submit/status/ssh/stop commands, and post-stop status are recorded.

### 2. `/home/xu.yang` Storage

PASS requires all launch outputs and generated/intermediate artifacts under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Required covered paths:

- stdout/stderr logs
- xtrace logs
- diagnostics and `exit_status.txt`
- preflight JSON
- run manifest
- generated runtime config
- temporary converted datasets and caches/intermediates controlled by the run
- checkpoints/model artifacts
- run metadata
- capacity probes

Any non-`/home/xu.yang` path is a gate failure unless it is an existing required input with explicit justification, such as the base model, dependency archives/wheels, or accepted source dataset.

### 3. PR39 Diagnostics

PASS requires durable PR39 diagnostics to exist and be hash/listing-verifiable:

- `train_stdout_stderr.log`
- `train_xtrace.log`
- `early_exit_diagnostics.txt`
- `exit_status.txt`
- `preflight.json`
- generated runtime config copy
- `run_manifest.json`

The manifest/preflight/config/log paths must agree with the `/home/xu.yang/coding_agent_playground/outputs` root.

### 4. PR41 Single-Process Preprocessing Proof

PASS requires:

- Generated config records dataset `coding_agent_m1_sft_10_sharegpt`.
- Generated config records `preprocessing_num_workers: null` or another PM/test accepted single-process equivalent.
- Generated config records `dataloader_num_workers: 0`.
- Run manifest records `preflight.preprocessing_num_workers` as the generated config value.
- Future log must not show the old failure signature `Converting format of dataset (num_proc=4): 0/10`.
- If `PREPROCESSING_NUM_WORKERS` is set in env, it must be explicitly justified and must not reintroduce multiprocessing for the 10-row smoke.

### 5. Data Contract

PASS requires:

- Dataset name: `coding_agent_m1_sft_10_sharegpt`.
- Source artifact: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Source sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Row count remains 10.
- ShareGPT mapping remains `messages[*].from/value`.
- No data regeneration or schema conversion appears unless separately authorized and evidenced.

### 6. Checkpoint/Model Acceptance

`PASS_FOR_EVAL_HANDOFF` requires:

- Complete checkpoint/model path under `/home/xu.yang/coding_agent_playground/outputs`.
- File listing with sizes and checksum or equivalent integrity proof.
- Required model/tokenizer/config artifacts present for downstream eval or serving.
- `trainer_state.json` present.
- `all_results.json` present.
- If either `trainer_state.json` or `all_results.json` is absent, PM/test must explicitly accept a replacement artifact before eval handoff.

### 7. Old Failure Absence

PASS requires absence of:

- `KeyError: 'from'`.
- Missing or wrong `dataset_info`.
- Wrong dataset name.
- `datasets.map(num_proc=4)` / SyncManager EOFError.
- Old scheduler signature failure.
- DP/TP zero-step or old DP=8/TP=8 mismatch failure.
- ENOSPC / safetensors no-space checkpoint failure.
- Early wrapper exit before diagnostics.

### 8. Stop Proof

PASS requires:

- Stop command recorded after success or failure.
- LTP reaches terminal stopped/released state.
- Endpoint post-stop is refused or otherwise unreachable as expected.
- Artifact preservation path remains visible on CephFS after stop.

### 9. Eval Handoff Decision

Record one of:

- `EVAL_HANDOFF_PASS`: only if checkpoint/model acceptance passes, `trainer_state.json` and `all_results.json` or accepted replacements exist, diagnostics are complete, old failures are absent, and stop proof passes.
- `EVAL_HANDOFF_BLOCKED`: if checkpoint/model, trainer state/results, diagnostics, stop proof, or old-failure absence fails.

Mini-swe eval remains unauthorized until PM gates the model/checkpoint or served endpoint.

## Current Decision

`BLOCKED_FINAL_RUNTIME`: dev_2 final durable evidence passes authorization/provenance, `/home/xu.yang` storage, PR39 diagnostics, PR41 single-process preprocessing, data contract, old-failure absence, and stop-proof gates. The runtime fails before checkpoint save with fresh `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`; checkpoint/model, `trainer_state.json`, and `all_results.json` are absent, so eval handoff is blocked.

## Completion Marker

```yaml
task_under_gate: M1-S22-POSTPR41-SFT-RUNTIME-DEV2
test_owner: intern_code_test_1
result: BLOCKED_FINAL_RUNTIME
pr41_merge_commit_required: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
pr41_merge_commit_observed: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
output_root_required: /home/xu.yang/coding_agent_playground/outputs
home_xu_yang_cephfs_pass: true
capacity_probe_24gib_pass: true
pr39_diagnostics_required: true
pr39_diagnostics_complete: true
pr41_single_process_preprocessing_required: true
preprocessing_num_workers_observed: null
sharegpt_conversion_10_of_10: true
training_startup_reached: true
exit_status: 1
runtime_blocker: BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY
checkpoint_model_required_for_eval: true
checkpoint_model_present: false
trainer_state_required: true
trainer_state_present: false
all_results_required: true
all_results_present: false
old_keyerror_from_absent: true
old_enospc_absent: true
old_num_proc4_syncmanager_absent: true
ltp_stopped_completed: true
endpoint_refused_after_stop: true
eval_handoff_allowed: false
eval_handoff_status: EVAL_HANDOFF_BLOCKED
sft_gpu_eval_executed_by_test1: false
```
