# Dev 1 PR53 Preflight Blocker Review - M1-S23-PR53-PREFLIGHT-BLOCKER-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-PR53-PREFLIGHT-BLOCKER-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_pr53_preflight_blocker_review.md`  
Execution boundary: no LTP, GPU, preflight, SFT, eval, remote commands, remote experiment, or dry-run by `intern_code_dev_1`.

## Result

`PASS_FOR_PM_RETRY`

I refreshed the review against PR #55 and `evidence/dev_4_s23_pr53_preflight_parser_runtime_fix.md`. The prior dev_1 blocker is resolved for PM retry gate: dev_4's fix addresses the real PR53 artifact layout where `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings and `TORCHRUN_EXIT=0` / `ALLREDUCE_OK` success markers can be split across torch/NCCL/allreduce artifacts.

Runtime remains separately PM-authorized. This review does not authorize LTP/GPU/preflight/SFT/eval/dry-run.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_pr53_placementprobe_preflight_sft_runtime.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_pr53_placementprobe_preflight_sft_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_ltp_placement_plan.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr53_preflight_parser_runtime_fix.md`
- PR #55 functional head named by PM: `6c959e89a75ce162076292ad6d6c317f421cd45f`
- PR #55 fetched ref head: `b6deabeda9342bd3341fefb25b9f15e99e3903df`

PR #55 note: local fetch of `pull/55/head` resolved to `b6deabeda9342bd3341fefb25b9f15e99e3903df`, which contains PM-named functional commit `6c959e89a75ce162076292ad6d6c317f421cd45f`. The delta after `6c959e8` is docs/status/evidence only: dev_4 status, task README/history/knowledge, dev_4 evidence, milestone history, and task registry.

## Prior Runtime Blocker

The PR53 placement-probe runtime cleared placement, storage, transfer, and data gates, then blocked before SFT:

```text
assigned node: lg-cmc-b7r401-a05u06-h200-000770
forbidden-node gate: PASS_NON_FORBIDDEN
HOME_XU_YANG_STORAGE_STATUS=PASS
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
TORCH_NCCL_ALLREDUCE_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
SFT_ALLOWED=false
```

The exact prior blocker was parser-side:

```text
BLOCKER_PR53_RUNTIME_PARSER_FALSE_POSITIVE_NCCL_ASYNC_WARNING
```

The runtime evidence reported `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings in `torch_nccl_allreduce.log` classified as actionable `nccl_or_collective_failure` despite successful all-reduce. SFT/eval/checkpoint/model/trainer_state/all_results were correctly absent because preflight did not pass.

## Cleared Runtime Gates

Placement: PASS.

- Hostname check ran before transfer.
- Assigned node `lg-cmc-b7r401-a05u06-h200-000770` was non-forbidden.

Storage/capacity: PASS.

- `ceph-fuse` present.
- `/mnt/cephfs` and `/home/xu.yang/coding_agent_playground/outputs` were `fuse.ceph-fuse`.
- 24 GiB capacity probe under `/home/xu.yang/coding_agent_playground/outputs` ended `PASS_AND_CLEANED`.

Source/data transfer: PASS.

- source bundle sha256: `34c5655cc8d7003ef3855b7ef5d285311794ab2fcad435dc4d52a3c80c10de77`
- remote file count: `111`
- dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`
- no remote `git clone`, `git fetch`, GitHub/source fetch, remote source download, or project dependency download was run on the GPU node.

Data: PASS.

- accepted 10-row ShareGPT dataset;
- schema `messages[*].from/value`;
- dataset entry `coding_agent_m1_sft_10_sharegpt`;
- no data-side error was reached.

Stop/release: PASS.

- final state `STOPPED (Completed)`;
- endpoint refused after stop;
- no running `coding-agent-playground` job remained.

## PR #55 Fix Review

Status: PASS.

dev_4 diagnosis is consistent with the runtime facts: PR #53 used source-local all-reduce success context, but the real preflight can split the warning log and success markers across torch/NCCL/allreduce artifacts. The PR #55 functional fix:

- adds `is_torch_nccl_allreduce_source(path)`;
- adds `preflight_allreduce_ok(files)`;
- computes `global_allreduce_ok` once in `parse()`;
- treats `allreduce_ok` as source-local success OR preflight-level success for torch/NCCL/allreduce sources;
- uses that widened context only for `is_benign_nccl_deprecation_warning()`.

This is appropriately narrow. It does not generally suppress NCCL failures; it suppresses only `NCCL_ASYNC_ERROR_HANDLING` deprecation warning lines when preflight-level torch/NCCL/allreduce artifacts prove `TORCHRUN_EXIT=0` and `ALLREDUCE_OK`.

## Real-Fault Preservation

Status: PASS.

The patch preserves actionable detection for:

- fresh/current or timestamp-unknown Xid/SXid;
- fatal or nonzero ECC;
- NVLink link/down/error/replay/CRC faults;
- NCCL/CUDA invalid peer GPU memory;
- NCCL unhandled/system error;
- collective/all_reduce failure or exception;
- nonzero `TORCHRUN_EXIT`;
- `SIGABRT`;
- `ChildFailedError`.

dev_4 evidence reports local static/test commands:

```bash
python3 -m py_compile scripts/parse_s22_preflight_health.py tests/test_parse_s22_preflight_health.py
python3 -m pytest tests/test_parse_s22_preflight_health.py -q
```

Observed result:

```text
4 passed in 0.02s
```

The added test models the PR53 runtime shape:

```text
torch_nccl_allreduce.log: NCCL_ASYNC_ERROR_HANDLING deprecation warnings
torch_nccl_allreduce_status.txt: TORCHRUN_EXIT=0 and ALLREDUCE_OK world_size=8 value=36.0
```

Expected result is parser `PASS`, `sft_allowed=true`, no `nccl_or_collective_failure` from warning lines, and non-actionable audit records for benign warning lines.

I did not run tests, parser, preflight, LTP, GPU, SFT, eval, or dry-run.

## Remaining Conditions For Future Runtime

No dev_1 blocker remains for PM retry gate after PR #55. A future runtime still needs explicit PM authorization and must preserve:

- non-forbidden node gate before transfer;
- no remote source/dependency network;
- local bundle/data transfer and checksum verification;
- `/home/xu.yang/coding_agent_playground/outputs` storage/capacity proof;
- structured preflight before SFT;
- SFT only if preflight `PASS` and `sft_allowed=true`;
- stop proof and artifact preservation.

## Completion Marker

```yaml
task_id: M1-S23-PR53-PREFLIGHT-BLOCKER-REVIEW-DEV1
owner: intern_code_dev_1
result: PASS_FOR_PM_RETRY
pass_for_pm_retry: true
runtime_evidence_reviewed: true
dev4_fix_present: true
dev4_fix_evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr53_preflight_parser_runtime_fix.md
pr55_functional_head_reviewed: 6c959e89a75ce162076292ad6d6c317f421cd45f
pr55_fetched_head_reviewed: b6deabeda9342bd3341fefb25b9f15e99e3903df
delta_after_functional_head_docs_status_evidence_only: true
placement_cleared: true
assigned_node: lg-cmc-b7r401-a05u06-h200-000770
forbidden_node_gate: PASS_NON_FORBIDDEN
storage_cleared: true
capacity_probe_pass_and_cleaned: true
source_transfer_checksum_cleared: true
data_cleared: true
dataset_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
prior_preflight_result: FAIL_HEALTH_SIGNATURE
prior_sft_allowed: false
prior_runtime_blocker: BLOCKER_PR53_RUNTIME_PARSER_FALSE_POSITIVE_NCCL_ASYNC_WARNING
pr55_fix_addresses_prior_blocker: true
real_xid_sxid_detection_preserved: true
real_ecc_detection_preserved: true
real_nvlink_detection_preserved: true
real_nccl_failure_detection_preserved: true
sft_run_by_dev1: false
eval_run_by_dev1: false
ltp_gpu_preflight_sft_eval_remote_commands_by_dev1: false
exact_blockers: []
```
