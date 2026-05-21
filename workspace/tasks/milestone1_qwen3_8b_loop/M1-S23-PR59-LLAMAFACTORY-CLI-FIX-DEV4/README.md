# M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4

<!-- METADATA:STATUS=InProgress,ASSIGNEE=intern_code_dev_4 -->

Owner: `intern_code_dev_4`

Evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr59_llamafactory_cli_fix.md`

Acceptance:

- Cite dev_2 PR59 runtime logs/evidence for `EXIT_STATUS=127`.
- Explain why a space-containing `LLAMAFACTORY_CLI` command string failed when executed as one quoted path.
- Patch or propose safe command-plus-args support or a real executable wrapper path.
- Preserve `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, `MCORE_ADAPTER_DIR`, no remote source/dependency downloads, and `/home/xu.yang/coding_agent_playground/outputs`.
- Include static/unit evidence if code changes.
- Do not run LTP/GPU/preflight/SFT/eval/dry-run/runtime.

Completion marker: patch PR open and waiting for PM gate; complete only after PM-gated owner self-merge plus durable completion record.

PR: https://github.com/peteryang1/coding_agent_playground/pull/61

PR state at recording check: open, non-draft, `MERGEABLE` / `CLEAN`; waiting for PM gate before any owner self-merge.
