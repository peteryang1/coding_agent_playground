# intern_code_dev_4 - 状态

<!-- METADATA:STATUS=Working,TASK=milestone1_qwen3_8b_loop -->

| 字段 | 值 |
|------|-----|
| Name | intern_code_dev_4 |
| Status | Working |
| Current Task | milestone1_qwen3_8b_loop |
| PR | https://github.com/peteryang1/coding_agent_playground/pull/1 (MERGED 2026-05-20T08:23:54Z, 882d1642884e82d1a40674266f244a52cf69defc) |
| Session | 0 |

## PM Corrections

- 2026-05-20: Acknowledged PM correction: do not use `peer_send` for routine confirmations, status, blockers, or test information to PM. Future dev evidence/status will be recorded in PM-named durable files, task docs, PR comments, or evidence paths. Do not use `/esc` to PM for routine status.

## Active Assignment

- 2026-05-20: Accepted Milestone 1 assignment for Qwen3-8B SFT pipeline, GPU workflow, training command templates, checkpoint layout, and run manifest. Routine updates will be written to `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_pipeline.md`.
- 2026-05-20: Implemented initial SFT pipeline artifacts on branch `intern_code_dev_4/milestone1_qwen3_8b_loop`: Qwen3-8B LLamaFactory/MCA config, training launch wrapper, run manifest writer, and checkpoint/GPU workflow doc. Current blockers: GPU node or milestone `nodes.json` not confirmed; final SFT dataset pending dev_3 output.
- 2026-05-20: Applied PM critical address correction. Correct final workspace is `ssh -p 31787 root@10.100.194.40`; old `20087/root@10.100.193.54` probes are scratch-only. Re-probed new machine and recorded findings in PM evidence. Current blockers remain: corrected entry host has no `nvidia-smi`, milestone GPU `nodes.json` is not confirmed, and `/root/workspace/coding_agent_playground` is missing on the corrected machine.
- 2026-05-20: Completed PM Session 3 SFT planning update in durable evidence. Validated axrd registry facts for `Qwen/Qwen3-8B`, LLamaFactory/MCA deps and archive hash, historical Qwen3-8B checkpoint shapes, GPU-machine options, launcher templates, and output manifest/checkpoint layout. New critical blocker: `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is a broken symlink on corrected machine, so clean base model path must be materialized or explicitly replaced before real SFT.
- 2026-05-20: Self-merged PR #1 after scoped local checks passed. Merge commit `882d1642884e82d1a40674266f244a52cf69defc`, mergedAt `2026-05-20T08:23:54Z`. Wrote Session 8 SFT unblock decision package to durable evidence: clean base cannot currently be located/repaired from verified local artifacts; warm-start fallback recommended only if PM/supervisor approves `/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-final`; GPU/current nodes.json remains required.
- 2026-05-20 Session 9: Applied PM gate decision to use dev_1 clean-base candidate `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` for the next SFT smoke. Verified the candidate has config/tokenizer/generation config, 5 safetensors shards, and no missing index shards. Prepared no-launch SFT smoke command package in `evidence/dev_4_sft_pipeline.md`; real launch remains blocked only on GPU endpoint or current Milestone 1 `nodes.json`.
