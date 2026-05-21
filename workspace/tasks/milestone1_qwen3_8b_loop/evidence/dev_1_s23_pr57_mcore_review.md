# Dev 1 Review - M1-S23-PR57-MCORE-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-PR57-MCORE-REVIEW-DEV1`  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_pr57_mcore_review.md`  
Review timestamp: `2026-05-21T16:21:19Z`  
Result: `PASS_FOR_PM_RETRY`

## Execution Boundary

- Dev_1 did not run LTP, GPU, preflight, SFT, eval, dry-run, transfer, or remote commands.
- Dev_1 reviewed durable PM evidence and PR #59 code statically.
- Local static checks run by dev_1 were shell syntax, Python compile, and pytest for static wrapper tests only.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- `evidence/dev_2_s23_pr57_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr57_preflight_sft_tracking.md`
- `evidence/dev_4_s23_pr57_mcore_fix.md`
- `evidence/dev_4_s23_pr57_launch_support.md`
- `evidence/test_1_s23_pr57_runtime_gate.md`
- PR #59 head named by PM: `92e437cf690b68121b9ad9d2f76b18a60a10a2d6`

## Runtime Evidence Review

Dev_2 PR57 final runtime evidence remains sufficient to classify the active blocker:

- Authorized source commit: `b4ac31ef1e3772953108348bf099818326ed65cc`.
- Runtime frame: `xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z`.
- Endpoint/node: `ssh -p 22662 root@10.100.22.31`, `lg-cmc-b7r202-q04u06-h200-000725`.
- Remote GPU/LTP node was treated as no-external-network for project source/dependency staging.
- Local source bundle recorded 122 files with sha256 `1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa`.
- ShareGPT dataset had 10 rows with sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Transfer command was recorded as `scp` to `/root/workspace/`, with bundle, file list, critical checksums, transfer manifest, and dataset.
- Post-transfer verification recorded bundle sha256 OK, critical file checksums OK, remote file count 122, and dataset sha256 match.
- Dependency bundles transferred for PR57 were verified, but did not include a usable `mcore_adapter` path for `USE_MCA=1`.
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

Failure signature:

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
- Eval remains blocked until a future retry produces an accepted model/checkpoint or endpoint.

## Stop Proof

Stop proof is sufficient:

- Stop command was recorded for the PR57 LTP frame.
- Stop response was HTTP 202.
- Final state was `STOPPED (Completed)`.
- Endpoint refused connection after stop.
- `ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground` returned no jobs.
- Dev_2 records no active Milestone GPU is held after stop.

## PR #59 / Dev_4 Fix Review

PR #59 head reviewed: `92e437cf690b68121b9ad9d2f76b18a60a10a2d6`  
PM-reported state: open, non-draft, `MERGEABLE` / `CLEAN`

PR #59 changed files at the reviewed head include the expected functional files:

- `scripts/train_qwen3_8b_sft.sh`
- `scripts/write_sft_run_manifest.py`
- `tests/test_train_qwen3_8b_sft_static.py`

The remaining changed files are task/status/evidence/history documentation for the PR57 launch support and mcore fix tasks.

Dev_4 fix package and PR #59 are acceptable for PM retry gate:

- Cites dev_2 PR57 runtime failure and correctly diagnoses the MCA path: `USE_MCA=1` requires `mcore_adapter` importability before training can proceed.
- Keeps the MCA path as the primary path and does not silently switch to non-MCA.
- Explicitly states non-MCA fallback is not selected and would need separate PM/dev_1/test_1 approval.
- Adds `MCORE_ADAPTER_DIR`, defaulting to `${REPO_ROOT}/code/mcore_adapter`.
- Exports `MCORE_ADAPTER_DIR` with the wrapper environment contract.
- Prepends `${MCORE_ADAPTER_DIR}` to `PYTHONPATH_PREFIX` when that directory exists, while preserving LLamaFactory `src` in the prefix.
- Records `MCORE_ADAPTER_DIR` and `PYTHONPATH_PREFIX` in the manifest environment/preflight fields.
- Adds a `USE_MCA=1` import gate before LLamaFactory train invocation.
- If `mcore_adapter` is not importable, exits early with explicit instruction to use a local/provided dependency bundle and not remote GitHub/fetch/download dependency staging on GPU/LTP nodes.
- Preserves PR57 wrapper/env contract for `DEP_TARGET`, `LF`, and `LLAMAFACTORY_CLI`.
- Preserves `/home/xu.yang/coding_agent_playground/outputs` output-root behavior.
- Provides future runtime bundle requirements: local/provided `mcore_adapter` provenance, file list, bundle sha256, transfer command, destination, remote sha256 verification, `MCORE_ADAPTER_DIR`, and Python import check result.

## Dev_1 Static Checks

Commands run locally in dev_4 worktree:

```bash
bash -n scripts/train_qwen3_8b_sft.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/write_sft_run_manifest.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Results:

```text
bash -n scripts/train_qwen3_8b_sft.sh: exit 0
python3 -m py_compile scripts/write_sft_run_manifest.py: exit 0
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 3 passed in 0.01s
```

## Remaining Retry Conditions

`PASS_FOR_PM_RETRY` here means the PR #59 mcore fix is acceptable for PM retry gating. It does not mean eval handoff or checkpoint readiness.

Before any new runtime, the runtime owner evidence should still record:

- PR #59 merged/completion-marked source commit selected by PM.
- Local/provided `mcore_adapter` dependency source provenance.
- `mcore_adapter` file list and bundle checksum.
- Exact transfer command, destination, and post-transfer checksum verification.
- `MCORE_ADAPTER_DIR` used by the SFT wrapper.
- Python import check result for `mcore_adapter`.
- `/home/xu.yang/coding_agent_playground/outputs` paths for generated outputs/logs/checkpoints/run metadata/intermediates.
- Structured preflight PASS and `SFT_ALLOWED=true` before SFT.
- SFT result, checkpoint/model or exact blocker, and stop/no-running-job proof.

## Decision

`PASS_FOR_PM_RETRY`

PR #59 fixes the reviewed mcore blocker at the wrapper/launch gate level without weakening prior transfer, storage, preflight, SFT, or stop-proof gates. The next retry still requires PM authorization and runtime evidence that the local/provided `mcore_adapter` bundle was transferred and verified without remote project/dependency downloads on the GPU/LTP node.
