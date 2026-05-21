# Test 1 S23 Same-Node Runtime Gate

Task ID: `M1-S23-SAME-NODE-RUNTIME-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_same_node_runtime_gate.md`
Status timestamp: `2026-05-21T14:16:01Z`

## Result

`BLOCKED_FINAL_PLACEMENT_SAME_SXID_NODE_STOPPED_NO_PREFLIGHT_NO_SFT`

No LTP, GPU, preflight, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

## Inputs Reviewed

- `evidence/pm_s23_sxid_differentnode_preflight_sft_authorization.md`
- `evidence/dev_2_s23_sxid_differentnode_preflight_sft_runtime.md`
- `evidence/gpu_s23_sxid_differentnode_preflight_sft_tracking.md`
- `task_registry.md`
- `blockers.md`

## Authorized Placement Requirement

PM authorized exactly one fresh owner-executed runtime under:

```text
M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2
```

Required placement:

- fresh single-node `8 x H200`;
- must be different from the flagged SXid node `lg-cmc-b7r202-q03u26-h200-000730`;
- should avoid prior failed/blocked nodes if selectable:
  - `lg-cmc-b7r202-p07u16-h200-000708`
  - `lg-cmc-b7r401-a04u26-h200-000769`
  - `lg-cmc-b7r202-q04u06-h200-000725`
  - `lg-cmc-b7r202-q03u26-h200-000730`

Authorization required dev_2 to stop/release if LTP assigned the flagged SXid node instead of running transfer, preflight, or SFT.

## Runtime Evidence Check

Reviewed final dev_2 facts:

```text
final status: BLOCKED_SAME_SXID_NODE_STOPPED_NO_PREFLIGHT_NO_SFT
frame: xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
endpoint: ssh -p 39629 root@10.100.22.36
assigned node: lg-cmc-b7r202-q03u26-h200-000730
avoid/SXid node: lg-cmc-b7r202-q03u26-h200-000730
node decision: SAME_SXID_NODE_BLOCKER
```

Placement gate result:

`PASS_CORRECTLY_STOPPED_ON_FORBIDDEN_NODE`

Reason: the allocation landed on the exact node PM required dev_2 to avoid, and dev_2 stopped/released instead of consuming the node for transfer/preflight/SFT.

## Stop Before Transfer / Preflight / SFT / Eval

PASS.

Reviewed evidence records:

```text
source/data transfer: not performed because avoid-node gate failed first
preflight: not run
SFT: not run
eval: not authorized and not run
remote project source/dependency network: none
```

The node identity check saw bootstrap still in OS package setup:

```text
checked UTC: 2026-05-21T14:03:48Z
process sample: apt update -y
```

Because the placement gate failed first, skipping all later work was correct.

## Checkpoint / Model / Trainer / Eval Artifacts

PASS for absence under the placement blocker.

Reviewed evidence records:

```text
generated /home/xu.yang artifacts: none from this runtime; stopped before transfer/preflight
checkpoint/model: absent; SFT was not run
trainer_state.json: absent; SFT was not run
all_results.json: absent; SFT was not run
eval output: absent; eval was not authorized
```

No eval handoff exists.

## Stop / No-Running-Job Proof

PASS.

Reviewed stop proof:

```text
stop timestamp UTC: 2026-05-21T14:04:01Z
stop command: ltp.py stop xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
stop result: HTTP 202, stop signal sent
post-stop state: STOPPED (Completed)
completed: 2026-05-21 14:04:32
endpoint proof: ssh -p 39629 root@10.100.22.36 refused connection after stop
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

No active `coding-agent-playground` / Milestone 1 GPU allocation remains held for this task.

## Preserved Local Provenance

The local/provided package remains available as future input, but it was not transferred to the forbidden node:

```text
source commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
file list count: 106
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset rows: 10
```

## Placement-Safe Future Authorization Criteria

Before PM can authorize another placement-safe runtime, test_1 requires:

1. A no-submit placement/resource plan from dev_2 that explains how the next allocation can avoid `lg-cmc-b7r202-q03u26-h200-000730` and prior failed nodes.
2. A concrete route to verify node identity before transfer/preflight/SFT.
3. A hard rule to stop/release immediately if the forbidden SXid node is assigned again.
4. Evidence that no current `coding-agent-playground` GPU job is held.
5. PM authorization that names owner, allocation count, node policy, and whether scheduler constraints or manual placement controls are available.
6. The existing runtime safety contract remains required:
   - local/provided workspace bundle and checksum transfer only;
   - no remote source/dependency network;
   - `/home/xu.yang/coding_agent_playground/outputs` for generated artifacts;
   - structured preflight before SFT;
   - SFT only if structured preflight is `PASS` and `sft_allowed=true`;
   - stop/no-running-job proof.

## Completion Marker

```yaml
task_id: M1-S23-SAME-NODE-RUNTIME-GATE-TEST1
owner: intern_code_test_1
result: BLOCKED_FINAL_PLACEMENT_SAME_SXID_NODE_STOPPED_NO_PREFLIGHT_NO_SFT
runtime_task: M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2
runtime_owner: intern_code_dev_2
frame: xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
assigned_node: lg-cmc-b7r202-q03u26-h200-000730
forbidden_sxid_node: lg-cmc-b7r202-q03u26-h200-000730
placement_decision: PASS_CORRECTLY_STOPPED_ON_FORBIDDEN_NODE
transfer_preflight_sft_eval_gate: PASS_NOT_RUN_AS_REQUIRED
checkpoint_model_trainer_eval_gate: PASS_ABSENT_AS_EXPECTED
stop_no_running_job_gate: PASS
future_authorization_requires_placement_plan: true
no_ltp_gpu_preflight_sft_eval_by_test1: true
peer_send_pm_used: false
```
