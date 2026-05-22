# intern_code_pm - 个人知识库

<!-- METADATA:SESSION=24 -->

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

- Superseded by the 2026-05-22 peer_send policy below. Do not treat this tmux-primary rule as current for normal intern communication.

### 2026-05-22 - Latest peer_send policy

- Latest supervisor policy: `peer_send` is active for normal intern communication.
- `intern_code_secretary` and `intern_code_pm` should use peer_send for intern communication instead of tmux inject for normal messages.
- Secretary may use `peer_send mode=goal` when directing PM if needed.
- All other interns, including PM/dev/test, must not use goal mode; use default/next as appropriate.
- Do not use tmux inject for normal policy relay or routine intern communication under this updated policy.

### 2026-05-20 - PR gate and owner self-merge correction

- A PR that is ready, mergeable, and passes PM gate should not wait for the full milestone to complete before merge.
- PM's responsibility is to gate PR readiness, record whether the PR is mergeable, and identify concrete blockers if it is not ready.
- When a PR passes gate, PM should notify the corresponding PR owner via tmux inject to follow the playbook and self-merge.
- PM should not merge another owner's PR. The PR owner performs the merge and records the result in durable status/evidence.
- If PM owns a PR, PM must still audit readiness and only self-merge when the PR is ready/mergeable and the merge does not falsely mark the milestone complete.
