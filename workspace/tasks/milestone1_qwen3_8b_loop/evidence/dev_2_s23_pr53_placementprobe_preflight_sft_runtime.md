# dev_2 S23 PR53 Placement-Probe Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PR53-PLACEMENTPROBE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T14:23:58Z

Scope: PM-authorized exactly one bounded placement-probe single-node 8 x H200 LTP runtime using PR #53 merge commit `e29c93736be3384663cad953cd18da68c30070fb`. Immediately check hostname before transfer. If assigned to a forbidden node, stop/release before transfer/preflight/SFT/eval. If non-forbidden, use `/home/xu.yang/coding_agent_playground/outputs`, transfer local bundle/data, run structured preflight, and run SFT only if preflight `PASS` and `sft_allowed=true`. Eval is not authorized.

## Authorization / Hard Gates

```text
authorization file: evidence/pm_s23_pr53_placement_probe_preflight_sft_authorization.md
authorization time: 2026-05-21T14:24:00Z
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
source commit: e29c93736be3384663cad953cd18da68c30070fb
forbidden nodes: lg-cmc-b7r202-q03u26-h200-000730, lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
remote network rule: no remote git clone/fetch/GitHub/source/dependency download
eval authorized: false
```

## Local Source/Data Preparation

PR #53 merge commit was available locally in `/work-agents/intern_code_dev_4/coding_agent_playground`; no network fetch was used. I created a detached local worktree and run-specific source bundle.

```text
source repository: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb
commit: e29c93736be3384663cad953cd18da68c30070fb
worktree status: clean
file list: /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_file_list.txt
file list count: 111
bundle: /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb.tar.gz
bundle sha256: 34c5655cc8d7003ef3855b7ef5d285311794ab2fcad435dc4d52a3c80c10de77
remote bundle sha file: /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_remote_bundle.sha256
critical checksum file: /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_remote_critical_files.sha256
```

Critical file checksums:

```text
scripts/parse_s22_preflight_health.py sha256: b90ead39614dd127e9a27de3433a648acbf37bcd9f008637bfb43ccb5aad9a69
tests/test_parse_s22_preflight_health.py sha256: b51d669732bcce41c7db0d6e37255ea806d622aa41904cc4118f50791138faa1
scripts/train_qwen3_8b_sft.sh sha256: 9dd84e02bea54915a613159012b0981070ba03e5d3b9cbd8fcda1047957b3cc5
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml sha256: 6493c82d54025d9c7bf6f3afe6e37cb9ea4e5bfe850af9643411f6d6d2591614
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml sha256: b841ff72532eb30d9fd2cabfde4b5f119ddb2679694b3b231e8facf016f8b465
scripts/write_sft_run_manifest.py sha256: f0f80d88452c26dc46866316b2946f419c5eabd6ab2b41ab2d7c9a4b394f997f
```

Dataset:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_s23_pr53_placementprobe_20260521T142358Z/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

## LTP Submit Plan

```text
run id: milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z
LTP yaml: /tmp/coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z.yaml
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
shape: single node, 8 x H200, h200agentic virtual cluster
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z.yaml
status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
```

Initial status: `LOCAL_PR53_BUNDLE_READY_PRE_SUBMIT`

## Final Runtime Result

Final status: `BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT`

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z.yaml
submit result: HTTP 202
RUNNING observed: 2026-05-21T14:25:55Z
endpoint: ssh -p 30073 root@10.100.24.12
assigned node: lg-cmc-b7r401-a05u06-h200-000770
forbidden-node gate: PASS_NON_FORBIDDEN
forbidden nodes: lg-cmc-b7r202-q03u26-h200-000730, lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
```

The assigned node was not in the forbidden list, so the runtime proceeded to storage proof, transfer, and structured preflight. SFT was not run because structured preflight returned `FAIL_HEALTH_SIGNATURE` and `sft_allowed=false`.

## Node / Storage / Capacity Proof

Hostname check before transfer:

```text
command: ssh -p 30073 root@10.100.24.12 'hostname'
checked UTC: 2026-05-21T14:26:02Z
hostname: lg-cmc-b7r401-a05u06-h200-000770
node decision: PASS_NON_FORBIDDEN
```

Bootstrap/storage proof:

```text
bootstrap ready UTC: 2026-05-21T14:27:18Z
command -v ceph-fuse: /usr/bin/ceph-fuse
/mnt/cephfs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
/home/xu.yang/coding_agent_playground/outputs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
df -h /home/xu.yang/coding_agent_playground/outputs: 18P size, 1.8P used, 16P available, 10% used
GPU sample: 8 x NVIDIA H200, 0% util, 1 MiB memory used per GPU
```

Capacity probe:

```text
path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z
start UTC: 2026-05-21T14:27:36Z
probe: wrote 4 files x 6144 MiB, total 25,769,803,776 bytes
cleanup: probe files removed
status: PASS_AND_CLEANED
end UTC: 2026-05-21T14:27:58Z
```

## Source/Data Transfer and Verification

Remote paths:

```text
remote staging path: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z/staging
remote repo path: /root/workspace/coding_agent_playground
remote data path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Commands used:

```bash
ssh -p 30073 root@10.100.24.12 "mkdir -p /root/workspace '/home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z/staging' '/root/workspace/cleaned_m1_sft_10_sharegpt'"
scp -P 30073 /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb.tar.gz /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_remote_bundle.sha256 /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_file_list.txt /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_remote_critical_files.sha256 /tmp/cleaned_m1_sft_10_sharegpt_s23_pr53_placementprobe_20260521T142358Z/train.jsonl root@10.100.24.12:/root/workspace/
ssh -p 30073 root@10.100.24.12 "cp /root/workspace/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb.tar.gz /root/workspace/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_remote_bundle.sha256 /root/workspace/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_file_list.txt /root/workspace/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_remote_critical_files.sha256 /root/workspace/train.jsonl /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z/staging/"
ssh -p 30073 root@10.100.24.12 "sha256sum -c /root/workspace/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_remote_bundle.sha256"
ssh -p 30073 root@10.100.24.12 "rm -rf /root/workspace/coding_agent_playground && mkdir -p /root/workspace/coding_agent_playground && tar -xzf /root/workspace/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb.tar.gz -C /root/workspace/coding_agent_playground"
ssh -p 30073 root@10.100.24.12 "cp /root/workspace/train.jsonl /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl && sha256sum /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl"
ssh -p 30073 root@10.100.24.12 "cd /root/workspace/coding_agent_playground && sha256sum -c /root/workspace/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_remote_critical_files.sha256"
```

Verification results:

```text
/root/workspace/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb.tar.gz: OK
remote bundle sha256: 34c5655cc8d7003ef3855b7ef5d285311794ab2fcad435dc4d52a3c80c10de77
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote file count: 111
remote file-list count: 111
scripts/parse_s22_preflight_health.py: OK
tests/test_parse_s22_preflight_health.py: OK
scripts/train_qwen3_8b_sft.sh: OK
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml: OK
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml: OK
scripts/write_sft_run_manifest.py: OK
PR53_MERGE_COMMIT.txt sha256: f9dbe2f962964575266d1cdae75d8a8c93d4ec92abfdd129219b3f0a80728c21
```

No remote `git clone`, `git fetch`, GitHub/source fetch, remote source download, or project dependency download was run on the GPU node.

## Structured Preflight

Preflight artifacts:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z
preflight runner: /root/workspace/run_pr53_preflight.sh
health json: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z/health_status.json
health text: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z/health_status.txt
torch all-reduce log: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z/torch_nccl_allreduce.log
parser exit: 2
preflight end UTC: 2026-05-21T14:29:42Z
```

Structured output:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE
ACTIONABLE_FAULT=true
SFT_ALLOWED=false
SFT_ALLOWED_IF_PM_AUTHORIZED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=actionable GPU/NCCL health signature found
```

Exact blocker:

```text
BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE
```

The PR #53 parser still reported actionable faults from `torch_nccl_allreduce.log` NCCL async deprecation warnings:

```text
fault_count: 8
representative match: torch_nccl_allreduce.log line 5, "Warning: Environment variable NCCL_ASYNC_ERROR_HANDLING is deprecated; use TORCH_NCCL_ASYNC_ERROR_HANDLING instead"
```

The functional torch/NCCL all-reduce passed:

```text
TORCHRUN_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
```

Because structured preflight did not pass and `sft_allowed=false`, SFT was not run.

## SFT / Checkpoint / Eval

```text
SFT command: not run
reason SFT not run: structured preflight FAIL_HEALTH_SIGNATURE and sft_allowed=false
checkpoint/model: absent; SFT was not run
trainer_state.json: absent; SFT was not run
all_results.json: absent; SFT was not run
eval: not authorized and not run
```

## Stop Proof

```text
stop timestamp UTC: 2026-05-21T14:30:11Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
stop result: HTTP 202, stop signal sent
post-stop wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z --state STOPPED --timeout 600 --interval 10
post-stop state: STOPPED (Completed)
completed: 2026-05-21 14:30:42
endpoint proof: ssh -p 30073 root@10.100.24.12 => connect to host 10.100.24.12 port 30073: Connection refused
no-running-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
artifact preservation: generated artifacts remain under /home/xu.yang/coding_agent_playground/outputs on CephFS
```

Final next fix recommendation: PR #53 did not clear the current structured preflight blocker in runtime; the parser still blocks on NCCL async deprecation warnings even though torch all-reduce exits 0. Future work should fix the parser/rule or preflight env contract so `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings are non-actionable before another SFT runtime is authorized.
