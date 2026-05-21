# M1-S23-PR55-SFT-WRAPPER-FIX-DEV4 History

<!-- METADATA:SESSION=1 -->

## Session 1 - SFT Wrapper Fix Package - 2026-05-21

- Accepted PM assignment `M1-S23-PR55-SFT-WRAPPER-FIX-DEV4`.
- Reviewed dev_2 PR55 runtime evidence and GPU tracking evidence.
- Diagnosed root cause: an exported LLamaFactory wrapper referenced `DEP_TARGET`, but `DEP_TARGET` was not exported into the `set -u` shell environment seen by the wrapper.
- Patched `scripts/train_qwen3_8b_sft.sh` to default/export `DEP_TARGET`, `LF`, and `LLAMAFACTORY_CLI`, include those values in logs and manifest command, and invoke configurable `"${LLAMAFACTORY_CLI}"`.
- Added static tests in `tests/test_train_qwen3_8b_sft_static.py`.
- Wrote evidence `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr55_sft_wrapper_fix.md`.
- Opened PR #57 `https://github.com/peteryang1/coding_agent_playground/pull/57`; GitHub reports open, non-draft, `MERGEABLE` / `CLEAN`, with no required checks reported.
- No LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run.
