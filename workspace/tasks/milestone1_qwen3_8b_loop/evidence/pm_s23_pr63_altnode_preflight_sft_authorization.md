# PM Session 23 PR63 Alternate-Node Preflight/SFT Authorization

Task: `M1-S23-PR63-ALTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`
Owner: `intern_code_dev_2`
Authorization time: 2026-05-21

## Decision

PM authorizes exactly one fresh bounded alternate-node owner-executed preflight plus conditional SFT smoke attempt for `intern_code_dev_2`.

The immediately prior different-node attempt proved the PR63 code/data/package path progressed further: placement was non-forbidden, `/home/xu.yang` storage passed, transfer/import/preflight passed, `PREFLIGHT_RESULT=PASS`, `SFT_ALLOWED=true`, and SFT reached distributed training. It then failed with CUDA/NCCL peer-memory hardware error on node `lg-cmc-b7r202-q04u06-h200-000725`. No checkpoint/model/trainer_state/all_results exists, and the node was stopped/released.

## Hard Boundaries

- Eval is not authorized.
- PM will not run LTP, remote commands, transfer, preflight, SFT, eval, or stop commands personally.
- Forbidden nodes for this attempt:
  - `lg-cmc-b7r202-k07u06-h200-000580`
  - `lg-cmc-b7r202-q04u06-h200-000725`
- If LTP assigns any forbidden node, dev_2 must stop/release before transfer, preflight, SFT, or eval and record placement blocker evidence.
- If LTP assigns a different node, dev_2 may proceed with local/provided bundle transfer, `/home/xu.yang` proof, structured preflight, and SFT only if `PREFLIGHT_RESULT=PASS` plus `SFT_ALLOWED=true`.

## Required Evidence

Dev_2 must record:

- New frame/job id, endpoint, node id, and placement decision against the forbidden-node set.
- Runtime source commit `7ad24ae328a350c0be596f41ea143affb4034486`.
- Reused or regenerated local/provided source/data/`mcore_adapter` bundle paths, file lists, checksums, transfer commands, and post-transfer verification.
- No remote GitHub/source/dependency clone, fetch, or download on the GPU/LTP node.
- `/home/xu.yang/coding_agent_playground/outputs` proof and capacity probe.
- `mcore_adapter import OK for USE_MCA=1`.
- Structured preflight output and final gate result.
- If SFT runs, PR63 launcher normalization logs, checkpoint/model/trainer_state/all_results presence or exact blocker.
- Stop/release proof and no running `coding-agent-playground` jobs.

This authorization is consumed by one fresh attempt only.
