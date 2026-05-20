# Milestone 1 History Log

<!-- METADATA:SESSION=8 -->

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

## Session 6 - 2026-05-20

- Applied supervisor PM role correction: PM's responsibility is now assignment, gatekeeping, information collection, and decision-making only.
- PM will not directly modify code, run remote workspace code, run experiments, launch SFT, probe GPU/model paths, or execute mini-swe-agent eval; those actions are delegated to dev/test owners.
- Delivered direct activation for all six dev/test interns:
  - `intern_code_dev_3` and `intern_code_test_1` received normal peer assignment messages.
  - `intern_code_dev_1`, `intern_code_dev_2`, `intern_code_dev_4`, and `intern_code_test_2` received `/esc` interrupts and tmux-submitted direct assignments after peer delivery remained busy/unconfirmed.
- Re-established owner responsibilities:
  - `intern_code_dev_1`: task/prompt quality review for 10 complete-process trajectories.
  - `intern_code_dev_2`: rollout harness/run evidence, old-300 stopped evidence, manifest and rerun strategy.
  - `intern_code_dev_3`: cleaned data and `coding_agent_playground_sft_v1` conversion evidence.
  - `intern_code_dev_4`: SFT/GPU/model path probing and any SFT execution.
  - `intern_code_test_1`: 10-trajectory complete-process validation.
  - `intern_code_test_2`: mini-swe-agent smoke readiness/execution once a model/checkpoint/endpoint exists.
- Durable files remain the only routine status channel; dev/test should write evidence/status files and not peer-send PM for routine updates.

## Session 7 - 2026-05-20

- Applied supervisor PM -> dev/test notification-channel change.
- New default delivery for PM task/correction messages is direct tmux injection into the target intern pane followed by Enter.
- `peer_send` is no longer the primary delivery path for dev/test tasking because its priority is insufficient for this workflow.
- PM should not casually interrupt: avoid `C-c`, `/esc`, or equivalent unless the supervisor explicitly requires urgent interruption, or the target's current behavior would keep wasting resources or continue incorrect execution.
- After each tmux injection, PM must run `tmux capture-pane` to verify the message was submitted and did not remain parked on the input line.
- This communication change was recorded in PM personal knowledge, task knowledge, status, and assignments; durable evidence files remain the route for dev/test routine status/results.
- PM gated the current SFT/eval evidence and did not mark the loop complete: dev_4 evidence still shows no valid clean Qwen3-8B base path, no GPU/current `nodes.json`, and only a dry-run manifest; test_2 evidence still shows mini-swe-agent readiness but no SFT model/checkpoint/endpoint.
- PM used the new non-interrupt tmux flow to assign:
  - `intern_code_dev_4`: write a current SFT unblock decision package covering clean base repair/location, warm-start fallback recommendation, GPU/current `nodes.json` acquisition/verification, exact next command after base+GPU, and blockers requiring PM/supervisor decision.
  - `intern_code_test_2`: write a current mini-swe gate package covering exact checkpoint/endpoint acceptance checks, prediction/results/metrics verification, and dirty checkout provenance.
- `tmux capture-pane` verified both dev_4 and test_2 messages were submitted to the target panes; PM did not use `/esc` or `C-c` for this assignment.
- PM checked for follow-up evidence and found dev_4/test_2 had not yet written new decision/gate packages. PM kept the goal active and did not mark blocked or complete.
- PM split parallel support work by non-interrupt tmux injection:
  - `intern_code_dev_1`: clean Qwen3-8B base path/model registry support evidence.
  - `intern_code_dev_2`: current GPU allocation/`nodes.json`/compute workflow support evidence.
  - `intern_code_test_1`: SFT+mini-swe completion audit gate.
- `tmux capture-pane` verified dev_1/dev_2/test_1 messages were submitted; PM did not use `/esc` or `C-c`.
- PM rechecked the durable evidence directory after the parallel support assignment. The requested support files `dev_1_sft_base_path_support.md`, `dev_2_gpu_nodes_support.md`, and `test_1_sft_eval_completion_gate.md` are not present yet, and dev_4/test_2 evidence still has no new decision/gate package.
- PM kept the active goal open: current evidence still proves rollout/data/dry-run/readiness only, not real SFT smoke or mini-swe eval smoke.

## Active Next Steps

- Gate dev_4's durable decision package for valid Qwen3-8B base/checkpoint path and allocated GPU node or current milestone `nodes.json`.
- Gate test_2's mini-swe-agent smoke evidence after dev_4 provides an SFT smoke model/checkpoint path or endpoint.
- Gate dev_1/dev_2/test_1 support evidence when those files appear, then decide whether to escalate clean base/GPU allocation or accept an explicit warm-start smoke fallback.

## Session 8 - 2026-05-20

- Applied supervisor PR gate correction: a PR that is ready/mergeable and passes PM gate should not wait for whole-milestone completion; PM gates readiness and notifies the PR owner to self-merge.
- Audited PR #1 `https://github.com/peteryang1/coding_agent_playground/pull/1`:
  - state `OPEN`, non-draft, mergeable `MERGEABLE`;
  - head `intern_code_dev_4/milestone1_qwen3_8b_loop`, base `main`;
  - scope is Qwen3-8B SFT pipeline artifacts and dev_4 status;
  - PM gate pass for scoped SFT pipeline artifact merge, independent of unresolved real SFT/eval smoke blockers.
- PM notified `intern_code_dev_4` by non-interrupt tmux inject to self-merge PR #1 via playbook and update durable status/evidence with the merge result; `capture-pane` verified the message was submitted.
- Audited PR #2 `https://github.com/peteryang1/coding_agent_playground/pull/2`:
  - state `OPEN`, non-draft, mergeable `UNKNOWN` at initial audit;
  - PM branch had current uncommitted durable rule/status updates, so PR #2 was not gate-ready at that point.
  - blocker for PR #2: push current PM durable updates and recheck mergeability before any self-merge decision.
- After pushing Session 8 durable updates, PM rechecked PR state:
  - PR #1 remains `OPEN`, non-draft, mergeable `MERGEABLE`, with `mergedAt=null`; owner dev_4 has been notified to self-merge.
  - PR #2 remains `OPEN`, non-draft, mergeable `UNKNOWN`, with `mergedAt=null`; PM-owned PR #2 is not self-merge-ready until mergeability resolves to mergeable or a concrete conflict/check blocker is identified.
- PM rechecked PR #2 again and mergeability resolved to `MERGEABLE`.
- PM gate pass for PR #2: it is a coordination/evidence PR, remains explicit that SFT/eval smoke is incomplete, and does not claim milestone completion. Under the supervisor PR gate correction, PM-owned PR #2 should be self-merged without waiting for the whole milestone loop to finish.
- PM self-merged PR #2 as owner. Merge commit `07b0dd167b9004af1c6994652966b7e1de5f2084`, merged at `2026-05-20T07:51:54Z`.
- PM created continuation branch `pm/milestone1-continuation-20260520` from updated `origin/main` so further coordination updates keep flowing through PR instead of the already-merged PR #2.
- PM rechecked PR #1 and found it still `OPEN`, non-draft, mergeable `MERGEABLE`, `mergedAt=null`; PM sent a non-interrupt tmux follow-up to dev_4 to self-merge PR #1 as owner and continue the SFT unblock package.
- PM rechecked support evidence and found the requested files still missing: `dev_1_sft_base_path_support.md`, `dev_2_gpu_nodes_support.md`, and `test_1_sft_eval_completion_gate.md`.
- PM sent non-interrupt tmux follow-ups to dev_1/dev_2/test_1 for the missing support evidence and verified all messages with `capture-pane`.
