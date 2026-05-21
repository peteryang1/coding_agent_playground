# M1-S23-PR57-MCORE-FIX-DEV4

<!-- METADATA:STATUS=Completed,ASSIGNEE=intern_code_dev_4 -->

Owner: `intern_code_dev_4`

Evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr57_mcore_fix.md`

Acceptance:

- Cite dev_2 PR57 runtime logs/evidence for `ImportError: mcore_adapter is required when USE_MCA=1`.
- Explain why the MCA path requires `mcore_adapter`.
- Patch or propose the dependency bundle/base-image/launch-config path, or explicitly justify a non-MCA fallback.
- Preserve no-remote-network local bundle transfer and `/home/xu.yang/coding_agent_playground/outputs` generated-artifact rules.
- Include static/unit evidence if code changes.
- Do not run LTP/GPU/preflight/SFT/eval/dry-run/runtime.

Completion marker: complete after PM-gated PR #59 owner self-merge; runtime remains separately PM-gated.

PR: https://github.com/peteryang1/coding_agent_playground/pull/59

PR state at PM gate: open, non-draft, `MERGEABLE` / `CLEAN`; PM authorized owner self-merge only.
