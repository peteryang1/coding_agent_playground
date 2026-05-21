# Dev 1 Parser Hygiene Review - M1-S23-NCCL-WARNING-PARSER-HYGIENE-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-NCCL-WARNING-PARSER-HYGIENE-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_nccl_warning_parser_hygiene_review.md`  
Execution boundary: no LTP, GPU, preflight, SFT, eval, remote commands, remote experiment, or dry-run by `intern_code_dev_1`.

## Result

`PASS_FOR_PM_RETRY`

PR #53 parser hygiene is acceptable for PM gate. The suppression is narrow enough for the observed false-positive class: `NCCL_ASYNC_ERROR_HANDLING` deprecation warning lines are suppressed only when the same source has both `TORCHRUN_EXIT=0` and `ALLREDUCE_OK`. Real Xid/SXid/ECC/NVLink/NCCL failures remain actionable by code inspection and dev_4's synthetic test evidence.

## Inputs Reviewed

- PR #53 local fetched head: `8b00ebd1d3ed00b8c18591d49ef0eb559456cb0f`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_nccl_warning_parser_hygiene.md`
- `scripts/parse_s22_preflight_health.py`
- `tests/test_parse_s22_preflight_health.py`

PM stated PR #53 is open/non-draft `MERGEABLE` / `CLEAN`; local fetch of `pull/53/head` resolved to `8b00ebd1d3ed00b8c18591d49ef0eb559456cb0f`.

## PR Scope

Changed runtime/parser files:

- `scripts/parse_s22_preflight_health.py`
- `tests/test_parse_s22_preflight_health.py`

Durable docs/status/evidence changes are present for dev_4 status, task registry, history, task knowledge, and dev_4 parser hygiene evidence. PR #53 also carries prior Session 23 ceph-fuse launch package durable files relative to the local `origin/main` comparison; those are already PM-gated/merged context and are not a parser-hygiene blocker in this review.

No LTP/GPU/preflight/SFT/eval/dry-run execution is claimed by dev_4 evidence.

## Parser Gate

Status: PASS.

The code adds:

- `NCCL_DEPRECATION_WARNING_RE`
- `ALLREDUCE_OK_RE`
- `source_allreduce_ok(lines)`
- `is_benign_nccl_deprecation_warning(line, source_allreduce_ok=...)`

The suppression condition is:

```text
line matches NCCL_ASYNC_ERROR_HANDLING deprecation warning
AND same source contains TORCHRUN_EXIT=0
AND same source contains ALLREDUCE_OK
```

Only then the parser:

- avoids adding `nccl_or_collective_failure` for that warning line;
- records the line as non-actionable with reason `benign_nccl_async_error_handling_deprecation_warning`.

This matches the PM gate requirement: warning suppression is narrow to `NCCL_ASYNC_ERROR_HANDLING` plus successful same-source all-reduce proof.

## Real-Fault Preservation

Status: PASS.

The patch does not suppress:

- `Invalid access of peer GPU memory`
- NCCL invalid/abort/fail/error/unhandled/system error lines outside the benign deprecation-warning pattern
- collective/all_reduce failure/error/exception lines
- nonzero `TORCHRUN_EXIT`
- `SIGABRT`
- `ChildFailedError`
- fresh/current or timestamp-unknown Xid/SXid
- fatal ECC
- nonzero uncorrected ECC
- NVLink link/down/error/replay/CRC faults

dev_4 test evidence covers:

- benign `NCCL_ASYNC_ERROR_HANDLING` + `TORCHRUN_EXIT=0` + `ALLREDUCE_OK` => `PASS`, warning non-actionable.
- `SXid 20009` unknown-time record => `FAIL_HEALTH_SIGNATURE`, `sft_allowed=false`.
- `NCCL unhandled system error` with `TORCHRUN_EXIT=1` => `FAIL_HEALTH_SIGNATURE`, `nccl_or_collective_failure` preserved.

I did not run tests, per no-execution boundary; this is a static/durable-evidence review only.

## Residual Risk

The parser now keys benign suppression at the source-file level. That is appropriate for `torch_nccl_allreduce.log` because `TORCHRUN_EXIT=0` and `ALLREDUCE_OK` are produced in the same log. If future logs combine unrelated runs in one file, same-source success markers could over-suppress deprecation-warning lines from a different run. That is a low risk for the current preflight artifact contract and is not a PM-gate blocker.

The patch intentionally does not change the prior ceph-fuse runtime decision because `SXid 20009` unknown-time NVLink/link evidence remains independently actionable.

## Completion Marker

```yaml
task_id: M1-S23-NCCL-WARNING-PARSER-HYGIENE-REVIEW-DEV1
owner: intern_code_dev_1
result: PASS_FOR_PM_RETRY
pr: 53
pr53_head_reviewed: 8b00ebd1d3ed00b8c18591d49ef0eb559456cb0f
warning_suppression_narrow: true
suppression_requires_nccl_async_error_handling: true
suppression_requires_torchrun_exit_0: true
suppression_requires_allreduce_ok: true
suppression_records_non_actionable_match: true
real_xid_sxid_detection_preserved: true
real_ecc_detection_preserved: true
real_nvlink_detection_preserved: true
real_nccl_failure_detection_preserved: true
dev4_tests_claimed_pass: true
dev1_tests_run: false
ltp_gpu_preflight_sft_eval_dry_run_by_dev1: false
exact_blockers: []
```
