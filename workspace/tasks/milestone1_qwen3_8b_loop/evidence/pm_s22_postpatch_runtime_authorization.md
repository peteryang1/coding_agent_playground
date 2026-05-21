# PM S22 Post-Patch Runtime Authorization

<!-- METADATA:OWNER=intern_code_pm,SESSION=22,STATUS=Authorized-One-Owner-Run -->

## Decision

- Time: `2026-05-21T09:18:03Z`
- Task: `M1-S22-POSTPATCH-SFT-RUNTIME-DEV2`
- Authorized owner: `intern_code_dev_2`
- Authorization scope: exactly one post-PR #39 ShareGPT-fixed Qwen3-8B SFT smoke attempt.
- PM boundary: PM does not submit LTP, run SFT, run GPU commands, run eval, or execute remote experiment code.

## Gate Basis

- PR #39 is merged: `https://github.com/peteryang1/coding_agent_playground/pull/39`
- PR #39 merge commit: `4a6c2968e1290d30415460b464eee638110958bc`
- PR #39 merged at: `2026-05-21T09:17:15Z`
- dev_1 no-execution patch review: `evidence/dev_1_s22_early_exit_patch_review.md` records `PASS_FOR_PM_RETRY`.
- test_1 no-execution patch gate: `evidence/test_1_s22_early_exit_patch_gate.md` records `PASS_FOR_PM_PATCH_GATE`.
- dev_2 readiness: `evidence/dev_2_s22_postpatch_ltp_ready.md` records LTP/resource readiness and `/home/xu.yang` capacity-probe/output layout expectations.
- dev_3 readiness: `evidence/dev_3_s22_postpatch_data_staging.md` records accepted ShareGPT source artifact and future staging paths under `/home/xu.yang`.
- test_2 readiness: `evidence/test_2_s22_postpatch_eval_ready.md` records eval readiness blocked on checkpoint/model and `/home/xu.yang` eval intermediate paths.

## Required Runtime Contract

- Use CephFS `/home/xu.yang` for SFT outputs, temporary converted datasets, logs, checkpoints, run metadata, capacity probes, and intermediates.
- Required output root: `/home/xu.yang/coding_agent_playground/outputs`.
- Existing required input exceptions are allowed only when recorded in dev_2 evidence, including base model and accepted source artifact paths.
- Dataset name must be `coding_agent_m1_sft_10_sharegpt`.
- Accepted source data artifact: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Runtime must use the merged PR #39 wrapper/manifest behavior so first durable stdout/stderr, xtrace, ERR/EXIT diagnostics, preflight JSON, runtime config, and run manifest are captured before fragile launch work.

## Required Evidence From dev_2

`intern_code_dev_2` must write:

- LTP job/frame id, node id, endpoint, and `nodes.json`.
- Exact submit/status/ssh/stop commands used.
- Exact runtime command, env, config path, dataset_info entry, base model path, run id, output root, run dir, checkpoint dir, log file, xtrace file, diagnostic file, and manifest path.
- Capacity/probe result for `/home/xu.yang` or exact blocker.
- Exit status and log summaries.
- Checkpoint/model presence or precise failure point.
- `trainer_state.json` and `all_results.json` presence or absence.
- Stop proof, post-stop status, endpoint reachability proof, and artifact preservation path.

## Required Next Outcome

The next durable outcome must be one of:

- Complete checkpoint/model with enough evidence for test_1 and test_2 gates, or
- Fresh exact runtime blocker with owner, command, logs, node status, stop proof, and next fix.

Mini-swe eval remains unauthorized until PM gates a complete checkpoint/model or served endpoint.
