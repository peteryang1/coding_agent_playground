# dev_2 Session 22 ENOSPC-Fixed Retry Runtime

Task ID: `M1-S22-ENOSPC-RETRY-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T08:19:32Z

Scope: one PM-authorized owner-executed ENOSPC-fixed ShareGPT Qwen3-8B SFT smoke.

Authorization source:

```text
PM authorized exactly one fresh LTP job and exactly one SFT attempt.
dev_1 gate: PASS_FOR_PM_RETRY
test_1 gate: PASS_FOR_PM_RETRY
dataset: coding_agent_m1_sft_10_sharegpt
source dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
required output root: /home/xu.yang/coding_agent_playground/outputs
save_steps: 2
save_total_limit: 1
max_steps: 2
eval: not authorized
```

## Execution Boundary

```text
LTP submit authorized: yes, exactly one fresh job.
SFT authorized: yes, exactly one attempt after mount/path proof and real-write capacity probe pass.
Eval authorized: no.
Routine PM peer_send: no.
Durable evidence/status only.
```

## Planned Paths

```text
output_root: /home/xu.yang/coding_agent_playground/outputs
capacity_probe_root: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>
run_metadata_root: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>
logs: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
config: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
nodes_json: /home/xu.yang/coding_agent_playground/outputs/milestone1_s22_nodes.json
```

Existing required path exceptions:

```text
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dependency archives/wheels: /mnt/3fs/data/ai4ai/deps
justification: existing required read-only inputs; not used for outputs/checkpoints/logs/probes/run metadata.
```

## LTP Submit

Attempted JSON submit first:

```bash
RUNTIME_ID=20260521T082037Z
JOB_NAME=coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
FRAME=xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
LTP_JSON=/tmp/coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z.json
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_JSON}"
```

Result:

```text
HTTP 400 InvalidProtocolError; no resource allocated from this JSON submit.
```

Successful YAML submit:

```bash
LTP_YAML=/tmp/coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z.yaml
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Result:

```text
status: 202
message: Update job coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z for user xu.yang successfully.
```

## Node And Endpoint

Initial LTP status:

```text
state: RUNNING (AttemptRunning)
submitted: 2026-05-21 08:20:48
started: 2026-05-21 08:20:53
ip: 10.100.16.69
ssh port: 31346
endpoint: ssh -p 31346 root@10.100.16.69
```

## Mount And Capacity Proof

Initial SSH/mount check before LTP bootstrap completed:

```text
2026-05-21T08:21:34Z
hostname: lg-cmc-b7r202-i03u06-h200-000571
/home/xu.yang: missing
/mnt/cephfs: missing
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB memory used each
SFT: not started
```

LTP bootstrap completion check:

```text
2026-05-21T08:23:38Z
sleep infinity running
ceph-fuse running
/mnt/cephfs: fuse.ceph-fuse
/mnt/3fs: fuse.hf3fs
/mnt/cephfs/home/xu.yang exists
/home/xu.yang missing
```

Path fix applied on the worker:

```bash
ln -s /mnt/cephfs/home/xu.yang /home/xu.yang
```

Justification: LTP mounted CephFS at `/mnt/cephfs`, with the user home at `/mnt/cephfs/home/xu.yang`; PM-required storage root is `/home/xu.yang/coding_agent_playground/outputs`, so `/home/xu.yang` was created as a path entry to the same CephFS home.

Post-fix proof:

```text
2026-05-21T08:23:57Z
hostname: lg-cmc-b7r202-i03u06-h200-000571
readlink -f /home/xu.yang: /mnt/cephfs/home/xu.yang
findmnt -T /home/xu.yang: /mnt/cephfs fuse.ceph-fuse ceph-fuse
output path: /home/xu.yang/coding_agent_playground/outputs
df: ceph-fuse 18P size, 1.8P used, 16P available, 10% use
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB memory used each
```

Real-write capacity probe:

```bash
RUN_ID=milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
OUT=/home/xu.yang/coding_agent_playground/outputs
PROBE="${OUT}/capacity_probes/${RUN_ID}"
mkdir -p "${PROBE}"
for i in 0 1 2 3; do
  dd if=/dev/zero of="${PROBE}/probe_${i}.bin" bs=1G count=6 status=progress conv=fsync
  ls -lh "${PROBE}/probe_${i}.bin"
done
sync
```

Probe result:

```text
2026-05-21T08:24:13Z start
All four 6.0G files wrote successfully under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>.
The first bookkeeping command after writes had a shell quoting error (`parameter not set`), so a recovery verification was run.
2026-05-21T08:24:52Z recovery verification
findmnt -T probe path: /mnt/cephfs fuse.ceph-fuse ceph-fuse
probe files: 4
du -sb: 25769803776 bytes
cleanup: probe_*.bin removed and probe directory removed
PROBE_STATUS=PASS_RECOVERED_AND_CLEANED
```

## Exact SFT Command

Staging completed:

```text
2026-05-21T08:25:49Z
/root/workspace/coding_agent_playground staged
/root/workspace/cleaned_m1_sft_10_sharegpt staged
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset rows: 10
output root: /home/xu.yang/coding_agent_playground/outputs
```

Installed runtime dependencies and dataset_info:

```text
2026-05-21T08:27:03Z
LLamaFactory installed from /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz
mcore_adapter installed from /mnt/3fs/data/ai4ai/deps/mcore_adapter/
flash_attn wheel installed from /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
dataset_info paths:
  /root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
  /root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
entry: coding_agent_m1_sft_10_sharegpt
file_name: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
formatting: sharegpt
columns.messages: messages
tags.role_tag: from
tags.content_tag: value
tags.user_tag: human
tags.assistant_tag: gpt
tags.system_tag: system
tags.observation_tag: tool
```

Nodes JSON:

```text
path: /root/workspace/coding_agent_playground/nodes.json
path: /home/xu.yang/coding_agent_playground/outputs/milestone1_s22_nodes.json
sha256: f385360b681fec6d300da9d11f918995c0c7c29cb39825733b1d5e49d3c3948e
content: {"node_count":1,"nodes":[{"ip":"10.100.16.69","port":"31346","user":"root","node_rank":0,"hostname":"lg-cmc-b7r202-i03u06-h200-000571"}]}
```

S22 config template:

```text
path: /tmp/qwen3_8b_sft_s22_enospc.yaml
sha256: f351182b03d7adcd642835048f065322eba9ddb547cb413a6219ffb72dcd1ee3
assertions:
  dataset: coding_agent_m1_sft_10_sharegpt
  output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
  save_steps: 2
  save_total_limit: 1
  warmup_steps: 0
  max_steps: 2
  tensor_model_parallel_size: 8
  pipeline_model_parallel_size: 1
  context_parallel_size: 1
  sequence_parallel: false
```

Exact launched SFT command:

```bash
cd /root/workspace/coding_agent_playground
CONFIG_TEMPLATE=/tmp/qwen3_8b_sft_s22_enospc.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Launch wrapper:

```text
tmux session: s22_sft_runtime
started: 2026-05-21T08:27:52Z
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/logs/train_stdout_stderr.log
exit_status path: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/exit_status.txt
```

## Runtime Result

Final result: **failed before training produced manifest/config/checkpoint artifacts**.

SFT attempt count:

```text
authorized_attempts: 1
attempts_started: 1
attempts_completed: 1
additional_retries_run: 0
eval_run: false
```

Runtime status:

```text
run_id: milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
tmux: completed
exit_status_path: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/exit_status.txt
exit_status: EXIT_STATUS=1
end_utc: 2026-05-21T08:27:52Z
```

Log path:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/logs/train_stdout_stderr.log
```

Log content:

```text
START_UTC=2026-05-21T08:27:52Z
```

Artifact presence:

```text
run_manifest.json: absent
generated runtime config under run dir: absent
checkpoint files: absent
trainer_state.json: absent
all_results.json: absent
complete checkpoint/model: absent
```

CephFS preserved files, visible after node stop via `/mnt/cephfs/home/xu.yang/...`:

```text
31 /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/logs/train_stdout_stderr.log
43 /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/exit_status.txt
```

Old failure signature checks:

```text
KeyError: 'from': not observed in produced log
No space left on device: not observed in produced log
safetensors ENOSPC: not observed in produced log
ShareGPT conversion progress: not observed
training step progress: not observed
```

Runtime blocker:

```text
SFT wrapper launched exactly once, but scripts/train_qwen3_8b_sft.sh returned exit status 1 before it emitted stderr/stdout into the run log and before it generated run_manifest.json, copied runtime config, or created checkpoint artifacts. GPU sampling after failure showed no torchrun/llamafactory/python training process and all 8 H200 GPUs idle at 0% util / 1 MiB memory. Because only one SFT attempt was authorized, no retry/debug rerun was performed on the node.
```

Next fix recommendation:

```text
Before any future PM-authorized retry, add a preflight wrapper that runs the training script with shell tracing or captures the failure boundary before the script redirects into the durable log. The current failure is earlier than data conversion, training, and checkpoint save, so it does not validate the ENOSPC fix or the ShareGPT runtime path.
```

## Stop Proof

Stop command:

```bash
FRAME=xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"
```

Stop issued:

```text
2026-05-21T08:29:55Z
STOP signal sent
status: 202
```

Post-stop status:

```text
2026-05-21T08:30:36Z
State: STOPPED (Completed)
ExecType: STOP
Submitted: 2026-05-21 08:20:48
Started: 2026-05-21 08:20:53
Completed: 2026-05-21 08:30:26
ExitCode: -210 Failed
task idx 0: STOPPED
```

Endpoint proof:

```text
ssh -p 31346 root@10.100.16.69
result after STOPPED: connection refused
confirmed again at 2026-05-21T08:30:57Z, 2026-05-21T08:31:17Z, and 2026-05-21T08:31:37Z
```

Artifact preservation note:

```text
CephFS output root is preserved:
/home/xu.yang/coding_agent_playground/outputs

After node stop, the same files are visible from the shared CephFS mount:
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs

No cleanup of runtime log/exit artifacts was performed.
No eval was run.
```
