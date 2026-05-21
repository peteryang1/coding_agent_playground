# Dev 1 Same-Node Review - M1-S23-SAME-NODE-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-SAME-NODE-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_same_node_review.md`  
Execution boundary: no LTP, GPU, preflight, SFT, eval, remote commands, remote experiment, or dry-run by `intern_code_dev_1`.

## Result

`BLOCKER_MISSING_ENFORCEABLE_DIFFERENT_NODE_PLACEMENT_PLAN`

The same-node stopped runtime evidence is sufficient and internally consistent: dev_2 correctly stopped the fresh allocation before source/data transfer, preflight, or SFT because LTP assigned the exact SXid node PM instructed dev_2 to avoid. However, I do not see a separate dev_2 placement plan that can enforce or materially improve different-node placement before PM authorizes another runtime. The current evidence only recommends such a mechanism.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_sxid_differentnode_preflight_sft_runtime.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_sxid_differentnode_preflight_sft_tracking.md`
- Prior context from:
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_cephfuse_preflight_sft_tracking.md`
  - `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_cephfuse_runtime_review.md`

## Same-Node Runtime Facts

Task reviewed: `M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`.

Authorization required dev_2 to avoid:

```text
lg-cmc-b7r202-q03u26-h200-000730
lg-cmc-b7r202-p07u16-h200-000708
lg-cmc-b7r401-a04u26-h200-000769
lg-cmc-b7r202-q04u06-h200-000725
```

The authorization also required same-SXid-node handling: stop/release and do not run preflight/SFT.

Observed assignment:

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
RUNNING observed: 2026-05-21T14:03:41Z
endpoint: ssh -p 39629 root@10.100.22.36
assigned node: lg-cmc-b7r202-q03u26-h200-000730
avoid/SXid node: lg-cmc-b7r202-q03u26-h200-000730
node decision: SAME_SXID_NODE_BLOCKER
```

dev_2 action:

- preflight: not run
- SFT: not run
- eval: not authorized and not run
- source/data transfer: not performed because avoid-node gate failed first
- remote project source/dependency network: none

Stop proof:

```text
stop timestamp UTC: 2026-05-21T14:04:01Z
post-stop state: STOPPED (Completed)
completed: 2026-05-21 14:04:32
endpoint proof: ssh -p 39629 root@10.100.22.36 refused connection after stop
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

## Review Decision

Status of dev_2 stopped evidence: PASS.

The stop decision was correct. Running preflight or SFT on `lg-cmc-b7r202-q03u26-h200-000730` would have violated the same-SXid-node stop condition from the PM authorization.

Status of placement plan: BLOCKED.

The final dev_2 runtime evidence states:

```text
Final next routing recommendation: a future retry needs fresh PM authorization and a mechanism to avoid scheduling onto lg-cmc-b7r202-q03u26-h200-000730 and the prior failed nodes, or a compute/LTP placement route that can guarantee a different physical node before dev_2 consumes another runtime attempt.
```

That is a recommendation, not an enforceable placement plan. I did not find a current durable file that names a concrete next placement route, node-exclusion mechanism, reservation strategy, VC/queue change, or pre-allocation validation process that would prevent consuming another authorization on the same avoided node.

Exact remaining blocker:

```text
BLOCKER_MISSING_ENFORCEABLE_DIFFERENT_NODE_PLACEMENT_PLAN
```

## Required Next Runtime Conditions

Before `PASS_FOR_PM_NEXT_RUNTIME`, PM should require dev_2 or the resource owner to provide one of:

- an enforceable LTP/compute placement mechanism excluding `lg-cmc-b7r202-q03u26-h200-000730` and prior failed nodes;
- a different VC/queue/node-selection route with durable rationale;
- a pre-allocation validation procedure that does not consume the runtime attempt if an avoided node is assigned;
- or an explicit PM waiver accepting repeated stop-and-release attempts as the placement strategy.

Any future runtime must preserve the prior gates:

- no remote git clone/fetch/GitHub/source/dependency download on GPU node;
- local bundle/checksum source transfer only after node gate passes;
- `/home/xu.yang/coding_agent_playground/outputs` CephFS storage and capacity proof;
- structured preflight before SFT;
- SFT only if preflight `PASS` and `sft_allowed=true`;
- stop proof and artifact preservation.

## Completion Marker

```yaml
task_id: M1-S23-SAME-NODE-REVIEW-DEV1
owner: intern_code_dev_1
result: BLOCKER_MISSING_ENFORCEABLE_DIFFERENT_NODE_PLACEMENT_PLAN
pass_for_pm_next_runtime: false
same_node_stopped_evidence_reviewed: true
same_node_stop_action_correct: true
assigned_node: lg-cmc-b7r202-q03u26-h200-000730
avoid_node_matched: true
preflight_run: false
sft_run: false
eval_run: false
source_data_transfer_run: false
remote_project_source_dependency_fetch_run: false
ltp_final_state: STOPPED_COMPLETED
endpoint_after_stop_refused: true
no_active_milestone_gpu_after_stop: true
placement_plan_available: false
exact_blocker: BLOCKER_MISSING_ENFORCEABLE_DIFFERENT_NODE_PLACEMENT_PLAN
no_ltp_gpu_preflight_sft_eval_remote_commands_by_dev1: true
```
