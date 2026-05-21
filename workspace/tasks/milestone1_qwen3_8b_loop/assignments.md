# Milestone 1 Assignments

## Durable Response Rule

Do not send routine confirmations, status, blockers, reports, or test results to PM by peer message. Write updates to the evidence paths listed below, plus your own `status.md` when your state changes.

## PM Notification Rule

PM -> dev/test task or correction messages now default to direct tmux injection into the target intern pane, followed by Enter and `tmux capture-pane` verification that the message was submitted. `peer_send` is no longer the primary notification method. PM should avoid interrupts by default and use `/esc`, `C-c`, or equivalent only for supervisor-explicit urgent interruptions or when current execution would keep wasting resources or continuing an error.

## PM Top Priority

Every dev/test intern must have active, non-waiting work. If an upstream artifact is incomplete, continue on the nearest useful slice and write durable evidence: assumptions, sample inputs, validators, scripts, smoke plans, failure logs, or integration requirements. PM will treat idle owner areas as a coordination bug.

## GPU Resource Management Rule

Do not route routine GPU requests through axrd interns. The coding_agent_playground team must use LTP directly: submit jobs, check status, record job/node information, and stop/release resources after use.

PM only organizes, gates, collects durable evidence, and decides. PM does not submit LTP jobs, run training/eval, or stop GPU jobs directly. The assigned dev/test owner must write exact LTP commands, job/frame id, node endpoint, logs, and final stop proof to durable evidence.

Current active 8xH200 node is tracked in `evidence/gpu_resource_tracking.md`. `intern_code_dev_2` owns LTP lifecycle and stop proof; `intern_code_dev_4` owns SFT workload execution and smoke artifacts. The node must not sit idle.

## Task-To-PR Gate Rule

PM must maintain explicit tasks instead of driving work only through scattered assignments. The task index for this milestone is `task_registry.md`.

Every dev/test PR must map to a task id with owner, acceptance criteria, durable evidence path, and completion marker. PR owners must reference the task id in the PR body, task file, or evidence/status update.

PM gate for a ready PR includes:

- task id exists;
- owner is named;
- acceptance criteria are clear;
- durable evidence path is updated;
- PR is ready and mergeable.

When an owner self-merges a PR, that owner must mark the corresponding task complete in the task README/status or `task_registry.md`, update their own `status.md`, update history/evidence when needed, push, and merge that completion record. Ready/mergeable owner PRs should still be self-merged as soon as they pass PM gate; do not wait for the whole milestone.

2026-05-20 Session 12 reaffirmation: no dev/test PR should be opened or marked ready without a task id first. If a work item needs a PR, the owner must either use an existing task id from `task_registry.md` or PM must create/update the task record before the PR is gated. PM gate checks task id, owner, acceptance criteria, evidence path, mergeability, and the post-merge completion marker. Owner self-merge remains the owner responsibility; PM does not merge dev/test PRs.

2026-05-20 Session 12 supervisor reaffirmation: PM and all dev/test interns must follow the intern conduct flow for every PR-bearing item: PM maintains an explicit task, assigns that task to the owner, the owner maps any PR to that task, PM gates task id/owner/acceptance/evidence/mergeability, and the owner self-merges only after PM gate. After self-merge, the owner must mark the matching task complete, blocked-with-final-evidence, or ready-for-retry in task docs or `task_registry.md`, update their own `status.md`, update required history/evidence, and push or merge the completion record. PM will reject PRs that do not have a task mapping or completion-marker plan.

## Assignments

| Intern | Role | Owner Area | Durable Evidence Path |
|--------|------|------------|-----------------------|
| `intern_code_dev_1` | Dev | Maintain the 10-total task set and ensure prompts force complete coding-process trajectories rather than no-edit read-only conclusions. | `evidence/dev_1_repo_tasks.md` |
| `intern_code_dev_2` | Dev | Codex rollout harness for exactly 10 total trajectories on the final workspace machine. Include stop/supersede evidence for old 300 runs, resume, logging, metadata, and failure accounting. | `evidence/dev_2_rollout_harness.md` |
| `intern_code_dev_3` | Dev | Trajectory schema discovery, normalization, cleaning, conversion, and quality gate for complete coding-process trajectories. | `evidence/dev_3_data_pipeline.md` |
| `intern_code_dev_4` | Dev | Qwen3-8B SFT pipeline, GPU workflow, training command templates, checkpoint layout, and run manifest. | `evidence/dev_4_sft_pipeline.md` |
| `intern_code_test_1` | Test | Validate rollout harness, 10-total scope, and complete coding-process quality gate including actual edit/patch attempt and test/check attempt. | `evidence/test_1_validation.md` |
| `intern_code_test_2` | Test | Validate mini-swe-agent evaluation setup and final report metrics format; define smoke eval before full run. | `evidence/test_2_eval_validation.md` |

## Follow-Up Assignments

- 2026-05-20 Session 3: all interns must use final workspace `ssh -p 31787 root@10.100.194.40`; previous scratch-host artifacts are not final evidence.
- 2026-05-20 Session 3: `intern_code_dev_1` owns the immediate 300-task input gate. Produce `/root/workspace/rollout_harness/tasks_300.jsonl` or a deterministic generator/spec that yields exactly 100 prompts per selected repo. Write task family counts, sample prompts, and any blocked assumptions to `evidence/dev_1_repo_tasks.md`.
- 2026-05-20 Session 3: `intern_code_dev_2` owns full rollout launch readiness on the corrected final workspace. Harness gate is closed by PM tiny non-dry success; prepare/resume the 300-run command, batching plan, and failure accounting around `/root/workspace/rollouts`. Write commands and run status to `evidence/dev_2_rollout_harness.md`.
- 2026-05-20 Session 3: `intern_code_dev_3` must not wait for all 300 trajectories. Consume `/root/workspace/rollouts_smoke_v3` and `/root/workspace/rollouts_nondry_new_machine_tiny`, keep the converter contract current, and prepare validation for `/root/workspace/rollouts`. Write schema findings to `evidence/dev_3_data_pipeline.md`.
- 2026-05-20 Session 3: `intern_code_dev_4` must continue SFT planning independently of rollout completion. Validate Qwen3-8B base/checkpoint/GPU assumptions, produce launcher commands, and identify exact GPU-machine needs in `evidence/dev_4_sft_pipeline.md`.
- 2026-05-20 Session 3: `intern_code_test_1` must revalidate corrected final-workspace artifacts now available under `/root/workspace/rollouts_smoke_v3` and `/root/workspace/rollouts_nondry_new_machine_tiny`. Write pass/fail evidence to `evidence/test_1_validation.md`.
- 2026-05-20 Session 3: `intern_code_test_2` must re-check mini-swe-agent/backend availability on the corrected final workspace. `singularity` exists but `mini`, `mini-extra`, Docker, Apptainer, and `sb-cli` were not found in PM checks; write the install/backend recommendation and smoke-eval command to `evidence/test_2_eval_validation.md`.
- 2026-05-20 Session 4: supervisor scope changed Milestone 1 from producing all 300 results to running an end-to-end smoke loop. Old 300/100-per-repo rollouts are stopped/superseded and scratch-only.
- 2026-05-20 Session 4: active rollout target is exactly 10 total trajectories at `/root/workspace/rollouts_m1_10`, driven by `/root/workspace/rollout_harness/tasks_m1_10.jsonl`.
- 2026-05-20 Session 4: every accepted trajectory must include requirements understanding, repo/file localization, code inspection, actual code edit/patch attempt, test/check attempt, observed result/error, and final changed-files/tests/blockers.
- 2026-05-20 Session 4: `intern_code_dev_2` and `intern_code_test_1` should use `evidence/rollout_harness/validate_complete_coding_trajectories.py` for the 10-run quality gate and write results to their evidence files.
- 2026-05-20 Session 5: do not interrupt the active `/root/workspace/rollouts_m1_10` rollout. Current PM snapshot is 9/10 manifest entries with 9/9 valid complete-process trajectories; keep working on the following parallel tracks:
  - `intern_code_dev_1`: review `/root/workspace/rollout_harness/tasks_m1_10.jsonl` and write task/prompt quality findings to `evidence/dev_1_repo_tasks.md`, including whether each prompt forces actual edit/patch attempt and test/check attempt.
  - `intern_code_dev_2`: monitor `/root/workspace/rollouts_m1_10`, `/root/workspace/rollout_harness/rollouts_m1_10.log`, and manifest/done files; if any of the 10 fail or hang, document rerun strategy in `evidence/dev_2_rollout_harness.md` before taking action.
  - `intern_code_dev_3`: convert completed valid trajectories as they appear using `convert_rollouts_to_sft.py`; write counts, rejected examples, and final `coding_agent_playground_sft_v1` paths to `evidence/dev_3_data_pipeline.md`.
  - `intern_code_dev_4`: proceed with Qwen3-8B SFT smoke/GPU path using `/root/workspace/cleaned_m1_sft_10/train.jsonl` or the current partial clean file when available; write exact commands, machine needs, and blockers to `evidence/dev_4_sft_pipeline.md`.
  - `intern_code_test_1`: continuously validate complete-process quality using `validate_complete_coding_trajectories.py`; write latest checked/valid/invalid counts and any missing process markers to `evidence/test_1_validation.md`.
  - `intern_code_test_2`: prepare mini-swe-agent eval smoke using the SFT smoke model/checkpoint path and corrected final workspace backend; write command, config, and blocker evidence to `evidence/test_2_eval_validation.md`.
  Routine confirmations/status/results must be written to these durable files and each intern's own `status.md`; do not peer-send PM for routine updates.
- 2026-05-20 Session 5 final PM update: `/root/workspace/rollouts_m1_10` completed 10/10, `complete_process_validation.json` reports 10 valid / 0 invalid, and `/root/workspace/cleaned_m1_sft_10/train.jsonl` has 10 kept examples. PM used exact `/esc` interrupts for all six dev/test interns; follow-up delivery succeeded for dev_3/test_1/test_2, dev_1 remained unconfirmed, and dev_2/dev_4 were busy for follow-up messages. This file is the authoritative assignment record for all six.
- 2026-05-20 Session 6 supervisor correction: PM must only assign, gate, collect information, and decide. PM must not directly modify code or execute code/experiments, including on `ssh -p 31787 root@10.100.194.40`. All further final-workspace execution is delegated to the owner intern below.
- 2026-05-20 Session 6 direct activation:
  - `intern_code_dev_1`: review `/root/workspace/rollout_harness/tasks_m1_10.jsonl` for task quality and complete-process pressure; write findings to `evidence/dev_1_repo_tasks.md` and own `status.md`.
  - `intern_code_dev_2`: own rollout harness/run evidence, confirm old 300 remains stopped, verify `/root/workspace/rollouts_m1_10` manifest and rerun/failure strategy; write to `evidence/dev_2_rollout_harness.md` and own `status.md`.
  - `intern_code_dev_3`: verify `/root/workspace/cleaned_m1_sft_10/train.jsonl` plus conversion summary and schema fit; write to `evidence/dev_3_data_pipeline.md` and own `status.md`.
  - `intern_code_dev_4`: own all SFT/GPU/model path probing and any SFT execution; resolve/report valid base/checkpoint, GPU/nodes, broken symlink, and warm-start decision needs in `evidence/dev_4_sft_pipeline.md` and own `status.md`.
  - `intern_code_test_1`: validate the 10 trajectories for complete coding process including actual edit/patch attempt and test/check attempt; write to `evidence/test_1_validation.md` and own `status.md`.
  - `intern_code_test_2`: own mini-swe-agent eval smoke readiness and execution after dev_4 supplies a model/checkpoint/endpoint; write readiness, blockers, commands, and results to `evidence/test_2_eval_validation.md` and own `status.md`.
  Routine status and results go to durable files only. No routine peer-send reply to PM is requested.
- 2026-05-20 Session 7 continuation, non-interrupt tmux assignment verified by `capture-pane`:
  - `intern_code_dev_4`: produce a current SFT unblock decision package in `evidence/dev_4_sft_pipeline.md`, covering clean Qwen3-8B base path repair/location, warm-start historical checkpoint fallback recommendation, GPU/current `nodes.json` acquisition/verification, exact next command once base+GPU are available, and blockers requiring PM/supervisor decision.
  - `intern_code_test_2`: produce a current eval gate package in `evidence/test_2_eval_validation.md`, covering exact acceptance checks for SFT checkpoint path or endpoint, prediction/results/metrics verification, and whether the dirty mini-swe-agent checkout is acceptable or needs provenance note.
  PM used tmux inject plus Enter and capture-pane verification; no interrupt was used for this assignment.
- 2026-05-20 Session 7 continuation parallel support, non-interrupt tmux assignments verified by `capture-pane`:
  - `intern_code_dev_1`: independently check clean Qwen3-8B base model candidates and model registry evidence on corrected/shared paths; classify each path as clean base or historical/warm-start; write to `evidence/dev_1_sft_base_path_support.md` and own `status.md`.
  - `intern_code_dev_2`: independently check current GPU allocation, `nodes.json`, and compute workflow evidence for Milestone 1 without starting training; write exact checked paths/commands and routing recommendation to `evidence/dev_2_gpu_nodes_support.md` and own `status.md`.
  - `intern_code_test_1`: define the SFT+mini-swe smoke completion audit gate and identify which current evidence is insufficient for completion; write to `evidence/test_1_sft_eval_completion_gate.md` and own `status.md`.
  These assignments keep the team parallelized while dev_4/test_2 prepare the primary SFT/eval decision packages.
- 2026-05-20 Session 11 resource-management correction:
  - `intern_code_dev_2`: own LTP lifecycle for the active H200 job `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130` at `ssh -p 39314 root@10.100.20.37`. Track status, idle time, stop conditions, and final stop proof in `evidence/gpu_resource_tracking.md` or `evidence/dev_2_gpu_lifecycle.md`. Do not run SFT.
  - `intern_code_dev_4`: after resolving PR #14 conflict, run the short SFT smoke on the approved node only, write `evidence/dev_4_sft_smoke_run.md`, and record whether dev_2 should stop the node immediately or keep it for a bounded retry.
  - `intern_code_test_2`: prepare mini-swe eval for the produced SFT model/checkpoint or endpoint only after dev_4 writes SFT smoke evidence. Do not use the SFT GPU node by default.
- 2026-05-20 Session 12 task/PR conduct reaffirmation delivered by tmux inject to `intern_code_dev_1`, `intern_code_dev_2`, `intern_code_dev_3`, `intern_code_dev_4`, `intern_code_test_1`, and `intern_code_test_2`: all future dev/test work must follow task -> PR -> merge -> task-complete. Routine confirmations, status, blockers, and test results must be written to durable evidence/status files, not peer-sent to PM.
- 2026-05-20 Session 12 retry authorization task split:
  - `intern_code_dev_2`: task `M1-GPU-RETRY-SUBMIT-DEV2`; submit or block a fresh LTP H200 retry job only, write resource/lifecycle evidence to `evidence/dev_2_gpu_retry_submit.md` and `evidence/gpu_retry_resource_tracking.md`; do not run SFT.
  - `intern_code_dev_4`: task `M1-SFT-RETRY-RUN-DEV4`; after dev_2 provides endpoint/node, run one SFT retry using `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml` and the PM-approved dataset; write `evidence/dev_4_sft_retry_run.md`.
  - `intern_code_dev_3`: task `M1-SFT-RETRY-DATA-GATE-DEV3`; gate retry data choice and write checksum/schema/limits to `evidence/dev_3_sft_retry_data_gate.md`.
  - `intern_code_dev_1`: task `M1-SFT-RETRY-PREGATE-DEV1`; independently sanity-check config/resource/test/data package and write `evidence/dev_1_sft_retry_pregate.md`.
  - `intern_code_test_1`: task `M1-SFT-RETRY-VALIDATE-TEST1`; validate retry against `test_1_sft_retry_gate.md` and write `evidence/test_1_sft_retry_validation.md`.
  - `intern_code_test_2`: task `M1-EVAL-UNBLOCK-TEST2`; keep mini-swe unblock command/gate ready and run/gate only after checkpoint or served endpoint exists; write `evidence/test_2_eval_unblock.md`.
  PM decision for first retry: use original `/root/workspace/cleaned_m1_sft_10/train.jsonl` unless dev_3 or test_1 records a launch-blocking issue. The repeated x16 dataset remains fallback/supporting smoke data, not the first retry default.
- 2026-05-20 Session 12 data-format unblock task split:
  - `intern_code_dev_4`: continue owning PR #30 conflict refresh for `M1-SFT-RETRY-RUN-DEV4`; no SFT rerun.
  - `intern_code_dev_3`: task `M1-SFT-DATAFORMAT-FIX-DEV3`; produce a no-execution fix plan for LLamaFactory `KeyError: 'from'`, covering OpenAI role/content registration and ShareGPT `from`/`value` fallback; write `evidence/dev_3_sft_dataformat_fix_plan.md`.
  - `intern_code_dev_1`: task `M1-SFT-DATAFORMAT-REVIEW-DEV1`; independently review retry failure facts and dev_3 fix plan for provenance/schema risks; write `evidence/dev_1_sft_dataformat_review.md`.
  - `intern_code_test_1`: task `M1-SFT-DATAFORMAT-GATE-TEST1`; define the pre-run/post-run gate for a data-format-fixed retry; write `evidence/test_1_sft_dataformat_gate.md`.
  - `intern_code_dev_2`: task `M1-GPU-RETRY-PLAN2-DEV2`; prepare next LTP plan and stale-resource proof only; do not submit a GPU job; write `evidence/dev_2_gpu_retry_plan2.md`.
  - `intern_code_test_2`: task `M1-EVAL-BLOCKED-REFRESH-TEST2`; refresh mini-swe blocked/unblock evidence after the retry failure; write `evidence/test_2_eval_blocked_after_retry_failure.md`.
  No GPU, SFT, or eval execution is authorized by this split.
- 2026-05-20 Session 12 data-format artifact follow-up:
  - `intern_code_dev_3`: task `M1-SFT-DATAFORMAT-ARTIFACT-DEV3`; produce the concrete no-GPU data-format artifact/preflight package for the chosen fix path and write `evidence/dev_3_sft_dataformat_artifact.md`.
  - PM gate inputs from `M1-SFT-DATAFORMAT-FIX-DEV3`, `M1-SFT-DATAFORMAT-REVIEW-DEV1`, `M1-SFT-DATAFORMAT-GATE-TEST1`, `M1-GPU-RETRY-PLAN2-DEV2`, and `M1-EVAL-BLOCKED-REFRESH-TEST2` are sufficient for planning only; they do not authorize GPU/SFT/eval execution.
  - Concrete launch remains blocked until artifact evidence, PR #30 owner refresh/merge, test_1 artifact gate, and fresh PM authorization are complete.
- 2026-05-20 Session 12 post-PR #38 parallel launch-package assignments:
  - `intern_code_dev_4`: immediate priority remains task `M1-SFT-RETRY-RUN-DEV4` PR #30 refresh against current `origin/main`; no self-merge until fresh PM gate and no SFT/GPU rerun. After or while preserving that priority, task `M1-SFT-LAUNCH-PACKAGE-DEV4` may draft exact future command/config/env/output evidence only.
  - `intern_code_dev_3`: task `M1-SFT-DATASETINFO-PACKAGE-DEV3`; turn the accepted ShareGPT artifact into exact `dataset_info.json`/mapping/package evidence without running SFT/GPU/eval.
  - `intern_code_dev_1`: task `M1-SFT-LAUNCH-REVIEW-DEV1`; independently review launch inputs and record current missing inputs/blockers without remote experiments.
  - `intern_code_dev_2`: task `M1-GPU-RETRY-READY-DEV2`; refresh LTP readiness/no-active-GPU proof and templates only; do not submit.
  - `intern_code_test_1`: task `M1-SFT-LAUNCH-GATE-TEST1`; prepare the final no-execution preflight/post-run gate for the data-format-fixed retry.
  - `intern_code_test_2`: task `M1-EVAL-SMOKE-PACKAGE-TEST2`; prepare mini-swe smoke command/result package while recording that execution is blocked until a checkpoint/model/endpoint exists.
  - These tasks keep all interns active but do not authorize GPU, SFT, or mini-swe execution. Any dev/test PR created from these tasks must cite the task id, owner, acceptance criteria, evidence path, and completion marker.
- 2026-05-21 Session 21 supervisor resume / replacement checkpoint path:
  - Stale PR #30 and missing Session 12 launch-package files are no longer allowed to stop checkpoint progress.
  - `intern_code_dev_3`: task `M1-S21-DATASETINFO-PACKAGE-DEV3`; write exact ShareGPT LLamaFactory `dataset_info.json` package to `evidence/dev_3_s21_datasetinfo_package.md`; no SFT/GPU/eval.
  - `intern_code_test_1`: task `M1-S21-LAUNCH-GATE-TEST1`; gate dev_3 package and expected runtime artifacts in `evidence/test_1_s21_launch_gate.md`; no SFT/GPU/eval.
  - `intern_code_dev_1`: task `M1-S21-LAUNCH-REVIEW-DEV1`; independently review package/gate/runtime plan in `evidence/dev_1_s21_launch_review.md`; no remote experiments.
  - `intern_code_dev_2`: task `M1-S21-RUNTIME-DEV2`; acting resource/runtime owner. Prepare LTP and, after PM gate on dev_3/test_1/dev_1 evidence, submit/run ShareGPT-fixed SFT smoke and write `evidence/dev_2_s21_sft_runtime.md` plus `evidence/gpu_s21_resource_tracking.md`. Target checkpoint/model or fresh exact runtime blocker with logs and next fix.
  - `intern_code_test_2`: task `M1-S21-EVAL-PACKAGE-TEST2`; prepare mini-swe package in `evidence/test_2_s21_eval_package.md`; do not run eval until checkpoint/endpoint exists and PM gates it.
  - `intern_code_dev_4`: task `M1-S21-PR30-CLEANUP-DEV4`; refresh, merge, close, or supersede PR #30 as archival evidence; this must not block Session 21 runtime path.

## PM Integration Responsibilities

- Keep `status.md` updated with milestone state.
- Keep `blockers.md` updated with active blockers and routing.
- Ensure largest-scale rollout/training/eval owner assignments point to `ssh -p 31787 root@10.100.194.40`; PM gates evidence but does not execute code or experiments directly.
- Write secretary/supervisor-readable task split, tracking paths, and blockers to durable task files such as `pm_secretary_report.md`, `status.md`, and `blockers.md`; do not send routine PM -> secretary peer messages.
