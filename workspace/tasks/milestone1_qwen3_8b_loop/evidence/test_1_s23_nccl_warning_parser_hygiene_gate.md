# Test 1 S23 NCCL Warning Parser Hygiene Gate

Task ID: `M1-S23-NCCL-WARNING-PARSER-HYGIENE-GATE-TEST1`
Gate owner: `intern_code_test_1`
Patch owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_nccl_warning_parser_hygiene_gate.md`
Status timestamp: `2026-05-21T14:16:01Z`

## Result

`PASS_FOR_OWNER_SELF_MERGE_AFTER_PM_GATE`

No LTP, GPU, preflight, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

This is test_1's no-execution gate pass for PR #53. Owner self-merge still requires PM's explicit gate/merge instruction and any required dev_1 review completion.

## Inputs Reviewed

PR #53:

- URL: `https://github.com/peteryang1/coding_agent_playground/pull/53`
- Title: `M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4 parser hygiene`
- State: open
- Draft: false
- Mergeability: `MERGEABLE` / `CLEAN`
- Head reviewed: `8b00ebd1d3ed00b8c18591d49ef0eb559456cb0f`
- Functional patch commit: `b3c639bd507d48fe9ae317f61f3bcb035a328389`

Durable evidence:

- `evidence/dev_4_s23_nccl_warning_parser_hygiene.md`

Files reviewed:

- `scripts/parse_s22_preflight_health.py`
- `tests/test_parse_s22_preflight_health.py`
- `evidence/dev_4_s23_nccl_warning_parser_hygiene.md`
- PR metadata/file list

## Patch Scope

PASS.

Functional diff adds:

- `NCCL_DEPRECATION_WARNING_RE`
- `ALLREDUCE_OK_RE`
- `source_allreduce_ok(lines)`
- `is_benign_nccl_deprecation_warning(...)`
- suppression of only `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings when the same source has:
  - `TORCHRUN_EXIT=0`
  - `ALLREDUCE_OK`
- non-actionable audit record reason:
  - `benign_nccl_async_error_handling_deprecation_warning`

The patch does not broadly suppress NCCL matches. The existing `NCCL_FAILURE_RE` path remains active unless the specific benign deprecation-warning condition is met.

## Real-Fault Preservation

PASS.

Source review and tests preserve detection for:

- SXid/Xid health signatures, including SXid 20009;
- NCCL unhandled system error;
- nonzero `TORCHRUN_EXIT`;
- collective/all-reduce failure or exception;
- invalid peer GPU memory;
- `SIGABRT`;
- `ChildFailedError`;
- fatal/nonzero ECC;
- NVLink link/counter faults.

Important residual behavior: the patch intentionally does not unblock the prior ceph-fuse fixed runtime by itself. SXid 20009 / NVLink health signal remains actionable and still blocks SFT.

## Owner Test Evidence

PASS.

dev_4 evidence reports:

```bash
python3 -m py_compile scripts/parse_s22_preflight_health.py tests/test_parse_s22_preflight_health.py
python3 -m pytest tests/test_parse_s22_preflight_health.py -q
```

Observed result:

```text
3 passed in 0.02s
```

Test coverage reviewed:

1. `NCCL_ASYNC_ERROR_HANDLING` deprecation warning plus `TORCHRUN_EXIT=0` and `ALLREDUCE_OK` yields parser `PASS`, `sft_allowed=true`, no `nccl_or_collective_failure`, and a non-actionable match.
2. SXid 20009 in dmesg still yields `FAIL_HEALTH_SIGNATURE` and `sft_allowed=false`.
3. Real NCCL unhandled system error with `TORCHRUN_EXIT=1` still yields `FAIL_HEALTH_SIGNATURE` and `nccl_or_collective_failure`.

test_1 did not run tests; this gate relies on source review and dev_4's durable test evidence.

## PR Scope / Merge Readiness

PASS for test_1 gate.

PR #53 includes the expected functional files:

- `scripts/parse_s22_preflight_health.py`
- `tests/test_parse_s22_preflight_health.py`
- `evidence/dev_4_s23_nccl_warning_parser_hygiene.md`

The PR also contains milestone status/history/task records. For test_1 this is acceptable process scope because the task requires durable evidence/status updates and no unrelated runtime execution artifacts were added by dev_4's evidence.

Owner self-merge is not authorized by test_1 alone. PM must record the gate decision and issue owner self-merge instruction after required reviews.

## Residual Risk

Low for the requested hygiene change.

Residual risks:

- The pass depends on the exact same-source condition for `TORCHRUN_EXIT=0` plus `ALLREDUCE_OK`; malformed all-reduce logs may still require manual triage.
- This patch does not solve node-health SXid/NVLink blockers and must not be interpreted as runtime authorization.

## Completion Marker

```yaml
task_id: M1-S23-NCCL-WARNING-PARSER-HYGIENE-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_OWNER_SELF_MERGE_AFTER_PM_GATE
pr: 53
pr_head_reviewed: 8b00ebd1d3ed00b8c18591d49ef0eb559456cb0f
functional_patch_commit: b3c639bd507d48fe9ae317f61f3bcb035a328389
dev4_evidence: PASS
owner_tests_reported: "3 passed in 0.02s"
benign_nccl_warning_suppression: PASS_NARROW
real_fault_preservation: PASS
runtime_authorized_by_this_gate: false
owner_self_merge_authorized_by_test1_alone: false
no_ltp_gpu_preflight_sft_eval_by_test1: true
peer_send_pm_used: false
```
