# Test 1 S22 Parser-Fixed Preflight + Conditional SFT Runtime Gate

Task ID: `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_parserfixed_runtime_gate.md`
Status timestamp: `2026-05-21T11:59:49Z`

## Result

`PASS_FOR_NEXT_PM_DECISION`

No SFT, GPU command, LTP action, eval, dry-run, parser execution, or remote experiment was run by `intern_code_test_1`.

Eval handoff status: `EVAL_HANDOFF_BLOCKED`.

## Final Runtime Gate Refresh

Final gate result for `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`:

`PASS_FOR_NEXT_PM_DECISION`

This is not `PASS_FOR_EVAL_HANDOFF`: parser-fixed preflight produced a structured FAIL, SFT was correctly skipped, and no checkpoint/model, `trainer_state.json`, or `all_results.json` exists.

Inputs reviewed:

- `evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md`.
- `evidence/gpu_s22_parserfixed_preflight_sft_tracking.md`.

### Verified Facts

Authorization and staging:

- PM authorization file: `evidence/pm_s22_parserfixed_preflight_sft_authorization.md`.
- Authorized owner: `intern_code_dev_2`.
- Authorized attempts: exactly one fresh parser-fixed preflight plus conditional SFT attempt.
- PR #45 merged at `2026-05-21T11:42:20Z`.
- PR #45 merge commit staged on node: `6f61489e85fcf7e129699061c9ddcb6e8db80926`.
- Remote HTTPS clone stuck on the GPU node; dev_2 stopped it and staged the exact merge commit by tar-over-SSH.
- `PR45_MERGE_COMMIT.txt` records `6f61489e85fcf7e129699061c9ddcb6e8db80926`.

Runtime/resource:

- Frame: `xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z`.
- Endpoint while active: `ssh -p 22662 root@10.100.22.14`.
- Node: `lg-cmc-b7r202-p07u16-h200-000708`.
- Different-node check: PASS versus immediate failed parser preflight node `lg-cmc-b7r401-a04u26-h200-000769`.
- Caveat recorded by dev_2: node matches older post-PR41 NCCL runtime failure node, but PM authorization was "preferably different-node", not a hard rejection.

Storage/artifacts:

- Declared required output root: `/home/xu.yang/coding_agent_playground/outputs`.
- Preflight dir recorded: `/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z`.
- Preserved CephFS mirror: `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z`.
- Parser structured storage status: `HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS`.
- Gate interpretation: this structured storage status is a valid blocker and correctly prevents SFT, even though dev_2 also records artifacts were written through `/home/xu.yang` and preserved on CephFS. This points to a parser path-resolution/classification issue for the next PM decision.

Preflight evidence:

- Capacity probe: PASS_AND_CLEANED, 4 x 6GiB files, `25769803776` bytes verified, then probe files removed.
- Topology: `nvidia-smi topo -m` captured; NV18 between every GPU pair.
- NVLink: `nvidia-smi nvlink --status` captured links 0-17 at 26.562 GB/s per GPU.
- GPU query: 8 x NVIDIA H200 visible; ECC volatile/aggregate uncorrected counters 0 at query time.
- NCCL all-reduce substitute: torchrun 8-rank NCCL all-reduce.
- Torch NCCL result: `TORCHRUN_EXIT=0`, start `2026-05-21T11:55:23Z`, end `2026-05-21T11:55:35Z`.
- NCCL env included `NCCL_DEBUG=INFO`, `NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL`, `NCCL_ASYNC_ERROR_HANDLING=1`, `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`, `CUDA_DEVICE_MAX_CONNECTIONS=1`, and `NCCL_P2P_DISABLE` unset.

Structured parser-fixed health result:

- `PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE`.
- `PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE`.
- `ACTIONABLE_FAULT=true`.
- `SFT_ALLOWED=false`.
- `SFT_ALLOWED_IF_PM_AUTHORIZED=false`.
- `SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE`.
- `TORCH_NCCL_ALLREDUCE_EXIT=0`.
- `CAPACITY_PROBE_STATUS=PASS`.
- `DIFFERENT_NODE_GATE=PASS`.
- `HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS`.
- `TOPOLOGY_CAPTURE_STATUS=PRESENT`.
- `NVLINK_CAPTURE_STATUS=PRESENT`.
- Reason: actionable GPU/NCCL health signature found.

Exact preflight blockers:

- `BLOCKED_PARSERFIXED_PREFLIGHT_FAILED_NO_SFT_RUN`.
- `FAIL_HEALTH_SIGNATURE` from actionable Xid matches in `dmesg_gpu_fault_scan.txt`.
- Structured storage blocker `HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS`.

Conditional SFT/eval:

- SFT was correctly not run because parser-fixed preflight did not PASS and `sft_allowed=false`.
- No SFT command/config/log/checkpoint was generated.
- Checkpoint/model: absent because SFT was not run.
- `trainer_state.json`: absent because SFT was not run.
- `all_results.json`: absent because SFT was not run.
- Eval: not authorized and not run.

Stop proof:

- Stop sent: `2026-05-21T11:56:07Z`.
- Wait result: STOPPED at `2026-05-21T11:56:45Z`.
- LTP status: `STOPPED (Completed)`.
- LTP completed: `2026-05-21 11:56:39`.
- Endpoint proof: SSH to `10.100.22.14:22662` returned `Connection refused`.
- GPU tracking records no active held Milestone GPU for this task.

### Final Decision

`PASS_FOR_NEXT_PM_DECISION`

The runtime obeyed the conditional SFT contract: parser-fixed preflight failed, `sft_allowed=false`, SFT was skipped, artifacts were preserved, and stop proof passed. PM can make the next decision from this complete blocker evidence.

`EVAL_HANDOFF_BLOCKED`

Eval handoff remains blocked because SFT did not run and no checkpoint/model, `trainer_state.json`, or `all_results.json` exists.

## Inputs Watched

Required PM durable inputs:

- Runtime evidence: `evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md`.
- GPU tracking: `evidence/gpu_s22_parserfixed_preflight_sft_tracking.md`.
- PM authorization: `evidence/pm_s22_parserfixed_preflight_sft_authorization.md`.
- Parser package gate: `evidence/test_1_s22_preflight_parser_gate.md`.

Current watched evidence now records final parser-fixed preflight failure, correct SFT skip, missing SFT artifacts because SFT was not run, and stop proof.

## Current Evidence Snapshot

From dev_2 runtime/tracking evidence:

- Task: `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`.
- Authorization basis: `evidence/pm_s22_parserfixed_preflight_sft_authorization.md`.
- PR #45 merge commit: `6f61489e85fcf7e129699061c9ddcb6e8db80926`.
- Conditional SFT rule: run exactly one SFT only if structured parser-fixed preflight is PASS and `sft_allowed=true`.
- Eval authorization: false.
- Frame: `xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z`.
- Job: `coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z`.
- Endpoint: `ssh -p 22662 root@10.100.22.14`.
- Node: `lg-cmc-b7r202-p07u16-h200-000708`.
- Runtime state in current evidence: `ALLOCATED_BOOTSTRAPPING` / `RUNNING_BOOTSTRAPPING`.
- Initial GPU sample: 8 x NVIDIA H200 visible and idle at `2026-05-21T11:46:23Z`.
- Different-node evidence: PASS versus immediate failed preflight node `lg-cmc-b7r401-a04u26-h200-000769`.
- Caveat: node matches older post-PR41 NCCL runtime failure node; dev_2 records PM authorization as "preferably different-node", not a hard rejection.
- Required generated artifact root: `/home/xu.yang/coding_agent_playground/outputs`.
- SFT status in current evidence: not started.
- Eval status in current evidence: not authorized and not run.

## Final Gate Checklist

When dev_2 writes final runtime evidence, test_1 will validate all of the following from durable files only.

### Authorization And Scope

PASS requires:

- Runtime task id is `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`.
- Runtime owner is `intern_code_dev_2`.
- PM authorization file exists and authorizes exactly one parser-fixed preflight plus conditional SFT attempt.
- PR #45 parser package is merged before runtime evidence.
- No eval is run or authorized.

FAIL/BLOCKER conditions:

- More than one runtime attempt is reported without fresh PM authorization.
- Eval is run or prepared as if authorized.
- SFT runs before parser-fixed structured preflight PASS and `sft_allowed=true`.

### `/home/xu.yang` Artifact Paths

PASS requires every generated artifact path to be under:

`/home/xu.yang/coding_agent_playground/outputs`

This includes:

- Preflight directory.
- `health_status.json` and `health_status.txt`.
- Capacity probe artifacts.
- Topology/NVLink/NCCL logs.
- Temporary converted datasets and intermediates.
- SFT logs, generated config, manifest, checkpoint/model output, trainer outputs, and run metadata.

Allowed existing read-only input exceptions:

- Base model: `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`.
- Source dataset: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Dependency archives/wheels if needed: `/mnt/3fs/data/ai4ai/deps`.

FAIL/BLOCKER conditions:

- Generated output/log/checkpoint/tmp/intermediate/run metadata appears outside `/home/xu.yang/coding_agent_playground/outputs`.
- Non-`/home/xu.yang` generated paths lack existing-required-path justification.
- Artifact paths are not recorded durably.

### Parser-Fixed Preflight Fields

PASS requires durable `health_status.json` or equivalent evidence with:

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

PASS-to-allow-SFT requires:

- `preflight_result: PASS`
- `sft_allowed: true`
- `home_xu_yang_storage_status: PASS`
- `capacity_probe_status` accepted as PASS.
- `topology_capture_status` accepted as present/pass.
- `nvlink_capture_status` accepted as present/pass.
- `torch_nccl_allreduce_exit: 0`.
- No actionable fault in `health_result` / `actionable_faults`.

FAIL/BLOCKER conditions:

- Any required parser field is missing.
- `home_xu_yang_storage_status` is not PASS.
- Parser result is WARN/FAIL and SFT still runs.
- Parser result is PASS but required capacity/topology/NVLink/NCCL evidence is missing.

### Capacity, Topology, NVLink, NCCL

PASS requires durable evidence of:

- Capacity probe pass or exact blocker.
- `nvidia-smi -L` or equivalent GPU inventory.
- Topology capture.
- NVLink status/counters or exact unavailable/blocker evidence.
- 8-rank torch NCCL all-reduce or equivalent NCCL collective preflight.
- No current-node Xid, fatal/nonzero ECC, actionable NVLink error, invalid peer memory, SIGABRT, or NCCL collective failure unless recorded as the exact blocker.

### Conditional SFT

If parser-fixed preflight is PASS and `sft_allowed=true`, post-run evidence must include:

- Exact SFT command/env/config.
- Dataset name and source dataset checksum.
- PR39 diagnostics and PR41 single-process preprocessing behavior where applicable.
- Generated config/manifest.
- Runtime logs.
- Checkpoint/model output or exact blocker before checkpoint.
- `trainer_state.json` and `all_results.json`, or PM/test accepted replacements.

If parser-fixed preflight is not PASS or `sft_allowed=false`, PASS-for-next-decision requires:

- SFT not run.
- Exact preflight blocker recorded.
- Artifacts preserved under `/home/xu.yang/coding_agent_playground/outputs`.
- Allocation stopped/released with stop proof.

### Stop Proof

PASS requires:

- LTP status reaches `STOPPED (Completed)` or equivalent terminal stop state.
- Completion timestamp is recorded.
- Endpoint refuses connection or is otherwise unreachable after stop.
- No active GPU allocation remains held for this task.

## Decision Labels

Final test_1 update will use exactly one of:

- `PASS_FOR_EVAL_HANDOFF`: parser-fixed preflight passed, SFT ran under the conditional rule, complete checkpoint/model plus `trainer_state.json` and `all_results.json` or accepted replacements exist, generated artifacts are under `/home/xu.yang`, old failure signatures are absent, and stop proof passes.
- `PASS_FOR_NEXT_PM_DECISION`: runtime evidence is complete but eval handoff remains blocked, for example parser-fixed preflight cleanly fails and SFT is correctly skipped, or SFT exposes a new exact blocker with complete evidence and stop proof.
- Exact blocker: required final evidence is missing, generated paths violate `/home/xu.yang`, SFT runs despite failed/missing parser preflight PASS, old blocker recurs without exact handling, checkpoint/model/trainer outputs are absent after an attempted successful SFT, or stop proof is missing.

## Final Missing Eval Evidence

Current watched evidence still does not include eval-handoff artifacts:

- SFT command/config/logs, because SFT was correctly skipped.
- Checkpoint/model.
- `trainer_state.json`.
- `all_results.json`.

Eval handoff is currently blocked.

## Completion Marker

```yaml
task_id: M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2
gate_owner: intern_code_test_1
runtime_owner: intern_code_dev_2
result: PASS_FOR_NEXT_PM_DECISION
eval_handoff_status: EVAL_HANDOFF_BLOCKED
watched_runtime_evidence: evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md
watched_gpu_tracking: evidence/gpu_s22_parserfixed_preflight_sft_tracking.md
home_xu_yang_required: true
parser_fixed_preflight_required_before_sft: true
sft_allowed_only_if_preflight_pass_and_sft_allowed_true: true
parser_fixed_preflight_result: FAIL_HEALTH_SIGNATURE
home_xu_yang_storage_status: FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
torch_nccl_allreduce_exit: 0
sft_run: false
stop_proof: STOPPED_COMPLETED_ENDPOINT_REFUSED
eval_handoff_allowed_now: false
sft_gpu_eval_dry_run_executed_by_test1: false
```
