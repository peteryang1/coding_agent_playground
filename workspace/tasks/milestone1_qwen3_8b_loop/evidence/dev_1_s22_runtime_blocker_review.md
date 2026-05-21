# Dev 1 Session 22 Runtime Blocker Review

Owner: `intern_code_dev_1`  
Task ID: `M1-S22-RUNTIME-BLOCKER-REVIEW-DEV1`  
Date: 2026-05-21  
Scope: refreshed independent no-execution review of the Session 22 final runtime blocker, dev_4 early-exit fix package, and test_1 postrun gate. No remote experiments, SFT, GPU, or eval were run.

## Sources Reviewed

Commands/files checked from the PM worktree:

```text
sed -n '1,360p' evidence/dev_2_s22_enospc_retry_runtime.md
sed -n '1,260p' evidence/gpu_s22_enospc_retry_tracking.md
sed -n '1,320p' evidence/dev_4_s22_early_exit_fix.md
sed -n '1,360p' evidence/test_1_s22_postrun_gate.md
grep -n "M1-S22-EARLY-EXIT-FIX-DEV4\\|M1-S22-RUNTIME-BLOCKER-REVIEW-DEV1\\|M1-S22-POSTRUN-GATE-TEST1" task_registry.md
```

## Current Result

```text
review_status: BLOCKED_PENDING_EARLY_EXIT_PATCH_GATE
pass_for_pm_retry: false
```

The missing-input blocker is resolved because `evidence/dev_4_s22_early_exit_fix.md` now exists. However, I do not issue `PASS_FOR_PM_RETRY` yet because the current dev_4 package is a no-execution diagnosis/fix plan, while the task registry says PM requested the package be turned into a no-execution patch PR and that no retry is authorized. test_1 also requires the early-exit/pre-redirection logging fix before a future retry.

## Session 22 Runtime Facts From dev_2

Reviewed evidence:

```text
evidence/dev_2_s22_enospc_retry_runtime.md
evidence/gpu_s22_enospc_retry_tracking.md
```

Accepted facts:

- PM authorized exactly one fresh LTP job and one SFT attempt.
- Eval was not authorized.
- Required output root was `/home/xu.yang/coding_agent_playground/outputs`.
- `/home/xu.yang` resolved to CephFS via `/mnt/cephfs/home/xu.yang`.
- 24GiB real-write capacity probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>` passed and was cleaned up.
- Dataset entry was `coding_agent_m1_sft_10_sharegpt`.
- Dataset sha256 matched `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- S22 config template asserted `dataset: coding_agent_m1_sft_10_sharegpt`, `save_steps: 2`, `save_total_limit: 1`, `max_steps: 2`, `warmup_steps: 0`, TP=8, PP=1, CP=1.
- dev_2 stopped/released the LTP frame; final state `STOPPED (Completed)`.

Runtime failure:

```text
run_id: milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
exit_status: EXIT_STATUS=1
log_content: START_UTC=2026-05-21T08:27:52Z
run_manifest.json: absent
generated runtime config under run dir: absent
checkpoint files: absent
trainer_state.json: absent
all_results.json: absent
complete checkpoint/model: absent
```

## Blocker Classification

This remains a new early-exit / pre-redirection runtime blocker.

Distinct from prior `KeyError: from`:

- S22 log does not show `KeyError: 'from'`.
- The run did not reach dataset conversion logging.
- Dataset_info and ShareGPT staging were prepared before launch.

Distinct from prior ENOSPC:

- S22 log does not show `No space left on device`.
- S22 log does not show safetensors serialization.
- No checkpoint save began.
- `/home/xu.yang` CephFS proof and 24GiB real-write capacity probe passed before SFT launch.

Interpretation:

```text
The SFT wrapper was launched exactly once but returned exit status 1 before useful durable stdout/stderr, run_manifest.json, generated runtime config copy, or checkpoint artifacts. The failure boundary is before LLamaFactory data conversion, training, or checkpoint save.
```

## dev_4 Early-Exit Fix Review

Reviewed path:

```text
evidence/dev_4_s22_early_exit_fix.md
```

Status: **PLAN PRESENT / IMPLEMENTATION GATE STILL BLOCKING**

Positive findings:

- dev_4 diagnoses failure as before or inside the early wrapper/script prelude, before durable artifact writes.
- dev_4 distinguishes it from `KeyError: from`, ENOSPC, DP=8 zero-step, and scheduler assertion.
- dev_4 preserves:
  - `OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs`
  - `DATASET_NAME=coding_agent_m1_sft_10_sharegpt`
  - `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`
  - base model `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`
- dev_4 proposes concrete wrapper changes:
  - durable logging from the first executable point;
  - `tee` stdout/stderr capture inside `scripts/train_qwen3_8b_sft.sh`;
  - `train_xtrace.log`;
  - ERR/EXIT traps;
  - `early_exit_diagnostics.txt`;
  - config/template/dataset/path preflight assertions;
  - `DATASET_NAME` rewrite into generated config;
  - manifest hardening to record actual save policy and paths.

Blocking findings:

- The dev_4 package is explicitly no-execution and does not say the patch is landed.
- Registry says `M1-S22-EARLY-EXIT-FIX-DEV4` is "Fix package complete / PR requested" and "no retry authorized".
- The proposed touched files include `scripts/train_qwen3_8b_sft.sh`, `scripts/write_sft_run_manifest.py`, and config files, but this review did not find durable evidence that those changes are merged or staged on the worker for the next retry.
- test_1 postrun gate requires the early-exit/pre-redirection logging fix before any future retry.

## test_1 Postrun Gate Review

Reviewed path:

```text
evidence/test_1_s22_postrun_gate.md
```

Status: **BLOCKED_FINAL_RUNTIME / FUTURE PRE-RUN FIX REQUIRED**

Accepted gate facts:

- Post-run result is `BLOCKED_FINAL_RUNTIME`.
- Mini-swe remains blocked.
- Stop proof is accepted.
- Old signatures were not observed in the minimal log, but that is not a runtime pass because the log contains only `START_UTC`.
- No checkpoint/model or served endpoint exists.

Future retry requirements from test_1:

- durable early-exit / pre-redirection logging fix;
- generated runtime config durably captured before training starts;
- run manifest exists before training starts;
- `/home/xu.yang` output paths preserved;
- dataset entry `coding_agent_m1_sft_10_sharegpt` preserved;
- PM explicitly authorizes any future LTP/GPU/SFT attempt.

## Exact Blockers

1. **Early-exit fix is not yet proven landed/staged**
   - `dev_4_s22_early_exit_fix.md` exists, but it is a no-execution fix package.
   - Registry says PM requested a no-execution patch PR and no retry is authorized.
   - Need durable evidence that the wrapper/logging patch is merged or staged on the future worker before retry.

2. **No reviewed PR/patch completion record for touched files**
   - Expected files include `scripts/train_qwen3_8b_sft.sh`, `scripts/write_sft_run_manifest.py`, and a Session 22 config.
   - Need PR/evidence proving the changes implement first-line durable logging, xtrace, ERR/EXIT diagnostics, manifest/config preflight, and `DATASET_NAME` rewrite.

3. **test_1 gate still requires the fix before retry**
   - Current postrun gate is `BLOCKED_FINAL_RUNTIME`.
   - It defines next pre-run requirements, including the early-exit logging fix.

## Recommendation

```text
Do not authorize another SFT retry yet. The dev_4 early-exit fix package now exists and is directionally correct, but the durable evidence does not show that the wrapper/logging patch is landed or staged. Require the no-execution patch PR/completion evidence for scripts/train_qwen3_8b_sft.sh and related manifest/config changes, then re-run dev_1/test_1 gates before PM authorizes runtime.
```

## Completion Marker

Complete-with-patch-gate-blocker: dev_2 S22 runtime/stop proof, dev_4 early-exit fix package, and test_1 postrun gate were reviewed. The blocker is early-exit/pre-redirection and remains distinct from prior `KeyError: from` and ENOSPC failures. No `PASS_FOR_PM_RETRY` is issued until the early-exit wrapper/logging fix is landed or staged and gated. No remote experiments, SFT, GPU, or eval were run.
