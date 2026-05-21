# GPU Resource Tracking - S22 Parser-Fixed Preflight + Conditional SFT

Task ID: `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T11:44:48Z

Scope:

```text
One fresh preferably different-node single-node 8 x H200 LTP allocation.
Run PR #45 parser-fixed preflight first under /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>.
Run exactly one Qwen3-8B ShareGPT SFT smoke only if health_status.json is PASS and sft_allowed=true.
Stop/release after preflight failure/SFT skip, SFT success/failure, health/idle issue, or PM/test stop.
No eval.
```

Required output root:

```text
/home/xu.yang/coding_agent_playground/outputs
```

## Resource State

Initial state: `RUNNING_BOOTSTRAPPING`

```text
frame: xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
job: coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
ltp_yaml: /tmp/coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z.yaml
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z.yaml
submit result: status 202
started: 2026-05-21 11:45:49
state: RUNNING (AttemptRunning)
endpoint: ssh -p 22662 root@10.100.22.14
node: lg-cmc-b7r202-p07u16-h200-000708
different-node check: PASS versus immediate failed preflight node lg-cmc-b7r401-a04u26-h200-000769
initial GPU sample: all 8 H200 idle at 2026-05-21T11:46:23Z
expected stop/review: 2026-05-21T12:45:49Z unless preflight/SFT finishes earlier
```

Staging blocker and recovery:

```text
2026-05-21T11:52:54Z: remote HTTPS git clone was stuck for about 1m53s with only a 124K .git skeleton; GPUs idle.
action: stopped/removed stuck remote GitHub staging attempt.
fallback: staged exact PR #45 merge commit 6f61489e85fcf7e129699061c9ddcb6e8db80926 from local checkout to /root/workspace/coding_agent_playground by tar-over-SSH.
staged_utc: 2026-05-21T11:53:40Z
```

## Final Resource State

Outcome: `STOPPED_AFTER_PARSERFIXED_PREFLIGHT_FAILURE_NO_SFT`

Preflight result:

```text
run_id: milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
preflight_dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
preserved CephFS path: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s22_parserfixed_preflight_sharegpt_tp8_maxsteps2_20260521T114448Z
structured status: FAIL_HEALTH_SIGNATURE
sft_allowed: false
capacity_probe: PASS_AND_CLEANED, 4 x 6GiB real writes verified then removed
torch NCCL substitute: TORCHRUN_EXIT=0, 8 ranks, NCCL_DEBUG enabled, NCCL_P2P_DISABLE unset
SFT: not run because parser-fixed preflight did not pass
eval: not authorized and not run
```

Post-preflight live sample before stop:

```text
sample_time: 2026-05-21T11:55:52Z
endpoint: ssh -p 22662 root@10.100.22.14
node: lg-cmc-b7r202-p07u16-h200-000708
GPU 0-7: 0% utilization, 1 MiB used each
matching training processes: none
```

Stop action and proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
stop sent: 2026-05-21T11:56:07Z
wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z --timeout 600 --interval 15
wait result: STOPPED at 2026-05-21T11:56:45Z
status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
post-stop state: STOPPED (Completed)
completed: 2026-05-21 11:56:39
endpoint proof command: ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 22662 root@10.100.22.14 true
endpoint proof result: ssh: connect to host 10.100.22.14 port 22662: Connection refused
```

No active held Milestone GPU:

```text
dev_2 stopped the only allocation acquired for M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2.
The endpoint refuses connection after LTP STOPPED (Completed).
No SFT or eval process was left running because SFT/eval were never started.
Future LTP/GPU/NCCL preflight/SFT work requires fresh PM authorization.
```
