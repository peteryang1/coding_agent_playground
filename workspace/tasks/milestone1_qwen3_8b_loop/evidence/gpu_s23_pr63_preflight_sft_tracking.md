# dev_2 S23 PR63 GPU Runtime Tracking

Task ID: `M1-S23-PR63-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T18:12:07Z

## Allocation

```text
authorized allocation count: 1 fresh owner-executed runtime
planned LTP frame: xu.yang~coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z
planned submit yaml: /tmp/coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z.yaml
shape: single node, 8 x NVIDIA H200
output root: /home/xu.yang/coding_agent_playground/outputs
source commit: 7ad24ae328a350c0be596f41ea143affb4034486
source bundle sha256: 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
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
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z
endpoint: ssh -p 17408 root@10.100.18.14
node: lg-cmc-b7r202-k07u06-h200-000580
state before stop: RUNNING
CephFS/output root: PASS
capacity probe: PASS_AND_CLEANED, 25769803776 bytes
transfer verification: PASS
mcore_adapter import check: PASS
structured preflight: FAIL_HEALTH_SIGNATURE
SFT_ALLOWED: false
conditional SFT: not run
SFT skip reason: FAIL_HEALTH_SIGNATURE / actionable SXid 22013 in dmesg_gpu_fault_scan.txt
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized, not run
final blocker: BLOCKED_PR63_PREFLIGHT_HEALTH_SIGNATURE_SXID_22013
```

Stop/release required on source/data/dependency verification failure, storage/capacity failure, mcore import failure, structured preflight failure, `SFT_ALLOWED=false`, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Stop Proof

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z
stop response: status 202, Execute job successfully
final LTP state: STOPPED (Completed)
completed: 2026-05-21 18:26:03
endpoint proof: ssh -p 17408 root@10.100.18.14 refused connection
running coding-agent-playground jobs: No jobs found.
outputs preserved: /home/xu.yang/coding_agent_playground/outputs
active Milestone GPU held by dev_2: no
fresh authorization required before further LTP/GPU/preflight/SFT/eval: yes
```
