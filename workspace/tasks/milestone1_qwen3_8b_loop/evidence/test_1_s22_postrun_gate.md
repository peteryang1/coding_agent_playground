# Test 1 Session 22 Post-Run Gate

Date: 2026-05-21

Task ID: `M1-S22-POSTRUN-GATE-TEST1`

Owner: `intern_code_test_1`

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_postrun_gate.md`

Scope: apply the post-run gate to the Session 22 ENOSPC-fixed SFT retry and define the next no-execution pre-run acceptance criteria.

Execution boundary:

```text
No SFT command was run by test_1.
No GPU command was run by test_1.
No eval command was run by test_1.
No peer_send PM routine status was used.
```

## Sources Reviewed

- `evidence/dev_2_s22_enospc_retry_runtime.md`
- `evidence/gpu_s22_enospc_retry_tracking.md`
- `evidence/pm_s22_enospc_retry_authorization.md`
- `evidence/test_1_s21_enospc_retry_gate.md`
- `task_registry.md`
- `assignments.md`

## Post-Run Result

Result: **BLOCKED_FINAL_RUNTIME**

Mini-swe status: **BLOCKED**

Reason: the single PM-authorized Session 22 SFT attempt exited with `EXIT_STATUS=1` before producing required runtime artifacts. No complete checkpoint/model or served endpoint exists.

## Runtime Facts Accepted From dev_2 Evidence

```text
task_id: M1-S22-ENOSPC-RETRY-RUNTIME-DEV2
frame: xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
endpoint: ssh -p 31346 root@10.100.16.69
run_id: milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
output_root: /home/xu.yang/coding_agent_playground/outputs
log_path: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/logs/train_stdout_stderr.log
exit_status_path: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/exit_status.txt
exit_status: EXIT_STATUS=1
attempts_authorized: 1
attempts_started: 1
attempts_completed: 1
additional_retries_run: 0
eval_run: false
```

Pre-run resource proof accepted from dev_2 evidence:

- `/home/xu.yang` resolved to `/mnt/cephfs/home/xu.yang`.
- `findmnt -T /home/xu.yang` showed CephFS via `fuse.ceph-fuse`.
- Output root was `/home/xu.yang/coding_agent_playground/outputs`.
- Capacity probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>` wrote four real 6.0G files, total `25769803776` bytes, then cleaned them up.
- Capacity probe result was `PROBE_STATUS=PASS_RECOVERED_AND_CLEANED`.

Data/config facts accepted from dev_2 evidence:

- Dataset entry: `coding_agent_m1_sft_10_sharegpt`.
- Source dataset: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Dataset rows: `10`.
- Base model: `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.
- Planned output dir: `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>`.
- Planned S22 config asserted `dataset: coding_agent_m1_sft_10_sharegpt`, `save_steps: 2`, `save_total_limit: 1`, `warmup_steps: 0`, `max_steps: 2`, TP=8, PP=1, CP=1, and `sequence_parallel: false`.

## Artifact Gate

Required post-run artifacts were absent:

```text
run_manifest.json: absent
generated runtime config under run dir: absent
checkpoint files: absent
complete checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
served endpoint: absent
```

Only these minimal preserved files were reported after stop:

```text
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/exit_status.txt
```

The durable run log contained only:

```text
START_UTC=2026-05-21T08:27:52Z
```

Interpretation: this run failed before durable stdout/stderr captured the failure boundary and before the training wrapper emitted manifest/config/checkpoint artifacts. Therefore the run does not validate the ENOSPC checkpoint fix, ShareGPT conversion, training step progress, or checkpoint save behavior.

## Old Failure Signature Checks

From the produced durable log and dev_2 evidence:

```text
KeyError: 'from': not observed
missing dataset_info: not observed
ZeroDivisionError / steps_in_epoch: not observed
scheduler warmup assertion: not observed
No space left on device: not observed
safetensors ENOSPC: not observed
ShareGPT conversion progress: not observed
training step progress: not observed
```

Gate interpretation:

- Old signatures were absent in the produced log.
- This absence is not a full runtime PASS because the log contains only `START_UTC`; the script exited before useful runtime output was captured.
- ENOSPC did not recur in evidence, but the run did not reach checkpoint creation, so the ENOSPC fix remains unproven.

## Stop Proof

Stop proof is accepted.

```text
stop_command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
stop_issued_utc: 2026-05-21T08:29:55Z
stop_status: 202 STOP signal sent
post_stop_first_observed_utc: 2026-05-21T08:30:36Z
final_state: STOPPED (Completed)
completed_timestamp: 2026-05-21 08:30:26
endpoint_after_stop: ssh -p 31346 root@10.100.16.69 refused connection
endpoint_refused_confirmed_again: 2026-05-21T08:30:57Z, 2026-05-21T08:31:17Z, 2026-05-21T08:31:37Z
artifact_preservation: /home/xu.yang/coding_agent_playground/outputs preserved on CephFS and visible via /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs
cleanup: no cleanup of runtime log/exit artifacts
eval_run: false
```

## Required Next Pre-Run Acceptance Criteria

No further retry is authorized by this post-run gate. Before PM can authorize any future SFT retry, durable no-execution evidence must satisfy all criteria below.

Current next pre-run gate status after dev_4 package refresh: **BLOCKED_WAITING_DEV1_REFRESH**

Reviewed refresh inputs:

```text
dev_4_fix_package: evidence/dev_4_s22_early_exit_fix.md
dev_4_fix_status: PRESENT_COMPLETE_FOR_PLAN
dev_1_review: evidence/dev_1_s22_runtime_blocker_review.md
dev_1_review_status: STALE_BLOCKED_MISSING_DEV4_FIX
```

test_1 interpretation:

- `evidence/dev_4_s22_early_exit_fix.md` now exists and satisfies the package-presence portion of the next pre-run gate: it diagnoses the early exit as before useful durable capture, distinguishes it from `KeyError: 'from'` and ENOSPC, preserves `/home/xu.yang/coding_agent_playground/outputs`, preserves `coding_agent_m1_sft_10_sharegpt`, and proposes durable stdout/stderr/xtrace/ERR-trap/preflight manifest fixes.
- The dev_4 package is no-execution planning evidence. A future retry still needs the proposed wrapper/logging fix landed in code or explicitly staged on the worker before launch.
- `evidence/dev_1_s22_runtime_blocker_review.md` is not refreshed against the current dev_4 package. It still reports `review_status: BLOCKED_MISSING_DEV4_FIX` and says `evidence/dev_4_s22_early_exit_fix.md` is missing.
- Therefore test_1 cannot mark the next pre-run gate `PASS_FOR_PM_RETRY` yet.

Exact current blockers:

1. `BLOCKED_WAITING_DEV1_REFRESH`: dev_1 must re-read current `evidence/dev_4_s22_early_exit_fix.md`, dev_2 Session 22 runtime/stop proof, and this test_1 post-run gate, then output `PASS_FOR_PM_RETRY` or exact remaining blockers.
2. Before any actual retry launch, the early-exit logging fix must be landed or staged so `scripts/train_qwen3_8b_sft.sh` owns durable logging/xtrace/ERR-trap diagnostics from the first safe point and writes config/manifest/preflight evidence before training starts.
3. PM must explicitly authorize any future LTP/GPU/SFT attempt. This test gate does not authorize execution.

### Early-Exit / Pre-Redirection Logging Fix

Required owner package:

```text
evidence/dev_4_s22_early_exit_fix.md
task_id: M1-S22-EARLY-EXIT-FIX-DEV4
```

Acceptance criteria:

- Diagnose why `scripts/train_qwen3_8b_sft.sh` returned `EXIT_STATUS=1` before durable stdout/stderr, `run_manifest.json`, generated runtime config, or checkpoint files.
- Provide an exact wrapper/script/config patch or command change that captures failures before the training script redirects into the durable run log.
- Future logs must include shell tracing or equivalent pre-redirection capture for:
  - environment setup;
  - config template discovery;
  - run directory creation;
  - generated runtime config copy;
  - dataset_info path setup;
  - dependency import/setup boundary;
  - exact command handoff into LLamaFactory/Megatron.
- The fix must write an early preflight log under `/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/` before invoking the training script.
- The fix must preserve `RUN_ID`, `OUTPUT_ROOT`, `CHECKPOINT_DIR`, generated config path, and exit status even if the training script fails before its own redirection.

### Storage And Runtime Preconditions

Required:

- SFT launch outputs, stdout/stderr logs, checkpoints/model artifacts, generated configs, run metadata, temporary converted datasets/staging copies, capacity probes, and stop proof remain under `/home/xu.yang/coding_agent_playground/outputs` unless an explicit existing-required-path exception is recorded.
- Non-`/home/xu.yang` paths remain limited to recorded existing-required input/audit/compatibility exceptions, such as the base model, dependency archives/wheels, historical failed-run evidence, existing source dataset, and small metadata mirrors.
- Fresh `/home/xu.yang` mount/path proof on the allocated node.
- Fresh real-write capacity probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>`.
- Fresh unique `RUN_ID`; do not reuse Session 21 or Session 22 failed output/checkpoint directories.
- PM must explicitly authorize any future LTP/GPU/SFT attempt.
- No eval remains authorized until a complete checkpoint/model or served endpoint exists.

### Data / Config Preconditions

Required:

- Preserve dataset entry `coding_agent_m1_sft_10_sharegpt`.
- Preserve source dataset checksum `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2` and row count `10`, unless a new PM-approved data task changes it.
- Preserve ShareGPT `messages[*].from/value` dataset_info mapping.
- Generated runtime config must be durably captured before training starts.
- Generated runtime config must show:
  - `dataset: coding_agent_m1_sft_10_sharegpt`;
  - base model `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`;
  - `output_dir` under `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>`;
  - `save_steps: 2`;
  - `save_total_limit: 1`;
  - `max_steps: 2`;
  - `warmup_steps: 0`;
  - TP=8, PP=1, CP=1.

### Post-Run PASS Criteria For Any Future Retry

Future post-run PASS requires:

- exit status `0`, or a PM-preapproved accepted replacement outcome;
- durable stdout/stderr includes the failure/success boundary, not only `START_UTC`;
- old failure signatures absent:
  - `KeyError: 'from'`;
  - missing `dataset_info`;
  - `ZeroDivisionError` / `steps_in_epoch`;
  - scheduler warmup assertion;
  - `No space left on device`;
  - safetensors ENOSPC;
- ShareGPT conversion and training progress observed, or a clear preapproved alternative endpoint proof;
- complete checkpoint/model produced and accepted, not a partial checkpoint;
- `trainer_state.json` present, unless PM pre-approves a replacement;
- `all_results.json` present, unless PM pre-approves a replacement;
- generated runtime config, run manifest, exit status, logs, checkpoint/model files, and stop proof are all durably present;
- LTP stopped/released and endpoint refused/unavailable after stop.

## Completion Marker

```text
task_id: M1-S22-POSTRUN-GATE-TEST1
post_run_status: BLOCKED_FINAL_RUNTIME
next_pre_run_gate_status: BLOCKED_WAITING_DEV1_REFRESH
checkpoint_model_status: ABSENT
trainer_state_json: ABSENT
all_results_json: ABSENT
old_failure_signatures_observed: false
runtime_log_useful_failure_boundary: false
stop_proof: PASS
mini_swe_can_proceed: false
next_pre_run_requires_home_xu_yang: true
next_pre_run_requires_pre_redirection_logging_fix: true
dev_4_early_exit_fix_package: PRESENT_COMPLETE_FOR_PLAN
dev_1_runtime_blocker_review: STALE_BLOCKED_MISSING_DEV4_FIX
sft_gpu_eval_executed_by_test1: false
```
