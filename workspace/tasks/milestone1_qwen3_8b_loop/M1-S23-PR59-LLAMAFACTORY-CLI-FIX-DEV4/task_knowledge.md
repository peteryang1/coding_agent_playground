# M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

1. PR59 runtime blocker is launcher-side: a space-containing `LLAMAFACTORY_CLI` value must be executed as command plus args, not as one quoted executable path.
2. Bash arrays are the preferred fix for the launcher invocation because they preserve a real executable path and its fixed args while safely appending `train "${RUNTIME_CONFIG}"`.
3. The patch preserves `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, `MCORE_ADAPTER_DIR`, no-remote-network dependency staging, and `/home/xu.yang/coding_agent_playground/outputs`.
4. Dev_4 did not run LTP/GPU/preflight/SFT/eval/dry-run/runtime for this task.
