# Dev 4 S22 Preflight Parser Fix Package

Task ID: `M1-S22-PREFLIGHT-PARSER-FIX-DEV4`

Owner: `intern_code_dev_4`

Created: 2026-05-21

Scope: no-execution parser refinement package for the S22 NCCL/NVLink preflight false health-signature fail.

Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_preflight_parser_fix.md`

Completion marker: ready-for-review; wait for PM/dev_1/test_1 gate before owner self-merge. This package does not authorize LTP/GPU/SFT/eval/dry-run execution.

## Inputs Reviewed

Primary evidence:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_nccl_preflight_sft_runtime.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s22_nccl_retry_gate.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_nccl_preflight_sft_tracking.md
```

Dev 2 final preflight result:

```text
runtime task: M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2
node: lg-cmc-b7r401-a04u26-h200-000769
endpoint while active: ssh -p 27402 root@10.100.24.11
run_id: milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
preflight_dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
preflight_result: PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
conditional_sft: NOT_RUN
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
stop proof: STOPPED (Completed), endpoint refused after stop
```

What passed before the final health scan:

```text
fresh different H200 node: PASS
capacity probe: PASS_AND_CLEANED, 4 x 6GiB verified and removed
GPU visibility: 8 x NVIDIA H200 visible and idle
topology: nvidia-smi topo -m captured NV18 between every GPU pair
NVLink status: links 0-17 captured at 26.562 GB/s per GPU
torch NCCL substitute: torchrun --standalone --nnodes 1 --nproc_per_node 8 torch_nccl_allreduce.py
torchrun result: TORCHRUN_EXIT=0
SFT command: not run because final preflight marker was FAIL
```

Observed false-fail source:

```text
The preflight driver recursively scanned the whole preflight directory with:
rg -i "Invalid access of peer GPU memory|hardware error|SIGABRT|Xid|fatal|uncorrected.*[1-9]" "$PREFLIGHT"

The scan matched generated command/process/evidence text and generic captured NVRM lines, including copied search terms. That turned an otherwise passing capacity/topology/NVLink/8-rank torch NCCL preflight into PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE.
```

## Diagnosis

The runtime did the correct safety action by not launching SFT after a FAIL marker. The blocker is the health-signature parser policy: a recursive grep across the entire preflight directory treats generated command text, process scans, evidence notes, and copied historical phrases as actionable GPU health faults.

This is not a regression in:

```text
PR39 diagnostics: preserved
PR41 single-process preprocessing: preserved, preprocessing_num_workers: null remains required
PR43 NCCL env/preflight concept: preserved
CephFS output policy: preserved, outputs/logs/checkpoints/run metadata/intermediates remain under /home/xu.yang/coding_agent_playground/outputs
ShareGPT data contract: preserved, coding_agent_m1_sft_10_sharegpt remains the dataset entry
```

## Patch Scope

Added:

```text
scripts/parse_s22_preflight_health.py
```

PM PR #45 gate update addressed:

```text
dev_1 blocker: BLOCKER_ECC_FALSE_NEGATIVE_RISK_IN_PR45
test_1 blocker: BLOCKED_STRUCTURED_FIELDS_AND_STORAGE_STATUS
```

The parser is no-execution and local-artifact-only. It does not contact a GPU node, start LTP, run SFT, run eval, or perform a dry-run launch.

Core behavior:

```text
1. Allowlist actionable sources such as dmesg/journal/kernel/NVRM logs, nvidia-smi ECC/NVLink/topology captures, torch_nccl/allreduce logs, and training stdout/stderr.
2. Exclude generated command files, process listings, durable evidence/history/task notes, parser outputs, manifests, xtrace, summaries, and legacy result files from actionable matching.
3. Preserve excluded matches under ignored_non_actionable_matches for audit.
4. Produce structured JSON fields: status, actionable_fault, actionable_faults, ignored_non_actionable_matches, sources_scanned, sources_excluded, checks, decision, policy.
5. Return PASS only when allowlisted artifacts have no actionable fault and required topology/NVLink/NCCL evidence is present.
```

Required stable top-level compatibility fields:

```text
preflight_result
health_result
non_actionable_matches
torch_nccl_allreduce_exit
capacity_probe_status
different_node_gate
home_xu_yang_storage_status
topology_capture_status
nvlink_capture_status
sft_allowed
sft_skip_reason
```

Preserved real-fault detection:

```text
Xid in kernel/dmesg/NVRM logs
fatal or nonzero uncorrected ECC
NVLink link/down/error/replay/CRC faults
NCCL/CUDA invalid access of peer GPU memory
rank SIGABRT or torch elastic ChildFailedError
NCCL collective/all_reduce failures
nonzero torchrun status
```

ECC parsing refinement:

```text
fatal ECC: always actionable when present in an allowlisted hardware/runtime source
uncorrected ECC: actionable when the counter tied to the uncorrected/ECC field is nonzero
false-negative fix: unrelated standalone zero tokens such as GPU 0, rank 0, or timestamp fields no longer suppress a nonzero uncorrected ECC counter
example actionable line: GPU 0 timestamp 2026-05-21 11:00:00 Uncorrected ECC errors: 1
example non-actionable line: GPU 0 timestamp 2026-05-21 11:00:00 Uncorrected ECC errors: 0
```

Excluded from actionable scan:

```text
generated command text
process scan output
durable evidence/history/task notes
summary/result files that can copy searched terms
xtrace/manifest/parser outputs
unknown artifact names
```

Storage status behavior:

```text
home_xu_yang_storage_status=PASS only when the parsed preflight directory is under /home/xu.yang/coding_agent_playground/outputs
home_xu_yang_storage_status=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS blocks sft_allowed
```

## Proposed Future Usage

Run only after PM authorizes a future GPU preflight or runtime gate:

```bash
cd /root/workspace/coding_agent_playground
python3 scripts/parse_s22_preflight_health.py \
  --preflight-dir "/home/xu.yang/coding_agent_playground/outputs/preflight/${RUN_ID}" \
  --out-json "/home/xu.yang/coding_agent_playground/outputs/preflight/${RUN_ID}/health_status.json" \
  --out-text "/home/xu.yang/coding_agent_playground/outputs/preflight/${RUN_ID}/health_status.txt"
```

Future SFT launch rule:

```text
Only a structured parser status of PASS should allow conditional SFT to proceed, and only when PM has authorized that runtime. FAIL_HEALTH_SIGNATURE or WARN_INCOMPLETE must block SFT.
```

Expected structured pass fields after a healthy preflight:

```json
{
  "preflight_result": "PASS",
  "status": "PASS",
  "actionable_fault": false,
  "home_xu_yang_storage_status": "PASS",
  "sft_allowed": true,
  "sft_skip_reason": "",
  "decision": {
    "sft_allowed_if_pm_authorized": true,
    "reason": [
      "allowlisted preflight artifacts passed without actionable health signatures"
    ]
  }
}
```

Expected structured fail fields for a true NCCL/NVLink fault:

```json
{
  "preflight_result": "FAIL_HEALTH_SIGNATURE",
  "status": "FAIL_HEALTH_SIGNATURE",
  "actionable_fault": true,
  "sft_allowed": false,
  "sft_skip_reason": "FAIL_HEALTH_SIGNATURE",
  "decision": {
    "sft_allowed_if_pm_authorized": false,
    "reason": [
      "actionable GPU/NCCL health signature found"
    ]
  }
}
```

## Storage And Boundary

Default future SFT/preflight paths remain:

```text
output root: /home/xu.yang/coding_agent_playground/outputs
preflight root: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>
run logs: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs
checkpoint root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
temporary converted datasets/intermediates: /home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>
```

Existing required input exceptions remain read-only only:

```text
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dependency archives/wheels: /mnt/3fs/data/ai4ai/deps
source dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

No LTP/GPU/SFT/eval/dry-run command was run for this task.

## Verification

Local non-runtime checks:

```text
python3 -m py_compile scripts/parse_s22_preflight_health.py
python3 scripts/parse_s22_preflight_health.py on a synthetic local artifact directory
git diff --check
```

Synthetic parser check result:

```text
excluded command/process text containing Invalid access of peer GPU memory, SIGABRT, Xid, and fatal was recorded as ignored_non_actionable_matches
torchrun_status.txt with TORCHRUN_EXIT=0 was treated as non-actionable status evidence
allowlisted torch_nccl_allreduce.log without fault signatures did not produce actionable faults
home_xu_yang_storage_status was emitted and gates sft_allowed
ECC false-negative regression: GPU 0 plus Uncorrected ECC errors: 1 is detected as ecc_nonzero_or_fatal
structured status: PASS
```

## PR Status

PR: PR #45 `https://github.com/peteryang1/coding_agent_playground/pull/45`

GitHub mergeability after gate-fix push: pending recheck.

Completion marker: ready-for-review; wait for PM gate before self-merge.
