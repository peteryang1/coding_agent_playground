# Test 1 S22 Preflight Parser Gate

Task ID: `M1-S22-PREFLIGHT-PARSER-GATE-TEST1`
Owner: `intern_code_test_1`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_preflight_parser_gate.md`
Status timestamp: `2026-05-21T11:36:37Z`

## Result

`PASS_FOR_PM_RETRY`

No SFT, GPU command, LTP action, eval, dry-run, or remote experiment was run by `intern_code_test_1`.

## PR #45 Latest Re-Gate Result

Gate result for PR #45 latest head / `M1-S22-PREFLIGHT-PARSER-FIX-DEV4`:

`PASS_FOR_PM_RETRY`

Inputs checked:

- Dev_4 evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_preflight_parser_fix.md`.
- PR: `https://github.com/peteryang1/coding_agent_playground/pull/45`.
- Corrected latest PR head reviewed: `01eebb7508768cd8b8ba3a1601e4a1f3774c27b4`.
- Prior superseded head from first PM message: `4a7c5c1945734f290ed55eec23ce3a48226a4926` was not used for the final decision.
- Script reviewed from latest PR head: `scripts/parse_s22_preflight_health.py`.
- PM request states PR #45 is open, non-draft, `MERGEABLE` / `CLEAN`; dev_4 evidence also records open/non-draft `MERGEABLE` / `CLEAN`.

No SFT/GPU/eval/dry-run was run. No parser execution was performed by test_1; review was source/evidence only.

### Latest Passing Findings

False-positive suppression: PASS.

- Generated command/process/evidence/history/task/summary/readme/preflight_result/health_status/parser/manifest/xtrace files remain excluded from actionable matching.
- Excluded matches are preserved under `ignored_non_actionable_matches` and compatibility field `non_actionable_matches`.
- This addresses the prior broad recursive scan failure mode where copied command/process/evidence/generic text produced `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.

Real-fault detection preservation: PASS.

- The parser preserves detection for Xid in kernel/dmesg/NVRM logs.
- It preserves invalid peer GPU memory, rank `SIGABRT`, torch `ChildFailedError`, NCCL/collective failure, NVLink down/fail/fatal/CRC/replay/error signatures, and nonzero torchrun/all-reduce status handling.
- ECC false-negative risk is addressed: fatal ECC is always actionable in allowlisted sources, and uncorrected ECC counters are parsed from the ECC/uncorrected field suffix so unrelated zeros such as GPU id, rank, or timestamps do not suppress a nonzero ECC counter.

Structured preflight fields: PASS.

The latest parser now emits the required top-level compatibility fields:

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

Storage/artifact gate: PASS.

- The parser defines expected output root `/home/xu.yang/coding_agent_playground/outputs`.
- `home_xu_yang_storage_status=PASS` only when the parsed preflight directory is under that root.
- `home_xu_yang_storage_status=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS` is included in missing required checks and blocks `sft_allowed`.
- Dev_4 evidence keeps future output, preflight, logs, checkpoints, run metadata, temporary converted datasets, and intermediates under `/home/xu.yang/coding_agent_playground/outputs`.

Conditional SFT rule: PASS.

- `sft_allowed` is true only when parser `status == "PASS"`.
- `sft_skip_reason` is populated when parser status is not PASS.
- This still does not authorize SFT by itself; any runtime still requires fresh PM authorization and a parser-fixed preflight PASS.

No-execution boundary: PASS.

- Dev_4 evidence states no LTP/GPU/SFT/eval/dry-run command was run for this package.
- The script is local-artifact-only and does not itself contact GPU nodes or launch SFT/eval.

### Remaining Runtime/Eval Boundaries

`PASS_FOR_PM_RETRY` means the no-execution parser package gate passes. It does not authorize runtime by itself.

Before any SFT launch, PM still needs a fresh runtime authorization, and the future runtime must provide:

- Parser-fixed structured preflight PASS.
- `/home/xu.yang/coding_agent_playground/outputs` artifact preservation.
- Capacity/topology/NVLink/NCCL status evidence.
- Different-node/resource evidence as required by the runtime gate.
- No recurrence of old blocker signatures.

Eval handoff remains blocked until a later PM-authorized SFT run produces checkpoint/model artifacts plus `trainer_state.json` and `all_results.json`, or PM/test explicitly accepts replacement artifacts.

## Superseded PR #45 Refresh Result

Superseded gate result for older PR #45 head `84959deac17560995a51a8f9a7be9093624cdf16`:

`BLOCKED_STRUCTURED_FIELDS_AND_STORAGE_STATUS`

Inputs checked:

- Dev_4 evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_preflight_parser_fix.md`.
- PR: `https://github.com/peteryang1/coding_agent_playground/pull/45`.
- PR state from PM request and fetched head: open, non-draft, `MERGEABLE` / `CLEAN`.
- PR head fetched for read-only review: `84959deac17560995a51a8f9a7be9093624cdf16`.
- Script reviewed from PR head: `scripts/parse_s22_preflight_health.py`.

No SFT/GPU/eval/dry-run was run. No parser execution was performed by test_1; review was source/evidence only.

### Passing Findings

False-positive suppression: PASS for direction.

- The parser classifies generated command/process/evidence/history/task/summary/readme/preflight_result/health_status/parser/manifest/xtrace files as excluded.
- Excluded matches are retained under `ignored_non_actionable_matches` for audit instead of becoming actionable health failures.
- Dev_4 evidence correctly identifies the prior false fail as broad recursive scanning over command/process/evidence/generic text.

Real-fault detection preservation: PASS for source review.

- The script retains detection paths for Xid in dmesg/journal/kernel/NVRM logs.
- It retains invalid peer GPU memory, SIGABRT, torch `ChildFailedError`, NCCL/collective failures, fatal/nonzero ECC, NVLink down/fail/fatal/CRC/replay/error signatures, and nonzero torchrun status handling.
- Actionable sources include hardware/runtime-oriented logs such as dmesg/journal/kernel/NVRM, nvidia-smi, NVLink/topology, torch NCCL/allreduce, stdout, stderr, and training logs.

No-execution boundary: PASS.

- Dev_4 evidence states no LTP/GPU/SFT/eval/dry-run command was run for the package.
- The script is local-artifact-only and does not itself contact GPU nodes or launch SFT/eval.

Storage policy in evidence: PASS for documented future defaults.

- Dev_4 evidence keeps future output, preflight, logs, checkpoints, temporary converted datasets, and intermediates under `/home/xu.yang/coding_agent_playground/outputs`.
- Existing non-`/home/xu.yang` paths are read-only required inputs: base model, dependencies, and source dataset.

### Blocking Findings

Structured preflight fields: BLOCKER.

The current script emits useful structured fields, but it does not yet satisfy the full test_1 gate contract. Missing or mismatched required fields:

- No explicit `preflight_result` field or direct equivalent named for the final preflight marker; only top-level `status`.
- No explicit `health_result` field or direct equivalent named for parser health status; only top-level `status`.
- No `non_actionable_matches` field by that name; current field is `ignored_non_actionable_matches`. This is close, but future gate consumers need either the required name or a documented compatibility alias.
- No `torch_nccl_allreduce_exit` field by that name; torch status is nested under `checks.torch_nccl.exit_code`.
- No `capacity_probe_status` field by that name; capacity is nested under `checks.capacity.status`.
- No `different_node_gate` field.
- No `home_xu_yang_storage_status` field.
- No `topology_capture_status` field by that name; topology is nested under `checks.topology.status`.
- No `nvlink_capture_status` field by that name; NVLink is nested under `checks.nvlink.status`.
- No explicit `sft_allowed` boolean; current equivalent is nested as `decision.sft_allowed_if_pm_authorized`.
- No `sft_skip_reason` field when SFT is not allowed; current reasons are nested under `decision.reason`.

Storage/artifact enforcement: BLOCKER.

- The script records `preflight_dir`, but it does not validate or emit whether `preflight_dir`, `out_json`, and `out_text` are under `/home/xu.yang/coding_agent_playground/outputs`.
- The required gate field `home_xu_yang_storage_status` is absent, so PM/test cannot distinguish compliant `/home/xu.yang` artifacts from accidental local/tmp or non-CephFS outputs using the parser JSON alone.

SFT-allowance clarity: BLOCKER.

- The script correctly gates `decision.sft_allowed_if_pm_authorized` on `status == "PASS"`.
- However, the gate requires a direct structured `sft_allowed` boolean and `sft_skip_reason` when false so the launch wrapper can consume the parser result without policy interpretation drift.

### Required Fixes For PASS_FOR_PM_RETRY

PR #45 can pass test_1 after dev_4 updates the package to provide one of the following:

- Preferred: update `scripts/parse_s22_preflight_health.py` to emit the required top-level compatibility fields:
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
- Acceptable alternative: dev_4 evidence must define a stable wrapper/manifest schema that maps current nested fields to every required gate field and records `home_xu_yang_storage_status` and `different_node_gate` outside the parser.
- Add parser or wrapper validation that output artifacts are under `/home/xu.yang/coding_agent_playground/outputs`, or emit `home_xu_yang_storage_status: FAIL` with exact path blockers.
- Keep the current false-positive suppression and real-fault detection behavior.

Those fixes are present in latest reviewed head `01eebb7508768cd8b8ba3a1601e4a1f3774c27b4`; see the latest result above.

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

Current gate status after latest PR #45 re-gate:

- Dev_4 parser package evidence is accepted for no-execution PM retry gate.
- PR #45 latest head `01eebb7508768cd8b8ba3a1601e4a1f3774c27b4` has been evaluated by source/evidence review.
- No dev_1 parser review has been evaluated in this gate yet.
- No parser-fixed preflight PASS exists.
- No SFT run exists after parser fix.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` exists.

## Completion Marker

```yaml
task_id: M1-S22-PREFLIGHT-PARSER-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
pr_45_head_reviewed: 01eebb7508768cd8b8ba3a1601e4a1f3774c27b4
superseded_pr_45_head_not_used_for_final_decision: 4a7c5c1945734f290ed55eec23ce3a48226a4926
false_positive_suppression_required: true
real_fault_detection_required: true
structured_preflight_fields_required: true
home_xu_yang_required: true
sft_allowed_only_after_parser_fixed_preflight_pass: true
eval_handoff_allowed_now: false
sft_gpu_eval_dry_run_executed_by_test1: false
blocking_findings: []
next_gate_result_options:
  - PASS_FOR_PM_RETRY
  - PASS_FOR_NEXT_PM_DECISION
  - exact_blocker
```
