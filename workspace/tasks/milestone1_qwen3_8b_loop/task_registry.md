# Milestone 1 Task Registry

<!-- METADATA:STATUS=Open,SESSION=12 -->

This registry is the PM gate index for task -> PR -> merge -> task-complete flow.

## Required Flow

1. PM creates or maintains a clear task entry before assigning owner work.
2. Each dev/test PR must reference the task id in the PR body, evidence file, or task status entry.
3. Each task entry must name owner, acceptance criteria, durable evidence path, and completion marker.
4. PM gates PR readiness by checking task id, owner, acceptance criteria, evidence path, and mergeability.
5. When an owner self-merges a PR, that owner must mark the task complete in the task README/status or this registry, update their own `status.md`, update history/evidence if needed, push, and merge the completion record.

Routine status and completion proof stay in durable files. Do not peer-send PM for routine task confirmation.

## Active Tasks

| Task ID | Owner | Scope | Acceptance Criteria | Evidence / Status | PR State | Completion Marker |
|---------|-------|-------|---------------------|-------------------|----------|-------------------|
| `M1-SFT-SMOKE-DEV4` | `intern_code_dev_4` | Run short Qwen3-8B SFT smoke on approved clean-base/data/GPU route, record commands/logs/results, and state whether dev_2 should stop or retry resource. | Evidence records `DRY_RUN=0`, base model, dataset, GPU endpoint, run ids, exit status, logs, checkpoint/model presence or blocker, and resource action recommendation. | `evidence/dev_4_sft_smoke_run.md`; `workspace/interns/intern_code_dev_4/status.md` | PR #18 self-merged at `2026-05-20T10:18:04Z`, merge commit `1c3a3e23921dd3fc91b340f9b67f83c747d42948`. | Open until dev_4's completion-record update marks this task blocked-with-final-evidence with `mergedAt` and merge commit. |
| `M1-GPU-LIFECYCLE-DEV2` | `intern_code_dev_2` | Track and release active 8xH200 LTP resource after SFT completion/failure/no-retry. | Evidence includes stop command/action, LTP frame id, UTC timestamp, post-stop status, endpoint proof, and preserved-output note. | `evidence/dev_2_gpu_lifecycle.md`; `evidence/gpu_resource_tracking.md`; `workspace/interns/intern_code_dev_2/status.md` | PR #20 merged: `https://github.com/peteryang1/coding_agent_playground/pull/20`; `mergedAt=2026-05-20T10:02:28Z`; merge commit `3bfcb3781931070b932d138957620dbe9f1d2ee9`. | Complete: LTP stop sent at 2026-05-20T09:52Z; post-stop status `STOPPED (Completed)` at 2026-05-20T09:53:21; endpoint `ssh -p 39314 root@10.100.20.37` refused connection after stop; outputs preserved under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`. |
| `M1-EVAL-SMOKE-TEST2` | `intern_code_test_2` | Run or block mini-swe smoke only after SFT model/checkpoint or served endpoint exists. | Evidence identifies accepted model/endpoint, command, backend/provenance, predictions/results path, metrics, or explicit blocker if SFT failed. | `evidence/test_2_eval_validation.md`; `workspace/interns/intern_code_test_2/status.md` | No eval PR until SFT gate resolves. | Open: blocked by absent SFT checkpoint/endpoint. |
| `M1-SFT-BASEPATH-DEV1` | `intern_code_dev_1` | Support SFT unblock by independently checking clean Qwen3-8B base model candidates and registry evidence on corrected workspace/shared paths without modifying remote state. | Evidence lists exact commands/paths checked, candidate paths, clean-base vs historical/warm-start classification, and whether a candidate unblocks dev_4. | `evidence/dev_1_sft_base_path_support.md`; `workspace/interns/intern_code_dev_1/status.md` | No PR: durable evidence/status-only PM support task. | Complete: recommended clean-base candidate `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`; broken alias/incomplete cache and historical/warm-start candidates classified; no active base-path blocker. |
| `M1-PROMPT-QUALITY-DEV1` | `intern_code_dev_1` | Own 10-task prompt/task quality review for Milestone 1 after supervisor correction. | Evidence confirms `tasks_m1_10.jsonl` can produce complete coding trajectories with actual edit/patch attempt and test/check attempt; issues/fixes needed recorded. | `evidence/dev_1_repo_tasks.md`; `workspace/interns/intern_code_dev_1/status.md` | No PR: durable evidence/status-only review task. | Complete: 10-task gate passes; quality risks and possible fixes recorded. |
| `M1-SFT-EVAL-COMPLETION-GATE-TEST1` | `intern_code_test_1` | Define the SFT + mini-swe smoke completion audit gate from current milestone evidence. | Evidence defines required files, commands, output artifacts, metrics, pass/fail criteria, PM completion record, and current insufficient evidence for real SFT smoke plus mini-swe smoke. | `evidence/test_1_sft_eval_completion_gate.md`; `workspace/interns/intern_code_test_1/status.md` | No PR: durable evidence/status-only PM support task. | Complete: `evidence/test_1_sft_eval_completion_gate.md` created on 2026-05-20 and own status updated; current evidence is insufficient because SFT is dry-run/readiness only and mini-swe has no SFT-model smoke predictions/metrics. |
| `M1-TASK-PR-GATE-PM` | `intern_code_pm` | Record intern conduct task->PR->merge->complete rule and notify all dev/test owners. | Durable knowledge/status/assignments/history updated; tmux inject submitted and capture-pane verified for all six dev/test interns. | `task_registry.md`; `assignments.md`; `task_knowledge.md`; `history_log.md`; `workspace/interns/intern_code_pm/status.md` | PR #19 merged; PR #22 merged follow-up gate sync. | Complete: task->PR->merge->task-complete flow is the active PM gate rule for all dev/test PRs. |

## Completed Task Gate Examples

| Task ID | Owner | Completion Evidence |
|---------|-------|---------------------|
| `M1-ROLLOUT-10-DEV2-TEST1` | `intern_code_dev_2`, `intern_code_test_1` | `/root/workspace/rollouts_m1_10` completed 10/10; validator reports 10 checked / 10 valid / 0 invalid. |
| `M1-SFT-DATA-DEV3` | `intern_code_dev_3` | `/root/workspace/cleaned_m1_sft_10/train.jsonl` has 10 kept `coding_agent_playground_sft_v1` examples, 0 rejects, 0 conversion errors. |
| `M1-SFT-HANDOFF-DEV3` | `intern_code_dev_3` | Complete: SFT input handoff for `intern_code_dev_4` is recorded in `evidence/dev_3_sft_input_handoff.md` with train path, sha256, schema/version, repo split, validation status, exact data contract, and data-side blockers. No PR required for this durable evidence-only PM assignment. |
