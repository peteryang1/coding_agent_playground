# GPU Resource Tracking - S22 Post-PR39 Runtime

Task ID: `M1-S22-POSTPATCH-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T09:24:00Z

Scope:

```text
Exactly one post-PR39 ShareGPT-fixed Qwen3-8B SFT smoke attempt.
Stop/release after checkpoint/model, failure, failed capacity probe, idle/health limit, or PM/test stop.
No eval.
Durable files only; no peer_send PM.
```

Required output root:

```text
/home/xu.yang/coding_agent_playground/outputs
```

## Resource State

Submitted/running:

```text
frame: xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z
job: coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z
submitted: 2026-05-21 09:24:58
started: 2026-05-21 09:25:02
state: RUNNING (AttemptRunning)
endpoint: ssh -p 38445 root@10.100.24.11
```

Submit command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z.yaml
```

Node/storage proof:

```text
2026-05-21T09:28:11Z
hostname: lg-cmc-b7r401-a04u26-h200-000769
endpoint: ssh -p 38445 root@10.100.24.11
CephFS: /home/xu.yang resolves to /mnt/cephfs/home/xu.yang; findmnt shows /mnt/cephfs fuse.ceph-fuse ceph-fuse
output root: /home/xu.yang/coding_agent_playground/outputs
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB memory each
```

Capacity probe:

```text
2026-05-21T09:28:25Z to 2026-05-21T09:28:54Z
path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
result: PASS_AND_CLEANED
bytes written: 25769803776
files: 4 x 6.0G real dd writes with conv=fsync
cleanup: probe files and directory removed
SFT status after probe: not started yet
```

SFT launch:

```text
2026-05-21T09:31:23Z
tmux session: s22_postpatch_sft
run_id: milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
run_dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
attempt count: 1 authorized SFT attempt started
```

SFT final observation:

```text
2026-05-21T09:33:10Z
tmux: done
exit_status: EXIT_STATUS=1, END_UTC=2026-05-21T09:32:16Z
training processes: none observed
GPU: all 8 H200 idle, 0% util, 1 MiB memory each
checkpoint/model/trainer_state/all_results: absent
failure: dataset conversion multiprocessing EOFError before training/checkpoint save
authorized same-node retry remaining: none
```

Stop proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z
stop issued: 2026-05-21T09:33:26Z
post-stop terminal status first observed: 2026-05-21T09:34:08Z
final state: STOPPED (Completed)
completed timestamp: 2026-05-21 09:33:57
endpoint after stop: ssh -p 38445 root@10.100.24.11 refused connection
artifact preservation: /home/xu.yang/coding_agent_playground/outputs preserved on CephFS; shared mount path /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs remains visible
eval: not run
```

## PM Follow-Up Resource Closure

Task: `M1-S22-DATASET-MAP-RESOURCE-DEV2`

Updated: 2026-05-21T09:41:58Z

Execution boundary for this follow-up:

```text
ltp_submit_performed: false
gpu_occupied: false
sft_run: false
eval_run: false
```

Fresh LTP status command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z
```

Fresh LTP status result:

```text
State: STOPPED (Completed)
ExecType: STOP
Submitted: 2026-05-21 09:24:58
Started: 2026-05-21 09:25:02
Completed: 2026-05-21 09:33:57
task idx 0: STOPPED
```

Endpoint proof:

```text
ssh -p 38445 root@10.100.24.11 refused connection after STOPPED state.
The endpoint is no longer usable and no active resource is held by this frame.
```

Fresh no-active-Milestone-GPU proof commands:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 100 --json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 100 --json
```

Visible RUNNING H200/H200-agentic jobs:

```text
h200agentic:
  xu.yang~ltp-axis-eval-platform-a71e4142, 8 GPUs, RUNNING
h200:
  xu.yang~ltp-axis-eval-platform-6493743e, 8 GPUs, RUNNING
  xu.yang~ltp-axis-eval-platform-2de3c892, 8 GPUs, RUNNING
```

Conclusion:

```text
No active coding_agent_playground / Milestone 1 / S22 runtime GPU is held by intern_code_dev_2.
Visible RUNNING H200 jobs are unrelated ltp-axis-eval-platform allocations and must not be reused, modified, or stopped for this task.
Any future resource work requires fresh PM authorization after dev_4, dev_3, dev_1, and test_1 gates complete for the dataset-map EOF blocker.
```
