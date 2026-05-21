# dev_2 S23 Ceph-Fuse Fixed GPU Runtime Tracking

Task ID: `M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T13:26:28Z

Initial state: `LOCAL_BUNDLE_READY_PRE_SUBMIT`

```text
authorized allocation count: 1 fresh single-node 8 x H200
LTP frame: pending
endpoint: pending
node: pending
output root: /home/xu.yang/coding_agent_playground/outputs
remote network rule: no remote git clone/fetch/GitHub/source/dependency download
source commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
source bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
storage proof: pending
preflight: pending
conditional SFT: pending only if PASS and sft_allowed=true
eval: not authorized
```

Stop/release required after checkpoint/model success, exact blocker, preflight fail, SFT fail, idle/no-progress condition, or PM/test stop instruction.

## Final Tracking Record

Final state: `STOPPED_AFTER_PREFLIGHT_BLOCKER`

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z.yaml
submit result: HTTP 202
RUNNING observed: 2026-05-21T13:29:00Z
node: lg-cmc-b7r202-q03u26-h200-000730
endpoint: ssh -p 38862 root@10.100.22.36
output root: /home/xu.yang/coding_agent_playground/outputs
```

Runtime resource observations:

```text
ceph-fuse proof: /usr/bin/ceph-fuse; /mnt/cephfs FSTYPE fuse.ceph-fuse
/home/xu.yang output proof: /home/xu.yang/coding_agent_playground/outputs resolved on fuse.ceph-fuse
capacity proof: 24 GiB real-write probe PASS_AND_CLEANED under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z
GPU idle sample before preflight: all 8 NVIDIA H200 at 0% util, 1 MiB memory
source transfer: local bundle + dataset copied to CephFS staging and verified by sha256/file count
remote source network: no remote git clone/fetch/GitHub/source/dependency download was run
```

Preflight outcome:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
SFT_ALLOWED=false
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
exact blocker: structured parser found actionable GPU/NCCL health signature
representative parser matches: SXid 20009 records in dmesg_gpu_fault_scan.txt and NCCL_ASYNC_ERROR_HANDLING warning lines in torch_nccl_allreduce.log
SFT: not run because structured preflight did not PASS and sft_allowed was false
eval: not authorized and not run
```

Stop/release proof:

```text
stop timestamp UTC: 2026-05-21T13:39:17Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
stop result: HTTP 202, stop signal sent
post-stop state: STOPPED (Completed)
completed: 2026-05-21 13:39:48
endpoint proof: ssh -p 38862 root@10.100.22.36 refused connection after stop
no-active-Milestone-GPU proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
artifact preservation: outputs/logs/preflight/staging artifacts preserved under /home/xu.yang/coding_agent_playground/outputs
```

No active coding_agent_playground/Milestone 1 GPU allocation remains held by dev_2 for this task.
