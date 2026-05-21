# Test 1 S23 PR63 Alternate-Node Runtime Gate

Task ID: `M1-S23-PR63-ALTNODE-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_pr63_altnode_gate.md`
Status timestamp: `2026-05-21T18:53:56Z`

## Result

`WAITING_FINAL_ALTNODE_RUNTIME_EVIDENCE`

No LTP, GPU, preflight, SFT, eval, dry-run, transfer command, remote command, parser execution, or PR code execution was run by `intern_code_test_1`.

The PM-authorized dev_2 alternate-node evidence currently records authorization, local/provided package readiness, planned LTP submit, and initial tracking only. It does not yet include allocation/node placement, transfer/post-transfer verification, `/home/xu.yang` proof, structured preflight result, SFT result, checkpoint/model artifacts, exact runtime blocker, or stop/no-running-job proof. Final pass/fail gate is therefore pending final dev_2 runtime evidence.

## Inputs Reviewed

- `evidence/pm_s23_pr63_altnode_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr63_altnode_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr63_altnode_tracking.md`
- `evidence/test_1_s23_pr61_mca_model_path_gate.md`

## Current Evidence State

### Authorization

PASS for scope definition.

```text
task: M1-S23-PR63-ALTNODE-PREFLIGHT-SFT-RUNTIME-DEV2
owner: intern_code_dev_2
authorization: exactly one fresh bounded alternate-node attempt
eval authorized: false
forbidden nodes:
- lg-cmc-b7r202-k07u06-h200-000580
- lg-cmc-b7r202-q04u06-h200-000725
runtime source commit: 7ad24ae328a350c0be596f41ea143affb4034486
SFT condition: run SFT only if PREFLIGHT_RESULT=PASS and SFT_ALLOWED=true
```

### Local Package Readiness

PASS for pre-submit local/provided package evidence.

```text
source bundle sha256: 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
source file count: 139
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
mcore_adapter file count: 222
LLamaFactory sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
python dependency bundle sha256: e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
flash_attn sha256: c3941d81dd09fd1b39dc3df75097d8aa491250a551c919cd2e3c5df0a514fe0d
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download
```

### Current Runtime Progress

PENDING final evidence.

```text
dev_2 runtime status: LOCAL_PACKAGE_READY_PRE_SUBMIT
tracking status: LTP submit pending
planned frame: xu.yang~coding-agent-playground-m1-s23-pr63-altnode-preflight-sft-20260521T181207Z
planned yaml: /tmp/coding-agent-playground-m1-s23-pr63-altnode-preflight-sft-20260521T181207Z.yaml
initial no-active-job proof: No jobs found
placement decision: pending
CephFS/output root proof: pending
capacity probe: pending
transfer verification: pending
mcore_adapter import check: pending
structured preflight: pending
conditional SFT: pending
checkpoint/model/trainer_state/all_results: pending
stop/no-running-job proof: pending
```

## Final Gate Criteria

When final dev_2 evidence lands, `intern_code_test_1` will gate these required fields:

1. Complete process evidence:
   - allocation frame/job id, endpoint, node id, and placement decision against forbidden nodes;
   - exact transfer command, destination, file lists, bundle checksums, and post-transfer verification;
   - no remote source/dependency network proof;
   - `/home/xu.yang/coding_agent_playground/outputs` proof and capacity probe;
   - `mcore_adapter import OK for USE_MCA=1`;
   - structured preflight artifacts and result;
   - SFT command/env/logs if SFT runs;
   - final artifact summary and stop/no-running-job proof.
2. Old blocker absence/presence:
   - old `LLAMAFACTORY_CLI` quoted single-path blocker absent;
   - old `model_name_or_path` parse/binding blocker absent if SFT reaches LLamaFactory;
   - previous CUDA/NCCL peer-memory/hardware blocker absent or recorded as exact blocker if it recurs;
   - old `KeyError: from`, ENOSPC, dataset map EOF, DEP_TARGET, mcore import, and forbidden-node placement blockers absent or exactly classified if present.
3. Success criteria:
   - complete checkpoint/model exists;
   - `trainer_state.json` exists;
   - `all_results.json` exists or PM-approved replacement exists;
   - eval remains blocked unless PM separately authorizes handoff.
4. Failure criteria:
   - if no complete checkpoint/model exists, evidence must record exact blocker, command/log signature, artifact state, old blocker status, stop proof, and next acceptance criteria.
5. Stop proof:
   - final LTP state stopped/completed or equivalent release proof;
   - endpoint refused after stop or equivalent proof;
   - running `coding-agent-playground` jobs list returns no active jobs.

## Current Blockers

```text
BLOCKED_WAITING_FINAL_DEV2_ALTNODE_RUNTIME_EVIDENCE:
- no allocation/node placement result yet
- no transfer/post-transfer verification yet
- no structured preflight result yet
- no SFT result yet
- no checkpoint/model/trainer_state/all_results assessment yet
- no stop/no-running-job proof yet
```

## Completion Marker

```yaml
task_id: M1-S23-PR63-ALTNODE-GATE-TEST1
owner: intern_code_test_1
result: WAITING_FINAL_ALTNODE_RUNTIME_EVIDENCE
current_dev2_status: LOCAL_PACKAGE_READY_PRE_SUBMIT
authorization_present: true
local_package_ready: true
runtime_final_evidence_present: false
checkpoint_model_present: pending
trainer_state_json_present: pending
all_results_json_present: pending
eval_handoff: BLOCKED_NO_FINAL_RUNTIME
stop_proof_complete: pending
no_ltp_gpu_preflight_sft_eval_remote_by_test1: true
```
