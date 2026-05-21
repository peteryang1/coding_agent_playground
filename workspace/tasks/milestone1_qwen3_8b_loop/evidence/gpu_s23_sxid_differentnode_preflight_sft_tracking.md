# dev_2 S23 SXid Different-Node GPU Runtime Tracking

Task ID: `M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T14:01:55Z

Initial state: `LOCAL_BUNDLE_READY_PRE_SUBMIT`

```text
authorized allocation count: 1 fresh single-node 8 x H200
LTP frame: xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
endpoint: pending
node: pending
avoid nodes: lg-cmc-b7r202-q03u26-h200-000730, lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
source commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
source bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote network rule: no remote git clone/fetch/GitHub/source/dependency download
preflight: pending
conditional SFT: pending only if PASS and sft_allowed=true
eval: not authorized
```

Stop/release required on same-SXid-node assignment, same/prior failed node assignment, preflight fail, `sft_allowed=false`, source/data verification fail, storage/capacity fail, SFT success, SFT failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Tracking Record

Final state: `STOPPED_AFTER_SAME_SXID_NODE_BLOCKER`

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z.yaml
submit result: HTTP 202
RUNNING observed: 2026-05-21T14:03:41Z
endpoint: ssh -p 39629 root@10.100.22.36
assigned node: lg-cmc-b7r202-q03u26-h200-000730
avoid node matched: lg-cmc-b7r202-q03u26-h200-000730
blocker: SAME_SXID_NODE_ASSIGNED
```

Action taken:

```text
preflight: not run
SFT: not run
eval: not authorized and not run
source/data transfer: not performed because avoid-node gate failed first
remote project source/dependency network: none
```

Stop/release proof:

```text
stop timestamp UTC: 2026-05-21T14:04:01Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
stop result: HTTP 202, stop signal sent
post-stop state: STOPPED (Completed)
completed: 2026-05-21 14:04:32
endpoint proof: ssh -p 39629 root@10.100.22.36 refused connection after stop
no-active-Milestone-GPU proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

No active coding_agent_playground/Milestone 1 GPU allocation remains held by dev_2 for this task.
