# PM Session 23 PR63 Preflight/SFT Authorization

Task: `M1-S23-PR63-PREFLIGHT-SFT-RUNTIME-DEV2`
Owner: `intern_code_dev_2`
Authorization time: 2026-05-21

## Authorization

PM authorizes exactly one fresh owner-executed PR63/PR64 preflight plus conditional SFT smoke attempt for `intern_code_dev_2`.

Eval is not authorized. PM will not run LTP, remote commands, transfer, preflight, SFT, eval, or stop commands personally.

## Required Source State

- PR #63 merged at `2026-05-21T18:08:48Z`, merge commit `2f89e9234bb5f9dfdcc433a30bc0f6dcfd9a8689`.
- Completion PR #64 merged at `2026-05-21T18:12:07Z`, merge commit `7ad24ae328a350c0be596f41ea143affb4034486`.
- Runtime source commit must be `origin/main` at `7ad24ae328a350c0be596f41ea143affb4034486` unless dev_2 records an exact blocker before submit.
- PR63 fix to verify during runtime: direct `*/llamafactory/launcher.py` invocation is normalized to `python3 -m llamafactory.cli`, preserving PR61 command-array parsing and allowing `model_name_or_path` from runtime YAML to bind.

## Mandatory Runtime Gates

Dev_2 must record all of the following in durable evidence before claiming SFT was gateable:

- Local/provided workspace preparation for code/config/scripts/data/dependencies; no remote GitHub/source/dependency clone, fetch, or download on the GPU/LTP node.
- Exact source bundle commit, file list, and checksum.
- Exact ShareGPT dataset path, row count, and checksum, expected checksum `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Exact `mcore_adapter` and local dependency bundle provenance, file list, checksum, destination, `MCORE_ADAPTER_DIR`, and `mcore_adapter import OK for USE_MCA=1`.
- Exact transfer command, destination paths, post-transfer checksum/file-count verification, and proof that remote source/dependency network was not used.
- Generated outputs, logs, temporary converted datasets, checkpoints, metadata, and later eval intermediates under `/home/xu.yang/coding_agent_playground/outputs` unless a required existing input path is explicitly justified.
- Structured preflight result with `PREFLIGHT_RESULT=PASS`, `SFT_ALLOWED=true`, capacity/home-storage/topology/NVLink/all-reduce status, and any skip reason if not allowed.
- PR63 launcher verification logs: original command, normalization status, final parsed command, generated runtime YAML path, and whether the previous `ValueError: Please provide model_name_or_path` recurs.
- If SFT is allowed, exactly one SFT smoke attempt result: command, exit status, checkpoint/model/trainer_state/all_results presence or exact runtime blocker.
- Final LTP/resource stop proof: job/frame id, node id, endpoint, final state, endpoint refusal or equivalent stop proof, and no running `coding-agent-playground` jobs.

## Boundary

This authorization is consumed by one fresh dev_2 attempt only. Any failed preflight, failed SFT, missing checkpoint, resource placement issue, or stopped/released blocker requires fresh PM decision before another LTP/GPU/preflight/SFT/eval attempt.
