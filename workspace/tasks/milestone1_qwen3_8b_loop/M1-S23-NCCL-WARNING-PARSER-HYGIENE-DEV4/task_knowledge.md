# M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

1. `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings are benign only when the same all-reduce source reports `TORCHRUN_EXIT=0` and `ALLREDUCE_OK`.
2. Real NCCL/CUDA invalid peer memory, unhandled system error, collective failures, nonzero torchrun exits, SIGABRT, ChildFailedError, Xid/SXid/ECC, and NVLink faults remain actionable.
3. Suppressed deprecation warnings are retained as non-actionable matches with reason `benign_nccl_async_error_handling_deprecation_warning` for auditability.
4. PR #53 was PM-gated and self-merged at `2026-05-21T14:20:56Z`; merge commit `e29c93736be3384663cad953cd18da68c30070fb`.
