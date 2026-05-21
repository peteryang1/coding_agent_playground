# Milestone 1 History Log

<!-- METADATA:SESSION=27 -->

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

## Session 9 - 2026-05-20

- Dev_4 applied the PM gate decision to prefer dev_1's clean-base candidate for Qwen3-8B SFT smoke:
  - `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.
- Dev_4 verified the candidate on `ssh -p 31787 root@10.100.194.40`: `config.json`, tokenizer files, `generation_config.json`, `model.safetensors.index.json`, 5 safetensors shards, and no missing index shards are present.
- Dev_4 verified the current SFT input checksum:
  - `/root/workspace/cleaned_m1_sft_10/train.jsonl`
  - SHA-256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`.
- Dev_4 wrote the no-launch SFT smoke launch package to `evidence/dev_4_sft_pipeline.md`, including exact single-node command, required GPU evidence, manifest/checkpoint paths to verify, and blockers.
- No SFT launch was attempted because GPU endpoint/current Milestone 1 `nodes.json` is still missing; only historical non-milestone `nodes.json` exists.
- PR #1 was already merged at `2026-05-20T08:23:54Z` with merge commit `882d1642884e82d1a40674266f244a52cf69defc`; no duplicate merge action was needed.
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
- PM opened continuation PR #3 `https://github.com/peteryang1/coding_agent_playground/pull/3`.
- PR #3 is `OPEN`, non-draft, mergeable `MERGEABLE`, and scoped to PM durable coordination after PR #2 merge; PM gate passes because it records active blockers and does not claim milestone completion.
- Under the supervisor PR gate rule, PM will self-merge PR #3 as owner after this durable gate record is pushed.
- PM self-merged PR #3 as owner. Merge commit `ba058d3a87831630c232edbe6d8622b1b648ed54`, merged at `2026-05-20T07:58:02Z`.
- Latest gate check after PR #3 merge:
  - PR #1 remains `OPEN`, non-draft, mergeable `MERGEABLE`, `mergedAt=null`, and still awaits dev_4 owner self-merge.
  - `dev_1_sft_base_path_support.md`, `dev_2_gpu_nodes_support.md`, and `test_1_sft_eval_completion_gate.md` are still missing.
  - dev_4/test_2 evidence still has no new SFT unblock decision package or eval gate package.
- PM keeps the active goal open because current evidence still does not prove real SFT smoke or mini-swe eval smoke.
- PM self-merged PR #4 as owner after it passed the same coordination-only gate. Merge commit `002155e6295461871544cfc267863facc5570dd5`, merged at `2026-05-20T08:01:24Z`.
- PM re-audited PR #1 after PR #4 merge:
  - PR #1 remains `OPEN`, non-draft, mergeable `MERGEABLE`, `mergedAt=null`;
  - scope remains dev_4-owned Qwen3-8B SFT pipeline artifacts, so PM gate remains pass for owner self-merge and does not wait for full milestone completion;
  - PM sent another non-interrupt tmux inject to `intern_code_dev_4` instructing owner self-merge plus durable merge evidence/status updates, and `capture-pane` verified the message was submitted.
- PM rechecked current SFT/eval gate support evidence:
  - `dev_1_sft_base_path_support.md` is still missing;
  - `dev_2_gpu_nodes_support.md` is still missing;
  - `test_1_sft_eval_completion_gate.md` is still missing;
  - dev_4/test_2 evidence files still do not contain a new SFT unblock decision package or mini-swe eval gate package.
- PM decision: keep the active goal open; do not mark complete because no durable evidence yet proves real SFT smoke output or mini-swe eval smoke output/metrics.
- PM self-merged PR #5 as owner after it passed coordination-only gate. Merge commit `8f5b7736939453c15ffb802c42a0ee9c875b531d`, merged at `2026-05-20T08:07:31Z`.
- PM re-audited PR #1 after PR #5 merge:
  - PR #1 is still `OPEN`, non-draft, mergeable `MERGEABLE`, with `mergedAt=null` and no merge commit;
  - PM gate remains pass for dev_4 owner self-merge of scoped Qwen3-8B SFT pipeline artifacts;
  - PM still must not merge PR #1 on dev_4's behalf.
- PM rechecked durable evidence directory and found no new support files:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_sft_base_path_support.md` missing;
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_gpu_nodes_support.md` missing;
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_sft_eval_completion_gate.md` missing.
- PM used non-interrupt tmux injection plus `capture-pane` verification to submit active-gate follow-ups:
  - `intern_code_dev_4`: self-merge PR #1 if local playbook check passes, or write exact blocker; also write SFT unblock decision package.
  - `intern_code_dev_1`: write clean Qwen3-8B base/model registry support evidence.
  - `intern_code_dev_2`: write GPU/current `nodes.json`/compute workflow support evidence.
  - `intern_code_test_1`: write SFT+mini-swe completion audit gate.
- PM decision remains unchanged: active goal stays open because SFT/eval smoke completion is unproven; continue collecting owner evidence rather than running experiments directly as PM.
- PM self-merged PR #6 as owner after it passed coordination-only gate. Merge commit `9f43d16932098010b12a138d661f90a383ff2d0a`, merged at `2026-05-20T08:14:18Z`.
- PM re-audited current state after PR #6:
  - PR #1 remains `OPEN`, non-draft, mergeable `MERGEABLE`, with `mergedAt=null`; dev_4 remains responsible for self-merge or writing a concrete blocker.
  - The requested support files remain absent from the PM worktree: `dev_1_sft_base_path_support.md`, `dev_2_gpu_nodes_support.md`, and `test_1_sft_eval_completion_gate.md`.
  - dev_4 evidence remains at the earlier dry-run/blocker state and does not yet include a new SFT unblock decision package.
  - test_2 evidence remains at eval readiness/blocker state and does not yet include the requested current acceptance gate package.
- PM expanded the non-interrupt tmux follow-up to keep all six dev/test owners active and verified delivery with `capture-pane`:
  - `intern_code_dev_4`: self-merge PR #1 or write blocker; write SFT unblock package.
  - `intern_code_dev_1`: write clean Qwen3-8B base/model registry support evidence.
  - `intern_code_dev_2`: write GPU/current `nodes.json`/compute route support evidence.
  - `intern_code_dev_3`: write SFT input handoff package for dev_4.
  - `intern_code_test_1`: write SFT+mini-swe smoke completion audit gate.
  - `intern_code_test_2`: write mini-swe eval acceptance gate package and dirty-checkout provenance decision.
- PM decision: do not mark complete or blocked. Completion is unproven; the PM still has meaningful coordination work by collecting owner evidence and making gate decisions.
- PM self-merged PR #7 as owner after it passed coordination-only gate. Merge commit `98eb9d3573e24a732a7de354e8ecbf1c0173c2c3`, merged at `2026-05-20T08:20:50Z`.
- Dev_4 self-merged PR #1 as owner. Merge commit `882d1642884e82d1a40674266f244a52cf69defc`, merged at `2026-05-20T08:23:54Z`.
- Dev_4 appended a Session 8 SFT decision package to `evidence/dev_4_sft_pipeline.md`:
  - clean `Qwen/Qwen3-8B` base path remains broken and cannot be repaired without an approved source;
  - warm-start fallback is only acceptable with explicit PM/supervisor approval, recommended path `/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-final`;
  - GPU route is not ready until compute provides a GPU shell or current Milestone 1 `nodes.json`;
  - exact clean-base and warm-start launch commands are documented.
- Dev_2 wrote `evidence/dev_2_gpu_nodes_support.md`. PM gate result: evidence is sufficient to prove there is no current live GPU route on `ssh -p 31787 root@10.100.194.40`; current Milestone 1 `nodes.json` is missing; historical nodes.json must not be reused without explicit approval.
- Dev_3 wrote `evidence/dev_3_sft_input_handoff.md`. PM gate result: data-side SFT handoff is sufficient for dev_4, using `/root/workspace/cleaned_m1_sft_10/train.jsonl`, format `coding_agent_playground_sft_v1`, 10 examples, 10/10 validation, and SHA-256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`.
- Dev_1 wrote `evidence/dev_1_sft_base_path_support.md`. PM gate result: evidence is sufficient to identify a usable local clean-base candidate at `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`; the broken registry symlink remains invalid, but base-model selection no longer needs warm-start fallback unless the clean-base candidate is rejected later.
- PM sent a non-interrupt tmux decision update to dev_4: prefer dev_1's clean-base candidate as `BASE_MODEL` once GPU/current `nodes.json` exists; keep warm-start fallback only for explicit approval.
- Remaining PM gate gaps:
  - `test_1_sft_eval_completion_gate.md` is still missing;
  - test_2 has not yet appended the current eval acceptance/provenance gate package to `test_2_eval_validation.md`;
  - no current GPU endpoint or Milestone 1 `nodes.json` exists;
  - no real SFT smoke output/checkpoint and no mini-swe eval output/metrics exist yet.
- PM decision: milestone remains active and incomplete. Next decision point is GPU allocation/current `nodes.json`; with current evidence, the preferred SFT base is dev_1's clean-base candidate, not warm-start fallback.
- PM self-merged PR #8 as owner after it passed coordination/evidence gate. Merge commit `97cff0dddfb460585b62193b4f567470b047ffd5`, merged at `2026-05-20T08:33:38Z`.
- PM re-audited the current remaining blockers after PR #8:
  - `test_1_sft_eval_completion_gate.md` is still missing;
  - `test_2_eval_validation.md` still ends at the earlier readiness package and has not yet received the requested current acceptance/provenance package;
  - there is still no current GPU endpoint or Milestone 1 `nodes.json`;
  - there is still no real SFT smoke checkpoint/output and no mini-swe eval metrics.
- PM used non-interrupt tmux injection plus `capture-pane` verification for remaining owner actions:
  - `intern_code_test_1`: create `test_1_sft_eval_completion_gate.md` with required SFT+mini-swe completion files, commands, artifacts, metrics, pass/fail criteria, and insufficient current evidence.
  - `intern_code_test_2`: update `test_2_eval_validation.md` with checkpoint-vs-endpoint acceptance forms, env/config checks, prediction/result/metrics files, pass/fail criteria, and dirty checkout provenance.
  - `intern_code_dev_4`: prepare a no-launch SFT smoke launch package using accepted clean-base candidate `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`, plus required GPU evidence and output/checkpoint manifest verification paths.
- PM decision remains active/incomplete: clean-base and data are ready enough for next SFT smoke, but GPU allocation/current `nodes.json` and test/eval gates are still required before real execution can be authorized.
- PM self-merged PR #9 as owner after it passed coordination-only gate. Merge commit `e876c755d92f8c39fc862daaec8ac7968dfac845`, merged at `2026-05-20T08:39:36Z`.
- PM waited after the required-now tmux messages and rechecked durable evidence:
  - `test_1_sft_eval_completion_gate.md` remains missing;
  - `test_2_eval_validation.md` timestamp remains `2026-05-20 07:19` and does not include the current acceptance/provenance package;
  - `dev_4_sft_pipeline.md` timestamp remains `2026-05-20 08:28` and does not include the requested no-launch clean-base SFT smoke package using `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`;
  - there is no real SFT smoke checkpoint/output and no mini-swe eval metrics.
- PM checked `tmux capture-pane` for `intern_code_test_1`, `intern_code_test_2`, and `intern_code_dev_4`; the required-now messages are present in their panes. PM did not interrupt with `/esc` or `C-c`.
- PM decision: goal remains active, not complete. Current actionable blocker is owner evidence/execution readiness: test_1/test_2 gates and dev_4 clean-base no-launch package must land before PM can authorize SFT/eval execution, and GPU/current `nodes.json` is still required for real SFT.

## Session 9 - Dev 4 Completion Record - 2026-05-20

- Dev_4 completed the PM-required no-launch SFT smoke package using the accepted clean-base candidate `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.
- Dev_4 verified that candidate on `ssh -p 31787 root@10.100.194.40`: `config.json`, tokenizer files, `generation_config.json`, `model.safetensors.index.json`, 5 safetensors shards, and no missing index shards.
- Dev_4 verified current SFT input `/root/workspace/cleaned_m1_sft_10/train.jsonl` with SHA-256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`.
- Dev_4 updated `evidence/dev_4_sft_pipeline.md` with the exact no-launch command package, required GPU evidence, output/checkpoint/manifest paths to verify, and remaining blockers.
- Dev_4 opened PR #11 for Session 9 durable updates: `https://github.com/peteryang1/coding_agent_playground/pull/11`.
- No real SFT launch was attempted; the current blocker remains missing GPU endpoint/current Milestone 1 `nodes.json`.

## 2026-05-20 Session 8 Post-PR10 Test Gate Landing

- PR #10 merged at `2026-05-20T08:45:07Z` with merge commit `ce59c983372ac12dc3433091278efb6eec1876eb`.
- `intern_code_test_1` created `evidence/test_1_sft_eval_completion_gate.md`.
  - PM gate: pass for completion-audit criteria.
  - The file correctly states current evidence is insufficient for completion and requires real `DRY_RUN=0` SFT, checkpoint/model artifacts, logs/metrics, mini-swe smoke against the resulting model, predictions/trajectories, and metrics before PM can mark the loop complete.
- `intern_code_test_2` updated `evidence/test_2_eval_validation.md`.
  - PM gate: pass for mini-swe acceptance/provenance criteria.
  - The package correctly requires a served OpenAI-compatible endpoint/model string for mini-swe; raw checkpoint paths must first be served and kept as provenance.
  - The package records the dirty mini-swe checkout as acceptable for smoke only with explicit provenance.
- `intern_code_dev_4` has not yet landed the requested no-launch clean-base SFT smoke package in PM worktree. PM observed dev_4 working in its own workspace and handling a local `status.md` conflict; dev_4 remains owner for resolving and landing durable evidence.
- PM decision: no SFT/eval execution authorization yet. The remaining hard blockers are current GPU endpoint or Milestone 1 `nodes.json`, dev_4's no-launch package, real SFT checkpoint/output, and mini-swe eval metrics.

## 2026-05-20 Session 8 PR #11 Gate Audit

- PR #12 merged at `2026-05-20T08:56:29Z` with merge commit `1e32de047754e376f107b727ddf7349417696db9`.
- PM audited dev_4 PR #11 for the no-launch clean-base SFT smoke package.
  - URL: `https://github.com/peteryang1/coding_agent_playground/pull/11`
  - state: `OPEN`
  - draft: `false`
  - mergeability: `CONFLICTING`
- PM gate result: PR #11 is not ready for owner self-merge because it conflicts with current `main`.
- PM action: notified dev_4 by non-interrupt tmux inject to rebase/merge current `origin/main`, resolve conflicts without dropping PM/test_1/test_2 post-PR10 gate records, push PR #11 again, and record durable conflict files/resolution. PM did not merge PR #11.

## 2026-05-20 Session 8 PR #11 Merge And GPU Route Gate

- PR #13 merged at `2026-05-20T09:00:25Z` with merge commit `9a6de432919102c17fdd839e5544d46c98a8f1f7`.
- Dev_4 resolved PR #11 conflicts, preserved PM/test_1/test_2 post-PR10 gate records, pushed the branch, and PR #11 became `MERGEABLE`.
- PM notified dev_4 by non-interrupt tmux inject that PR #11 passed PM gate and should be self-merged by the owner.
- Dev_4 self-merged PR #11:
  - mergedAt: `2026-05-20T09:10:26Z`
  - merge commit: `93c4efaaff3e50220f7bb8583070321e65289efa`
- Dev_2 wrote `evidence/dev_2_gpu_route_attempt.md`.
  - Compute manager peer route attempt was undeliverable with reason `unconfirmed`.
  - No current Milestone 1 `nodes.json` exists.
  - Read-only LTP discovery found two live H200 8-GPU candidate endpoints: `ssh -p 27094 root@10.100.10.20` and `ssh -p 31403 root@10.100.8.24`.
  - PM gate: these candidates are not approved for Milestone 1, show high GPU memory use, and lack local SFT paths, so they cannot be used without compute/PM approval and staging.
- PM decision: real SFT remains blocked on approved current GPU route. No SFT/eval execution is authorized by PM yet.

## 2026-05-20 Session 8 Approved GPU Route And SFT Dispatch

- PR #15 merged at `2026-05-20T09:19:31Z` with merge commit `21c59cd013e6d8c1a736483cc91864b11325f417`.
- Compute manager wrote:
  - `evidence/compute_gpu_route_decision.md`
  - `evidence/compute_gpu_route_nodes.json`
- Approved fresh single-node H200 SFT smoke route:
  - `ssh -p 39314 root@10.100.20.37`
  - LTP frame `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130`
  - node `lg-cmc-b7r202-o09u26-h200-000667`
  - 8 x NVIDIA H200, empty compute process list at verification
  - CephFS mounted and output root writable
  - `/root/workspace/coding_agent_playground` and `/root/workspace/cleaned_m1_sft_10/train.jsonl` staged
- PM decision: route is approved for short Qwen3-8B SFT smoke only.
- PM notified dev_4 by tmux inject:
  - PR #14 became `CONFLICTING` after PR #15 and must be resolved/preserved first.
  - After PR #14 is mergeable/self-merged, dev_4 should run the short SFT smoke using `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`, `DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl`, `OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`, and `DRY_RUN=0`.
  - Results must be written to `evidence/dev_4_sft_smoke_run.md`.
- PM did not run SFT and did not run mini-swe.

## Session 10 - Dev 4 PR #11 Conflict Resolution - 2026-05-20

- Dev_4 handled PM gate notice that PR #11 was `CONFLICTING`.
- Dev_4 merged current `origin/main` into branch `intern_code_dev_4/session9-sft-smoke-launch-package`.
- Conflict file:
  - `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md`
- Resolution:
  - preserved dev_4 Session 9 completion record for the no-launch clean-base SFT smoke package;
  - preserved PM/test_1/test_2 post-PR10 gate records, including PR #10 merge, test_1 completion gate, test_2 eval acceptance/provenance gate, and PM PR #11 gate audit;
  - appended this Session 10 conflict-resolution record.
- After push, GitHub PR #11 recheck reported `mergeable=MERGEABLE`, `state=OPEN`.
- No SFT launch was attempted. The only remaining SFT launch blocker remains GPU endpoint/current Milestone 1 `nodes.json`; the next SFT command should use `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.

## Session 11 - Dev 4 PR #11 Merge Evidence - 2026-05-20

- PM gate input: PR #11 was `MERGEABLE` and passed PM gate for scoped no-launch clean-base SFT smoke package/conflict-resolution evidence.
- Dev_4 owner action: self-merged PR #11 using merge commit workflow after local `git diff --check` passed.
- PR URL: `https://github.com/peteryang1/coding_agent_playground/pull/11`
- `mergedAt`: `2026-05-20T09:10:26Z`
- Merge commit: `93c4efaaff3e50220f7bb8583070321e65289efa`
- Scope merged by PR #11: Session 9 no-launch clean-base SFT smoke package plus Session 10 conflict-resolution evidence preserving PM/test_1/test_2 post-PR10 gate records.
- Session 11 evidence PR: `https://github.com/peteryang1/coding_agent_playground/pull/14`
- No SFT launch was attempted. Real SFT remains blocked on GPU endpoint/current Milestone 1 `nodes.json`; the next launch package still uses `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.

## Session 12 - Dev 4 PR #14 Conflict Refresh Before SFT Smoke - 2026-05-20

- PM order update: PR #14 became `CONFLICTING` after PR #15 merged; dev_4 must refresh PR #14 against current `origin/main`, preserve PR #15 dev_2 GPU route evidence and PM records, push PR #14, and self-merge only after it becomes mergeable.
- Approved GPU route for the subsequent SFT smoke, after PR #14 is mergeable and self-merged: `ssh -p 39314 root@10.100.20.37`.
- Approved `nodes.json` evidence path: `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/compute_gpu_route_nodes.json`; staged on GPU at `/root/workspace/coding_agent_playground/nodes.json` and `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_nodes.json`.
- Dev_4 merged current `origin/main` into PR #14 branch `intern_code_dev_4/session11-pr11-merge-evidence`.
- Conflict file:
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`
- Resolution:
  - preserved dev_4 PR #11 merge facts and no-launch package facts;
  - preserved PR #15/PM records from `origin/main`, including dev_2 GPU route acquisition evidence and prior unapproved H200 candidate findings;
  - added PM's newly approved GPU route as the active route for the next SFT smoke.
- No SFT launch was attempted during conflict resolution; launch remains ordered only after PR #14 is mergeable and self-merged.

## Session 13 - Dev 4 Qwen3-8B SFT Smoke Run - 2026-05-20

- Resource rule update: active H200 resource is tracked by PM/dev_2; dev_4 owns only SFT workload evidence, and dev_2 owns LTP lifecycle/stop proof.
- Dev_4 did not ask axrd interns for GPU and did not run mini-swe.
- PR #14 was self-merged before SFT execution:
  - mergedAt: `2026-05-20T09:33:27Z`
  - merge commit: `e21d6ba8c94ca4561777ec22444e9c1dd3d61b7a`
- Approved endpoint used: `ssh -p 39314 root@10.100.20.37`.
- Prechecks passed for H200 GPUs, staged `nodes.json`, repo, dataset, clean base, output root, and LLamaFactory/MCA dependencies.
- Dev_4 ran the approved short clean-base SFT smoke with:
  - `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`
  - `DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl`
  - `OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`
  - `DRY_RUN=0`
- Result evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_smoke_run.md`.
- Result: no checkpoint/model was produced. Baseline run reached training setup but failed with MCA tiny-data DP=8 `ZeroDivisionError` from `steps_in_epoch=0`; one bounded TP=8 retry failed Megatron scheduler assertion `lr_warmup_steps < lr_decay_steps` for 1-step smoke.
- Resource decision: dev_2 should stop the active H200 allocation immediately and record stop proof. Further retry should wait for PM-approved config change for MCA/Megatron tiny-data smoke.
- Evidence PR: `https://github.com/peteryang1/coding_agent_playground/pull/18`

## 2026-05-20 Session 11 Resource Management Correction

- Supervisor correction applied: do not keep asking axrd interns for GPU machines. coding_agent_playground dev/test owners must learn and use LTP directly for submit/status/ssh/stop workflows.
- PM boundary reaffirmed: PM organizes, gates, collects durable evidence, and decides; PM does not submit LTP jobs, run SFT/eval, or stop resources directly.
- Created `evidence/gpu_resource_tracking.md` for the active 8xH200 node:
  - LTP frame `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130`
  - endpoint `ssh -p 39314 root@10.100.20.37`
  - lifecycle/stop-proof owner `intern_code_dev_2`
  - SFT workload owner `intern_code_dev_4`
  - expected end `2026-05-20T10:30:00Z` or earlier
  - stop conditions and stop proof requirements recorded
- Updated assignments/status/blockers/task knowledge with the new resource-management rule and owner split.
- PM sent non-interrupt tmux instructions to dev_2 and dev_4: dev_2 must track/stop the LTP job and write stop proof; dev_4 must run the SFT smoke only after PR #14 conflict resolution and write SFT evidence. No mini-swe execution is authorized yet.

## 2026-05-20 Session 12 Task-To-PR Gate And Resource Stop Gate

- Supervisor conduct rule applied: PM must create and maintain explicit tasks, then assign dev/test work through those tasks rather than only scattered assignment lines.
- Created `task_registry.md` as the Milestone 1 task -> PR -> merge -> task-complete gate index.
- PM gate updated: each dev/test PR must reference a task id, owner, acceptance criteria, durable evidence path, and completion marker before PM marks it ready/mergeable for owner self-merge.
- Owner merge rule updated: when a dev/test intern self-merges a PR, that owner must mark the matching task complete in task README/status or `task_registry.md`, update own `status.md`, update necessary history/evidence, push, and merge the completion record.
- PM will keep ready/mergeable PRs moving immediately after gate pass; no PR waits for entire milestone completion.
- Dev_4 reported the real SFT smoke attempt plus one bounded retry both failed: first on MCA/drop_last zero-step with 10 examples under DP=8, then on Megatron LR scheduler assertion with TP=8/DP=1/max_steps=1. No checkpoint/model output exists from these attempts.
- PM resource gate decision: no more GPU use is authorized for this dev_4 attempt. PM injected dev_2 to stop/release LTP frame `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130` and write stop proof to `evidence/dev_2_gpu_lifecycle.md` and `evidence/gpu_resource_tracking.md`.
- PM audited dev_4 PR #18 for the new task-to-PR gate. Gate result: not ready because GitHub reports `mergeable=CONFLICTING` and the PR body does not reference task id `M1-SFT-SMOKE-DEV4`.
- PM injected dev_4 with the required correction: attach PR #18 to task `M1-SFT-SMOKE-DEV4`, resolve conflicts preserving PM Session 12 task registry/gate records, push, self-merge only after mergeable, and then mark the task complete or blocked-with-final-evidence in durable task/status files.

## Session 15 - Dev 4 PR #18 Task ID And Conflict Refresh - 2026-05-20

- PM correction applied: PR #18 must use existing PM task id `M1-SFT-SMOKE-DEV4`.
- Dev_4 merged current `origin/main` into branch `intern_code_dev_4/session12-sft-smoke-run`; after main advanced with dev_2 lifecycle evidence and then PR #20 post-merge evidence, dev_4 merged `origin/main` again and preserved dev_2 stop-proof records.
- Conflict files:
  - `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- Resolution:
  - preserved PM Session 12 `task_registry.md` and task-to-PR gate records from PR #19;
  - preserved dev_2 GPU lifecycle stop proof and PR #20 merge evidence from `origin/main`;
  - preserved dev_4 Session 13 SFT smoke run evidence and no-checkpoint result;
  - updated dev_4 evidence/status/history/task knowledge to reference task id `M1-SFT-SMOKE-DEV4`.
- PR #18 body was updated to reference task id `M1-SFT-SMOKE-DEV4`, owner, acceptance criteria, durable evidence path, and completion marker.
- No self-merge was attempted in this session because the latest PM gate said PR #18 was not ready; owner self-merge remains blocked until GitHub reports `MERGEABLE` and PM gate passes.

## 2026-05-20 Session 12 Dev 2 GPU Lifecycle Stop Completion

- Task id: `M1-GPU-LIFECYCLE-DEV2`.
- Owner: `intern_code_dev_2`.
- PM resource gate input: dev_4 reported the real Qwen3-8B SFT smoke plus one bounded retry both failed and recommended no further GPU use.
- dev_2 lifecycle action:
  - observed active torchrun/python GPU work at 2026-05-20T09:41Z and did not stop during real SFT progress;
  - observed bounded retry artifacts for `milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z`;
  - after PM resource gate, sent `ltp.py stop xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130` at 2026-05-20T09:52Z.
- Stop proof:
  - LTP state reached `STOPPED (Completed)`;
  - completed timestamp: `2026-05-20 09:53:21`;
  - endpoint proof: `ssh -p 39314 root@10.100.20.37` refused connection after stop;
  - outputs preserved under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.
- Durable evidence:
  - `evidence/dev_2_gpu_lifecycle.md`;
  - `evidence/gpu_resource_tracking.md`;
  - `task_registry.md` completion marker for `M1-GPU-LIFECYCLE-DEV2`.
- Completion record PR #20: `https://github.com/peteryang1/coding_agent_playground/pull/20`.
- PR #20 PM gate passed and dev_2 self-merged it:
  - `mergedAt`: `2026-05-20T10:02:28Z`
  - merge commit: `3bfcb3781931070b932d138957620dbe9f1d2ee9`
- PR #21 backfilled PR #20 merge facts into durable task files:
  - `mergedAt`: `2026-05-20T10:05:06Z`
  - merge commit: `36ee08ae3ad98f7a94b7c5c7155938479333bd37`
- dev_2 did not run SFT and did not peer-send PM routine status.

## 2026-05-20 Session 12 Dev 2 GPU Retry Submit

- Task id: `M1-GPU-RETRY-SUBMIT-DEV2`.
- Owner: `intern_code_dev_2`.
- PM assignment: submit or explicitly block a fresh LTP H200 job for SFT retry using the merged resource plan; do not run SFT.
- dev_2 action:
  - confirmed previous Milestone 1 frame `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130` remained `STOPPED / Completed` with completed timestamp `2026-05-20 09:53:21`;
  - submitted fresh single-node `h200agentic` LTP worker `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z`;
  - first JSON submit attempt for `...T110520Z` failed with LTP API `HTTP 400 InvalidProtocolError` and created no job;
  - successful YAML submit returned status `202`;
  - LTP state became `RUNNING / AttemptRunning`, submitted `2026-05-20 11:06:15`, started `2026-05-20 11:06:20`;
  - endpoint: `ssh -p 23121 root@10.100.22.53`;
  - node: `lg-cmc-b7r202-r05u16-h200-000747`;
  - verified 8 x NVIDIA H200 idle at 0% utilization and about 1 MiB used per GPU, no compute processes, `/mnt/cephfs` as `fuse.ceph-fuse`, and writable output root.
- Staging:
  - copied `/root/workspace/coding_agent_playground` and `/root/workspace/cleaned_m1_sft_10` from corrected final workspace to retry GPU node;
  - wrote `/root/workspace/coding_agent_playground/nodes.json`;
  - wrote `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_retry_nodes.json`.
- Stop/lifecycle:
  - expected review time: `2026-05-20T12:06:20Z` unless PM records a bounded extension;
  - stop conditions recorded in `evidence/gpu_retry_resource_tracking.md`;
  - final stop proof is pending while the retry resource remains active.
- Durable evidence:
  - `evidence/dev_2_gpu_retry_submit.md`;
  - `evidence/gpu_retry_resource_tracking.md`;
  - `workspace/interns/intern_code_dev_2/status.md`.
- dev_2 did not run SFT and did not peer-send PM routine status.

## 2026-05-20 Session 12 Dev 2 GPU Retry Stop Completion

- Task id: `M1-GPU-RETRY-SUBMIT-DEV2`.
- Owner: `intern_code_dev_2`.
- PM stop order input:
  - dev_4 one authorized SFT retry finished with `EXIT_STATUS=1`;
  - no checkpoint/model/trainer_state/all_results were produced;
  - failure was `KeyError: 'from'` during LLamaFactory dataset conversion;
  - dev_4 recommended stopping immediately.
- Pre-stop state:
  - frame `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z`;
  - endpoint `ssh -p 23121 root@10.100.22.53`;
  - LTP state `RUNNING / AttemptRunning`;
  - GPUs idle at 0% utilization and about 1 MiB memory used;
  - latest retry run id `milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z`;
  - retry artifacts visible under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/`.
- dev_2 stop action:
  - sent `ltp.py stop xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z` at 2026-05-20T11:22Z;
  - stop command returned status `202`.
- Stop proof:
  - LTP state reached `STOPPED (Completed)`;
  - completed timestamp: `2026-05-20 11:23:29`;
  - endpoint proof: `ssh -p 23121 root@10.100.22.53` refused connection after stop;
  - repeated post-stop polls through 2026-05-20T11:24:48Z remained `STOPPED (Completed)`.
- Artifact preservation:
  - outputs preserved under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`;
  - stop action released compute only and did not delete `/mnt/3fs` artifacts.
- Durable evidence:
  - `evidence/dev_2_gpu_retry_submit.md`;
  - `evidence/gpu_retry_resource_tracking.md`;
  - `task_registry.md`;
  - `workspace/interns/intern_code_dev_2/status.md`.
- dev_2 did not run SFT and did not peer-send PM routine status.

## 2026-05-20 Session 12 PM Gate Sync After PR #20/#21

- PM gate state: GPU lifecycle resource blocker is closed. The active 8xH200 LTP frame `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130` reached `STOPPED (Completed)` and the SSH endpoint refused connection after stop.
- PM gate state: PR #18 remains open and not ready. It now has task id `M1-SFT-SMOKE-DEV4` in the PR body, but GitHub still reports `CONFLICTING` / `DIRTY` after PR #20/#21 advanced `main`.
- PM action: dev_4 is already resolving PR #18 against current `origin/main`, preserving PM task registry and dev_2 stop-proof records. PM will gate PR #18 only after GitHub reports it mergeable.
- PM decision: no new GPU retry is authorized from the failed SFT attempts. Any additional SFT retry requires a new explicit task/PR gate with a concrete MCA/Megatron tiny-data config fix plan and resource plan.

## 2026-05-20 Session 12 Task-Flow Reaffirmation

- Supervisor task-flow requirement re-applied to running PM policy: PM must create/maintain explicit tasks before dev/test PR work, and each dev/test PR must map to a task with owner, acceptance criteria, durable evidence path, and completion marker.
- PM gate rule: a dev/test PR cannot pass until the task mapping exists and GitHub reports the PR ready/mergeable. Ready PRs that pass PM gate are self-merged by their owner immediately, without waiting for the whole milestone.
- Owner post-merge rule: after self-merge, the PR owner marks the matching task complete or blocked-with-final-evidence in task docs or `task_registry.md`, updates own `status.md`, updates necessary history/evidence, and merges/pushes that completion record.
- PM refreshed `task_registry.md`: `M1-TASK-PR-GATE-PM` is complete via PR #19/#22, and PR #18 references `M1-SFT-SMOKE-DEV4`.
- PM notified all six dev/test panes by tmux inject that dev/test PRs must follow task -> PR -> merge -> task completion flow; capture-pane showed the messages in each pane, and PM sent actual `C-m` after an initial literal-Enter submission issue.

## Session 16 - Dev 4 PR #18 Refresh After PR #22 Gate Sync - 2026-05-20

- PM gate update: after PM PR #22 merged, GitHub reported PR #18 `CONFLICTING` / `DIRTY` again.
- Dev_4 merged latest `origin/main` into branch `intern_code_dev_4/session12-sft-smoke-run`.
- Conflict file:
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`
- Resolution:
  - preserved `M1-SFT-SMOKE-DEV4` SFT smoke task mapping and evidence facts;
  - preserved `M1-GPU-LIFECYCLE-DEV2` completion, PR #20 merge, PR #21 backfill, and PM PR #22 gate sync facts;
  - kept the PM decision that no further SFT GPU retry is authorized without a new explicit task and config/resource plan.
- No self-merge was attempted; PR #18 remains waiting for GitHub mergeability and PM gate pass.

## Session 17 - Dev 4 Task-Flow Rule Receipt For PR #18 - 2026-05-20

- PM task-flow rule update received: every dev/test PR must map to an explicit task with owner, acceptance criteria, durable evidence path, and completion marker.
- PR #18 task id remains `M1-SFT-SMOKE-DEV4`.
- Durable mapping locations:
  - PR #18 body;
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`;
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_smoke_run.md`;
  - `workspace/interns/intern_code_dev_4/status.md`.
- Current PR #18 gate state: GitHub reports open, non-draft, `MERGEABLE` / `CLEAN`.
- Dev_4 did not self-merge because this update restates the flow and says to wait for PM gate; owner self-merge remains pending PM gate pass.
- Required post-merge action after PM gate pass and self-merge: mark `M1-SFT-SMOKE-DEV4` complete or blocked-with-final-evidence with `mergedAt` and merge commit in task docs/task registry, then update status/history/evidence and push/merge that completion record.

## Session 18 - Dev 4 PR #18 PM Gate Pass And Owner Merge - 2026-05-20

- PM gate pass received for PR #18 / task `M1-SFT-SMOKE-DEV4`.
- Gate facts: PR body cites task id, owner, acceptance criteria, durable evidence path, and completion marker; GitHub reports `MERGEABLE` / `CLEAN`; no required checks are reported.
- Dev_4 recorded this gate pass durably before owner self-merge.
- Planned completion state after PR #18 merge: `M1-SFT-SMOKE-DEV4` will be marked blocked-with-final-evidence because the SFT smoke was attempted under the approved route and produced final failure evidence without checkpoint/model output.
- Owner self-merge completed:
  - PR: `https://github.com/peteryang1/coding_agent_playground/pull/18`
  - `mergedAt`: `2026-05-20T10:18:04Z`
  - merge commit: `1c3a3e23921dd3fc91b340f9b67f83c747d42948`
- Completion record: task `M1-SFT-SMOKE-DEV4` marked blocked-with-final-evidence because the approved SFT smoke reached real launch/failure evidence but produced no checkpoint/model, `trainer_state.json`, or `all_results.json`.
- No peer-send PM routine confirmation was used.

## Session 19 - Dev 4 SFT Config Fix Package - 2026-05-20

- Task accepted: `M1-SFT-CONFIG-FIX-DEV4`.
- Owner: `intern_code_dev_4`.
- Scope: produce the next SFT unblock package after `M1-SFT-SMOKE-DEV4` blocked-with-final-evidence; no GPU run authorized.
- Evidence created:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_config_fix_plan.md`
- Config patch created:
  - `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`
- PR opened:
  - `https://github.com/peteryang1/coding_agent_playground/pull/26`
- Plan summary:
  - use TP=8 / DP=1 to avoid MCA/drop-last zero-step behavior on 10 examples;
  - use `max_steps: 2` plus `warmup_steps: 0` to avoid the Megatron one-step scheduler assertion;
  - use `save_steps: 1` so a successful smoke can produce immediate checkpoint/model evidence.
- No GPU run was attempted. Fresh execution requires PM gate plus test/resource plans.

## 2026-05-20 Session 19 Next Blocker Task Split

- PM audited current state after PR #18/#23/#24 merged: no open PRs, GPU released, SFT smoke blocked-with-final-evidence, and mini-swe blocked by absent checkpoint/endpoint.
- PM decision: do not authorize another GPU run from the failed DP=8 and TP=8 attempts without a new task-attached config/data/test/resource package.
- Created next explicit tasks in `task_registry.md`:
  - `M1-SFT-CONFIG-FIX-DEV4`;
  - `M1-SFT-DATA-MITIGATION-DEV3`;
  - `M1-GPU-RETRY-RESOURCE-DEV2`;
  - `M1-SFT-RETRY-GATE-TEST1`;
  - `M1-EVAL-BLOCKED-TEST2`;
  - `M1-SFT-FAILURE-REVIEW-DEV1`.
- PM delivered these task assignments by tmux inject to `intern_code_dev_1`, `intern_code_dev_2`, `intern_code_dev_3`, `intern_code_dev_4`, `intern_code_test_1`, and `intern_code_test_2`; `capture-pane` verified each pane showed the submitted task text.
- PM remains within role boundary: task assignment, gate, durable evidence collection, and decisions only.

## 2026-05-20 Session 12 Conduct Reaffirmation And PR Audit

- Supervisor required PM and all interns to follow the intern conduct rule using explicit tasks, not scattered assignments. PM updated durable task/PR gate records so every dev/test PR must map to a task id, owner, acceptance criteria, evidence path, and completion marker before PM marks it ready.
- PM delivered the task -> PR -> merge -> task-complete rule to all six dev/test panes by tmux inject and capture-pane verification. The notification instructed owners to write confirmations, status, blockers, and completion proof to durable files rather than peer-send PM.
- PR #26 for `M1-SFT-CONFIG-FIX-DEV4` and PR #27 completion record are merged; latest open-PR audit returned no open PRs. PM gate now focuses on whether support evidence is merged and whether a fresh GPU retry task can be authorized without PM running experiments.

## Session 20 - Dev 4 PR #26 Config Fix Package Merge - 2026-05-20

- PM gate pass received for PR #26 / task `M1-SFT-CONFIG-FIX-DEV4`.
- Gate facts: PR body cites task id, owner, acceptance criteria, durable evidence, and completion marker; GitHub reports `MERGEABLE` / `CLEAN`; no required checks are reported.
- Dev_4 self-merged PR #26:
  - PR: `https://github.com/peteryang1/coding_agent_playground/pull/26`
  - `mergedAt`: `2026-05-20T10:44:55Z`
  - merge commit: `6a704f842c992f83a8d86167dfe870fa6ff72440`
- Completion state: `M1-SFT-CONFIG-FIX-DEV4` is ready-for-retry. The config package is landed and durable, but no GPU run is authorized until PM also gates test/resource plans.
- No peer-send PM routine confirmation was used.

## 2026-05-20 Session 12 SFT Retry Authorization Split

- PM self-merged coordination PR #28 after it passed gate: non-draft, `MERGEABLE` / `CLEAN`, no required checks. Merge commit `d6d1092b8cf72eb6210502da0b058cd9bf9abab6`.
- PM decision: support evidence is durable enough to authorize the next owner-executed retry path through explicit tasks. PM will not run LTP, SFT, eval, or GPU stop commands.
- New task split: dev_2 fresh LTP submit/lifecycle, dev_4 one SFT retry after endpoint exists, dev_3 data gate, dev_1 pre-run package sanity check, test_1 retry validation, and test_2 mini-swe unblock readiness.
- First retry defaults: config `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`; data `/root/workspace/cleaned_m1_sft_10/train.jsonl`; repeated x16 data remains fallback/supporting evidence only.

## Session 21 - Dev 4 SFT Retry Run Assignment Receipt - 2026-05-20

- Task accepted: `M1-SFT-RETRY-RUN-DEV4`.
- Owner: `intern_code_dev_4`.
- Scope: run exactly one Qwen3-8B SFT retry only after dev_2 provides a fresh endpoint/node.
- Durable evidence created:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_retry_run.md`
- PR opened:
  - `https://github.com/peteryang1/coding_agent_playground/pull/30`
- Current status: blocked before execution.
- Blockers:
  - at Session 21 receipt time, no `evidence/dev_2_gpu_retry_submit.md` was present in the dev_4 worktree;
  - at Session 21 receipt time, `M1-GPU-RETRY-SUBMIT-DEV2` had no visible fresh endpoint evidence in the dev_4 worktree;
  - Session 22 superseded the auth fact: `M1-SFT-RETRY-AUTH-PM` is complete via PR #29.
  - prior endpoint `ssh -p 39314 root@10.100.20.37` is released and must not be reused.
- Planned retry command uses `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml` and PM-approved original data `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- No GPU run was attempted and no peer-send PM routine status was used.

## 2026-05-20 Session 12 Retry Resource Handoff

- PM collected owner durable evidence from dev_1/dev_2/dev_3/test_1/test_2 for the retry gate.
- PM gate result: config/data/base/test/resource planning are sufficient for dev_4 to run exactly one retry after consuming dev_2's fresh endpoint evidence.
- Active resource: `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z`, endpoint `ssh -p 23121 root@10.100.22.53`, node `lg-cmc-b7r202-r05u16-h200-000747`, hard review `2026-05-20T12:06:20Z`.
- PM notified dev_4 by tmux inject with endpoint, node, frame, staged repo/data/nodes facts, and no-extra-retry rule.
- PR #30 was not PM-gate-ready until dev_4 corrected stale PR facts from before PR #29 and updated evidence for the current dev_2 endpoint handoff.

## Session 22 - Dev 4 SFT Retry Execution - 2026-05-20

- Task: `M1-SFT-RETRY-RUN-DEV4`.
- PM gate correction applied: `M1-SFT-RETRY-AUTH-PM` is complete via PR #29, `mergedAt=2026-05-20T11:02:32Z`, merge commit `c14fa045b210a74fc243f2d2690a2523cc7ec2db`.
- PM provided fresh dev_2 endpoint evidence in durable PM paths:
  - `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_gpu_retry_submit.md`
  - `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_retry_resource_tracking.md`
- Endpoint used:
  - `ssh -p 23121 root@10.100.22.53`
  - node `lg-cmc-b7r202-r05u16-h200-000747`
  - frame `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z`
- Pre-run gate passed after remote staging repair:
  - 8 x H200 visible and idle;
  - original dataset `/root/workspace/cleaned_m1_sft_10/train.jsonl` sha256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`, 10 rows, schema `coding_agent_playground_sft_v1`;
  - clean base `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` passed Qwen3 config checks;
  - config `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml` passed TP=8/max_steps=2/warmup_steps=0 checks;
  - LLamaFactory 0.9.5.dev0, `flash_attn`, and `mcore_adapter` were available.
- Exactly one retry was launched:
  - run id `milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z`;
  - command used `CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`, `DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl`, `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`, `OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`, `LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory`, `DRY_RUN=0`.
- Result:
  - exit status `1`;
  - manifest, runtime config, log, and exit status file are present under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/`;
  - no checkpoint/model, `trainer_state.json`, or `all_results.json` exists under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/`.
- Failure signature:
  - `KeyError: 'from'` in `LLamaFactory/src/llamafactory/data/converter.py` while converting dataset rows;
  - current blocker is data registration/format mapping because the JSONL uses OpenAI-style role/content messages while the runtime registration used ShareGPT defaults expecting `from`/`value`.
- Post-run resource state: GPUs returned to 1 MiB memory used and 0% utilization; no active torchrun/LLamaFactory workload was visible. Endpoint recheck at `2026-05-20T11:23:57Z` refused SSH.
- Resource recommendation: dev_2 should stop the active H200 resource immediately if it is not already stopped. No extra retry is authorized without a new PM gate.
- Durable evidence updated:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_retry_run.md`
  - `workspace/interns/intern_code_dev_4/status.md`
- PR #30 branch refresh: latest `origin/main` was merged after main advanced through retry handoff/support evidence. Conflicts in `history_log.md`, `task_knowledge.md`, and `task_registry.md` were resolved by preserving PM/dev_1/dev_2/dev_3/test_1/test_2 records and dev_4 Session 22 retry result evidence.

## 2026-05-20 Session 12 Retry Failure And Resource Stop

- Dev_4's one authorized retry reached LLamaFactory distributed launch and failed before checkpoint creation with `KeyError: 'from'` during dataset conversion.
- The prior DP=8 `steps_in_epoch=0` and TP=8 one-step scheduler assertion were not the failure signatures for this retry; the current blocker is OpenAI-style `role`/`content` data being registered with ShareGPT defaults expecting `from`/`value`.
- PM sent a stop order to dev_2 after dev_4 recommended immediate resource release and no further retry was authorized.
- Dev_2 stopped LTP frame `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z`; final state is `STOPPED (Completed)`, completed `2026-05-20 11:23:29`, endpoint refused connection, and `/mnt/3fs` artifacts were preserved.
- PM gate for PR #30: not ready while GitHub reports `CONFLICTING` / `DIRTY`; dev_4 must merge current main and preserve both dev_2 stop proof and retry result evidence.

## Session 23 - Dev 4 PR #30 Stop-Proof Conflict Refresh - 2026-05-20

- Task: `M1-SFT-RETRY-RUN-DEV4`.
- PM gate update received: PR #30 remained not ready because PR #32 stop-proof main commit `5afb945bbfd97faca7af3e56b0765baa48632aa1` landed after the prior PR #30 branch merge.
- Branch action: fetched and merged latest `origin/main` into `intern_code_dev_4/M1-SFT-RETRY-RUN-DEV4`.
- Conflict files:
  - `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- Resolution:
  - preserved dev_2 final stop proof from main: frame `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z`, final state `STOPPED (Completed)`, completed `2026-05-20 11:23:29`, endpoint refused connection, `/mnt/3fs` outputs preserved, dev_2 did not run SFT;
  - preserved dev_4 retry result evidence: run id `milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z`, exit status `1`, `KeyError: 'from'`, no checkpoint/model, no `trainer_state.json`, no `all_results.json`;
  - kept PR #30 mapped to task `M1-SFT-RETRY-RUN-DEV4` with owner `intern_code_dev_4`, durable evidence path `evidence/dev_4_sft_retry_run.md`, and blocked-with-final-evidence completion marker pending PR merge.
- No SFT retry or extra GPU command was run in Session 23.
- PR #30 remains open for PM gate after push; dev_4 must not self-merge until PM gate says ready.

## Session 24 - Dev 4 PR #30 Archival Cleanup - 2026-05-21

- Task: `M1-S21-PR30-CLEANUP-DEV4`.
- PM Session 21 replacement task reclassified PR #30 as archival cleanup rather than the checkpoint critical path.
- Owner action chosen: close/supersede PR #30 instead of refreshing it against current main again.
- PR closure:
  - PR: `https://github.com/peteryang1/coding_agent_playground/pull/30`
  - `closedAt`: `2026-05-21T07:23:06Z`
  - `mergedAt`: `null`
  - closure comment: `https://github.com/peteryang1/coding_agent_playground/pull/30#issuecomment-4505715612`
- Durable cleanup evidence:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s21_pr30_cleanup.md`
  - `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s21_pr30_cleanup.md`
- Preserved retry facts:
  - run id `milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z`;
  - exit status `1`;
  - failure `KeyError: 'from'` during LLamaFactory dataset conversion;
  - no checkpoint/model, no `trainer_state.json`, no `all_results.json`;
  - no extra retry was launched.
- Preserved stop proof:
  - frame `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z`;
  - LTP final state `STOPPED (Completed)`;
  - completed `2026-05-20 11:23:29`;
  - endpoint refused connection after stop;
  - `/mnt/3fs` artifacts preserved.
- Replacement path: Session 21 replacement/runtime tasks own any future launch package and runtime. This cleanup task does not authorize SFT/GPU work.

## Session 25 - Dev 4 ENOSPC Config Fix Package - 2026-05-21

- Accepted task `M1-S21-ENOSPC-CONFIG-FIX-DEV4`.
- Reviewed Session 21 final runtime blocker from run `milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_20260521T073106Z`: ShareGPT conversion reached 10/10 and training reached step 1/2, then checkpoint save failed with `safetensors_rust.SafetensorError` / `No space left on device (os error 28)`.
- Recorded that `checkpoint-1` is partial only and must not be handed to eval; no complete checkpoint/model, `trainer_state.json`, or `all_results.json` exists for that failed run.
- Wrote no-execution fix evidence to `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s21_enospc_config_fix.md` and the PM durable path.
- Primary recommendation: keep `coding_agent_m1_sft_10_sharegpt`, use a fresh capacity-verified output/checkpoint path, and change the retry template from step-1 checkpointing to `save_steps: 2` with `save_total_limit: 1` for the `max_steps: 2` smoke so it targets one complete eval-usable final checkpoint/model.
- Cited files/PR scope if PM requests a code/config PR: add `configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml`, harden `scripts/train_qwen3_8b_sft.sh` to rewrite `dataset:` from `DATASET_NAME`, and update `scripts/write_sft_run_manifest.py` to record runtime save strategy from the generated config.
- No SFT/GPU/eval command was run.

## Session 26 - Dev 4 ENOSPC Storage Rule Refresh - 2026-05-21

- Applied supervisor storage rule to task `M1-S21-ENOSPC-CONFIG-FIX-DEV4`.
- Updated `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s21_enospc_config_fix.md` and the PM durable copy.
- Superseded the prior future output-root recommendation `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.
- Current recommendation: future SFT launch outputs, logs, checkpoints, run metadata, temporary converted datasets, and intermediates default under CephFS `/home/xu.yang/coding_agent_playground/outputs`.
- Required-path exceptions documented in evidence:
  - clean base model remains `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` because it is an existing PM-selected input path;
  - historical failed-run `/mnt/3fs` run/checkpoint paths remain audit evidence only and must not be reused for future outputs.
- Refreshed command and capacity-probe templates to target `/home/xu.yang`.
- No SFT/GPU/eval command was run.

## Session 27 - Dev 4 Session 22 Early-Exit Fix Package - 2026-05-21

- Accepted task `M1-S22-EARLY-EXIT-FIX-DEV4`.
- Reviewed dev_2 Session 22 evidence `evidence/dev_2_s22_enospc_retry_runtime.md` and `evidence/gpu_s22_enospc_retry_tracking.md`.
- Runtime facts reviewed: run `milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z` used `/home/xu.yang/coding_agent_playground/outputs`, preserved `coding_agent_m1_sft_10_sharegpt`, passed 24GiB CephFS capacity probe, then exited `EXIT_STATUS=1` with log content only `START_UTC=2026-05-21T08:27:52Z`.
- Diagnostic conclusion: because `scripts/train_qwen3_8b_sft.sh` should create the run config and run_manifest before dataset/GPU/LLamaFactory checks, the absence of run_manifest/runtime config/checkpoint artifacts means the failure happened before or inside the wrapper prelude, and durable stderr/stdout capture started too late or the script was not reached.
- Wrote no-execution evidence to `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_early_exit_fix.md` and the PM durable path.
- Proposed fix scope: patch `scripts/train_qwen3_8b_sft.sh` to own first-line durable logging under `/home/xu.yang`, add xtrace and ERR/EXIT diagnostics, write preflight proof before training, preserve `DATASET_NAME=coding_agent_m1_sft_10_sharegpt`, and avoid direct `exec` of `llamafactory-cli` so traps can record trainer status.
- Also proposed `scripts/write_sft_run_manifest.py` manifest hardening to record actual runtime save policy and preflight fields rather than stale static checkpoint policy.
- No SFT/GPU/eval command was run.
