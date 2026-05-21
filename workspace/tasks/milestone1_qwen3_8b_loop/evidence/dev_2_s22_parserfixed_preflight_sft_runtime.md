# dev_2 S22 Parser-Fixed Preflight + Conditional SFT Runtime

Task ID: `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T11:44:48Z

Scope: PM-authorized one fresh preferably different-node single-node 8 x H200 LTP allocation; run PR #45 parser-fixed NCCL/NVLink/capacity preflight; run exactly one Qwen3-8B ShareGPT SFT smoke only if structured parser-fixed preflight is PASS and `sft_allowed=true`. No eval authorization.

Authorization:

```text
authorization file: evidence/pm_s22_parserfixed_preflight_sft_authorization.md
authorization basis timestamp: 2026-05-21T11:42:20Z
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
PR #45 mergedAt: 2026-05-21T11:42:20Z
PR #45 merge commit: 6f61489e85fcf7e129699061c9ddcb6e8db80926
conditional SFT: only if structured preflight PASS and sft_allowed=true
eval authorized: false
```

Storage contract:

```text
output_root: /home/xu.yang/coding_agent_playground/outputs
All generated artifacts, including preflight, health_status.json/txt, temporary converted datasets, logs, checkpoints, run metadata, trainer outputs, and intermediates must be under output_root.
```

Existing required input exceptions:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source_dataset_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dependency archives/wheels if needed: /mnt/3fs/data/ai4ai/deps
justification: existing required read-only inputs; not used for generated outputs/logs/checkpoints/probes/run metadata/intermediates.
```

## Runtime Status

Initial status: `ALLOCATED_BOOTSTRAPPING`

```text
frame: xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
job: coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
runtime_id: 20260521T114448Z
submit_utc: 2026-05-21T11:44:48Z evidence init; LTP submitted before 2026-05-21T11:45:55Z
ltp_yaml: /tmp/coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z.yaml
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z.yaml
submit result: status 202, Update job coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z for user xu.yang successfully.
wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z --state RUNNING --timeout 1800 --interval 15
wait result: RUNNING at 2026-05-21T11:45:55Z
status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
ssh command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
endpoint: ssh -p 22662 root@10.100.22.14
node: lg-cmc-b7r202-p07u16-h200-000708
initial GPU sample: 8 x NVIDIA H200 visible and idle, 0% util, 1 MiB used each at 2026-05-21T11:46:23Z
SFT: not started
eval: not authorized and not run
```

Different-node check:

```text
failed parser preflight node from immediately prior task: lg-cmc-b7r401-a04u26-h200-000769
fresh allocated node: lg-cmc-b7r202-p07u16-h200-000708
result against authorization preference: PASS_DIFFERENT_FROM_FAILED_PREFLIGHT_NODE
note: allocated node matches older post-PR41 NCCL runtime failure node; PM authorization said preferably different-node, not hard rejection. This is the single authorized fresh allocation, so dev_2 proceeds unless a preflight/runtime blocker appears.
```

## Source Staging

Remote GitHub staging blocker and recovery:

```text
2026-05-21T11:52:54Z check found HTTPS clone stuck on GPU node for about 1m53s.
stuck command: git clone https://github.com/peteryang1/coding_agent_playground.git coding_agent_playground
remote process state: git remote-https/git-remote-http still running, repo only 124K with .git skeleton.
GPU state during blocker: all 8 H200 idle, 0% util, 1 MiB used each.
action: stopped the stuck remote clone attempt and removed partial /root/workspace/coding_agent_playground.
fallback staging: fetched exact merge commit locally, checked out 6f61489e85fcf7e129699061c9ddcb6e8db80926, and staged code to GPU node by tar-over-SSH.
```

Exact code staged on node:

```text
remote repo path: /root/workspace/coding_agent_playground
PR45_MERGE_COMMIT.txt: 6f61489e85fcf7e129699061c9ddcb6e8db80926
scripts/parse_s22_preflight_health.py sha256: 46899d7f280db96a49162d715c5a5bd901a1ee9aebefcb9e939d51567db73c80
scripts/train_qwen3_8b_sft.sh sha256: 9dd84e02bea54915a613159012b0981070ba03e5d3b9cbd8fcda1047957b3cc5
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml sha256: 6493c82d54025d9c7bf6f3afe6e37cb9ea4e5bfe850af9643411f6d6d2591614
staged_utc: 2026-05-21T11:53:40Z
```

## Final Runtime Outcome

Status: `BLOCKED_PARSERFIXED_PREFLIGHT_FAILED_NO_SFT_RUN`

Final decision:

```text
preflight run id: milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
preserved CephFS path: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
structured preflight status: FAIL_HEALTH_SIGNATURE
sft_allowed: false
sft_allowed_if_pm_authorized: false
sft_skip_reason: FAIL_HEALTH_SIGNATURE
conditional SFT: NOT_RUN
reason: PM contract required structured preflight PASS and sft_allowed=true; parser-fixed preflight failed.
checkpoint/model: absent, because SFT was not run.
trainer_state.json: absent, because SFT was not run.
all_results.json: absent, because SFT was not run.
eval: not authorized and not run.
```

Preflight command summary:

```text
capacity probe: PASS_AND_CLEANED; wrote 4 x 6GiB files under preflight dir, verified 25769803776 bytes, then removed probe files.
topology: nvidia-smi topo -m captured; NV18 between every GPU pair.
NVLink: nvidia-smi nvlink --status captured links 0-17 at 26.562 GB/s per GPU.
GPU query: 8 x NVIDIA H200 visible; ECC volatile/aggregate uncorrected counters 0 at query time.
all_reduce_perf: absent in searched paths; accepted substitute used torchrun 8-rank NCCL all-reduce.
NCCL env: NCCL_DEBUG=INFO; NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL; NCCL_ASYNC_ERROR_HANDLING=1; TORCH_NCCL_ASYNC_ERROR_HANDLING=1; CUDA_DEVICE_MAX_CONNECTIONS=1; NCCL_P2P_DISABLE unset.
torchrun command: torchrun --standalone --nnodes 1 --nproc_per_node 8 torch_nccl_allreduce.py
torchrun result: TORCHRUN_EXIT=0, start 2026-05-21T11:55:23Z, end 2026-05-21T11:55:35Z.
parser command: python3 scripts/parse_s22_preflight_health.py --preflight-dir "$PREFLIGHT" --out-json "$PREFLIGHT/health_status.json" --out-text "$PREFLIGHT/health_status.txt"
```

Parser-fixed health evidence:

```text
health_status.json sha256: 52d1f1c42c4dae91c8e61a3cf3d212733657d53436ae9a4f7b2d1d422ef95b96
health_status.txt sha256: 49c825365e692fc75f2141d252b4ce0fc23e6bce3d657f77b80ebb99e3d95116
torchrun_status.txt sha256: 5967f198344a5e5c0c4a527091acbaf4b9bd60dfb4728e68fb5fc811a4a32848
torch_nccl_allreduce.log sha256: 092c2e3078edec2c5acfaba6fdb9d27c6912ac1bd93d6475a56b1517ac125a2c
artifact_count: 28 top-level files
artifact_size: 885K
```

`health_status.txt` summary:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE
ACTIONABLE_FAULT=true
SFT_ALLOWED=false
SFT_ALLOWED_IF_PM_AUTHORIZED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=actionable GPU/NCCL health signature found
```

Health blocker details:

```text
health_status.json recorded actionable_fault=true with Xid matches in dmesg_gpu_fault_scan.txt.
Examples include historical Xid 43 entries from 2026-04-17 and Xid 137 / SXid 12028 entries from 2026-05-21 18:18:48 local node time.
The parser also reported HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS even though artifacts were written through /home/xu.yang/coding_agent_playground/outputs and preserved under the CephFS mirror; this may be due path resolution/classification, but it is still a structured fail and blocks SFT.
Because structured status was not PASS and sft_allowed was false, no SFT command/config/log/checkpoint was generated for this task.
```

Immediate post-preflight node sample before stop:

```text
sample_time: 2026-05-21T11:55:52Z
endpoint: ssh -p 22662 root@10.100.22.14
node: lg-cmc-b7r202-p07u16-h200-000708
GPU 0-7: 0% utilization, 1 MiB used each
matching torchrun/LLamaFactory/deepspeed/accelerate/train_qwen3 processes: none
```

Stop proof:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z --timeout 600 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 22662 root@10.100.22.14 true
```

```text
stop_sent_utc: 2026-05-21T11:56:07Z
wait_result: STOPPED at 2026-05-21T11:56:45Z
ltp_status: STOPPED (Completed)
ltp_completed: 2026-05-21 11:56:39
endpoint proof: ssh to 10.100.22.14:22662 returned "Connection refused"
artifact preservation: preflight artifacts remain under /home/xu.yang/coding_agent_playground/outputs/preflight/... on CephFS; no cleanup of evidence artifacts was performed.
```
