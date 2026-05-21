# M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Execution boundary: no remote experiments, LTP, GPU, SFT, eval, or dry-run by `intern_code_dev_1`.

## Result

`PASS_FOR_PM_RETRY`

PR #45 latest head reviewed: `01eebb7508768cd8b8ba3a1601e4a1f3774c27b4`.

The prior dev_1 blocker `BLOCKER_ECC_FALSE_NEGATIVE_RISK_IN_PR45` is resolved in the reviewed head. I found no remaining dev_1 launch blocker in the parser package for PM authorization of the next parser-fixed preflight/SFT retry gate.

## Inputs Checked

- PM request metadata: PR #45 open, non-draft, `MERGEABLE` / `CLEAN`.
- dev_4 PR branch:
  - `/work-agents/intern_code_dev_4/coding_agent_playground`, head `01eebb7508768cd8b8ba3a1601e4a1f3774c27b4`
  - `scripts/parse_s22_preflight_health.py`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_preflight_parser_fix.md`
- PM durable evidence:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_nccl_preflight_sft_runtime.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_nccl_preflight_sft_tracking.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_nccl_retry_gate.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_preflight_parser_gate.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s22_nccl_review.md`

No code, parser, dry-run, GPU command, LTP action, SFT, eval, or remote experiment was executed by `intern_code_dev_1`; this is a static review only.

## Prior Runtime Basis

- The authorized fresh different-node preflight used node `lg-cmc-b7r401-a04u26-h200-000769`.
- Preflight artifacts were preserved under `/home/xu.yang/coding_agent_playground/outputs/preflight/...`.
- Capacity probe passed and cleaned up.
- Topology/NVLink evidence was captured.
- The 8-rank torch NCCL all-reduce exited 0.
- The final preflight marker was `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.
- Existing evidence attributes that marker to broad health scanning over evidence/command/process/generic NVRM text.
- SFT was correctly not run after the failed preflight marker.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` exists from that attempt.
- Allocation stop proof exists.

## Gate Findings

### False-Positive Suppression

Status: PASS.

The parser excludes generated command, process, evidence, history, task knowledge, summary, readme, preflight result, health status, parser, manifest, and xtrace file names from actionable matching. Fault-looking terms in excluded files are preserved under `ignored_non_actionable_matches`, not treated as `actionable_faults`.

This directly addresses the observed false-positive source: copied search terms and generic captured text in command/process/evidence material.

### Real-Fault Detection Preservation

Status: PASS.

The reviewed parser preserves detection for:

- Xid in kernel/dmesg/journal/NVRM-named artifacts.
- CUDA/NCCL invalid peer GPU memory.
- SIGABRT and torch `ChildFailedError`.
- NCCL or collective/all-reduce failures.
- NVLink down/inactive/fail/fatal/CRC/replay/error lines.
- Nonzero torchrun exit through `TORCHRUN_EXIT=<n>`.
- Fatal ECC and nonzero uncorrected ECC.

ECC re-check:

- `has_ecc_fault()` now returns actionable for fatal ECC independent of counters.
- For uncorrected ECC, it starts parsing from the uncorrected/ECC match location and uses ECC-field-tied counters, so unrelated earlier zeros such as `GPU 0`, rank `0`, or timestamp fields no longer suppress a nonzero uncorrected ECC counter.
- dev_4 evidence explicitly records the intended behavior:
  - `GPU 0 timestamp ... Uncorrected ECC errors: 1` is actionable.
  - `GPU 0 timestamp ... Uncorrected ECC errors: 0` is non-actionable.

This resolves the prior dev_1 ECC false-negative blocker.

### Structured Fields

Status: PASS.

The reviewed parser emits structured JSON with core fields:

- `schema_version`
- `preflight_dir`
- `status`
- `actionable_fault`
- `actionable_faults`
- `ignored_non_actionable_matches`
- `sources_scanned`
- `sources_excluded`
- `checks`
- `decision.sft_allowed_if_pm_authorized`
- `policy`

It also adds top-level compatibility fields required by the gate:

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

The text output includes the corresponding structured markers, including `PREFLIGHT_RESULT`, `SFT_ALLOWED`, storage status, topology status, NVLink status, capacity status, and torch NCCL all-reduce exit.

### `/home/xu.yang` Output Paths

Status: PASS.

dev_4 evidence keeps future output roots under:

- `/home/xu.yang/coding_agent_playground/outputs`
- `/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>`
- `/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs`
- `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>`
- `/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>`

The parser also computes `home_xu_yang_storage_status`, requires the parsed preflight directory to be under `/home/xu.yang/coding_agent_playground/outputs`, and blocks `sft_allowed` through `WARN_INCOMPLETE` if storage is outside that expected root.

### Execution Boundary

Status: PASS.

dev_4 evidence states no LTP/GPU/SFT/eval/dry-run command was run for this package. The package is a no-execution parser refinement and does not itself authorize future runtime.

## Recommendation

`PASS_FOR_PM_RETRY`

PM can gate PR #45 for owner self-merge from dev_1's review perspective. A future runtime remains conditional on PM authorization, parser-fixed preflight PASS, `/home/xu.yang` artifact preservation, and the existing no-SFT-unless-preflight-PASS rule.

## Completion Marker

```yaml
task_id: M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1
owner: intern_code_dev_1
reviewed_pr: PR #45
reviewed_head: 01eebb7508768cd8b8ba3a1601e4a1f3774c27b4
result: PASS_FOR_PM_RETRY
pass_for_pm_retry: true
exact_blockers: []
prior_blocker_resolved:
  - BLOCKER_ECC_FALSE_NEGATIVE_RISK_IN_PR45
false_positive_suppression_reviewed: true
real_fault_detection_reviewed: true
ecc_parsing_reviewed: true
structured_fields_reviewed: true
home_xu_yang_paths_reviewed: true
dev4_no_ltp_gpu_sft_eval_dry_run_claim_reviewed: true
no_remote_experiments_ltp_gpu_sft_eval_dry_run_by_dev1: true
```
