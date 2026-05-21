# M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=2 -->

1. PR59 runtime blocker is launcher-side: a space-containing `LLAMAFACTORY_CLI` value must be executed as command plus args, not as one quoted executable path.
2. Bash arrays are the preferred fix for the launcher invocation because they preserve a real executable path and its fixed args while safely appending `train "${RUNTIME_CONFIG}"`.
3. The patch preserves `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, `MCORE_ADAPTER_DIR`, no-remote-network dependency staging, and `/home/xu.yang/coding_agent_playground/outputs`.
4. Dev_4 did not run LTP/GPU/preflight/SFT/eval/dry-run/runtime for this task.
5. PR #61 PM gate passed for owner self-merge only; runtime remains separately gated and no LTP/GPU/preflight/SFT/eval/runtime retry is authorized by the merge gate.
6. PR #61 merged at `2026-05-21T17:13:17Z` with merge commit `aa426b045b52b71bc23b4a2f73f3ee1c42187037`; the task is complete as a no-execution launcher command invocation fix.
