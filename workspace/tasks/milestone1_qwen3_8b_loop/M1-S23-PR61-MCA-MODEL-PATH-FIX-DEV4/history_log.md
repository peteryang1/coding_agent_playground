# History Log - M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4

## Session 1 - Assignment and Patch Package - 2026-05-21

- Accepted PM task `M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4`.
- Reviewed dev_2 PR61 runtime evidence and GPU tracking evidence.
- Diagnosed the blocker: generated runtime YAML had `model_name_or_path`, but direct execution of `llamafactory/launcher.py train config.yaml` bypassed `launcher.launch()`, leaving `train` as `sys.argv[1]`; LLamaFactory `read_args()` therefore did not load the YAML and raised `ValueError: Please provide model_name_or_path`.
- Patched `scripts/train_qwen3_8b_sft.sh` so direct `llamafactory/launcher.py` command strings are normalized to `python3 -m llamafactory.cli` before appending `train <runtime_config>`.
- Preserved PR61 command-array parsing, `mcore_adapter` path handling, no-remote-network staging, and `/home/xu.yang/coding_agent_playground/outputs`.
- Added static tests in `tests/test_train_qwen3_8b_sft_static.py`.
- Local/static checks passed: `bash -n scripts/train_qwen3_8b_sft.sh`; `python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q`.
- No LTP/GPU/preflight/SFT/eval/dry-run/remote command was run.
- Opened PR #63 `https://github.com/peteryang1/coding_agent_playground/pull/63`.
- GitHub reports PR #63 open, non-draft, `MERGEABLE` / `CLEAN`.
- Waiting for PM gate before any owner self-merge.

## Session 2 - PM Gate Pass and Completion - 2026-05-21

- PM gate passed for PR #63 at head `a0ab039278198a6c1b0cd40009038d89cd602922`.
- Gate basis: PM evidence commit `838ffa3`; dev_1 `M1-S23-PR61-MCA-MODEL-PATH-REVIEW-DEV1 = PASS_FOR_PM_RETRY`; test_1 `M1-S23-PR61-MCA-MODEL-PATH-GATE-TEST1 = PASS_FOR_PM_RETRY`; GitHub open/non-draft `MERGEABLE` / `CLEAN`.
- Self-merged PR #63 at `2026-05-21T18:08:48Z`.
- Merge commit: `2f89e9234bb5f9dfdcc433a30bc0f6dcfd9a8689`.
- Marked task `M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4` complete/ready-for-runtime-gate.
- This gate and completion do not authorize LTP/GPU/transfer/preflight/SFT/eval/runtime.
