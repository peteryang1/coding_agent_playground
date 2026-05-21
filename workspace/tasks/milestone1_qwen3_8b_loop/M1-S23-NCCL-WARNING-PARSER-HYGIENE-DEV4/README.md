# M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4

<!-- METADATA:STATUS=Completed,ASSIGNEE=intern_code_dev_4 -->

Owner: `intern_code_dev_4`

Evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_nccl_warning_parser_hygiene.md`

PR: #53 `https://github.com/peteryang1/coding_agent_playground/pull/53` (merged at `2026-05-21T14:20:56Z`, merge commit `e29c93736be3384663cad953cd18da68c30070fb`)

Acceptance:

- Suppress `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings only when the same all-reduce source reports `TORCHRUN_EXIT=0` and `ALLREDUCE_OK`.
- Preserve real NCCL/CUDA invalid peer memory, unhandled system error, collective failure, nonzero torchrun exit, SIGABRT, ChildFailedError, Xid/SXid/ECC/NVLink detection.
- Add synthetic tests or static test evidence.
- State no LTP/GPU/preflight/SFT/eval/dry-run/runtime execution is authorized.

Completion marker: complete after PM-gated owner self-merge. Runtime remains separately PM-gated; no LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run for completion.
