# M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4

<!-- METADATA:STATUS=Completed,ASSIGNEE=intern_code_dev_4 -->

Owner: `intern_code_dev_4`

Evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr59_llamafactory_cli_fix.md`

Acceptance:

- Cite dev_2 PR59 runtime logs/evidence for `EXIT_STATUS=127`.
- Explain why a space-containing `LLAMAFACTORY_CLI` command string failed when executed as one quoted path.
- Patch or propose safe command-plus-args support or a real executable wrapper path.
- Preserve `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, `MCORE_ADAPTER_DIR`, no remote source/dependency downloads, and `/home/xu.yang/coding_agent_playground/outputs`.
- Include static/unit evidence if code changes.
- Do not run LTP/GPU/preflight/SFT/eval/dry-run/runtime.

Completion marker: complete after PM-gated PR #61 owner self-merge; runtime remains separately PM-gated.

PR: https://github.com/peteryang1/coding_agent_playground/pull/61

PR state at PM gate: open, non-draft, `MERGEABLE` / `CLEAN`; PM authorized owner self-merge only.

Merged: `2026-05-21T17:13:17Z`

Merge commit: `aa426b045b52b71bc23b4a2f73f3ee1c42187037`
