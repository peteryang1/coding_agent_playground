# Test 1 S23 Ceph-Fuse Runtime Gate

Task ID: `M1-S23-CEPHFUSE-RUNTIME-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_cephfuse_runtime_gate.md`
Status timestamp: `2026-05-21T13:54:30Z`

## Result

`BLOCKED_FINAL_RUNTIME_PREFLIGHT_HEALTH_SIGNATURE_NO_SFT`

No LTP, GPU, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

## Inputs Reviewed

Durable inputs:

- `evidence/pm_s23_cephfuse_preflight_sft_authorization.md`
- `evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md`
- `evidence/gpu_s23_cephfuse_preflight_sft_tracking.md`
- Prior test gate: `evidence/test_1_s23_cephfuse_resource_gate.md`

Authorized runtime scope:

- Owner: `intern_code_dev_2`
- Authorized fresh allocations: `1`
- PR #51 merge commit: `c02a53a344f2ad7a33b04f529d5125677237d4cb`
- Conditional SFT only if structured preflight is `PASS` and `sft_allowed=true`
- Eval authorized: `false`
- Remote source/dependency network: forbidden

## Runtime Facts

Final runtime status from dev_2:

```text
status: BLOCKED_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT
frame: xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
node: lg-cmc-b7r202-q03u26-h200-000730
endpoint: ssh -p 38862 root@10.100.22.36
state before stop: RUNNING
final state: STOPPED (Completed)
completed: 2026-05-21 13:39:48
```

The node was a fresh different physical node versus the prior blocked nodes named in the resource gate:

```text
current node: lg-cmc-b7r202-q03u26-h200-000730
prior avoid nodes: lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
different-node gate: PASS
```

## Source / Data Transfer Proof

PASS.

Reviewed source preparation:

```text
source commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
local worktree status: clean
file list count: 106
bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
```

Critical file checksum verification passed for:

- `scripts/parse_s22_preflight_health.py`
- `scripts/train_qwen3_8b_sft.sh`
- `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`
- `scripts/write_sft_run_manifest.py`

Reviewed data proof:

```text
dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

Remote transfer used `scp` and remote checksum verification, with staging under:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging
```

dev_2 records that no remote `git clone`, `git fetch`, GitHub source fetch, project source download, or project dependency download ran on the GPU node.

The `scp` metadata/truncate warnings into CephFS staging are not a gate blocker because dev_2 records the remote files were present and content verification passed by sha256/file count.

## `/home/xu.yang` Storage Gate

PASS.

Reviewed storage proof:

```text
command -v ceph-fuse: /usr/bin/ceph-fuse
ceph-common: 19.2.3-0ubuntu0.24.04.3
ceph-fuse: 19.2.3-0ubuntu0.24.04.3
/mnt/cephfs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
/home/xu.yang/coding_agent_playground/outputs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
df -h /home/xu.yang/coding_agent_playground/outputs: 18P size, 16P available
```

Capacity probe:

```text
path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z
probe: 4 files x 6144 MiB, total 25,769,803,776 bytes
status: PASS_AND_CLEANED
```

This resolves the prior `ceph-fuse: command not found` runtime blocker for this run.

## Structured Preflight Fields

PASS for completeness; FAIL as runtime health decision.

Structured output recorded by dev_2:

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
REASON=actionable GPU/NCCL health signature found
```

Functional torch/NCCL all-reduce succeeded:

```text
TORCHRUN_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
```

However, parser output still set `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE` and `sft_allowed=false`. The exact runtime blocker is:

```text
BLOCKED_PREFLIGHT_HEALTH_SIGNATURE
```

Representative recorded matches:

- `dmesg_gpu_fault_scan.txt` lines 446-448: `SXid 20009`, `unknown_time`, link 57 RX short error rate and related records.
- `torch_nccl_allreduce.log` lines 5-22: `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings classified by the current parser as `nccl_or_collective_failure`.

## Why SFT Was Correctly Skipped

PASS.

The PM authorization and test_1 resource gate allowed SFT only when both conditions held:

- structured preflight result is `PASS`;
- `sft_allowed=true`.

Actual structured fields were:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
SFT_ALLOWED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
```

Therefore dev_2 correctly did not launch SFT. Running SFT after this preflight would have violated the PM authorization and prior test gate.

## Checkpoint / Eval Absence

PASS for correct blocker handling; eval handoff remains blocked.

Reviewed final facts:

```text
SFT command: not run
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
```

No eval handoff is allowed because no checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or PM-approved replacement exists.

## Stop / No-Running-Job Proof

PASS.

Reviewed stop proof:

```text
stop timestamp UTC: 2026-05-21T13:39:17Z
stop command: ltp.py stop xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
stop result: HTTP 202, stop signal sent
post-stop state: STOPPED (Completed)
completed: 2026-05-21 13:39:48
endpoint proof: ssh -p 38862 root@10.100.22.36 refused connection after stop
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
artifact preservation: outputs/logs/preflight/staging artifacts preserved under /home/xu.yang/coding_agent_playground/outputs
```

## Next Acceptance Criteria

Before PM can authorize any further SFT attempt:

1. Treat this run as a final runtime blocker: `BLOCKED_PREFLIGHT_HEALTH_SIGNATURE_NO_SFT`.
2. Do not reuse this node for SFT without PM accepting a specific health-signal interpretation or mitigation.
3. Resolve or explicitly classify the structured preflight findings:
   - SXid 20009 `unknown_time` records in live dmesg scan;
   - current parser classification of `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings.
4. Preserve the successful parts of this run for the next gate:
   - `/home/xu.yang` CephFS proof;
   - 24 GiB capacity probe;
   - local bundle/checksum transfer workflow;
   - dataset sha/count/schema;
   - no remote source/dependency downloads;
   - stop/no-running-job proof.
5. If PM authorizes another attempt, require a fresh preferably different 8xH200 allocation and the same conditional SFT rule: SFT only after structured preflight `PASS` plus `sft_allowed=true`.
6. Eval remains blocked until a later authorized run produces a complete checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM approves a served endpoint/replacement handoff.

## Completion Marker

```yaml
task_id: M1-S23-CEPHFUSE-RUNTIME-GATE-TEST1
owner: intern_code_test_1
result: BLOCKED_FINAL_RUNTIME_PREFLIGHT_HEALTH_SIGNATURE_NO_SFT
runtime_owner: intern_code_dev_2
runtime_task: M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2
frame: xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
node: lg-cmc-b7r202-q03u26-h200-000730
endpoint: ssh -p 38862 root@10.100.22.36
source_data_transfer_gate: PASS
home_xu_yang_storage_gate: PASS
structured_preflight_fields_gate: PASS_COMPLETE_BUT_PREFLIGHT_FAIL
sft_skip_gate: PASS_CORRECTLY_SKIPPED
checkpoint_model_gate: BLOCKED_ABSENT_SFT_NOT_RUN
eval_handoff: BLOCKED_NO_MODEL
stop_no_running_job_gate: PASS
next_pm_decision_required: true
no_ltp_gpu_sft_eval_dry_run_by_test1: true
peer_send_pm_used: false
```
