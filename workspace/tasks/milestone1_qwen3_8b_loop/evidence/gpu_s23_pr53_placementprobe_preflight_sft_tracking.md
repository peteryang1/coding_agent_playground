# dev_2 S23 PR53 Placement-Probe GPU Runtime Tracking

Task ID: `M1-S23-PR53-PLACEMENTPROBE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T14:23:58Z

Initial state: `LOCAL_PR53_BUNDLE_READY_PRE_SUBMIT`

```text
authorized allocation count: 1 fresh single-node 8 x H200
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
endpoint: pending
node: pending
forbidden nodes: lg-cmc-b7r202-q03u26-h200-000730, lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
source commit: e29c93736be3384663cad953cd18da68c30070fb
source bundle sha256: 34c5655cc8d7003ef3855b7ef5d285311794ab2fcad435dc4d52a3c80c10de77
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote network rule: no remote git clone/fetch/GitHub/source/dependency download
preflight: pending
conditional SFT: pending only if PASS and sft_allowed=true
eval: not authorized
```

Stop/release required on forbidden-node assignment, source/data verification fail, storage/capacity fail, preflight fail, `sft_allowed=false`, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Tracking Record

Final state: `STOPPED_AFTER_PR53_PREFLIGHT_BLOCKER`

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z.yaml
submit result: HTTP 202
RUNNING observed: 2026-05-21T14:25:55Z
endpoint: ssh -p 30073 root@10.100.24.12
assigned node: lg-cmc-b7r401-a05u06-h200-000770
forbidden-node gate: PASS_NON_FORBIDDEN
```

Runtime resource observations:

```text
ceph-fuse proof: /usr/bin/ceph-fuse; /mnt/cephfs FSTYPE fuse.ceph-fuse
/home/xu.yang output proof: /home/xu.yang/coding_agent_playground/outputs resolved on fuse.ceph-fuse
capacity proof: 24 GiB real-write probe PASS_AND_CLEANED under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z
GPU idle sample before/after preflight: all 8 NVIDIA H200 at 0% util, 1 MiB memory
source transfer: local PR #53 bundle + dataset copied and verified by sha256/file count
remote source network: no remote git clone/fetch/GitHub/source/dependency download was run
```

Preflight outcome:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
SFT_ALLOWED=false
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
exact blocker: PR53 structured parser still classified NCCL_ASYNC_ERROR_HANDLING deprecation warnings as nccl_or_collective_failure
SFT: not run because structured preflight did not PASS and sft_allowed was false
eval: not authorized and not run
```

Stop/release proof:

```text
stop timestamp UTC: 2026-05-21T14:30:11Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
stop result: HTTP 202, stop signal sent
post-stop state: STOPPED (Completed)
completed: 2026-05-21 14:30:42
endpoint proof: ssh -p 30073 root@10.100.24.12 refused connection after stop
no-active-Milestone-GPU proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
artifact preservation: outputs/logs/preflight/staging artifacts preserved under /home/xu.yang/coding_agent_playground/outputs
```

No active coding_agent_playground/Milestone 1 GPU allocation remains held by dev_2 for this task.
