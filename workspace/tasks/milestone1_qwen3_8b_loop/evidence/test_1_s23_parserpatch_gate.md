# Test 1 S23 Parser Patch Gate

Task ID: `M1-S23-PARSERPATCH-GATE-TEST1`
Gate owner: `intern_code_test_1`
Patch owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_parserpatch_gate.md`
Status timestamp: `2026-05-21T12:39:16Z`

## Result

`PASS_FOR_PM_RETRY`

No LTP, GPU, preflight, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

## PR #49 Re-Gate Result

Gate result for PR #49 / `M1-S23-PARSERFIXED-PARSER-PATCH-DEV4`:

`PASS_FOR_PM_RETRY`

Inputs checked:

- PR: `https://github.com/peteryang1/coding_agent_playground/pull/49`
- PR state: open, non-draft, `MERGEABLE` / `CLEAN`
- PR head reviewed: `1ddfe31d8345418572a6d70d1ba15da424fd7aef`
- PR branch: `intern_code_dev_4/M1-S23-PARSERFIXED-PARSER-PATCH-DEV4`
- Durable evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md`
- Script reviewed: `scripts/parse_s22_preflight_health.py`

No LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run by test_1. No parser execution was performed by test_1; this gate is based on PR metadata, source review, and dev_4 durable evidence/test-attempt records.

### Structured Fields

PASS.

The patch preserves stable top-level fields required by test_1:

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

The patch keeps `sft_allowed` tied to parser status PASS and preserves `sft_skip_reason` for non-PASS outcomes.

### Storage Status

PASS.

The patch implements generated-artifact storage classification with:

- Required raw generated-output root: `/home/xu.yang/coding_agent_playground/outputs`.
- Accepted resolved CephFS mirror: `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs`.
- Structured storage output including raw path, resolved path, classification, and status.
- `home_xu_yang_storage_status` preserved as the stable top-level compatibility field.
- Generated artifact roots outside accepted `/home` and CephFS roots continue to fail.

Gate interpretation:

- Raw `/home/xu.yang/coding_agent_playground/outputs/...` paths pass.
- Resolved `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/...` paths pass.
- Arbitrary outside generated-output paths remain blockers.

### Xid/SXid Stale-vs-Actionable Behavior

PASS.

The patch adds Xid/SXid freshness classification:

- `fresh_current`: actionable and blocks SFT.
- `unknown_time`: actionable by default and blocks SFT.
- `stale_historical`: non-actionable audit evidence under `non_actionable_matches` and `xid_sxid_history`.

The patch infers freshness start from a run id timestamp such as `20260521T114448Z`, supports `--freshness-start-utc`, parses ISO-like dates/timestamps from log lines, and uses a grace window. This satisfies the gate requirement that stale historical records, such as `2026-04-17` Xid lines during a `2026-05-21` preflight, do not block by themselves while fresh/current or timestamp-unknown Xid/SXid remains actionable.

### Real-Fault Preservation

PASS.

Reviewed source/evidence preserves actionability for:

- Fresh/current Xid/SXid.
- Timestamp-unknown Xid/SXid in allowlisted hardware/runtime sources.
- Fatal ECC.
- Nonzero uncorrected ECC counters.
- NVLink link/down/error/replay/CRC faults.
- NCCL/CUDA invalid peer GPU memory.
- Rank `SIGABRT` or torch elastic `ChildFailedError`.
- NCCL collective/all-reduce failures.
- Nonzero torchrun status.
- Missing required capacity/topology/NVLink/NCCL evidence.

Existing false-positive suppression for generated command/process/evidence/history/task/summary/readme/preflight_result/health_status/parser/manifest/xtrace text is preserved.

### Tests / Test Attempts

PASS.

Dev_4 evidence records local non-runtime checks:

- `python3 -m py_compile scripts/parse_s22_preflight_health.py`.
- Synthetic stale Xid sample: `2026-04-17` Xid during run id `20260521T114448Z` exits 0 / `PREFLIGHT_RESULT=PASS`, with stale historical Xid recorded as non-actionable audit evidence.
- Synthetic fresh Xid/SXid sample: `2026-05-21 18:18:48` Xid/SXid exits 2 / `FAIL_HEALTH_SIGNATURE`.
- Synthetic unknown-time Xid sample exits 2 / `FAIL_HEALTH_SIGNATURE`.
- Synthetic outside storage path exits 2 with storage failure.

No LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run by dev_4 according to evidence.

### Future PASS/FAIL Conditions

Future runtime can only allow SFT if:

- `preflight_result=PASS`.
- `sft_allowed=true`.
- `home_xu_yang_storage_status=PASS`.
- Capacity/topology/NVLink/NCCL all-reduce evidence passes.
- No actionable fresh/current or timestamp-unknown Xid/SXid/ECC/NVLink/NCCL/SIGABRT/collective fault exists.

Future runtime must block SFT if:

- Parser result is WARN/FAIL.
- `sft_allowed=false`.
- Generated artifact storage is outside accepted `/home`/CephFS roots.
- Fresh/current or timestamp-unknown Xid/SXid is present.
- Fatal/nonzero ECC, NVLink, NCCL, SIGABRT, collective, or nonzero torchrun failure appears.
- Required preflight artifacts are missing.

Eval handoff remains blocked until a later authorized SFT run produces checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM/test accepts explicit replacements.

### Decision

`PASS_FOR_PM_RETRY`

This is a no-execution PR gate only. It does not authorize LTP/GPU/preflight/SFT/eval/dry-run/runtime. Runtime remains controlled by separate PM authorization after owner self-merge/completion records.

## PR #49 Head Refresh

PM requested re-gate after PR #49 advanced to `6dd0f1bfe1635af650a7fbc928bfbabe4c8c4098`.

Current GitHub PR #49 head observed by test_1 is newer:

`9393fdec8e5fef7df250743e1a958436a8dfa79a`

Head refresh result:

`PASS_FOR_PM_RETRY`

Review notes:

- Commit `6dd0f1bfe1635af650a7fbc928bfbabe4c8c4098` is docs/status/evidence/task-registry only relative to previously gated `1ddfe31d8345418572a6d70d1ba15da424fd7aef`.
- Current head `9393fdec8e5fef7df250743e1a958436a8dfa79a` adds one further evidence cleanup commit after `6dd0f1b`; it removes stale head evidence from `dev_4_s23_parserfixed_parser_patch.md`.
- Diff from `1ddfe31d8345418572a6d70d1ba15da424fd7aef` to current `9393fdec8e5fef7df250743e1a958436a8dfa79a` touches only:
  - `workspace/interns/intern_code_dev_4/status.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PARSERFIXED-PARSER-PATCH-DEV4/README.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PARSERFIXED-PARSER-PATCH-DEV4/history_log.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PARSERFIXED-PARSER-PATCH-DEV4/task_knowledge.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- `scripts/parse_s22_preflight_health.py` is unchanged between `1ddfe31d8345418572a6d70d1ba15da424fd7aef` and current head `9393fdec8e5fef7df250743e1a958436a8dfa79a`.
- The prior source-review gate remains valid: structured fields, storage normalization, Xid/SXid freshness behavior, local test-attempt evidence, real-fault preservation, and future PASS/FAIL conditions still pass.

No LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run by test_1 for this head refresh.

## Superseded Missing-PR Check

Current GitHub check:

- `gh pr list --state open ...` returned no open PRs.
- Remote refs include PR #48 head, but PR #48 is not the Session 23 parser patch PR.
- PR #48 content is a PR #47 merge-completion record and does not add `evidence/dev_4_s23_parserfixed_parser_patch.md`.
- Required dev_4 parser patch evidence file is not present in reviewed PR content.

Superseded earlier blocker:

`BLOCKED_MISSING_DEV4_PARSER_PATCH_PR`

Required missing input:

- An open dev_4 parser patch PR for task `M1-S23-PARSERFIXED-PARSER-PATCH-DEV4`.
- PR body must cite task id, owner, acceptance criteria, durable evidence path, and completion marker.
- Durable evidence path expected by task registry: `evidence/dev_4_s23_parserfixed_parser_patch.md`.
- Patch must include actual parser code changes, expected file `scripts/parse_s22_preflight_health.py`.

## Gate Scope

When dev_4 opens the patch PR, test_1 will gate only durable PR/evidence contents. Test_1 will not run LTP/GPU/preflight/SFT/eval/dry-run.

### Structured Fields

PASS requires the parser still emits stable top-level fields:

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

BLOCKER conditions:

- Any required field is removed or renamed without compatibility alias.
- `sft_allowed` can become true when `preflight_result` is not PASS.
- `sft_skip_reason` is empty when preflight is WARN/FAIL.

### Storage Status

PASS requires generated-artifact storage classification to accept both:

- Raw generated output root: `/home/xu.yang/coding_agent_playground/outputs`.
- Resolved CephFS mirror root: `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs`.

PASS also requires:

- Raw `/home/xu.yang/...` preflight paths resolving through `/mnt/cephfs/home/xu.yang/...` are not marked `FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS`.
- Generated artifacts outside both accepted roots still fail with an exact storage blocker.
- Read-only required inputs outside `/home/xu.yang`, such as base model, dependency archives, and source dataset, remain justified exceptions and are not treated as generated artifacts.

BLOCKER conditions:

- Parser still reports `HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS` for generated artifacts written under `/home/xu.yang/coding_agent_playground/outputs` and resolved under the accepted CephFS mirror.
- Parser accepts arbitrary non-`/home` generated output paths.

### Xid/SXid Freshness Behavior

PASS requires structured Xid/SXid freshness classification in allowlisted hardware sources:

- `fresh_current`: actionable and blocks SFT.
- `unknown_time`: actionable by default and blocks SFT.
- `stale_historical`: non-actionable audit evidence and does not block SFT by itself.

PASS requires stale-vs-actionable behavior:

- Clearly stale historical Xid/SXid records, such as `2026-04-17` lines during a `2026-05-21` preflight, are recorded under non-actionable/audit fields.
- Fresh current-node Xid/SXid records, such as matching allocation/preflight window lines, remain actionable.
- Timestamp-unknown Xid/SXid records in allowlisted hardware logs remain actionable unless PM/test explicitly accepts a safer alternative.

BLOCKER conditions:

- All Xid/SXid records are treated as non-actionable.
- All Xid/SXid records are treated as actionable without freshness classification, recreating the Session 22/23 blocker.
- Fresh/current or timestamp-unknown Xid/SXid can pass silently.
- Stale Xid/SXid text copied into command/process/evidence files becomes actionable.

### Real-Fault Preservation

PASS requires the patch preserves existing PR #45 real-fault detection:

- Fatal ECC.
- Nonzero uncorrected ECC counters.
- NVLink link/down/error/replay/CRC/fatal faults.
- NCCL/CUDA invalid peer GPU memory.
- Rank `SIGABRT` or torch elastic `ChildFailedError`.
- NCCL collective/all-reduce failures.
- Nonzero torchrun status.
- Missing required capacity/topology/NVLink/NCCL evidence.

BLOCKER conditions:

- The patch weakens real current hardware/runtime fault detection without an explicit accepted replacement.
- The patch suppresses actionable faults only to force PASS.

### Test Coverage / Test Attempts

PASS requires dev_4 evidence to record local non-runtime tests or explicit test attempts, such as:

- `python3 -m py_compile scripts/parse_s22_preflight_health.py`.
- Synthetic stale Xid/SXid sample: stale historical Xid does not block by itself.
- Synthetic fresh Xid/SXid sample: fresh/current Xid/SXid blocks.
- Synthetic unknown-time Xid/SXid sample: unknown-time hardware-log Xid/SXid blocks.
- Synthetic `/home` path resolving to `/mnt/cephfs/home` is accepted.
- Synthetic outside generated-output path is rejected.
- Synthetic command/process copied Xid/SXid text remains non-actionable.

BLOCKER conditions:

- No tests or explicit test attempts are recorded.
- Tests require GPU/LTP/SFT/eval/dry-run execution.
- Tests do not cover both storage normalization and Xid/SXid stale-vs-actionable behavior.

## Expected Post-Run PASS/FAIL Conditions

After any future PM-authorized runtime, parser output may allow SFT only when:

- `preflight_result=PASS`.
- `sft_allowed=true`.
- `home_xu_yang_storage_status=PASS`.
- Capacity/topology/NVLink/NCCL all-reduce evidence passes.
- No actionable fresh/current or timestamp-unknown Xid/SXid/ECC/NVLink/NCCL/SIGABRT/collective fault exists.

Future runtime must block SFT when:

- Parser result is WARN/FAIL.
- `sft_allowed=false`.
- Generated artifact storage is outside accepted `/home`/CephFS roots.
- Fresh/current or timestamp-unknown Xid/SXid is present.
- Fatal/nonzero ECC, NVLink, NCCL, SIGABRT, collective, or nonzero torchrun failure appears.
- Required preflight artifacts are missing.

Eval handoff remains blocked until a later authorized SFT run produces checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM/test accepts explicit replacements.

## Completion Marker

```yaml
task_id: M1-S23-PARSERPATCH-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
pr: https://github.com/peteryang1/coding_agent_playground/pull/49
pr_head_reviewed: 9393fdec8e5fef7df250743e1a958436a8dfa79a
previous_pass_head: 1ddfe31d8345418572a6d70d1ba15da424fd7aef
pm_requested_head_checked: 6dd0f1bfe1635af650a7fbc928bfbabe4c8c4098
parser_code_changed_after_previous_pass_head: false
prior_missing_pr_blocker: superseded
required_output_when_pr_exists:
  - PASS_FOR_PM_RETRY
  - exact_blocker
no_ltp_gpu_sft_eval_dry_run_by_test1: true
peer_send_pm_used: false
```
