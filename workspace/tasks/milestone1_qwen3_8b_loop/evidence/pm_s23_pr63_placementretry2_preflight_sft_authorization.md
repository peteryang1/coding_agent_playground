# PM Authorization: M1-S23-PR63-PLACEMENTRETRY2-PREFLIGHT-SFT-RUNTIME-DEV2

Timestamp: 2026-05-21T18:59:30Z

Owner: `intern_code_dev_2`

Authorization scope: exactly one fresh bounded placement-retry allocation, then preflight plus conditional SFT only if placement and gates pass.

## Basis

- PR63/PR64 source commit remains `7ad24ae328a350c0be596f41ea143affb4034486`.
- First PR63 post-merge runtime stopped before SFT on node-health signature SXid 22013 at `lg-cmc-b7r202-k07u06-h200-000580`.
- PR63 different-node runtime reached SFT on `lg-cmc-b7r202-q04u06-h200-000725` and failed with NCCL/NVLink peer-memory hardware error before checkpoint.
- PR63 alternate-node attempt was assigned back to forbidden node `lg-cmc-b7r202-k07u06-h200-000580` and was correctly stopped before transfer, preflight, SFT, or eval.
- No checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or eval artifact exists.

## Hard Gates

Forbidden nodes:

- `lg-cmc-b7r202-k07u06-h200-000580`
- `lg-cmc-b7r202-q04u06-h200-000725`

If LTP assigns either forbidden node, dev_2 must stop/release before source/data/dependency transfer, `/home/xu.yang` capacity probing, mcore import, structured preflight, SFT, or eval. Record placement blocker and stop proof.

If LTP assigns a different node, dev_2 may proceed only with:

- local/provided source, data, dependency, LLamaFactory, flash-attn, and `mcore_adapter` bundles;
- no remote `git clone`, `git fetch`, GitHub access, source download, dependency download, or remote `pip` download;
- exact source commit, file lists, checksums, transfer command, destination, and post-transfer verification;
- generated outputs under `/home/xu.yang/coding_agent_playground/outputs`;
- `mcore_adapter import OK for USE_MCA=1`;
- structured preflight;
- SFT only if `PREFLIGHT_RESULT=PASS` and `SFT_ALLOWED=true`.

Eval is not authorized.

## Required Evidence

Owner evidence:

- `evidence/dev_2_s23_pr63_placementretry2_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr63_placementretry2_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`

Required fields:

- LTP job/frame/node/endpoint and exact submit/status/stop commands;
- placement decision against both forbidden nodes;
- if stopped due forbidden placement: final LTP state, endpoint refused or equivalent release proof, and no running `coding-agent-playground` jobs;
- if non-forbidden: transfer/checksum/file-list evidence, no remote source/dependency network proof, `/home/xu.yang` proof/capacity, mcore import, structured preflight, SFT command/result, checkpoint/model or exact blocker, `trainer_state.json`, `all_results.json`, eval absence, stop proof, and no running jobs.

Fresh PM authorization is required after this attempt before any additional LTP/GPU/preflight/SFT/eval work.
