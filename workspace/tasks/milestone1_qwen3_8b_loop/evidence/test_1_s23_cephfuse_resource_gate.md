# Test 1 S23 Ceph-Fuse Resource Gate

Task ID: `M1-S23-CEPHFUSE-RESOURCE-GATE-TEST1`
Gate owner: `intern_code_test_1`
Resource owner: `intern_code_dev_2`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_cephfuse_resource_gate.md`
Status timestamp: `2026-05-21T13:16:53Z`

## Result

`PASS_FOR_PM_RETRY`

No LTP, GPU, preflight, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

This is a no-execution gate pass only. It does not authorize runtime by itself. A future retry still requires fresh PM authorization naming owner, run scope, and exactly one fresh allocation/run.

## Inputs Reviewed

PM durable branch commit:

- `88e0482` - `Publish S23 cephfuse fix package evidence`

PM durable evidence files reviewed:

- `evidence/dev_2_s23_cephfuse_resource_fix.md`
- `evidence/gpu_s23_cephfuse_resource_plan.md`
- `evidence/dev_3_s23_cephfuse_data_transfer_staging.md`
- `evidence/test_2_s23_cephfuse_eval_blocked.md`

PR #51 / dev_4 package reviewed:

- PR: `https://github.com/peteryang1/coding_agent_playground/pull/51`
- Latest head reviewed: `972c91f7da4aa5b89877023fcff3b6c1d0b9fe9b`
- Prior package commit in PR: `326b769acb33cfa53de184e640196353c1d00a07`
- State: open
- Draft: false
- Mergeability: `MERGEABLE` / `CLEAN`
- Evidence file: `evidence/dev_4_s23_cephfuse_launch_package.md`

## Failed Runtime Basis

Reviewed prior runtime facts from durable evidence:

- Frame: `xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z`
- Job: `coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z`
- Node: `lg-cmc-b7r202-q04u06-h200-000725`
- Endpoint: `ssh -p 36822 root@10.100.22.31`
- Final state: `FAILED (Completed)`
- Exit code: `220 Failed`
- Origin user exit code: `127`
- Exact blocker: `/usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found`
- Failure point: storage bootstrap before usable source transfer, `/home/xu.yang` proof, parser preflight, or SFT.
- No checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or model id exists.
- Endpoint proof after terminal state: connection refused.
- Running-job proof in dev_2 evidence: no `coding-agent-playground` jobs found.

## Gate Checks

### `/home/xu.yang` Storage Proof Plan

PASS.

Reviewed evidence requires the next runtime to prove:

- `ceph-fuse` binary exists before it is invoked.
- `/mnt/cephfs` mounts as `fuse.ceph-fuse`.
- `/home/xu.yang` resolves to the CephFS-backed home path.
- `/home/xu.yang/coding_agent_playground/outputs` exists and is writable.
- Real-write capacity probe runs under `/home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>` before parser preflight/SFT.
- Future generated SFT outputs, logs, configs, manifests, temporary converted datasets, checkpoints, run metadata, and intermediates stay under `/home/xu.yang/coding_agent_playground/outputs`.

dev_2/dev_4 use the corrected required path `/home/xu.yang`. If PM text says `/home.xu.yang`, test_1 treats that as a typo and gates against `/home/xu.yang`.

### Storage Bootstrap / Image Fix

PASS.

dev_2 provides a concrete storage bootstrap plan:

- Install/prove `ceph-common` and `ceph-fuse` before mount.
- Run `command -v ceph-fuse` and optional `ceph-fuse --version`.
- Mount `/mnt/cephfs` with the `xu.yang` keyring and accepted monitors.
- Verify `findmnt -n -o FSTYPE -T /mnt/cephfs` equals `fuse.ceph-fuse`.
- Create/link `/home/xu.yang` to `/mnt/cephfs/home/xu.yang` when needed.
- Verify `/home/xu.yang/coding_agent_playground/outputs` using `findmnt`, `df`, and real write probe before preflight.

dev_4 correctly keeps `ceph-fuse` out of the SFT launcher and treats CephFS mounting as resource/bootstrap responsibility before handoff. This avoids both known classes:

- `ceph-fuse: command not found`
- `fuse: unknown option(s): -o nonempty`

### No Remote Source / Dependency Downloads

PASS.

Reviewed evidence preserves the rule:

- No remote `git clone`.
- No remote `git fetch`.
- No remote GitHub source download.
- No remote project source/dependency fetch on the GPU/LTP node.
- No remote `pip install` / dependency download for project dependencies.

Allowed future operations are limited to:

- Infrastructure-only package/bootstrap commands for storage utilities, explicitly separated from project source/dependency retrieval.
- Local/provided-workspace source and data bundle preparation.
- Local checksum/file-list evidence.
- Transfer by tar-over-SSH, `scp`, or `rsync`.
- Remote checksum verification after transfer.

### Bundle Transfer / Checksum Evidence

PASS.

Reviewed evidence provides reusable baseline transfer/checksum facts:

- Source commit baseline: `2de4bab2248f052d09f118eb6c28c48231f3d719`
- Source bundle sha256: `13521a43bf64690b5cb3aefb8830316a799f2f079a35b17554379c99231988c8`
- File list count: `105`
- Dataset path: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`
- Dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`
- Dataset row count: `10`
- Dataset schema: `messages[*].from/value`
- Dataset info entry: `coding_agent_m1_sft_10_sharegpt`

dev_3 confirms no current data-side blocker and requires future transfer/post-transfer checksum verification into:

- `/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/train.jsonl`
- `/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/SHA256SUMS`
- `/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>/data`

If source files change before retry, the owning runtime evidence must regenerate and record new bundle/file/checksum evidence before transfer.

### Node / Job / Endpoint / Stop Proof

PASS.

dev_2 resource plan requires future runtime evidence for:

- Fresh allocation after PM authorization.
- Node id and preferably a different node from prior blocked nodes when scheduler allows.
- Endpoint host/port.
- Submit/status/wait evidence.
- Terminal stop state.
- Endpoint refused or equivalent unreachable proof after stop.
- No active held `coding-agent-playground` GPU job after completion/blocker.
- Artifact preservation under `/home/xu.yang/coding_agent_playground/outputs`.

The prior failed frame already has endpoint refusal and no-running-job proof recorded, which supports cleanup of the previous attempt.

### Conditional SFT Rule

PASS.

All reviewed evidence preserves the conditional rule:

- SFT must not run until storage proof passes.
- SFT must not run until structured parser-fixed preflight is `PASS`.
- SFT must not run unless `sft_allowed=true`.
- Capacity/topology/NVLink/NCCL all-reduce preflight must pass.
- Any current/fresh or timestamp-unknown Xid/SXid/ECC/NVLink/NCCL/SIGABRT/collective fault blocks SFT.
- If preflight is missing, malformed, WARN/FAIL, or `sft_allowed=false`, the correct behavior is to skip SFT, record the blocker, preserve artifacts, and stop/release the allocation.

### Eval Handoff

PASS for blocked-eval readiness; eval remains blocked.

test_2 evidence correctly states mini-swe eval is blocked because the failed runtime produced no accepted model form:

- No SFT ran.
- No checkpoint/model exists.
- No `trainer_state.json` exists.
- No `all_results.json` exists.
- No served endpoint or model id exists.

Future eval can proceed only after PM gates a complete checkpoint/model plus serving handoff or a reachable served endpoint, with generated eval artifacts under `/home/xu.yang`.

## Remaining Runtime Preconditions

No test_1 blocker remains for PM to authorize a retry. Before any actual retry, PM should still require:

- Explicit fresh PM runtime authorization naming dev_2 owner and exactly one fresh allocation/run.
- PR #51 or equivalent launch package accepted/merged if PM requires it before runtime.
- Runtime owner uses the reviewed no-remote-source/dependency transfer plan.
- Runtime owner records actual fresh endpoint, node, mount proof, capacity proof, transfer checksums, parser preflight result, SFT decision, checkpoint/model status, and stop proof.

## Decision

`PASS_FOR_PM_RETRY`

Reason: the previously missing dev_2 resource fix, GPU resource plan, dev_3 data transfer staging, and test_2 eval-blocked evidence are now present in durable commit `88e0482`; PR #51 latest head `972c91f7da4aa5b89877023fcff3b6c1d0b9fe9b` remains open/non-draft `MERGEABLE`/`CLEAN`; reviewed inputs satisfy the no-execution gate for `/home/xu.yang` proof plan, storage bootstrap/image fix, no remote source/dependency downloads, bundle transfer/checksum evidence, node/job/endpoint/stop proof, and SFT only after structured preflight PASS plus `sft_allowed=true`.

## Completion Marker

```yaml
task_id: M1-S23-CEPHFUSE-RESOURCE-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
pm_durable_commit_reviewed: 88e0482
pr_51_head_reviewed: 972c91f7da4aa5b89877023fcff3b6c1d0b9fe9b
dev2_resource_fix_gate: PASS
gpu_resource_plan_gate: PASS
dev3_data_transfer_gate: PASS
test2_eval_blocked_gate: PASS_EVAL_REMAINS_BLOCKED
dev4_launch_package_gate: PASS_SOURCE_EVIDENCE_ONLY
runtime_authorized_by_this_gate: false
fresh_pm_authorization_required: true
eval_handoff: BLOCKED_NO_MODEL
no_ltp_gpu_sft_eval_dry_run_by_test1: true
peer_send_pm_used: false
```
