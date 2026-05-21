# dev_2 S23 LTP Placement Plan

Task ID: `M1-S23-LTP-PLACEMENT-PLAN-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T14:08:00Z

Scope: no-submit/no-runtime placement/resource plan after the authorized different-node runtime landed on a forbidden SXid node. This task does not authorize LTP submit, GPU use, preflight, SFT, eval, dry-run, or remote endpoint mutation.

## Current Blocker

The one authorized different-node runtime landed on the same forbidden SXid node and was stopped before source transfer, preflight, SFT, or eval:

```text
task: M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2
frame: xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
endpoint while running: ssh -p 39629 root@10.100.22.36
assigned node: lg-cmc-b7r202-q03u26-h200-000730
blocker: SAME_SXID_NODE_ASSIGNED
stop timestamp UTC: 2026-05-21T14:04:01Z
final state: STOPPED (Completed)
completed: 2026-05-21 14:04:32
endpoint after stop: refused connection
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

Known failed/forbidden nodes:

```text
lg-cmc-b7r202-q03u26-h200-000730  # SXid node from M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2 and repeated placement in M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2
lg-cmc-b7r202-p07u16-h200-000708  # prior post-PR41/parser-fixed health/NCCL failures
lg-cmc-b7r401-a04u26-h200-000769  # prior preflight health-signature failure
lg-cmc-b7r202-q04u06-h200-000725  # prior ceph-fuse bootstrap failure
```

## LTP Placement Capability Check

Commands/read-only paths checked:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py --help
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit --help
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py launch --help
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --help
rg -n "node|affinity|anti|constraint|placement|sku|virtualCluster|vc|hived|pinned|host|hostname|priority" /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts /tmp/coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z.yaml /tmp/coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z.yaml
sed -n '440,540p' /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py
```

Findings:

```text
ltp.py submit: accepts only a yaml/json path; no CLI placement/anti-affinity arguments.
ltp.py launch: renders template from exp/meta.json; supported LTP meta fields are template, run_script, job_name, instances, gpu_per_node, cpu_per_node, memory_mb, shm_mb, vc, sku_type.
ltp.py list: can filter by vc/keyword/state/user only; no placement control.
local YAML templates used by dev_2: specify virtualCluster h200agentic and hivedScheduler skuNum=8, skuType=h200; no hostname, nodeSelector, anti-affinity, exclude-node, rack, zone, or placement constraint field is present.
local ltp.py script: exposes VC and sku selection but no documented node pinning or anti-affinity field in its launch renderer.
```

Assessment:

```text
Available via current local LTP client/spec: VC selection, skuType, skuNum, image, resource shape.
Not available/verified via current local LTP client/spec: guaranteed physical-node exclusion, hostname pinning, anti-affinity, rack/zone constraints, or "not in node list" placement constraints.
```

Exact blocker if PM requires guaranteed different-node placement:

```text
BLOCKED_PLACEMENT_NOT_GUARANTEED_BY_CURRENT_LTP_TEMPLATE
```

Changing VC, image, or job name might alter scheduler choice but does not prove exclusion of `lg-cmc-b7r202-q03u26-h200-000730` or the other failed nodes. A future runtime should not be considered placement-safe unless PM/compute/LTP provides one of:

```text
1. A documented YAML field for node exclusion/anti-affinity, validated by test_1/dev_1 before submit.
2. A separate VC/queue/resource pool known not to contain the forbidden nodes.
3. A pre-reserved endpoint/node identity that is already proven outside the forbidden list before dev_2 consumes runtime authorization.
4. A scheduler-side placement request handled by the LTP/compute owner with durable proof of the assigned node before preflight/SFT.
```

## Future Submit/Status/Stop Templates

These are templates only. Do not run them unless PM gives a fresh explicit runtime authorization after placement is solved.

```bash
# Render or prepare a future YAML that includes the approved placement mechanism.
# If no placement mechanism is available, do not submit.
FUTURE_RUN_TS=<YYYYMMDDTHHMMSSZ>
FUTURE_FRAME="xu.yang~coding-agent-playground-m1-s23-placementfixed-preflight-sft-${FUTURE_RUN_TS}"
FUTURE_YAML="/tmp/coding-agent-playground-m1-s23-placementfixed-preflight-sft-${FUTURE_RUN_TS}.yaml"

# Submit only after PM authorization and placement proof.
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "$FUTURE_YAML"

# Wait/status.
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait "$FUTURE_FRAME" --state RUNNING --timeout 1800 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "$FUTURE_FRAME"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py events "$FUTURE_FRAME"

# Immediate node gate before transfer/preflight/SFT.
ssh -p <PORT> root@<HOST> 'hostname'
# If hostname is in forbidden list, stop immediately and do not run transfer/preflight/SFT.

# Stop/release.
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "$FUTURE_FRAME"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait "$FUTURE_FRAME" --state STOPPED --timeout 600 --interval 10
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
```

## Runtime Rules to Preserve

Future runtime rules remain unchanged:

```text
No remote git clone/fetch/GitHub/source/dependency download on GPU node.
Prepare code/config/scripts/data locally or from provided workspace.
Verify source commit, file list, and checksums locally before transfer.
Transfer by scp/rsync/tar-over-SSH only after node placement gate passes.
Post-transfer verify bundle/data/checksums before preflight.
Use /home/xu.yang/coding_agent_playground/outputs for all generated outputs, logs, tmp data, preflight artifacts, run metadata, checkpoints, and evidence artifacts.
Run structured preflight first.
Run SFT only if structured preflight PASS and sft_allowed=true.
Eval is not authorized unless separately gated by PM.
Stop/release on same/forbidden node assignment, transfer verification failure, storage/capacity failure, preflight failure, sft_allowed=false, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.
```

## Boundary

For `M1-S23-LTP-PLACEMENT-PLAN-DEV2`, I did not submit LTP, occupy a GPU, connect to any GPU endpoint, run preflight, run SFT, run eval, or mutate remote state. I only inspected local LTP CLI help/source, local YAML templates, existing durable evidence, and wrote this placement plan/status.
