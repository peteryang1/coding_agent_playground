# M1-S22-NCCL-MITIGATION-DEV4

<!-- METADATA:STATUS=Completed,ASSIGNEE=intern_code_dev_4 -->

## Background

The post-PR41 authorized SFT run cleared PR39 diagnostics, PR41 single-process preprocessing, ShareGPT conversion, and training startup, then failed before checkpoint save with CUDA/NCCL invalid peer GPU memory over NVLink or hardware error on local rank 5.

## Acceptance Criteria

- Cite dev_2/test_1 final runtime evidence.
- Preserve PR39 diagnostics, PR41 `preprocessing_num_workers: null`, and `/home/xu.yang` output paths.
- Propose exact NCCL/NVL/launcher or hardware-preflight mitigation.
- State whether a different H200 node is required.
- List future command/config/env changes.
- Do not run LTP/SFT/GPU/NCCL preflight/eval/dry-run launch.

## Completion

PR #43 merged at `2026-05-21T10:47:20Z` with merge commit `2c867d3226f7ebb4962b5b173235639df8f1f9be`.

Completion marker: complete/ready-for-runtime-gate.
