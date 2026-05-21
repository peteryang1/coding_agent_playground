# Test 1 S23 SXid Different-Node Standby Gate

Task ID: `M1-S23-SXID-DIFFERENTNODE-RUNTIME-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Parser hygiene owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_sxid_standby_gate.md`
Status timestamp: `2026-05-21T14:02:28Z`

## Result

`STANDBY_WAITING_DEV4_PR_OR_DEV2_RUNTIME_EVIDENCE`

No LTP, GPU, preflight, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

## Assignment

PM assigned test_1 to watch two Session 23 paths:

- dev_4 parser hygiene task: `M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4`
- dev_2 fresh different-node runtime task: `M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`

Routine status/results are durable-only; no peer_send to PM.

## Current Input Availability

Present:

- `evidence/pm_s23_sxid_differentnode_preflight_sft_authorization.md`

Not present at this check:

- `evidence/dev_4_s23_nccl_warning_parser_hygiene.md`
- open dev_4 PR for `M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4`
- `evidence/dev_2_s23_sxid_differentnode_preflight_sft_runtime.md`
- `evidence/gpu_s23_sxid_differentnode_preflight_sft_tracking.md`

GitHub open PR check result:

```text
gh pr list --state open => []
```

## Authorization Basis

From PM authorization:

- Authorized owner: `intern_code_dev_2`
- Authorized allocation count: exactly `1`
- Required shape: fresh single-node `8 x H200`
- Runtime must avoid the flagged SXid node `lg-cmc-b7r202-q03u26-h200-000730`
- Runtime should avoid prior failed/blocked nodes if selectable:
  - `lg-cmc-b7r202-p07u16-h200-000708`
  - `lg-cmc-b7r401-a04u26-h200-000769`
  - `lg-cmc-b7r202-q04u06-h200-000725`
  - `lg-cmc-b7r202-q03u26-h200-000730`
- Eval is not authorized.
- SFT may run only after structured preflight `PASS` and `sft_allowed=true`.

PM classification from authorization:

```text
primary blocker: real_or_unknown_time_sxid_nvlink_node_health
exact blocker: SXid 20009 / NVLink RX Short Error Rate on node lg-cmc-b7r202-q03u26-h200-000730
secondary parser noise: NCCL_ASYNC_ERROR_HANDLING deprecation warnings classified as nccl_or_collective_failure despite TORCHRUN_EXIT=0 and ALLREDUCE_OK
```

## dev_4 Parser Hygiene Gate Criteria

When dev_4 PR/evidence appears, test_1 will gate without LTP/GPU/SFT/eval/parser execution.

Required checks:

1. PR/evidence cites task `M1-S23-NCCL-WARNING-PARSER-HYGIENE-DEV4`.
2. Evidence path exists: `evidence/dev_4_s23_nccl_warning_parser_hygiene.md`.
3. Patch ensures benign `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings are not classified as collective failures when:
   - `TORCHRUN_EXIT=0`;
   - `ALLREDUCE_OK` is present.
4. Patch preserves detection for real failures:
   - NCCL/CUDA invalid peer memory;
   - unhandled system error;
   - true collective failure;
   - nonzero `torchrun` exit;
   - `SIGABRT`;
   - `ChildFailedError`;
   - Xid/SXid/ECC/NVLink faults.
5. Evidence includes synthetic tests or static test attempts.
6. Evidence states no LTP/GPU/preflight/SFT/eval was run by dev_4.
7. Any PR is open/non-draft and PM-gateable, with task id/owner/acceptance/evidence/completion marker cited.

Expected output when available:

- `PASS_FOR_PM_RETRY` if parser hygiene is narrow and preserves real-fault detection.
- Exact blocker if the patch suppresses real NCCL/GPU fault detection, lacks test evidence, lacks durable evidence, or expands outside task scope.

## dev_2 Runtime Gate Criteria

When dev_2 runtime evidence appears, test_1 will gate:

Required files:

- `evidence/dev_2_s23_sxid_differentnode_preflight_sft_runtime.md`
- `evidence/gpu_s23_sxid_differentnode_preflight_sft_tracking.md`

Required checks:

1. Authorization/ownership:
   - task id is `M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`;
   - owner is `intern_code_dev_2`;
   - exactly one fresh runtime attempt is recorded.
2. Node policy:
   - node differs from `lg-cmc-b7r202-q03u26-h200-000730`;
   - prior failed/blocked nodes are avoided if selectable, or any unavoidable assignment is explicitly justified and stopped before unsafe work.
3. Source/data transfer:
   - local/provided-workspace source commit, file list, bundle sha256, critical checksums, dataset sha256, and post-transfer verification are recorded;
   - no remote `git clone`, `git fetch`, GitHub/source/dependency download, or remote project dependency fetch is used.
4. `/home/xu.yang` storage:
   - CephFS mount/output proof exists;
   - generated outputs/logs/preflight artifacts/checkpoints/tmp/run metadata/intermediates use `/home/xu.yang/coding_agent_playground/outputs`;
   - real-write capacity probe passes and cleans.
5. Structured preflight:
   - required fields are present, including `PREFLIGHT_RESULT`, `SFT_ALLOWED`, `SFT_SKIP_REASON`, `TORCH_NCCL_ALLREDUCE_EXIT`, `CAPACITY_PROBE_STATUS`, `DIFFERENT_NODE_GATE`, `HOME_XU_YANG_STORAGE_STATUS`, `TOPOLOGY_CAPTURE_STATUS`, and `NVLINK_CAPTURE_STATUS`;
   - parser health findings are recorded with exact blocker or PASS.
6. SFT decision:
   - if preflight is `PASS` and `sft_allowed=true`, exactly one SFT smoke may run and must record command/env/config;
   - if preflight is not PASS or `sft_allowed=false`, SFT must be skipped and exact blocker recorded.
7. Checkpoint/eval:
   - checkpoint/model plus `trainer_state.json` and `all_results.json` are present if SFT succeeds;
   - otherwise absence is tied to exact blocker;
   - eval handoff remains blocked unless PM gates a model/served endpoint.
8. Stop proof:
   - terminal state is recorded;
   - endpoint refused or equivalent unreachable proof exists;
   - no running `coding-agent-playground` job remains.

Expected output when available:

- `PASS_FOR_EVAL_HANDOFF` only if checkpoint/model plus `trainer_state.json`/`all_results.json` or PM-approved replacement and serving/eval handoff criteria are met.
- `PASS_FOR_NEXT_PM_DECISION` if the runtime reached a complete non-eval decision with no test blocker but eval remains blocked.
- Exact blocker if source/data, `/home/xu.yang`, preflight, SFT, checkpoint, or stop proof fails.

## Completion Marker

```yaml
task_id: M1-S23-SXID-DIFFERENTNODE-RUNTIME-GATE-TEST1
owner: intern_code_test_1
result: STANDBY_WAITING_DEV4_PR_OR_DEV2_RUNTIME_EVIDENCE
dev4_parser_hygiene_input: missing
dev4_open_pr: absent
dev2_runtime_evidence: missing
dev2_gpu_tracking_evidence: missing
pm_authorization_present: true
no_ltp_gpu_sft_eval_dry_run_by_test1: true
peer_send_pm_used: false
```
