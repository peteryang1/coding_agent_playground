# M1-S23-PR57-MCORE-FIX-DEV4 History

<!-- METADATA:SESSION=3 -->

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

## Session 3 - PM Gate Pass and Owner Self-Merge Prep - 2026-05-21

- PM gate passed for PR #59 / `M1-S23-PR57-MCORE-FIX-DEV4`; PM observed GitHub open, non-draft, `MERGEABLE` / `CLEAN` at head `b0b54279bcf87add7e617b0c08686c40fac41b48`, with functional patch commit `92e437cf690b68121b9ad9d2f76b18a60a10a2d6`.
- PM reported dev_1 and test_1 both recorded `PASS_FOR_PM_RETRY` in durable evidence.
- Recorded pre-merge completion state before owner self-merge per playbook.
- This gate authorizes PR #59 owner self-merge only; it does not authorize LTP/GPU/preflight/SFT/eval/runtime retry.
- Self-merged PR #59 at `2026-05-21T16:34:13Z`; merge commit `8ed6248cd7bd56b89ac1124689fed0b56e4eba02`.
- Task `M1-S23-PR57-MCORE-FIX-DEV4` is complete as a no-execution launcher/dependency fix package.
- Runtime remains separately PM-gated; no LTP/GPU/preflight/SFT/eval/runtime retry was run.
