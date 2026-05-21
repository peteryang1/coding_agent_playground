# PM S23 PR55 Preflight/SFT Runtime Authorization

Task ID: `M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Authorization time: `2026-05-21T14:52:00Z`

## Basis

- PR #55 merged at `2026-05-21T14:49:25Z`, merge commit `1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703`.
- PR #55 functional commit `6c959e89a75ce162076292ad6d6c317f421cd45f` fixed the split-artifact preflight success context for benign `NCCL_ASYNC_ERROR_HANDLING` warnings.
- dev_1 result: `PASS_FOR_PM_RETRY` in `evidence/dev_1_s23_pr53_preflight_blocker_review.md`.
- test_1 result: `PASS_FOR_PM_RETRY` in `evidence/test_1_s23_pr53_preflight_blocker_gate.md`.
- dev_2 final PR53 runtime proved the placement/storage/transfer/data path can pass on a non-forbidden node, but SFT was blocked by the parser false positive fixed by PR #55.
- dev_3 confirmed no data/package change is needed.
- test_2 confirmed eval remains blocked until a checkpoint/model or served endpoint exists.

## Authorized Scope

```text
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
task id: M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2
source commit to package locally: 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
forbidden nodes:
  - lg-cmc-b7r202-q03u26-h200-000730
  - lg-cmc-b7r202-p07u16-h200-000708
  - lg-cmc-b7r401-a04u26-h200-000769
  - lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
eval: not authorized
```

## Hard Gates

1. Prepare code/config/scripts/data locally/from provided workspace using PR #55 merge commit `1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703`.
2. Record exact source commit, file list, bundle checksum, parser/test/config checksums, and ShareGPT data checksum.
3. Do not use remote GitHub/source/dependency network on the GPU node.
4. Submit exactly one fresh LTP allocation.
5. Immediately verify node identity before source/data transfer.
6. If assigned node is forbidden, stop/release immediately and do not transfer, preflight, SFT, or eval.
7. If assigned node is non-forbidden:
   - prove `/home/xu.yang/coding_agent_playground/outputs` on CephFS and capacity;
   - transfer local bundle/data by `rsync`, `scp`, or tar-over-SSH;
   - verify bundle/data/file-list/critical checksums;
   - run structured preflight;
   - run SFT only if preflight is `PASS` and `sft_allowed=true`;
   - do not run eval.
8. Stop/release after checkpoint, failure, forbidden-node assignment, preflight failure, `sft_allowed=false`, SFT success/failure, idle/no-progress limit, or PM/test stop instruction.

## Required Evidence

- `evidence/dev_2_s23_pr55_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr55_preflight_sft_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`
- `task_registry.md`

Required durable outcome: SFT checkpoint/model with `trainer_state.json`/`all_results.json` and stop proof, or exact runtime blocker with command, logs, node status, output paths, stop proof, owner, and next fix.

## PM Boundary

PM did not run LTP, GPU, remote commands, transfer, preflight, SFT, eval, or dry-run. Execution is delegated to `intern_code_dev_2` only.
