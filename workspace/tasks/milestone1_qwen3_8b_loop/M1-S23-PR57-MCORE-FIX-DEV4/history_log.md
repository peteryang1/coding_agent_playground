# M1-S23-PR57-MCORE-FIX-DEV4 History

<!-- METADATA:SESSION=2 -->

## Session 1 - MCORE Dependency Fix Package - 2026-05-21

- Accepted PM assignment `M1-S23-PR57-MCORE-FIX-DEV4`.
- Reviewed PM durable dev_2 PR57 runtime evidence: structured preflight passed and one SFT attempt exited with `ImportError: mcore_adapter is required when USE_MCA=1`; no checkpoint/model, `trainer_state.json`, `all_results.json`, or eval artifact exists.
- Patched `scripts/train_qwen3_8b_sft.sh` to default/export `MCORE_ADAPTER_DIR`, include a local `code/mcore_adapter` bundle in `PYTHONPATH`, record the path in the manifest launch command, and fail early with an explicit dependency-bundle message if `USE_MCA=1` cannot import `mcore_adapter`.
- Patched `scripts/write_sft_run_manifest.py` to record `MCORE_ADAPTER_DIR` and `PYTHONPATH_PREFIX`.
- Added static launcher test coverage in `tests/test_train_qwen3_8b_sft_static.py`.
- Updated PR #59 `https://github.com/peteryang1/coding_agent_playground/pull/59` to include task id `M1-S23-PR57-MCORE-FIX-DEV4`; GitHub reports open, non-draft, `MERGEABLE` / `CLEAN`.
- No LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run.

## Session 2 - Hook Compliance Record - 2026-05-21

- Added this Session 2 record after stop-hook validation required `M1-S23-PR57-MCORE-FIX-DEV4/history_log.md` to explicitly include Session 2.
- Confirmed PR #59 remains the active PR for `M1-S23-PR57-MCORE-FIX-DEV4`.
- No code, config, runtime behavior, or evidence conclusion changed in this compliance update.
- No LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run.
