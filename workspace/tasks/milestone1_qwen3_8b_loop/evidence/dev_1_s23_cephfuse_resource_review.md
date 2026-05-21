# Dev 1 Resource Review - M1-S23-CEPHFUSE-RESOURCE-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-CEPHFUSE-RESOURCE-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_cephfuse_resource_review.md`  
Execution boundary: no LTP, GPU, SFT, eval, remote experiment, or dry-run by `intern_code_dev_1`.

## Result

`PASS_FOR_PM_RETRY`

I reviewed the current ceph-fuse/storage-bootstrap fix inputs and found no dev_1 blocker for PM retry gate. Runtime remains separately PM-authorized; this review does not authorize LTP/GPU/preflight/SFT/eval/dry-run.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_cephfuse_resource_fix.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_cephfuse_resource_plan.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_cephfuse_launch_package.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_3_s23_cephfuse_data_transfer_staging.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_parserpatch_preflight_sft_runtime.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_parserpatch_preflight_sft_tracking.md`
- PR #51 head `326b769acb33cfa53de184e640196353c1d00a07`, open/non-draft `MERGEABLE` / `CLEAN` per PM request.

## Failed Runtime Facts

The prior parser-patch runtime failed before transfer/preflight/SFT:

- Frame: `xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z`.
- Node: `lg-cmc-b7r202-q04u06-h200-000725`.
- Endpoint: `ssh -p 36822 root@10.100.22.31`.
- Final state: `FAILED (Completed)`.
- Exit code: `220`; origin user exit code `127`.
- Exact log: `/usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found`.
- No source/dataset transfer, parser preflight, SFT, eval, checkpoint/model, `trainer_state.json`, or `all_results.json` occurred.
- dev_2 no-running-job proof says `No jobs found` for RUNNING `coding-agent-playground` jobs at `2026-05-21T13:05:27Z`.

## No-Remote-Network Rule

Status: PASS.

dev_2 and dev_4 both preserve the Session 23 rule that GPU/LTP nodes must not fetch project source or dependencies from remote networks:

- no remote git clone/fetch;
- no remote GitHub download/fetch;
- no remote pip install/download for project source/dependencies;
- no external source/dependency fetch on the GPU/LTP node.

The proposed `apt update` / `apt install ceph-common ceph-fuse rsync openssh-client tmux screen` is scoped as infrastructure/OS bootstrap from the internal cluster/local mirror before any project source transfer. That is acceptable for this resource fix review because it is not project source, GitHub content, Python package dependency download, or training-code fetch. If PM/test wants stricter runtime evidence, dev_2 should record the package source/mirror used in the future runtime.

## `/home/xu.yang` Proof Plan

Status: PASS.

dev_2 plan requires the next spec/image to prove `ceph-fuse` before invoking it:

- install or otherwise provide `ceph-common` and `ceph-fuse`;
- run `command -v ceph-fuse`;
- mount `/mnt/cephfs` using `ceph-fuse`;
- require `findmnt` to report `fuse.ceph-fuse`;
- create/prove `/home/xu.yang/coding_agent_playground/outputs`;
- run `findmnt`, `df`, path proof, and a real write/delete capacity probe under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>`.

dev_4 launch package keeps CephFS mounting as resource/bootstrap responsibility and requires the launcher to block before SFT if `/home/xu.yang/coding_agent_playground/outputs` is missing, unwritable, not capacity-verified, or resolves outside accepted `/home` / CephFS paths.

## Local Bundle / Checksum Transfer

Status: PASS.

The plan reuses the exact parser-patch source commit and bundle contract from the failed runtime:

- source commit: `2de4bab2248f052d09f118eb6c28c48231f3d719`;
- source bundle sha256: `13521a43bf64690b5cb3aefb8830316a799f2f079a35b17554379c99231988c8`;
- file list count: `105`;
- dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.

Accepted future transfer methods are local/provided-workspace-only:

- tar-over-SSH;
- `scp`;
- `rsync`.

Required evidence includes exact transfer commands, source/destination paths, endpoint, source commit, file list, bundle sha256, critical-file sha256s, dataset sha256, post-transfer verification, and statement that no remote git/pip/GitHub/download source/dependency fetch occurred.

dev_3 confirms the accepted ShareGPT dataset remains data-ready, with future transferred/staged/copy/checksum/provenance artifacts under `/home/xu.yang/coding_agent_playground/outputs` unless explicitly justified.

## Stop Conditions

Status: PASS.

dev_2 plan includes stop/release conditions for:

- missing `ceph-fuse` after bootstrap;
- failed `/mnt/cephfs` mount;
- failed `/home/xu.yang/coding_agent_playground/outputs` proof;
- failed capacity probe or cleanup;
- failed source/dataset transfer or checksum verification;
- any need for remote git/fetch/pip/download/GitHub;
- malformed or non-PASS parser preflight;
- `sft_allowed` not true;
- fresh/current or timestamp-unknown Xid/SXid/ECC/NVLink/NCCL fault;
- torch NCCL all-reduce fail/hang;
- conditional SFT fail/success terminal conditions;
- node unhealthy/idle without progress;
- PM/test stop instruction;
- bounded runtime expiry.

Required stop proof includes LTP stop/action, UTC timestamp, terminal state, endpoint refusal or equivalent unreachable proof, and artifact preservation note under `/home/xu.yang/coding_agent_playground/outputs`.

## PR #51 Review

Status: PASS for PM owner-self-merge gate.

PR #51 head `326b769acb33cfa53de184e640196353c1d00a07` is open/non-draft `MERGEABLE` / `CLEAN` per PM request.

Diff review:

- Adds `evidence/dev_4_s23_cephfuse_launch_package.md`.
- Updates dev_4 status and milestone durable docs (`history_log.md`, `task_knowledge.md`, `task_registry.md`).
- Does not modify parser code, training launcher code, model config, or runtime scripts.
- dev_4 evidence states no LTP/GPU/preflight/SFT/eval was run.
- Package is a no-execution launch/spec package and explicitly keeps runtime separately gated.

From dev_1's perspective, PR #51 is safe for PM owner-self-merge gate as a durable spec/evidence package. It does not authorize a runtime.

## Remaining Conditions For Future Runtime

PM should still require fresh runtime authorization naming owner and exact attempt count. Before SFT can run, the future runtime must produce:

- fresh endpoint/nodes.json;
- `ceph-fuse` binary proof or image proof;
- `/mnt/cephfs` mounted as `fuse.ceph-fuse`;
- `/home/xu.yang/coding_agent_playground/outputs` mount/path/write/capacity proof;
- local bundle transfer and remote checksum verification for commit `2de4bab2248f052d09f118eb6c28c48231f3d719` or a PM-named replacement commit;
- no remote source/dependency network proof;
- parser preflight PASS and `sft_allowed=true`;
- stop proof after completion/blocker.

## Completion Marker

```yaml
task_id: M1-S23-CEPHFUSE-RESOURCE-REVIEW-DEV1
owner: intern_code_dev_1
result: PASS_FOR_PM_RETRY
pass_for_pm_retry: true
exact_blockers: []
dev2_plan_reviewed: true
gpu_resource_plan_reviewed: true
dev4_pr51_reviewed: true
dev3_data_transfer_reviewed: true
pr51_head: 326b769acb33cfa53de184e640196353c1d00a07
pr51_safe_for_pm_owner_self_merge_gate: true
no_remote_network_rule_reviewed: true
home_xu_yang_proof_plan_reviewed: true
local_bundle_checksum_transfer_reviewed: true
stop_conditions_reviewed: true
required_source_commit_for_future_retry: 2de4bab2248f052d09f118eb6c28c48231f3d719
no_ltp_gpu_sft_eval_remote_experiment_dry_run_by_dev1: true
```
