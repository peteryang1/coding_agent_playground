# PM Authorization - M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2

Task ID: `M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2`
Authorized owner: `intern_code_dev_2`
Authorization timestamp: `2026-05-21T15:50:00Z`

## Gate Basis

- PR #57 merged at `2026-05-21T15:45:10Z`, merge commit `c450429c2e3369adc723d132396399cd17dba684`.
- Completion PR #58 merged at `2026-05-21T15:48:30Z`, merge commit `b4ac31ef1e3772953108348bf099818326ed65cc`.
- Dev_1 recorded `PASS_FOR_PM_RETRY` for PR #57 wrapper/env fix.
- Test_1 recorded `PASS_FOR_PM_RETRY` for PR #57 wrapper/env fix.
- Dev_2 recorded PR55 resource recovery/no active job.
- Dev_3 confirmed no data/package change is needed.
- Test_2 recorded eval remains blocked until a checkpoint/model or served endpoint exists.

## Authorized Scope

`intern_code_dev_2` may run exactly one fresh owner-executed GPU/LTP runtime using `origin/main` commit `b4ac31ef1e3772953108348bf099818326ed65cc`.

The run may include:

- one fresh LTP allocation;
- local/provided-workspace source/config/script/data packaging;
- bundle transfer to the allocated node;
- `/home/xu.yang/coding_agent_playground/outputs` storage proof;
- structured preflight;
- exactly one SFT smoke only if structured preflight reports `PREFLIGHT_RESULT=PASS` and `SFT_ALLOWED=true`.

Eval is not authorized.

## Mandatory Runtime Rules

- Treat the remote GPU/LTP node as having no external network for project code/dependency staging.
- Do not `git clone`, `git fetch`, or download project code/dependencies from GitHub on the remote node.
- Prepare code/config/scripts/data in the provided/local workspace first.
- Verify exact source commit, file list, and checksums locally before transfer.
- Transfer the prepared bundle to the remote node by `rsync`, `scp`, or tar-over-SSH.
- Record exact transfer command, source commit, bundle checksum, file list, destination path, and post-transfer verification.
- Store generated SFT launch outputs, temporary converted datasets, logs, checkpoints, run metadata, and eval-ready intermediates under `/home/xu.yang/coding_agent_playground/outputs` unless a required input path is explicitly justified.
- Record LTP frame/job id, node id, endpoint, start/stop timestamps, stop command/action, final status, endpoint-after-stop proof, and no-running-job proof.

## Required Result Evidence

Dev_2 must write:

- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_pr57_preflight_sft_runtime.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_pr57_preflight_sft_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`

The evidence must end with either:

- checkpoint/model produced, with `trainer_state.json` and `all_results.json` presence/absence and stop proof; or
- exact blocker with command, logs, exit status, node status, output paths, owner, next fix, and stop proof.

PM did not run LTP, remote commands, transfer commands, preflight, SFT, eval, or code changes for this authorization.
