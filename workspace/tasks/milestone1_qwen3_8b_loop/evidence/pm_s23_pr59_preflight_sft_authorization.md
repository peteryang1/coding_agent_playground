# PM S23 PR59 Preflight/SFT Runtime Authorization

Task ID: `M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: `2026-05-21T16:35:06Z`

Authorization status: `AUTHORIZED_EXACTLY_ONCE`

## Basis

- PR #59 `M1-S23 PR57 launch support and mcore adapter fix` merged at `2026-05-21T16:34:13Z`.
- PR #59 merge commit: `8ed6248cd7bd56b89ac1124689fed0b56e4eba02`.
- PR #59 final head before squash merge: `8e05c28adbca6a237dc8baaab2c8767d72b94e15`.
- Functional patch commit reviewed by dev_1/test_1: `92e437cf690b68121b9ad9d2f76b18a60a10a2d6`.
- dev_1 evidence `evidence/dev_1_s23_pr57_mcore_review.md`: `PASS_FOR_PM_RETRY`.
- test_1 evidence `evidence/test_1_s23_pr57_mcore_gate.md`: `PASS_FOR_PM_RETRY`.
- dev_2 readiness evidence `evidence/dev_2_s23_pr59_runtime_ready.md`: `READY_PACKAGE_ONLY_NO_SUBMIT`.

## Authorized Scope

PM authorizes only `intern_code_dev_2` to run exactly one fresh PR59 preflight/SFT runtime attempt.

The source commit for packaging must be `origin/main` at PR #59 merge commit `8ed6248cd7bd56b89ac1124689fed0b56e4eba02`, or a local/provided workspace explicitly verified to that commit.

Eval is not authorized.

No other owner is authorized to run LTP, GPU, transfer, preflight, SFT, eval, dry-run, or remote commands from this authorization.

## Required Runtime Gates

Before remote use, dev_2 must prepare and verify locally/provided workspace bundles:

- source code/config/scripts for merge commit `8ed6248cd7bd56b89ac1124689fed0b56e4eba02`;
- accepted ShareGPT data, expected sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`;
- local/provided `mcore_adapter` source tree or package artifact;
- file lists, file counts, critical checksums, and bundle sha256 values for source and `mcore_adapter`.

Remote GPU/LTP node rules:

- no remote `git clone`, `git fetch`, GitHub source fetch, source download, dependency download, `pip download`, or package-index install for project code/dependencies;
- transfer prepared bundles by `scp`, `rsync`, or tar-over-SSH;
- record exact transfer command, destination, and post-transfer verification;
- set `MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter` or record the exact equivalent transferred local/provided path;
- run and record a Python import check that prints `mcore_adapter import OK for USE_MCA=1` before SFT.

Generated artifacts and intermediates must be under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

This includes launch outputs, temporary converted datasets, logs, checkpoints, run metadata, capacity probes, preflight outputs, and stop/evidence copies.

SFT may start only if all are true:

```text
source/data/mcore transfer verification: PASS
mcore_adapter import check: PASS
PREFLIGHT_RESULT=PASS
SFT_ALLOWED=true
HOME_XU_YANG_STORAGE_STATUS=PASS
capacity probe: PASS
PM authorization: this file
```

If any gate fails, dev_2 must not run SFT; dev_2 must stop/release the frame and record the exact blocker.

## Required Durable Outputs

dev_2 must write:

- `evidence/dev_2_s23_pr59_preflight_sft_runtime.md`;
- `evidence/gpu_s23_pr59_preflight_sft_tracking.md`;
- `workspace/interns/intern_code_dev_2/status.md`.

Required final outcome:

- complete checkpoint/model with `trainer_state.json`, `all_results.json`, command/logs/run metadata, and stop proof; or
- fresh exact runtime blocker with command, logs, owner, node/frame/endpoint status, transfer/import/preflight/SFT evidence as applicable, stop proof, no-running-job proof, and next fix.

mini-swe eval remains blocked until PM gates a complete checkpoint/model or served endpoint.
