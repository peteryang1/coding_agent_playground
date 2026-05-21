# dev_2 S23 PR59 GPU Runtime Tracking

Task ID: `M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T16:34:13Z

## Allocation

```text
authorized allocation count: 1 fresh owner-executed runtime
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
endpoint: ssh -p 27043 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
state: RUNNING
submitted: 2026-05-21 16:39:38
started: 2026-05-21 16:39:44
shape: single node, 8 x NVIDIA H200
output root: /home/xu.yang/coding_agent_playground/outputs
source commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
source bundle sha256: 2f272f210b67ed45b4a7b05592881c8c036fb34de2660645d6f96af76adf4d85
mcore_adapter bundle sha256: ec0ace00eeca1f4d60710deea59621c868860e34827a5b645122f64f043170e7
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download
eval: not authorized
```

Initial node observation:

```text
hostname: lg-cmc-b7r202-q05u06-h200-000722
GPU sample: all 8 NVIDIA H200 GPUs 0% util, 1 MiB used
```

## Final Gate State

```text
CephFS/output root: PASS after local mount/path repair using LTP bootstrap parameters
capacity probe: PASS_AND_CLEANED, 25769803776 bytes
source/data/mcore transfer: PASS
mcore_adapter import check: PASS
preflight: PASS
SFT_ALLOWED: true
conditional SFT: ran exactly once
SFT exit status: 127
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized, not run
final blocker: BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING
```

Stop/release required on source/data/dependency verification failure, storage/capacity failure, mcore import failure, structured preflight failure, `SFT_ALLOWED=false`, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Stop Proof

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
stop response: status 202, Execute job successfully
stop proof checked UTC: 2026-05-21T16:53:07Z
final LTP state: STOPPED (Completed)
completed: 2026-05-21 16:52:02
endpoint proof: ssh -p 27043 root@10.100.22.28 refused connection
running coding-agent-playground jobs: No jobs found.
outputs preserved: /home/xu.yang/coding_agent_playground/outputs
active Milestone GPU held by dev_2: no
fresh authorization required before further LTP/GPU/preflight/SFT/eval: yes
```
