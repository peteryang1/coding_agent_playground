# Dev 1 Review - M1-S23-PR63-ALTNODE-REVIEW-DEV1

Owner: `intern_code_dev_1`
Task: `M1-S23-PR63-ALTNODE-REVIEW-DEV1`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_pr63_altnode_review.md`
Review timestamp: `2026-05-21T18:53:25Z`
Result: `BLOCKER_MISSING_FINAL_ALTNODE_RUNTIME_EVIDENCE`

## Execution Boundary

- Dev_1 did not run LTP, GPU, preflight, SFT, eval, dry-run, transfer, or remote commands.
- Review used durable local PM evidence only.

## Inputs Reviewed

- `evidence/pm_s23_pr63_altnode_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr63_altnode_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr63_altnode_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

## Current Evidence State

PM authorized exactly one fresh bounded alternate-node owner-executed preflight plus conditional SFT attempt for `intern_code_dev_2`.

Forbidden nodes for this attempt:

- `lg-cmc-b7r202-k07u06-h200-000580`
- `lg-cmc-b7r202-q04u06-h200-000725`

Current dev_2 altnode runtime evidence records only pre-submit/local package readiness:

- Runtime source commit: `7ad24ae328a350c0be596f41ea143affb4034486`.
- Source bundle sha256: `5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c`.
- Source file count: 139.
- Dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- `mcore_adapter` bundle sha256: `4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb`.
- `mcore_adapter` file count: 222.
- LLamaFactory, Python dependency, and flash-attn local/provided bundle checksums are listed.
- Initial no-active-job proof is recorded as `No jobs found`.
- Status is `LOCAL_PACKAGE_READY_PRE_SUBMIT`.

Current GPU tracking likewise records only initial gate state:

- LTP submit: pending.
- Placement decision: pending.
- `/home/xu.yang` proof/capacity: pending if node is non-forbidden.
- Transfer verification: pending if node is non-forbidden.
- `mcore_adapter` import check: pending if node is non-forbidden.
- Structured preflight: pending if node is non-forbidden.
- Conditional SFT: pending, allowed only if non-forbidden node, transfer/import/preflight PASS, and `SFT_ALLOWED=true`.

## Missing Final Evidence

Dev_1 cannot classify checkpoint readiness or final runtime blocker yet. Required final fields are missing:

- Actual LTP submit result, frame/job status, endpoint, and node id.
- Placement decision against both forbidden nodes.
- If assigned a forbidden node: stop/release proof before transfer/preflight/SFT/eval.
- If assigned a non-forbidden node:
  - transfer commands and post-transfer verification;
  - no remote source/dependency network proof;
  - `/home/xu.yang/coding_agent_playground/outputs` proof and capacity probe;
  - `mcore_adapter import OK for USE_MCA=1`;
  - structured preflight result;
  - `SFT_ALLOWED` status;
  - SFT command/result if run;
  - PR63 launcher normalization logs if SFT runs;
  - checkpoint/model presence or exact blocker;
  - `trainer_state.json` presence/absence;
  - `all_results.json` presence/absence;
  - eval absence;
  - stop/release proof and no-running-job proof.

## Decision

`BLOCKER_MISSING_FINAL_ALTNODE_RUNTIME_EVIDENCE`

Current evidence is a valid pre-submit/readiness snapshot, but it is not final runtime evidence. Refresh this review after `dev_2_s23_pr63_altnode_preflight_sft_runtime.md` and `gpu_s23_pr63_altnode_tracking.md` include final placement, runtime/preflight/SFT outcome, checkpoint/artifact status, and stop proof.
