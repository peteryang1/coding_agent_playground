# Test 1 S23 PR57 Runtime Gate

Task ID: `M1-S23-PR57-RUNTIME-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_pr57_runtime_gate.md`
Status timestamp: `2026-05-21T15:52:15Z`

## Result

`WAITING_DEV2_PR57_RUNTIME_EVIDENCE`

No LTP, GPU, preflight, SFT, eval, dry-run, transfer command, remote command, or parser execution was run by `intern_code_test_1`.

This file defines the no-execution post-run gate for dev_2's PR57 runtime evidence. Final result must be refreshed to `PASS_FOR_EVAL_HANDOFF`, `PASS_FOR_NEXT_PM_DECISION`, or an exact blocker after dev_2 writes the required durable evidence.

## Current Inputs Reviewed

Reviewed:

- `task_registry.md`
- `evidence/pm_s23_pr57_preflight_sft_authorization.md`
- prior `evidence/test_1_s23_pr55_sft_blocker_gate.md`

Currently missing for final gate:

- `evidence/dev_2_s23_pr57_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr57_preflight_sft_tracking.md`

## Authorization Facts

PM authorization names:

```text
runtime task: M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2
authorized owner: intern_code_dev_2
authorization timestamp: 2026-05-21T15:50:00Z
authorized source: origin/main commit b4ac31ef1e3772953108348bf099818326ed65cc
PR57 merge: c450429c2e3369adc723d132396399cd17dba684
completion PR58 merge: b4ac31ef1e3772953108348bf099818326ed65cc
fresh allocations authorized: exactly one
eval authorized: false
```

The runtime is not gateable until dev_2 provides final runtime/tracking evidence.

## Supervisor No-External-Network Rule

For this PR57 path, all remote GPU/LTP nodes are treated as no-external-network targets for project code and dependency staging.

Final gate must PASS all of the following:

1. dev_2 prepared code/config/scripts/data in a local or provided workspace before remote use.
2. dev_2 recorded exact source commit `b4ac31ef1e3772953108348bf099818326ed65cc`.
3. dev_2 recorded local file list and local checksums before transfer.
4. dev_2 transferred prepared materials by `rsync`, `scp`, or tar-over-SSH.
5. dev_2 recorded exact transfer command, source path, destination path, and timestamp.
6. dev_2 recorded post-transfer file list/checksum verification on the remote node.
7. dev_2 recorded that no remote `git clone`, `git fetch`, GitHub source fetch, project source download, project dependency download, or remote dependency install/download was used for project code/dependency staging.

Any evidence of remote project source/dependency clone/fetch/download is a gate blocker unless PM explicitly reclassifies the action before the gate is applied.

## Required Runtime Evidence Checklist

The final gate must validate:

- LTP frame/job id, node id, endpoint, start timestamp, and owner.
- Node placement is not a known forbidden node for the current PM authorization.
- `/home/xu.yang/coding_agent_playground/outputs` is used for generated launch outputs, logs, temporary converted datasets, checkpoints, run metadata, and intermediates.
- Non-`/home/xu.yang` paths are limited to existing-required inputs such as base model, source staging, or explicitly justified executable/source staging.
- Storage/capacity proof exists for `/home/xu.yang/coding_agent_playground/outputs`.
- Structured preflight fields are present, including `PREFLIGHT_RESULT`, `SFT_ALLOWED`, storage status, capacity status, topology/NVLink capture status, and torch NCCL/all-reduce status when applicable.
- SFT starts only if `PREFLIGHT_RESULT=PASS` and `SFT_ALLOWED=true`.
- If SFT runs, evidence includes exact SFT command, config path, dataset name, base model path, output/checkpoint path, relevant env, stdout/stderr log, xtrace log, diagnostics, run manifest, and exit status.
- Logs do not regress to old blockers including `DEP_TARGET: unbound variable`, missing dataset info, `KeyError: 'from'`, ENOSPC checkpoint save failure, `datasets.map(num_proc=4)` SyncManager EOF, or prior parser false-positive failure.
- Final model state is classified as either complete checkpoint/model with `trainer_state.json` and `all_results.json`, or exact blocker with missing artifact list and next fix.
- Stop proof includes stop action or terminal-state justification, final LTP status, endpoint-after-stop refusal or equivalent proof, and no-running-job proof.

## Eval Handoff Criteria

Eval handoff remains blocked until the final PR57 runtime evidence proves one accepted model form:

```text
complete checkpoint/model directory: present
trainer_state.json: present, or PM-approved replacement
all_results.json: present, or PM-approved replacement
served endpoint/model id: present if eval expects serving, or PM-approved offline checkpoint path
stop/no-running-job proof: present
```

If no checkpoint/model exists, final result must be `EVAL_HANDOFF_BLOCKED` with the exact runtime blocker.

## Completion Marker

```yaml
task_id: M1-S23-PR57-RUNTIME-GATE-TEST1
owner: intern_code_test_1
result: WAITING_DEV2_PR57_RUNTIME_EVIDENCE
authorized_runtime_owner: intern_code_dev_2
authorized_commit: b4ac31ef1e3772953108348bf099818326ed65cc
required_runtime_evidence:
  - evidence/dev_2_s23_pr57_preflight_sft_runtime.md
  - evidence/gpu_s23_pr57_preflight_sft_tracking.md
no_external_network_gate_required: true
home_xu_yang_outputs_required: true
eval_handoff: BLOCKED_WAITING_MODEL
no_ltp_gpu_preflight_sft_eval_by_test1: true
```
