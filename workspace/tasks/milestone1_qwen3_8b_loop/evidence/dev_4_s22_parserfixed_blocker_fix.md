# Dev 4 S22 Parser-Fixed Blocker Fix Package

Task ID: `M1-S22-PARSERFIXED-BLOCKER-FIX-DEV4`

Owner: `intern_code_dev_4`

Created: 2026-05-21

Scope: no-execution fix package and PR plan for the parser-fixed preflight blocker after PR #45.

Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_parserfixed_blocker_fix.md`

Completion marker: ready-for-review; no LTP/GPU/preflight/SFT/eval/dry-run/runtime command is authorized or run by this package.

## Inputs Reviewed

Primary runtime evidence:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_parserfixed_preflight_sft_tracking.md
```

Refreshed review/gate evidence:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s22_parserfixed_runtime_review.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_parserfixed_runtime_gate.md
```

Runtime facts:

```text
runtime task: M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2
PR #45 merge commit staged on GPU: 6f61489e85fcf7e129699061c9ddcb6e8db80926
frame: xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
endpoint while active: ssh -p 22662 root@10.100.22.14
node: lg-cmc-b7r202-p07u16-h200-000708
preflight run id: milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
preserved CephFS mirror: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
structured preflight status: FAIL_HEALTH_SIGNATURE
sft_allowed: false
conditional SFT: NOT_RUN
checkpoint/model/trainer_state/all_results: absent because SFT was not run
stop proof: STOPPED (Completed), endpoint refused
```

Checks that passed before the parser blocker:

```text
capacity probe: PASS_AND_CLEANED, 4 x 6GiB writes verified and removed
topology: nvidia-smi topo -m captured, NV18 between every GPU pair
NVLink: nvidia-smi nvlink --status captured links 0-17 at 26.562 GB/s per GPU
GPU query: 8 x NVIDIA H200 visible; ECC volatile/aggregate uncorrected counters 0 at query time
torch NCCL all-reduce: TORCHRUN_EXIT=0
different-node gate: PASS versus immediate failed parser preflight node
```

Structured blocker:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
ACTIONABLE_FAULT=true
SFT_ALLOWED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=actionable GPU/NCCL health signature found
```

Health-signature details:

```text
health_status.json recorded Xid matches in dmesg_gpu_fault_scan.txt.
dev_2 evidence names historical Xid 43 entries from 2026-04-17.
dev_2 evidence also names Xid 137 / SXid 12028 entries from 2026-05-21 18:18:48 local node time.
```

dev_1/test_1 refreshed conclusion:

```text
dev_1 result: PASS_FOR_PM_NEXT_DECISION
test_1 result: PASS_FOR_NEXT_PM_DECISION
eval handoff: blocked because SFT was skipped and no checkpoint/model exists
recommended next area: preflight health/storage blocker, not SFT training failure
```

## Diagnosis

The runtime correctly obeyed the conditional SFT contract. The current blocker is not LLamaFactory training, data, checkpointing, NCCL collective failure, or capacity. It is a preflight parser classification issue with two parts:

1. Xid/SXid classification is too coarse. PR #45 correctly preserved real Xid detection, but the current runtime shows the parser needs a freshness policy so clearly stale/historical Xid lines do not block SFT while fresh or timestamp-unknown Xid/SXid lines still block.
2. Storage status is a path normalization bug. The artifacts were written through `/home/xu.yang/coding_agent_playground/outputs/...` and preserved under the CephFS mirror, but the parser likely resolved the symlink to `/mnt/cephfs/home/xu.yang/...` and then compared only against the literal `/home/xu.yang/coding_agent_playground/outputs` root.

## Proposed PR Scope

Exact files to modify:

```text
scripts/parse_s22_preflight_health.py
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_parserfixed_blocker_fix.md
workspace/interns/intern_code_dev_4/status.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md
```

Optional task-local docs if PM wants per-task durable docs:

```text
workspace/tasks/milestone1_qwen3_8b_loop/M1-S22-PARSERFIXED-BLOCKER-FIX-DEV4/README.md
workspace/tasks/milestone1_qwen3_8b_loop/M1-S22-PARSERFIXED-BLOCKER-FIX-DEV4/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/M1-S22-PARSERFIXED-BLOCKER-FIX-DEV4/task_knowledge.md
```

The PR must cite:

```text
task id: M1-S22-PARSERFIXED-BLOCKER-FIX-DEV4
owner: intern_code_dev_4
acceptance criteria: listed below
durable evidence path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_parserfixed_blocker_fix.md
completion marker: ready-for-review or complete after PM gate/self-merge
runtime boundary: no LTP/GPU/preflight/SFT/eval/dry-run/runtime authorization
```

## Proposed Parser Changes

### 1. Xid/SXid freshness classification

Add structured Xid/SXid parsing for allowlisted hardware sources:

```text
source files: dmesg/journal/kernel/NVRM logs, including dmesg_gpu_fault_scan.txt
signatures: Xid <code>, SXid <code>, NVRM Xid, NVRM SXid
metadata fields per match: code, kind, source, line, parsed_time, freshness, text
```

Add a runtime/preflight time context:

```text
preferred start source: run id timestamp, e.g. 20260521T114448Z
secondary start source: torchrun_status start timestamp when available
optional CLI override: --freshness-start-utc
default grace window: include faults at or after allocation/preflight start minus 10 minutes
```

Classification policy:

```text
fresh_current: parsed timestamp is within the current preflight allocation window or later than freshness_start_utc - grace
stale_historical: parsed timestamp is clearly older than the current preflight window
unknown_time: timestamp cannot be parsed from an allowlisted hardware source
```

Action policy:

```text
fresh_current Xid/SXid: actionable fault, blocks SFT
unknown_time Xid/SXid: actionable by default, blocks SFT to avoid suppressing real current hardware faults
stale_historical Xid/SXid: not actionable, recorded under non_actionable_matches and xid_history with freshness=stale_historical
```

This preserves real GPU health detection while allowing PM/test gates to distinguish historical residue from current-node failures.

### 2. Storage status path normalization

Replace literal-only `Path.resolve().relative_to("/home/xu.yang/coding_agent_playground/outputs")` with a storage policy that evaluates both raw and resolved paths.

Accepted generated-output roots:

```text
/home/xu.yang/coding_agent_playground/outputs
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs
```

Required checks:

```text
preflight_dir raw path under /home root: PASS
preflight_dir resolved path under /mnt/cephfs mirror: PASS_WITH_CEPHFS_RESOLUTION
out_json raw/resolved path under accepted roots: PASS
out_text raw/resolved path under accepted roots: PASS when provided
```

Suggested top-level output:

```json
{
  "home_xu_yang_storage_status": "PASS",
  "storage": {
    "status": "PASS",
    "expected_root": "/home/xu.yang/coding_agent_playground/outputs",
    "accepted_resolved_roots": [
      "/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs"
    ],
    "preflight_dir_raw": "/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>",
    "preflight_dir_resolved": "/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>",
    "classification": "PASS_WITH_CEPHFS_RESOLUTION"
  }
}
```

Storage fail policy remains strict for generated artifacts outside both accepted roots.

### 3. Preserve existing real-fault detection

Do not weaken these blockers:

```text
fresh/current Xid or SXid
timestamp-unknown Xid or SXid in allowlisted hardware logs
fatal ECC or nonzero uncorrected ECC counters
NVLink link/down/error/replay/CRC faults
NCCL/CUDA invalid peer GPU memory
rank SIGABRT or torch elastic ChildFailedError
NCCL collective/all_reduce failures
nonzero torchrun status
missing capacity/topology/NVLink/NCCL evidence
generated artifacts outside accepted /home or CephFS mirror roots
```

## Acceptance Criteria

The PR is reviewable when all are true:

```text
1. Parser records Xid/SXid matches with freshness classification: fresh_current, stale_historical, or unknown_time.
2. Clearly stale Xid/SXid entries, such as 2026-04-17 entries during a 2026-05-21 preflight, are non-actionable audit evidence.
3. Fresh or timestamp-unknown Xid/SXid entries remain actionable and block SFT.
4. Storage status is PASS for raw /home/xu.yang/coding_agent_playground/outputs paths even when resolved through /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs.
5. Storage status still fails generated artifacts outside the accepted /home/CephFS roots.
6. Existing PR #45 false-positive suppression for generated command/process/evidence/summary text remains intact.
7. Existing ECC/NVLink/NCCL/SIGABRT/collective failure detection remains intact.
8. Parser emits stable top-level fields required by test_1: preflight_result, health_result, non_actionable_matches, torch_nccl_allreduce_exit, capacity_probe_status, different_node_gate, home_xu_yang_storage_status, topology_capture_status, nvlink_capture_status, sft_allowed, sft_skip_reason.
9. No LTP/GPU/preflight/SFT/eval/dry-run/runtime command is run by dev_4.
```

Recommended local non-runtime tests for that PR:

```text
python3 -m py_compile scripts/parse_s22_preflight_health.py
synthetic stale Xid sample: 2026-04-17 Xid during run_id 20260521T114448Z -> PASS if no other faults
synthetic fresh Xid sample: 2026-05-21 18:18:48 Xid/SXid during matching preflight window -> FAIL_HEALTH_SIGNATURE
synthetic unknown-time Xid sample in dmesg source -> FAIL_HEALTH_SIGNATURE
synthetic /home path with resolved /mnt/cephfs mirror -> home_xu_yang_storage_status PASS
synthetic outside path -> home_xu_yang_storage_status FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
synthetic command/process copied Xid text -> ignored_non_actionable_matches, not actionable
```

## Future Runtime Gate

No future runtime is authorized by this evidence. If PM later gates a parser patch and runtime, the same conditional rule should remain:

```text
Run SFT only if preflight_result=PASS, sft_allowed=true, home_xu_yang_storage_status=PASS, torch_nccl_allreduce_exit=0, capacity/topology/NVLink evidence is present/pass, and no actionable fresh/unknown GPU/NCCL/NVLink/ECC fault is present.
```

Future generated SFT/eval/preflight artifacts must stay under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

CephFS mirror path is acceptable only as the resolved form of that `/home/xu.yang` output tree:

```text
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs
```

## Current Completion

```yaml
task_id: M1-S22-PARSERFIXED-BLOCKER-FIX-DEV4
owner: intern_code_dev_4
result: COMPLETE_PENDING_SELF_MERGE
evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_parserfixed_blocker_fix.md
runtime_review_inputs:
  - evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md
  - evidence/gpu_s22_parserfixed_preflight_sft_tracking.md
  - evidence/dev_1_s22_parserfixed_runtime_review.md
  - evidence/test_1_s22_parserfixed_runtime_gate.md
recommended_pr_files:
  - scripts/parse_s22_preflight_health.py
  - workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_parserfixed_blocker_fix.md
current_pr: https://github.com/peteryang1/coding_agent_playground/pull/47
pm_gate: PASS_OWNER_SELF_MERGE_ONLY
runtime_authorized: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
```
