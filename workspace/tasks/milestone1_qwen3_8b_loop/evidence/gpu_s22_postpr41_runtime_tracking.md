# GPU Resource Tracking - S22 Post-PR41 Runtime

Task ID: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T10:06:34Z

Scope:

```text
Exactly one post-PR41 ShareGPT Qwen3-8B SFT smoke attempt.
Stop/release after checkpoint/model, failure, failed capacity probe, idle/health limit, or PM/test stop.
No eval.
Durable files only; no peer_send PM.
```

Required output root:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Pre-submit readiness refresh for `M1-S22-DATASET-MAP-RESOURCE-DEV2`:

```text
prior post-PR39 frame: xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z
prior frame status: STOPPED (Completed)
prior endpoint: ssh -p 38445 root@10.100.24.11 refused connection after stop
active Milestone GPU held by dev_2 before this authorized post-PR41 submit: none
future command/output/log/checkpoint/run metadata/intermediates root: /home/xu.yang/coding_agent_playground/outputs
fresh authorization inputs now present: PR #41 owner-merged at 2026-05-21T10:00:25Z merge commit 2fc4b797a85c9375c6c5e1171963abe67aab35e8; dev_1/test_1 PASS_FOR_PM_RETRY; dev_3 no data content/schema change; PM authorization for exactly one owner run.
```

## Resource State

Submitted/running:

```text
frame: xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z
job: coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z
submitted: 2026-05-21 10:07:19
started: 2026-05-21 10:07:22
state: RUNNING (AttemptRunning)
endpoint: ssh -p 27021 root@10.100.22.14
hostname: lg-cmc-b7r202-p07u16-h200-000708
```

Submit command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z.yaml
```

Bootstrap observation:

```text
2026-05-21T10:07:38Z
LTP container is RUNNING but still in apt/bootstrap.
GPU: all 8 H200 idle.
SFT: not started.
```

Node/storage proof:

```text
2026-05-21T10:09:12Z
hostname: lg-cmc-b7r202-p07u16-h200-000708
endpoint: ssh -p 27021 root@10.100.22.14
CephFS: /home/xu.yang resolves to /mnt/cephfs/home/xu.yang; findmnt shows /mnt/cephfs fuse.ceph-fuse ceph-fuse
output root: /home/xu.yang/coding_agent_playground/outputs
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB used each before launch
```

Capacity probe:

```text
2026-05-21T10:09:12Z to 2026-05-21T10:09:40Z
path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
result: PASS_AND_CLEANED
bytes written: 25769803776
files: 4 x 6.0G real dd writes with conv=fsync
cleanup: probe files and directory removed
SFT status after probe: not started yet
```

SFT launch:

```text
2026-05-21T10:14:23Z
tmux session: s22_postpr41_sft
run_id: milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
run_dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
attempt count: 1 authorized SFT attempt started
```

Active-training observation:

```text
2026-05-21T10:14:46Z
torchrun/python/llamafactory processes active across 8 ranks
GPU memory nonzero on all 8 H200 GPUs
runtime config and run manifest prove PR41 single-process preprocessing: preprocessing_num_workers null
eval: not run
```

SFT final observation:

```text
2026-05-21T10:17:13Z
tmux/training: done
exit_status: EXIT_STATUS=1, END_UTC=2026-05-21T10:16:21Z
training processes: none observed
GPU: all 8 H200 idle, 0% util, 1 MiB memory each
checkpoint/model/trainer_state/all_results: absent
failure: CUDA/NCCL `Invalid access of peer GPU memory over nvlink or a hardware error`; torch elastic local_rank 5 exitcode -6 / SIGABRT
authorized same-node retry remaining: none
```

Stop proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z
stop issued: 2026-05-21T10:17:27Z
post-stop terminal status observed: 2026-05-21T10:18:19Z
final state: STOPPED (Completed)
completed timestamp: 2026-05-21 10:17:58
endpoint after stop: ssh -p 27021 root@10.100.22.14 refused connection
artifact preservation: /home/xu.yang/coding_agent_playground/outputs preserved on CephFS; shared mount path /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs remains visible
eval: not run
```

No-active-Milestone-GPU proof after stop:

```text
2026-05-21T10:18:20Z
fresh RUNNING list for h200agentic/h200 shows only unrelated `ltp-axis-eval-platform-*` allocations.
No active coding_agent_playground / Milestone 1 / S22 post-PR41 GPU is held by intern_code_dev_2.
Future resource work requires fresh PM authorization after new dev_4/dev_3/dev_1/test_1 gates.
```
