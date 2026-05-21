# Test 1 S23 Ceph-Fuse Resource Gate

Task ID: `M1-S23-CEPHFUSE-RESOURCE-GATE-TEST1`
Gate owner: `intern_code_test_1`
Resource owner: `intern_code_dev_2`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_cephfuse_resource_gate.md`
Status timestamp: `2026-05-21T13:11:49Z`

## Result

`BLOCKED_MISSING_REQUIRED_DURABLE_INPUTS`

No LTP, GPU, preflight, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

## Refresh Against PM-Named Inputs

PM requested refresh against:

- `evidence/dev_2_s23_cephfuse_resource_fix.md`
- `evidence/gpu_s23_cephfuse_resource_plan.md`
- `evidence/dev_4_s23_cephfuse_launch_package.md`
- `evidence/dev_3_s23_cephfuse_data_transfer_staging.md`
- `evidence/test_2_s23_cephfuse_eval_blocked.md`
- PR #51 head `326b769acb33cfa53de184e640196353c1d00a07`

Current availability check:

- Missing in PM worktree, `origin/main`, and fetched PR refs checked by test_1: `evidence/dev_2_s23_cephfuse_resource_fix.md`
- Missing in PM worktree, `origin/main`, and fetched PR refs checked by test_1: `evidence/gpu_s23_cephfuse_resource_plan.md`
- Missing in PM worktree, `origin/main`, and fetched PR refs checked by test_1: `evidence/dev_3_s23_cephfuse_data_transfer_staging.md`
- Missing in PM worktree, `origin/main`, and fetched PR refs checked by test_1: `evidence/test_2_s23_cephfuse_eval_blocked.md`
- Present in PR #51: `evidence/dev_4_s23_cephfuse_launch_package.md`

Exact blocker:

`BLOCKED_MISSING_REQUIRED_DURABLE_INPUTS`

The dev_4 PR #51 launch package is present and reviewable, but test_1 cannot output `PASS_FOR_PM_RETRY` until the PM-named dev_2 resource fix/plan, dev_3 data transfer staging, and test_2 eval-blocked inputs are durably available for review.

## PR #51 / dev_4 Launch Package Check

PR #51 metadata:

- PR: `https://github.com/peteryang1/coding_agent_playground/pull/51`
- Head reviewed: `326b769acb33cfa53de184e640196353c1d00a07`
- State: open
- Draft: false
- Mergeability: `MERGEABLE` / `CLEAN`
- Required checks: none reported

dev_4 launch package source/evidence review:

- PASS for no-execution boundary: dev_4 states no LTP/GPU/preflight/SFT/eval command was run.
- PASS for launch ownership boundary: dev_4 correctly states CephFS mounting is resource/bootstrap owner responsibility before handoff, not something the SFT launcher should invoke directly.
- PASS for avoiding known bootstrap failures: package says the training launcher should not invoke `ceph-fuse`, avoiding both `ceph-fuse: command not found` and prior `-o nonempty` failure classes.
- PASS for future output root: package keeps generated artifacts under `/home/xu.yang/coding_agent_playground/outputs`.
- PASS for no remote source/dependency network: package requires local checksum-recorded bundle transfer, no GitHub/source/dependency fetch on GPU node.
- PASS for future mount/output verification skeleton: package includes checks for `/home/xu.yang`, output writability, resolved root under `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs`, `findmnt`, `df`, and capacity probe policy.
- PASS for SFT launch boundary: package says runtime remains blocked until PM separately authorizes and resource/test gates provide mount proof, capacity proof, bundle checksum proof, and reviews.

This dev_4-only pass is insufficient for full resource gate pass because dev_2/dev_3/test_2 durable inputs are missing.

## Missing Required Inputs

Required dev_2 fix-plan inputs are not present yet:

- Missing: `evidence/dev_2_s23_cephfuse_resource_fix.md`
- Missing: `evidence/gpu_s23_cephfuse_resource_plan.md`
- Missing: `evidence/dev_3_s23_cephfuse_data_transfer_staging.md`
- Missing: `evidence/test_2_s23_cephfuse_eval_blocked.md`

Exact blocker:

`BLOCKED_MISSING_REQUIRED_DURABLE_INPUTS`

The gate is ready to re-check once those files exist.

## Basis From Failed Runtime

Reviewed existing durable runtime evidence:

- `evidence/dev_2_s23_parserpatch_preflight_sft_runtime.md`
- `evidence/gpu_s23_parserpatch_preflight_sft_tracking.md`

Facts recorded by dev_2:

- Failed runtime task: `M1-S23-PARSERPATCH-PREFLIGHT-SFT-RUNTIME-DEV2`.
- Frame: `xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z`.
- Node: `lg-cmc-b7r202-q04u06-h200-000725`.
- Endpoint: `ssh -p 36822 root@10.100.22.31`.
- State: `FAILED (Completed)`.
- Exit code: `220`.
- Exact log: `/usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found`.
- Failure point: LTP bootstrap before usable RUNNING endpoint.
- Root cause recorded by dev_2: LTP image/spec lacked `ceph-fuse`, so `/home/xu.yang` / CephFS output root could not be mounted or proved.
- No remote source transfer occurred.
- No remote git clone/fetch/download, pip install/download, GitHub fetch, or external source/dependency retrieval occurred.
- No preflight, SFT, eval, checkpoint/model, `trainer_state.json`, or `all_results.json` was produced.
- Stop/release proof: stop command returned HTTP 500 because the frame was already terminal, post-stop state remained `FAILED (Completed)`, endpoint refused, and no RUNNING `coding-agent-playground` jobs were found.

## Gate Requirements When dev_2 Plan Exists

### `/home/xu.yang` Mount / Proof

PASS requires dev_2's plan to prove the next runtime can establish:

- `/home/xu.yang` exists.
- `/home/xu.yang/coding_agent_playground/outputs` is writable.
- `/home/xu.yang` resolves to the accepted CephFS-backed home path, for example `/mnt/cephfs/home/xu.yang`.
- `findmnt` or equivalent mount proof records CephFS/fuse status where available.
- A real write/read/checksum/capacity probe under `/home/xu.yang/coding_agent_playground/outputs` is planned before preflight/SFT.

Exact blocker if missing:

- No proof path for `/home/xu.yang`.
- Plan depends on `/home/xu.yang` but does not prove mount/create/link behavior.
- Plan would run preflight/SFT before proving `/home/xu.yang`.

### Storage Bootstrap / Image Fix

PASS requires one concrete fix path:

- Use an LTP image/spec where `ceph-fuse` is already available, or
- Add an explicit infrastructure-only bootstrap that provides `ceph-fuse` before `/home/xu.yang` is used.

The plan must include:

- Exact image/spec/bootstrap delta.
- Exact commands or config snippets for the bootstrap path.
- Evidence that bootstrap commands are infrastructure/storage-only and not project source or Python dependency retrieval.
- Expected proof commands for `command -v ceph-fuse`, mount state, `/home/xu.yang` resolution, and write probe.

Exact blocker if missing:

- Plan says "fix image" or "install ceph-fuse" without exact image/spec/bootstrap command.
- Plan requires remote package/network access without identifying it as approved internal infrastructure-only access.
- Plan cannot distinguish storage bootstrap from source/dependency downloads.

### No Remote Source/Dependency Network

PASS requires the next attempt to keep the no-remote-network rule:

- No remote `git clone`.
- No remote `git fetch`.
- No remote GitHub source download.
- No remote `pip install` / dependency download.
- No external source/dependency fetch from the GPU/LTP node.

Allowed:

- Local/provided-workspace source bundle preparation.
- Local checksums and file list.
- Transfer by `tar` over SSH, `scp`, or `rsync`.
- Internal infrastructure-only storage/bootstrap commands when explicitly documented and not used for project source/dependency retrieval.

Exact blocker if missing:

- LTP spec or plan includes remote clone/fetch/pip/download of project source or dependencies.
- Plan does not say how source/dataset reaches the node without external network.

### Local Bundle Transfer / Checksums

PASS requires preserving the prior local bundle discipline:

- Exact source commit for the next attempt.
- Clean local/provided source worktree proof.
- File list with count.
- Source bundle path and sha256.
- Critical script/config checksums.
- Dataset path, row count, schema, and sha256.
- Exact transfer template to future endpoint.
- Post-transfer verification commands and expected checksums.

Recommended baseline from failed attempt:

- PR #49 merge commit: `2de4bab2248f052d09f118eb6c28c48231f3d719`.
- Prior source bundle sha256: `13521a43bf64690b5cb3aefb8830316a799f2f079a35b17554379c99231988c8`.
- Dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.

Exact blocker if missing:

- No checksum evidence.
- No file list.
- No transfer command template.
- No post-transfer verification plan.

### Node / Job / Endpoint / Stop Proof

PASS requires the plan to require future runtime evidence for:

- LTP frame/job id.
- Node id.
- Endpoint.
- Submit/wait/status commands.
- Terminal stop state.
- Endpoint refused or otherwise unreachable after stop.
- No active held `coding-agent-playground` GPU job after completion/blocker.

Exact blocker if missing:

- No stop criteria.
- No endpoint refusal proof requirement.
- No active-job cleanup check.

### Conditional SFT Rule

PASS requires SFT remains forbidden unless:

- Structured preflight result is `PASS`.
- `sft_allowed=true`.
- `/home/xu.yang/coding_agent_playground/outputs` storage proof passes.
- Capacity/topology/NVLink/NCCL all-reduce preflight evidence passes.
- No actionable current/fresh or timestamp-unknown Xid/SXid/ECC/NVLink/NCCL/SIGABRT/collective fault exists.

If preflight is missing, WARN, FAIL, malformed, or `sft_allowed=false`, the correct behavior is:

- Do not run SFT.
- Record exact blocker.
- Preserve available artifacts.
- Stop/release the allocation.

Eval handoff remains blocked until a later authorized SFT run produces checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM/test accepts explicit replacements.

## Decision Labels For Future Refresh

When dev_2 writes the plan, test_1 will output one of:

- `PASS_FOR_PM_RETRY`: dev_2 plan proves ceph-fuse/storage bootstrap path, no-remote-source/dependency network, local bundle transfer/checksum discipline, future node/job/endpoint/stop proof, and conditional SFT gate.
- Exact blocker: missing or unsafe plan element, unproven `/home/xu.yang`, remote source/dependency network dependency, missing transfer/checksum proof, missing stop proof requirement, or SFT rule regression.

## Completion Marker

```yaml
task_id: M1-S23-CEPHFUSE-RESOURCE-GATE-TEST1
owner: intern_code_test_1
result: BLOCKED_MISSING_REQUIRED_DURABLE_INPUTS
pr_51_head_reviewed: 326b769acb33cfa53de184e640196353c1d00a07
dev4_launch_package_gate: PASS_SOURCE_EVIDENCE_ONLY
missing_inputs:
  - evidence/dev_2_s23_cephfuse_resource_fix.md
  - evidence/gpu_s23_cephfuse_resource_plan.md
  - evidence/dev_3_s23_cephfuse_data_transfer_staging.md
  - evidence/test_2_s23_cephfuse_eval_blocked.md
required_future_result_options:
  - PASS_FOR_PM_RETRY
  - exact_blocker
no_ltp_gpu_sft_eval_dry_run_by_test1: true
peer_send_pm_used: false
```
