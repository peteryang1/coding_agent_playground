# dev_2 S22 Parser-Fixed Resource Recovery Plan

Task ID: `M1-S22-PARSERFIXED-RESOURCE-RECOVERY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T12:01:42Z

Scope: no-submit resource recovery plan after `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2` stopped with parser-fixed health/storage failure and no SFT. This is planning/evidence only. I did not submit LTP, run GPU, run NCCL preflight, run SFT, run eval, or run commands on the stopped GPU node for this task; this file is based on prior durable evidence/status.

## Source Evidence Read

Read-only local evidence/status paths used:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_parserfixed_preflight_sft_tracking.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
```

No GPU-node command was run for this planning task.

## Stopped/Released Confirmation

Prior runtime frame:

```text
frame: xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
endpoint: ssh -p 22662 root@10.100.22.14
node: lg-cmc-b7r202-p07u16-h200-000708
post-stop LTP state from prior evidence: STOPPED (Completed)
completed timestamp from prior evidence: 2026-05-21 11:56:39
stop sent UTC from prior evidence: 2026-05-21T11:56:07Z
wait result from prior evidence: STOPPED at 2026-05-21T11:56:45Z
endpoint proof from prior evidence: ssh to 10.100.22.14:22662 returned "Connection refused"
resource conclusion: prior frame is stopped/released; dev_2 holds no active GPU for this task.
```

## Blocker Facts

Node/resource facts:

```text
node: lg-cmc-b7r202-p07u16-h200-000708
allocation freshness: fresh LTP frame for parser-fixed runtime, but node matched older post-PR41 NCCL-failure node.
different-node status: different from immediately failed parser-preflight node lg-cmc-b7r401-a04u26-h200-000769; not different from older post-PR41 NCCL blocker node.
remote staging blocker: GitHub HTTPS clone stuck with only a 124K .git skeleton while GPUs were idle; exact PR #45 merge commit was staged by local tar-over-SSH.
```

Preflight facts:

```text
preflight run id: milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
preflight artifacts: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
capacity probe: PASS_AND_CLEANED, 4 x 6GiB real writes verified and removed.
topology/NVLink: captured.
torch NCCL all-reduce: TORCHRUN_EXIT=0.
parser-fixed health status: FAIL_HEALTH_SIGNATURE.
sft_allowed: false.
sft_allowed_if_pm_authorized: false.
sft_skip_reason: FAIL_HEALTH_SIGNATURE.
storage status: HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS.
actionable health source: health_status.json recorded Xid matches in dmesg_gpu_fault_scan.txt.
SFT: not run, correctly blocked by structured preflight.
checkpoint/model/trainer_state/all_results: absent because SFT was not run.
eval: not authorized and not run.
```

Recovery interpretation:

```text
The next resource attempt should not treat the parser-fixed preflight as cleared.
It needs both health recovery and storage-status recovery before SFT can run.
The same physical node lg-cmc-b7r202-p07u16-h200-000708 should be avoided because it produced the parser-fixed health/storage blocker and also matches the older post-PR41 NCCL failure node.
```

## 2026-05-21T12:08:01Z Supervisor No-Remote-Network Correction

Supervisor correction applied to this recovery task and all future GPU/LTP runtime work:

```text
remote GPU/LTP node network assumption: treat as no external network.
remote forbidden actions for source/deps: no git clone, git fetch, pip/download, GitHub fetch, curl/wget source fetch, or equivalent external-network dependency/source retrieval on GPU nodes.
future staging rule: prepare all needed code, config, scripts, and dependency/material bundles in the provided/local workspace before allocation/runtime.
future verification rule: verify source commit, file list, and checksums locally before transfer.
future transfer rule: transfer prepared bundle to the remote node with rsync, scp, or tar-over-SSH only.
future evidence rule: record exact transfer command, source path, destination path, source commit, file list, sha256 checksums, and post-transfer verification in runtime evidence.
future command-template rule: runtime templates must not rely on remote GitHub clone/fetch or remote pip/download.
```

Clarification for the already completed parser-fixed runtime:

```text
remote GitHub SSH clone attempt: stopped after timeout/blockage.
remote GitHub HTTPS clone attempt: stopped/removed after it stuck with only a 124K .git skeleton while GPUs were idle.
actual successful code staging: local exact PR #45 merge commit tar-over-SSH to /root/workspace/coding_agent_playground.
staged source commit: 6f61489e85fcf7e129699061c9ddcb6e8db80926.
recorded staged-file checksums from prior runtime evidence:
  scripts/parse_s22_preflight_health.py sha256 46899d7f280db96a49162d715c5a5bd901a1ee9aebefcb9e939d51567db73c80
  scripts/train_qwen3_8b_sft.sh sha256 9dd84e02bea54915a613159012b0981070ba03e5d3b9cbd8fcda1047957b3cc5
  configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml sha256 6493c82d54025d9c7bf6f3afe6e37cb9ea4e5bfe850af9643411f6d6d2591614
frame state: already STOPPED (Completed); do not re-open or submit another allocation for this correction.
correction task actions: no LTP submit, no GPU command, no NCCL/preflight command, no SFT, no eval, and no GPU-node command.
```

## Future Retry Criteria

A future retry should be considered only after dev_4/dev_1/test_1 gates and fresh PM authorization. Recommended criteria:

```text
1. Fresh single-node 8 x NVIDIA H200 allocation.
2. Prefer a physical node different from:
   - lg-cmc-b7r202-p07u16-h200-000708
   - lg-cmc-b7r401-a04u26-h200-000769
3. Stage exact authorized code from a prepared local/provided-workspace bundle only; treat GPU/LTP nodes as no-external-network targets and do not run remote git clone/fetch, pip/download, or GitHub fetch. Transfer by tar-over-SSH, rsync, or scp, then record exact transfer command, source commit, file list, sha256 checksums, source path, destination path, and post-transfer verification.
4. Use /home/xu.yang/coding_agent_playground/outputs for every generated artifact.
5. Run capacity probe under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID> and require PASS.
6. Run NCCL/NVLink/topology preflight and parser-fixed health parser.
7. Require health_status.json/txt to show:
   - preflight status PASS
   - sft_allowed=true
   - actionable_fault=false
   - HOME_XU_YANG_STORAGE_STATUS=PASS
   - capacity/topology/NVLink/NCCL statuses present and passing
8. Run exactly one SFT smoke only if PM explicitly authorizes runtime and the structured preflight criteria pass.
```

## Required Future Paths

All future generated artifacts must be under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Recommended path layout:

```text
capacity probes: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>/
preflight artifacts: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/
parser JSON status: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/health_status.json
parser text status: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/health_status.txt
run metadata: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/
SFT logs: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/logs/
SFT config: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/config/
temporary converted datasets/intermediates: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/tmp/
checkpoints/model: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/checkpoints/
trainer outputs: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/trainer_outputs/
stop proof/evidence copies: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/stop_proof/
```

Existing required read-only input exceptions:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source_dataset_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dependency archives/wheels if needed: /mnt/3fs/data/ai4ai/deps
justification: existing required read-only inputs only; no generated artifacts belong outside /home/xu.yang/coding_agent_playground/outputs.
```

## Stop Conditions

Future stop/release conditions:

```text
allocation lands on a PM-rejected/same blocked physical node;
/home/xu.yang path proof fails;
capacity probe fails or cannot clean probe files;
parser health_status.json/txt missing, malformed, or ambiguous;
structured status is not PASS;
sft_allowed is not true;
HOME_XU_YANG_STORAGE_STATUS is not PASS;
actionable Xid/ECC/NVLink/NCCL fault is detected;
torch NCCL all-reduce fails or hangs;
SFT succeeds and writes accepted checkpoint/model;
SFT fails with no PM-authorized same-node retry;
node becomes unhealthy or idle without progress;
PM/test stop instruction;
bounded max runtime reached.
```

Required stop proof:

```text
LTP stop command/action
UTC stop timestamp
post-stop LTP terminal status
endpoint refusal or equivalent unreachable proof
artifact preservation note for /home/xu.yang/coding_agent_playground/outputs
```

## No-Submit Boundary

```text
No LTP submit is authorized by this recovery plan.
No GPU command is authorized by this recovery plan.
No NCCL preflight is authorized by this recovery plan.
No SFT is authorized by this recovery plan.
No eval is authorized by this recovery plan.
Future execution requires fresh PM authorization after the required dev_4/dev_1/test_1 gates.
```

## Completion Marker

`M1-S22-PARSERFIXED-RESOURCE-RECOVERY-DEV2` is complete as a no-submit planning task. Evidence/status were updated durably; no resource was acquired or touched.
