# intern_code_dev_4 - 状态

<!-- METADATA:STATUS=Working,TASK=milestone1_qwen3_8b_loop -->

| 字段 | 值 |
|------|-----|
| Name | intern_code_dev_4 |
| Status | Working |
| Current Task | milestone1_qwen3_8b_loop |
| PR | https://github.com/peteryang1/coding_agent_playground/pull/18 |
| Session | 15 |

## PM Corrections

- 2026-05-20: Acknowledged PM correction: do not use `peer_send` for routine confirmations, status, blockers, or test information to PM. Future dev evidence/status will be recorded in PM-named durable files, task docs, PR comments, or evidence paths. Do not use `/esc` to PM for routine status.

## Active Assignment

- 2026-05-20: Accepted Milestone 1 assignment for Qwen3-8B SFT pipeline, GPU workflow, training command templates, checkpoint layout, and run manifest. Routine updates will be written to `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_pipeline.md`.
- 2026-05-20: Implemented initial SFT pipeline artifacts on branch `intern_code_dev_4/milestone1_qwen3_8b_loop`: Qwen3-8B LLamaFactory/MCA config, training launch wrapper, run manifest writer, and checkpoint/GPU workflow doc. Current blockers: GPU node or milestone `nodes.json` not confirmed; final SFT dataset pending dev_3 output.
- 2026-05-20: Applied PM critical address correction. Correct final workspace is `ssh -p 31787 root@10.100.194.40`; old `20087/root@10.100.193.54` probes are scratch-only. Re-probed new machine and recorded findings in PM evidence. Current blockers remain: corrected entry host has no `nvidia-smi`, milestone GPU `nodes.json` is not confirmed, and `/root/workspace/coding_agent_playground` is missing on the corrected machine.
- 2026-05-20: Completed PM Session 3 SFT planning update in durable evidence. Validated axrd registry facts for `Qwen/Qwen3-8B`, LLamaFactory/MCA deps and archive hash, historical Qwen3-8B checkpoint shapes, GPU-machine options, launcher templates, and output manifest/checkpoint layout. New critical blocker: `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is a broken symlink on corrected machine, so clean base model path must be materialized or explicitly replaced before real SFT.
- 2026-05-20: Self-merged PR #1 after scoped local checks passed. Merge commit `882d1642884e82d1a40674266f244a52cf69defc`, mergedAt `2026-05-20T08:23:54Z`. Wrote Session 8 SFT unblock decision package to durable evidence: clean base cannot currently be located/repaired from verified local artifacts; warm-start fallback recommended only if PM/supervisor approves `/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-final`; GPU/current nodes.json remains required.
- 2026-05-20 Session 9: Applied PM gate decision to use dev_1 clean-base candidate `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` for the next SFT smoke. Verified the candidate has config/tokenizer/generation config, 5 safetensors shards, and no missing index shards. Prepared no-launch SFT smoke command package in `evidence/dev_4_sft_pipeline.md`; real launch remains blocked only on GPU endpoint or current Milestone 1 `nodes.json`. Opened PR #11 for Session 9 durable updates.
- 2026-05-20 Session 10: Resolved PR #11 conflict by merging current `origin/main` into `intern_code_dev_4/session9-sft-smoke-launch-package`. Conflict file was `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md`; resolution preserved dev_4 Session 9 records and PM/test_1/test_2 post-PR10 gate records. Pushed refreshed PR #11 and GitHub recheck reports `mergeable=MERGEABLE`. No SFT launch attempted; GPU/current `nodes.json` remains blocker.
- 2026-05-20 Session 11: Self-merged PR #11 after PM gate pass and local `git diff --check`. PR #11 merged at `2026-05-20T09:10:26Z` with merge commit `93c4efaaff3e50220f7bb8583070321e65289efa`. Opened PR #14 to land this merge evidence. No SFT launch attempted; next real launch still requires GPU endpoint/current Milestone 1 `nodes.json`.
- 2026-05-20 Session 12: PM approved current GPU route `ssh -p 39314 root@10.100.20.37`, but ordered PR #14 conflict resolution first because PR #15 landed. Merged current `origin/main` into PR #14 branch, preserved PR #15 dev_2 GPU route/PM records, and resolved the only conflict in `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`. SFT launch is queued until PR #14 becomes mergeable and is self-merged.
- 2026-05-20 Session 13: Ran the approved short Qwen3-8B clean-base SFT smoke on `ssh -p 39314 root@10.100.20.37` after PR #14 self-merge. GPU/base/data/deps prechecks passed, but no checkpoint was produced: baseline run failed on MCA tiny-data DP=8 `steps_in_epoch=0`, and one bounded TP=8 retry failed Megatron scheduler assertion for 1-step smoke. Evidence is in `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_smoke_run.md`; dev_2 should stop the H200 allocation immediately. Opened PR #18 for this evidence.
- 2026-05-20 Session 15: Applied PM correction for PR #18 task mapping. Merged current `origin/main`, preserved PM Session 12 `task_registry.md`/task gate records, resolved conflicts in `history_log.md` and `task_knowledge.md`, and updated PR/evidence/task docs to use task id `M1-SFT-SMOKE-DEV4`. PR #18 remains open pending GitHub `MERGEABLE` status and PM gate pass before self-merge.
