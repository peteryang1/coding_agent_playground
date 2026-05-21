# M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4

- Owner: `intern_code_dev_4`
- Scope: no-execution launcher fix package for PR61 runtime blocker `BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE`.
- Acceptance criteria:
  - Cite dev_2 PR61 runtime/tracking evidence.
  - Explain why generated YAML contained `model_name_or_path` while LLamaFactory/MCA parser still saw it as missing.
  - Patch or propose a minimal launcher/config/MCA parser fix.
  - Preserve PR61 `LLAMAFACTORY_CLI` command parsing, `mcore_adapter`, no remote source/dependency downloads, and `/home/xu.yang/coding_agent_playground/outputs`.
  - Include local/static/unit checks if code changes.
  - Run no LTP/GPU/preflight/SFT/eval/dry-run/remote command.
- Durable evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr61_mca_model_path_fix.md`
- Completion marker: `complete/ready-for-runtime-gate` only after PM gate and owner self-merge; runtime remains separately PM-gated.

## Status

- 2026-05-21: Package prepared with launcher normalization patch and static tests. PR #63 is open/non-draft and GitHub reports `MERGEABLE` / `CLEAN`; waiting for PM gate before any owner self-merge.
