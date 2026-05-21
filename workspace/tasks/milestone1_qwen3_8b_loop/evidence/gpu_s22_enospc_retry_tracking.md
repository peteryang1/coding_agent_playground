# GPU Resource Tracking - Session 22 ENOSPC-Fixed Retry

Task ID: `M1-S22-ENOSPC-RETRY-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T08:19:32Z

Authorization:

```text
Exactly one fresh LTP job and one ShareGPT Qwen3-8B SFT smoke attempt are authorized.
Stop/release after checkpoint, failure, failed capacity probe, idle/health limit, or PM/test stop instruction.
Do not run eval.
Do not peer_send PM routine status.
```

Required storage root:

```text
/home/xu.yang/coding_agent_playground/outputs
```

## Resource State

Submitted/running:

```text
frame: xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
job: coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
submitted: 2026-05-21 08:20:48
started: 2026-05-21 08:20:53
state: RUNNING (AttemptRunning)
endpoint: ssh -p 31346 root@10.100.16.69
```

Submit command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z.yaml
```

Node proof:

```text
2026-05-21T08:23:57Z
hostname: lg-cmc-b7r202-i03u06-h200-000571
endpoint: ssh -p 31346 root@10.100.16.69
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB memory each
CephFS: /home/xu.yang resolves to /mnt/cephfs/home/xu.yang, findmnt shows /mnt/cephfs fuse.ceph-fuse ceph-fuse
output root writable: /home/xu.yang/coding_agent_playground/outputs
```

Capacity probe:

```text
2026-05-21T08:24:13Z to 2026-05-21T08:24:52Z
path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
result: PASS_RECOVERED_AND_CLEANED
bytes written: 25769803776
files: 4 x 6.0G real dd writes with conv=fsync
cleanup: probe files and directory removed
SFT status after probe: not started yet
```

SFT launch:

```text
2026-05-21T08:27:52Z
tmux session: s22_sft_runtime
run_id: milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/logs/train_stdout_stderr.log
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
attempt count: 1 authorized SFT attempt started
```

SFT final observation:

```text
2026-05-21T08:29:06Z
tmux: done
exit_status: EXIT_STATUS=1, END_UTC=2026-05-21T08:27:52Z
GPU: all 8 H200 idle, 0% util, 1 MiB memory each
training processes: none observed
run log: only START_UTC line
run_manifest/config/checkpoint/trainer_state/all_results: absent
authorized same-node retry remaining: none
```

Stop proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
stop issued: 2026-05-21T08:29:55Z
post-stop terminal status first observed: 2026-05-21T08:30:36Z
final state: STOPPED (Completed)
completed timestamp: 2026-05-21 08:30:26
endpoint after stop: ssh -p 31346 root@10.100.16.69 refused connection
artifact preservation: /home/xu.yang/coding_agent_playground/outputs preserved on CephFS; shared mount path /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs remains visible
eval: not run
```

## Stop Conditions

```text
1. Complete checkpoint/model is produced and artifact presence is verified.
2. SFT fails and no PM-authorized retry remains.
3. Capacity probe fails before launch.
4. Node becomes unhealthy or endpoint disappears unexpectedly.
5. 15 minutes idle without active torchrun/python GPU work or fresh artifact progress after launch.
6. 60 minute max runtime unless PM records a bounded extension.
7. PM/test stop instruction.
```
