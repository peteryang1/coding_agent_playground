# dev_2 S23 Ceph-Fuse Fixed Preflight + Conditional SFT Runtime

Task ID: `M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T13:26:28Z

Scope: PM-authorized exactly one fresh owner-executed LTP/GPU runtime attempt. Run ceph-fuse-fixed parser-patch preflight, then run one Qwen3-8B ShareGPT SFT smoke only if structured preflight is `PASS` and `sft_allowed=true`. No eval authorization.

## Authorization

```text
authorization file: evidence/pm_s23_cephfuse_preflight_sft_authorization.md
authorization durable commit: 641a1a5
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
PR #51 mergedAt: 2026-05-21T13:23:23Z
preferred source commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
fallback PR #51 head if merge commit unavailable: 972c91f7da4aa5b89877023fcff3b6c1d0b9fe9b
conditional SFT: only if structured preflight PASS and sft_allowed=true
eval authorized: false
remote network rule: no remote git clone/fetch/GitHub/source/dependency download on GPU node.
```

Gate basis read locally:

```text
dev_1 ceph-fuse resource review: PASS_FOR_PM_RETRY
test_1 ceph-fuse resource gate: PASS_FOR_PM_RETRY
dev_2 ceph-fuse resource plan: complete no-submit plan
dev_3 data/transfer staging: data-ready
test_2 eval readiness: eval blocked until checkpoint/model exists
```

## Local Source Preparation

The PR #51 merge commit was available locally in the dev_4 repository object database. The PM worktree had durable-file changes and was not used directly as the runtime source. I prepared a detached local worktree from the exact merge commit.

```text
source repository used for object: /work-agents/intern_code_dev_4/coding_agent_playground
local detached worktree: /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb
source commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
commit check: git rev-parse HEAD == c02a53a344f2ad7a33b04f529d5125677237d4cb
local worktree status: clean
file list: /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_file_list.txt
file list count: 106
bundle: /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb.tar.gz
bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
```

Critical file checksums:

```text
scripts/parse_s22_preflight_health.py sha256: 4bf4843adfee7f169ce9bcc99a2e67fd2cd149467a031cfa81d1b548da193084
scripts/train_qwen3_8b_sft.sh sha256: 9dd84e02bea54915a613159012b0981070ba03e5d3b9cbd8fcda1047957b3cc5
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml sha256: 6493c82d54025d9c7bf6f3afe6e37cb9ea4e5bfe850af9643411f6d6d2591614
scripts/write_sft_run_manifest.py sha256: f0f80d88452c26dc46866316b2946f419c5eabd6ab2b41ab2d7c9a4b394f997f
```

Dataset package prepared locally from prior dev_3 deterministic artifact recipe:

```text
local staged copy: /tmp/cleaned_m1_sft_10_sharegpt_s23_cephfuse_20260521T132628Z/train.jsonl
sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: messages[*].from/value, dataset_info coding_agent_m1_sft_10_sharegpt
```

## Runtime Status

Initial status: `LOCAL_BUNDLE_READY_PRE_SUBMIT`

```text
LTP submit: pending
endpoint: pending
node: pending
storage proof: pending
source/data transfer: pending
preflight: pending
SFT: pending, conditional only after PASS + sft_allowed=true
eval: not authorized and not run
```

## No-Remote-Network Contract

Future remote GPU-node actions for this runtime must not execute:

```text
git clone
git fetch
GitHub source download/fetch
remote project source/dependency download
remote pip install/download for project dependencies
```

Source and dataset must be transferred from the local/provided workspace by `scp`, `rsync`, or tar-over-SSH, then verified on the remote before preflight.

## Final Runtime Result

Final status: `BLOCKED_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT`

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
LTP submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z.yaml
LTP submit result: HTTP 202
LTP wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z --state RUNNING --timeout 1800 --interval 15
LTP RUNNING observed: 2026-05-21T13:29:00Z
node: lg-cmc-b7r202-q03u26-h200-000730
endpoint: ssh -p 38862 root@10.100.22.36
ports: ssh=38862, http=32216
state before stop: RUNNING
final state: STOPPED (Completed)
completed: 2026-05-21 13:39:48
endpoint after stop: ssh connect refused
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

The allocated node was a fresh different physical node relative to the prior failed nodes listed in the preflight gate:

```text
current node: lg-cmc-b7r202-q03u26-h200-000730
prior failed/avoid nodes: lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
different-node gate: PASS
```

## Storage, Image, and Capacity Proof

Remote checks on `ssh -p 38862 root@10.100.22.36`:

```text
checked UTC: 2026-05-21T13:35:17Z
hostname: lg-cmc-b7r202-q03u26-h200-000730
command -v ceph-fuse: /usr/bin/ceph-fuse
ceph-common: 19.2.3-0ubuntu0.24.04.3
ceph-fuse: 19.2.3-0ubuntu0.24.04.3
python3-ceph-common: 19.2.3-0ubuntu0.24.04.3
/mnt/cephfs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
/home/xu.yang/coding_agent_playground/outputs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
df -h /home/xu.yang/coding_agent_playground/outputs: 18P size, 1.8P used, 16P available, 10% used
GPU sample: 8 x NVIDIA H200, 0% util, 1 MiB memory used per GPU
```

Capacity probe:

```text
path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z
start UTC: 2026-05-21T13:32:26Z
probe: wrote 4 files x 6144 MiB, total 25,769,803,776 bytes
cleanup: probe files removed
status: PASS_AND_CLEANED
end UTC: 2026-05-21T13:32:47Z
```

The LTP image/bootstrap installed and proved `ceph-common`/`ceph-fuse`, then mounted `/mnt/cephfs` and exposed `/home/xu.yang` before any source transfer or preflight. The bootstrap used infrastructure package installation for OS storage tooling only; no project source/dependency clone/fetch/download was performed on the GPU node.

## Source and Data Transfer

Exact transfer/verification path:

```text
remote staging path: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging
remote repo path: /root/workspace/coding_agent_playground
remote data path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Commands used:

```bash
ssh -p 38862 root@10.100.22.36 "mkdir -p /root/workspace '/home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging' '/root/workspace/cleaned_m1_sft_10_sharegpt'"
scp -P 38862 /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb.tar.gz /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_remote_bundle.sha256 /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_file_list.txt /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_remote_critical_files.sha256 /tmp/cleaned_m1_sft_10_sharegpt_s23_cephfuse_20260521T132628Z/train.jsonl root@10.100.22.36:/home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging/
ssh -p 38862 root@10.100.22.36 "cp /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb.tar.gz /root/workspace/ && sha256sum -c /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_remote_bundle.sha256"
ssh -p 38862 root@10.100.22.36 "rm -rf /root/workspace/coding_agent_playground && mkdir -p /root/workspace/coding_agent_playground && tar -xzf /root/workspace/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb.tar.gz -C /root/workspace/coding_agent_playground"
ssh -p 38862 root@10.100.22.36 "cp /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging/train.jsonl /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl && sha256sum /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl"
ssh -p 38862 root@10.100.22.36 "cd /root/workspace/coding_agent_playground && sha256sum -c /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_remote_critical_files.sha256"
```

Transfer note: `scp` returned metadata/truncate permission warnings when preserving into the CephFS staging path, but the remote files were present and content verification passed. The warnings did not affect the verified bundle/data contents; CephFS generated-artifact paths were still used.

Verification results:

```text
/root/workspace/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb.tar.gz: OK
remote bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote file count: 106
remote file-list count: 106
scripts/parse_s22_preflight_health.py: OK
scripts/train_qwen3_8b_sft.sh: OK
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml: OK
scripts/write_sft_run_manifest.py: OK
PR51_MERGE_COMMIT.txt sha256: 8fee146576d6f8d1eba0021bfeedffb82cf4afeea35a881a58adf4a89f9860b7
```

No remote `git clone`, `git fetch`, GitHub source fetch, project source download, or project dependency download was run on the GPU node.

## Preflight

Preflight artifacts:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z
preflight runner: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/run_preflight.sh
health json: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/health_status.json
health text: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/health_status.txt
torch all-reduce log: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/torch_nccl_allreduce.log
parser exit: 2
preflight end UTC: 2026-05-21T13:38:51Z
```

Structured preflight output:

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
BLOCKED_PREFLIGHT_HEALTH_SIGNATURE
```

The structured parser found actionable health signatures and set `sft_allowed=false`. Representative actionable records in `health_status.json`:

```text
dmesg_gpu_fault_scan.txt line 446: SXid 20009, unknown_time, "Non-fatal, Link 57 RX Short Error Rate"
dmesg_gpu_fault_scan.txt line 447: SXid 20009, unknown_time, severity record for Engine instance 57
dmesg_gpu_fault_scan.txt line 448: SXid 20009, unknown_time, data payload record
torch_nccl_allreduce.log lines 5-22: NCCL_ASYNC_ERROR_HANDLING deprecation warnings were also classified by the current parser as nccl_or_collective_failure
```

The torch/NCCL functional all-reduce itself succeeded:

```text
TORCHRUN_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
```

Because the contract allowed SFT only when structured preflight was `PASS` and `sft_allowed=true`, no SFT was launched.

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
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
stop command timestamp UTC: 2026-05-21T13:39:17Z
stop result: HTTP 202, stop signal sent
post-stop wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z --state STOPPED --timeout 600 --interval 10
post-stop state: STOPPED (Completed)
completed: 2026-05-21 13:39:48
endpoint proof: ssh -p 38862 root@10.100.22.36 => connect to host 10.100.22.36 port 38862: Connection refused
no-running-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
artifact preservation: generated artifacts remain under /home/xu.yang/coding_agent_playground/outputs on CephFS
```

Final next fix recommendation: do not reuse this node for SFT. Review the structured parser findings and resource health signals before any future runtime authorization. If PM authorizes another attempt, require a fresh preferably different 8xH200 allocation, keep the no-remote-source/dependency-network rule, and preserve the local bundle/checksum transfer workflow.
