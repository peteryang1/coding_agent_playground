# dev_2 S23 PR55 Resource Recovery

Task ID: `M1-S23-PR55-RESOURCE-RECOVERY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T15:30:29Z

Scope: no-submit recovery/readiness record after the stopped PR55 runtime. This task does not authorize LTP submit, GPU use, preflight, SFT, eval, or dry-run.

## Control-Plane Proof

Checked commands:

```text
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
```

Result:

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
state: STOPPED (Completed)
exec type: STOP
submitted: 2026-05-21 14:54:36
started: 2026-05-21 14:54:40
completed: 2026-05-21 15:09:43
task role state: STOPPED
endpoint while active: ssh -p 15535 root@10.100.22.28
node while active: lg-cmc-b7r202-q05u06-h200-000722
post-stop endpoint proof: refused connection at 2026-05-21T15:10:02Z per runtime evidence
running coding-agent-playground jobs: No jobs found.
```

Conclusion: dev_2 holds no active coding_agent_playground/Milestone 1 GPU allocation for PR55.

## Final PR55 Runtime Summary

Durable source evidence:

```text
runtime evidence: evidence/dev_2_s23_pr55_preflight_sft_runtime.md
GPU tracking: evidence/gpu_s23_pr55_preflight_sft_tracking.md
authorization evidence: evidence/pm_s23_pr55_preflight_sft_authorization.md
```

PR55 source/data provenance:

```text
PR #55 merge commit: 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
local source repository used: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr55_20260521T145240Z_1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
source bundle: /tmp/cap_s23_pr55_20260521T145240Z_1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703.tar.gz
source bundle sha256: db82b9162af2c37d670e568e16002cfc595e9090d578121545827622c3141df7
file list count: 118
dataset source: /tmp/cleaned_m1_sft_10_sharegpt_s23_pr55_20260521T145240Z/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset row count: 10
dataset schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

Runtime facts:

```text
active endpoint: ssh -p 15535 root@10.100.22.28
assigned node: lg-cmc-b7r202-q05u06-h200-000722
forbidden-node gate: PASS, node was not forbidden
output root: /home/xu.yang/coding_agent_playground/outputs
storage proof: /home/xu.yang/coding_agent_playground/outputs on fuse.ceph-fuse
capacity probe: PASS_AND_CLEANED, wrote/removed 25769803776 bytes
remote source/data transfer: local/provided bundle and data only
remote source/dependency network: no remote git clone/fetch/GitHub/source/dependency download
```

Preflight result:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
```

SFT result:

```text
SFT attempt count: exactly one
SFT run id: milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
SFT started: 2026-05-21T15:08:24Z
SFT exit status: EXIT_STATUS=1
SFT ended: 2026-05-21T15:08:25Z
blocker: environment: DEP_TARGET: unbound variable
blocker class: launch-wrapper environment variable bug before GPU training
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
```

Artifact roots preserved:

```text
source/data staging: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z/staging
preflight artifacts: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
SFT run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
capacity probe: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
```

## Recovery / Readiness Statement

No new LTP/GPU/preflight/SFT/eval/dry-run is authorized from this recovery task. Future runtime work requires a fresh PM task and explicit PM authorization after the appropriate owner/test gates.

If a future PM-authorized retry occurs, the known next fix is to avoid an exported bash function that references non-exported local variables. Use an executable wrapper in a chmod-capable local path with explicit environment values, or export `DEP_TARGET`/`LF` before invoking `scripts/train_qwen3_8b_sft.sh`. If any wrapper or generated helper must live outside `/home/xu.yang/coding_agent_playground/outputs` because CephFS rejects `chmod`, record that as a justified exception in runtime evidence.

Final recovery status: `COMPLETE_NO_SUBMIT_RECOVERY_READY_FOR_FRESH_PM_GATE`.
