# PM S23 PR53 Placement-Probe Preflight/SFT Authorization

Task ID: `M1-S23-PR53-PLACEMENTPROBE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Authorization time: `2026-05-21T14:24:00Z`

## Basis

- PR #53 self-merged at `2026-05-21T14:20:56Z`, merge commit `e29c93736be3384663cad953cd18da68c30070fb`.
- dev_1 PR #53 review result: `PASS_FOR_PM_RETRY`.
- test_1 PR #53 gate result: `PASS_FOR_OWNER_SELF_MERGE_AFTER_PM_GATE`.
- dev_2 placement plan result: `BLOCKED_PLACEMENT_NOT_GUARANTEED_BY_CURRENT_LTP_TEMPLATE`; current local LTP client/spec has no verified node exclusion, pinning, or anti-affinity field.
- dev_1 same-node review result: `BLOCKER_MISSING_ENFORCEABLE_DIFFERENT_NODE_PLACEMENT_PLAN`.
- test_1 same-node gate result: `BLOCKED_FINAL_PLACEMENT_SAME_SXID_NODE_STOPPED_NO_PREFLIGHT_NO_SFT`, with stop-before-transfer/preflight/SFT/eval behavior correct.

## PM Decision

Because no enforceable LTP node-exclusion mechanism is currently proven and the milestone must keep moving, PM authorizes exactly one bounded placement-probe runtime attempt by `intern_code_dev_2`.

This is an explicit PM waiver of the missing enforceable placement mechanism for one attempt only. It accepts the stop-and-release placement strategy under strict early node-gate limits.

## Authorized Scope

```text
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
task id: M1-S23-PR53-PLACEMENTPROBE-PREFLIGHT-SFT-RUNTIME-DEV2
source commit to package locally: e29c93736be3384663cad953cd18da68c30070fb
forbidden nodes:
  - lg-cmc-b7r202-q03u26-h200-000730
  - lg-cmc-b7r202-p07u16-h200-000708
  - lg-cmc-b7r401-a04u26-h200-000769
  - lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
eval: not authorized
```

## Hard Gates

1. Prepare the PR #53 merge commit package locally/from provided workspace first. Record exact commit, file list, bundle checksum, critical file checksums, and dataset checksum.
2. Do not use remote GitHub/source/dependency network on the GPU node.
3. Submit exactly one fresh LTP allocation.
4. Immediately verify node identity before source/data transfer.
5. If assigned node is in the forbidden list, stop/release immediately and do not transfer, preflight, SFT, or eval.
6. If assigned node is not in the forbidden list:
   - verify `/home/xu.yang/coding_agent_playground/outputs` and capacity;
   - transfer local/provided workspace source/data bundle by `rsync`, `scp`, or tar-over-SSH;
   - verify post-transfer checksums/file list;
   - run structured preflight;
   - run SFT only if preflight is `PASS` and `sft_allowed=true`;
   - do not run mini-swe eval.
7. Stop/release after checkpoint, failure, forbidden-node assignment, preflight failure, `sft_allowed=false`, SFT result, idle/no-progress limit, or PM/test stop instruction.

## Required Evidence

- `evidence/dev_2_s23_pr53_placementprobe_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr53_placementprobe_preflight_sft_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`
- `task_registry.md`

Evidence must include:

- LTP frame/job/node/endpoint and node identity;
- whether the assignment hit a forbidden node;
- exact stop proof and no-running-job proof if stopped early;
- local bundle/source commit/file list/checksums and dataset checksum;
- exact transfer command/checksum verification if transfer occurs;
- `/home/xu.yang` storage proof and capacity result if non-forbidden node;
- structured preflight output fields;
- SFT command/config/env only if SFT runs;
- checkpoint/model or exact runtime blocker;
- `trainer_state.json` and `all_results.json` presence/absence;
- final stop/release proof.

## PM Boundary

PM did not run LTP, GPU, remote commands, transfer, preflight, SFT, or eval. Execution is delegated to `intern_code_dev_2` only.
