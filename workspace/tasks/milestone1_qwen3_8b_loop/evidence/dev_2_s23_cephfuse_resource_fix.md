# dev_2 S23 Ceph-Fuse Resource Fix Plan

Task ID: `M1-S23-CEPHFUSE-RESOURCE-FIX-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T13:05:27Z

Scope: no-submit/no-runtime storage-bootstrap and resource fix plan for the failed Session 23 parser-patch runtime frame. This task does not authorize LTP submit, GPU use, NCCL/preflight, SFT, eval, dry-run, or remote GPU-node commands.

## Source Evidence Read

Local durable sources and read-only LTP status used:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_parserpatch_preflight_sft_runtime.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_parserpatch_preflight_sft_tracking.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
```

No LTP submit, GPU-node SSH, GPU command, NCCL/preflight, SFT, eval, or dry-run was run for this fix-plan task.

## Failed Frame Facts

```text
frame: xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
job: coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
node: lg-cmc-b7r202-q04u06-h200-000725
endpoint: ssh -p 36822 root@10.100.22.31
submitted: 2026-05-21 12:53:42
started: 2026-05-21 12:53:47
completed: 2026-05-21 12:53:50
final state: FAILED (Completed)
exit code: 220 Failed
origin user exit code: 127
endpoint proof from runtime evidence: ssh -p 36822 root@10.100.22.31 true => Connection refused
```

Exact ceph-fuse blocker log:

```text
/usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found
```

No-running-job proof:

```text
command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
result: No jobs found.
checked_utc: 2026-05-21T13:05:27Z
```

## Root Cause

The Session 23 LTP spec attempted to call `ceph-fuse` in the user command before ensuring the binary/package existed in the container. The container image did not provide `ceph-fuse`, so the task exited during bootstrap before the node became usable for local bundle transfer, `/home/xu.yang` proof, preflight, or SFT.

This was a resource/spec bootstrap blocker, not a parser-patch, data, checkpoint, model, or SFT blocker.

## Required Fix

Next PM-authorized runtime must use one of these storage-bootstrap fixes:

```text
Preferred fix: use the previously proven bootstrap sequence from successful S22/S21 specs:
  - install required OS packages from the internal cluster/local mirror before calling ceph-fuse;
  - include ceph-common and ceph-fuse before mount proof;
  - only then run ceph-fuse mount and /home/xu.yang symlink/proof.

Alternative fix: use an LTP image that already contains ceph-fuse and ceph-common, then prove the binary and mount before any source transfer.
```

The internal package/bootstrap commands are infrastructure-only. They must not fetch project source, GitHub content, Python dependencies, or training code. Remote GPU/LTP nodes remain no-external-network targets for project source/dependencies.

## Proposed LTP Spec Bootstrap

The next spec should restore package availability before mount:

```bash
export DEBIAN_FRONTEND=noninteractive
apt update -y
apt install -y ceph-common ceph-fuse rsync openssh-client tmux screen
command -v ceph-fuse
command -v rsync

export CEPH_USER="xu.yang"
mkdir -p /etc/ceph /mnt/cephfs /root/workspace
cat > "/etc/ceph/${CEPH_USER}.keyring" <<'EOF'
[client.xu.yang]
    key = <CEPHFS_KEY_FROM_LTP_PARAMETER>
EOF
chmod 600 "/etc/ceph/${CEPH_USER}.keyring"

if mountpoint -q /mnt/cephfs; then
  fstype="$(findmnt -n -o FSTYPE -T /mnt/cephfs 2>/dev/null || true)"
  if [ "${fstype}" != "fuse.ceph-fuse" ]; then
    umount -l /mnt/cephfs || true
    sleep 1
  fi
fi

if ! mountpoint -q /mnt/cephfs; then
  ceph-fuse -m 10.100.65.50,10.100.65.51,10.100.160.70 \
    /mnt/cephfs \
    --client_fs=mycephfs \
    --id "${CEPH_USER}" \
    --keyring "/etc/ceph/${CEPH_USER}.keyring" \
    --client_reconnect_stale=1
fi

findmnt -n -o FSTYPE,SOURCE -T /mnt/cephfs
test "$(findmnt -n -o FSTYPE -T /mnt/cephfs)" = "fuse.ceph-fuse"
mkdir -p "/mnt/cephfs/home/${CEPH_USER}/coding_agent_playground/outputs"
if [ ! -e "/home/${CEPH_USER}" ]; then
  mkdir -p /home
  ln -s "/mnt/cephfs/home/${CEPH_USER}" "/home/${CEPH_USER}"
fi
mkdir -p "/home/${CEPH_USER}/coding_agent_playground/outputs"
findmnt -T "/home/${CEPH_USER}/coding_agent_playground/outputs"
df -h "/home/${CEPH_USER}/coding_agent_playground/outputs"
```

If `/mnt/3fs` is required for the existing read-only base model path, the spec may use the already proven internal 3FS bootstrap commands. This remains an existing required input/storage mount, not a project source/dependency fetch.

## `/home/xu.yang` Verification Plan

Before any source transfer or preflight:

```bash
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
RUN_ID=<PM_AUTHORIZED_RUN_ID>
PROBE_DIR="${OUTPUT_ROOT}/capacity_probes/${RUN_ID}"
mkdir -p "${PROBE_DIR}"
findmnt -T "${OUTPUT_ROOT}"
df -h "${OUTPUT_ROOT}"
python3 - <<'PY'
from pathlib import Path
root = Path("/home/xu.yang/coding_agent_playground/outputs/capacity_probes/<PM_AUTHORIZED_RUN_ID>")
root.mkdir(parents=True, exist_ok=True)
payload = b"0" * (1024 * 1024)
for idx in range(64):
    (root / f"probe_{idx:03d}.bin").write_bytes(payload)
print(sum(p.stat().st_size for p in root.glob("probe_*.bin")))
for p in root.glob("probe_*.bin"):
    p.unlink()
PY
```

For full SFT readiness, reuse the prior 24GiB probe size if PM/test requires it. The key acceptance condition is a real-write probe under `/home/xu.yang/coding_agent_playground/outputs`, followed by cleanup and logged byte count.

## No-Remote-Source-Network Rule

Future runtime must keep the Session 23 rule:

```text
no remote git clone
no remote git fetch
no remote GitHub download/fetch
no remote pip install/download for source/dependencies
no external source/dependency fetch on the GPU/LTP node
```

Allowed future transfer method:

```text
prepare exact code/config/scripts locally/provided workspace;
verify commit, file list, bundle sha256, and critical-file checksums locally;
transfer bundle/dataset/checksum sidecars by tar-over-SSH, scp, or rsync;
verify sha256/file list on remote after transfer;
record exact transfer commands and destination paths in runtime evidence.
```

Reuse local bundle contract from failed runtime:

```text
source commit: 2de4bab2248f052d09f118eb6c28c48231f3d719
source bundle sha256: 13521a43bf64690b5cb3aefb8830316a799f2f079a35b17554379c99231988c8
file list count: 105
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

If source files change after this task, regenerate and record new checksums before any transfer.

## Next Runtime Gate

Next runtime remains unauthorized until PM explicitly re-authorizes after dev_1/test_1 review of this resource fix plan.

Required next authorization inputs:

```text
dev_1 review of ceph-fuse resource fix: PASS_FOR_PM_RETRY or exact blocker
test_1 gate of ceph-fuse resource fix: PASS_FOR_PM_RETRY or exact blocker
PM explicit runtime authorization naming dev_2 owner and exactly one fresh allocation/run
confirmed LTP spec/image includes ceph-fuse before use or otherwise proves ceph-fuse availability
confirmed no-remote-source-network transfer plan
```

## No-Submit Boundary

```text
No LTP submit was run for this task.
No GPU command was run for this task.
No preflight was run for this task.
No SFT was run for this task.
No eval was run for this task.
No dry-run was run for this task.
```

## Completion Marker

`M1-S23-CEPHFUSE-RESOURCE-FIX-DEV2` is complete as a no-submit resource/spec fix plan. Runtime remains blocked until PM gates dev_1/test_1 review and issues fresh runtime authorization.
