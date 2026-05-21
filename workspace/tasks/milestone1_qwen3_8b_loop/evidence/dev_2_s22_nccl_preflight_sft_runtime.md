# dev_2 S22 NCCL Preflight + Conditional SFT Runtime

Task ID: `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T10:55:25Z

Scope: one PM-authorized fresh single-node 8 x H200 LTP allocation; run NCCL/NVLink preflight first; run exactly one Qwen3-8B ShareGPT SFT smoke only if preflight passes. No eval authorization.

Authorization:

```text
authorization file: evidence/pm_s22_nccl_preflight_sft_authorization.md
authorization timestamp: 2026-05-21T10:53:00Z
authorization decision: AUTHORIZED_DEV2_ONLY_ONE_FRESH_DIFFERENT_NODE_PREFLIGHT_THEN_CONDITIONAL_SFT
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
preferred node rule: different physical node than failed post-PR41 node lg-cmc-b7r202-p07u16-h200-000708
conditional SFT: only if NCCL/NVLink preflight passes
eval authorized: false
```

Storage contract:

```text
output_root: /home/xu.yang/coding_agent_playground/outputs
preflight_root: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
all generated artifacts, output/log/tmp/checkpoint/run metadata/intermediates/capacity probes must stay under /home/xu.yang/coding_agent_playground/outputs unless an existing required input path is explicitly justified.
```

Existing required input exceptions:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dependency_archives_wheels: /mnt/3fs/data/ai4ai/deps
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
justification: required read-only inputs/source artifact; not used for outputs/logs/checkpoints/probes/run metadata/intermediates.
```

## Submit And Node

Submit command:

```bash
RUNTIME_ID=20260521T105525Z
JOB_NAME=coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
FRAME=xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
LTP_YAML=/tmp/coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z.yaml
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Submit result:

```text
status: 202
message: Update job coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z for user xu.yang successfully.
```

Initial status:

```text
frame: xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
state: RUNNING (AttemptRunning)
submitted: 2026-05-21 10:56:15
started: 2026-05-21 10:56:20
ip: 10.100.24.11
ssh port: 27402
endpoint: ssh -p 27402 root@10.100.24.11
hostname: lg-cmc-b7r401-a04u26-h200-000769
```

Different-node gate:

```text
failed post-PR41 node: lg-cmc-b7r202-p07u16-h200-000708
fresh node: lg-cmc-b7r401-a04u26-h200-000769
result: PASS_DIFFERENT_PHYSICAL_NODE
```

Initial bootstrap observation:

```text
2026-05-21T10:56:52Z
hostname: lg-cmc-b7r401-a04u26-h200-000769
bootstrap still running apt update
/home/xu.yang missing before CephFS bootstrap
/mnt/cephfs/home/xu.yang missing before CephFS bootstrap
GPU: 8 x NVIDIA H200 visible and idle, 0% util, 1 MiB used each
SFT: not started
preflight: not started
```

## Final Runtime Outcome

Status: `BLOCKED_PREFLIGHT_FAILED_NO_SFT_RUN`

Final decision:

```text
preflight_result: PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
conditional_sft: NOT_RUN
reason: PM contract required SFT only if preflight passes; preflight wrote FAIL marker.
checkpoint/model: absent, because SFT was not run.
trainer_state.json: absent, because SFT was not run.
all_results.json: absent, because SFT was not run.
eval: not authorized and not run.
```

Allocation and endpoint:

```text
frame: xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
job: coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
state after stop: STOPPED (Completed)
submitted: 2026-05-21 10:56:15
started: 2026-05-21 10:56:20
completed: 2026-05-21 11:02:09
endpoint: ssh -p 27402 root@10.100.24.11
node: lg-cmc-b7r401-a04u26-h200-000769
different-node check: PASS, not failed node lg-cmc-b7r202-p07u16-h200-000708
```

Nodes JSON content:

```json
{
  "frame": "xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z",
  "job": "coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z",
  "nodes": [
    {
      "hostname": "lg-cmc-b7r401-a04u26-h200-000769",
      "ip": "10.100.24.11",
      "ssh_port": 27402,
      "endpoint": "ssh -p 27402 root@10.100.24.11",
      "gpu": "8 x NVIDIA H200"
    }
  ]
}
```

Preflight artifacts:

```text
preflight_dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
preserved CephFS path: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
artifact_count: 26 files at top level
artifact_size: 815K
preflight_result.txt sha256: 2bf3887d5cf81d9ab6cf0f0ec3aea267c45efe8af83ecd757a2c151d937b1775
torchrun_status.txt sha256: 653722c900ccceb6c19295854cdc93c3bf0b5519340bf4c72aea9ec65bc7e861
torch_nccl_allreduce.log sha256: 4ccd4c253cd6e66e5ba79d3bf7e781595da74b6ab15964d9f8013dd823c669af
```

Preflight command/probe summary:

```text
/home/xu.yang proof: created /home/xu.yang symlink to /mnt/cephfs/home/xu.yang after CephFS mount was available.
output root: /home/xu.yang/coding_agent_playground/outputs
df output root: ceph-fuse, 18P size, 16P available, 11% used.
capacity probe: PASS_AND_CLEANED; wrote 4 x 6GiB files under preflight dir, verified 25769803776 bytes, then removed probe files.
GPU query: 8 x NVIDIA H200 visible, 0% util, 1 MiB used each before and after preflight.
NVLink status: nvidia-smi nvlink --status captured links 0-17 at 26.562 GB/s per GPU.
topology: nvidia-smi topo -m showed NV18 between every GPU pair.
all_reduce_perf: not present in searched paths; acceptable substitute used torchrun 8-rank NCCL all-reduce.
NCCL env: NCCL_DEBUG=INFO; NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL; NCCL_ASYNC_ERROR_HANDLING=1; TORCH_NCCL_ASYNC_ERROR_HANDLING=1; CUDA_DEVICE_MAX_CONNECTIONS=1; NCCL_P2P_DISABLE unset.
torchrun command: torchrun --standalone --nnodes 1 --nproc_per_node 8 torch_nccl_allreduce.py
torchrun result: TORCHRUN_EXIT=0, start 2026-05-21T10:59:18Z, end 2026-05-21T10:59:31Z.
final preflight marker: PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE.
```

Conditional SFT command/config status:

```text
SFT command executed: no
SFT config generated: no
SFT log path: none
SFT output/checkpoint path: none
reason: preflight marker was FAIL, and PM authorization allowed SFT only if preflight passed.
base model that would have been used after PASS: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset that would have been used after PASS: coding_agent_m1_sft_10_sharegpt
source dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
required post-PASS output root: /home/xu.yang/coding_agent_playground/outputs
```

Health-signature blocker:

```text
The preflight driver scanned the whole preflight directory with:
rg -i "Invalid access of peer GPU memory|hardware error|SIGABRT|Xid|fatal|uncorrected.*[1-9]" "$PREFLIGHT"

That final scan matched broad evidence content in the preflight artifacts and wrote PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE.
Notable captured matches include historical/generic NVRM loading lines and the command text/process-scan copies that contain the searched terms.
The torch NCCL substitute itself exited 0, capacity passed, and immediate post-preflight GPU/process sampling showed all 8 GPUs idle with no training process.
However, because the durable preflight result is FAIL, I did not run SFT.
```

Immediate post-preflight node sample:

```text
sample_time: 2026-05-21T11:01:22Z
hostname: lg-cmc-b7r401-a04u26-h200-000769
GPU 0-7: NVIDIA H200, 0% utilization, 1 MiB used each
matching torchrun/LLamaFactory/deepspeed/accelerate training processes: none
```

Stop proof:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z --timeout 600 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 27402 root@10.100.24.11 true
```

```text
stop_sent_utc: 2026-05-21T11:01:38Z
wait_result: STOPPED at 2026-05-21T11:02:18Z
ltp_status: STOPPED (Completed)
ltp_completed: 2026-05-21 11:02:09
endpoint proof: ssh to 10.100.24.11:27402 returned "Connection refused"
artifact preservation: preflight artifacts remain under /home/xu.yang/coding_agent_playground/outputs/preflight/... on CephFS; no cleanup of evidence artifacts was performed.
```

Next fix recommendation:

```text
Do not reuse this stopped allocation. Before any future PM authorization, refine the preflight health parser so it does not scan its own command/process text and so it distinguishes actionable GPU fault patterns from historical/generic NVRM/NVLink initialization lines. A future authorization should still require a fresh different-node allocation, /home/xu.yang output root, capacity probe, NCCL/NVLink preflight, and SFT only after a PASS marker.
```
