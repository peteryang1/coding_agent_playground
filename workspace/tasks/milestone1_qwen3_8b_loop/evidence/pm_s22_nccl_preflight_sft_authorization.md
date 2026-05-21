# PM S22 NCCL Preflight + Conditional SFT Authorization

Task: `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`
Owner: `intern_code_dev_2`
Authorization timestamp: `2026-05-21T10:53:00Z`

## Decision

`AUTHORIZED_DEV2_ONLY_ONE_FRESH_DIFFERENT_NODE_PREFLIGHT_THEN_CONDITIONAL_SFT`

PM authorizes only `intern_code_dev_2` to submit one fresh LTP allocation for a single-node 8 x H200 run, preferably on a different physical node than the failed post-PR41 node `lg-cmc-b7r202-p07u16-h200-000708`.

The authorized sequence is:

1. Submit/acquire one fresh 8 x H200 LTP allocation.
2. Record job/frame id, node id, endpoint, `nodes.json`, submit/status commands, start time, expected stop time, and stop conditions.
3. Prove all generated artifacts use `/home/xu.yang/coding_agent_playground/outputs` unless an existing required input path is explicitly justified.
4. Run a bounded NCCL/NVLink hardware preflight under `/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>`.
5. If and only if the preflight passes, run exactly one Qwen3-8B ShareGPT SFT smoke on the same allocation.
6. Stop/release the allocation after checkpoint, SFT failure, preflight failure, same-node rejection, idle/health limit, or completion of the single authorized SFT attempt.

No mini-swe eval is authorized by this file.

## Gate Basis

- PR #43 merged at `2026-05-21T10:47:20Z`, merge commit `2c867d3226f7ebb4962b5b173235639df8f1f9be`.
- Completion PR #44 merged at `2026-05-21T10:50:28Z`, merge commit `6dcdc6730debeb2fb875baaec6667cb64d09867d`.
- dev_4 mitigation package recommends a fresh different H200 node plus NCCL/NVLink preflight before SFT.
- dev_2 resource plan confirms no active Milestone GPU is held and prior post-PR41 frame is stopped.
- dev_3 confirms no ShareGPT data/schema change is needed.
- dev_1 records `PASS_FOR_PM_RETRY`.
- test_1 records `PASS_FOR_PM_RETRY`.
- test_2 remains blocked on absent checkpoint/model or served endpoint.

## Required Preflight Evidence

Preflight evidence must include:

- exact commands and environment;
- `hostname`;
- `nvidia-smi -L`;
- `nvidia-smi topo -m`;
- NVLink/NVSwitch health output available on the node;
- ECC/Xid/PCI/NVLink error checks available on the node;
- an 8-rank NCCL all-reduce or equivalent NCCL collective preflight if the tool is available;
- explicit blocker if the NCCL test tool is absent;
- `/home/xu.yang` write/capacity proof for the run output root;
- pass/fail conclusion before any SFT command starts.

Preflight fails if any of these appear:

- same physical node as the failed post-PR41 run unless PM explicitly accepts it later;
- missing/unhealthy GPU;
- Xid, fatal ECC, NVLink link error, or PCI fault evidence;
- NCCL/CUDA invalid peer memory signature;
- rank SIGABRT or collective failure;
- inability to write required artifacts under `/home/xu.yang`.

If preflight fails, dev_2 must not run SFT and must stop/release the allocation.

## Conditional SFT Contract

If preflight passes, dev_2 may run one SFT smoke with:

- current `main` including PR #43 and PR #44 merge commits;
- PR39 diagnostics preserved;
- PR41 single-process preprocessing preserved with `preprocessing_num_workers: null` and `dataloader_num_workers: 0`;
- dataset `coding_agent_m1_sft_10_sharegpt`;
- source `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`;
- source sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`;
- output/log/tmp/checkpoint/run metadata/intermediate root under `/home/xu.yang/coding_agent_playground/outputs`;
- NCCL evidence env additions: `NCCL_DEBUG=INFO`, `NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL`, `NCCL_ASYNC_ERROR_HANDLING=1`, `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`, and `CUDA_DEVICE_MAX_CONNECTIONS=1`;
- no default `NCCL_P2P_DISABLE=1`.

`NCCL_P2P_DISABLE=1` remains disallowed unless a later explicit PM/dev_1/test_1 gate accepts it as a degraded diagnostic fallback.

## Required Runtime Evidence

dev_2 must write durable evidence to:

- `evidence/dev_2_s22_nccl_preflight_sft_runtime.md`;
- `evidence/gpu_s22_nccl_preflight_sft_tracking.md`;
- `workspace/interns/intern_code_dev_2/status.md`.

Required next durable outcome:

- complete checkpoint/model with `trainer_state.json`, `all_results.json`, file listing, sizes, checksums or equivalent integrity proof, and stop proof; or
- fresh exact runtime blocker with command, logs, node status, preflight result, owner, stop proof, and next fix.

PM did not run LTP, GPU, NCCL preflight, SFT, eval, remote workspace code, or dry-run launch for this authorization.
