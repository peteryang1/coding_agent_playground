# PM Authorization: M1-S23-PARSERPATCH-PREFLIGHT-SFT-RUNTIME-DEV2

Timestamp: `2026-05-21T12:45:00Z`

Owner: `intern_code_dev_2`

Authorized scope:

- Submit one fresh preferably different-node single-node 8xH200 LTP allocation.
- Run the PR #49 parser-patch preflight.
- Run one Qwen3-8B ShareGPT SFT smoke only if structured preflight result is `PASS` and `sft_allowed=true`.
- Stop/release the node after checkpoint, failure, blocker, idle/resource condition, or PM/test stop condition.

Not authorized:

- mini-swe eval.
- Any second retry.
- Remote GitHub clone/fetch/download or remote dependency download.
- PM-run SSH/LTP/GPU/preflight/SFT/eval commands.

Gate basis:

- PR #49 merged at `2026-05-21T12:44:14Z`.
- PR #49 merge commit: `2de4bab2248f052d09f118eb6c28c48231f3d719`.
- dev_1 `M1-S23-PARSERPATCH-REVIEW-DEV1`: `PASS_FOR_PM_RETRY` after head refresh.
- test_1 `M1-S23-PARSERPATCH-GATE-TEST1`: `PASS_FOR_PM_RETRY` after head refresh.
- dev_2 `M1-S23-PARSERPATCH-RUNTIME-READY-DEV2`: complete no-submit readiness.
- dev_3 `M1-S23-PARSERPATCH-DATA-STAGING-DEV3`: data-ready, no data-side blocker.
- test_2 `M1-S23-PARSERPATCH-EVAL-READY-TEST2`: eval-ready but blocked until checkpoint/model exists.

Mandatory runtime evidence:

- LTP frame/job id, node id, endpoint, start/end timestamps, submit/status/stop commands, and final stop proof.
- Local/provided-workspace source commit `2de4bab2248f052d09f118eb6c28c48231f3d719`.
- File list and sha256 checksums verified before transfer.
- Exact `rsync`, `scp`, or tar-over-SSH transfer command, destination path, and post-transfer verification.
- Statement and evidence that no remote `git clone`, `git fetch`, GitHub download, `pip` download, or external network source/dependency fetch was used on the GPU node.
- Generated artifact root under `/home/xu.yang/coding_agent_playground/outputs`.
- Capacity proof, topology/NVLink capture, torch NCCL all-reduce, parser `health_status.json/txt`, structured `preflight_result`, `sft_allowed`, and `home_xu_yang_storage_status`.
- Exact SFT command/config/env if and only if preflight PASS and `sft_allowed=true`.
- Complete checkpoint/model path or exact runtime blocker.
- `trainer_state.json` and `all_results.json` presence/absence.

Required next durable outcome:

- SFT checkpoint/model with `trainer_state.json` and `all_results.json`, or a fresh exact runtime blocker with logs, command, owner, node/job state, stop proof, and next fix.
