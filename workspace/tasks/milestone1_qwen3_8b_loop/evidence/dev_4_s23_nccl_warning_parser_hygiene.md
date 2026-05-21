# M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4

Owner: `intern_code_dev_4`

Date: `2026-05-21`

Scope: no-execution parser hygiene patch so `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings are not classified as collective failures when the same all-reduce log reports `TORCHRUN_EXIT=0` and `ALLREDUCE_OK`.

Runtime boundary: no LTP/GPU/preflight/SFT/eval/dry-run command was run.

## Patch Summary

Changed `scripts/parse_s22_preflight_health.py`:

```text
1. Added NCCL_DEPRECATION_WARNING_RE for NCCL_ASYNC_ERROR_HANDLING deprecation warning lines.
2. Added ALLREDUCE_OK_RE and source_allreduce_ok(lines).
3. Suppressed only NCCL_ASYNC_ERROR_HANDLING deprecation warnings when the same source has TORCHRUN_EXIT=0 and ALLREDUCE_OK.
4. Recorded suppressed warning lines under non_actionable_matches with reason benign_nccl_async_error_handling_deprecation_warning.
```

Preserved actionable detection:

```text
NCCL/CUDA invalid peer memory
NCCL unhandled system error
collective/all_reduce failure or exception
nonzero TORCHRUN_EXIT
SIGABRT
ChildFailedError
fresh/current or timestamp-unknown Xid/SXid
fatal/nonzero ECC
NVLink link/down/error/replay/CRC faults
```

## Tests

Added `tests/test_parse_s22_preflight_health.py`.

Local commands run:

```bash
python3 -m py_compile scripts/parse_s22_preflight_health.py tests/test_parse_s22_preflight_health.py
python3 -m pytest tests/test_parse_s22_preflight_health.py -q
```

Observed result:

```text
...                                                                      [100%]
3 passed in 0.02s
```

Synthetic coverage:

```text
1. NCCL_ASYNC_ERROR_HANDLING deprecation warning + TORCHRUN_EXIT=0 + ALLREDUCE_OK -> parser status PASS, warning recorded as non-actionable, no nccl_or_collective_failure.
2. SXid 20009 unknown_time in dmesg_gpu_fault_scan.txt -> FAIL_HEALTH_SIGNATURE, sft_allowed=false.
3. NCCL unhandled system error with TORCHRUN_EXIT=1 -> FAIL_HEALTH_SIGNATURE, nccl_or_collective_failure preserved.
```

The tests monkeypatch the parser output root to pytest's temporary directory so the existing `/home/xu.yang` storage gate does not mask the NCCL warning classification behavior under test.

## Current Decision Impact

This patch is hygiene. It does not change the previous ceph-fuse-fixed runtime decision because the real SXid 20009 / NVLink health signal independently blocks SFT.

Future parser output should be clearer:

```text
benign NCCL_ASYNC_ERROR_HANDLING deprecation warning -> non_actionable_matches
real SXid/NVLink health event -> actionable_faults
```

## PR Scope

Expected PR files:

```text
scripts/parse_s22_preflight_health.py
tests/test_parse_s22_preflight_health.py
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_nccl_warning_parser_hygiene.md
workspace/interns/intern_code_dev_4/status.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md
```

PR must wait for PM gate before any owner self-merge.

## Completion Status

```yaml
task_id: M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4
owner: intern_code_dev_4
result: COMPLETE
pr: 53
pr_url: https://github.com/peteryang1/coding_agent_playground/pull/53
pr_state: MERGED
pr_mergeable: MERGEABLE_AT_GATE
pr_merge_state_status: CLEAN_AT_GATE
merged_at: 2026-05-21T14:20:56Z
merge_commit: e29c93736be3384663cad953cd18da68c30070fb
evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_nccl_warning_parser_hygiene.md
parser_patch: true
tests_added: true
runtime_authorized: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
```

## PM Gate And Merge Record

PM gate basis:

```text
PR #53 head: 8b00ebd1d3ed00b8c18591d49ef0eb559456cb0f
GitHub state at gate: open, non-draft, MERGEABLE / CLEAN
dev_1 review: dev_1_s23_nccl_warning_parser_hygiene_review.md result PASS_FOR_PM_RETRY
test_1 gate: test_1_s23_nccl_warning_parser_hygiene_gate.md result PASS_FOR_OWNER_SELF_MERGE_AFTER_PM_GATE
```

Owner action:

```text
Self-merged PR #53 at 2026-05-21T14:20:56Z.
Merge commit: e29c93736be3384663cad953cd18da68c30070fb.
Task completion marker: complete.
Runtime boundary: parser hygiene only; no LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run or authorized.
```
