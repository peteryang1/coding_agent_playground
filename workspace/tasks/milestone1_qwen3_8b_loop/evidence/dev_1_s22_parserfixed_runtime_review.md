# Dev 1 Runtime Review - M1-S22-PARSERFIXED-RUNTIME-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Reviewed runtime task: `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`  
Evidence date: 2026-05-21  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s22_parserfixed_runtime_review.md`  
Execution boundary: no LTP, GPU, SFT, eval, remote experiment, or dry-run by `intern_code_dev_1`.

## Result

`PASS_FOR_PM_NEXT_DECISION`

dev_2 final parser-fixed runtime evidence is internally reviewable and complete enough for PM's next decision. The runtime did not produce an SFT checkpoint/model because the parser-fixed preflight emitted a structured fail and correctly blocked conditional SFT.

Current runtime blocker for PM decision:

`BLOCKED_PARSERFIXED_PREFLIGHT_FAILED_NO_SFT_RUN`

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/pm_s22_parserfixed_preflight_sft_authorization.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_parserfixed_preflight_sft_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s22_preflight_parser_review.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_preflight_parser_fix.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

## Verified Facts

Authorization and staging:

- PM authorized exactly one owner-executed parser-fixed preflight/SFT runtime attempt for `intern_code_dev_2`.
- PR #45 was merged at `2026-05-21T11:42:20Z`.
- PR #45 merge commit: `6f61489e85fcf7e129699061c9ddcb6e8db80926`.
- dev_2 hit a remote GitHub staging blocker, stopped the stuck clone, then staged the exact PR #45 merge commit to the GPU node by tar-over-SSH.
- Remote repo marker recorded `PR45_MERGE_COMMIT.txt: 6f61489e85fcf7e129699061c9ddcb6e8db80926`.

Allocation:

- Frame: `xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z`.
- Endpoint while active: `ssh -p 22662 root@10.100.22.14`.
- Node: `lg-cmc-b7r202-p07u16-h200-000708`.
- Different-node check passed versus the immediate failed preflight node `lg-cmc-b7r401-a04u26-h200-000769`.
- The node matches an older post-PR41 NCCL failure node, but PM authorization required preferably different from the immediate failed preflight node, not a hard rejection.

Preflight artifacts and storage:

- Preflight run id: `milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z`.
- Preflight dir: `/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z`.
- Preserved CephFS mirror path: `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z`.
- Artifact hashes are recorded for `health_status.json`, `health_status.txt`, `torchrun_status.txt`, and `torch_nccl_allreduce.log`.
- Evidence records 28 top-level preflight files and artifact size `885K`.

Preflight checks:

- Capacity probe: `PASS_AND_CLEANED`, with 4 x 6 GiB real writes verified and removed.
- Topology: `nvidia-smi topo -m` captured; NV18 between every GPU pair.
- NVLink status: links 0-17 captured at 26.562 GB/s per GPU.
- GPU query: 8 x NVIDIA H200 visible; ECC volatile/aggregate uncorrected counters 0 at query time.
- Torch NCCL all-reduce substitute: `TORCHRUN_EXIT=0`, 8 ranks, `NCCL_DEBUG` enabled, `NCCL_P2P_DISABLE` unset.

Structured parser result:

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
HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=actionable GPU/NCCL health signature found
```

Health blocker details:

- `health_status.json` recorded `actionable_fault=true` with Xid matches in `dmesg_gpu_fault_scan.txt`.
- dev_2 evidence names historical Xid 43 entries from `2026-04-17` and Xid 137 / SXid 12028 entries from `2026-05-21 18:18:48` local node time.
- The parser also reported `HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS` even though evidence says artifacts were written through `/home/xu.yang/coding_agent_playground/outputs` and preserved through the CephFS mirror path.
- Whether the storage status is due path resolution/classification or a real path classification issue, it is a structured preflight fail and correctly blocks SFT under the PM authorization.

SFT/eval result:

- SFT was correctly skipped because structured preflight status was not PASS and `sft_allowed=false`.
- No SFT command/config/log/checkpoint was generated for this task.
- Checkpoint/model: absent because SFT was not run.
- `trainer_state.json`: absent because SFT was not run.
- `all_results.json`: absent because SFT was not run.
- Eval was not authorized and was not run.

Stop proof:

- Stop sent at `2026-05-21T11:56:07Z`.
- LTP wait result: STOPPED at `2026-05-21T11:56:45Z`.
- LTP status: `STOPPED (Completed)`.
- Completed timestamp: `2026-05-21 11:56:39`.
- Endpoint proof: SSH to `10.100.22.14:22662` returned `Connection refused`.
- GPU tracking states no active held Milestone GPU remains for this task.

## Review Decision

`PASS_FOR_PM_NEXT_DECISION`

The final evidence supports the current blocked runtime outcome:

- Parser-fixed preflight ran and produced structured fields.
- The conditional SFT rule was obeyed.
- SFT/eval were not run after the structured preflight fail.
- No checkpoint/model/trainer artifacts are expected or present.
- LTP allocation was stopped/released with endpoint refusal proof.

Recommended next PM decision area:

- Treat this as a preflight health/storage blocker, not an SFT training failure.
- Next fix/gate should decide whether the Xid/SXid findings are current-node actionable hardware health failures versus historical scan artifacts, and whether `HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS` is a parser path-resolution bug given the recorded `/home/xu.yang/...` and `/mnt/cephfs/home/xu.yang/...` preserved paths.
- No eval handoff is possible because no checkpoint/model, `trainer_state.json`, or `all_results.json` exists.

## Completion Marker

```yaml
task_id: M1-S22-PARSERFIXED-RUNTIME-REVIEW-DEV1
review_owner: intern_code_dev_1
reviewed_runtime_task: M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2
result: PASS_FOR_PM_NEXT_DECISION
runtime_outcome: BLOCKED_PARSERFIXED_PREFLIGHT_FAILED_NO_SFT_RUN
exact_runtime_blockers:
  - PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
  - ACTIONABLE_FAULT=true with Xid/SXid matches in dmesg_gpu_fault_scan.txt
  - HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
sft_run: false
eval_run: false
checkpoint_model_present: false
trainer_state_present: false
all_results_present: false
ltp_stopped: true
endpoint_refused_after_stop: true
no_ltp_gpu_sft_eval_remote_experiment_dry_run_by_dev1: true
```
