# dev_2 S23 Ceph-Fuse GPU Resource Plan

Task ID: `M1-S23-CEPHFUSE-RESOURCE-FIX-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T13:05:27Z

Scope: no-submit/no-runtime resource plan for the next possible parser-patch runtime after ceph-fuse bootstrap failure.

## Current Resource State

Failed frame:

```text
frame: xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
state: FAILED (Completed)
node: lg-cmc-b7r202-q04u06-h200-000725
endpoint: ssh -p 36822 root@10.100.22.31
completed: 2026-05-21 12:53:50
exit_code: 220 Failed
failure: /usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found
endpoint after terminal state: Connection refused
```

No-running-job proof:

```text
command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
result: No jobs found.
checked_utc: 2026-05-21T13:05:27Z
```

## Proposed Future Resource Shape

Only after fresh PM authorization:

```text
virtual cluster: h200agentic or PM-approved equivalent
node shape: single node
gpu shape: 8 x NVIDIA H200
allocation: fresh
node preference: preferably different from prior blocked nodes when scheduler allows
avoid/prefer-different if possible:
  - lg-cmc-b7r202-p07u16-h200-000708
  - lg-cmc-b7r401-a04u26-h200-000769
  - lg-cmc-b7r202-q04u06-h200-000725
```

## Required Storage Bootstrap Fix

The next LTP spec/image must prove `ceph-fuse` before invoking it:

```bash
apt update -y
apt install -y ceph-common ceph-fuse rsync openssh-client tmux screen
command -v ceph-fuse
ceph-fuse --version || true
```

Then mount/prove `/home/xu.yang`:

```bash
ceph-fuse -m 10.100.65.50,10.100.65.51,10.100.160.70 /mnt/cephfs \
  --client_fs=mycephfs \
  --id xu.yang \
  --keyring /etc/ceph/xu.yang.keyring \
  --client_reconnect_stale=1
test "$(findmnt -n -o FSTYPE -T /mnt/cephfs)" = "fuse.ceph-fuse"
mkdir -p /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs
test -e /home/xu.yang || ln -s /mnt/cephfs/home/xu.yang /home/xu.yang
findmnt -T /home/xu.yang/coding_agent_playground/outputs
df -h /home/xu.yang/coding_agent_playground/outputs
```

Acceptance criteria before any parser preflight:

```text
ceph-fuse binary present
/mnt/cephfs mounted as fuse.ceph-fuse
/home/xu.yang resolves to CephFS-backed home
/home/xu.yang/coding_agent_playground/outputs exists
real-write capacity probe under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID> passes and cleans
```

## Transfer / Checksum Plan

Remote GPU/LTP nodes must remain no-external-network for project source and dependencies.

Future runtime should use:

```text
local source commit: 2de4bab2248f052d09f118eb6c28c48231f3d719 unless a newer PM-authorized commit is named
local bundle: /tmp/cap_s23_parserpatch_20260521T124736Z_2de4bab2248f052d09f118eb6c28c48231f3d719.tar.gz
local bundle sha256: 13521a43bf64690b5cb3aefb8830316a799f2f079a35b17554379c99231988c8
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
transfer: tar-over-SSH, scp, or rsync from local/provided workspace to future endpoint
remote code destination: /root/workspace/coding_agent_playground
remote staging evidence: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/staging
```

Required transfer evidence:

```text
exact command used
source path
destination path
endpoint host/port
source commit
file list
bundle sha256
critical file sha256s
dataset sha256
post-transfer sha256 verification output
statement that no remote git/pip/GitHub/download source/dependency fetch occurred
```

## Stop Conditions

Future allocation must be stopped/released if:

```text
ceph-fuse is still missing after bootstrap
/mnt/cephfs cannot mount as fuse.ceph-fuse
/home/xu.yang/coding_agent_playground/outputs proof fails
capacity probe fails or cannot clean
source/dataset transfer or checksum verification fails
remote staging would require git/fetch/pip/download/GitHub
parser preflight is missing/malformed/not PASS
sft_allowed is not true
fresh/current or timestamp-unknown Xid/SXid/ECC/NVLink/NCCL fault appears
torch NCCL all-reduce fails or hangs
conditional SFT fails with no authorized same-node retry
conditional SFT succeeds and checkpoint/model/trainer_state/all_results are captured
node is unhealthy or idle without progress
PM/test stop instruction arrives
bounded runtime expires
```

Required stop proof:

```text
LTP stop command/action
UTC stop timestamp
post-stop terminal state
endpoint refusal or equivalent unreachable proof
artifact preservation note under /home/xu.yang/coding_agent_playground/outputs
```

## No-Submit Boundary

```text
No LTP submit was run for this plan.
No GPU command was run for this plan.
No preflight/SFT/eval/dry-run was run for this plan.
Next runtime remains unauthorized until PM gates dev_1/test_1 review and explicitly authorizes dev_2.
```
