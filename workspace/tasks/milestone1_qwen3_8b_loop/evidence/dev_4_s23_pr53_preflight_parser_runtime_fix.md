# M1-S23-PR53-PREFLIGHT-PARSER-RUNTIME-FIX-DEV4

Owner: `intern_code_dev_4`

Date: `2026-05-21`

Scope: no-execution parser/runtime fix package after dev_2's PR #53 placement-probe runtime showed the parser still classified `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings as actionable despite successful torch/NCCL all-reduce.

Runtime boundary: no LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run by dev_4 for this task.

## Inputs Reviewed

Dev_2 runtime evidence:

```text
evidence/dev_2_s23_pr53_placementprobe_preflight_sft_runtime.md
evidence/gpu_s23_pr53_placementprobe_preflight_sft_tracking.md
```

Key facts cited:

```text
source commit: PR #53 merge commit e29c93736be3384663cad953cd18da68c30070fb
frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
endpoint: ssh -p 30073 root@10.100.24.12
node: lg-cmc-b7r401-a05u06-h200-000770
forbidden-node gate: PASS_NON_FORBIDDEN
home output root: /home/xu.yang/coding_agent_playground/outputs
capacity: PASS_AND_CLEANED
topology capture: PRESENT
NVLink capture: PRESENT
torch all-reduce: TORCHRUN_EXIT=0 and ALLREDUCE_OK world_size=8 value=36.0
structured preflight: FAIL_HEALTH_SIGNATURE
sft_allowed: false
SFT/checkpoint/model/trainer_state/all_results/eval: not produced
stop proof: STOPPED (Completed), endpoint refused after stop, no active coding-agent-playground job
```

The exact blocker from dev_2:

```text
BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE
fault_count: 8
representative match: torch_nccl_allreduce.log line 5, "Warning: Environment variable NCCL_ASYNC_ERROR_HANDLING is deprecated; use TORCH_NCCL_ASYNC_ERROR_HANDLING instead"
```

## Diagnosis

PR #53 correctly made `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings non-actionable when the same parsed source contained both:

```text
TORCHRUN_EXIT=0
ALLREDUCE_OK
```

The runtime evidence shows the current preflight artifact contract can split all-reduce success proof across torch/NCCL/allreduce artifacts. In that layout, a warning line in `torch_nccl_allreduce.log` may be scanned before or independently from the status artifact that proves `TORCHRUN_EXIT=0` and `ALLREDUCE_OK`.

Root cause:

```text
source-local success context was too narrow for the real preflight artifact layout.
```

Required fix:

```text
Use preflight-level success context across actionable torch/NCCL/allreduce artifacts, but only for the narrow NCCL_ASYNC_ERROR_HANDLING deprecation-warning exception.
```

This does not suppress:

```text
fresh/current or timestamp-unknown Xid/SXid
fatal or nonzero ECC
NVLink link/down/error/replay/CRC faults
NCCL/CUDA invalid peer GPU memory
NCCL unhandled system error
collective/all_reduce failure or exception
nonzero TORCHRUN_EXIT
SIGABRT
ChildFailedError
```

## Patch

Files changed:

```text
scripts/parse_s22_preflight_health.py
tests/test_parse_s22_preflight_health.py
```

Parser change:

```text
1. Add is_torch_nccl_allreduce_source(path).
2. Add preflight_allreduce_ok(files), which combines actionable torch/NCCL/allreduce artifact lines and checks for TORCHRUN_EXIT=0 plus ALLREDUCE_OK.
3. In parse(), compute global_allreduce_ok once.
4. For each actionable source, treat allreduce_ok as source-local success OR preflight-level success for torch/NCCL/allreduce sources.
5. Keep that context wired only through is_benign_nccl_deprecation_warning(), so real NCCL/CUDA/Xid/SXid/ECC/NVLink failures remain actionable.
```

New synthetic coverage:

```text
test_nccl_deprecation_warning_is_non_actionable_when_status_is_split
```

The test models the PR53 runtime shape:

```text
torch_nccl_allreduce.log: NCCL_ASYNC_ERROR_HANDLING deprecation warning lines
torch_nccl_allreduce_status.txt: TORCHRUN_EXIT=0 and ALLREDUCE_OK world_size=8 value=36.0
```

Expected result:

```text
parser status: PASS
sft_allowed: true
nccl_or_collective_failure from warning lines: absent
non_actionable_matches: benign_nccl_async_error_handling_deprecation_warning entries present
```

Existing tests still cover:

```text
same-source warning + TORCHRUN_EXIT=0 + ALLREDUCE_OK -> PASS
SXid 20009 in dmesg source -> FAIL_HEALTH_SIGNATURE
NCCL unhandled system error with TORCHRUN_EXIT=1 -> FAIL_HEALTH_SIGNATURE
```

## Local Static/Test Evidence

Commands run locally only:

```bash
python3 -m py_compile scripts/parse_s22_preflight_health.py tests/test_parse_s22_preflight_health.py
python3 -m pytest tests/test_parse_s22_preflight_health.py -q
```

Observed result:

```text
....                                                                     [100%]
4 passed in 0.02s
```

## PR / Completion Status

```yaml
task_id: M1-S23-PR53-PREFLIGHT-PARSER-RUNTIME-FIX-DEV4
owner: intern_code_dev_4
result: READY_FOR_PR
evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr53_preflight_parser_runtime_fix.md
patch_files:
  - scripts/parse_s22_preflight_health.py
  - tests/test_parse_s22_preflight_health.py
runtime_authorized: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
completion_marker: ready-for-review; owner self-merge requires PM gate
```
