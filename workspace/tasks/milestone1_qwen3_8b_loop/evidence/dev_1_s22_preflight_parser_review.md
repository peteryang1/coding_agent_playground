# M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Execution boundary: no remote experiments, LTP, GPU, SFT, eval, or dry-run by `intern_code_dev_1`.

## Result

`BLOCKER_MISSING_DEV4_PREFLIGHT_PARSER_FIX_PACKAGE`

I cannot output `PASS_FOR_PM_RETRY` yet because the required dev_4 parser refinement package is absent from the PM durable evidence path.

Missing required input:
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_preflight_parser_fix.md`

## Inputs Checked

- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/assignments.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_nccl_preflight_sft_runtime.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_nccl_preflight_sft_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_nccl_retry_gate.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s22_nccl_review.md`

## Current Facts From Existing Evidence

- The authorized fresh different-node preflight used node `lg-cmc-b7r401-a04u26-h200-000769`.
- Preflight artifacts were preserved under `/home/xu.yang/coding_agent_playground/outputs/preflight/...`.
- The capacity probe passed and cleaned up.
- Topology/NVLink evidence was captured.
- The 8-rank torch NCCL all-reduce exited 0.
- The final preflight marker was `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.
- Existing evidence attributes the failure to a broad health scan matching evidence/command/process/generic NVRM text.
- SFT was correctly not run after the failed preflight marker.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` exists from that attempt.
- The allocation was stopped and the endpoint refused afterward.

## Required Review Once dev_4 Package Exists

False-positive risk gate:
- The parser must not classify generated command text, process listings, prior evidence files, historical logs, or self-authored diagnostic summaries as actionable current health failures.
- The parser should scope actionable health detection to the intended active health/preflight outputs.

False-negative risk gate:
- Detection must remain preserved for real current faults including Xid, fatal ECC, NVLink errors, NCCL invalid peer memory, rank SIGABRT, collective failure/nonzero torchrun, missing/unhealthy GPU, and required path/write failures.

Structured preflight fields gate:
- The package should preserve or add structured fields for capacity probe status, torch NCCL all-reduce status, nvidia-smi/health status, NVLink/topology status, parser health status, and overall preflight result.

Artifact path gate:
- Preflight logs, diagnostics, run metadata, and any generated intermediates must remain under `/home/xu.yang/coding_agent_playground/outputs/...`.
- The package must not regress prior `/home/xu.yang` output preservation requirements.

Scope gate:
- The package must preserve PR39 diagnostics, PR41 single-process preprocessing behavior, and PR43 NCCL environment behavior.
- The package must not include or imply remote experiments, LTP, GPU, SFT, eval, or dry-run execution by dev_4 unless separately authorized by PM.

## Completion Marker

```yaml
task_id: M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1
owner: intern_code_dev_1
result: BLOCKER_MISSING_DEV4_PREFLIGHT_PARSER_FIX_PACKAGE
missing_inputs:
  - workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_preflight_parser_fix.md
pass_for_pm_retry: false
no_remote_experiments_ltp_gpu_sft_eval_dry_run_by_dev1: true
```
