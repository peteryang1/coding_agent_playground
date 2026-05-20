# Milestone 1 Blockers

## Active

- PR #2 gate: after pushing current PM durable updates, PR #2 still reports mergeability `UNKNOWN`; PM-owned PR #2 is not self-merge-ready until mergeability resolves or a concrete conflict/check blocker is identified.
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

## Resolved / Mitigated

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
