# Dev 1 Review - M1-S23-PR57-MCORE-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-PR57-MCORE-REVIEW-DEV1`  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_pr57_mcore_review.md`  
Review timestamp: `2026-05-21T16:11:29Z`  
Result: `BLOCKER_MISSING_DEV4_MCORE_FIX_PACKAGE`

## Execution Boundary

- Dev_1 did not run LTP, GPU, preflight, SFT, eval, dry-run, transfer, or remote commands.
- Review used durable local PM evidence only.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- `evidence/dev_2_s23_pr57_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr57_preflight_sft_tracking.md`
- `evidence/dev_4_s23_pr57_launch_support.md`
- `evidence/test_1_s23_pr57_runtime_gate.md`

Missing required fix input:

- `evidence/dev_4_s23_pr57_mcore_fix.md`

## Runtime Evidence Review

Dev_2 PR57 final runtime evidence is sufficient to classify the new blocker:

- Authorized source commit: `b4ac31ef1e3772953108348bf099818326ed65cc`.
- Runtime frame: `xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z`.
- Endpoint/node: `ssh -p 22662 root@10.100.22.31`, `lg-cmc-b7r202-q04u06-h200-000725`.
- Remote GPU/LTP node was treated as no-external-network for project source/dependency staging.
- Local source bundle recorded 122 files with sha256 `1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa`.
- ShareGPT dataset had 10 rows with sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Transfer command was recorded as `scp` to `/root/workspace/`, with bundle, file list, critical checksums, transfer manifest, and dataset.
- Post-transfer verification recorded bundle sha256 OK, critical file checksums OK, remote file count 122, and dataset sha256 match.
- Dependency bundles were transferred and verified: `cap_pr55_pydeps_20260521T1505.tar.gz` and `LLamaFactory_4fa8e1ee_20260507.tar.gz`.
- `/home/xu.yang` storage proof passed: `/home/xu.yang` resolves to `/mnt/cephfs/home/xu.yang`, output root is `/home/xu.yang/coding_agent_playground/outputs`, and 24 GiB capacity probe passed and cleaned.
- Structured preflight passed:
  - `PREFLIGHT_RESULT=PASS`
  - `PREFLIGHT_STRUCTURED_STATUS=PASS`
  - `ACTIONABLE_FAULT=false`
  - `SFT_ALLOWED=true`
  - `TORCH_NCCL_ALLREDUCE_EXIT=0`
  - `CAPACITY_PROBE_STATUS=PASS`
  - `DIFFERENT_NODE_GATE=PASS`
  - `HOME_XU_YANG_STORAGE_STATUS=PASS`
  - `TOPOLOGY_CAPTURE_STATUS=PRESENT`
  - `NVLINK_CAPTURE_STATUS=PRESENT`
- Exactly one SFT attempt was run after preflight PASS and `SFT_ALLOWED=true`, matching PM authorization.
- SFT outputs/logs/config/manifest/final summary paths were under `/home/xu.yang/coding_agent_playground/outputs`.
- Eval was not run.

## Blocker Classification

Runtime result: `BLOCKED_PR57_RUNTIME_MISSING_MCORE_ADAPTER_STOPPED_NO_CHECKPOINT`

The SFT attempt failed before checkpoint/training output creation with:

```text
ImportError: mcore_adapter is required when USE_MCA=1. Please install `mcore_adapter` and its dependencies.
torch.distributed.elastic.multiprocessing.errors.ChildFailedError
/root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py FAILED
local_rank: 7 exitcode 1
```

Classification:

- This is a runtime dependency/environment blocker for the MCA path.
- It is distinct from prior blockers: no `DEP_TARGET: unbound variable`, missing dataset info, `KeyError: 'from'`, ENOSPC checkpoint save failure, `datasets.map(num_proc=4)` SyncManager EOF, parser false-positive preflight failure, NCCL/SXid health blocker, or ceph-fuse bootstrap blocker is shown as the active failure.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` was produced.

## Stop Proof

Stop proof is sufficient:

- Stop command was recorded for the PR57 LTP frame.
- Stop response was HTTP 202.
- Final state was `STOPPED (Completed)`.
- Endpoint refused connection after stop.
- `ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground` returned no jobs.
- Dev_2 records no active Milestone GPU is held after stop.

## Fix Gate

No `PASS_FOR_PM_RETRY` is possible yet because the required dev_4 fix package is absent:

- Missing: `evidence/dev_4_s23_pr57_mcore_fix.md`

The expected fix package must either:

- provide `mcore_adapter` and dependencies when `USE_MCA=1`, using local/provided workspace preparation and bundle transfer with checksums and no remote project/dependency downloads; or
- explicitly select a supported non-MCA path, with rationale and evidence that it does not weaken prior model/config/runtime acceptance criteria.

The fix package must preserve:

- PR57 wrapper/env contract;
- no-external-network staging rule for remote GPU/LTP nodes;
- `/home/xu.yang/coding_agent_playground/outputs` for generated outputs/logs/checkpoints/run metadata/intermediates;
- structured preflight before SFT;
- SFT only after `PREFLIGHT_RESULT=PASS` and `SFT_ALLOWED=true`;
- stop/no-active-job proof requirement for the future retry.

## Decision

`BLOCKER_MISSING_DEV4_MCORE_FIX_PACKAGE`

Dev_2 final runtime evidence cleanly identifies the active blocker as missing `mcore_adapter` while `USE_MCA=1`. Transfer, storage, preflight, conditional SFT, and stop proof are sufficient for classifying the runtime failure. PM should wait for `dev_4_s23_pr57_mcore_fix.md` and then request a refreshed dev_1/test_1 gate before authorizing any retry.
