# dev_2 S23 PR61 GPU Runtime Tracking

Task ID: `M1-S23-PR61-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T17:15:51Z

## Allocation

```text
authorized allocation count: 1 fresh owner-executed runtime
planned LTP frame: xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
planned submit yaml: /tmp/coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z.yaml
shape: single node, 8 x NVIDIA H200
output root: /home/xu.yang/coding_agent_playground/outputs
source commit: 713862da983f73b165af1cfe27935ccef616a049
source bundle sha256: a8aeb73d6f3c69775997b7c4b6cf49344a0e8691a44811b68d5678caaacb83c4
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download
eval: not authorized
```

## Final Gate State

```text
no active coding-agent-playground LTP job before submit: yes
source/data/mcore local package: ready
LTP submit: done
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
endpoint: ssh -p 33089 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
state before stop: RUNNING
CephFS/output root: PASS after mount/path repair using LTP bootstrap parameters
capacity probe: PASS_AND_CLEANED, 25769803776 bytes
transfer verification: PASS
mcore_adapter import check: PASS
structured preflight: PASS
SFT_ALLOWED: true
conditional SFT: ran exactly once
SFT exit status: 1
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized, not run
final blocker: BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE
```

Stop/release required on source/data/dependency verification failure, storage/capacity failure, mcore import failure, structured preflight failure, `SFT_ALLOWED=false`, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Stop Proof

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
stop response: status 202, Execute job successfully
final LTP state: STOPPED (Completed)
completed: 2026-05-21 17:32:52
endpoint proof: ssh -p 33089 root@10.100.22.31 refused connection
running coding-agent-playground jobs: No jobs found.
outputs preserved: /home/xu.yang/coding_agent_playground/outputs
active Milestone GPU held by dev_2: no
fresh authorization required before further LTP/GPU/preflight/SFT/eval: yes
```
