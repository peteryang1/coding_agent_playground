# dev_2 S23 Parser-Patch GPU Resource Tracking

Task ID: `M1-S23-PARSERPATCH-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T12:47:36Z

Initial state: `LOCAL_BUNDLE_READY_PRE_SUBMIT`

```text
authorized allocation count: 1 fresh preferably different-node single-node 8 x H200
LTP frame: pending
endpoint: pending
node: pending
output root: /home/xu.yang/coding_agent_playground/outputs
remote network rule: no remote git clone/fetch/download/pip/GitHub source/dependency fetch
source commit: 2de4bab2248f052d09f118eb6c28c48231f3d719
source bundle sha256: 13521a43bf64690b5cb3aefb8830316a799f2f079a35b17554379c99231988c8
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
preflight: pending
conditional SFT: pending only if PASS and sft_allowed=true
eval: not authorized
```

Stop/release required after checkpoint, blocker, final failure, unhealthy/idle condition, PM/test stop order, or bounded runtime.

## Final Tracking Update

Outcome: `FAILED_COMPLETED_BOOTSTRAP_NO_GPU_RUNTIME`

```text
frame: xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z.yaml
submit result: status 202
wait result: FAILED at 2026-05-21T12:53:53Z
LTP state: FAILED (Completed)
submitted: 2026-05-21 12:53:42
started: 2026-05-21 12:53:47
completed: 2026-05-21 12:53:50
exit_code: 220 Failed
node from events: lg-cmc-b7r202-q04u06-h200-000725
endpoint: ssh -p 36822 root@10.100.22.31
```

Failure:

```text
termination log: originUserExitCode=127, command not found
exact log: /usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found
resource effect: job failed before usable RUNNING endpoint, so no code transfer, no preflight, no SFT, no eval, and no generated remote artifacts.
```

Release/stop proof:

```text
stop attempted UTC: 2026-05-21T12:54:40Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
stop result: HTTP 500 Unexpected end of JSON input because frame was already terminal Completed
post-stop state: FAILED (Completed)
endpoint proof: ssh -p 36822 root@10.100.22.31 true => Connection refused
running coding-agent-playground jobs: No jobs found.
```

Boundary:

```text
No remote git clone/fetch/download/pip/GitHub source/dependency fetch was run.
No LTP retry or second allocation was submitted.
No preflight/SFT/eval was run.
Future runtime requires fresh PM authorization.
```
