# dev_2 S23 PR53 Resource Recovery / Readiness

Task ID: `M1-S23-PR53-RESOURCE-RECOVERY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T14:34:00Z

Scope: no-submit/no-runtime recovery evidence after the stopped PR53 placement-probe runtime. This task does not authorize a new LTP allocation, GPU command, preflight, SFT, eval, dry-run, endpoint connection, or remote mutation.

## Read-Only Control-Plane Checks

Commands checked:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
```

Current proof:

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
state: STOPPED (Completed)
submitted: 2026-05-21 14:25:40
started: 2026-05-21 14:25:46
completed: 2026-05-21 14:30:42
endpoint while allocated: ssh -p 30073 root@10.100.24.12
node: lg-cmc-b7r401-a05u06-h200-000770
post-stop endpoint proof from runtime evidence: connection refused
running coding-agent-playground jobs: No jobs found
```

Conclusion: no active coding_agent_playground/Milestone 1 GPU job is held by dev_2 for this runtime.

## Final Runtime Blocker Summary

Final runtime evidence:

```text
evidence/dev_2_s23_pr53_placementprobe_preflight_sft_runtime.md
evidence/gpu_s23_pr53_placementprobe_preflight_sft_tracking.md
```

Final status:

```text
BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT
```

Placement/resource status:

```text
assigned node: lg-cmc-b7r401-a05u06-h200-000770
forbidden-node gate: PASS_NON_FORBIDDEN
forbidden nodes: lg-cmc-b7r202-q03u26-h200-000730, lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
ceph-fuse/home output proof: PASS
capacity probe: PASS_AND_CLEANED, 25,769,803,776 bytes written and removed
source/data transfer: PASS, checksums and file count verified
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

Important nuance: placement and storage were good, and the 8-rank torch/NCCL all-reduce completed successfully with `TORCHRUN_EXIT=0` and `ALLREDUCE_OK world_size=8 value=36.0`. The PR53 structured parser still blocked SFT by classifying `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings in `torch_nccl_allreduce.log` as actionable `nccl_or_collective_failure`.

Representative blocker detail:

```text
fault_count: 8
representative match: torch_nccl_allreduce.log line 5, "Warning: Environment variable NCCL_ASYNC_ERROR_HANDLING is deprecated; use TORCH_NCCL_ASYNC_ERROR_HANDLING instead"
```

Per PM authorization, SFT was allowed only if structured preflight was `PASS` and `sft_allowed=true`; therefore SFT was not run. There is no checkpoint/model, `trainer_state.json`, `all_results.json`, or eval output from this runtime.

## Preserved Provenance for Future Work

Source package:

```text
PR #53 merge commit: e29c93736be3384663cad953cd18da68c30070fb
source repository used locally: /work-agents/intern_code_dev_4/coding_agent_playground
detached local worktree: /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb
local file list: /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb_file_list.txt
file count: 111
local bundle: /tmp/cap_s23_pr53_placementprobe_20260521T142358Z_e29c93736be3384663cad953cd18da68c30070fb.tar.gz
bundle sha256: 34c5655cc8d7003ef3855b7ef5d285311794ab2fcad435dc4d52a3c80c10de77
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
remote runtime dataset path during stopped allocation: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry name: coding_agent_m1_sft_10_sharegpt
```

Remote generated artifacts from the stopped runtime were preserved under:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z
/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z
/home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z
```

No remote `git clone`, `git fetch`, GitHub/source fetch, remote source download, or project dependency download was used on the GPU node. Future runtime work must preserve the local/provided bundle plus checksum transfer workflow and `/home/xu.yang/coding_agent_playground/outputs` generated-artifact root.

## Recovery Recommendation

No fresh runtime is authorized by this recovery task. The current blocker is not placement or storage; it is the PR53 structured preflight parser/rule still treating NCCL async deprecation warnings as actionable despite successful all-reduce. Recommended next work before any further SFT authorization:

```text
fix or re-gate the parser/preflight environment contract so NCCL_ASYNC_ERROR_HANDLING deprecation warnings are non-actionable only when torch all-reduce exits 0 and ALLREDUCE_OK is present;
preserve real NCCL/CUDA/Xid/SXid/ECC/NVLink failures as actionable;
dev_1/test_1 should review the corrected parser or runtime preflight evidence before PM authorizes another GPU attempt;
if PM authorizes a future runtime, require fresh single-node 8 x H200 allocation, immediate forbidden-node gate, /home/xu.yang capacity proof, local bundle/data transfer verification, structured preflight PASS plus sft_allowed=true before SFT, and final stop proof.
```

## Boundary

For `M1-S23-PR53-RESOURCE-RECOVERY-DEV2`, I did not submit LTP, occupy a GPU, connect to the stopped GPU endpoint, run preflight, run SFT, run eval, run dry-run, or mutate remote state. I only read existing durable evidence and local/control-plane LTP status/list output, then wrote this recovery/readiness record and status.

No new LTP/GPU/preflight/SFT/eval may run without fresh PM authorization.
