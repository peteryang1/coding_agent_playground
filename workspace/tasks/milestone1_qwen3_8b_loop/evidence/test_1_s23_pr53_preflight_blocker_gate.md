# Test 1 S23 PR53 Preflight Blocker Gate

Task ID: `M1-S23-PR53-PREFLIGHT-BLOCKER-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Fix owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_pr53_preflight_blocker_gate.md`
Status timestamp: `2026-05-21T14:44:57Z`

## Result

`PASS_FOR_PM_RETRY`

No LTP, GPU, preflight, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

This is a no-execution gate pass for PM decision only. It does not authorize runtime by itself.

## Inputs Reviewed

Prior runtime evidence:

- `evidence/pm_s23_pr53_placement_probe_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr53_placementprobe_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr53_placementprobe_preflight_sft_tracking.md`

dev_4 fix package:

- `evidence/dev_4_s23_pr53_preflight_parser_runtime_fix.md`

PR #55:

- PR: `https://github.com/peteryang1/coding_agent_playground/pull/55`
- Title: `M1-S23 PR53 preflight parser runtime fix`
- State: open
- Draft: false
- Mergeability: `MERGEABLE` / `CLEAN`
- Functional patch commit reviewed: `6c959e89a75ce162076292ad6d6c317f421cd45f`
- Current PR head observed by test_1: `b6deabeda9342bd3341fefb25b9f15e99e3903df`

Note: PM cited PR #55 head `6c959e89a75ce162076292ad6d6c317f421cd45f`. GitHub currently reports a later head `b6deabeda9342bd3341fefb25b9f15e99e3903df`; the later commit changes status/task/evidence docs only. The functional parser/test diff is commit `6c959e89a75ce162076292ad6d6c317f421cd45f`.

## Prior Runtime Gate Findings

These runtime facts remain unchanged from the prior gate.

### Node / Placement

PASS.

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
endpoint: ssh -p 30073 root@10.100.24.12
assigned node: lg-cmc-b7r401-a05u06-h200-000770
forbidden-node gate: PASS_NON_FORBIDDEN
```

### Storage / Capacity

PASS.

```text
/mnt/cephfs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
/home/xu.yang/coding_agent_playground/outputs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
capacity probe: 25,769,803,776 bytes
capacity status: PASS_AND_CLEANED
```

### Source / Data Transfer

PASS.

```text
source commit: e29c93736be3384663cad953cd18da68c30070fb
bundle sha256: 34c5655cc8d7003ef3855b7ef5d285311794ab2fcad435dc4d52a3c80c10de77
file list count: 111
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset row count: 10
dataset schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

dev_2 records no remote `git clone`, `git fetch`, GitHub/source fetch, remote source download, or project dependency download on the GPU node.

### Runtime Blocker

The prior runtime blocker was:

```text
BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE
```

Structured preflight fields:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
SFT_ALLOWED=false
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
```

The concrete issue was that PR #53 still classified `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings in `torch_nccl_allreduce.log` as actionable despite:

```text
TORCHRUN_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
```

### SFT / Checkpoint / Eval

PASS for correct blocker handling; eval remains blocked.

```text
SFT command: not run
reason SFT not run: structured preflight FAIL_HEALTH_SIGNATURE and sft_allowed=false
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
```

### Stop Proof

PASS.

```text
post-stop state: STOPPED (Completed)
completed: 2026-05-21 14:30:42
endpoint proof: ssh -p 30073 root@10.100.24.12 refused connection after stop
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

## PR #55 / dev_4 Fix Gate

PASS.

dev_4 diagnosis matches the runtime evidence:

- PR #53 handled only source-local all-reduce success context.
- The real preflight artifact shape can split warning lines and success proof across torch/NCCL/allreduce artifacts.
- The required fix is preflight-level success context across actionable torch/NCCL/allreduce artifacts, only for the narrow `NCCL_ASYNC_ERROR_HANDLING` deprecation-warning exception.

Functional code review:

- Adds `is_torch_nccl_allreduce_source(path)`.
- Adds `preflight_allreduce_ok(files)`.
- Computes `global_allreduce_ok` once in `parse()`.
- Treats all-reduce context as source-local success or preflight-level success only for torch/NCCL/allreduce sources.
- Keeps the context wired through `is_benign_nccl_deprecation_warning()` only.

This is sufficiently narrow for the observed PR53 runtime blocker.

## Real-Fault Preservation

PASS.

The patch does not suppress:

- fresh/current or timestamp-unknown Xid/SXid;
- fatal or nonzero ECC;
- NVLink link/down/error/replay/CRC faults;
- NCCL/CUDA invalid peer GPU memory;
- NCCL unhandled system error;
- collective/all-reduce failure or exception;
- nonzero `TORCHRUN_EXIT`;
- `SIGABRT`;
- `ChildFailedError`.

The tests still cover:

- SXid 20009 remains `FAIL_HEALTH_SIGNATURE`;
- NCCL unhandled system error with `TORCHRUN_EXIT=1` remains `FAIL_HEALTH_SIGNATURE`.

## Test Evidence

PASS.

dev_4 evidence records local-only commands:

```bash
python3 -m py_compile scripts/parse_s22_preflight_health.py tests/test_parse_s22_preflight_health.py
python3 -m pytest tests/test_parse_s22_preflight_health.py -q
```

Observed result:

```text
4 passed in 0.02s
```

New coverage models the PR53 split artifact shape:

```text
torch_nccl_allreduce.log: NCCL_ASYNC_ERROR_HANDLING deprecation warning lines
torch_nccl_allreduce_status.txt: TORCHRUN_EXIT=0 and ALLREDUCE_OK world_size=8 value=36.0
```

Expected and covered:

- parser status `PASS`;
- `sft_allowed=true`;
- no `nccl_or_collective_failure` for the benign warning;
- warning recorded under `non_actionable_matches`.

test_1 did not run tests; this gate relies on source review and dev_4's durable test evidence.

## Remaining Runtime Criteria

No test_1 blocker remains for PM to consider a fresh retry after PR #55/fix package review. Any future runtime still requires fresh PM authorization and must preserve:

1. PR #55 or equivalent fix package merged/accepted as PM requires.
2. Non-forbidden node check before transfer.
3. `/home/xu.yang/coding_agent_playground/outputs` storage and capacity proof.
4. Local/provided workspace source/data bundle transfer and checksum verification.
5. No remote source/dependency network.
6. Structured preflight before SFT.
7. SFT only if preflight is `PASS` and `sft_allowed=true`.
8. If SFT runs, checkpoint/model plus `trainer_state.json` and `all_results.json`, or exact blocker.
9. Stop/no-running-job proof.
10. Eval remains blocked until PM gates a complete checkpoint/model or served endpoint.

## Completion Marker

```yaml
task_id: M1-S23-PR53-PREFLIGHT-BLOCKER-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
runtime_task: M1-S23-PR53-PLACEMENTPROBE-PREFLIGHT-SFT-RUNTIME-DEV2
runtime_owner: intern_code_dev_2
prior_runtime_frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
prior_runtime_node_gate: PASS_NON_FORBIDDEN
prior_runtime_storage_gate: PASS
prior_runtime_transfer_gate: PASS
prior_runtime_stop_gate: PASS
prior_runtime_sft_checkpoint_eval: BLOCKED_ABSENT_SFT_NOT_RUN
fix_task: M1-S23-PR53-PREFLIGHT-PARSER-RUNTIME-FIX-DEV4
pr: 55
pr_head_observed: b6deabeda9342bd3341fefb25b9f15e99e3903df
functional_patch_commit_reviewed: 6c959e89a75ce162076292ad6d6c317f421cd45f
dev4_fix_package: PASS
benign_nccl_warning_split_context_fix: PASS
real_fault_preservation: PASS
owner_tests_reported: "4 passed in 0.02s"
runtime_authorized_by_this_gate: false
future_pm_authorization_required: true
eval_handoff: BLOCKED_NO_MODEL
no_ltp_gpu_preflight_sft_eval_by_test1: true
peer_send_pm_used: false
```
