# dev_2 S23 PR57 GPU Runtime Tracking

Task ID: `M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T15:52:00Z

Initial state: `LOCAL_PR57_BUNDLE_READY_PRE_SUBMIT`

```text
authorized allocation count: 1 fresh single-node 8 x H200
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
endpoint: pending
node: pending
output root: /home/xu.yang/coding_agent_playground/outputs
source commit: b4ac31ef1e3772953108348bf099818326ed65cc
source bundle sha256: 1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa
source file count: 122
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote network rule: no remote git clone/fetch/GitHub/source/dependency download for project code/dependencies
preflight: pending
conditional SFT: pending only if PREFLIGHT_RESULT=PASS and SFT_ALLOWED=true
eval: not authorized
```

Stop/release required on source/data verification failure, storage/capacity failure, preflight failure, `SFT_ALLOWED=false`, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Tracking Update

Final state: `STOPPED_AFTER_FINAL_RUNTIME_BLOCKER`

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
endpoint: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
submitted: 2026-05-21 15:55:39
started: 2026-05-21 15:55:45
preflight: PASS
sft_allowed: true
sft attempt count: 1 of 1 authorized
sft exit: EXIT_STATUS=1, END_UTC=2026-05-21T16:03:28Z
runtime blocker: ImportError: mcore_adapter is required when USE_MCA=1
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
```

Final remote artifact paths:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr57_preflight_sft_20260521T155200Z
train run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
checkpoint/output dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_stdout_stderr.log
xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_xtrace.log
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/run_manifest.json
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/config/qwen3_8b_sft.yaml
final summary: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/final_artifact_summary.txt
```

Last live-node sample before stop:

```text
sample time: 2026-05-21T16:05:21Z
process scan: no torchrun/llamafactory/launcher.py/train_qwen3_8b/python training process
gpu sample: all 8 NVIDIA H200 GPUs 0% util, 1 MiB used
```

Stop proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
stop response: HTTP 202, Execute job xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z successfully.
post-stop state: STOPPED (Completed)
completed: 2026-05-21 16:06:06
endpoint proof: ssh -p 22662 root@10.100.22.31 refused connection after stop
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
outputs preserved: /home/xu.yang/coding_agent_playground/outputs
```

No active Milestone GPU is held by dev_2 after this stop. Fresh PM authorization is required before any further LTP/GPU/preflight/SFT/eval work.
