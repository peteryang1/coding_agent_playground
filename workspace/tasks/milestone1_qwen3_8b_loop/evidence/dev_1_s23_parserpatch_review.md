# Dev 1 Review - M1-S23-PARSERPATCH-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-PARSERPATCH-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_parserpatch_review.md`  
Execution boundary: no LTP, GPU, SFT, eval, remote experiment, or dry-run by `intern_code_dev_1`.

## Result

`PASS_FOR_PM_RETRY`

Reviewed PR #49 for `M1-S23-PARSERFIXED-PARSER-PATCH-DEV4`. PM reports PR #49 is open, non-draft, `MERGEABLE` / `CLEAN`. Initial review covered local dev_4 PR branch head `1ddfe31` (`Remove stale S23 storage helper`), with prior patch commit `91333d4`. Refresh review then checked the PM-named head `6dd0f1bfe1635af650a7fbc928bfbabe4c8c4098` and the currently fetched branch head `9393fdec8e5fef7df250743e1a958436a8dfa79a`.

I found no dev_1 blocker for PM retry gate. Runtime remains separately gated; this review does not authorize LTP/GPU/preflight/SFT/eval/dry-run.

## Inputs Reviewed

- PR #47 blocker package:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_parserfixed_blocker_fix.md`
  - PR #47 merge commit `e9cce7b1ee60949c4481b1efcc7074c06761c7fc`
- dev_2 final runtime evidence:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_parserfixed_preflight_sft_tracking.md`
- dev_4 PR #49 patch evidence:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md`
- PR #49 branch content:
  - `/work-agents/intern_code_dev_4/coding_agent_playground`, current fetched head `9393fdec8e5fef7df250743e1a958436a8dfa79a`
  - PM-named refreshed head `6dd0f1bfe1635af650a7fbc928bfbabe4c8c4098`
  - `scripts/parse_s22_preflight_health.py`
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

No parser execution, local test, dry-run, LTP, GPU, preflight, SFT, eval, or remote experiment was run by `intern_code_dev_1`; this is a static review of durable evidence and patch diff.

## Changed Files

PR #49 changes are scoped to parser implementation and durable task/status docs:

- `scripts/parse_s22_preflight_health.py`
- `workspace/interns/intern_code_dev_4/status.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PARSERFIXED-PARSER-PATCH-DEV4/README.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PARSERFIXED-PARSER-PATCH-DEV4/history_log.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PARSERFIXED-PARSER-PATCH-DEV4/task_knowledge.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

Refresh delta:

- `1ddfe31..6dd0f1bfe1635af650a7fbc928bfbabe4c8c4098` changes only durable status/evidence/task docs. It records PR #49 status as open, non-draft, `MERGEABLE` / `CLEAN`; it does not change `scripts/parse_s22_preflight_health.py`.
- `6dd0f1bfe1635af650a7fbc928bfbabe4c8c4098..9393fdec8e5fef7df250743e1a958436a8dfa79a` changes only `evidence/dev_4_s23_parserfixed_parser_patch.md` by removing one stale `latest head commit: 1ddfe31...` line. It does not change parser code or tests.
- Therefore the code/test review from `1ddfe31` remains valid for the current fetched head.

## Runtime Context

dev_2 final parser-fixed runtime evidence showed:

- PR #45 exact merge commit staged after remote GitHub staging blocker: `6f61489e85fcf7e129699061c9ddcb6e8db80926`.
- Preflight artifacts were preserved under `/home/xu.yang/coding_agent_playground/outputs/preflight/...` and mirrored through `/mnt/cephfs/home/xu.yang/...`.
- Capacity probe passed and cleaned up.
- Topology/NVLink capture completed.
- Torch 8-rank NCCL all-reduce exited 0.
- Structured parser result was `FAIL_HEALTH_SIGNATURE`.
- `sft_allowed=false`.
- `HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS`.
- SFT was skipped; no checkpoint/model, no `trainer_state.json`, no `all_results.json`.
- LTP reached `STOPPED (Completed)` and endpoint refused afterward.

PR #49 directly addresses the two parser-side blockers from that runtime: stale/fresh Xid/SXid classification and `/home.xu.yang`/CephFS storage-root normalization.

## Xid/SXid Freshness

Status: PASS.

The patch changes `XID_RE` to detect both `Xid` and `SXid`, adds run-id timestamp inference and optional `--freshness-start-utc`, and records `xid_sxid_history` plus `freshness_start_utc` in the structured output.

Freshness behavior reviewed:

- Lines with timestamps older than `freshness_start - 10 minutes` are classified as `stale_historical`.
- `stale_historical` Xid/SXid is added to `ignored_non_actionable_matches` and `xid_sxid_history`, not `actionable_faults`.
- Fresh/current Xid/SXid remains actionable and blocks SFT.
- Timestamp-unknown Xid/SXid remains actionable by default and blocks SFT.

This matches the PR #47 package requirement: do not let clearly stale audited records block current runs, while preserving fail-fast behavior for current or timestamp-unknown Xid/SXid.

## Storage Normalization

Status: PASS.

The patch replaces the prior raw-only storage check with `storage_info()`:

- Raw path under `/home/xu.yang/coding_agent_playground/outputs` passes as `PASS_RAW_HOME_XU_YANG`.
- Resolved path under `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs` passes as `PASS_WITH_CEPHFS_RESOLUTION`.
- Paths outside those accepted roots still fail as `FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS`.

Structured storage details are preserved under `storage` and `checks.home_xu_yang_storage`, including raw path, resolved path, classification, expected root, and accepted resolved roots. The stable top-level compatibility field `home_xu_yang_storage_status` remains present.

## Structured Fields

Status: PASS.

The patch preserves existing stable top-level fields:

- `preflight_result`
- `health_result`
- `non_actionable_matches`
- `torch_nccl_allreduce_exit`
- `capacity_probe_status`
- `different_node_gate`
- `home_xu_yang_storage_status`
- `topology_capture_status`
- `nvlink_capture_status`
- `sft_allowed`
- `sft_skip_reason`

The patch also adds structured fields useful for review:

- `xid_sxid_history`
- `freshness_start_utc`
- `storage`
- expanded `checks.home_xu_yang_storage`

## Real-Fault Preservation

Status: PASS.

The patch keeps existing actionable detection for:

- Fresh/current or timestamp-unknown Xid/SXid in allowlisted actionable sources.
- Fatal ECC and nonzero uncorrected ECC.
- NVLink link/down/error/replay/CRC faults.
- NCCL/CUDA invalid peer memory.
- SIGABRT and torch elastic `ChildFailedError`.
- NCCL collective/all-reduce failures.
- Nonzero torchrun status.
- Storage roots outside accepted `/home`/CephFS output paths.

Generated command/process/evidence/history/task/summary/readme/preflight-result/health-status/parser/manifest/xtrace text remains excluded from actionable matching, with fault-looking text preserved as non-actionable audit evidence.

## Tests / Attempts

Status: PASS for no-runtime patch gate.

dev_4 evidence records local non-runtime tests:

- `python3 -m py_compile scripts/parse_s22_preflight_health.py`
- Synthetic parser run with local artifacts only.

Synthetic scenarios recorded by dev_4:

- Stale Xid sample from `2026-04-17` during `20260521T114448Z` run: exit 0, `PREFLIGHT_RESULT=PASS`, stale Xid audited as non-actionable.
- Fresh Xid/SXid sample from `2026-05-21 18:18:48`: exit 2, `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.
- Timestamp-unknown Xid sample: exit 2, `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.
- Outside-storage sample: `home_xu_yang_storage_status=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS`, `sft_allowed=false`.

dev_4 evidence states no LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run.

## Remaining Notes

- The parser treats date-only timestamps as midnight UTC. That is conservative for same-day current-run health logs and stale prior-day history. If future hardware logs use non-ISO month-name dmesg timestamps, they will be classified `unknown_time` and remain actionable by default, which is safer than suppressing real faults.
- This PR should be treated as code/parser readiness only. A future runtime still requires PM authorization and should require structured preflight PASS plus `sft_allowed=true` before SFT.

## Completion Marker

```yaml
task_id: M1-S23-PARSERPATCH-REVIEW-DEV1
owner: intern_code_dev_1
reviewed_pr: PR #49
reviewed_heads:
  - 1ddfe31
  - 6dd0f1bfe1635af650a7fbc928bfbabe4c8c4098
  - 9393fdec8e5fef7df250743e1a958436a8dfa79a
result: PASS_FOR_PM_RETRY
pass_for_pm_retry: true
exact_blockers: []
head_refresh_delta_docs_status_evidence_only: true
pr47_cited: true
dev2_final_runtime_cited: true
changed_files_reviewed: true
tests_reviewed: true
xid_sxid_freshness_reviewed: true
storage_normalization_reviewed: true
structured_fields_reviewed: true
real_fault_preservation_reviewed: true
no_ltp_gpu_sft_eval_remote_experiment_dry_run_by_dev1: true
```
