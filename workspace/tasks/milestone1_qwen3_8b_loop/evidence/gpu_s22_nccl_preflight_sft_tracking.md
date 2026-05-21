# GPU Resource Tracking - S22 NCCL Preflight + Conditional SFT

Task ID: `M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T10:55:25Z

Scope:

```text
One fresh single-node 8 x H200 LTP allocation.
First run NCCL/NVLink preflight under /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>.
Run exactly one SFT smoke only if preflight passes.
Stop/release after preflight failure, same-node rejection, SFT success/failure, health/idle issue, or PM/test stop.
No eval.
```

Required output root:

```text
/home/xu.yang/coding_agent_playground/outputs
```

## Resource State

Submitted and initial running state:

```text
frame: xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
job: coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
submitted: 2026-05-21 10:56:15
started: 2026-05-21 10:56:20
state: RUNNING (AttemptRunning)
endpoint: ssh -p 27402 root@10.100.24.11
hostname: lg-cmc-b7r401-a04u26-h200-000769
different-node gate: PASS, not failed node lg-cmc-b7r202-p07u16-h200-000708
expected stop/review: 2026-05-21T11:56:20Z unless preflight/SFT finishes earlier
```

Submit command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z.yaml
```

Stop conditions:

```text
same-node rejection;
failed /home/xu.yang proof;
failed NCCL/NVLink preflight;
SFT checkpoint/model success;
SFT failure with no authorized retry;
health/idle issue;
PM/test stop order.
```

Bootstrap observation:

```text
2026-05-21T10:56:52Z
LTP container is RUNNING but still in apt/bootstrap.
GPU: all 8 H200 idle.
SFT: not started.
preflight: not started.
```

## Final Resource State

Outcome: `STOPPED_AFTER_PREFLIGHT_FAILURE_NO_SFT`

Preflight result:

```text
run_id: milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
preflight_dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
preserved CephFS path: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_nccl_preflight_sharegpt_tp8_maxsteps2_20260521T105525Z
preflight_result: PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
capacity_probe: PASS_AND_CLEANED, 4 x 6GiB real writes verified then removed
torch NCCL substitute: TORCHRUN_EXIT=0, 8 ranks, NCCL_DEBUG enabled, NCCL_P2P_DISABLE unset
SFT: not run because preflight did not pass
eval: not authorized and not run
```

Artifact preservation:

```text
artifact_count: 26 files at top level
artifact_size: 815K
preflight_result.txt sha256: 2bf3887d5cf81d9ab6cf0f0ec3aea267c45efe8af83ecd757a2c151d937b1775
torchrun_status.txt sha256: 653722c900ccceb6c19295854cdc93c3bf0b5519340bf4c72aea9ec65bc7e861
torch_nccl_allreduce.log sha256: 4ccd4c253cd6e66e5ba79d3bf7e781595da74b6ab15964d9f8013dd823c669af
```

Post-preflight live sample before stop:

```text
sample_time: 2026-05-21T11:01:22Z
endpoint: ssh -p 27402 root@10.100.24.11
hostname: lg-cmc-b7r401-a04u26-h200-000769
GPU 0-7: NVIDIA H200, 0% utilization, 1 MiB used each
matching training processes: none
```

Stop action and proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
stop sent: 2026-05-21T11:01:38Z
wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z --timeout 600 --interval 15
wait result: STOPPED at 2026-05-21T11:02:18Z
status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
post-stop state: STOPPED (Completed)
completed: 2026-05-21 11:02:09
endpoint proof command: ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 27402 root@10.100.24.11 true
endpoint proof result: ssh: connect to host 10.100.24.11 port 27402: Connection refused
```

No active held Milestone GPU:

```text
dev_2 stopped the only allocation acquired for M1-S22-NCCL-PREFLIGHT-SFT-RUNTIME-DEV2.
The endpoint refuses connection after LTP STOPPED (Completed).
No SFT or eval process was left running because SFT/eval were never started.
Future LTP/GPU/NCCL preflight/SFT work requires fresh PM authorization.
```
