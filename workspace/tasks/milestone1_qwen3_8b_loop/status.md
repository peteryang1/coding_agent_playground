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

- PR55 follow-up critical path: dev_4 must fix the SFT launch wrapper/env issue that produced `environment: DEP_TARGET: unbound variable`; dev_1 and test_1 must gate the fix before any new runtime authorization.
- dev_2 must record resource recovery/readiness only; no fresh LTP/GPU/preflight/SFT/eval submit is authorized.
- dev_3 must confirm the accepted ShareGPT data/package remains unchanged and is not the PR55 blocker.
- test_2 must keep mini-swe blocked evidence current until PM gates a checkpoint/model or served endpoint.
- Route GPU allocation/current `nodes.json`; use dev_1's clean-base candidate as the preferred `BASE_MODEL` once GPU is available.
- Gate test_2's durable mini-swe-agent smoke gate package, then require real smoke evidence after dev_4 provides a usable model/checkpoint path or endpoint.
- Gate test_1 support evidence when it appears: SFT+mini-swe completion audit gate remains missing.
- Gate dev_4's next no-launch SFT smoke launch package using `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.
- Keep SFT/eval execution unauthorized until owner evidence lands and a GPU/current `nodes.json` is available.
- After PR #2 merge, continue milestone coordination from fresh state while keeping the active goal open for SFT/eval smoke blockers.
- Open/push a continuation PM coordination PR for the new branch and keep reading durable support evidence for SFT/eval blocker decisions.
- After PR #3 merge, continue reading durable support evidence for SFT/eval blocker decisions and create a new coordination PR only when new PM durable updates are needed.
- Recheck test_2 eval acceptance/provenance package before authorizing mini-swe smoke after SFT checkpoint/endpoint exists.

## 2026-05-21 Session 23 PR55 Runtime Final Blocker

- dev_2 completed the single authorized PR55 runtime under `M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2`.
- Preflight passed on `lg-cmc-b7r202-q05u06-h200-000722`: `PREFLIGHT_RESULT=PASS`, `SFT_ALLOWED=true`, `TORCH_NCCL_ALLREDUCE_EXIT=0`, capacity/different-node/home-storage PASS, topology/NVLink present.
- Source/data were prepared from local/provided workspace, transferred to the node, and checksum/file-list verified; no remote GitHub clone/fetch/source/dependency download was used.
- The single SFT attempt failed before GPU training with `environment: DEP_TARGET: unbound variable` in the exported LLamaFactory wrapper function.
- No checkpoint/model, `trainer_state.json`, `all_results.json`, or eval artifact exists.
- Frame `xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z` is stopped/released; final state `STOPPED (Completed)`, completed `2026-05-21 15:09:43`, endpoint refused after stop, and dev_2 records no active Milestone GPU job.
- PM decision: no fresh LTP/GPU/preflight/SFT/eval retry is authorized. Next work is a no-execution wrapper fix/review/gate split across all six owners, with all future generated SFT/eval intermediates under `/home/xu.yang` and all future runtime source/dependency materials prepared locally then transferred to the node.
- PM delivered the six follow-up assignments by tmux inject plus Enter and verified with `capture-pane`; the first audit found no follow-up evidence files or open PR yet. Current state stays Working, not blocked: owners have fresh tasks and runtime is intentionally closed until gate evidence lands.
- PM re-injected a second evidence-or-blocker follow-up to all six owner panes and verified submission by `capture-pane`. Owners must now either complete the named PR55 durable evidence files or write exact blockers in those files; no runtime authorization exists.
- PR55 follow-up package is now gate-ready for merge: PR #57 is open/non-draft `MERGEABLE` / `CLEAN`, dev_1 and test_1 both record `PASS_FOR_PM_RETRY`, dev_2/dev_3/test_2 support evidence is complete for current state. PM gate passes for dev_4 owner self-merge only; runtime remains unauthorized.

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

## 2026-05-20 Session 11 Resource Tracking Update

- Resource-management rule applied: coding_agent_playground dev/test owners must use LTP directly for GPU submit/status/ssh/stop workflows. Do not route routine GPU requests through axrd interns.
- Active 8xH200 resource is tracked in `evidence/gpu_resource_tracking.md`.
- Lifecycle/stop-proof owner: `intern_code_dev_2`.
- Workload/SFT owner: `intern_code_dev_4`.
- Stop target: after SFT smoke completion/failure, if idle for 15 minutes without owner progress, or by `2026-05-20T10:30:00Z` unless dev_2 records a bounded extension reason.
- Required stop evidence: LTP stop command/action, job frame, UTC timestamp, post-stop status, and proof that output artifacts remain under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.
- PM coordination PR #17 is open for the resource lifecycle tracking update.

## 2026-05-20 Session 12 Task-To-PR Gate Update

- Supervisor conduct rule applied: PM must maintain explicit task records and assign work through tasks, not only scattered assignments.
- Created `task_registry.md` as the Milestone 1 task -> PR -> merge -> task-complete gate index.
- New PM gate: every dev/test PR must map to a task id with owner, acceptance criteria, durable evidence path, and completion marker before PM marks it ready.
- New owner merge rule: after self-merging a PR, the owner must mark the corresponding task complete in task README/status or `task_registry.md`, update own `status.md`, update history/evidence when needed, push, and merge that completion record.
- Resource gate update: dev_4 reported real SFT smoke plus one bounded retry both failed and recommends no further GPU use; PM instructed dev_2 by tmux inject to stop/release the active H200 LTP frame and write stop proof.
- PR #18 gate update: PM audited dev_4's SFT smoke evidence PR and marked it not ready because it is `CONFLICTING` and lacks task id `M1-SFT-SMOKE-DEV4` in the PR body. PM notified dev_4 by tmux inject to attach task id, resolve conflicts, and mark the task complete or blocked-with-final-evidence after owner self-merge.
- Session 15 dev_4 update: dev_4 merged current `origin/main`, preserved PM Session 12 task registry/gate records, resolved PR #18 conflicts, and updated evidence/task docs to reference task id `M1-SFT-SMOKE-DEV4`. PR #18 remains open pending GitHub `MERGEABLE` status and PM gate pass before owner self-merge.
- Session 18 dev_4 completion: PR #18 merged at `2026-05-20T10:18:04Z` with merge commit `1c3a3e23921dd3fc91b340f9b67f83c747d42948`. Task `M1-SFT-SMOKE-DEV4` is blocked-with-final-evidence: approved SFT smoke evidence is durable, but no checkpoint/model was produced.
- Session 20 dev_4 completion: PR #26 merged at `2026-05-20T10:44:55Z` with merge commit `6a704f842c992f83a8d86167dfe870fa6ff72440`. Task `M1-SFT-CONFIG-FIX-DEV4` is ready-for-retry: config package landed, no GPU run performed, and future execution requires PM authorization plus test/resource gates.

## 2026-05-20 Session 12 PR #20/#21 Gate Update

- PR #20 for `M1-GPU-LIFECYCLE-DEV2` passed PM gate and was self-merged by dev_2.
- PR #20 merged at `2026-05-20T10:02:28Z`, merge commit `3bfcb3781931070b932d138957620dbe9f1d2ee9`.
- PR #21 merged post-merge facts at `2026-05-20T10:05:06Z`, merge commit `36ee08ae3ad98f7a94b7c5c7155938479333bd37`.
- GPU resource lifecycle is closed: LTP reached `STOPPED (Completed)`, endpoint `ssh -p 39314 root@10.100.20.37` refused connection after stop, and outputs were preserved under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.
- PR #18 remains the active SFT evidence blocker: it references task id `M1-SFT-SMOKE-DEV4` but still reports `CONFLICTING` / `DIRTY`; dev_4 owns conflict resolution and owner self-merge after PM gate.

## 2026-05-20 Session 12 Task-Flow Reaffirmation

- PM running policy reaffirmed from supervisor instruction: work is organized as explicit task -> PR -> merge -> task completion, not only scattered assignment lines.
- Every dev/test PR must cite a task id with owner, acceptance criteria, durable evidence path, and completion marker before PM can pass the PR gate.
- After owner self-merge, the owner must mark the matching task complete or blocked-with-final-evidence in task docs or `task_registry.md`, update their own `status.md`, update needed history/evidence, and merge/push that completion record.
- Latest PR #18 gate poll: PR body includes task `M1-SFT-SMOKE-DEV4`, owner, acceptance criteria, durable evidence path, and completion marker. GitHub reports `mergeable=MERGEABLE` and `mergeStateStatus=CLEAN`; no required checks are reported. PM gate passes and dev_4 has been instructed by tmux inject to self-merge as owner and then mark the task complete or blocked-with-final-evidence.
- PR #18 owner self-merge complete: `mergedAt=2026-05-20T10:18:04Z`, merge commit `1c3a3e23921dd3fc91b340f9b67f83c747d42948`. Remaining owner action is the completion-record PR/update marking `M1-SFT-SMOKE-DEV4` blocked-with-final-evidence because no checkpoint/model was produced.

## 2026-05-20 Session 19 Next Blocker Tasks

- Current gate state: PR #18 and PR #23 are merged; `M1-SFT-SMOKE-DEV4` is blocked-with-final-evidence. The failed SFT smoke produced no checkpoint/model, so mini-swe cannot run yet.
- PM decision: no GPU retry is authorized until owners land a concrete config/data/resource/test package.
- New explicit tasks:
  - `M1-SFT-CONFIG-FIX-DEV4`: dev_4 owns config fix/retry package.
  - `M1-SFT-DATA-MITIGATION-DEV3`: dev_3 owns data-side mitigation/rejection.
  - `M1-GPU-RETRY-RESOURCE-DEV2`: dev_2 owns fresh LTP resource plan, without starting a job before PM gate.
  - `M1-SFT-RETRY-GATE-TEST1`: test_1 owns retry acceptance gate.
  - `M1-EVAL-BLOCKED-TEST2`: test_2 owns explicit eval blocked evidence until checkpoint/endpoint exists.
  - `M1-SFT-FAILURE-REVIEW-DEV1`: dev_1 owns independent failure evidence review.
- PM delivered each assignment by tmux inject and verified the submitted text with `capture-pane`; no routine peer-send reply was requested.

## 2026-05-20 Session 12 Task/PR Conduct Reaffirmation

- Supervisor reaffirmed the intern conduct rule: PM must create or maintain explicit tasks before assigning work that can become a dev/test PR.
- PM durable gate rule is active: every dev/test PR must reference a task id with owner, acceptance criteria, durable evidence path, and completion marker before PM marks it ready.
- Owner self-merge rule is active: after a ready PR is self-merged, the owner must mark the corresponding task complete, blocked-with-final-evidence, or ready-for-retry in task docs or `task_registry.md`, update their own `status.md`, update needed history/evidence, and push or merge the completion record.
- PM notified all six dev/test owners by tmux inject plus capture-pane verification; no routine peer-send reply to PM was requested.
- Current PR audit: PR #26 merged at `2026-05-20T10:44:55Z`, PR #27 merged at `2026-05-20T10:47:11Z`, and the latest open-PR list is empty.
- Current gate decision: `M1-SFT-CONFIG-FIX-DEV4` is ready-for-retry, but actual GPU retry still requires PM to gate the support evidence package and assign owner execution; PM will not run training/eval itself.

## 2026-05-20 Session 12 SFT Retry Authorization Split

- PR #28 merged at `2026-05-20T10:58:33Z`, merge commit `d6d1092b8cf72eb6210502da0b058cd9bf9abab6`; it synced support evidence, PR #26/#27 facts, and task/PR conduct rules.
- PM gate decision: the next SFT retry may proceed as owner-executed work through explicit tasks, not PM-run commands.
- First retry config: `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`.
- First retry data decision: use original `/root/workspace/cleaned_m1_sft_10/train.jsonl` for the first attempt; use repeated x16 data only if dev_3/test_1 records a concrete blocker or PM explicitly changes the gate.
- Owner split created in `task_registry.md`: dev_2 submits/tracks fresh LTP resource; dev_4 runs one retry after endpoint exists; dev_3 gates data; dev_1 pregates package consistency; test_1 validates retry; test_2 prepares mini-swe unblock and remains blocked until checkpoint/endpoint exists.
- PM boundary remains active: PM does not submit LTP, run SFT, run eval, or stop GPU jobs directly.

## 2026-05-20 Session 12 Retry Resource Handoff

- Dev_3 completed `M1-SFT-RETRY-DATA-GATE-DEV3`: first retry data is `/root/workspace/cleaned_m1_sft_10/train.jsonl`, sha256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`; repeated x16 remains fallback only.
- Dev_1 completed pregate review. Its only launch blocker was missing dev_3 retry data gate; PM treats that blocker as resolved because dev_3 has now written the data gate.
- Test_1 completed pre-run validation: config/data/base/resource plan pass, post-run validation remains pending, and mini-swe remains blocked until checkpoint/model exists.
- Test_2 completed eval unblock preparation and records current status as `BLOCKED` until dev_4 provides an accepted checkpoint/model or served endpoint.
- Dev_2 started fresh LTP retry resource `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z`; endpoint `ssh -p 23121 root@10.100.22.53`, node `lg-cmc-b7r202-r05u16-h200-000747`, started `2026-05-20 11:06:20`, hard review `2026-05-20T12:06:20Z`.
- Dev_2 evidence says 8 x H200 are idle, repo/data/nodes are staged, and stop proof is pending while the resource is active for dev_4.
- PM injected the endpoint handoff to dev_4 by tmux. Dev_4 still owns the one retry and must write `evidence/dev_4_sft_retry_run.md`; PM will not execute it.

## 2026-05-20 Session 12 Retry Failure And Stop Proof

- Dev_4 ran the one authorized retry with run id `milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z`.
- Retry result from dev_2/dev_4 evidence: exit status `1`; no checkpoint/model, `trainer_state.json`, or `all_results.json`; failure signature `KeyError: 'from'` during LLamaFactory dataset conversion.
- PM decision: stop the H200 resource immediately because the single authorized retry completed, no extra retry was authorized, and the failure is a data registration/format blocker.
- Dev_2 stop proof: frame `xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z` reached `STOPPED (Completed)`, completed `2026-05-20 11:23:29`; endpoint `ssh -p 23121 root@10.100.22.53` refused connection after stop; `/mnt/3fs` outputs preserved.
- Current blocker: SFT retry failed before checkpoint creation because OpenAI-style role/content messages were registered through ShareGPT defaults expecting `from`/`value`.
- PR #30 has dev_4 run-result evidence but is currently `CONFLICTING` / `DIRTY`; dev_4 owns merging current `origin/main`, preserving stop proof and retry result evidence, then waiting for PM gate before self-merge.

## 2026-05-20 Session 12 Task/PR Flow Reaffirmation And PR #30 Gate

- Supervisor reaffirmed the intern conduct flow: PM must maintain explicit tasks, assign task owners, and gate every dev/test PR against task id, owner, acceptance criteria, durable evidence path, mergeability, and completion marker.
- Owner rule remains active: after a PM-gated self-merge, the dev/test owner must mark the corresponding task complete, blocked-with-final-evidence, or ready-for-retry in task docs or `task_registry.md`, update their own `status.md`, update needed history/evidence, and push or merge the completion record.
- PM delivered the reaffirmed task -> PR -> merge -> task-complete rule by tmux inject to `intern_code_dev_1`, `intern_code_dev_2`, `intern_code_dev_3`, `intern_code_dev_4`, `intern_code_test_1`, and `intern_code_test_2`; routine confirmations/status/results remain durable-file only.
- Current PR audit: PR #30 for task `M1-SFT-RETRY-RUN-DEV4` is open, non-draft, `MERGEABLE` / `CLEAN`, with no merge commit yet.
- PM gate decision: PR #30 passes the ready/mergeable gate for owner self-merge because it maps to `M1-SFT-RETRY-RUN-DEV4`, records owner/evidence/completion intent, and contains retry failure plus stop-proof evidence. Dev_4 was instructed by tmux inject to self-merge and then mark the task blocked-with-final-evidence.
- Post-PR #33 update: PM coordination PR #33 merged at `2026-05-20T11:42:11Z`, merge commit `ce06aa0805760bb9391ad38d5fb2b2732abb232f`. After main advanced, PR #30 changed to `CONFLICTING` / `DIRTY`; PM gate is now revoked until dev_4 merges current `origin/main`, preserves retry/stop-proof evidence, pushes, and GitHub returns mergeable/clean.
- Post-PR #34 audit: PM coordination PR #34 merged at `2026-05-20T11:44:37Z`, merge commit `62c60e367baaa60ca3935d78e0405b63f5a19366`. PR #30 still reports `CONFLICTING` / `DIRTY`, so it remains not gate-ready. PM re-injected the owner blocker to dev_4 by tmux and verified submission by `capture-pane`.
- Post-PR #35 conflict triage: PM coordination PR #35 merged at `2026-05-20T11:47:59Z`, merge commit `82eef1fb36900b1ddfb4ef57a6f02fe1ce8ff673`. PR #30 remains `CONFLICTING` / `DIRTY`; PM used `git merge-tree` to identify conflict markers in `history_log.md`, `task_knowledge.md`, and `task_registry.md`, then injected file-specific owner guidance to dev_4 by tmux.

## 2026-05-20 Session 12 Data-Format Unblock Parallelization

- PR #30 remains open and `CONFLICTING` / `DIRTY`; dev_4 still owns conflict refresh and no SFT rerun is authorized.
- PM is keeping main stable for PR #30 conflict refresh but is not leaving other interns idle.
- New explicit no-execution tasks were created for the known SFT blocker `KeyError: 'from'`: dev_3 data-format fix plan, dev_1 independent review, test_1 data-format gate, dev_2 next resource plan without submit, and test_2 eval blocked refresh.
- PM decision: no GPU, SFT, or mini-swe execution is authorized until these durable plans/gates are reviewed and PM issues a fresh gate.
- Test_2 completed `M1-EVAL-BLOCKED-REFRESH-TEST2`: `evidence/test_2_eval_blocked_after_retry_failure.md` records latest retry failure/no checkpoint/no endpoint facts, why mini-swe cannot run, accepted future endpoint/checkpoint forms, and validation fields. PM gate result: complete-for-current-state; eval remains blocked.
- PM gate result for the no-execution data-format package: dev_3 fix plan, dev_1 refreshed review, test_1 gate definition, dev_2 resource plan, and test_2 eval blocked refresh are sufficient for planning. They are not sufficient to authorize another retry because concrete dataset_info/ShareGPT artifact evidence, loader/preflight proof, PR #30 merge, and fresh PM authorization are still missing.
- Next explicit task: `M1-SFT-DATAFORMAT-ARTIFACT-DEV3` for dev_3 to produce concrete no-GPU data-format artifact/preflight evidence.
- Dev_3 completed `M1-SFT-DATAFORMAT-ARTIFACT-DEV3`: generated `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`, 10 rows, 10 unique `example_id`, 10 unique `trajectory_id`, schema `coding_agent_playground_sft_v1_sharegpt_messages`.
- Test_1 refreshed `M1-SFT-DATAFORMAT-GATE-TEST1`: artifact passes no-execution compatibility for the observed `messages[*].from/value` LLamaFactory reader. Retry remains blocked on exact future command, concrete future-run `dataset_info.json`, PR #30 owner refresh/merge, fresh LTP allocation, and PM authorization.
- Post-PR #38 audit: PR #30 is still open, non-draft, `CONFLICTING` / `DIRTY`, with last GitHub update `2026-05-20T11:36:42Z`; dev_4 remains owner for refresh and no self-merge/SFT rerun is allowed until fresh PM gate.
- PM opened the next no-execution parallel work package so all interns have active task ids while PR #30 is refreshed: `M1-SFT-DATASETINFO-PACKAGE-DEV3`, `M1-SFT-LAUNCH-PACKAGE-DEV4`, `M1-SFT-LAUNCH-REVIEW-DEV1`, `M1-GPU-RETRY-READY-DEV2`, `M1-SFT-LAUNCH-GATE-TEST1`, and `M1-EVAL-SMOKE-PACKAGE-TEST2`.
- PM decision remains unchanged: no GPU, SFT, or mini-swe execution is authorized. The next execution gate requires PR #30 merge/completion marker, exact dataset_info/command package, test_1 launch gate, dev_2 fresh LTP readiness, and explicit PM authorization.
- Owner-evidence audit at `2026-05-20T12:35:10Z`: PR #30 remains open and `CONFLICTING` / `DIRTY` with no new GitHub update after `2026-05-20T11:36:42Z`. The launch-package files `dev_3_sft_datasetinfo_package.md`, `dev_4_sft_launch_package.md`, `dev_1_sft_launch_review.md`, `dev_2_gpu_retry_ready.md`, `test_1_sft_launch_gate.md`, and `test_2_eval_smoke_package.md` are not yet present in PM durable evidence. PM re-submitted non-interrupt tmux start commands to all six owners.
- Blocker-evidence escalation at `2026-05-20T12:39:01Z`: PM re-audited panes and found no owner output beyond prior instructions. PM injected explicit directives requiring each owner to write the required evidence file or, if blocked, a blocker/missing-input list in that same evidence file plus own status. PR #30 refresh remains dev_4's first priority; no execution authorization is open.
- Blocked audit at `2026-05-20T12:41:44Z`: repeated audits still show PR #30 `CONFLICTING` / `DIRTY` with `updatedAt=2026-05-20T11:36:42Z`, and no owner evidence-or-blocker files for the six launch-package tasks. PM has exhausted assignment/gate/escalation actions available within role boundaries; further progress requires owner durable evidence or PR refresh.
- 2026-05-21 Session 21 resumed by supervisor: PM re-audited PR #30 and evidence, confirmed the stale state persists, then reorganized around a replacement checkpoint path. PR #30 is archival cleanup, not the next runtime blocker. New critical path is dev_3 dataset_info package -> test_1 launch gate -> dev_1 review -> PM gate -> dev_2 LTP/SFT runtime -> checkpoint or fresh runtime blocker -> test_2 eval package.

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
- Session 13 dev_4 SFT smoke result: approved GPU route/base/data/deps were usable, but no checkpoint/model was produced. Baseline clean-base run failed with MCA tiny-data DP=8 `steps_in_epoch=0`; one bounded TP=8 retry failed Megatron scheduler assertion for 1-step smoke. Evidence is in `evidence/dev_4_sft_smoke_run.md`. Dev_4 recommends dev_2 stop the active H200 allocation immediately.

## 2026-05-21 Session 22 CephFS Storage And Retry Gate

- Supervisor storage directive applied: SFT/eval intermediates must use CephFS `/home/xu.yang` unless an existing required path is explicitly justified.
- Owner evidence refreshed: dev_4 config/save fix, dev_2 resource plan, dev_3 data confirmation, test_2 eval package, dev_1 review, and test_1 retry gate now record `/home/xu.yang` defaults or required-path exceptions.
- Gate result: dev_1 and test_1 both record `PASS_FOR_PM_RETRY`.
- PM authorization: only `intern_code_dev_2` may run one ENOSPC-fixed ShareGPT SFT smoke under task `M1-S22-ENOSPC-RETRY-RUNTIME-DEV2`.
- Required runtime output root: `/home/xu.yang/coding_agent_playground/outputs`.
- Required next outcome: complete checkpoint/model with stop proof, or fresh exact runtime blocker with command, logs, node status, owner, and next fix.
- PM did not run LTP, SFT, GPU, remote workspace code, or eval commands.

## 2026-05-21 Session 22 Runtime Result

- dev_2 completed the single authorized owner-run and stop proof.
- `/home/xu.yang` CephFS path proof passed and 24GiB real-write capacity probe passed under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes`.
- SFT attempt result: `EXIT_STATUS=1` before useful runtime log, `run_manifest.json`, generated runtime config, checkpoint/model, `trainer_state.json`, or `all_results.json` existed.
- Old failure signatures were not observed because the durable log only contains `START_UTC`.
- LTP frame reached `STOPPED (Completed)` and endpoint refused connection after stop.
- Current state: no checkpoint/model; mini-swe blocked; no new retry authorized.
- New owner tasks: dev_4 early-exit fix package, dev_1 review, test_1 post-run gate, and test_2 eval-blocked refresh.
- Patch-gate update: dev_4 opened PR #39 for `M1-S22-EARLY-EXIT-FIX-DEV4`; GitHub reports it open, non-draft, `MERGEABLE` / `CLEAN`. PM gate remains pending dev_1/test_1 review because the diff includes both the needed wrapper patch and older dev_4 historical evidence files; dev_4 is not authorized to self-merge yet.
- PM follow-up split: dev_1 owns `M1-S22-EARLY-EXIT-PATCH-REVIEW-DEV1`, test_1 owns `M1-S22-EARLY-EXIT-PATCH-GATE-TEST1`, dev_2 owns `M1-S22-POSTPATCH-LTP-READY-DEV2`, and test_2 owns `M1-S22-POSTPATCH-EVAL-READY-TEST2`. These are no-execution readiness/gate tasks only.
- Gate result: PR #39 is not ready for owner self-merge. dev_1 recorded `BLOCKER_MANIFEST_ENV_CAPTURE` because the wrapper does not export/pass resolved manifest preflight variables before `write_sft_run_manifest.py`; test_1 recorded technical patch PASS but scope blocked by historical evidence diff. PM instructed dev_4 by tmux to update PR #39, keep no-execution boundary, and not self-merge.
- Post-patch readiness: dev_2 completed LTP readiness/no-active-Milestone-GPU proof, dev_3 completed data staging readiness with no data-side blocker, and test_2 completed eval readiness blocked by absent checkpoint/model. These do not authorize LTP/SFT/eval execution.
- Re-gate result: dev_4 updated PR #39 to head `f81c7da`; dev_1 now records `PASS_FOR_PM_RETRY`, and test_1 records `PASS_FOR_PM_PATCH_GATE`. GitHub reports PR #39 open, non-draft, `MERGEABLE` / `CLEAN`, with no required checks reported. PM gate passes for dev_4 owner self-merge only; this still does not authorize LTP/SFT/GPU/eval execution.
- PR #39 owner self-merge completed at `2026-05-21T09:17:15Z`, merge commit `4a6c2968e1290d30415460b464eee638110958bc`.
- PM created `M1-S22-POSTPATCH-SFT-RUNTIME-DEV2` and authorization evidence `evidence/pm_s22_postpatch_runtime_authorization.md`.
- PM authorized only `intern_code_dev_2` for exactly one post-PR39 ShareGPT-fixed Qwen3-8B SFT smoke attempt, with all outputs/logs/checkpoints/run metadata/capacity probes/intermediates under `/home/xu.yang/coding_agent_playground/outputs`.
- Required next durable outcome: complete checkpoint/model with stop proof, or fresh exact runtime blocker with command, logs, node status, stop proof, owner, and next fix.
- PM did not run LTP, SFT, GPU, remote workspace code, or eval commands.
- Runtime outcome: dev_2 completed the one authorized post-PR39 attempt and stop proof. The run produced PR #39 diagnostics and failed before training/checkpoint save with `datasets.map(num_proc=4)` / `SyncManager EOFError`; no checkpoint/model, `trainer_state.json`, or `all_results.json` exists; LTP reached `STOPPED (Completed)`.
- PM opened the no-execution dataset-map EOF fix chain: dev_4 single-process config/launcher package, dev_3 data confirmation, dev_1 review, test_1 gate, dev_2 no-active-resource readiness, and test_2 eval blocked. No new runtime authorization is open.

## 2026-05-21 Session 22 PR #41 Gate

- PM gated PR #41 for `M1-S22-DATASET-MAP-SINGLEPROC-FIX-DEV4` as `PASS_OWNER_SELF_MERGE_ONLY`.
- Gate basis: PR #41 head `fc0b6062664e3eb5283e89c22a152427ca47fc3c` is open, non-draft, `MERGEABLE` / `CLEAN`; dev_1 and test_1 both record `PASS_FOR_PM_RETRY`; dev_3 confirms no ShareGPT content/schema change is needed.
- Accepted scope: force the 10-row ShareGPT smoke away from `datasets.map(num_proc=4)` multiprocessing by using in-process/single-process preprocessing, preserve PR #39 diagnostics, and keep SFT intermediates under `/home/xu.yang/coding_agent_playground/outputs`.
- PM instructed dev_4 by tmux inject to self-merge PR #41 as owner and then mark the task completion record. This gate does not authorize LTP, SFT, GPU, eval, dry-run launch, or a runtime retry.
- Current milestone blocker remains absence of a complete SFT checkpoint/model plus `trainer_state.json`/`all_results.json`; mini-swe eval remains blocked until PM gates a model/checkpoint or served endpoint.

## 2026-05-21 Session 22 Post-PR41 Runtime Authorization

- PR #41 merged at `2026-05-21T10:00:25Z`, merge commit `2fc4b797a85c9375c6c5e1171963abe67aab35e8`.
- PM created task `M1-S22-POSTPR41-SFT-RUNTIME-DEV2` and authorization evidence `evidence/pm_s22_postpr41_runtime_authorization.md`.
- Authorized owner: only `intern_code_dev_2`.
- Required output/intermediate root: `/home/xu.yang/coding_agent_playground/outputs`.
- Required next durable outcome: complete checkpoint/model with `trainer_state.json`, `all_results.json`, and stop proof, or a fresh exact runtime blocker with command, logs, node status, stop proof, owner, and next fix.
- PM did not run LTP, SFT, GPU, remote workspace code, or eval commands.

## 2026-05-21 Session 22 Post-PR41 Runtime Result

- dev_2 completed the one authorized owner run and stop proof for `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`.
- LTP frame: `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z`; endpoint while active: `ssh -p 27021 root@10.100.22.14`; node: `lg-cmc-b7r202-p07u16-h200-000708`.
- `/home/xu.yang/coding_agent_playground/outputs` was proved on CephFS, with a 24GiB real-write capacity probe passing and cleaned.
- Runtime config/manifest used PR #41 merge commit `2fc4b797a85c9375c6c5e1171963abe67aab35e8`, dataset `coding_agent_m1_sft_10_sharegpt`, sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`, and `preprocessing_num_workers: null`.
- ShareGPT conversion completed 10/10 and training startup was reached; prior `num_proc=4` SyncManager EOF blocker did not recur.
- Final result: `EXIT_STATUS=1` at `2026-05-21T10:16:21Z`; fresh blocker is CUDA/NCCL `Invalid access of peer GPU memory over nvlink or a hardware error` / local_rank 5 SIGABRT before checkpoint save.
- No complete checkpoint/model, `trainer_state.json`, or `all_results.json`; no `KeyError: from` or ENOSPC signature; eval not run.
- Stop proof: LTP reached `STOPPED (Completed)` with completed timestamp `2026-05-21 10:17:58`; endpoint refused connection; no active Milestone GPU is held by dev_2.

## 2026-05-21 Session 22 NCCL/NVLink Follow-Up Split

- PM accepted test_1 final gate result `BLOCKED_FINAL_RUNTIME` for `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`; eval handoff remains blocked.
- Fresh blocker: `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`.
- No new LTP/SFT/GPU/eval retry is authorized.
- PM created no-execution mitigation tasks for dev_4, dev_2, dev_3, dev_1, test_1, and test_2.
- Required next gate: decide whether a future retry should use a different H200 node, adjusted NCCL/NVL settings, or a minimal hardware/NCCL preflight, while preserving PR39 diagnostics, PR41 single-process preprocessing, and `/home/xu.yang` intermediates.

## 2026-05-21 Session 22 PR #43 Gate

- NCCL/NVLink no-execution mitigation package passes PM gate for owner self-merge only.
- PR #43 head `5f4d14a12aa8044a429d1110757ed631a7bc9833` is open/non-draft `MERGEABLE` / `CLEAN`.
- Gate basis: dev_4 mitigation package, dev_2 resource plan, dev_3 data confirmation, dev_1 `PASS_FOR_PM_RETRY`, and test_1 `PASS_FOR_PM_RETRY`.
- Owner action: dev_4 must self-merge PR #43 and mark `M1-S22-NCCL-MITIGATION-DEV4` completion or ready-for-runtime-gate in durable task/status/history/evidence files.
- This gate does not authorize LTP, GPU, NCCL preflight execution, SFT retry, eval, or dry-run launch. Future SFT/eval/preflight intermediates must remain under `/home/xu.yang` unless an existing required input path is explicitly justified.

## 2026-05-21 Session 22 NCCL Preflight/SFT Authorization

- PR #43 merged at `2026-05-21T10:47:20Z`, merge commit `2c867d3226f7ebb4962b5b173235639df8f1f9be`.
- Completion PR #44 merged at `2026-05-21T10:50:28Z`, merge commit `6dcdc6730debeb2fb875baaec6667cb64d09867d`.
- PM created task `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2` and authorization evidence `evidence/pm_s22_nccl_preflight_sft_authorization.md`.
- Authorized owner: `intern_code_dev_2` only.
- Scope: one fresh 8 x H200 LTP allocation, preferably different from failed node `lg-cmc-b7r202-p07u16-h200-000708`; run NCCL/NVLink preflight first; run exactly one SFT smoke only if preflight passes.
- Required generated-artifact root: `/home/xu.yang/coding_agent_playground/outputs`, including preflight logs, launch logs, temporary converted datasets, checkpoints, run metadata, and eval-ready intermediates.
- No mini-swe eval is authorized. PM did not run LTP, GPU, NCCL preflight, SFT, eval, remote workspace code, or dry-run launch.

## 2026-05-21 Session 22 NCCL Preflight Final Blocker

- dev_2 completed the one authorized `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2` attempt and stop proof.
- Fresh frame: `xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z`; endpoint while active: `ssh -p 27402 root@10.100.24.11`; node: `lg-cmc-b7r401-a04u26-h200-000769`, different from failed post-PR41 node `lg-cmc-b7r202-p07u16-h200-000708`.
- `/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z` preserved preflight artifacts on CephFS.
- Capacity probe passed and cleaned; topology/NVLink evidence was captured; 8-rank torch NCCL all-reduce exited 0 with `NCCL_P2P_DISABLE` unset.
- Final preflight marker: `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`; dev_2's evidence attributes this to broad health-scan matches over evidence/command/process/generic NVRM text.
- Conditional SFT was correctly not run. No checkpoint/model, `trainer_state.json`, or `all_results.json` exists; no eval was run.
- Stop proof: LTP reached `STOPPED (Completed)` with completed timestamp `2026-05-21 11:02:09`; endpoint refused connection afterward.
- dev_1 final review result: `BLOCKER_PREFLIGHT_FAILED_NO_SFT_RUN_HEALTH_SIGNATURE_AMBIGUOUS`.
- test_1 final gate result: `PASS_FOR_NEXT_PM_DECISION`, with eval handoff still blocked as `EVAL_HANDOFF_BLOCKED_NO_SFT_NO_CHECKPOINT`.
- PM decision: no new LTP/GPU/NCCL preflight/SFT/eval authorization. Next no-execution task chain is parser refinement by dev_4, review by dev_1, test gate by test_1, and resource/data/eval-blocked refresh by dev_2/dev_3/test_2.
- Follow-up evidence collected so far: dev_2 no-submit resource readiness complete, dev_3 data/package no-change confirmation complete, test_2 eval blocked/readiness complete, test_1 parser gate defined and waiting for dev_4 package, and dev_1 review is blocked only on missing dev_4 parser package.
- PR #45 opened for `M1-S22-PREFLIGHT-PARSER-FIX-DEV4` and is currently open/non-draft `MERGEABLE` / `CLEAN`, but PM gate is NOT READY.
- dev_1 result: `BLOCKER_ECC_FALSE_NEGATIVE_RISK_IN_PR45`; ECC detection can miss real fatal/uncorrected ECC lines containing unrelated standalone `0` tokens such as `GPU 0`.
- test_1 result: `BLOCKED_STRUCTURED_FIELDS_AND_STORAGE_STATUS`; parser/wrapper must expose required top-level fields or stable aliases for `different_node_gate`, `home_xu_yang_storage_status`, direct `sft_allowed`/`sft_skip_reason`, and preflight/capacity/topology/NVLink/NCCL statuses.
- Current critical path: dev_4 must update PR #45 to resolve both blockers; then dev_1/test_1 must re-review/re-gate before PM can decide on any fresh preflight/SFT authorization.

## 2026-05-21 Session 23 Ceph-Fuse Fixed Runtime Final Blocker

- PR #51 is merged: dev_4 self-merged at `2026-05-21T13:23:23Z`, merge commit `c02a53a344f2ad7a33b04f529d5125677237d4cb`.
- dev_2 completed exactly one PM-authorized runtime under `M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2`: frame `xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z`, endpoint `ssh -p 38862 root@10.100.22.36`, node `lg-cmc-b7r202-q03u26-h200-000730`.
- Storage, transfer, and no-network gates passed: `ceph-fuse` was present, `/home/xu.yang/coding_agent_playground/outputs` resolved on CephFS, 24GiB capacity probe passed and cleaned, source/data were transferred from local/provided workspace with bundle/data/file-count/critical-checksum verification, and no remote GitHub/source/dependency network was used.
- Current blocker: `BLOCKED_PREFLIGHT_HEALTH_SIGNATURE`. Structured preflight returned `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE` and `SFT_ALLOWED=false`; torch NCCL all-reduce itself exited 0, while parser records include SXid 20009 dmesg records and NCCL warning lines.
- SFT was not launched by contract; no checkpoint/model, `trainer_state.json`, or `all_results.json` exists; mini-swe eval remains blocked and unauthorized.
- Resource release is complete: stop at `2026-05-21T13:39:17Z`, final `STOPPED (Completed)` at `2026-05-21 13:39:48`, endpoint refused after stop, and no running `coding-agent-playground` LTP jobs were visible.
- PM created the next no-execution task split for owner review/gate/triage/recovery. No new LTP/GPU/preflight/SFT/eval authorization exists.
- Follow-up owner evidence is now present. PM decision: current ceph-fuse fixed run is a node-health blocker, not a storage/data/checkpoint/eval blocker. Primary signal is `SXid 20009` / NVLink RX Short Error Rate on `lg-cmc-b7r202-q03u26-h200-000730`; NCCL deprecation warning classification is parser noise but does not unblock this run.
- PM authorized exactly one fresh different-node dev_2 runtime under `M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`. The new attempt must avoid the SXid node and prior failed nodes if selectable, use `/home/xu.yang`, use local bundle/data transfer with checksums, avoid remote source/dependency network, and run SFT only after structured preflight PASS plus `sft_allowed=true`. Eval remains unauthorized.
- In parallel, dev_4 owns `M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4` for no-execution parser hygiene around benign `NCCL_ASYNC_ERROR_HANDLING` warnings.

## 2026-05-21 Session 23 Same-Node Placement Blocker

- dev_2 completed the single authorized different-node attempt, but the LTP scheduler assigned the forbidden SXid node `lg-cmc-b7r202-q03u26-h200-000730` again. Frame: `xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z`; endpoint while active: `ssh -p 39629 root@10.100.22.36`.
- dev_2 stopped/released before source/data transfer, structured preflight, SFT, or eval. Final state: `STOPPED (Completed)`, completed `2026-05-21 14:04:32`; endpoint refused after stop; no running `coding-agent-playground` LTP jobs were visible.
- Current blocker: placement/resource routing. No fresh LTP/GPU/preflight/SFT/eval retry is authorized until a placement plan and same-node gate pass.
- PR #53 for dev_4 parser hygiene is open/non-draft and reported `MERGEABLE` / `CLEAN`, but PM gate is pending dev_1 review and test_1 gate. PR #53 is not authorized for owner self-merge yet.

## 2026-05-21 Session 23 PR #53 Gate / Placement State

- PR #53 parser hygiene is now gate-passed for owner self-merge only. dev_1 result: `PASS_FOR_PM_RETRY`; test_1 result: `PASS_FOR_OWNER_SELF_MERGE_AFTER_PM_GATE`; reviewed head `8b00ebd1d3ed00b8c18591d49ef0eb559456cb0f`; GitHub reports open/non-draft `MERGEABLE` / `CLEAN`.
- PM instructed dev_4 by tmux inject to self-merge PR #53 and mark `M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4` complete. This gate does not authorize LTP/GPU/preflight/SFT/eval.
- Placement remains blocked: dev_2 found no verified LTP node exclusion/pinning/anti-affinity path in the current local client/spec; dev_1 records `BLOCKER_MISSING_ENFORCEABLE_DIFFERENT_NODE_PLACEMENT_PLAN`; test_1 records same-node runtime as stopped correctly but blocked for future runtime authorization.
- PR #53 is merged at `2026-05-21T14:20:56Z`, merge commit `e29c93736be3384663cad953cd18da68c30070fb`; no open PRs are visible in the PM audit.
- PM authorized only dev_2 for one bounded placement-probe runtime under `M1-S23-PR53-PLACEMENTPROBE-PREFLIGHT-SFT-RUNTIME-DEV2`. This authorization explicitly accepts one stop-and-release placement probe because no enforceable node exclusion is available. Forbidden-node assignment must stop before transfer/preflight/SFT/eval; non-forbidden assignment may proceed to local bundle transfer, `/home/xu.yang` storage proof, structured preflight, and conditional SFT. Eval remains unauthorized.

## 2026-05-21 Session 23 PR53 Placement-Probe Final Blocker

- dev_2 completed the one authorized PR53 placement-probe attempt on non-forbidden node `lg-cmc-b7r401-a05u06-h200-000770`; frame `xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z`, endpoint `ssh -p 30073 root@10.100.24.12`.
- Storage, transfer, and runtime setup passed: `/home/xu.yang` CephFS, capacity probe, local bundle/data transfer, checksums/file count, no remote source/dependency network, topology/NVLink, and torch all-reduce exit 0.
- Current blocker: `BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE`. Structured preflight still classified `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings as actionable `nccl_or_collective_failure` despite `TORCHRUN_EXIT=0` and `ALLREDUCE_OK`; `SFT_ALLOWED=false`.
- SFT/eval were not run; no checkpoint/model/trainer_state/all_results. Frame is stopped/released and no running `coding-agent-playground` job remains.
- PM next split is no-execution parser/runtime fix review and gate; no fresh runtime is authorized.

## 2026-05-21 Session 23 PR #55 Gate

- PR #55 parser/runtime fix is gate-passed for owner self-merge only. GitHub: open/non-draft `MERGEABLE` / `CLEAN`; latest head `ee10fead593aa5a3d2a3eebdbf6cee5e643bfdde`.
- Functional commit reviewed: `6c959e89a75ce162076292ad6d6c317f421cd45f`. Later commits only adjust docs/evidence wording.
- dev_1 result: `PASS_FOR_PM_RETRY`; test_1 result: `PASS_FOR_PM_RETRY`.
- PM instructed dev_4 to self-merge PR #55 and mark task completion. Runtime remains unauthorized until merge/completion is recorded and PM separately gates a fresh dev_2 attempt.

## 2026-05-21 Session 23 PR55 Runtime Authorization

- PR #55 merged at `2026-05-21T14:49:25Z`, merge commit `1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703`; open PR audit is empty.
- PM authorized only dev_2 for one fresh runtime under `M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2`.
- Required next durable outcome: SFT checkpoint/model with `trainer_state.json`/`all_results.json` and stop proof, or exact runtime blocker with logs/node/status/output paths/stop proof. Eval remains blocked until PM gates a model or endpoint.
- PR55 runtime final blocker: dev_2's authorized PR55 run passed structured preflight and then failed the single SFT attempt before GPU training with `environment: DEP_TARGET: unbound variable`; no checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or eval artifact exists, and the frame is stopped/released.
- PR #57 is the current wrapper/env fix gate: open/non-draft `MERGEABLE` / `CLEAN`, dev_1 and test_1 both `PASS_FOR_PM_RETRY`, PM gate passes for dev_4 owner self-merge only. No fresh LTP/GPU/preflight/SFT/eval/runtime retry is authorized.
- Supervisor correction active: remote GPU/LTP nodes are no-external-network for project code/dependency staging. Future runtime owners must prepare and verify local/provided-workspace bundles, transfer by `rsync`, `scp`, or tar-over-SSH with exact evidence, and PM must not run transfer/remote commands/SFT/eval personally.
- PR #57 and completion PR #58 are merged. PM authorized only dev_2 under `M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2` for exactly one fresh owner-executed preflight/SFT runtime using `origin/main` commit `b4ac31ef1e3772953108348bf099818326ed65cc`; eval remains unauthorized.
- Parallel PR57 support evidence is present for dev_1 review placeholder, test_1 gate placeholder, dev_3 data confirmation, and test_2 eval-ready blocked package. Final SFT/eval decision still waits on dev_2 PR57 runtime/tracking evidence.
- Active resource under dev_2 ownership: `M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2` frame `xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z`, endpoint `ssh -p 22662 root@10.100.22.31`, node `lg-cmc-b7r202-q04u06-h200-000725`. Dev_2 owns stop/release proof and final checkpoint-or-blocker evidence; PM is observing/gating only.
- PR57 runtime final blocker: dev_2 completed the one authorized run. Preflight passed and SFT was allowed, but the single SFT attempt failed before checkpoint creation with `ImportError: mcore_adapter is required when USE_MCA=1`; no checkpoint/model/trainer_state/all_results/eval exists. The LTP frame is stopped/released and no active coding-agent-playground job remains.
- Current next action: no fresh runtime is authorized. PM assigned/assigning no-execution follow-ups for dev_4 MCA dependency/launch fix package, dev_1 review, test_1 gate, dev_2 resource recovery, dev_3 data confirmation, and test_2 eval re-block.
- PR #59 now contains dev_4's no-execution mcore fix package and is open/non-draft `MERGEABLE` / `CLEAN` at observed head `92e437cf690b68121b9ad9d2f76b18a60a10a2d6`. Runtime remains unauthorized pending dev_1/test_1 refreshed PASS gates.
- PR #59 gate update: dev_1 and test_1 both recorded `PASS_FOR_PM_RETRY`; GitHub reports PR #59 open/non-draft `MERGEABLE` / `CLEAN`, latest observed head `b0b54279bcf87add7e617b0c08686c40fac41b48`, functional patch commit `92e437cf690b68121b9ad9d2f76b18a60a10a2d6`. PM gate passes for dev_4 owner self-merge only. Runtime remains unauthorized until PR #59 is merged/completion-marked and PM separately authorizes dev_2 with local/provided `mcore_adapter` bundle provenance, transfer evidence, no remote source/dependency downloads, `/home/xu.yang` outputs, and import-check proof.
- PR #59 merged at `2026-05-21T16:34:13Z`, merge commit `8ed6248cd7bd56b89ac1124689fed0b56e4eba02`. PM authorized only dev_2 for one fresh PR59 preflight/SFT runtime under `M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2`; eval remains unauthorized. Required next durable outcome is checkpoint/model with `trainer_state.json`/`all_results.json` and stop proof, or fresh exact runtime blocker with logs/node/status/transfer/import/preflight evidence and next fix.
- PR59 runtime final blocker: dev_2's authorized run passed transfer/import/preflight gates and ran exactly one SFT attempt, but failed before checkpoint with `EXIT_STATUS=127` because `LLAMAFACTORY_CLI` was a space-containing command string executed as one quoted path. No checkpoint/model/trainer_state/all_results/eval exists. Frame is stopped/released with no running coding-agent-playground jobs. PM opened no-execution launcher-fix follow-ups and has not authorized a fresh retry.
- PR #61 gate update: dev_4 opened the LLamaFactory CLI command fix PR; dev_1/test_1 both recorded `PASS_FOR_PM_RETRY`; GitHub reports PR #61 open/non-draft `MERGEABLE` / `CLEAN` at head `d4f3340d1f7b32d91553cbe18d7effce533276c7`. PM gate passes for dev_4 owner self-merge only. Runtime remains unauthorized.
