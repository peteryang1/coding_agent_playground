# dev_2 S23 Ceph-Fuse Runtime Recovery / Readiness

Task ID: `M1-S23-CEPHFUSE-RESOURCE-RECOVERY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T13:47:00Z

Scope: no-submit/no-runtime recovery evidence after the stopped ceph-fuse fixed preflight runtime. This task does not authorize a new LTP allocation, GPU command, NCCL/preflight, SFT, eval, dry-run, or endpoint mutation.

## Read-Only Control-Plane Checks

Commands checked from local/control plane only:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
```

Current proof:

```text
frame: xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
state: STOPPED (Completed)
submitted: 2026-05-21 13:28:52
started: 2026-05-21 13:28:55
completed: 2026-05-21 13:39:48
node: lg-cmc-b7r202-q03u26-h200-000730
endpoint while allocated: ssh -p 38862 root@10.100.22.36
post-stop endpoint proof from runtime evidence: connection refused
running coding-agent-playground jobs: No jobs found
```

Conclusion: no active coding_agent_playground/Milestone 1 GPU job is held by dev_2 for this runtime.

## Final Runtime Blocker Summary

Final runtime evidence:

```text
evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md
evidence/gpu_s23_cephfuse_preflight_sft_tracking.md
```

Final status:

```text
BLOCKED_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT
```

Structured preflight result:

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
```

Important nuance: the functional 8-rank torch/NCCL all-reduce completed successfully with `TORCHRUN_EXIT=0` and `ALLREDUCE_OK world_size=8 value=36.0`, but the structured parser still blocked SFT because it classified GPU/NCCL health signatures as actionable. Representative parser matches were:

```text
dmesg_gpu_fault_scan.txt: SXid 20009 records, unknown_time, link RX short error rate
torch_nccl_allreduce.log: NCCL_ASYNC_ERROR_HANDLING deprecation warning lines classified by current parser as nccl_or_collective_failure
```

Per PM authorization, SFT was allowed only if structured preflight was `PASS` and `sft_allowed=true`; therefore SFT was not run. There is no checkpoint/model, `trainer_state.json`, `all_results.json`, or eval output from this runtime.

## Preserved Provenance for Future Retry

Source commit/package:

```text
PR #51 merge commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
local source object/worktree source: /work-agents/intern_code_dev_4/coding_agent_playground
detached local worktree: /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb
local file list: /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_file_list.txt
file count: 106
local bundle: /tmp/cap_s23_cephfuse_20260521T132628Z_c02a53a344f2ad7a33b04f529d5125677237d4cb.tar.gz
bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
```

Critical file checksums from the staged package:

```text
scripts/parse_s22_preflight_health.py sha256: 4bf4843adfee7f169ce9bcc99a2e67fd2cd149467a031cfa81d1b548da193084
scripts/train_qwen3_8b_sft.sh sha256: 9dd84e02bea54915a613159012b0981070ba03e5d3b9cbd8fcda1047957b3cc5
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml sha256: 6493c82d54025d9c7bf6f3afe6e37cb9ea4e5bfe850af9643411f6d6d2591614
scripts/write_sft_run_manifest.py sha256: f0f80d88452c26dc46866316b2946f419c5eabd6ab2b41ab2d7c9a4b394f997f
```

Dataset:

```text
local staged dataset: /tmp/cleaned_m1_sft_10_sharegpt_s23_cephfuse_20260521T132628Z/train.jsonl
remote runtime dataset path during stopped allocation: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry name: coding_agent_m1_sft_10_sharegpt
```

Remote generated artifacts from the stopped runtime were preserved under:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z
/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z
/home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z
```

Future runtime rule: remote GPU/LTP nodes must continue to be treated as no-external-network targets. Do not run remote `git clone`, `git fetch`, GitHub/source download, or remote project dependency download. Prepare source/config/scripts/data locally or in a provided workspace, verify commit/file list/checksums locally, transfer by scp/rsync/tar-over-SSH, and verify after transfer before any preflight.

## Future Retry Readiness / Stop Conditions

No fresh runtime is authorized by this recovery task. If PM later authorizes another attempt, recommended readiness criteria are:

```text
fresh PM authorization naming owner/task/evidence paths
fresh preferably different single-node 8 x H200 allocation
avoid reusing lg-cmc-b7r202-q03u26-h200-000730 until PM reviews the health-signature blocker
all generated outputs/logs/tmp/preflight/checkpoints/run metadata under /home/xu.yang/coding_agent_playground/outputs
ceph-fuse and /home/xu.yang mount/write/capacity proof before preflight
local bundle/data transfer with sha256/file-count verification before preflight
structured preflight must report PASS and sft_allowed=true before any SFT
no eval unless separately authorized
```

Stop conditions for any future PM-authorized retry:

```text
preflight fails or sft_allowed=false
same-node/resource-health blocker is detected before SFT
/home/xu.yang mount/write/capacity proof fails
source/data transfer or checksum verification fails
SFT completes successfully with checkpoint/model and required trainer artifacts
SFT fails with a fresh exact runtime blocker
node becomes unhealthy or endpoint unavailable
idle/no-progress limit specified by PM/runtime owner is reached
PM/test stop instruction is received
```

## Boundary

For `M1-S23-CEPHFUSE-RESOURCE-RECOVERY-DEV2`, I did not submit LTP, occupy a GPU, connect to the stopped GPU endpoint, run preflight, run SFT, run eval, or mutate remote state. I only read existing durable evidence and local/control-plane LTP status/list output, then wrote this recovery/readiness record and status.

No new LTP/GPU/preflight/SFT/eval may run without fresh PM authorization.
