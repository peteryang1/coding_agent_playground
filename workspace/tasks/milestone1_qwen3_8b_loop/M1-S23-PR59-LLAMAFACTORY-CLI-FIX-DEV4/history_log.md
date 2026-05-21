# M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4 History

<!-- METADATA:SESSION=1 -->

## Session 1 - LLamaFactory CLI Command-String Fix - 2026-05-21

- Accepted PM assignment `M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4`.
- Reviewed PM durable dev_2 PR59 runtime evidence: transfer/import/preflight passed and one SFT attempt exited `127` because `LLAMAFACTORY_CLI` was set to `python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py` and executed as one quoted path.
- Patched `scripts/train_qwen3_8b_sft.sh` to parse `LLAMAFACTORY_CLI` into `LLAMAFACTORY_CMD` with Bash `read -r -a`, render it for logs/manifests with `%q`, and execute `"${LLAMAFACTORY_CMD[@]}" train "${RUNTIME_CONFIG}"`.
- Added static launcher test coverage in `tests/test_train_qwen3_8b_sft_static.py`.
- Opened PR #61 `https://github.com/peteryang1/coding_agent_playground/pull/61`; GitHub reports open, non-draft, `MERGEABLE` / `CLEAN`.
- No LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run.
