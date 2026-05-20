# Milestone 1 History Log

<!-- METADATA:SESSION=5 -->

## Session 1 - 2026-05-20

- Accepted Milestone 1 under `secretary_pm_dev_test_intern_team_pattern_skill`.
- Applied durable-channel correction for dev/test: PM assignments name evidence paths; dev/test routine confirmations, status, blockers, reports, and test results are written to durable files rather than peer-sent to PM.
- Applied durable-reporting correction for secretary: PM does not proactively peer_send secretary for routine milestone reports/status/blockers/summaries/completion; secretary-facing content is written to `pm_secretary_report.md`, `status.md`, `blockers.md`, and evidence files.
- Created durable task root `workspace/tasks/milestone1_qwen3_8b_loop`.
- Selected three different high-star repositories: `fastapi/fastapi`, `scikit-learn/scikit-learn`, and `Textualize/rich`.
- Verified final workspace machine `ssh -p 31787 root@10.100.194.40` and cloned repos under `/root/workspace/{fastapi,scikit-learn,rich}`.
- Assigned all dev/test interns with durable evidence paths in `assignments.md`.
- Reviewed evidence from dev/test:
  - Dev 2 implemented/deployed rollout harness and ran dry-run smoke.
  - Dev 3 proposed `coding_agent_playground_sft_v1` trajectory format and cleaning policy.
  - Dev 4 began Qwen3-8B SFT/GPU workflow research from axrd records.
  - Test 1 recorded validation preflight and needs recheck now that harness artifacts exist.
  - Test 2 recorded mini-swe-agent/backend blocker and smoke eval gate.
- Verified `/mnt/3fs/data/tools/codex` exists on the final workspace machine and passes rollout harness preflight.
- Opened PR #2: `https://github.com/peteryang1/coding_agent_playground/pull/2`.
- Continued Session 1 after test_1 updated `evidence/test_1_validation.md` with rollout harness dry-run validation.
- Captured test_1's rollout harness gate findings in durable PM files and routed a durable dev_2 follow-up assignment.
- Confirmed PR #1 and PR #2 are open and mergeable.
- Session 2: checked an earlier final-workspace candidate and found direct zsh Codex/auth unavailable there.
- Session 2: verified dev_2 harness v2 dry-run outputs under `/root/workspace/rollouts_smoke_v2` include required placeholder files, `raw_trajectory.json`, stable trajectory IDs, full repo IDs, and manifest-reconciled summary.
- Session 2: ran tiny non-dry rollout attempts; public endpoint failed with 401 and internal-provider attempt failed with stream-disconnect errors, leaving the non-dry rollout gate open.

## Session 3 - 2026-05-20

- Applied supervisor address correction: authoritative final workspace is `ssh -p 31787 root@10.100.194.40`; previous scratch-host outputs are not final evidence.
- Verified corrected final workspace hostname `lg-cmc-b7r201-k10u23-cpu-000158`.
- Revalidated `/root/workspace/{fastapi,scikit-learn,rich}` on the corrected final workspace:
  - `fastapi/fastapi` at `f4cafbc467c225263ad3b5b0d4a7306b42ac855b`, clean.
  - `scikit-learn/scikit-learn` at `ffc6cdc20b8d5eb58e38042fd90a2aeecc33dfb8`, clean.
  - `Textualize/rich` at `46cebbb032f920eb096efbaf23cdc6fe9dd541f7`, clean.
- Confirmed corrected final workspace has `/usr/local/bin/codex`, `codex-cli 0.130.0`, and `~/.codex/auth.json`.
- Updated rollout harness default Codex command to `/usr/local/bin/codex`, deployed harness/sample tasks to `/root/workspace/rollout_harness`, and passed preflight.
- Ran corrected final-workspace dry-run smoke under `/root/workspace/rollouts_smoke_v3`; all three repos produced required artifact files.
- Ran corrected final-workspace tiny non-dry rollout under `/root/workspace/rollouts_nondry_new_machine_tiny`; one `fastapi/fastapi` trajectory passed with normalized status `success`.
- Updated PM top priority: all six dev/test interns must keep active durable outputs; if an upstream artifact is missing, they must work on assumptions, samples, validators, launchers, smoke plans, or blockers instead of waiting.
- Generated `/root/workspace/rollout_harness/tasks_300.jsonl` with 300 JSONL records, exactly 100 per selected repo and 300 unique task ids.
- Started full rollout in the background on the corrected final workspace: PID file `/root/workspace/rollout_harness/rollouts_m1_300.pid`, log `/root/workspace/rollout_harness/rollouts_m1_300.log`, output root `/root/workspace/rollouts_m1_300`.
- Latest launch snapshot: rollout PID `1208139` is alive, manifest count is 1, and the first `fastapi` trajectory is `passed`.
- Sent PM assignment/correction fanout to dev/test interns with durable evidence paths only; no peer-send confirmations were requested. The daemon returned `undeliverable: unconfirmed` for all six, so PM recorded the assignments durably and proceeded without waiting.
- Continued Session 3: observed remote `tasks_300.jsonl` now uses full repo IDs plus `repo_key`; updated `launch_300_rollouts.sh` to accept slug, full repo ID, or `repo_key`, then redeployed and validated `prepare`.
- Started independent scikit-learn and rich rollout batches in parallel with the main fastapi-leading rollout to avoid idle waiting:
  - `/root/workspace/rollouts_m1_300_scikit_learn`, PID `1270557`;
  - `/root/workspace/rollouts_m1_300_rich`, PID `1270562`.
- Latest rollout snapshot after parallel launch: main PID `1208139` alive with 3 passed FastAPI trajectories; scikit-learn and rich PIDs alive with no manifest entries yet.
- Added and deployed `convert_rollouts_to_sft.py`; conversion smoke over `/root/workspace/rollouts_m1_300` produced `/root/workspace/cleaned_m1_sft_smoke/train.jsonl` with 3 kept examples, 0 rejects, and 0 errors.
- Re-ran conversion over all live roots after parallel batches produced artifacts; `/root/workspace/cleaned_m1_sft_live/train.jsonl` has 7 valid examples across all three repos with 0 conversion errors.

## Session 4 - 2026-05-20

- Applied supervisor scope change: Milestone 1 is now an end-to-end smoke loop, not a full 300-result run.
- New rollout target is 10 total trajectories across the same three repos. Every acceptable trajectory must include requirements understanding, repo/file localization, code inspection, actual code edit/patch attempt, test/check attempt, observation/result/error, and final changed-files/tests/blockers.
- Stopped/superseded old 300/100-per-repo rollout processes on the corrected final workspace:
  - old parent PIDs `1208139`, `1270557`, `1270562` are dead;
  - observed old codex child PIDs `1326371`, `1326392`, `1329762`, `1329783`, `1333349`, `1333370` are dead;
  - no process remains matching old `tasks_300`, `tasks_300_by_repo`, or `rollouts_m1_300` command lines.
- Marked old 300 outputs scratch-only with remote files:
  - `/root/workspace/rollout_harness/STOPPED_OLD_300_ROLLOUTS_AT.txt`;
  - `/root/workspace/rollout_harness/OLD_300_OUTPUTS_SCRATCH_ONLY.txt`.
- Old scratch manifests at stop time: `/root/workspace/rollouts_m1_300` had 6, `/root/workspace/rollouts_m1_300_scikit_learn` had 7, and `/root/workspace/rollouts_m1_300_rich` had 5.
- Created `/root/workspace/rollout_harness/tasks_m1_10.jsonl` with 10 total prompts: `fastapi=4`, `scikit-learn=3`, `rich=3`. Prompt validation confirmed every record requires actual edit/patch attempt plus test/check attempt.
- Deployed `validate_complete_coding_trajectories.py` to `/root/workspace/rollout_harness/validate_complete_coding_trajectories.py`.
- Cleared dry-run placeholders and started real non-dry 10-total rollout at `/root/workspace/rollouts_m1_10`, PID `1341184`, log `/root/workspace/rollout_harness/rollouts_m1_10.log`.
- Latest validation snapshot: `/root/workspace/rollouts_m1_10` has 4 manifest entries and `complete_process_validation.json` reports 4 checked, 4 valid, 0 invalid complete-process trajectories.

## Session 5 - 2026-05-20

- Continued the active 10-total rollout without interruption until completion.
- Final rollout and cleaning evidence:
  - `/root/workspace/rollouts_m1_10/manifest.jsonl` has 10 entries;
  - `/root/workspace/rollouts_m1_10/complete_process_validation.json` reports 10 checked, 10 valid, 0 invalid;
  - `/root/workspace/cleaned_m1_sft_10/train.jsonl` has 10 kept `coding_agent_playground_sft_v1` examples;
  - conversion summary reports 10 input, 10 kept, 0 dropped, 0 errors; kept split is `fastapi/fastapi=4`, `scikit-learn/scikit-learn=3`, `Textualize/rich=3`.
- Used the high-priority interrupt channel for dev/test activation:
  - exact `/esc` delivered to `intern_code_dev_1`, `intern_code_dev_2`, `intern_code_dev_3`, `intern_code_dev_4`, `intern_code_test_1`, and `intern_code_test_2`;
  - follow-up assignment messages delivered to `intern_code_dev_3`, `intern_code_test_1`, and `intern_code_test_2`;
  - `intern_code_dev_1` remained unconfirmed, and `intern_code_dev_2`/`intern_code_dev_4` were busy for follow-up messages, so `assignments.md` is the durable source of truth for their exact work.
- Dev_4 evidence now records Qwen3-8B SFT dry-run command validation with `/root/workspace/cleaned_m1_sft_10/train.jsonl`; dry-run manifest is under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/`.
- Test_2 evidence now records mini-swe-agent smoke readiness using `/root/workspace/swe-bench-related/mini-swe-agent`, `uv run --with datasets`, Singularity backend, and exact commands blocked only on the SFT smoke model/checkpoint or endpoint.
- PM wrote machine-readable eval readiness metrics to `/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json`, status `blocked`, with the exact prepared mini-swe-agent command.
- PM updated `final_report.md` with current rollout/data/SFT/eval evidence and explicit blockers.
- PM re-audited SFT real-launch blockers: no GPU on corrected entry host, no current Milestone 1 `nodes.json`, broken clean base symlink at `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B`, and historical Qwen3-8B checkpoints are readable but require explicit warm-start approval.

## Active Next Steps

- Resolve SFT blockers: valid Qwen3-8B base/checkpoint path and allocated GPU node or current milestone `nodes.json`.
- Run the prepared mini-swe-agent smoke after an SFT smoke model/checkpoint path exists.
