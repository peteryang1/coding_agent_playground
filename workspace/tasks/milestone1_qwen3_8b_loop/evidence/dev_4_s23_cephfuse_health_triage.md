# M1-S23-CEPHFUSE-HEALTH-TRIAGE-DEV4

Owner: `intern_code_dev_4`

Date: `2026-05-21`

Scope: no-execution triage for the ceph-fuse-fixed preflight `FAIL_HEALTH_SIGNATURE` after PR #51 runtime.

Runtime boundary: no LTP/GPU/preflight/SFT/eval/dry-run command was run by dev_4.

## Inputs Reviewed

PM durable runtime evidence:

```text
evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md
evidence/gpu_s23_cephfuse_preflight_sft_tracking.md
evidence/test_1_s23_cephfuse_resource_gate.md
evidence/dev_1_s23_cephfuse_resource_review.md
evidence/dev_4_s23_cephfuse_launch_package.md
```

Runtime facts reviewed:

```text
runtime task: M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2
PR #51 merge commit used: c02a53a344f2ad7a33b04f529d5125677237d4cb
node: lg-cmc-b7r202-q03u26-h200-000730
endpoint: ssh -p 38862 root@10.100.22.36
final runtime status: BLOCKED_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT
final resource state: STOPPED (Completed)
SFT: not run
eval: not authorized and not run
```

## Preflight Result

The ceph-fuse/storage fix worked. The runtime reached parser-patch preflight and produced the expected durable artifacts under `/home/xu.yang/coding_agent_playground/outputs`.

Passing gates:

```text
TORCH_NCCL_ALLREDUCE_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
ceph-fuse proof: /usr/bin/ceph-fuse; /mnt/cephfs and /home/xu.yang output root on fuse.ceph-fuse
no remote source/dependency network: preserved; local bundle/data transferred and checksum-verified
```

Blocking gate:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE
ACTIONABLE_FAULT=true
SFT_ALLOWED=false
SFT_ALLOWED_IF_PM_AUTHORIZED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
parser exit: 2
```

The conditional runtime behaved correctly: SFT was skipped because the structured preflight did not pass and `sft_allowed=false`.

## Health Signal Classification

### Real Actionable Signal

The primary actionable blocker is the SXid/NVLink health signal in the hardware scan:

```text
dmesg_gpu_fault_scan.txt line 446: SXid 20009, unknown_time, "Non-fatal, Link 57 RX Short Error Rate"
dmesg_gpu_fault_scan.txt line 447: SXid 20009, unknown_time, severity record for Engine instance 57
dmesg_gpu_fault_scan.txt line 448: SXid 20009, unknown_time, data payload record
```

Classification:

```text
kind: SXid
code: 20009
freshness: unknown_time
source: dmesg_gpu_fault_scan.txt
health domain: NVLink / GPU fabric health
triage classification: actionable health signal
SFT decision: block
```

Rationale:

- The parser intentionally treats timestamp-unknown Xid/SXid in allowlisted hardware logs as actionable, because suppressing unknown-time hardware events can hide current node faults.
- SXid 20009 is not generic command/evidence text. It appears in `dmesg_gpu_fault_scan.txt`, which is an allowlisted hardware source.
- The text names an NVLink/fabric-related link error rate on Link 57. It is marked non-fatal, but it is still a real GPU fabric health signal that should block SFT until PM/resource/test decide whether the node is acceptable.
- This preserves the existing real-fault detection policy for Xid/SXid/ECC/NVLink/NCCL/SIGABRT/collective failures.

### Benign Parser Noise

The current parser also classified NCCL deprecation warnings in the successful all-reduce log as `nccl_or_collective_failure`:

```text
torch_nccl_allreduce.log lines 5-22:
  NCCL_ASYNC_ERROR_HANDLING deprecation warnings
TORCHRUN_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
```

Classification:

```text
kind: NCCL deprecation warning
source: torch_nccl_allreduce.log
functional all-reduce result: PASS
triage classification: benign warning / parser noise
SFT decision impact for this run: none, because SXid 20009 independently blocks
```

Rationale:

- The warning is about a deprecated environment variable name/behavior, not an actual NCCL collective failure.
- The same log records `TORCHRUN_EXIT=0` and `ALLREDUCE_OK world_size=8 value=36.0`.
- The parser regex currently matches the substring `NCCL...ERROR` inside `NCCL_ASYNC_ERROR_HANDLING`, which is too broad for deprecation warnings.
- This should not be used as evidence that the NCCL all-reduce failed.

## Triage Decision

```text
primary blocker: real SXid 20009 / NVLink RX Short Error Rate health signal
secondary parser noise: NCCL_ASYNC_ERROR_HANDLING deprecation warnings misclassified as nccl_or_collective_failure
current preflight decision: FAIL_HEALTH_SIGNATURE remains correct because of SXid 20009
SFT decision: do not run SFT from this preflight
same-node retry: not recommended without PM/resource/test acceptance of SXid 20009 risk
```

No parser/spec PR is required for this specific blocker package because removing the benign NCCL deprecation warning from actionable matches would not change the current run decision: SXid 20009 still blocks. A future parser hygiene task can narrow `NCCL_FAILURE_RE` so deprecation warnings are recorded as non-actionable when `TORCHRUN_EXIT=0` and `ALLREDUCE_OK` are present.

## Future Parser Hygiene Recommendation

If PM assigns a parser patch, the safe change would be:

```text
1. Keep NCCL/CUDA invalid peer memory, unhandled system error, collective failure, all-reduce exception, nonzero torchrun exit, SIGABRT, and ChildFailedError actionable.
2. Treat deprecation warning lines such as NCCL_ASYNC_ERROR_HANDLING warnings as non-actionable when the same preflight log reports TORCHRUN_EXIT=0 and ALLREDUCE_OK.
3. Preserve SXid/Xid freshness policy unchanged: fresh/current and timestamp-unknown Xid/SXid in allowlisted hardware logs block; stale historical records are audit-only.
4. Add synthetic tests for:
   - SXid 20009 unknown_time in dmesg source -> FAIL_HEALTH_SIGNATURE.
   - NCCL_ASYNC_ERROR_HANDLING deprecation warning plus TORCHRUN_EXIT=0 plus ALLREDUCE_OK -> no nccl_or_collective_failure from that warning alone.
   - NCCL unhandled system error or invalid peer memory -> FAIL_HEALTH_SIGNATURE.
```

This future patch is hygiene, not an unblock for the current ceph-fuse-fixed runtime.

## Preserved Rules

```text
/home/xu.yang output rule: preserved
no remote GitHub/source/dependency network rule: preserved
local bundle/checksum transfer rule: preserved
real Xid/SXid/ECC/NVLink/NCCL fault detection: preserved
conditional SFT only after PASS + sft_allowed=true: preserved
```

## Completion Status

```yaml
task_id: M1-S23-CEPHFUSE-HEALTH-TRIAGE-DEV4
owner: intern_code_dev_4
result: COMPLETE_FOR_TRIAGE_READY_FOR_PM_REVIEW
evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_cephfuse_health_triage.md
primary_blocker: SXid 20009 / NVLink RX Short Error Rate
benign_noise_identified: NCCL_ASYNC_ERROR_HANDLING deprecation warnings
parser_or_spec_pr_opened: false
reason_no_pr: evidence-only triage; current run remains blocked by real SXid 20009 even after excluding benign NCCL warning noise
runtime_authorized: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
```
