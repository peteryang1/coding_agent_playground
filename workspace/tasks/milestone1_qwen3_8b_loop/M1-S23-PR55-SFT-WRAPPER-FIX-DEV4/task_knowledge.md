# M1-S23-PR55-SFT-WRAPPER-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

1. PR55 preflight passed and SFT was attempted once, but training did not start because the LLamaFactory wrapper environment failed with `DEP_TARGET: unbound variable`.
2. The launcher should explicitly default/export wrapper variables before invoking LLamaFactory: `DEP_TARGET`, `LF`, and `LLAMAFACTORY_CLI`.
3. Generated artifacts, logs, checkpoints, run metadata, temporary data, and dependency target defaults should remain under `/home/xu.yang/coding_agent_playground/outputs`.
4. GPU-node runtime must continue to use local transferred source/data/dependency bundles with checksum proof and no remote GitHub/source/dependency network.
5. Dev_4 did not run LTP/GPU/preflight/SFT/eval/dry-run/runtime for this task.
6. PR #57 is open for this wrapper env fix and must wait for PM gate before any owner self-merge.
