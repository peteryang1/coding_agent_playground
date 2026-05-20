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
- Session 8 continuation after PR #2 merge: PR #2 merged at `2026-05-20T07:51:54Z` with merge commit `07b0dd167b9004af1c6994652966b7e1de5f2084`; ongoing PM coordination moved to branch `pm/milestone1-continuation-20260520`.
- Latest PR/evidence gate: PR #1 remains open/mergeable and awaits dev_4 self-merge; dev_1/dev_2/test_1 support evidence files are still missing, so PM sent non-interrupt tmux reminders and verified with `capture-pane`.
- Continuation PR #3 is open/non-draft/mergeable and passes PM gate for coordination-only durable updates; PM will self-merge as owner after pushing this record.
- PR #3 merged at `2026-05-20T07:58:02Z` with merge commit `ba058d3a87831630c232edbe6d8622b1b648ed54`.
- Latest PM gate check: PR #1 remains open/mergeable and awaits dev_4 owner self-merge; dev_1/dev_2/test_1 support files remain missing; dev_4/test_2 decision packages remain absent; SFT/eval smoke remains unproven.
- Dev_4 self-merged PR #1 for scoped Qwen3-8B SFT pipeline artifacts at `2026-05-20T08:23:54Z`; merge commit `882d1642884e82d1a40674266f244a52cf69defc`.
- Dev_4 Session 8 decision package is recorded in `evidence/dev_4_sft_pipeline.md`: clean Qwen3-8B base path is still missing/broken on the corrected final workspace; warm-start fallback is recommended only with PM/supervisor approval using `/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-final`; GPU endpoint/current `nodes.json` remains required before real SFT smoke.
- Dev_2 GPU/nodes support evidence is recorded in `evidence/dev_2_gpu_nodes_support.md`: corrected entry host has no visible GPU and there is no current Milestone 1 `nodes.json`; SFT launch requires a new GPU allocation or explicit historical allocation reuse approval.
- Dev_3 SFT input handoff is recorded in `evidence/dev_3_sft_input_handoff.md`: `/root/workspace/cleaned_m1_sft_10/train.jsonl` is the current data contract for dev_4, format `coding_agent_playground_sft_v1`, 10 examples, SHA-256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`.
- Dev_1 base-path support evidence is recorded in `evidence/dev_1_sft_base_path_support.md`: PM accepts `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` as the preferred local clean-base candidate for the next SFT smoke, while `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` remains a broken alias.
- PR #8 merged at `2026-05-20T08:33:38Z` with merge commit `97cff0dddfb460585b62193b4f567470b047ffd5`; this recorded PR #1 merge plus dev_1/dev_2/dev_3/dev_4 SFT support evidence.
- Current incomplete gates: test_1 completion audit file is missing, test_2 eval acceptance/provenance package is stale, GPU/current `nodes.json` is missing, and no real SFT/eval output exists.
- PR #9 merged at `2026-05-20T08:39:36Z` with merge commit `e876c755d92f8c39fc862daaec8ac7968dfac845`; after a waiting recheck, test_1/test_2/dev_4 required-now artifacts are still missing or stale.
- Dev_4 Session 9 SFT smoke launch package is recorded in `evidence/dev_4_sft_pipeline.md`: PM decision now uses dev_1 clean-base candidate `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`; dev_4 verified this path has a complete Qwen3 HF-style layout, and the exact next no-launch command package is ready. Remaining hard blocker is GPU endpoint/current Milestone 1 `nodes.json`.
- Dev_4 Session 10 conflict resolution for PR #11 is recorded in `evidence/dev_4_sft_pipeline.md`: merged current `origin/main`, resolved conflict in `history_log.md`, preserved PM/test_1/test_2 post-PR10 gate records, and pushed the refreshed PR branch. GitHub recheck reports PR #11 `mergeable=MERGEABLE`. No SFT launch was attempted.
- PR #13 merged at `2026-05-20T09:00:25Z` with merge commit `9a6de432919102c17fdd839e5544d46c98a8f1f7`.
- Dev_4 self-merged PR #11 at `2026-05-20T09:10:26Z` with merge commit `93c4efaaff3e50220f7bb8583070321e65289efa`. PM gate: no-launch clean-base SFT smoke package and conflict-resolution evidence are now on main.
- Dev_2 GPU route acquisition evidence is recorded in `evidence/dev_2_gpu_route_attempt.md`. PM gate: sufficient route-attempt evidence. Compute manager peer route was undeliverable; no current Milestone 1 `nodes.json` exists; two live H200 candidates were discovered but are not approved Milestone 1 allocation, show high memory use, and lack local SFT paths.
- Current PM decision: SFT launch remains unauthorized until compute approves one discovered endpoint or provides a fresh GPU endpoint/current `nodes.json`. If approval lands, dev_4 owns staging/verifying paths and running the SFT smoke; PM will only gate durable evidence.
- PM coordination PR #15 is open to record PR #11 merge and dev_2 GPU route evidence.

## Next PM Checks

- Route GPU allocation/current `nodes.json`; use dev_1's clean-base candidate as the preferred `BASE_MODEL` once GPU is available.
- Gate test_2's durable mini-swe-agent smoke gate package, then require real smoke evidence after dev_4 provides a usable model/checkpoint path or endpoint.
- Gate test_1 support evidence when it appears: SFT+mini-swe completion audit gate remains missing.
- Gate dev_4's next no-launch SFT smoke launch package using `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.
- Keep SFT/eval execution unauthorized until owner evidence lands and a GPU/current `nodes.json` is available.
- After PR #2 merge, continue milestone coordination from fresh state while keeping the active goal open for SFT/eval smoke blockers.
- Open/push a continuation PM coordination PR for the new branch and keep reading durable support evidence for SFT/eval blocker decisions.
- After PR #3 merge, continue reading durable support evidence for SFT/eval blocker decisions and create a new coordination PR only when new PM durable updates are needed.
- Recheck test_2 eval acceptance/provenance package before authorizing mini-swe smoke after SFT checkpoint/endpoint exists.

## 2026-05-20 Session 8 Approved GPU Route

- PR #15 merged at `2026-05-20T09:19:31Z` with merge commit `21c59cd013e6d8c1a736483cc91864b11325f417`.
- Compute GPU route decision is recorded in `evidence/compute_gpu_route_decision.md`; one-node route file is `evidence/compute_gpu_route_nodes.json`.
- Approved SFT smoke route:
  - SSH: `ssh -p 39314 root@10.100.20.37`
  - LTP frame: `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130`
  - Node: `lg-cmc-b7r202-o09u26-h200-000667`
  - GPU: 8 x NVIDIA H200, idle at verification
  - repo/data staged: `/root/workspace/coding_agent_playground` and `/root/workspace/cleaned_m1_sft_10/train.jsonl`
  - output root writable: `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`
- PM authorized dev_4 to run only the short Qwen3-8B SFT smoke on this route after resolving PR #14 conflict and preserving PR #15 records. Test_2 still owns mini-swe after a real SFT model/checkpoint exists.

## 2026-05-20 Session 8 Post-PR10 Gate Update

- PR #10 merged at `2026-05-20T08:45:07Z` with merge commit `ce59c983372ac12dc3433091278efb6eec1876eb`; it recorded the prior missing-artifact wait state and kept the active goal open.
- Test_1 wrote `evidence/test_1_sft_eval_completion_gate.md`. PM gate result: sufficient completion audit gate. It explicitly requires real `DRY_RUN=0` SFT smoke, durable checkpoint/model, logs/metrics, mini-swe smoke against that exact model, trajectories/predictions/metrics, and a final PASS/FAIL decision block before PM can mark the loop complete.
- Test_2 updated `evidence/test_2_eval_validation.md` with the current mini-swe acceptance/provenance package. PM gate result: sufficient eval gate. It accepts an OpenAI-compatible served endpoint/model string plus `OPENAI_BASE_URL`/auth; a raw checkpoint path alone is not acceptable until served, and the dirty mini-swe checkout must be recorded as smoke provenance.
- Dev_4's requested no-launch clean-base SFT smoke launch package using `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` is not yet present in PM worktree. PM observed dev_4 working in its own workspace with a local `status.md` conflict after rebasing/stash-pop; dev_4 remains owner for resolving and landing the package.
- Current PM decision: SFT/eval execution is still not authorized. Data, clean-base candidate, test_1 completion gate, and test_2 eval acceptance gate are ready enough, but real SFT still needs a current GPU endpoint or Milestone 1 `nodes.json`; no real SFT checkpoint/output and no mini-swe eval metrics exist.
- PM coordination PR #12 is open for these post-PR10 gate records.
- PR #12 merged at `2026-05-20T08:56:29Z` with merge commit `1e32de047754e376f107b727ddf7349417696db9`.
- PR #11 gate audit: dev_4's no-launch clean-base SFT package PR is open/non-draft but mergeability resolved to `CONFLICTING`, so it is not ready for owner self-merge. PM notified dev_4 by tmux inject to rebase/resolve against current `origin/main`, preserve PM/test_1/test_2 post-PR10 gate records, push again, and record durable conflict resolution.
- PM coordination PR #13 is open to record the PR #11 conflict gate.
- Dev_4 self-merged PR #11 at `2026-05-20T09:10:26Z` with merge commit `93c4efaaff3e50220f7bb8583070321e65289efa`; PR #11 landed the no-launch clean-base SFT smoke package plus conflict-resolution evidence. Dev_4 opened Session 11 evidence PR #14: `https://github.com/peteryang1/coding_agent_playground/pull/14`. No SFT launch was attempted, and the remaining hard blocker is GPU endpoint/current Milestone 1 `nodes.json`.
- Session 12 dev_4 update: PM approved GPU route `ssh -p 39314 root@10.100.20.37` and ordered PR #14 conflict resolution first. Dev_4 merged current `origin/main` into PR #14 branch, preserved PR #15 dev_2 GPU route evidence/PM records, resolved the only conflict in `task_knowledge.md`, and did not launch SFT before PR #14 self-merge.
