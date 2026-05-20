# Milestone 1 Blockers

## Current Superseding Active Blockers

- PR #14 conflict: dev_4's PR #14 became `CONFLICTING` after PR #15 merged. Dev_4 must preserve PR #15 route records, rebase/merge current main, and self-merge once ready before proceeding with SFT smoke evidence.
- SFT real launch is now unblocked on GPU route but still not complete. Compute approved `ssh -p 39314 root@10.100.20.37`; dev_4 owns the real `DRY_RUN=0` SFT smoke and must produce `evidence/dev_4_sft_smoke_run.md`.
- GPU/current allocation: corrected final workspace entry host has no visible `nvidia-smi`, and no current Milestone 1 `nodes.json` exists. Real SFT smoke remains blocked until a GPU SSH endpoint/current `nodes.json` is provided, or explicit approval is given to reuse a historical allocation.
- GPU route approval: dev_2 found two live H200 candidate endpoints, but they are not approved for Milestone 1, appear occupied/high-memory, and lack local SFT paths. Real SFT smoke remains blocked until compute approves a candidate or allocates a fresh single-node H200/current `nodes.json`.
- SFT real launch is blocked until an approved GPU/current `nodes.json` exists. Dev_4's no-launch clean-base package is now on main via PR #11, but there is still no real `DRY_RUN=0` checkpoint/output.
- mini-swe-agent real smoke is blocked on the SFT smoke model/checkpoint or endpoint. Test_2's current gate requires a served OpenAI-compatible model string and endpoint; a raw checkpoint path alone is not accepted until served.
- PM gate: current dry-run manifest and eval readiness metrics do not prove loop completion. Test_1 and test_2 criteria are now present, but real SFT/eval artifacts are still absent.

## Active

- PR #1 owner action: PR #1 is gate-passed and mergeable, but still awaits dev_4 owner self-merge confirmation.
- Continuation PR: after PR #2 merged, PM coordination has moved to branch `pm/milestone1-continuation-20260520`; a new PR is needed for subsequent PM durable updates.
- Evidence still missing after PR #3 merge: dev_1 clean-base support, dev_2 GPU/nodes support, test_1 completion gate, dev_4 SFT unblock decision package, and test_2 eval gate package.
- GPU/SFT workflow: Qwen3-8B SFT GPU allocation and exact training launcher need confirmation from axrd records or compute manager.
- mini-swe-agent evaluation environment is not installed on the corrected final workspace machine. PM checks found `singularity` present, but `mini`, `mini-extra`, Docker, Apptainer, and `sb-cli` absent, so evaluation is blocked until an install/backend path is provided.
- Qwen3-8B SFT base/checkpoint path and GPU allocation are not yet validated. Dev_4 is deriving the training plan from axrd records.
- SFT real launch is blocked on a valid Qwen3-8B base/checkpoint path and GPU allocation/current milestone `nodes.json`. Dev_4 validated dry-run command/manifest with the cleaned 10-example dataset.
- mini-swe-agent real smoke is blocked on the SFT smoke model/checkpoint or endpoint. Test_2 validated the Singularity/mini-swe-agent command path.
- PM execution boundary: PM must not personally run additional code/experiments or remote workspace commands for this milestone. This is not a technical blocker, but it means dev_4/test_2 must provide the next SFT/eval execution evidence and PM will gate their durable outputs.
- PM gate: current dry-run manifest and eval readiness metrics do not prove loop completion; dev_4 must provide a base/checkpoint/GPU decision package, and test_2 must provide checkpoint/endpoint eval gate evidence before real smoke can proceed.
- Evidence gap: dev_4/test_2 decision packages are still pending; dev_1/dev_2/test_1 now own parallel support evidence for base-path candidates, GPU/current `nodes.json`, and completion gate criteria.
- Evidence pending: the new dev_1/dev_2/test_1 support files are not present yet, so PM cannot make the clean-base/GPU/warm-start decision from durable evidence in this check.

## Watch Items

- GitHub API rate limits may affect repo metadata refresh.
- Old 300/100-per-repo rollout outputs may look useful but are scratch-only after Session 4 scope change; final evidence must come from `/root/workspace/rollouts_m1_10`.
- mini-swe-agent benchmark target and scoring format need a smoke test before full evaluation.
- PM top priority is full team utilization: each dev/test owner must continue with independent durable evidence while upstream artifacts are still forming.
- PM should check durable files for progress rather than executing remote commands directly.
- Dev_4 was observed working through a local `status.md` conflict in its own workspace; this is an owner-workflow watch item until the no-launch clean-base SFT package lands.

## Resolved / Mitigated

- PR #1 owner action: dev_4 self-merged PR #1 at `2026-05-20T08:23:54Z`, merge commit `882d1642884e82d1a40674266f244a52cf69defc`.
- PR #10 coordination state: PM self-merged PR #10 at `2026-05-20T08:45:07Z`, merge commit `ce59c983372ac12dc3433091278efb6eec1876eb`.
- PR #12 coordination state: PM self-merged PR #12 at `2026-05-20T08:56:29Z`, merge commit `1e32de047754e376f107b727ddf7349417696db9`.
- PR #13 coordination state: PM self-merged PR #13 at `2026-05-20T09:00:25Z`, merge commit `9a6de432919102c17fdd839e5544d46c98a8f1f7`.
- PR #11 owner action: dev_4 self-merged PR #11 at `2026-05-20T09:10:26Z`, merge commit `93c4efaaff3e50220f7bb8583070321e65289efa`; no-launch clean-base SFT package and conflict-resolution evidence are on main.
- Dev_2 GPU route acquisition: `evidence/dev_2_gpu_route_attempt.md` is present and passes PM gate for route-attempt evidence.
- Compute GPU route: `evidence/compute_gpu_route_decision.md` and `evidence/compute_gpu_route_nodes.json` are present; approved endpoint is `ssh -p 39314 root@10.100.20.37`.
- Base-model selection: dev_1 evidence identified `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` as the preferred local clean-base candidate; PM decision is to prefer it over warm-start fallback once GPU/current `nodes.json` exists.
- Test_1 completion criteria: `evidence/test_1_sft_eval_completion_gate.md` is present and passes PM gate for required completion evidence criteria.
- Test_2 eval acceptance criteria: `evidence/test_2_eval_validation.md` now includes current checkpoint/endpoint acceptance forms, env/config checks, output/metrics requirements, pass/fail criteria, and dirty checkout provenance.
- PM active goal: current goal is active for Milestone 1 and uses corrected final workspace `ssh -p 31787 root@10.100.194.40`.
- Remote Codex CLI: corrected final workspace has `/usr/local/bin/codex`, `~/.codex/auth.json`, and `codex --version` reports `codex-cli 0.130.0`.
- Non-dry rollout gate: PM tiny non-dry rollout on corrected final workspace passed for `fastapi/fastapi`, wrote expected raw artifacts under `/root/workspace/rollouts_nondry_new_machine_tiny`, and left repo working trees clean.
- Full rollout input gate: PM generated `/root/workspace/rollout_harness/tasks_300.jsonl` with exactly 100 records per selected repo and 300 unique task ids.
- Data cleaning smoke gate: `convert_rollouts_to_sft.py` produced `/root/workspace/cleaned_m1_sft_live/train.jsonl` with 7 valid `coding_agent_playground_sft_v1` examples across all three repos, 0 rejects, and 0 conversion errors from real non-dry artifacts.
- Old 300 rollout stopped/superseded: known parent PIDs `1208139`, `1270557`, `1270562` and their observed codex child PIDs are dead. Scratch markers are written under `/root/workspace/rollout_harness/STOPPED_OLD_300_ROLLOUTS_AT.txt` and `OLD_300_OUTPUTS_SCRATCH_ONLY.txt`.
- Active 10-task input gate: `/root/workspace/rollout_harness/tasks_m1_10.jsonl` has exactly 10 records, split across `fastapi=4`, `scikit-learn=3`, and `rich=3`, and every prompt requires actual edit/patch plus test/check attempt.
- Active 10-total rollout quality gate: `/root/workspace/rollouts_m1_10/manifest.jsonl` has 10 entries and `complete_process_validation.json` reports 10 checked, 10 valid, 0 invalid.
- Final clean SFT smoke data gate: `/root/workspace/cleaned_m1_sft_10/train.jsonl` has 10 kept `coding_agent_playground_sft_v1` examples, 0 rejects, 0 conversion errors.
- Test_1's original "no executable harness artifact" blocker is resolved: dev_2 produced `evidence/rollout_harness/run_codex_rollouts.py`, deployed it to `/root/workspace/rollout_harness`, and created dry-run outputs under `/root/workspace/rollouts_smoke`.
- Test_1's dry-run artifact contract findings are mitigated in dev_2 harness v2: `/root/workspace/rollouts_smoke_v2` contains `stdout.jsonl`, `stderr.log`, `last_message.md`, `raw_trajectory.json`, stable `trajectory_id`, full repo IDs, and a manifest-reconciled `summary.json`.
