# Dev 1 Session 22 Runtime Blocker Review

Owner: `intern_code_dev_1`  
Task ID: `M1-S22-RUNTIME-BLOCKER-REVIEW-DEV1`  
Date: 2026-05-21  
Scope: independent no-execution review of the Session 22 final runtime blocker and dev_4 early-exit fix package when present. No remote experiments, SFT, GPU, or eval were run.

## Sources Reviewed

Commands/files checked from the PM worktree:

```text
sed -n '1,360p' evidence/dev_2_s22_enospc_retry_runtime.md
sed -n '1,260p' evidence/gpu_s22_enospc_retry_tracking.md
test -f evidence/dev_4_s22_early_exit_fix.md
sed -n '1,220p' evidence/pm_s22_enospc_retry_authorization.md
grep -n "M1-S22" task_registry.md
```

## Current Result

```text
review_status: BLOCKED_MISSING_DEV4_FIX
pass_for_pm_retry: false
```

The required dev_4 early-exit fix package is missing:

```text
missing: evidence/dev_4_s22_early_exit_fix.md
```

Therefore this review cannot output `PASS_FOR_PM_RETRY` yet.

## Session 22 Runtime Facts From dev_2

Reviewed evidence:

```text
evidence/dev_2_s22_enospc_retry_runtime.md
evidence/gpu_s22_enospc_retry_tracking.md
```

Authorization:

- PM authorized exactly one fresh LTP job and one SFT attempt.
- Eval was not authorized.
- Required output root was `/home/xu.yang/coding_agent_playground/outputs`.
- Dataset entry was `coding_agent_m1_sft_10_sharegpt`.
- Save strategy was `save_steps=2`, `save_total_limit=1`, `max_steps=2`.

Resource and storage proof:

- LTP frame: `xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z`.
- Endpoint while running: `ssh -p 31346 root@10.100.16.69`.
- `/home/xu.yang` was linked to `/mnt/cephfs/home/xu.yang`.
- `findmnt -T /home/xu.yang` showed CephFS.
- Output root `/home/xu.yang/coding_agent_playground/outputs` was writable.
- 24GiB real-write probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>` passed and was cleaned up.

SFT command facts:

- Dataset sha256 matched `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Dataset rows: `10`.
- Dataset info entry was staged as `coding_agent_m1_sft_10_sharegpt`.
- Generated config template assertions included:
  - `dataset: coding_agent_m1_sft_10_sharegpt`
  - output under `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>`
  - `save_steps: 2`
  - `save_total_limit: 1`
  - `warmup_steps: 0`
  - `max_steps: 2`
  - TP=8, PP=1, CP=1, sequence parallel false

Runtime result:

```text
run_id: milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
exit_status: EXIT_STATUS=1
log: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
log_content: START_UTC=2026-05-21T08:27:52Z
run_manifest.json: absent
generated runtime config under run dir: absent
checkpoint files: absent
trainer_state.json: absent
all_results.json: absent
complete checkpoint/model: absent
```

Stop proof:

- dev_2 stopped frame `xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z`.
- Post-stop state: `STOPPED (Completed)`.
- Endpoint refused connection after stop.
- `/home/xu.yang/coding_agent_playground/outputs` remained preserved on CephFS.
- Eval was not run.

## Blocker Classification

This is a new early-exit / pre-redirection runtime blocker.

It is distinct from the prior `KeyError: from` blocker:

- The S22 log does not show `KeyError: 'from'`.
- The S22 runtime did not reach dataset conversion logging.
- Dataset_info and ShareGPT staging were prepared before launch.
- The failure happened before durable runtime manifest/config/log artifacts were produced.

It is distinct from the prior ENOSPC blocker:

- The S22 log does not show `No space left on device`.
- The S22 log does not show safetensors serialization.
- No checkpoint save began.
- `/home/xu.yang` CephFS proof and 24GiB real-write capacity probe passed before SFT launch.
- The failure happened before checkpoint/model output existed.

Current interpretation:

```text
The wrapper launched exactly once but returned exit status 1 before stderr/stdout beyond START_UTC, before run_manifest.json, before generated runtime config copy, and before checkpoint artifacts. The next package must expose and fix the failure boundary in scripts/train_qwen3_8b_sft.sh or its invocation/log redirection path.
```

## Required dev_4 Fix Package

Missing required input:

```text
evidence/dev_4_s22_early_exit_fix.md
```

Expected content before this review can pass:

- diagnose why `scripts/train_qwen3_8b_sft.sh` returned `EXIT_STATUS=1` before durable stdout/stderr, `run_manifest.json`, generated runtime config, or checkpoint files;
- propose exact wrapper/script/config patch or command change;
- preserve `/home/xu.yang/coding_agent_playground/outputs` as the output root;
- preserve ShareGPT dataset contract `coding_agent_m1_sft_10_sharegpt`;
- preserve the accepted source dataset sha256;
- capture pre-redirection/pre-manifest failures in durable logs;
- state whether a PR/code change is required and cite task id `M1-S22-EARLY-EXIT-FIX-DEV4`;
- state that no SFT/GPU/eval was run by the fix package.

## Exact Blockers

1. `evidence/dev_4_s22_early_exit_fix.md` is missing.
2. No accepted diagnosis exists yet for the early script exit before durable manifest/config/log artifacts.
3. No wrapper/script/config patch or command-level logging fix has been reviewed.
4. No future retry should be authorized until dev_4 fix evidence exists and dev_1/test_1 review/gate the new early-exit fix.

## Recommendation

```text
Do not authorize another SFT retry yet. Session 22 cleared the prior storage/ENOSPC preflight and did not show KeyError/from or safetensors ENOSPC, but it failed earlier: scripts/train_qwen3_8b_sft.sh returned EXIT_STATUS=1 after only START_UTC was written. Require dev_4_s22_early_exit_fix.md before any retry gate.
```

## Completion Marker

Complete-with-missing-input-blocker: dev_2 Session 22 runtime/stop evidence reviewed; blocker is classified as early-exit/pre-redirection and is distinct from prior `KeyError: from` and ENOSPC failures. `evidence/dev_4_s22_early_exit_fix.md` is missing, so no `PASS_FOR_PM_RETRY` is issued. No remote experiments, SFT, GPU, or eval were run.
