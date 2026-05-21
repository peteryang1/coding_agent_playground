# Test 1 S22 NCCL/NVLink Retry Gate

Task ID: `M1-S22-NCCL-GATE-TEST1`
Owner: `intern_code_test_1`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_nccl_retry_gate.md`
Status timestamp: `2026-05-21T11:08:50Z`

## Result

`PASS_FOR_PM_RETRY`

No SFT, GPU command, LTP action, eval, or dry-run launch was run by `intern_code_test_1`.

## Runtime Watch: M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2

Current watch result: `PASS_FOR_NEXT_PM_DECISION`

PM has authorized `intern_code_dev_2` only for task `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`: one fresh single-node 8 x H200 LTP allocation, NCCL/NVLink preflight first, and exactly one SFT smoke only if preflight passes. Mini-swe eval is not authorized.

Authorization checked:

- Authorization file: `evidence/pm_s22_nccl_preflight_sft_authorization.md`.
- Authorization timestamp: `2026-05-21T10:53:00Z`.
- Decision: `AUTHORIZED_DEV2_ONLY_ONE_FRESH_DIFFERENT_NODE_PREFLIGHT_THEN_CONDITIONAL_SFT`.
- PR #43 merged at `2026-05-21T10:47:20Z`, merge commit `2c867d3226f7ebb4962b5b173235639df8f1f9be`.
- PR #44 merged at `2026-05-21T10:50:28Z`, merge commit `6dcdc6730debeb2fb875baaec6667cb64d09867d`.

Final dev_2 evidence state:

- `evidence/dev_2_s22_nccl_preflight_sft_runtime.md` records final result `BLOCKED_PREFLIGHT_FAILED_NO_SFT_RUN`.
- `evidence/gpu_s22_nccl_preflight_sft_tracking.md` records final result `STOPPED_AFTER_PREFLIGHT_FAILURE_NO_SFT`.
- SFT was not run because the durable preflight marker was FAIL.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` exists because SFT was not run.
- Stop proof is present and endpoint refused after stop.

### Final Preflight/SFT Gate Result

`PASS_FOR_NEXT_PM_DECISION`

This is not `PASS_FOR_EVAL_HANDOFF`: eval handoff remains blocked because SFT was not run and no checkpoint/model, `trainer_state.json`, or `all_results.json` exists.

Final facts verified from durable evidence:

- Frame: `xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z`.
- Endpoint while active: `ssh -p 27402 root@10.100.24.11`.
- Fresh node: `lg-cmc-b7r401-a04u26-h200-000769`.
- Different-node gate: PASS, not failed post-PR41 node `lg-cmc-b7r202-p07u16-h200-000708`.
- `/home/xu.yang/coding_agent_playground/outputs` storage contract: PASS.
- Preflight artifact root: `/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z`.
- CephFS preserved path: `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z`.
- Capacity probe: PASS_AND_CLEANED, 4 x 6GiB writes, `25769803776` bytes verified.
- Topology/NVLink captured: `nvidia-smi topo -m` showed NV18 between every GPU pair; `nvidia-smi nvlink --status` captured links 0-17 at 26.562 GB/s per GPU.
- Torch NCCL substitute: `torchrun --standalone --nnodes 1 --nproc_per_node 8 torch_nccl_allreduce.py`, `TORCHRUN_EXIT=0`.
- NCCL env evidence: `NCCL_DEBUG=INFO`, `NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL`, `NCCL_ASYNC_ERROR_HANDLING=1`, `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`, `CUDA_DEVICE_MAX_CONNECTIONS=1`; `NCCL_P2P_DISABLE` unset.
- Final preflight marker: `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.
- Health-signature cause recorded by dev_2: broad health scan matched evidence/command/process/generic NVRM text in preflight artifacts, including command text/process-scan copies containing searched terms.
- SFT command executed: no.
- SFT config/log/checkpoint path: none.
- Stop result: `STOPPED (Completed)`, completed `2026-05-21 11:02:09`.
- Endpoint proof after stop: `ssh -p 27402 root@10.100.24.11` refused connection.
- Artifact preservation: preflight artifacts remain under `/home/xu.yang/coding_agent_playground/outputs/preflight/...` on CephFS.

### Final Blocker And PM Decision Point

Exact blocker for eval handoff:

`EVAL_HANDOFF_BLOCKED_NO_SFT_NO_CHECKPOINT`

Operational blocker for next PM decision:

`BLOCKED_PREFLIGHT_FAILED_NO_SFT_RUN`

The failure is a preflight health-parser/health-signature gate failure, not a failed SFT run. The 8-rank torch NCCL all-reduce exited 0, capacity passed, topology/NVLink was captured, and immediate post-preflight GPU/process sampling was clean, but the durable final preflight marker is FAIL. Dev_2 correctly did not run SFT under the PM contract.

### Next Retry/Fix Criteria

Before any future PM authorization:

- Refine the preflight health parser so it does not scan its own command text, process-scan output, or copied historical evidence terms as actionable health failures.
- Separate actionable GPU/NCCL health faults from generic/historical NVRM/NVLink initialization text.
- Preserve failure-on-real-fault behavior for Xid, fatal ECC, NVLink link error, invalid peer GPU memory, rank SIGABRT, and NCCL collective failure.
- Continue to require a fresh allocation, preferably a different healthy H200 node if the current allocation has been stopped.
- Continue to require `/home/xu.yang/coding_agent_playground/outputs` for preflight/SFT artifacts.
- Continue to require capacity probe, topology/NVLink capture, NCCL collective preflight, and a clear PASS marker before SFT.
- Continue to forbid SFT if preflight marker is FAIL.
- If SFT later runs, post-run eval handoff still requires complete checkpoint/model plus `trainer_state.json` and `all_results.json` or PM/test accepted replacements, PR39 diagnostics, PR41 preprocessing, stop proof, and old blocker absence.

### Post-Run Decision Labels

When final dev_2 evidence lands, test_1 will record exactly one of:

- `PASS_FOR_EVAL_HANDOFF`: preflight passes, SFT runs and produces complete checkpoint/model plus `trainer_state.json` and `all_results.json` or accepted replacements, diagnostics/storage/stop/old-failure gates pass, and PM may decide eval handoff.
- `PASS_FOR_NEXT_PM_DECISION`: preflight and/or runtime evidence is complete enough for PM to decide the next action, but eval handoff is not allowed, for example preflight passes but SFT exposes a fresh exact blocker, or preflight fails cleanly with complete stop/artifact proof.
- Exact blocker: required evidence is missing, storage/diagnostics/preflight/stop proof fails, old blocker recurs, SFT runs despite failed preflight, same failed node is reused without PM acceptance, or a runtime blocker lacks reproducible evidence.

### Required Preflight Gate

PASS for preflight requires durable evidence of:

- Fresh LTP frame/job id, node id, endpoint, `nodes.json`, submit/status commands, and start time.
- Different-node proof against failed post-PR41 node `lg-cmc-b7r202-p07u16-h200-000708`, unless PM explicitly accepts same-node use later.
- `/home/xu.yang/coding_agent_playground/outputs` CephFS proof and capacity/write proof.
- Preflight root under `/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>`.
- Captured `hostname`, `nvidia-smi -L`, `nvidia-smi topo -m`, NVLink/NVSwitch health where available, and ECC/Xid/PCI/NVLink checks where available.
- 8-rank NCCL all-reduce or equivalent NCCL collective preflight if tool is available, or exact blocker if unavailable.
- Preflight PASS/FAIL conclusion before any SFT command starts.

Preflight FAIL conditions:

- Same physical node as `lg-cmc-b7r202-p07u16-h200-000708` without explicit later PM acceptance.
- Missing/unhealthy GPU.
- Xid, fatal ECC, NVLink link error, PCI fault, NCCL/CUDA invalid peer memory signature, rank SIGABRT, collective failure, or inability to write artifacts under `/home/xu.yang`.
- If preflight fails, SFT must not run and dev_2 must stop/release the allocation.

### Conditional SFT Gate If Preflight Passes

If and only if preflight passes, SFT evidence must include:

- Exact SFT command/env/config and owner boundary.
- Runtime source includes PR #43 and PR #44 merged state, plus already-merged PR39/PR41 behavior.
- PR39 diagnostics: stdout/stderr log, xtrace, diagnostics, exit status, preflight JSON, generated config, and run manifest.
- PR41 preprocessing proof: generated config and manifest record `preprocessing_num_workers: null` or accepted single-process equivalent, `dataloader_num_workers: 0`, dataset `coding_agent_m1_sft_10_sharegpt`.
- Required NCCL env evidence: `NCCL_DEBUG=INFO`, `NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL`, `NCCL_ASYNC_ERROR_HANDLING=1`, `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`, and `CUDA_DEVICE_MAX_CONNECTIONS=1`.
- No default `NCCL_P2P_DISABLE=1` unless later PM/dev_1/test_1 explicitly accepts degraded diagnostic fallback.
- Dataset path and sha: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- `/home/xu.yang/coding_agent_playground/outputs` for output/log/tmp/checkpoint/run metadata/intermediate paths.

### Final Artifact Acceptance

`PASS_FOR_EVAL_HANDOFF` requires:

- Complete checkpoint/model under `/home/xu.yang/coding_agent_playground/outputs`.
- File listing, sizes, and checksums or equivalent integrity proof.
- `trainer_state.json` present.
- `all_results.json` present.
- Stop/release proof and endpoint refused/unreachable after stop.
- Old blocker absence: no `KeyError: from`, no missing/wrong `dataset_info`, no `datasets.map(num_proc=4)` SyncManager EOF, no ENOSPC/safetensors no-space, no early wrapper exit before diagnostics, and no recurrence of `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.

If any of these are absent, eval handoff remains blocked unless PM/test explicitly accepts replacement artifacts.

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

Current runtime watch status for `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2` is `PASS_FOR_NEXT_PM_DECISION`: dev_2 produced complete preflight/stop evidence and correctly did not run SFT after `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`. Eval handoff remains blocked.

## Completion Marker

```yaml
task_id: M1-S22-NCCL-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
runtime_watch_result: PASS_FOR_NEXT_PM_DECISION
runtime_task: M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2
runtime_frame: xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
runtime_node: lg-cmc-b7r401-a04u26-h200-000769
different_node_gate: PASS
preflight_result: FAIL_HEALTH_SIGNATURE
torch_nccl_allreduce_exit_0: true
capacity_probe_pass: true
sft_run: false
runtime_operational_blocker: BLOCKED_PREFLIGHT_FAILED_NO_SFT_RUN
eval_handoff_status: EVAL_HANDOFF_BLOCKED_NO_SFT_NO_CHECKPOINT
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
checkpoint_model_present: false
trainer_state_required: true
trainer_state_present: false
all_results_required: true
all_results_present: false
stop_proof_required: true
stop_proof_present: true
old_failure_absence_required: true
eval_handoff_allowed_now: false
sft_gpu_eval_executed_by_test1: false
```
