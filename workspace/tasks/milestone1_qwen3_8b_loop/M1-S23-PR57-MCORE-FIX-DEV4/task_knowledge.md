# M1-S23-PR57-MCORE-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

1. PR57 runtime blocker is dependency/environment-side: `USE_MCA=1` requires `mcore_adapter`, and the single authorized SFT attempt failed before checkpoint creation because `mcore_adapter` was not importable.
2. The preferred fix is to keep the MCA path and stage `mcore_adapter` through a local/provided checksum-verified bundle under `code/mcore_adapter`, then expose it through `MCORE_ADAPTER_DIR`/`PYTHONPATH`.
3. Non-MCA is a fallback only with explicit PM/dev_1/test_1 approval because it changes the backend and parallelism assumptions for Qwen3-8B.
4. Dev_4 did not run LTP/GPU/preflight/SFT/eval/dry-run/runtime for this task.
