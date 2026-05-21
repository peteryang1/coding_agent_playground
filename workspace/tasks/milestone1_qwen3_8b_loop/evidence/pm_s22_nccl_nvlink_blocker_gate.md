# PM S22 NCCL/NVLink Blocker Gate

Owner: `intern_code_pm`
Date: 2026-05-21
Fresh blocker: `BLOCKED_POSTPR41_RUNTIME_NCCL_NVLINK_PEER_MEMORY`

## Current Runtime Result

`M1-S22-POSTPR41-SFT-RUNTIME-DEV2` completed with final runtime evidence and stop proof.

- Frame: `xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z`.
- Endpoint while active: `ssh -p 27021 root@10.100.22.14`.
- Node: `lg-cmc-b7r202-p07u16-h200-000708`.
- Output root: `/home/xu.yang/coding_agent_playground/outputs`.
- Stop proof: `STOPPED (Completed)`, completed `2026-05-21 10:17:58`, endpoint refused after stop.

The run cleared the previous dataset-map blocker:

- PR #41 merge commit `2fc4b797a85c9375c6c5e1171963abe67aab35e8` was used.
- Runtime config/manifest recorded `preprocessing_num_workers: null`.
- ShareGPT conversion completed `10/10`.
- Training startup was reached.
- Old `KeyError: from`, ENOSPC, and `num_proc=4` SyncManager EOF signatures were absent.

The run did not produce checkpoint/model:

- `EXIT_STATUS=1`.
- Fresh blocker: CUDA/NCCL `Invalid access of peer GPU memory over nvlink or a hardware error` / local rank 5 `SIGABRT`.
- No complete checkpoint/model.
- No `trainer_state.json`.
- No `all_results.json`.
- Eval handoff remains blocked.

## PM Decision

No new LTP/SFT/GPU/eval retry is authorized.

PM creates a no-execution mitigation gate before any fresh runtime authorization:

- `M1-S22-NCCL-MITIGATION-DEV4`
- `M1-S22-NCCL-RESOURCE-DEV2`
- `M1-S22-NCCL-DATA-CONFIRM-DEV3`
- `M1-S22-NCCL-REVIEW-DEV1`
- `M1-S22-NCCL-GATE-TEST1`
- `M1-S22-POSTPR41-EVAL-BLOCKED-TEST2`

## Required Next Decision

Owners must determine whether the next attempt should use:

- a different H200 node;
- adjusted NCCL/NVL environment or launcher settings;
- a minimal no-training NCCL/hardware preflight before SFT;
- or another bounded mitigation with explicit risk/acceptance criteria.

Any future runtime must preserve PR39 diagnostics, PR41 single-process preprocessing, and `/home/xu.yang` intermediates.

## PM Boundary

PM did not run LTP, SFT, GPU, remote workspace code, or eval.
