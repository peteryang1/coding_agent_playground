# Test 1 S22 Preflight Parser Gate

Task ID: `M1-S22-PREFLIGHT-PARSER-GATE-TEST1`
Owner: `intern_code_test_1`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_preflight_parser_gate.md`
Status timestamp: `2026-05-21T11:14:11Z`

## Result

`GATE_DEFINED_WAITING_DEV4_PARSER_PACKAGE`

No SFT, GPU command, LTP action, eval, dry-run, or remote experiment was run by `intern_code_test_1`.

Eval handoff remains blocked until a later PM-authorized SFT run produces checkpoint/model artifacts plus `trainer_state.json` and `all_results.json`, or PM/test explicitly accepts replacement artifacts.

## Basis From Prior Runtime

This gate is based on the final test gate for `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`:

- Dev_2 final runtime result: `BLOCKED_PREFLIGHT_FAILED_NO_SFT_RUN`.
- GPU tracking result: `STOPPED_AFTER_PREFLIGHT_FAILURE_NO_SFT`.
- Fresh node: `lg-cmc-b7r401-a04u26-h200-000769`.
- Different-node gate passed against failed post-PR41 node `lg-cmc-b7r202-p07u16-h200-000708`.
- `/home/xu.yang/coding_agent_playground/outputs` artifact storage passed.
- Capacity probe passed and cleaned.
- Topology/NVLink capture completed.
- Torch 8-rank NCCL all-reduce exited `0`.
- Final marker was `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.
- Failure cause recorded in durable evidence: broad health scan matched evidence text, command text, process text, and generic/historical NVRM/NVLink text.
- Conditional SFT correctly did not run.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` exists.
- Stop proof is present and endpoint refused after stop.

## Required dev_4 Parser Package Checks

The parser refinement package must pass all checks below before test_1 can report `PASS_FOR_PM_RETRY`.

### False Positive Rejection

The package must prevent broad self/command/process/historical text from becoming actionable health failures.

Required behavior:

- Generated command text, shell scripts, command echoes, and argument strings containing search terms must not be classified as live GPU health faults.
- Process listings or process-scan output containing search terms must not be classified as live GPU health faults by themselves.
- Copied historical evidence, previous runtime logs, README snippets, task evidence, or pattern-definition files must not be classified as live GPU health faults by themselves.
- Generic NVRM/NVLink initialization text must be separated from actionable fault signatures.
- Non-actionable matches may be preserved for diagnostics, but must be reported separately from actionable faults.

FAIL conditions:

- Parser still fails solely because it sees its own search terms in command/process/evidence text.
- Parser does not distinguish actionable current-node faults from historical or copied text.
- Parser suppresses evidence entirely instead of preserving non-actionable matches for review.

### Real Fault Detection Preservation

The package must preserve failure detection for real GPU, NVLink, NCCL, and distributed-runtime faults.

Required actionable-fault signatures include:

- Current-node Xid errors.
- Fatal, uncorrected, or otherwise actionable ECC errors.
- NVLink link-down, link error, replay/CRC/fatal counters, or comparable unhealthy-link evidence.
- CUDA/NCCL invalid peer GPU memory or invalid peer access signatures.
- Rank aborts, including `SIGABRT`, tied to current preflight or runtime.
- NCCL collective failure, timeout, nonzero torchrun/all-reduce exit, or distributed collective abort.
- Missing, unhealthy, or inaccessible GPU devices.

FAIL conditions:

- Any prior real-fault class is removed without an accepted replacement.
- Parser returns PASS when current-node actionable Xid/ECC/NVLink/NCCL/rank-abort evidence is present.
- Parser cannot report which actionable fault caused FAIL.

### Structured Preflight Fields

The package must require structured preflight output fields sufficient for durable test review.

Minimum required fields:

- `preflight_result` or equivalent final PASS/FAIL marker.
- `health_result` or equivalent parser health status.
- `actionable_faults` as a structured list.
- `non_actionable_matches` as a structured list.
- `torch_nccl_allreduce_exit` or exact unavailable/blocker field.
- `capacity_probe_status`.
- `different_node_gate`.
- `home_xu_yang_storage_status`.
- `topology_capture_status`.
- `nvlink_capture_status`.
- `sft_allowed` boolean.
- `sft_skip_reason` when `sft_allowed` is false.
- Artifact root path under `/home/xu.yang/coding_agent_playground/outputs`.

FAIL conditions:

- Only free-text PASS/FAIL exists with no structured basis.
- `actionable_faults` and `non_actionable_matches` are conflated.
- The marker allows SFT without an explicit parser-fixed preflight PASS.

### Storage And Artifact Rule

All future preflight, log, diagnostic, config, manifest, run metadata, temporary/intermediate, and SFT output artifacts must use:

`/home/xu.yang/coding_agent_playground/outputs`

FAIL conditions:

- New outputs default outside `/home/xu.yang`.
- Non-`/home/xu.yang` paths are used without existing-required-path justification.
- Preflight artifacts are not durably preserved for PM/test review.

## Conditional SFT Rule

SFT remains forbidden unless a later PM-authorized run has a parser-fixed preflight marker of PASS.

PASS-to-run-SFT requirements for a future authorized runtime:

- Parser package is accepted by PM gate.
- Preflight emits structured fields listed above.
- `preflight_result` is PASS.
- `actionable_faults` is empty.
- Any `non_actionable_matches` are explained and do not include live current-node faults.
- `/home/xu.yang/coding_agent_playground/outputs` storage proof is present.
- Capacity, topology/NVLink capture, and NCCL collective preflight have accepted PASS or accepted unavailable/blocker evidence.

If parser-fixed preflight returns FAIL, the correct runtime behavior is:

- Do not run SFT.
- Preserve artifacts under `/home/xu.yang/coding_agent_playground/outputs`.
- Stop/release the allocation.
- Record exact blocker and stop proof.

## Eval Handoff Gate

Eval handoff remains blocked until a later PM-authorized SFT run produces:

- Complete checkpoint/model artifacts under `/home/xu.yang/coding_agent_playground/outputs`.
- File listing, sizes, and checksums or equivalent integrity proof.
- `trainer_state.json`.
- `all_results.json`.
- Stop/release proof and endpoint refused/unreachable after stop.
- Old failure absence: no `KeyError: from`, missing/wrong `dataset_info`, `datasets.map(num_proc=4)` SyncManager EOF, ENOSPC/safetensors no-space, early wrapper exit before diagnostics, or recurrence of NCCL/NVLink peer-memory failure.

Without those artifacts, the only possible test outcomes are `PASS_FOR_NEXT_PM_DECISION` or an exact blocker, not `PASS_FOR_EVAL_HANDOFF`.

## Current Insufficient Evidence

Current gate status is waiting on dev_4 parser package evidence:

- Required input `evidence/dev_4_s22_preflight_parser_fix.md` is not yet accepted by this gate.
- No parser PR/head metadata has been evaluated in this gate yet.
- No dev_1 parser review has been evaluated in this gate yet.
- No parser-fixed preflight PASS exists.
- No SFT run exists after parser fix.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` exists.

## Completion Marker

```yaml
task_id: M1-S22-PREFLIGHT-PARSER-GATE-TEST1
owner: intern_code_test_1
result: GATE_DEFINED_WAITING_DEV4_PARSER_PACKAGE
false_positive_suppression_required: true
real_fault_detection_required: true
structured_preflight_fields_required: true
home_xu_yang_required: true
sft_allowed_only_after_parser_fixed_preflight_pass: true
eval_handoff_allowed_now: false
sft_gpu_eval_dry_run_executed_by_test1: false
next_gate_result_options:
  - PASS_FOR_PM_RETRY
  - PASS_FOR_NEXT_PM_DECISION
  - exact_blocker
```
