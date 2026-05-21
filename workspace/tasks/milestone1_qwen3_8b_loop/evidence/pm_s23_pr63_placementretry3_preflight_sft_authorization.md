# PM Authorization: M1-S23-PR63-PLACEMENTRETRY3-PREFLIGHT-SFT-RUNTIME-DEV2

Timestamp: 2026-05-21T19:06:30Z

Owner: `intern_code_dev_2`

Authorization scope: exactly one final bounded placement retry before classifying a repeated LTP placement/resource blocker.

## Basis

- Current source commit remains `7ad24ae328a350c0be596f41ea143affb4034486`.
- Prior PR63 runtime attempts proved local/provided bundle reuse, no-remote-network staging, `/home/xu.yang` path policy, and SFT launch path until resource failures.
- `M1-S23-PR63-ALTNODE-PREFLIGHT-SFT-RUNTIME-DEV2` landed on forbidden node `lg-cmc-b7r202-k07u06-h200-000580` and was stopped before transfer/preflight/SFT/eval.
- `M1-S23-PR63-PLACEMENTRETRY2-PREFLIGHT-SFT-RUNTIME-DEV2` landed on forbidden node `lg-cmc-b7r202-q04u06-h200-000725` and was stopped before transfer/preflight/SFT/eval.
- No checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or eval artifact exists.

## Required Before Submit

dev_2 must record whether the available LTP interface supports any node exclusion, queue/constraint, or placement-affinity option for this workflow. If unsupported or unknown, record that explicitly and proceed with the single bounded submit below. PM is not asking dev_2 to contact other teams or use peer messages.

## Hard Gates

Forbidden nodes:

- `lg-cmc-b7r202-k07u06-h200-000580`
- `lg-cmc-b7r202-q04u06-h200-000725`

If LTP assigns either forbidden node, stop/release before source/data/dependency transfer, `/home/xu.yang` capacity probing, mcore import, structured preflight, SFT, or eval. Record placement blocker, LTP placement-mechanism finding, stop proof, endpoint refusal, and no running jobs.

If LTP assigns a different node, proceed only with:

- local/provided bundles only;
- no remote `git clone`, `git fetch`, GitHub access, source download, dependency download, or remote `pip` download;
- exact source commit, file lists, checksums, transfer command, destination, and post-transfer verification;
- generated outputs under `/home/xu.yang/coding_agent_playground/outputs`;
- `mcore_adapter import OK for USE_MCA=1`;
- structured preflight;
- SFT only if `PREFLIGHT_RESULT=PASS` and `SFT_ALLOWED=true`.

Eval is not authorized.

## Required Evidence

- `evidence/dev_2_s23_pr63_placementretry3_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr63_placementretry3_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`

Required fields include LTP placement-mechanism finding, job/frame/node/endpoint, placement decision, transfer/preflight/SFT/checkpoint or exact blocker if non-forbidden, stop proof, endpoint refusal or equivalent, no running jobs, and explicit fresh-authorization requirement after this attempt.
