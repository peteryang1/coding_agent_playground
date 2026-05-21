# dev_2 S23 PR63 Different-Node GPU Runtime Tracking

Task ID: `M1-S23-PR63-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T18:12:07Z

## Allocation

```text
authorized allocation count: 1 fresh bounded different-node attempt
planned LTP frame: xu.yang~coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z
planned submit yaml: /tmp/coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z.yaml
forbidden node: lg-cmc-b7r202-k07u06-h200-000580
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

Stop/release required immediately if forbidden node is assigned; otherwise on source/data/dependency verification failure, storage/capacity failure, mcore import failure, structured preflight failure, `SFT_ALLOWED=false`, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Tracking Update

```text
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z
submitted: 2026-05-21 18:34:04
started: 2026-05-21 18:34:09
endpoint: ssh -p 27957 root@10.100.22.31
assigned node: lg-cmc-b7r202-q04u06-h200-000725
forbidden node: lg-cmc-b7r202-k07u06-h200-000580
placement decision: PASS, non-forbidden node
```

Storage/capacity:

```text
output root: /home/xu.yang/coding_agent_playground/outputs
resolved root after bootstrap: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs
mount: /mnt/cephfs source ceph-fuse fstype fuse.ceph-fuse
df: 18P size, 16P available
capacity probe: PASS_AND_CLEANED, 25769803776 bytes written/verified under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr63_differentnode_preflight_sft_20260521T181207Z
```

Gate outcomes:

```text
transfer/checksum verification: PASS
no remote source/dependency network: PASS
mcore_adapter import for USE_MCA=1: PASS
structured preflight: PASS
PREFLIGHT_RESULT=PASS
SFT_ALLOWED=true
torch NCCL all-reduce exit: 0
conditional SFT launched: yes, exactly one attempt
eval: not run, not authorized
```

SFT outcome:

```text
run id: milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z
exit status: 1
failure class: BLOCKED_PR63_DIFFERENTNODE_RUNTIME_NCCL_NVLINK_PEER_MEMORY
failure signature: CUDA error: Invalid access of peer GPU memory over nvlink or a hardware error
torch elastic root cause: rank 4 local_rank 4 SIGABRT
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
```

Stop/release proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z
stop command time: 2026-05-21T18:42:50Z
stop result: HTTP 202 accepted
final state: STOPPED (Completed)
completed: 2026-05-21 18:43:25
endpoint post-stop: ssh -p 27957 root@10.100.22.31 hostname -> Connection refused
running job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground -> No jobs found.
artifact preservation: outputs/logs/preflight/run metadata/checkpoint directory remain under /home/xu.yang/coding_agent_playground/outputs
```

Final state: `STOPPED_RELEASED_BLOCKED_WITH_FINAL_RUNTIME_EVIDENCE`. Fresh PM authorization is required before any further LTP/GPU/preflight/SFT/eval work.
