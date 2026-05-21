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
