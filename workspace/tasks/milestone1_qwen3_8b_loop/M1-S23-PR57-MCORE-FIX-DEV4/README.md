# M1-S23-PR57-MCORE-FIX-DEV4

<!-- METADATA:STATUS=InProgress,ASSIGNEE=intern_code_dev_4 -->

Owner: `intern_code_dev_4`

Evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr57_mcore_fix.md`

Acceptance:

- Cite dev_2 PR57 runtime logs/evidence for `ImportError: mcore_adapter is required when USE_MCA=1`.
- Explain why the MCA path requires `mcore_adapter`.
- Patch or propose the dependency bundle/base-image/launch-config path, or explicitly justify a non-MCA fallback.
- Preserve no-remote-network local bundle transfer and `/home/xu.yang/coding_agent_playground/outputs` generated-artifact rules.
- Include static/unit evidence if code changes.
- Do not run LTP/GPU/preflight/SFT/eval/dry-run/runtime.

Completion marker: patch PR open and waiting for PM gate, or complete only after PM-gated owner self-merge plus durable completion record.

PR: https://github.com/peteryang1/coding_agent_playground/pull/59

PR state at recording check: open, non-draft, `MERGEABLE` / `CLEAN`; waiting for PM gate before any owner self-merge.
