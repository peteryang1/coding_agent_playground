# dev_2 S23 PR63 Alternate-Node GPU Runtime Tracking

Task ID: `M1-S23-PR63-ALTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T18:12:07Z

## Allocation

```text
authorized allocation count: 1 fresh bounded alternate-node attempt
planned LTP frame: xu.yang~coding-agent-playground-m1-s23-pr63-altnode-preflight-sft-20260521T181207Z
planned submit yaml: /tmp/coding-agent-playground-m1-s23-pr63-altnode-preflight-sft-20260521T181207Z.yaml
forbidden nodes:
- lg-cmc-b7r202-k07u06-h200-000580
- lg-cmc-b7r202-q04u06-h200-000725
shape: single node, 8 x NVIDIA H200
output root: /home/xu.yang/coding_agent_playground/outputs
source commit: 7ad24ae328a350c0be596f41ea143affb4034486
source bundle sha256: 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download
eval: not authorized
```

## Initial Gate State

```text
no active coding-agent-playground LTP job before submit: yes
source/data/mcore local package: ready
LTP submit: pending
placement decision: pending
CephFS/output root: pending if node is non-forbidden
capacity probe: pending if node is non-forbidden
transfer verification: pending if node is non-forbidden
mcore_adapter import check: pending if node is non-forbidden
structured preflight: pending if node is non-forbidden
conditional SFT: pending; may run only if non-forbidden node, transfer/import/preflight PASS, and SFT_ALLOWED=true
```

Stop/release required immediately if a forbidden node is assigned; otherwise on source/data/dependency verification failure, storage/capacity failure, mcore import failure, structured preflight failure, `SFT_ALLOWED=false`, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Tracking Update

```text
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr63-altnode-preflight-sft-20260521T181207Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr63-altnode-preflight-sft-20260521T181207Z
submitted: 2026-05-21 18:52:17
started: 2026-05-21 18:52:22
endpoint: ssh -p 31316 root@10.100.18.14
assigned node: lg-cmc-b7r202-k07u06-h200-000580
forbidden node matched: yes, lg-cmc-b7r202-k07u06-h200-000580
placement decision: FAIL_FORBIDDEN_NODE
```

Gate outcomes:

```text
remote hostname/GPU probe: completed only to identify forbidden placement
transfer/checksum verification: not run
no remote source/dependency network: preserved
/home/xu.yang capacity probe: not run
mcore_adapter import for USE_MCA=1: not run
structured preflight: not run
conditional SFT: not run
eval: not run, not authorized
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
```

Stop/release proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr63-altnode-preflight-sft-20260521T181207Z
stop result: HTTP 202 accepted
final state: STOPPED (Completed)
completed: 2026-05-21 18:53:18
endpoint post-stop: ssh -p 31316 root@10.100.18.14 hostname -> Connection refused
running job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground -> No jobs found.
```

Final state: `STOPPED_RELEASED_BLOCKED_PLACEMENT_FORBIDDEN_NODE`. Fresh PM authorization is required before any further LTP/GPU/preflight/SFT/eval work.
