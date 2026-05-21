# M1-S23-PR57-MCORE-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=3 -->

1. PR57 runtime blocker is dependency/environment-side: `USE_MCA=1` requires `mcore_adapter`, and the single authorized SFT attempt failed before checkpoint creation because `mcore_adapter` was not importable.
2. The preferred fix is to keep the MCA path and stage `mcore_adapter` through a local/provided checksum-verified bundle under `code/mcore_adapter`, then expose it through `MCORE_ADAPTER_DIR`/`PYTHONPATH`.
3. Non-MCA is a fallback only with explicit PM/dev_1/test_1 approval because it changes the backend and parallelism assumptions for Qwen3-8B.
4. Dev_4 did not run LTP/GPU/preflight/SFT/eval/dry-run/runtime for this task.
5. PR #59 PM gate passed for owner self-merge only; runtime remains separately gated and no LTP/GPU/preflight/SFT/eval/runtime retry is authorized by the merge gate.
6. PR #59 merged at `2026-05-21T16:34:13Z` with merge commit `8ed6248cd7bd56b89ac1124689fed0b56e4eba02`; the task is complete as a no-execution launcher/dependency fix package.
