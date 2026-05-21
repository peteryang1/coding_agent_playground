# PM Authorization - S23 SXid Different-Node Preflight/SFT Retry

Task ID: `M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Authorization timestamp: `2026-05-21T13:58:14Z`

## Decision

PM authorizes exactly one fresh owner-executed LTP/GPU runtime attempt after the ceph-fuse fixed run stopped before SFT with `BLOCKED_PREFLIGHT_HEALTH_SIGNATURE_NO_SFT`.

This authorization is for a fresh different-node preflight plus conditional SFT only. It does not authorize eval.

## Gate Basis

Durable evidence reviewed:

```text
evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md
evidence/gpu_s23_cephfuse_preflight_sft_tracking.md
evidence/dev_1_s23_cephfuse_runtime_review.md
evidence/test_1_s23_cephfuse_runtime_gate.md
evidence/dev_4_s23_cephfuse_health_triage.md
evidence/dev_3_s23_cephfuse_runtime_data_confirm.md
evidence/test_2_s23_cephfuse_runtime_eval_blocked.md
evidence/dev_2_s23_cephfuse_resource_recovery.md
```

Gate conclusions:

```text
ceph-fuse/storage bootstrap: fixed for the prior run
/home/xu.yang storage: PASS
24GiB capacity probe: PASS_AND_CLEANED
local source/data transfer and checksum verification: PASS
remote project source/dependency network: not used
functional torch/NCCL all-reduce: TORCHRUN_EXIT=0 and ALLREDUCE_OK
SFT skip on failed preflight: correct
checkpoint/model/trainer_state/all_results: absent because SFT was not run
resource release: STOPPED (Completed), endpoint refused, no running coding-agent-playground jobs
```

Current blocker classification:

```text
primary blocker: real_or_unknown_time_sxid_nvlink_node_health
exact blocker: SXid 20009 / NVLink RX Short Error Rate on node lg-cmc-b7r202-q03u26-h200-000730
secondary parser noise: NCCL_ASYNC_ERROR_HANDLING deprecation warnings classified as nccl_or_collective_failure despite TORCHRUN_EXIT=0 and ALLREDUCE_OK
```

PM decision: treat the SXid 20009 finding as node-specific health risk. Do not reuse the flagged node for this retry. A parser-hygiene task will run separately for the benign NCCL warning noise, but the current retry does not wait on that hygiene patch because SXid 20009, not the warning noise, was the blocking signal.

## Authorized Scope

Authorized owner: `intern_code_dev_2`

Authorized allocation count: exactly `1`

Required allocation shape: fresh single-node `8 x H200`.

Node policy:

```text
must be different from lg-cmc-b7r202-q03u26-h200-000730
avoid prior failed/blocked nodes if selectable:
  lg-cmc-b7r202-p07u16-h200-000708
  lg-cmc-b7r401-a04u26-h200-000769
  lg-cmc-b7r202-q04u06-h200-000725
  lg-cmc-b7r202-q03u26-h200-000730
```

If LTP assigns the same flagged node `lg-cmc-b7r202-q03u26-h200-000730`, dev_2 must stop/release it and record the blocker instead of running preflight/SFT.

## Runtime Requirements

dev_2 must:

1. Use `/home/xu.yang/coding_agent_playground/outputs` for generated outputs, logs, temporary converted datasets, preflight artifacts, checkpoints, run metadata, and intermediates.
2. Treat the remote GPU/LTP node as having no external network for project source/dependency purposes.
3. Prepare source/config/scripts/data locally or in a provided workspace.
4. Verify exact source commit, file list, source bundle checksum, critical file checksums, and dataset checksum before transfer.
5. Transfer source/data by `rsync`, `scp`, or tar-over-SSH.
6. Record exact transfer command, destination, checksum/file-count verification, and any transfer warnings.
7. Prove `ceph-fuse`, `/home/xu.yang` CephFS mount, and real-write capacity before preflight.
8. Run structured preflight before SFT.
9. Run SFT only if structured preflight is `PASS` and `sft_allowed=true`.
10. Stop/release the node after checkpoint success, preflight failure, SFT failure, transfer failure, capacity failure, same-node health blocker, endpoint failure, idle/no-progress limit, or PM/test stop instruction.

## Required Evidence

Required files:

```text
evidence/pm_s23_sxid_differentnode_preflight_sft_authorization.md
evidence/dev_2_s23_sxid_differentnode_preflight_sft_runtime.md
evidence/gpu_s23_sxid_differentnode_preflight_sft_tracking.md
workspace/interns/intern_code_dev_2/status.md
```

Required final result:

```text
complete checkpoint/model with trainer_state.json, all_results.json, and stop proof
OR fresh exact runtime blocker with logs/preflight fields/node/job/status/stop proof/no-running-job proof
```

Eval remains blocked until PM gates a complete checkpoint/model or served endpoint.

## PM Boundary

PM did not run LTP, GPU commands, remote workspace commands, preflight, SFT, eval, source transfer, or parser execution. PM only reviewed durable evidence and issued this owner authorization.
