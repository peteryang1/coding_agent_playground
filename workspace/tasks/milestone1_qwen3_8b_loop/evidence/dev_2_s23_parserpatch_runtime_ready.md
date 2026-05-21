# dev_2 S23 Parser-Patch Runtime Readiness

Task ID: `M1-S23-PARSERPATCH-RUNTIME-READY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T12:26:47Z

Scope: no-submit runtime readiness for a possible future parser-patch retry. This task does not authorize LTP submit, GPU use, NCCL/preflight, SFT, eval, dry-run, or remote GPU-node commands.

## Source Evidence Read

Local durable sources used:

```text
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_parserfixed_resource_recovery.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md
workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s22_parserfixed_preflight_sft_tracking.md
workspace/interns/intern_code_dev_2/status.md
```

No LTP submit, LTP status command, GPU-node SSH command, NCCL/preflight command, SFT command, eval command, or dry-run command was run for this readiness task.

## Current Resource Closure / No Active Held GPU Proof

Durable stopped proof from the prior parser-fixed runtime:

```text
prior frame: xu.yang~coding-agent-playground-m1-s22-parserfixed-preflight-sft-20260521T114448Z
prior endpoint: ssh -p 22662 root@10.100.22.14
prior node: lg-cmc-b7r202-p07u16-h200-000708
post-stop LTP state: STOPPED (Completed)
completed timestamp: 2026-05-21 11:56:39
stop sent UTC: 2026-05-21T11:56:07Z
wait result: STOPPED at 2026-05-21T11:56:45Z
endpoint proof: ssh to 10.100.22.14:22662 returned "Connection refused"
dev_2 resource conclusion: no active parser-fixed/Milestone GPU is held by dev_2 from the prior runtime.
```

This Session 23 readiness task did not acquire a resource or touch any GPU node. If PM requires a fresh fleet-level LTP query beyond the durable stopped proof above, that should be explicitly authorized as a read-only status check; this task otherwise remains no-LTP/no-GPU.

## Runtime Readiness State

```text
ready_to_submit: no
ready_to_run_preflight: no
ready_to_run_sft: no
reason: parser-patch PR/merge commit, dev_1 review, test_1 gate, and fresh PM runtime authorization are still required before any runtime action.
```

Required PM authorization inputs before a future runtime:

```text
parser patch merge commit: <PARSER_PATCH_MERGE_COMMIT>
parser patch PR id: <PARSER_PATCH_PR>
dev_1 parserpatch review: PASS_FOR_PM_RETRY
test_1 parserpatch gate: PASS_FOR_PM_RETRY
dev_3 data staging confirmation: accepted source/data contract remains valid
PM runtime authorization: explicit one-run authorization naming dev_2 owner and allowed scope
```

## No-Remote-Network Rule

Future remote GPU/LTP nodes must be treated as no-external-network targets.

Forbidden on remote GPU/LTP nodes:

```text
git clone
git fetch
pip install from network
curl/wget/download from GitHub or external network
any source/dependency fetch that relies on GPU-node internet access
```

Required future staging pattern:

```text
1. Prepare code/config/scripts/dependency material locally or in the provided workspace before LTP runtime.
2. Verify exact source commit, file list, and sha256 checksums locally before transfer.
3. Transfer the prepared bundle to the future endpoint with rsync, scp, or tar-over-SSH.
4. Verify checksum/file list on the remote after transfer.
5. Record source commit, local source path, artifact path, transfer command, destination path, file list, sha256s, and post-transfer verification in runtime evidence.
```

## Intended Resource Shape

Future allocation shape, only after fresh PM authorization:

```text
vc/queue: h200agentic or PM-approved equivalent
node shape: single node
gpu shape: 8 x NVIDIA H200
node preference: fresh allocation, preferably different from prior blocked nodes
avoid if possible:
  - lg-cmc-b7r202-p07u16-h200-000708
  - lg-cmc-b7r401-a04u26-h200-000769
reason: prior parser-fixed health/storage blocker and prior NCCL/NVLink blocker evidence.
```

## Local Bundle Preparation Template

Use these commands locally/provided workspace before any future transfer. Replace placeholders only after PM authorization identifies the parser-patch merge commit.

```bash
TASK_ID=M1-S23-PARSERPATCH-RUNTIME-READY-DEV2
SOURCE_REPO=/work-agents/intern_code_pm/coding_agent_playground/workspace
SOURCE_COMMIT=<PARSER_PATCH_MERGE_COMMIT>
RUN_ID=milestone1_qwen3_8b_s23_parserpatch_preflight_sft_<UTC>
BUNDLE_ROOT=/tmp/${RUN_ID}_bundle
BUNDLE_TAR=/tmp/${RUN_ID}_coding_agent_playground_${SOURCE_COMMIT}.tar.gz
BUNDLE_SHA=/tmp/${RUN_ID}_bundle.sha256
FILE_LIST=/tmp/${RUN_ID}_file_list.txt

cd "$SOURCE_REPO"
git rev-parse HEAD
test "$(git rev-parse HEAD)" = "$SOURCE_COMMIT"
git status --short
git ls-files > "$FILE_LIST"
tar --exclude .git -czf "$BUNDLE_TAR" -C "$SOURCE_REPO" .
sha256sum "$BUNDLE_TAR" > "$BUNDLE_SHA"
sha256sum \
  scripts/parse_s22_preflight_health.py \
  scripts/train_qwen3_8b_sft.sh \
  configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml \
  > /tmp/${RUN_ID}_critical_files.sha256
```

Minimum required local evidence before transfer:

```text
source commit equals PM-authorized parser patch merge commit.
file list captured.
bundle tar sha256 captured.
critical script/config sha256 captured.
no unrecorded local source mutation in files needed for runtime.
```

## Transfer Templates

Future endpoint placeholders:

```text
ENDPOINT_HOST=<FUTURE_LTP_HOST>
ENDPOINT_PORT=<FUTURE_LTP_PORT>
REMOTE_REPO=/root/workspace/coding_agent_playground
REMOTE_BUNDLE=/root/workspace/${RUN_ID}_coding_agent_playground_${SOURCE_COMMIT}.tar.gz
REMOTE_EVIDENCE=/home/xu.yang/coding_agent_playground/outputs/runs/${RUN_ID}/staging
```

Preferred tar-over-SSH template:

```bash
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "mkdir -p /root/workspace '$REMOTE_EVIDENCE'"
cat "$BUNDLE_TAR" | ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "cat > '$REMOTE_BUNDLE'"
scp -P "$ENDPOINT_PORT" "$BUNDLE_SHA" "$FILE_LIST" /tmp/${RUN_ID}_critical_files.sha256 root@"$ENDPOINT_HOST":"$REMOTE_EVIDENCE"/
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "rm -rf '$REMOTE_REPO' && mkdir -p '$REMOTE_REPO' && tar -xzf '$REMOTE_BUNDLE' -C '$REMOTE_REPO'"
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "sha256sum -c '$REMOTE_EVIDENCE/$(basename "$BUNDLE_SHA")'"
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "cd '$REMOTE_REPO' && sha256sum -c '$REMOTE_EVIDENCE/${RUN_ID}_critical_files.sha256'"
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "cd '$REMOTE_REPO' && test \"\$(git rev-parse HEAD 2>/dev/null || true)\" = '' || git rev-parse HEAD"
```

`rsync` template:

```bash
rsync -a --delete -e "ssh -p $ENDPOINT_PORT" "$SOURCE_REPO"/ root@"$ENDPOINT_HOST":"$REMOTE_REPO"/
scp -P "$ENDPOINT_PORT" "$FILE_LIST" /tmp/${RUN_ID}_critical_files.sha256 root@"$ENDPOINT_HOST":"$REMOTE_EVIDENCE"/
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "cd '$REMOTE_REPO' && sha256sum -c '$REMOTE_EVIDENCE/${RUN_ID}_critical_files.sha256'"
```

`scp` template:

```bash
scp -P "$ENDPOINT_PORT" "$BUNDLE_TAR" "$BUNDLE_SHA" "$FILE_LIST" /tmp/${RUN_ID}_critical_files.sha256 root@"$ENDPOINT_HOST":"$REMOTE_EVIDENCE"/
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "mkdir -p '$REMOTE_REPO' && tar -xzf '$REMOTE_EVIDENCE/$(basename "$BUNDLE_TAR")' -C '$REMOTE_REPO'"
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "sha256sum -c '$REMOTE_EVIDENCE/$(basename "$BUNDLE_SHA")'"
ssh -p "$ENDPOINT_PORT" root@"$ENDPOINT_HOST" "cd '$REMOTE_REPO' && sha256sum -c '$REMOTE_EVIDENCE/${RUN_ID}_critical_files.sha256'"
```

Post-transfer evidence requirements:

```text
exact transfer command used.
endpoint host/port.
destination paths.
source commit and PR id.
bundle sha256 and critical-file sha256s.
remote verification command and output.
remote generated evidence path under /home/xu.yang/coding_agent_playground/outputs.
explicit statement that no remote git/pip/download/GitHub fetch was used.
```

## Future Output Paths

All generated artifacts must be under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Planned layout:

```text
capacity probes: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>/
preflight artifacts: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/
parser JSON status: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/health_status.json
parser text status: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>/health_status.txt
run metadata: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/
staging evidence: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/staging/
SFT logs: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/logs/
SFT config: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/config/
temporary converted datasets/intermediates: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/tmp/
checkpoints/model: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/checkpoints/
trainer outputs: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/trainer_outputs/
stop proof/evidence copies: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/stop_proof/
```

Existing required read-only input exceptions:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source_dataset_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
justification: existing required read-only inputs only; generated artifacts, temporary converted datasets, logs, checkpoints, run metadata, probes, and stop proof stay under /home/xu.yang/coding_agent_playground/outputs.
```

## LTP Command Templates Only

No command in this section was run for this task. These are templates for a future PM-authorized runtime only.

```bash
# submit template
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit <PM_AUTHORIZED_S23_LTP_SPEC.yaml>

# status/wait templates
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status <FRAME_ID>
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait <FRAME_ID> --state RUNNING --timeout 1800 --interval 15

# stop template
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop <FRAME_ID>
```

Future LTP spec requirements:

```text
single node
8 x NVIDIA H200
fresh allocation
preferably different physical node from prior blocked nodes
no remote source/dependency download in bootstrap
all generated artifacts under /home/xu.yang/coding_agent_playground/outputs
bounded runtime and stop conditions recorded before launch
```

## Future Runtime Stop Conditions

Stop/release the future allocation if any of the following occur:

```text
allocation lands on a PM-rejected or explicitly disallowed node;
source bundle cannot be transferred or post-transfer checksum verification fails;
remote staging would require git clone/fetch, pip/download, or GitHub/network fetch;
/home/xu.yang/coding_agent_playground/outputs path proof fails;
capacity probe fails or cannot clean probe files;
parser health_status.json/txt missing, malformed, or ambiguous;
structured preflight status is not PASS;
sft_allowed is not true;
HOME_XU_YANG_STORAGE_STATUS is not PASS;
fresh/current actionable Xid/SXid/ECC/NVLink/NCCL fault is detected;
torch NCCL all-reduce fails or hangs;
SFT succeeds and writes accepted checkpoint/model;
SFT fails with no PM-authorized same-node retry;
node becomes unhealthy or idle without progress;
PM/test stop instruction;
bounded max runtime reached.
```

Required stop proof:

```text
LTP stop command/action
UTC stop timestamp
post-stop LTP terminal status
endpoint refusal or equivalent unreachable proof
artifact preservation note for /home/xu.yang/coding_agent_playground/outputs
```

## No-Submit Boundary

```text
No LTP submit is authorized by this readiness task.
No GPU command is authorized by this readiness task.
No NCCL/preflight command is authorized by this readiness task.
No SFT is authorized by this readiness task.
No eval is authorized by this readiness task.
No dry-run is authorized by this readiness task.
No remote GPU-node source/dependency network action is ever acceptable for future runtime.
Future execution requires parser patch PR merge plus dev_1/test_1/dev_3 gates and fresh explicit PM runtime authorization.
```

## Completion Marker

`M1-S23-PARSERPATCH-RUNTIME-READY-DEV2` is complete as a no-submit readiness package. Runtime remains blocked until the parser patch is merged, gates pass, and PM explicitly authorizes a fresh one-run owner execution.
