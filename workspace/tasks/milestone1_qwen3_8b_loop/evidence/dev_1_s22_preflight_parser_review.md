# M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Execution boundary: no remote experiments, LTP, GPU, SFT, eval, or dry-run by `intern_code_dev_1`.

## Result

`BLOCKER_ECC_FALSE_NEGATIVE_RISK_IN_PR45`

I cannot output `PASS_FOR_PM_RETRY` for PR #45 yet. The dev_4 parser package now exists and addresses the prior missing-input blocker, but the current parser can miss real fatal/uncorrected ECC evidence when the same line contains any standalone `0`, such as `GPU 0` or a timestamp field. That violates the gate requirement to preserve real ECC failure detection.

## Inputs Checked

- PR #45 metadata from PM request: open, non-draft, `MERGEABLE` / `CLEAN`.
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_preflight_parser_fix.md`
- `scripts/parse_s22_preflight_health.py` from dev_4 PR branch at `/work-agents/intern_code_dev_4/coding_agent_playground/scripts/parse_s22_preflight_health.py`
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

Status: acceptable for the current review.

The parser classifies generated command/process/evidence/history/task/summary/readme/preflight-result/health-status/parser/manifest/xtrace file names as excluded before actionable matching. It records fault-looking text from excluded files under `ignored_non_actionable_matches` instead of `actionable_faults`. This addresses the main observed false positive class from copied search terms in command/process/evidence text.

Residual note: generic `.log`, `.out`, and `.err` files remain actionable by extension. That is acceptable only if future preflight packaging keeps copied historical logs and generated summaries named with the excluded markers or outside the actionable set.

### Real-Fault Detection Preservation

Status: blocker.

The parser preserves detection paths for:

- Xid in kernel/dmesg/journal/NVRM-named artifacts.
- CUDA/NCCL invalid peer GPU memory.
- SIGABRT and torch `ChildFailedError`.
- NCCL or collective/all-reduce failures.
- NVLink down/inactive/fail/fatal/CRC/replay/error lines, with a zero-counter suppression guard.
- Nonzero torchrun exit through `TORCHRUN_EXIT=<n>`.

Blocking issue:

- In `scripts/parse_s22_preflight_health.py`, ECC handling is:

```python
if ECC_RE.search(line) and NONZERO_RE.search(line) and not re.search(r"\b0\b", line.strip()):
    faults.append("ecc_nonzero_or_fatal")
```

This suppresses ECC detection whenever the line contains any standalone `0`, even if the line also contains a real fatal or uncorrected ECC fault. Common current-node lines can include `GPU 0`, device index `0`, timestamp fields, or counter labels containing `0`. Examples that should fail but are at risk of being ignored by this condition:

```text
GPU 0 fatal ECC error detected
GPU 0 volatile uncorrected ECC errors: 1
2026-05-21 GPU 0 aggregate uncorrected ECC: 1
```

Required fix before PASS:

- Treat fatal ECC as actionable regardless of numeric counters.
- For uncorrected ECC counters, parse the relevant ECC counter value instead of rejecting the whole line because some unrelated field is `0`.
- Preserve zero-counter suppression only for explicit healthy zero-count ECC lines.

### Structured Fields

Status: acceptable for current review, subject to the ECC blocker.

The parser emits structured JSON with:

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

The text output also emits a structured status marker and SFT-allowed boolean. Future runtime evidence should map these fields to the test gate's requested `preflight_result`, `health_result`, non-actionable matches, torch NCCL status, capacity status, topology/NVLink capture status, and SFT skip/allow decision.

### `/home/xu.yang` Output Paths

Status: acceptable for current review, subject to the ECC blocker.

dev_4 evidence keeps future output roots under:

- `/home/xu.yang/coding_agent_playground/outputs`
- `/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>`
- `/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs`
- `/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>`
- `/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>`

The parser accepts explicit `--preflight-dir`, `--out-json`, and optional `--out-text`; the proposed future usage writes under `/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>`.

### Execution Boundary

Status: acceptable for current review.

dev_4 evidence states no LTP/GPU/SFT/eval/dry-run command was run for the package. The package describes only local non-runtime parser checks and does not itself authorize future runtime.

## Required Next Fix

Before PM can treat PR #45 as `PASS_FOR_PM_RETRY`, dev_4 should update `scripts/parse_s22_preflight_health.py` so real fatal/uncorrected ECC evidence is not suppressed by unrelated `0` tokens, then refresh `evidence/dev_4_s22_preflight_parser_fix.md`.

## Completion Marker

```yaml
task_id: M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1
owner: intern_code_dev_1
reviewed_pr: PR #45
result: BLOCKER_ECC_FALSE_NEGATIVE_RISK_IN_PR45
pass_for_pm_retry: false
exact_blockers:
  - scripts/parse_s22_preflight_health.py ECC detection can miss real fatal/uncorrected ECC faults when the line contains an unrelated standalone 0 such as GPU 0 or timestamp fields.
required_fix:
  - Parse fatal ECC and nonzero uncorrected ECC counters without rejecting the whole line for unrelated zero tokens.
false_positive_suppression_reviewed: true
real_fault_detection_reviewed: true
structured_fields_reviewed: true
home_xu_yang_paths_reviewed: true
no_remote_experiments_ltp_gpu_sft_eval_dry_run_by_dev1: true
```
