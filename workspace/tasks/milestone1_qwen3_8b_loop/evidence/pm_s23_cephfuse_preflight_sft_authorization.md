# PM Authorization - S23 Ceph-Fuse Fixed Parser-Patch Preflight/SFT

Date: 2026-05-21
Owner: `intern_code_dev_2`
Task ID: `M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2`

## Gate Basis

- Prior parser-patch runtime `M1-S23-PARSERPATCH-PREFLIGHT-SFT-RUNTIME-DEV2` failed before transfer/preflight/SFT with `/usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found`, exit 220, state `FAILED (Completed)`.
- Dev_2 completed no-submit ceph-fuse resource fix plan:
  - `evidence/dev_2_s23_cephfuse_resource_fix.md`
  - `evidence/gpu_s23_cephfuse_resource_plan.md`
- Dev_4 completed no-execution launch package PR #51:
  - PR: `https://github.com/peteryang1/coding_agent_playground/pull/51`
  - mergedAt: `2026-05-21T13:23:23Z`
  - merge commit: `c02a53a344f2ad7a33b04f529d5125677237d4cb`
- Dev_3 completed data/transfer staging:
  - `evidence/dev_3_s23_cephfuse_data_transfer_staging.md`
- Test_2 refreshed eval-blocked readiness:
  - `evidence/test_2_s23_cephfuse_eval_blocked.md`
- Dev_1 refreshed review to `PASS_FOR_PM_RETRY` against PR #51 latest head `972c91f7da4aa5b89877023fcff3b6c1d0b9fe9b` and PM durable commit `88e0482`.
- Test_1 refreshed gate to `PASS_FOR_PM_RETRY` against PM durable commit `88e0482` and PR #51 latest head `972c91f7da4aa5b89877023fcff3b6c1d0b9fe9b`.
- PM gate commit: `50eada3` records the PR #51 gate pass.

## Authorization

PM authorizes only `intern_code_dev_2` to perform exactly one fresh owner-executed LTP/GPU runtime attempt:

1. Prepare exact local/provided-workspace source bundle for PR #51 merge commit `c02a53a344f2ad7a33b04f529d5125677237d4cb` or, if dev_2 proves the merge commit is not locally available yet, the exact PR #51 head `972c91f7da4aa5b89877023fcff3b6c1d0b9fe9b` with explicit provenance note.
2. Do not clone/fetch/download project source or dependencies on the remote GPU/LTP node.
3. Transfer code/config/scripts and accepted ShareGPT data from local/provided workspace to the remote endpoint using `rsync`, `scp`, or tar-over-SSH.
4. Record exact transfer command, source paths, destination paths, file list, bundle sha256, critical file checksums, dataset sha256, and post-transfer verification.
5. Use `/home/xu.yang/coding_agent_playground/outputs` for all generated outputs, logs, temporary converted/staged datasets, run metadata, preflight artifacts, checkpoints, and eval-related intermediates.
6. Prove storage before preflight/SFT:
   - `ceph-fuse` binary or image/spec proof;
   - `/mnt/cephfs` mounted as `fuse.ceph-fuse` or accepted equivalent;
   - `/home/xu.yang/coding_agent_playground/outputs` exists, resolves to accepted home/CephFS root, is writable, and passes a real-write capacity probe.
7. Run parser/NCCL/storage preflight.
8. Run SFT only if structured preflight is `PASS` and `sft_allowed=true`.
9. Stop/release the allocation after checkpoint/model success, exact blocker, preflight fail, SFT fail, idle/no-progress condition, or PM/test stop instruction.

## Explicit Non-Authorization

- No other owner may submit LTP/GPU for this runtime.
- No eval is authorized.
- No second same-node or retry attempt is authorized by this file.
- This file does not authorize remote GitHub/source/dependency network access.
- If storage bootstrap, transfer/checksum, preflight, or SFT fails, dev_2 must stop/release and write exact blocker evidence rather than retrying.

## Required Durable Evidence

Dev_2 must update:

- `evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md`
- `evidence/gpu_s23_cephfuse_preflight_sft_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`
- `task_registry.md`

Required result:

- Complete checkpoint/model with `trainer_state.json` and `all_results.json`, plus stop proof; or
- Fresh exact blocker with logs, owner, command, node/job/endpoint status, no-running-job proof, and next fix recommendation.

PM did not run LTP, GPU, remote commands, preflight, SFT, eval, or dry-run.
