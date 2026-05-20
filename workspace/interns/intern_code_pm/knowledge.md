# intern_code_pm - 个人知识库

<!-- METADATA:SESSION=7 -->

---

## 知识条目

### 2026-05-20 - PM/dev/test durable communication correction

- Project operating contract: `secretary_pm_dev_test_intern_team_pattern_skill`.
- PM may send assignments, test requests, and corrections to dev/test interns.
- PM must not ask dev/test interns to peer_send routine confirmations, status, blockers, reports, or test results back to PM.
- Dev/test -> PM routine communication must use durable project channels: `report.md`, `status.md`, task docs, PR comments, or a PM-designated evidence file.
- PM notification wording must name the exact durable file, PR comment, task doc, or evidence path to update.
- Dev/test interns must not use `/esc` toward PM for routine confirmations or status. Reserve `/esc` for urgent allowed-direction interruptions such as supervisor corrections.

### 2026-05-20 - PM/secretary durable reporting correction

- PM must not proactively peer_send `intern_code_secretary` for routine milestone reports, status, blockers, summaries, or completion notes.
- Secretary -> PM is the normal direction for supervisor instructions and status questions; PM -> Secretary is not the default routine reporting channel.
- PM-visible reports for secretary/supervisor must be written to durable milestone files, especially `workspace/tasks/milestone1_qwen3_8b_loop/pm_secretary_report.md`, `status.md`, `blockers.md`, and evidence files.
- PM must not use `/esc` toward secretary for routine milestone reports or status.

### 2026-05-20 - PM to dev/test notification channel change

- For PM -> dev/test tasking or correction messages, primary delivery is now direct `tmux send-keys` injection into the target intern pane, followed by Enter.
- `peer_send` is no longer the primary notification method for dev/test assignments because its priority is insufficient for this team workflow.
- PM should avoid interrupts by default: do not use `C-c`, `/esc`, or other interruption unless the supervisor explicitly asks for urgent interruption, or the target's current behavior would keep wasting resources or continue an incorrect execution.
- After tmux injection, PM must use `tmux capture-pane` to verify that the message was submitted and is not merely sitting in the input line.
- Routine dev/test status and evidence still go to durable files; this change is about PM's outbound task/correction delivery mechanism.
