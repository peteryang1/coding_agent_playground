# Milestone 1 Task Registry

<!-- METADATA:STATUS=Open,SESSION=15 -->

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
| `M1-SFT-SMOKE-DEV4` | `intern_code_dev_4` | Run short Qwen3-8B SFT smoke on approved clean-base/data/GPU route, record commands/logs/results, and state whether dev_2 should stop or retry resource. | Evidence records `DRY_RUN=0`, base model, dataset, GPU endpoint, run ids, exit status, logs, checkpoint/model presence or blocker, and resource action recommendation. | `evidence/dev_4_sft_smoke_run.md`; `workspace/interns/intern_code_dev_4/status.md` | PR #18 refreshed by dev_4 to attach this task id and resolve conflicts; awaiting GitHub mergeability recheck and PM gate pass before self-merge. | Open: after PR #18 is PM-gated and self-merged, dev_4 must mark this task complete or blocked-with-final-evidence with `mergedAt` and merge commit. |
| `M1-GPU-LIFECYCLE-DEV2` | `intern_code_dev_2` | Track and release active 8xH200 LTP resource after SFT completion/failure/no-retry. | Evidence includes stop command/action, LTP frame id, UTC timestamp, post-stop status, endpoint proof, and preserved-output note. | `evidence/dev_2_gpu_lifecycle.md`; `evidence/gpu_resource_tracking.md`; `workspace/interns/intern_code_dev_2/status.md` | PR #20 merged: `https://github.com/peteryang1/coding_agent_playground/pull/20`; `mergedAt=2026-05-20T10:02:28Z`; merge commit `3bfcb3781931070b932d138957620dbe9f1d2ee9`. | Complete: LTP stop sent at 2026-05-20T09:52Z; post-stop status `STOPPED (Completed)` at 2026-05-20T09:53:21; endpoint `ssh -p 39314 root@10.100.20.37` refused connection after stop; outputs preserved under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`. |
| `M1-EVAL-SMOKE-TEST2` | `intern_code_test_2` | Run or block mini-swe smoke only after SFT model/checkpoint or served endpoint exists. | Evidence identifies accepted model/endpoint, command, backend/provenance, predictions/results path, metrics, or explicit blocker if SFT failed. | `evidence/test_2_eval_validation.md`; `workspace/interns/intern_code_test_2/status.md` | No eval PR until SFT gate resolves. | Open: blocked by absent SFT checkpoint/endpoint. |
| `M1-TASK-PR-GATE-PM` | `intern_code_pm` | Record intern conduct task->PR->merge->complete rule and notify all dev/test owners. | Durable knowledge/status/assignments/history updated; tmux inject submitted and capture-pane verified for all six dev/test interns. | `task_registry.md`; `assignments.md`; `task_knowledge.md`; `history_log.md`; `workspace/interns/intern_code_pm/status.md` | PM coordination PR #19 expected for Session 12. | Open until PM PR is merged and notifications are verified. |

## Completed Task Gate Examples

| Task ID | Owner | Completion Evidence |
|---------|-------|---------------------|
| `M1-ROLLOUT-10-DEV2-TEST1` | `intern_code_dev_2`, `intern_code_test_1` | `/root/workspace/rollouts_m1_10` completed 10/10; validator reports 10 checked / 10 valid / 0 invalid. |
| `M1-SFT-DATA-DEV3` | `intern_code_dev_3` | `/root/workspace/cleaned_m1_sft_10/train.jsonl` has 10 kept `coding_agent_playground_sft_v1` examples, 0 rejects, 0 conversion errors. |
