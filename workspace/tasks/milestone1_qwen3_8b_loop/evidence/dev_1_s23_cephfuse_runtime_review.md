# Dev 1 Runtime Review - M1-S23-CEPHFUSE-RUNTIME-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-CEPHFUSE-RUNTIME-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_cephfuse_runtime_review.md`  
Execution boundary: no LTP, GPU, SFT, eval, remote commands, remote experiment, or dry-run by `intern_code_dev_1`.

## Result

`PASS_FOR_PM_NEXT_DECISION`

Decision classification: `REAL_OR_UNKNOWN_TIME_SXID_NVLINK_NODE_HEALTH_BLOCKER_WITH_SECONDARY_PARSER_NOISE`.

The post-PR51 ceph-fuse-fixed runtime produced sufficient durable evidence for PM's next decision. The run resolved the prior `ceph-fuse: command not found` blocker, proved `/home/xu.yang` CephFS output storage, transferred local source/data by checksum without remote project source/dependency fetch, then stopped correctly because structured preflight failed with `sft_allowed=false`. SFT and eval were correctly not run.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_cephfuse_preflight_sft_tracking.md`

## Runtime Facts

- Authorization: exactly one fresh dev_2 LTP/GPU runtime attempt, conditional SFT only if structured preflight `PASS` and `sft_allowed=true`; eval not authorized.
- Source commit: `c02a53a344f2ad7a33b04f529d5125677237d4cb`.
- PR #51 merge: `2026-05-21T13:23:23Z`.
- LTP frame: `xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z`.
- Node: `lg-cmc-b7r202-q03u26-h200-000730`.
- Endpoint: `ssh -p 38862 root@10.100.22.36`.
- Final runtime status: `BLOCKED_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT`.
- Final GPU tracking status: `STOPPED_AFTER_PREFLIGHT_BLOCKER`.
- Stop proof: post-stop state `STOPPED (Completed)`, completed `2026-05-21 13:39:48`, endpoint refused SSH after stop, and no running `coding-agent-playground` LTP jobs found.

## Fixed Prior Resource Blocker

Status: PASS.

The prior Session 23 resource blocker was `ceph-fuse: command not found`. The final dev_2 evidence shows this was fixed for the new attempt:

- `command -v ceph-fuse`: `/usr/bin/ceph-fuse`
- `ceph-common`: `19.2.3-0ubuntu0.24.04.3`
- `ceph-fuse`: `19.2.3-0ubuntu0.24.04.3`
- `/mnt/cephfs`: `fuse.ceph-fuse`
- `/home/xu.yang/coding_agent_playground/outputs`: `fuse.ceph-fuse`

The 24 GiB capacity probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/...` wrote, synced, deleted, and ended `PASS_AND_CLEANED`.

## Transfer And Storage Contract

Status: PASS.

dev_2 used local bundle and dataset transfer rather than remote project source/dependency fetch:

- bundle sha256: `59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a`
- dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`
- remote file count: `106`
- critical files verified by sha256:
  - `scripts/parse_s22_preflight_health.py`
  - `scripts/train_qwen3_8b_sft.sh`
  - `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`
  - `scripts/write_sft_run_manifest.py`

The scp metadata/truncate warnings are not a dev_1 blocker because the remote files were present and content checks passed. Future runtime evidence should continue to record these warnings separately from content verification.

## Preflight Outcome

Status: BLOCKED before SFT by structured preflight.

Structured preflight fields:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE
ACTIONABLE_FAULT=true
SFT_ALLOWED=false
SFT_ALLOWED_IF_PM_AUTHORIZED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
```

Functional torch/NCCL all-reduce passed:

```text
TORCHRUN_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
```

Representative actionable records from dev_2 evidence:

- `dmesg_gpu_fault_scan.txt` line 446: `SXid 20009`, `unknown_time`, `Non-fatal, Link 57 RX Short Error Rate`.
- `dmesg_gpu_fault_scan.txt` line 447: `SXid 20009`, `unknown_time`, severity record for Engine instance 57.
- `dmesg_gpu_fault_scan.txt` line 448: `SXid 20009`, `unknown_time`, data payload record.
- `torch_nccl_allreduce.log` lines 5-22: `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings classified by the current parser as `nccl_or_collective_failure`.

## Classification

This is not the old ceph-fuse/resource blocker. It is also not the old data/schema, ENOSPC, dataset-map, or NCCL peer-memory training-start blocker, because the run did not reach SFT.

dev_1 classification:

- Primary blocker: real or timestamp-unknown `SXid 20009` NVLink/link health evidence on the allocated node. Under the current PR #49 parser contract, fresh/current or timestamp-unknown Xid/SXid records remain actionable unless there is durable proof they are stale historical audit records.
- Secondary parser issue: `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings in a successful torch all-reduce log appear likely to be parser false positives. They should not by themselves be treated as a real collective failure when `TORCHRUN_EXIT=0` and `ALLREDUCE_OK` are present.
- Evidence sufficiency: sufficient for PM decision. The node, endpoint, storage proof, transfer checksums, structured preflight fields, SFT skip reason, and stop proof are all present.

Therefore the exact blocker for a retry decision is:

```text
BLOCKER_REAL_OR_UNKNOWN_TIME_SXID20009_NVLINK_NODE_HEALTH_ON_NODE_lg-cmc-b7r202-q03u26-h200-000730
```

There is no dev_1 blocker to PM making the next decision from this evidence. The correct next gate is not to run SFT on this stopped allocation; it is for PM to decide between:

- authorizing a fresh different-node runtime attempt that preserves the same ceph-fuse, `/home/xu.yang`, local bundle/checksum, and structured preflight gates; or
- first asking dev_4/test_1 to refine parser handling so NCCL deprecation warnings are not classified as collective failures, while still keeping timestamp-unknown `SXid 20009` actionable unless proven stale.

## SFT / Checkpoint / Eval

Status: correctly absent.

- SFT command: not run.
- Reason: structured preflight failed and `sft_allowed=false`.
- checkpoint/model: absent because SFT was not run.
- `trainer_state.json`: absent because SFT was not run.
- `all_results.json`: absent because SFT was not run.
- eval: not authorized and not run.

## Completion Marker

```yaml
task_id: M1-S23-CEPHFUSE-RUNTIME-REVIEW-DEV1
owner: intern_code_dev_1
result: PASS_FOR_PM_NEXT_DECISION
exact_blocker: BLOCKER_REAL_OR_UNKNOWN_TIME_SXID20009_NVLINK_NODE_HEALTH_ON_NODE_lg-cmc-b7r202-q03u26-h200-000730
parser_false_positive_present: true
parser_false_positive_detail: NCCL_ASYNC_ERROR_HANDLING deprecation warnings classified as nccl_or_collective_failure despite TORCHRUN_EXIT=0 and ALLREDUCE_OK
primary_classification: real_or_unknown_time_sxid_nvlink_node_health
insufficient_evidence: false
ceph_fuse_fixed: true
home_xu_yang_storage_pass: true
capacity_probe_pass_and_cleaned: true
local_bundle_checksum_transfer_pass: true
remote_project_source_dependency_fetch_run: false
preflight_result: FAIL_HEALTH_SIGNATURE
sft_allowed: false
sft_run: false
eval_run: false
ltp_final_state: STOPPED_COMPLETED
endpoint_after_stop_refused: true
no_active_milestone_gpu_after_stop: true
no_ltp_gpu_sft_eval_remote_commands_by_dev1: true
```
