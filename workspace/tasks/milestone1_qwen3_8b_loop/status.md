# Milestone 1 Status

<!-- METADATA:STATUS=Open,OWNER=intern_code_pm -->

## 2026-05-20

- PM accepted supervisor Milestone 1 and durable-channel correction.
- Final workspace SSH verified: `ssh -p 31787 root@10.100.194.40`.
- Final workspace root verified/created: `/root/workspace`.
- Selected initial repos: `fastapi/fastapi`, `scikit-learn/scikit-learn`, `Textualize/rich`.
- Created durable task tracking directory.
- PM active goal tool blocker recorded: cannot create a second goal in this thread after previous goal completed.
- Final workspace clones completed:
  - `/root/workspace/fastapi` at `f4cafbc`.
  - `/root/workspace/scikit-learn` at `ffc6cdc`.
  - `/root/workspace/rich` at `46cebbb`.
- PM assigned all 6 dev/test interns with durable evidence paths in `assignments.md`; no routine peer-send reply was requested.
- Remote rollout harness dry-run exists under `/root/workspace/rollouts_smoke` with one dry-run trajectory for each selected repo.
- Remote rollout harness preflight passes when using `CODEX_CMD=/mnt/3fs/data/tools/codex`.
- PM routed a durable follow-up assignment for `intern_code_test_1` to validate the current rollout harness dry-run artifacts.
- PM applied the secretary durable-reporting correction: PM will not proactively peer-send secretary for routine milestone reports/status/blockers/summaries/completion; secretary-facing updates live in durable task files.
- `intern_code_test_1` completed follow-up validation of the dev_2 rollout harness dry-run. Passing checks include JSONL parsing, per-repo dry-run directories, parseable metadata/done files, prompt matching, repo metadata capture, and partial resume evidence.
- PM routed a durable follow-up for `intern_code_dev_2` to close the rollout harness gate before full 300-trajectory execution.
- PR status: dev_4 SFT pipeline PR #1 is open/mergeable; PM coordination PR #2 is open/mergeable.
- Dev_2's rollout harness v2 is present in PM worktree and deployed to the final workspace; PM verified `/root/workspace/rollouts_smoke_v2` has full dry-run artifacts and schema fields that reconcile with `manifest.jsonl`.
- Session 3 address correction completed: the authoritative final workspace is `ssh -p 31787 root@10.100.194.40`; previous scratch-host outputs are not final evidence.
- Corrected final workspace verified hostname `lg-cmc-b7r201-k10u23-cpu-000158`, clean repos, `/usr/local/bin/codex`, `codex-cli 0.130.0`, and `~/.codex/auth.json`.
- Harness deployed to `/root/workspace/rollout_harness` on the corrected final workspace; preflight passed for all three selected repos and dry-run smoke exists under `/root/workspace/rollouts_smoke_v3`.
- PM ran one real tiny non-dry rollout through the harness on the corrected final workspace. It passed for `fastapi/fastapi`, wrote full raw artifacts under `/root/workspace/rollouts_nondry_new_machine_tiny`, and repo working trees remained clean.
- PM top priority updated: all six dev/test interns have active non-waiting assignments with durable evidence paths; idle owner areas are treated as PM coordination risk.
- PM generated `/root/workspace/rollout_harness/tasks_300.jsonl` on the corrected final workspace with 300 records, exactly 100 per selected repo.
- PM started full 300-trajectory rollout in the background: PID file `/root/workspace/rollout_harness/rollouts_m1_300.pid`, log `/root/workspace/rollout_harness/rollouts_m1_300.log`, output root `/root/workspace/rollouts_m1_300`.
- Latest PM snapshot after launch: rollout PID `1208139` is alive, `/root/workspace/rollouts_m1_300/manifest.jsonl` has 1 line, and the first `fastapi` trajectory is `passed`.
- PM attempted a fresh six-intern assignment fanout for this all-hands priority; peer channel returned `undeliverable: unconfirmed` for all six, so durable files remain the authoritative coordination channel.
- PM observed the remote `tasks_300.jsonl` was upgraded to full repo ID records with `repo_key`; launcher prepare now accepts slug, full repo ID, or `repo_key`.
- PM started separate parallel scikit-learn and rich rollout batches to avoid waiting behind the sequential main process:
  - scikit-learn PID `1270557`, output root `/root/workspace/rollouts_m1_300_scikit_learn`;
  - rich PID `1270562`, output root `/root/workspace/rollouts_m1_300_rich`.
- Latest rollout snapshot: main PID `1208139` alive with 3 passed FastAPI trajectories; scikit-learn and rich PIDs alive with no manifest entries yet.
- PM added/deployed `convert_rollouts_to_sft.py` and ran a cleaning smoke over `/root/workspace/rollouts_m1_300`; output `/root/workspace/cleaned_m1_sft_smoke/train.jsonl` has 3 valid `coding_agent_playground_sft_v1` examples, 0 rejects, 0 conversion errors.
- Updated live conversion after parallel roots produced artifacts: `/root/workspace/cleaned_m1_sft_live/train.jsonl` has 7 valid examples with per-repo counts `fastapi=4`, `scikit-learn=2`, `rich=1`, all `success`, 0 conversion errors.
- Session 4 scope change applied: Milestone 1 is now an end-to-end smoke loop with 10 total trajectories, not a full 300-result run.
- PM stopped/superseded old 300/100-per-repo rollout processes. Known old parent PIDs `1208139`, `1270557`, `1270562` and observed codex children are dead; old roots `/root/workspace/rollouts_m1_300*` are scratch-only.
- PM wrote scratch markers on the final workspace: `/root/workspace/rollout_harness/STOPPED_OLD_300_ROLLOUTS_AT.txt` and `/root/workspace/rollout_harness/OLD_300_OUTPUTS_SCRATCH_ONLY.txt`.
- PM created `/root/workspace/rollout_harness/tasks_m1_10.jsonl` with exactly 10 total prompts: `fastapi=4`, `scikit-learn=3`, `rich=3`; every prompt requires actual edit/patch attempt and test/check attempt.
- PM deployed `validate_complete_coding_trajectories.py` and started the real non-dry 10-total rollout: PID `1341184`, log `/root/workspace/rollout_harness/rollouts_m1_10.log`, output root `/root/workspace/rollouts_m1_10`.
- Latest Session 4 validation snapshot: `/root/workspace/rollouts_m1_10` has 4 manifest entries, rollout PID `1341184` is alive, and `complete_process_validation.json` reports 4 checked / 4 valid / 0 invalid complete-process trajectories.
- Session 5 completion snapshot: `/root/workspace/rollouts_m1_10` finished with 10 manifest entries; complete-process validator reports 10 checked / 10 valid / 0 invalid; `/root/workspace/cleaned_m1_sft_10/train.jsonl` has 10 kept SFT examples, 0 rejects, 0 conversion errors, split `fastapi=4`, `scikit-learn=3`, `rich=3`.
- PM used high-priority `/esc` interrupts for dev/test. `/esc` delivered to dev_1/dev_2/dev_3/dev_4/test_1/test_2; follow-up durable assignment messages were delivered to dev_3/test_1/test_2, dev_1 was unconfirmed, and dev_2/dev_4 remained busy, so `assignments.md` remains the authoritative control plane.
- Dev_4 durable evidence now includes Qwen3-8B SFT dry-run command validation using `/root/workspace/cleaned_m1_sft_10/train.jsonl`; run manifest was written under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/`.
- Test_2 durable evidence now includes mini-swe-agent eval smoke readiness and exact two-instance/single-instance commands using Singularity, blocked only on the SFT smoke model/checkpoint or endpoint.
- PM wrote mini-swe-agent machine-readable readiness metrics to `/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json`; status is `blocked` because no SFT smoke model/checkpoint or endpoint exists yet.
- PM updated `final_report.md` from pending placeholders to current evidence: 10/10 rollout valid, 10/10 cleaned, SFT dry-run manifest path, mini-swe readiness metrics, and remaining blockers.
- PM re-audited SFT real-launch blockers before the Session 6 role correction: corrected final workspace still has no `nvidia-smi`; no current Milestone 1 `nodes.json` exists; `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` remains a broken symlink; readable historical Qwen3-8B checkpoints exist but are warm-start candidates, not a clean base unless explicitly accepted.
- Session 6 PM role correction applied: PM now only assigns, gates, collects information, and decides. PM will not directly execute further remote workspace code, code changes, SFT/GPU probing, or mini-swe-agent eval; assigned dev/test owners must execute and record durable evidence.
- Session 6 activation update: dev_3/test_1 received peer assignments; dev_1/dev_2/dev_4/test_2 required `/esc` plus tmux direct assignment because normal peer delivery stayed busy/unconfirmed. `assignments.md` is the authoritative source for all six owners and evidence paths.
- Session 7 notification-channel change applied: PM -> dev/test task/correction messages now default to tmux injection plus Enter and `capture-pane` verification. `peer_send` is not the primary channel; interrupts are reserved for supervisor-explicit urgent cases or active resource-waste/error-continuation cases.
- Session 7 continuation gate: PM inspected dev_4/test_2 durable evidence and judged SFT/eval smoke still incomplete. Dev_4 must produce the base/checkpoint/GPU decision package; test_2 must produce the checkpoint/endpoint eval gate package. Both assignments were delivered by non-interrupt tmux inject and verified with `capture-pane`.
- Session 7 continuation parallelization: dev_4/test_2 have not yet produced new decision/gate packages. PM assigned dev_1 to collect clean-base candidate evidence, dev_2 to collect GPU/current `nodes.json` evidence, and test_1 to define the SFT+mini-swe completion gate. All were delivered by non-interrupt tmux inject and verified with `capture-pane`.
- Latest PM gate check: support evidence files from dev_1/dev_2/test_1 are not present yet, and dev_4/test_2 evidence still lacks the requested decision/gate package. Real SFT smoke and mini-swe eval smoke remain unproven.
- Session 8 PR gate correction applied: PR #1 is open/non-draft/mergeable and passes PM gate for its scoped SFT pipeline artifacts; PM notified dev_4 by non-interrupt tmux inject to self-merge. PR #2 was not gate-ready at initial audit because mergeability was `UNKNOWN` and PM durable updates were still local.
- Session 8 PR recheck after push: PR #1 remains open/mergeable and awaits dev_4 owner self-merge; PR #2 remains open with mergeability `UNKNOWN`, so PM-owned PR #2 remains blocked from self-merge.
- Session 8 PR #2 gate update: PR #2 mergeability resolved to `MERGEABLE`; PM gate passes for the coordination/evidence scope, and PM will self-merge PR #2 as owner after pushing this durable record.

## Next PM Checks

- Gate dev_4's durable SFT/GPU/model-path decision package and decide whether clean-base repair/location is available or explicit warm-start fallback should be escalated.
- Gate test_2's durable mini-swe-agent smoke gate package, then require real smoke evidence after dev_4 provides a usable model/checkpoint path or endpoint.
- Gate dev_1/dev_2/test_1 support evidence to decide whether PM can accept a warm-start fallback, needs compute-manager routing, or must escalate to supervisor for base/GPU decision.
- Recheck PR #1 merge result from dev_4 durable status/evidence and re-audit PR #2 mergeability after current PM updates are pushed.
- After PR #2 merge, continue milestone coordination from fresh state while keeping the active goal open for SFT/eval smoke blockers.
