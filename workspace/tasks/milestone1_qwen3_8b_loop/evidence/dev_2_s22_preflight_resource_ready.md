# dev_2 S22 Parser-Fixed Preflight Resource Readiness

Task ID: `M1-S22-PREFLIGHT-RESOURCE-READY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T11:14:22Z

Scope: no-submit resource/readiness plan for a future parser-fixed NCCL/NVLink preflight and conditional Qwen3-8B ShareGPT SFT retry. This file is readiness evidence only; it does not authorize LTP submit, GPU use, SFT, eval, dry-run, or remote probing beyond read-only LTP status/list checks.

## Current Resource Proof

Read-only checks performed:

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground --limit 50
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200agentic --limit 50
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --vc h200 --limit 50
```

Observed at `2026-05-21T11:14:22Z`:

```text
prior frame: xu.yang~coding-agent-playground-m1-s22-nccl-preflight-sft-20260521T105525Z
prior state: STOPPED (Completed)
prior submitted: 2026-05-21 10:56:15
prior started: 2026-05-21 10:56:20
prior completed: 2026-05-21 11:02:09
prior endpoint: ssh -p 27402 root@10.100.24.11
prior node: lg-cmc-b7r401-a04u26-h200-000769
running coding-agent-playground jobs: none found
running h200agentic jobs: one unrelated ltp-axis-eval-platform-* job
running h200 jobs: two unrelated ltp-axis-eval-platform-* jobs
current Milestone GPU held by dev_2: no
```

Conclusion:

```text
No active coding_agent_playground/Milestone 1 GPU allocation is held by dev_2 after the stopped preflight frame.
The prior frame must not be reused.
Any future allocation must be fresh and preferably on a different physical node from both prior failed nodes:
- lg-cmc-b7r202-p07u16-h200-000708
- lg-cmc-b7r401-a04u26-h200-000769
```

## Authorization Boundary

No LTP submit, GPU command, NCCL preflight, SFT, eval, dry-run, or remote workspace mutation may be performed until PM gives fresh authorization after the required parser-fixed gates:

```text
required before submit:
- dev_4 parser fix package/PR for M1-S22-PREFLIGHT-PARSER-FIX-DEV4
- dev_1 parser review PASS for M1-S22-PREFLIGHT-PARSER-REVIEW-DEV1
- test_1 parser gate PASS for M1-S22-PREFLIGHT-PARSER-GATE-TEST1
- explicit PM runtime authorization naming intern_code_dev_2 as owner
```

## Intended Resource Shape

```text
node shape: single node, 8 x NVIDIA H200
VC preference: h200agentic or PM-specified H200 VC
freshness: new LTP frame, not the stopped frame above
node preference: different physical node from lg-cmc-b7r202-p07u16-h200-000708 and lg-cmc-b7r401-a04u26-h200-000769 if available
duration target: <= 60 minutes unless PM records a bounded extension
owner: intern_code_dev_2 owns submit, preflight monitoring, conditional SFT launch only after preflight PASS, stop/release proof
```

## LTP Command Templates Only

These are templates, not commands to run under this no-submit task.

Submit template:

```bash
RUNTIME_ID=$(date -u +%Y%m%dT%H%M%SZ)
JOB_NAME="coding-agent-playground-m1-s22-parserfixed-preflight-sft-${RUNTIME_ID}"
FRAME="xu.yang~${JOB_NAME}"
LTP_YAML="/tmp/${JOB_NAME}.yaml"

# Prepare ${LTP_YAML} from the approved single-node 8xH200 template only after PM authorization.
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Wait/status/endpoint templates:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait "${FRAME}" --state RUNNING --timeout 1800 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh "${FRAME}"
```

Stop template:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait "${FRAME}" --timeout 600 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
```

Post-stop endpoint proof template:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p "${SSH_PORT}" root@"${HOST_IP}" true
```

## Path Plan

Required output root for any future authorized run:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Path layout:

```text
capacity probes: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>/
preflight artifacts: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/
run metadata: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/
SFT logs: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/logs/
SFT config: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/config/
temporary converted datasets/intermediates: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/tmp/
checkpoints/model: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/checkpoints/
stop proof/evidence copies: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/stop_proof/
```

Required input exceptions only:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source_dataset_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dependency archives/wheels if needed: /mnt/3fs/data/ai4ai/deps
justification: existing required read-only inputs; outputs, logs, checkpoints, probes, metadata, and intermediates must stay under /home/xu.yang/coding_agent_playground/outputs.
```

Capacity plan for future authorized run:

```text
1. Prove /home/xu.yang resolves to CephFS-backed path.
2. Record findmnt/df for /home/xu.yang and /home/xu.yang/coding_agent_playground/outputs.
3. Write a real capacity probe under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>.
4. Verify byte count and file count.
5. Clean only the probe files, preserving logs/proof.
6. Do not start preflight or SFT if capacity probe fails.
```

## Future Preflight/SFT Gate Shape

Future parser-fixed preflight should run before any SFT and should write structured fields under the preflight artifact directory:

```text
home_path_status
capacity_probe_status
gpu_idle_status
nvlink_status
topology_status
nccl_collective_status
health_fault_status
preflight_result
```

SFT may run only if the parser-fixed preflight writes a clear PASS marker. If preflight fails, is ambiguous, allocates a rejected/same physical node without PM acceptance, lacks acceptable NCCL substitute tooling, or cannot use `/home/xu.yang`, SFT must not run.

## Stop Conditions

Stop/release the future LTP frame after any of:

```text
same-node rejection if PM required a different physical node;
/home/xu.yang path or capacity probe failure;
parser-fixed preflight failure or ambiguous result;
missing NCCL test tooling without acceptable substitute;
SFT checkpoint/model success;
SFT failure with no PM-authorized same-node retry;
health fault, idle/progress timeout, or endpoint instability;
PM/test stop instruction;
bounded max runtime reached.
```

Required stop proof:

```text
LTP stop command/action
UTC stop timestamp
post-stop LTP status showing STOPPED/terminal state
endpoint refusal or equivalent unreachable proof
artifact preservation note for /home/xu.yang/coding_agent_playground/outputs
```

## Completion Marker

`M1-S22-PREFLIGHT-RESOURCE-READY-DEV2` is complete as a no-submit readiness task. No LTP job was submitted, no GPU was occupied, no NCCL preflight was run, no SFT was run, and no eval was run.

## 2026-05-21T11:40:53Z PR45 Pending Addendum

Context:

```text
PM requested a no-submit readiness refresh while PR #45 owner self-merge is pending.
PR #45 task: M1-S22-PREFLIGHT-PARSER-FIX-DEV4
latest known PR #45 head from durable PM files: 01eebb7508768cd8b8ba3a1601e4a1f3774c27b4
PM gate status in durable files: PR #45 gate passed for dev_4 owner self-merge only; runtime remains separately unauthorized.
dev_2 action in this addendum: readiness-only documentation update.
No LTP submit, GPU command, NCCL preflight, SFT, eval, dry-run, or remote workspace mutation was performed.
```

Planned durable evidence files for a future separately authorized runtime:

```text
primary runtime evidence: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_postpr45_preflight_sft_runtime.md
GPU/resource tracking: workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_postpr45_preflight_sft_tracking.md
owner status: workspace/interns/intern_code_dev_2/status.md
task registry/completion marker: workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
optional history entry if PM requests: workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
```

Post-PR45 path plan:

```text
output root: /home/xu.yang/coding_agent_playground/outputs
capacity probes: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>/
preflight root: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/
parser JSON status: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/health_status.json
parser text status: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/health_status.txt
run metadata: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/
SFT logs: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/logs/
SFT config: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/config/
temporary converted datasets/intermediates: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/tmp/
checkpoints/model: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/checkpoints/
stop proof/evidence copies: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/stop_proof/
```

Parser-fixed `health_status` usage from PR #45:

```text
After the future PM-authorized NCCL/NVLink preflight writes artifacts under /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>,
run scripts/parse_s22_preflight_health.py from the merged PR #45 workspace.
The parser must write:
- health_status.json
- health_status.txt

SFT may be launched only when health_status.json records:
- preflight_result/status PASS
- actionable_fault false
- home_xu_yang_storage_status PASS
- sft_allowed true, or decision.sft_allowed_if_pm_authorized true

SFT must not be launched when parser status is FAIL_HEALTH_SIGNATURE, WARN_INCOMPLETE, storage is outside /home/xu.yang/coding_agent_playground/outputs, NCCL/topology/capacity/preflight fields are missing/failed, same-node rejection applies, or PM has not separately authorized runtime.
```

Fresh allocation requirement:

```text
future allocation: fresh single-node 8 x NVIDIA H200
node preference: preferably different physical node from:
- lg-cmc-b7r202-p07u16-h200-000708
- lg-cmc-b7r401-a04u26-h200-000769
prior frame reuse: forbidden
same node outcome: if PM required different-node and the allocation lands on a rejected node, stop/release and record blocker; do not run preflight/SFT unless PM explicitly accepts the node.
```

Stop conditions for a future authorized run:

```text
same-node rejection when different-node was required;
/home/xu.yang storage proof or capacity probe failure;
missing NCCL test tooling without acceptable substitute;
parser-fixed preflight result not PASS;
health_status.json/txt missing or ambiguous;
home_xu_yang_storage_status not PASS;
sft_allowed false or missing after parsing;
SFT checkpoint/model success;
SFT failure with no PM-authorized same-node retry;
health fault, idle/progress timeout, or endpoint instability;
PM/test stop instruction;
bounded max runtime reached.
```

Command template for future use only after PR #45 is merged and PM separately authorizes dev_2 runtime:

```bash
RUNTIME_ID=$(date -u +%Y%m%dT%H%M%SZ)
JOB_NAME="coding-agent-playground-m1-s22-postpr45-preflight-sft-${RUNTIME_ID}"
FRAME="xu.yang~${JOB_NAME}"
LTP_YAML="/tmp/${JOB_NAME}.yaml"
OUTPUT_ROOT="/home/xu.yang/coding_agent_playground/outputs"
PREFLIGHT_DIR="${OUTPUT_ROOT}/preflight/${RUNTIME_ID}"
RUN_ROOT="${OUTPUT_ROOT}/runs/${RUNTIME_ID}"

# Submit fresh 1x8 H200 LTP only after PM authorization.
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait "${FRAME}" --state RUNNING --timeout 1800 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py ssh "${FRAME}"

# On the authorized node, after /home/xu.yang path proof, capacity probe, NCCL/NVLink preflight artifacts:
cd /root/workspace/coding_agent_playground
python3 scripts/parse_s22_preflight_health.py \
  --preflight-dir "${PREFLIGHT_DIR}" \
  --out-json "${PREFLIGHT_DIR}/health_status.json" \
  --out-text "${PREFLIGHT_DIR}/health_status.txt"

# Only if health_status.json is PASS and PM authorized conditional SFT:
# launch the one authorized Qwen3-8B ShareGPT SFT smoke with all generated outputs under "${RUN_ROOT}".

# Stop/release after success/failure/blocker:
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait "${FRAME}" --timeout 600 --interval 15
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status "${FRAME}"
```

Addendum completion marker:

```text
Readiness addendum complete.
No LTP submit/GPU/NCCL/SFT/eval/dry-run was performed.
Next executable action remains blocked until PR #45 is merged by dev_4, task completion is recorded, and PM separately authorizes dev_2 runtime.
```
