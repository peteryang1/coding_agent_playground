# Milestone 1 - Qwen3-8B Coding SFT Loop

<!-- METADATA:STATUS=Open,ASSIGNEE=intern_code_pm -->

## Goal

Build the first full training/evaluation loop:

- Select three high-star GitHub repositories from different categories.
- Use Codex to rollout 10 total high-quality coding trajectories for this milestone smoke loop.
- Each acceptable trajectory must include requirements understanding, repo/file localization, code inspection, an actual code edit or patch attempt, a test/check attempt with observed result, and final changed-files/tests/blockers.
- Normalize and clean trajectories into the `coding_agent_playground` data format.
- Run a Qwen3-8B SFT smoke/path check.
- Evaluate the resulting model path with a mini-swe-agent smoke/report.
- Produce an evaluation report.

## Operating Contract

- PM -> dev/test peer messages are allowed for assignments, test requests, and corrections.
- Dev/test -> PM routine confirmations, status, blockers, reports, and test results must be written to durable channels.
- Durable channels for this milestone are this task directory, intern `status.md`, PR comments, task docs, and PM-designated evidence files under `evidence/`.
- Dev/test interns must not use `/esc` toward PM for routine confirmations or status.
- PM top priority is full parallel utilization: every dev/test intern must keep active durable output in their owner area; upstream gaps should produce assumptions, sample data, validators, launch commands, smoke plans, or blocker evidence rather than idle time.
- PM must maintain explicit task records before assigning dev/test PR work; the registry is `task_registry.md`.
- Every dev/test PR must reference a task id with owner, acceptance criteria, durable evidence path, and completion marker.
- After owner self-merge, the owner must mark the corresponding task complete in task README/status or `task_registry.md`, update own `status.md`, update necessary history/evidence, push, and merge that completion record.

## Infrastructure

- Final workspace machine: `ssh -p 31787 root@10.100.194.40`.
- Final repo clone root: `/root/workspace/{repo}`.
- Local PM tracking root: `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop`.
- Largest-scale rollout/training/eval must run on the final workspace machine unless PM records a blocker and fallback.

## Selected Repositories

| Repo | Category | Stars observed 2026-05-20 | Final workspace path |
|------|----------|---------------------------|----------------------|
| `fastapi/fastapi` | Web API framework | 98356 | `/root/workspace/fastapi` |
| `scikit-learn/scikit-learn` | Machine learning library | 66124 | `/root/workspace/scikit-learn` |
| `Textualize/rich` | CLI/terminal rendering library | 56396 | `/root/workspace/rich` |

## Durable Files

- PM status: `status.md`
- PM assignments: `assignments.md`
- PM task registry and PR gate index: `task_registry.md`
- PM blockers: `blockers.md`
- Repository shortlist and evidence: `repo_selection.md`
- Intern outputs and evidence: `evidence/`
- Final report draft: `final_report.md`

## Current Blockers

- GPU allocation workflow and valid Qwen3-8B base/checkpoint path still need confirmation before real SFT.
- mini-swe-agent smoke is ready at the command/backend level, but needs the SFT smoke model/checkpoint or endpoint.
- The old 300/100-per-repo rollout scope has been stopped and superseded; old outputs are scratch-only.
- The active rollout target `/root/workspace/rollouts_m1_10` completed exactly 10 total complete coding-process trajectories; cleaned SFT data is `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
