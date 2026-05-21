# dev_2 S22 Post-PR41 SFT Runtime

Task ID: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T10:06:34Z

Scope: exactly one PM-authorized post-PR #41 ShareGPT Qwen3-8B SFT smoke attempt. No eval authorization.

Authorization:

```text
PM authorization: 2026-05-21
PR #41 merged: 2026-05-21T10:00:25Z
PR #41 merge commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
dev_1/test_1: PASS_FOR_PM_RETRY
dev_3: no data content/schema change
authorized owner: intern_code_dev_2
authorized attempts: one SFT smoke
eval authorized: false
```

Code source:

```text
source method: independent temporary clone, not PM shared dirty worktree
clone path: /tmp/cap_pr39_runtime_repo
checked out commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
```

Storage contract:

```text
output_root: /home/xu.yang/coding_agent_playground/outputs
all SFT launch outputs, temporary converted datasets, logs, checkpoints, run metadata, capacity probes, and intermediates must stay under output_root unless an existing required input path is explicitly justified.
```

Existing required input exceptions:

```text
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dependency_archives_wheels: /mnt/3fs/data/ai4ai/deps
source_dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
justification: required read-only inputs/source artifact; not used for outputs/logs/checkpoints/probes/run metadata/intermediates.
```

## Submit And Node

Submit command:

```bash
RUNTIME_ID=20260521T100634Z
JOB_NAME=coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z
FRAME=xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z
LTP_YAML=/tmp/coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z.yaml
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Submit result:

```text
status: 202
message: Update job coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z for user xu.yang successfully.
```

Initial status:

```text
state: RUNNING (AttemptRunning)
submitted: 2026-05-21 10:07:19
started: 2026-05-21 10:07:22
ip: 10.100.22.14
ssh port: 27021
endpoint: ssh -p 27021 root@10.100.22.14
hostname: lg-cmc-b7r202-p07u16-h200-000708
```

Initial bootstrap observation:

```text
2026-05-21T10:07:38Z
hostname: lg-cmc-b7r202-p07u16-h200-000708
bootstrap still running apt update
/home/xu.yang missing before CephFS bootstrap
/mnt/cephfs/home/xu.yang missing before CephFS bootstrap
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB used each
SFT: not started
```

## Mount And Capacity Proof

Bootstrap complete:

```text
2026-05-21T10:08:39Z
hostname: lg-cmc-b7r202-p07u16-h200-000708
/mnt/cephfs: fuse.ceph-fuse
/mnt/3fs: fuse.hf3fs
/mnt/cephfs/home/xu.yang exists
/home/xu.yang missing before path fix
```

Path fix applied on worker:

```bash
ln -s /mnt/cephfs/home/xu.yang /home/xu.yang
mkdir -p /home/xu.yang/coding_agent_playground/outputs
```

Justification: LTP mounted CephFS at `/mnt/cephfs`; PM requires `/home/xu.yang/coding_agent_playground/outputs`, so `/home/xu.yang` was created as an entry to the CephFS home.

Post-fix proof:

```text
2026-05-21T10:09:12Z
hostname: lg-cmc-b7r202-p07u16-h200-000708
readlink -f /home/xu.yang: /mnt/cephfs/home/xu.yang
findmnt -T /home/xu.yang: /mnt/cephfs fuse.ceph-fuse ceph-fuse
df: ceph-fuse 18P size, 1.8P used, 16P available, 10% use
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB used each
```

Capacity probe command:

```bash
RUN_ID=milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
OUT=/home/xu.yang/coding_agent_playground/outputs
PROBE="${OUT}/capacity_probes/${RUN_ID}"
mkdir -p "${PROBE}"
for i in 0 1 2 3; do
  dd if=/dev/zero of="${PROBE}/probe_${i}.bin" bs=1G count=6 status=progress conv=fsync
  ls -lh "${PROBE}/probe_${i}.bin"
done
sync
du -sb "${PROBE}"
rm -f "${PROBE}"/probe_*.bin
rmdir "${PROBE}"
```

Capacity probe result:

```text
2026-05-21T10:09:12Z start
path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
files: 4 x 6.0G real dd writes with conv=fsync
bytes verified by du -sb: 25769803776
file_count: 4
cleanup: probe files and directory removed
2026-05-21T10:09:40Z
PROBE_STATUS=PASS_AND_CLEANED
```

## Runtime Command

Staging completed:

```text
2026-05-21T10:11:00Z
/root/workspace/coding_agent_playground staged from /tmp/cap_pr39_runtime_repo
git HEAD on worker: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
/root/workspace/cleaned_m1_sft_10_sharegpt staged from accepted final-workspace artifact
source dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
source dataset rows: 10
script sha256: 9dd84e02bea54915a613159012b0981070ba03e5d3b9cbd8fcda1047957b3cc5
manifest writer sha256: f0f80d88452c26dc46866316b2946f419c5eabd6ab2b41ab2d7c9a4b394f997f
config template sha256: b841ff72532eb30d9fd2cabfde4b5f119ddb2679694b3b231e8facf016f8b465
```

PR41 preprocessing proof before launch:

```text
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml:
  preprocessing_num_workers: null
  dataloader_num_workers: 0
scripts/write_sft_run_manifest.py records preflight.preprocessing_num_workers and PREPROCESSING_NUM_WORKERS.
```

Runtime dependencies and dataset_info:

```text
2026-05-21T10:13:50Z
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
path: /home/xu.yang/coding_agent_playground/outputs/milestone1_s22_postpr41_nodes.json
sha256: a9a2a0920c6bcb39ed5266c9ed491562cc7d7b90dc373d8f281bed131899ab7c
content: {"node_count":1,"nodes":[{"ip":"10.100.22.14","port":"27021","user":"root","node_rank":0,"hostname":"lg-cmc-b7r202-p07u16-h200-000708"}]}
```

Exact launched command:

```bash
cd /root/workspace/coding_agent_playground
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z \
DRY_RUN=0 \
SFT_XTRACE=1 \
bash scripts/train_qwen3_8b_sft.sh
```

Run paths:

```text
run_id: milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
run_dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z/logs/train_stdout_stderr.log
xtrace: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z/logs/train_xtrace.log
diagnostics: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z/early_exit_diagnostics.txt
manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z/run_manifest.json
runtime_config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z/config/qwen3_8b_sft.yaml
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
```

Launch:

```text
2026-05-21T10:14:23Z
tmux session: s22_postpr41_sft
attempt count: 1 authorized SFT attempt started
```

Live runtime proof:

```text
2026-05-21T10:14:46Z
torchrun/python/llamafactory processes active on 8 ranks
GPU memory: 532 MiB on GPU0, 626 MiB on GPUs1-7
runtime config:
  dataset: coding_agent_m1_sft_10_sharegpt
  preprocessing_num_workers: null
  dataloader_num_workers: 0
  output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
  save_steps: 2
  save_total_limit: 1
  max_steps: 2
  tensor_model_parallel_size: 8
run_manifest git_commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
run_manifest preflight.preprocessing_num_workers: null
run_manifest environment.PREPROCESSING_NUM_WORKERS: empty
log reached: Loading dataset /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
previous signature `Converting format of dataset (num_proc=4)` not observed at this poll.
```

## Runtime Result

Final result: **failed with fresh exact runtime blocker**.

Attempt accounting:

```text
authorized_sft_attempts: 1
attempts_started: 1
attempts_completed: 1
additional_retries_run: 0
eval_run: false
```

Exit status:

```text
exit_status_path: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z/exit_status.txt
EXIT_STATUS=1
END_UTC=2026-05-21T10:16:21Z
```

Post-run node/GPU observation before stop:

```text
2026-05-21T10:17:13Z
training/tmux processes: none observed except the status probe shell
GPU: all 8 H200 idle, 0% util, 1 MiB memory each
```

Artifact inventory:

```text
preflight.json size 1392 sha256 f56ed2f63d321726014dd60d2ff9ca2b6984578b5a634750a989690a7b0eec75
config/qwen3_8b_sft.yaml size 1673 sha256 1250855323deebaf03dc062caee801f80ffaf718420774f6ec36d20706590c6c
run_manifest.json size 4765 sha256 f858e03a2fa99387b3608a9a6a89d055533935e0241db9b57e949638c24475a0
logs/train_stdout_stderr.log size 945454 sha256 8e729550c3be42285b589cd67ac86e834da30519f5bb9a9dc39ba3f7717f24ec
logs/train_xtrace.log size 9610 sha256 ae57965617cf37a1ef3b5a61597ff86014e3ea0426389180ca03704f20548f02
early_exit_diagnostics.txt size 1700 sha256 0928a0025c567fde03fc6fb5846c5407ca8f543a53386b0d6c3ebb657cae51f0
exit_status.txt size 43 sha256 98a84efece913e078896deb5af24f917d5402299cb99ee0fa36e98278e91285b
```

Generated config proof:

```text
dataset: coding_agent_m1_sft_10_sharegpt
preprocessing_num_workers: null
dataloader_num_workers: 0
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
save_steps: 2
save_total_limit: 1
max_steps: 2
tensor_model_parallel_size: 8
```

Run manifest proof:

```text
git_commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
data.train_path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
data.train_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
preflight.dataset_name: coding_agent_m1_sft_10_sharegpt
preflight.preprocessing_num_workers: null
preflight.output_root: /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs
checkpoint_policy.save_steps: 2
checkpoint_policy.save_total_limit: 1
```

Runtime progress:

```text
ShareGPT conversion completed 10/10 without `num_proc=4`.
The previous post-PR39 `datasets.map(num_proc=4)` / SyncManager EOFError blocker was not reproduced.
Training startup was reached: log contains `***** Running training *****`, `Num examples = 1`, and `Num Epochs = 2`.
No checkpoint save was reached.
```

Checkpoint/model/result status:

```text
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpr41_sharegpt_tp8_maxsteps2_20260521T100634Z
files present: only TensorBoard event file under runs/May21_18-14-43_lg-cmc-b7r202-p07u16-h200-000708/
complete checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
config.json: absent
model.safetensors: absent
```

Fresh blocker signature:

```text
failure class: CUDA/NCCL peer GPU memory / NVLink or hardware error during distributed training
primary log signature:
  ProcessGroupNCCL watchdog thread terminated with exception:
  CUDA error: Invalid access of peer GPU memory over nvlink or a hardware error
torch elastic root cause:
  local_rank: 5
  exitcode: -6
  traceback: Signal 6 (SIGABRT) received by PID 29044
wrapper result:
  CalledProcessError from torchrun; wrapper wrote DIAGNOSTIC_REASON=ERR_TRAP and EXIT_STATUS=1.
```

Old blocker signatures absent:

```text
KeyError: from: absent
No space left on device / safetensors ENOSPC: absent
datasets.map(num_proc=4) / SyncManager EOFError: absent
checkpoint-save failure: not reached
```

Next fix recommendation:

```text
Treat as fresh runtime/node or distributed backend blocker, not data-format or PR41 preprocessing failure.
Do not retry on the stopped node. Future resource work requires fresh PM authorization and dev_4/dev_3/dev_1/test_1 gates.
Recommended next review should decide whether to rerun on a different H200 node, adjust NCCL/NVL settings, or add a minimal hardware/NCCL preflight before another SFT attempt.
```

## Stop Proof

Stop command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s22-postpr41-qwen3-8b-runtime-20260521T100634Z
```

Stop result:

```text
stop issued: 2026-05-21T10:17:27Z
stop API status: 202
post-stop status observed: 2026-05-21T10:18:19Z
final state: STOPPED (Completed)
execution type: STOP
completed timestamp: 2026-05-21 10:17:58
endpoint after stop: ssh -p 27021 root@10.100.22.14 refused connection
artifact preservation: /home/xu.yang/coding_agent_playground/outputs preserved on CephFS; shared mount path /mnt/cephfs/home/xu.yang/coding_agent_playground/outputs remains visible
eval: not run
```
