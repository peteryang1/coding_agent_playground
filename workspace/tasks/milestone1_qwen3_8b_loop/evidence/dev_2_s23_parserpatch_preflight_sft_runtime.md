# dev_2 S23 Parser-Patch Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PARSERPATCH-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T12:47:36Z

Scope: PM-authorized one fresh preferably different-node single-node 8 x H200 LTP allocation; run PR #49 parser-patch preflight; run exactly one Qwen3-8B ShareGPT SFT smoke only if structured preflight is `PASS` and `sft_allowed=true`. No eval authorization.

## Authorization

```text
authorization file: evidence/pm_s23_parserpatch_preflight_sft_authorization.md
authorization timestamp: 2026-05-21T12:45:00Z
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
PR #49 mergedAt: 2026-05-21T12:44:14Z
PR #49 merge commit: 2de4bab2248f052d09f118eb6c28c48231f3d719
conditional SFT: only if structured preflight PASS and sft_allowed=true
eval authorized: false
remote network rule: GPU/LTP node is treated as no external network; no remote git clone/fetch/download/pip/GitHub source/dependency fetch.
```

Gate basis read locally:

```text
dev_1 review: evidence/dev_1_s23_parserpatch_review.md => PASS_FOR_PM_RETRY
test_1 gate: evidence/test_1_s23_parserpatch_gate.md => PASS_FOR_PM_RETRY
dev_2 readiness: evidence/dev_2_s23_parserpatch_runtime_ready.md => complete no-submit readiness
dev_3 data staging: evidence/dev_3_s23_parserpatch_data_staging.md => data-ready, no data-side blocker
test_2 eval readiness: evidence/test_2_s23_parserpatch_eval_ready.md => eval-ready but blocked until model/checkpoint
```

## Local Source Preparation

Shared PM worktree was not used as the source bundle because it was not at PR #49 merge commit and had unrelated durable-file changes. Exact PR #49 commit was available in the dev_4 local repository object database, so I prepared a detached local worktree from that commit.

```text
source repository used for object: /work-agents/intern_code_dev_4/coding_agent_playground
local detached worktree: /tmp/cap_s23_parserpatch_20260521T124736Z_2de4bab2248f052d09f118eb6c28c48231f3d719
source commit: 2de4bab2248f052d09f118eb6c28c48231f3d719
commit check: git rev-parse HEAD == 2de4bab2248f052d09f118eb6c28c48231f3d719
local worktree status: clean
file list: /tmp/cap_s23_parserpatch_20260521T124736Z_2de4bab2248f052d09f118eb6c28c48231f3d719_file_list.txt
file list count: 105
bundle: /tmp/cap_s23_parserpatch_20260521T124736Z_2de4bab2248f052d09f118eb6c28c48231f3d719.tar.gz
bundle sha256: 13521a43bf64690b5cb3aefb8830316a799f2f079a35b17554379c99231988c8
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
accepted source artifact path in contract: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
prepared local staged copy: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
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
preflight: pending
SFT: pending, conditional only after PASS + sft_allowed=true
eval: not authorized and not run
```

## LTP Submit / Allocation Attempt

Submit:

```text
ltp_yaml: /tmp/coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z.yaml
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z.yaml
submit result: status 202, Update job coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z for user xu.yang successfully.
frame: xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
```

LTP spec source/dependency network boundary:

```text
remote git clone/fetch: not present in spec and not run
remote GitHub source download: not present in spec and not run
remote pip install/download: not present in spec and not run
remote project source/dependency fetch: not present in spec and not run
remote bootstrap note: spec attempted only infra/storage setup needed for CephFS/3FS; source code and dataset were prepared locally for tar/scp transfer, but transfer never occurred because the job failed before a usable running endpoint.
```

Wait/status:

```text
wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z --state RUNNING --timeout 1800 --interval 15
wait observation: 2026-05-21T12:53:53Z FAILED
status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
state: FAILED (Completed)
submitted: 2026-05-21 12:53:42
started: 2026-05-21 12:53:47
completed: 2026-05-21 12:53:50
exit_code: 220 Failed
task ip/port: ssh -p 36822 root@10.100.22.31
node from events: lg-cmc-b7r202-q04u06-h200-000725
```

Different-node observation:

```text
prior parser-fixed failed node: lg-cmc-b7r202-p07u16-h200-000708
prior NCCL/preflight node to avoid if possible: lg-cmc-b7r401-a04u26-h200-000769
allocated node from events: lg-cmc-b7r202-q04u06-h200-000725
different-node result: PASS_DIFFERENT_FROM_PRIOR_BLOCKED_NODES
```

## Final Runtime Outcome

Status: `BLOCKED_LTP_BOOTSTRAP_CEPH_FUSE_MISSING_NO_PREFLIGHT_NO_SFT`

The single PM-authorized fresh allocation failed during LTP bootstrap before a usable running endpoint was available for transfer, preflight, or SFT.

Failure evidence:

```text
logs command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py logs --stream all xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
pai termination exitCode: 220
originUserExitCode: 127
matchedUserLogString: command not found
stderr/user log: /usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found
root cause: LTP image/spec lacked ceph-fuse at bootstrap, so /home/xu.yang/CephFS output root could not be mounted/proved.
```

Artifacts and run state:

```text
remote source transfer: not performed because job never reached usable RUNNING endpoint.
remote post-transfer verification: not performed because source transfer did not occur.
preflight: not run.
health_status.json/txt: absent because preflight did not run.
capacity/topology/NVLink/NCCL all-reduce: not run.
conditional SFT: not run because preflight did not run and sft_allowed was never true.
checkpoint/model: absent.
trainer_state.json: absent.
all_results.json: absent.
eval: not authorized and not run.
```

No-remote-network proof for this attempt:

```text
No remote git clone/fetch was run.
No remote GitHub fetch/download was run.
No remote pip install/download was run.
No source/dependency transfer from external network was run.
Local exact PR #49 bundle and dataset were prepared and checksummed, but not transferred because the LTP job failed before a usable endpoint.
```

Stop/release proof:

```text
stop/release action timestamp UTC: 2026-05-21T12:54:40Z
stop command attempted: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
stop command result: HTTP 500 Unexpected end of JSON input because the frame was already terminal Completed.
post-stop status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
post-stop terminal state: FAILED (Completed)
endpoint proof command: ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 36822 root@10.100.22.31 true
endpoint proof result: Connection refused
running coding-agent-playground jobs check: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
running coding-agent-playground jobs result: No jobs found.
artifact preservation: no remote generated artifacts exist because bootstrap failed before transfer/preflight/SFT; local bundle, file list, checksums, and prepared dataset remain under /tmp paths listed above.
```

Next fix recommendation:

```text
Do not submit another runtime without fresh PM authorization.
For the next resource spec, either restore the proven storage bootstrap that installs ceph-fuse from the internal cluster package path before use, or use an LTP image/spec where ceph-fuse is already available. Keep the no-remote-source-network rule: still no remote git clone/fetch, pip install/download, GitHub fetch, or external source/dependency download. If internal storage-bootstrap commands are required, record them explicitly as infrastructure-only and not source/dependency retrieval.
```

## No-Remote-Network Contract

Future remote actions for this run must not execute:

```text
git clone
git fetch
pip install/download
GitHub download/fetch
external network source/dependency fetch
```

Allowed transfer method for source code/dataset is local-to-remote tar/scp/SSH only. Any internal storage-mount bootstrap needed for `/mnt/3fs` or CephFS must be recorded separately and must not fetch project source or Python dependencies from external network.

## Stop Conditions

```text
allocation lands on a PM-rejected node;
source/dataset transfer or checksum verification fails;
remote staging would require git/pip/GitHub/download;
/home/xu.yang/coding_agent_playground/outputs path proof fails;
capacity probe fails;
parser health_status.json/txt missing, malformed, or not PASS;
sft_allowed is not true;
fresh/current or timestamp-unknown Xid/SXid/ECC/NVLink/NCCL fault is detected;
torch NCCL all-reduce fails or hangs;
conditional SFT succeeds and writes checkpoint/model plus trainer_state/all_results;
conditional SFT fails with no PM-authorized retry;
node becomes unhealthy or idle without progress;
PM/test stop instruction;
bounded runtime reached.
```
