# PM S23 PR61 Preflight/SFT Runtime Authorization

Task ID: `M1-S23-PR61-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: `2026-05-21T17:16:30Z`

Authorization status: `AUTHORIZED_EXACTLY_ONCE`

## Basis

- PR #61 `M1-S23 PR59 LLamaFactory CLI command fix` merged at `2026-05-21T17:13:17Z`.
- PR #61 merge commit: `aa426b045b52b71bc23b4a2f73f3ee1c42187037`.
- PR #62 completion record merged at `2026-05-21T17:15:51Z`.
- PR #62 merge commit: `713862da983f73b165af1cfe27935ccef616a049`.
- dev_1 evidence `evidence/dev_1_s23_pr59_llamafactory_cli_review.md`: `PASS_FOR_PM_RETRY`.
- test_1 evidence `evidence/test_1_s23_pr59_llamafactory_cli_gate.md`: `PASS_FOR_PM_RETRY`.
- dev_2 PR59 runtime final blocker evidence is complete and the previous frame is stopped/released with no running coding-agent-playground job.

## Authorized Scope

PM authorizes only `intern_code_dev_2` to run exactly one fresh post-PR61 preflight/SFT runtime attempt.

The source commit for packaging must be `origin/main` at PR #62 merge commit `713862da983f73b165af1cfe27935ccef616a049`, or a local/provided workspace explicitly verified to that commit. Functional launcher fix source is PR #61 merge commit `aa426b045b52b71bc23b4a2f73f3ee1c42187037`.

Eval is not authorized.

No other owner is authorized to run LTP, GPU, transfer, preflight, SFT, eval, dry-run, or remote commands from this authorization.

## Required Gates

Repeat the prior successful PR59 gates:

- prepare source/data/`mcore_adapter` locally/provided workspace;
- record source/data/`mcore_adapter` file lists, checksums, bundle sha256 values, exact transfer command, and post-transfer verification;
- no remote `git clone`, `git fetch`, GitHub/source fetch, source download, dependency download, `pip download`, or package-index install from the GPU/LTP node for project source/dependencies;
- store generated artifacts under `/home/xu.yang/coding_agent_playground/outputs`;
- prove `MCORE_ADAPTER_DIR` and `mcore_adapter import OK for USE_MCA=1`;
- run structured preflight;
- run SFT only if transfer/import/preflight PASS and `SFT_ALLOWED=true`.

The runtime must specifically verify the PR61 fix:

- `LLAMAFACTORY_CLI` may be the command string `python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`;
- logs/manifest should show parsed/rendered `LLAMAFACTORY_CMD`;
- SFT must not fail with the prior quoted single-path signature.

## Required Durable Outputs

dev_2 must write:

- `evidence/dev_2_s23_pr61_preflight_sft_runtime.md`;
- `evidence/gpu_s23_pr61_preflight_sft_tracking.md`;
- `workspace/interns/intern_code_dev_2/status.md`.

Required final outcome:

- complete checkpoint/model with `trainer_state.json`, `all_results.json`, command/logs/run metadata, and stop proof; or
- fresh exact runtime blocker with command, logs, owner, node/frame/endpoint status, transfer/import/preflight/SFT evidence as applicable, stop proof, no-running-job proof, and next fix.

mini-swe eval remains blocked until PM gates a complete checkpoint/model or served endpoint.
