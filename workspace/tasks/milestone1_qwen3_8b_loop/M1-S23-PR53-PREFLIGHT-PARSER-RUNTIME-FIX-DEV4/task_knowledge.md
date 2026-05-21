# M1-S23-PR53-PREFLIGHT-PARSER-RUNTIME-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=2 -->

1. Real PR53 preflight artifacts can split `NCCL_ASYNC_ERROR_HANDLING` warning lines from the `TORCHRUN_EXIT=0` and `ALLREDUCE_OK` proof.
2. Benign deprecation-warning suppression should use preflight-level torch/NCCL/allreduce success context, but only for `NCCL_ASYNC_ERROR_HANDLING` deprecation-warning lines.
3. Real Xid/SXid/ECC/NVLink/NCCL/CUDA failures, nonzero torchrun exit, SIGABRT, and ChildFailedError remain actionable.
4. Dev_4 did not run LTP/GPU/preflight/SFT/eval/dry-run/runtime for this task.
5. PR #55 was PM-gated and self-merged at `2026-05-21T14:49:25Z`; merge commit `1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703`.
