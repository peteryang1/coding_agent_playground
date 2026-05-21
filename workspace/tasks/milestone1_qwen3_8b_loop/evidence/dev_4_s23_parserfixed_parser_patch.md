# Dev 4 S23 Parser-Fixed Parser Patch

Task ID: `M1-S23-PARSERFIXED-PARSER-PATCH-DEV4`

Owner: `intern_code_dev_4`

Created: 2026-05-21

Scope: implement the actual parser patch from the PR #47 no-execution package.

Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md`

Completion marker: ready-for-review; no LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run.

## Inputs

Primary source package:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_parserfixed_blocker_fix.md
PR #47 mergedAt: 2026-05-21T12:13:48Z
PR #47 merge commit: e9cce7b1ee60949c4481b1efcc7074c06761c7fc
```

Runtime blocker being addressed:

```text
runtime task: M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2
preflight status: FAIL_HEALTH_SIGNATURE
health source: dmesg_gpu_fault_scan.txt Xid/SXid matches
storage status: HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
passed evidence: capacity probe, topology, NVLink capture, 8-rank torch NCCL all-reduce
SFT/eval: not run because parser-fixed preflight failed
```

## Code Changes

Updated:

```text
scripts/parse_s22_preflight_health.py
```

Xid/SXid freshness handling:

```text
- Detects both Xid and SXid signatures in allowlisted hardware/runtime sources.
- Infers freshness start from a run id timestamp such as 20260521T114448Z.
- Supports explicit --freshness-start-utc override for future wrappers.
- Parses ISO-like dates/timestamps from log lines.
- Classifies Xid/SXid records as fresh_current, stale_historical, or unknown_time.
- Treats fresh_current and unknown_time Xid/SXid as actionable faults.
- Treats stale_historical Xid/SXid as non-actionable audit evidence under non_actionable_matches and xid_sxid_history.
```

Storage normalization:

```text
- Keeps /home/xu.yang/coding_agent_playground/outputs as the required generated-artifact root.
- Accepts /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs as the resolved CephFS mirror of that output root.
- Emits storage.raw_path, storage.resolved_path, storage.classification, and storage.status.
- Keeps home_xu_yang_storage_status as the stable top-level compatibility field.
- Continues to fail generated artifact roots outside the accepted /home/CephFS paths.
```

Preserved behavior:

```text
- Generated command/process/evidence/history/task/summary/readme/preflight_result/health_status/parser/manifest/xtrace text remains excluded from actionable matching.
- Fresh or timestamp-unknown Xid/SXid remains actionable.
- Fatal ECC and nonzero uncorrected ECC remain actionable.
- NVLink link/down/error/replay/CRC faults remain actionable.
- NCCL/CUDA invalid peer memory, SIGABRT, torch elastic ChildFailedError, NCCL collective/all-reduce failures, and nonzero torchrun status remain actionable.
- Stable top-level fields remain present: preflight_result, health_result, non_actionable_matches, torch_nccl_allreduce_exit, capacity_probe_status, different_node_gate, home_xu_yang_storage_status, topology_capture_status, nvlink_capture_status, sft_allowed, sft_skip_reason.
```

## Local Non-Runtime Tests

Commands run locally only:

```bash
python3 -m py_compile scripts/parse_s22_preflight_health.py
```

Synthetic parser test command:

```bash
python3 scripts/parse_s22_preflight_health.py --preflight-dir <synthetic-dir> --out-json <synthetic-dir>/health_status.json --out-text <synthetic-dir>/health_status.txt
```

Synthetic scenarios and results:

```text
stale Xid sample:
  path: /home/xu.yang/coding_agent_playground/outputs/parser_patch_synthetic_<id>/preflight/...20260521T114448Z
  line: 2026-04-17 10:00:00 kernel: NVRM: Xid 43 GPU has fallen off bus
  result: exit 0, PREFLIGHT_RESULT=PASS, sft_allowed=true
  audit: stale_historical_xid_sxid recorded in non_actionable_matches

fresh Xid/SXid sample:
  line: 2026-05-21 18:18:48 kernel: NVRM: Xid 137 SXid 12028 peer memory fault
  result: exit 2, PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
  actionable: freshness=fresh_current

timestamp-unknown Xid sample:
  line: kernel: NVRM: Xid 137 without timestamp
  result: exit 2, PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
  actionable: freshness=unknown_time

outside storage sample:
  path: /tmp/parser_patch_outside_<id>
  result: home_xu_yang_storage_status=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS, sft_allowed=false
```

Observed local test output:

```text
stale_exit=0
stale_xid_pass_ok
fresh_exit=2 unknown_exit=2 outside_exit=2
fresh_unknown_storage_fail_ok
```

No LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run.

## PR Scope

PR opened:

```text
PR: #49
URL: https://github.com/peteryang1/coding_agent_playground/pull/49
head: intern_code_dev_4/M1-S23-PARSERFIXED-PARSER-PATCH-DEV4
state: OPEN
draft: false
mergeable: MERGEABLE
mergeStateStatus: CLEAN
status checks: none reported
```

PR cites:

```text
task id: M1-S23-PARSERFIXED-PARSER-PATCH-DEV4
owner: intern_code_dev_4
durable evidence: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md
completion marker: ready-for-review before PM gate; complete after PM-gated self-merge
runtime boundary: no LTP/GPU/preflight/SFT/eval/dry-run/runtime authorization
```

Expected PR files:

```text
scripts/parse_s22_preflight_health.py
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md
workspace/interns/intern_code_dev_4/status.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md
```

## Acceptance Criteria

```text
1. Stale historical Xid/SXid records are audited but do not block current runs.
2. Fresh/current Xid/SXid records block SFT.
3. Timestamp-unknown Xid/SXid records block SFT.
4. ECC/NVLink/NCCL/SIGABRT/collective failure detection remains intact.
5. /home/xu.yang/coding_agent_playground/outputs is valid for generated artifacts.
6. /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs is valid only as the resolved CephFS mirror.
7. Generated artifacts outside accepted roots still block SFT.
8. Stable top-level parser fields are preserved.
9. Local synthetic tests or explicit attempts are recorded.
10. No LTP/GPU/preflight/SFT/eval/dry-run/runtime is run.
```

## Current Completion

```yaml
task_id: M1-S23-PARSERFIXED-PARSER-PATCH-DEV4
owner: intern_code_dev_4
result: READY_FOR_REVIEW
pr: 49
pr_url: https://github.com/peteryang1/coding_agent_playground/pull/49
pr_state: OPEN
pr_mergeable: MERGEABLE
pr_merge_state_status: CLEAN
evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md
runtime_authorized: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
```
