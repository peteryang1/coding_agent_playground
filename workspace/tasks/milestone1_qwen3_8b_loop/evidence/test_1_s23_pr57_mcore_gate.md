# Test 1 S23 PR57 MCore Gate

Task ID: `M1-S23-PR57-MCORE-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Fix owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_pr57_mcore_gate.md`
Status timestamp: `2026-05-21T16:11:26Z`

## Result

`BLOCKED_MISSING_DEV4_MCORE_FIX_PACKAGE`

No LTP, GPU, preflight, SFT, eval, dry-run, transfer command, remote command, or parser execution was run by `intern_code_test_1`.

The PR57 runtime reached a new blocker after the prior PR57 wrapper fix: `mcore_adapter` is required when `USE_MCA=1`. A future retry is not gateable until dev_4 provides a no-execution fix package or PR and PM/dev_1/test_1 gate it.

## Inputs Reviewed

- `evidence/pm_s23_pr57_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr57_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr57_preflight_sft_tracking.md`
- `evidence/dev_4_s23_pr57_launch_support.md`
- `evidence/dev_1_s23_pr57_runtime_review.md`
- `evidence/test_2_s23_pr57_eval_ready.md`

Missing fix input:

- no concrete dev_4 mcore fix package or PR evidence was present in the PM durable evidence path at this check.

## Runtime Gate Findings

### Authorization / No-Execution Boundary

PASS for reviewed runtime scope.

PM authorized exactly one dev_2 runtime using:

```text
task: M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2
source commit: b4ac31ef1e3772953108348bf099818326ed65cc
PR57 merge commit: c450429c2e3369adc723d132396399cd17dba684
PR58 completion merge commit: b4ac31ef1e3772953108348bf099818326ed65cc
eval authorized: false
```

test_1 did not run any runtime command.

### Transfer / No-External-Network Proof

PASS for current evidence.

dev_2 records local/provided-workspace preparation and no remote project code/dependency staging network use:

```text
source repository: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc
commit: b4ac31ef1e3772953108348bf099818326ed65cc
worktree status: clean
file list count: 122
bundle sha256: 1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Transfer command was recorded as `scp -P 22662 ... root@10.100.22.31:/root/workspace/`, with post-transfer bundle checksum, critical-file checksums, file count, and dataset checksum verified.

dev_2 records no remote `git clone`, `git fetch`, GitHub/source fetch, or project/dependency download for project code/dependency staging on the GPU node.

### Storage / Artifacts

PASS.

Generated runtime artifacts are under `/home/xu.yang/coding_agent_playground/outputs`:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr57_preflight_sft_20260521T155200Z
train run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
checkpoint/output dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_stdout_stderr.log
xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_xtrace.log
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/run_manifest.json
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/config/qwen3_8b_sft.yaml
final summary: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/final_artifact_summary.txt
```

Storage proof:

```text
/mnt/cephfs mount: fuse.ceph-fuse
/home/xu.yang: /mnt/cephfs/home/xu.yang
capacity probe: PASS_AND_CLEANED, 25769803776 bytes written and removed
```

### Preflight / SFT Conditional Rule

PASS.

Durable preflight result:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
SFT_ALLOWED_IF_PM_AUTHORIZED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
torch all-reduce: ALLREDUCE_OK
```

SFT was run exactly once after preflight PASS and `SFT_ALLOWED=true`, matching PM authorization.

### SFT Runtime Blocker

BLOCKED.

SFT config evidence:

```text
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
preprocessing_num_workers: null
dataloader_num_workers: 0
max_steps: 2
save_steps: 2
save_total_limit: 1
tensor_model_parallel_size: 8
```

Final failure:

```text
EXIT_STATUS=1
END_UTC=2026-05-21T16:03:28Z
ImportError: mcore_adapter is required when USE_MCA=1. Please install `mcore_adapter` and its dependencies.
torch.distributed.elastic.multiprocessing.errors.ChildFailedError
/root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py FAILED
local_rank: 7 exitcode 1
```

The launcher initialized 8 distributed tasks before the import failure, then exited before training/checkpoint creation.

Gate classification:

`BLOCKED_PR57_RUNTIME_MISSING_MCORE_ADAPTER_USE_MCA`

### Checkpoint / Model / Eval

PASS for expected absence under the runtime blocker; eval handoff remains blocked.

Reviewed current state:

```text
checkpoint files: none
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
served endpoint/model id: absent
eval: not authorized and not run
```

No checkpoint/model/eval artifact exists for mini-swe.

### Stop / No-Running-Job Proof

PASS.

dev_2 records:

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
endpoint: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
post-stop state: STOPPED (Completed)
completed: 2026-05-21 16:06:06
endpoint proof: ssh refused connection after stop
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

## dev_4 Fix Package Gate

BLOCKED.

Current dev_4 evidence `dev_4_s23_pr57_launch_support.md` is standby/support evidence written before the concrete PR57 mcore blocker. It records PR57/PR58 landed state and no-execution boundary, but it does not provide a fix for:

```text
ImportError: mcore_adapter is required when USE_MCA=1
USE_MCA=1 runtime path
```

Required dev_4 fix package must cover one PM-approved path:

1. Provide `mcore_adapter` and required dependencies through local/provided workspace packaging and transfer only, with checksums and no remote project/dependency downloads on the GPU node.
2. Or explicitly disable/select away from MCA with a supported config/env path, explaining why non-MCA is valid for this milestone smoke and preserving tensor-parallel/training acceptance.
3. Preserve PR57 wrapper contract for `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, manifest/log/xtrace/diagnostics, and `/home/xu.yang/coding_agent_playground/outputs`.
4. Include static/source checks or precise no-execution review evidence.
5. State no LTP/GPU/preflight/SFT/eval was run by dev_4.

## Future Retry Acceptance Criteria

Before PM can authorize another runtime:

1. dev_4 mcore/USE_MCA fix package or PR exists.
2. dev_1/test_1 gates the fix as `PASS_FOR_PM_RETRY`.
3. dev_2 records no active prior job and fresh PM authorization names owner, commit/package, allocation count, and scope.
4. Source/config/scripts/data/dependency bundles are prepared locally/provided workspace, checksummed, transferred by `scp`, `rsync`, or tar-over-SSH, and post-transfer verified.
5. Remote GPU/LTP node does not run project source/dependency clone/fetch/download.
6. `/home/xu.yang/coding_agent_playground/outputs` remains the generated-artifact root.
7. Structured preflight must be `PASS` with `SFT_ALLOWED=true` before SFT.
8. SFT logs must show the mcore blocker absent and no regression to prior blockers.
9. Eval handoff requires complete checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM-approved replacements, plus stop proof.

## Completion Marker

```yaml
task_id: M1-S23-PR57-MCORE-GATE-TEST1
owner: intern_code_test_1
result: BLOCKED_MISSING_DEV4_MCORE_FIX_PACKAGE
runtime_blocker: BLOCKED_PR57_RUNTIME_MISSING_MCORE_ADAPTER_USE_MCA
preflight_pass_durable: true
sft_attempt_authorized_and_conditionally_valid: true
checkpoint_model_present: false
trainer_state_json_present: false
all_results_json_present: false
eval_handoff: BLOCKED_NO_MODEL
stop_proof_complete: true
dev4_fix_package_present: false
no_ltp_gpu_preflight_sft_eval_by_test1: true
```
