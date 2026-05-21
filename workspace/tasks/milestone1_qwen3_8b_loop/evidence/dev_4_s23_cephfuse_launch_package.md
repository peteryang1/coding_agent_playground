# M1-S23-CEPHFUSE-LAUNCH-PACKAGE-DEV4

Owner: `intern_code_dev_4`

Date: `2026-05-21`

Scope: no-execution launch/spec package to avoid `ceph-fuse: command not found` and keep all generated SFT artifacts under `/home/xu.yang/coding_agent_playground/outputs`.

Runtime boundary: no LTP/GPU/preflight/SFT/eval command was run.

## Decision

The SFT launch package should not invoke `ceph-fuse` from dev_4's training launcher. CephFS mounting is a resource/bootstrap responsibility owned before handoff. The dev_4 launcher should only verify that `/home/xu.yang/coding_agent_playground/outputs` is already backed by the expected CephFS path or a valid `/home/xu.yang` mount, verify writability/capacity, and block before SFT if the mount is absent.

This avoids both known failure classes:

```text
ceph-fuse: command not found
fuse: unknown option(s): `-o nonempty'
```

## Prior Successful Patterns

Observed successful or accepted `/home/xu.yang` patterns in existing evidence:

```text
PR #39 diagnostics:
  output root: /home/xu.yang/coding_agent_playground/outputs
  artifacts: preflight.json, generated config, run_manifest.json, logs, xtrace, diagnostics, exit_status

Session 22 storage rule:
  all generated SFT/eval intermediates default under /home/xu.yang
  /mnt/3fs is allowed only for existing required inputs/audit paths with explicit justification

Parser/storage fix:
  raw root accepted: /home/xu.yang/coding_agent_playground/outputs
  resolved CephFS mirror accepted: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs

Historical resource evidence:
  /mnt/cephfs reported as fuse.ceph-fuse on successful resource routes
```

Relevant contrast:

```text
compute_gpu_route_decision.md:
  one h200agentic attempt failed because the worker template used ceph-fuse -o nonempty
  the approved route removed -o nonempty
```

## Required Handoff Contract

Before any future SFT launch is PM-authorized, the resource owner must provide durable evidence that the allocated node already has:

```text
repo: /root/workspace/coding_agent_playground
data: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset name: coding_agent_m1_sft_10_sharegpt
output root: /home/xu.yang/coding_agent_playground/outputs
resolved output root: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs or equivalent valid /home-backed CephFS path
nodes json: /root/workspace/coding_agent_playground/nodes.json
no remote GitHub/source/dependency network required during launch
```

If `/home/xu.yang/coding_agent_playground/outputs` is missing, not writable, not capacity-verified, or resolves outside the accepted CephFS/home roots, the SFT launch must stop before invoking LLamaFactory.

## No-Network Bundle Rule

Future runtime must not fetch source or dependencies from GitHub or external package indexes on the GPU node. Use local, checksum-recorded bundle transfer only.

Recommended local bundle staging pattern for the resource owner:

```bash
# Source side: final controlled workspace or PM-approved staging host.
cd /root/workspace
tar --sort=name --mtime='UTC 2026-05-21' --owner=0 --group=0 --numeric-owner \
  -cf /tmp/coding_agent_playground_runtime_bundle.tar \
  coding_agent_playground cleaned_m1_sft_10_sharegpt
sha256sum /tmp/coding_agent_playground_runtime_bundle.tar

# Transfer side: scp/rsync over the approved private endpoint only.
scp -P <PORT> /tmp/coding_agent_playground_runtime_bundle.tar root@<GPU_IP>:/root/workspace/

# GPU side: verify checksum before extraction.
cd /root/workspace
sha256sum -c coding_agent_playground_runtime_bundle.tar.sha256
tar -xf coding_agent_playground_runtime_bundle.tar
```

For dependency archives/wheels, use the same rule: local path, checksum, transfer, verify, install from local bundle only. `/mnt/3fs` remains allowed only for existing required base-model/dependency input paths already justified by prior evidence.

## Mount And Output Verification Package

These checks are for a future PM-authorized run package. They were not run in this session.

```bash
set -euo pipefail

OUT=/home/xu.yang/coding_agent_playground/outputs
EXPECTED_RESOLVED=/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs

command -v ceph-fuse >/dev/null 2>&1 && echo "ceph_fuse_binary_present" || echo "ceph_fuse_binary_absent_ok_not_used_by_dev4"

test -d /home/xu.yang || { echo "BLOCKER_HOME_XU_YANG_MISSING"; exit 20; }
mkdir -p "${OUT}" || { echo "BLOCKER_OUTPUT_ROOT_MKDIR_FAILED"; exit 21; }
test -w "${OUT}" || { echo "BLOCKER_OUTPUT_ROOT_NOT_WRITABLE"; exit 22; }

RAW_OUT="${OUT}"
RESOLVED_OUT="$(readlink -f "${OUT}")"
printf 'RAW_OUT=%s\nRESOLVED_OUT=%s\n' "${RAW_OUT}" "${RESOLVED_OUT}"

case "${RESOLVED_OUT}" in
  "${OUT}"|/home/xu.yang/coding_agent_playground/outputs|/home/xu.yang/coding_agent_playground/outputs/*)
    echo "OUTPUT_ROOT_OK_RAW_HOME"
    ;;
  "${EXPECTED_RESOLVED}"|"${EXPECTED_RESOLVED}"/*)
    echo "OUTPUT_ROOT_OK_CEPHFS_RESOLVED"
    ;;
  *)
    echo "BLOCKER_OUTPUT_ROOT_RESOLVES_OUTSIDE_ACCEPTED_HOME_CEPHFS"
    exit 23
    ;;
esac

findmnt -T /home/xu.yang || true
findmnt -T "${OUT}" || true
df -h /home/xu.yang "${OUT}"
df -i /home/xu.yang "${OUT}" || true
```

Capacity probe policy before PM authorizes SFT:

```text
Run a bounded real-write probe under:
  /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>

Minimum acceptable proof:
  24 GiB write+sync+delete probe for the tiny max_steps=2 SFT smoke.

Stronger proof if PM/test require:
  48 GiB write+sync+delete probe, still under /home/xu.yang, not /mnt/3fs.
```

## Future SFT Launch Command Skeleton

This is a no-execution command skeleton. Do not run until PM authorizes runtime.

```bash
cd /root/workspace/coding_agent_playground

RUN_ID=milestone1_qwen3_8b_s23_cephfuse_safe_sharegpt_tp8_maxsteps2_$(date -u +%Y%m%dT%H%M%SZ)

BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml \
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs \
RUN_ID="${RUN_ID}" \
PREPROCESSING_NUM_WORKERS=null \
DRY_RUN=0 \
SFT_XTRACE=1 \
bash /root/workspace/coding_agent_playground/scripts/train_qwen3_8b_sft.sh
```

Expected generated paths:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/preflight.json
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/run_manifest.json
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_xtrace.log
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/early_exit_diagnostics.txt
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/exit_status.txt
/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>
/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
```

## Blockers For PM Gate

Runtime is blocked until PM separately authorizes it and resource/test gates provide:

```text
1. Fresh endpoint and nodes.json for a node with mounted /home/xu.yang output path.
2. Durable mount proof showing /home/xu.yang/coding_agent_playground/outputs writable and resolving to accepted CephFS/home root.
3. Durable capacity proof under /home/xu.yang/coding_agent_playground/outputs.
4. Bundle checksum proof for repo/data/dependencies, with no remote GitHub/source/dependency network on the GPU node.
5. dev_1/test_1 review of this package if PM requires a retry gate.
```

## Completion Status

```yaml
task_id: M1-S23-CEPHFUSE-LAUNCH-PACKAGE-DEV4
owner: intern_code_dev_4
result: READY_FOR_PM_REVIEW
evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_cephfuse_launch_package.md
code_changes_required: false
config_changes_required: false
spec_package_only: true
runtime_authorized: false
ltp_gpu_preflight_sft_eval_executed_by_dev4: false
```
