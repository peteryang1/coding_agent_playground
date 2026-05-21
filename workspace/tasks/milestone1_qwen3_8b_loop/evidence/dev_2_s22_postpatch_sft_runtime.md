# dev_2 S22 Post-PR39 SFT Runtime

Task ID: `M1-S22-POSTPATCH-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T09:24:00Z

Scope: exactly one PM-authorized post-PR #39 ShareGPT-fixed Qwen3-8B SFT smoke attempt.

Authorization:

```text
PM authorization: 2026-05-21T09:18:03Z
PR #39 merged: 2026-05-21T09:17:15Z
PR #39 merge commit: 4a6c2968e1290d30415460b464eee638110958bc
authorized owner: intern_code_dev_2
authorized attempts: one SFT smoke
eval authorized: false
```

Code source:

```text
source method: independent temporary clone, not PM shared dirty worktree
clone path: /tmp/cap_pr39_runtime_repo
checked out commit: 4a6c2968e1290d30415460b464eee638110958bc
```

Storage contract:

```text
output_root: /home/xu.yang/coding_agent_playground/outputs
all SFT outputs/logs/checkpoints/run metadata/capacity probes/intermediates must stay under output_root unless an existing required input path is explicitly justified.
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
RUNTIME_ID=20260521T092458Z
JOB_NAME=coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z
FRAME=xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z
LTP_YAML=/tmp/coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z.yaml
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit "${LTP_YAML}"
```

Submit result:

```text
status: 202
message: Update job coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z for user xu.yang successfully.
```

Initial status:

```text
state: RUNNING (AttemptRunning)
submitted: 2026-05-21 09:24:58
started: 2026-05-21 09:25:02
ip: 10.100.24.11
ssh port: 38445
endpoint: ssh -p 38445 root@10.100.24.11
```

## Mount And Capacity Proof

Bootstrap observation:

```text
2026-05-21T09:25:42Z
hostname: lg-cmc-b7r401-a04u26-h200-000769
bootstrap still running apt install
/home/xu.yang missing
/mnt/cephfs/home/xu.yang missing
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB memory used each
SFT: not started
```

Bootstrap complete:

```text
2026-05-21T09:27:56Z
sleep infinity running
ceph-fuse running
/mnt/cephfs: fuse.ceph-fuse
/mnt/3fs: fuse.hf3fs
/mnt/cephfs/home/xu.yang exists
/home/xu.yang missing
```

Path fix applied on worker:

```bash
ln -s /mnt/cephfs/home/xu.yang /home/xu.yang
mkdir -p /home/xu.yang/coding_agent_playground/outputs
```

Justification: LTP mounted CephFS at `/mnt/cephfs`; PM requires `/home/xu.yang/coding_agent_playground/outputs`, so `/home/xu.yang` was created as an entry to the CephFS home.

Post-fix proof:

```text
2026-05-21T09:28:11Z
hostname: lg-cmc-b7r401-a04u26-h200-000769
readlink -f /home/xu.yang: /mnt/cephfs/home/xu.yang
findmnt -T /home/xu.yang: /mnt/cephfs fuse.ceph-fuse ceph-fuse
df: ceph-fuse 18P size, 1.8P used, 16P available, 10% use
GPU: 8 x NVIDIA H200 idle, 0% util, 1 MiB memory used each
```

Capacity probe command:

```bash
RUN_ID=milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
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
2026-05-21T09:28:25Z start
path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
findmnt: /mnt/cephfs fuse.ceph-fuse ceph-fuse
files: 4 x 6.0G real dd writes with conv=fsync
bytes verified by du -sb: 25769803776
file_count: 4
cleanup: probe files and directory removed
2026-05-21T09:28:54Z
PROBE_STATUS=PASS_AND_CLEANED
```

## Runtime Command

Staging completed:

```text
2026-05-21T09:30:04Z
/root/workspace/coding_agent_playground staged from /tmp/cap_pr39_runtime_repo
git HEAD on worker: 4a6c2968e1290d30415460b464eee638110958bc
/root/workspace/cleaned_m1_sft_10_sharegpt staged
source dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
source dataset rows: 10
script sha256: 28302cf7322d713038485c213837cd749738d23d56561da973bddb03d6afc356
manifest writer sha256: 65c8bbc39d77abf850c1b933cd25272406aedcc3ff1f025c5f01e975ec46c4cb
config template sha256: 560e776615180107013f993a28175dfe6f025c8cf874164632d36f4d95c656fc
```

Runtime dependencies and dataset_info:

```text
2026-05-21T09:30:48Z
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
path: /home/xu.yang/coding_agent_playground/outputs/milestone1_s22_postpatch_nodes.json
sha256: 0eb120e9e6229795cdf80925841755fa369a7c44943c336eeffb0706dbd21c98
content: {"node_count":1,"nodes":[{"ip":"10.100.24.11","port":"38445","user":"root","node_rank":0,"hostname":"lg-cmc-b7r401-a04u26-h200-000769"}]}
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
RUN_ID=milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z \
DRY_RUN=0 \
SFT_XTRACE=1 \
bash scripts/train_qwen3_8b_sft.sh
```

Run paths:

```text
run_id: milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
run_dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/logs/train_stdout_stderr.log
xtrace: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/logs/train_xtrace.log
diagnostics: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/early_exit_diagnostics.txt
manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/run_manifest.json
runtime_config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/config/qwen3_8b_sft.yaml
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
```

Launch:

```text
2026-05-21T09:31:23Z
tmux session: s22_postpatch_sft
attempt count: 1 authorized SFT attempt started
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
exit_status_path: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/exit_status.txt
EXIT_STATUS=1
END_UTC=2026-05-21T09:32:16Z
```

Post-run node/GPU observation before stop:

```text
2026-05-21T09:33:10Z
training processes: none observed
GPU: all 8 H200 idle, 0% util, 1 MiB memory each
LTP state: RUNNING before explicit stop
```

Durable artifacts produced by PR #39 wrapper:

```text
1397 preflight.json
1522 config/qwen3_8b_sft.yaml
1709 early_exit_diagnostics.txt
22479 logs/train_stdout_stderr.log
43 exit_status.txt
4704 run_manifest.json
9612 logs/train_xtrace.log
```

CephFS preserved artifact paths, visible after stop:

```text
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/preflight.json
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/run_manifest.json
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/config/qwen3_8b_sft.yaml
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/logs/train_stdout_stderr.log
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/logs/train_xtrace.log
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/early_exit_diagnostics.txt
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z/exit_status.txt
```

Artifact sha256:

```text
preflight.json: b67192fd7e9d6777fa00b9b8a954eb36acc7ddf0aa95869032787184c008f4be
run_manifest.json: 293a496db8877f17a0f75e5c1004519ecbeb332e4eafb8d79c23b2baaa546f87
config/qwen3_8b_sft.yaml: b72358549025622fcefdf976c9349ffcba079a8748e73ebde7eeb20f2bc173f8
logs/train_stdout_stderr.log: 50ac9957c824e3289b990ba3c81c5aeb4fd32ca36a060ee70213e94c91b7ccbc
logs/train_xtrace.log: 2e020ecd44e94611d7da49e413dbb4aadfdef659275fb6c4056b46426672dce3
early_exit_diagnostics.txt: fb7694783fd685199338b9c2205bdef399cf590bf4f6f45de3ac08a84ad09c27
exit_status.txt: 6b5751e5d142fd77806fd1ca584f64fe43a982f625141c7d2c96bccd11134edb
```

Generated config proof:

```text
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset_dir: data/sft
dataset: coding_agent_m1_sft_10_sharegpt
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
save_steps: 2
save_total_limit: 1
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
```

Run manifest proof:

```text
git_commit: 4a6c2968e1290d30415460b464eee638110958bc
dataset_name: coding_agent_m1_sft_10_sharegpt
train_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
save_steps: 2
save_total_limit: 1
save_only_model: true
save_hf_model: true
preflight log/xtrace/diagnostics paths recorded
```

Checkpoint/model artifacts:

```text
checkpoint_root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s22_postpatch_sharegpt_tp8_maxsteps2_20260521T092458Z
checkpoint files: absent
complete checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
```

Failure signature:

```text
Failure occurred during LLamaFactory dataset conversion before training steps/checkpoint save.
Log shows: Converting format of dataset (num_proc=4): 0/10
Rank0 traceback: datasets.arrow_dataset.map -> multiprocess.managers.Manager.start -> reader.recv -> EOFError
Torch elastic root cause: ChildFailedError from local_rank 0 / llamafactory launcher, exitcode 1
PR39 diagnostics: DIAGNOSTIC_REASON=ERR_TRAP, ERROR_EXIT=1, ERROR_LINE=209
```

Old failure signatures:

```text
KeyError: 'from': not observed
No space left on device: not observed
safetensors ENOSPC: not observed
checkpoint save failure: not reached
training step progress: not reached
```

Fresh runtime blocker:

```text
BLOCKED_POSTPATCH_RUNTIME_DATASET_MAP_EOF: The post-PR39 wrapper fixed the previous early-exit observability gap and produced preflight/config/manifest/xtrace/diagnostics. The one authorized SFT attempt still failed before training while converting the accepted ShareGPT dataset with preprocessing_num_workers=4 / datasets map num_proc=4. The concrete failure is a multiprocessing SyncManager EOFError in datasets.map. No same-node retry was authorized or performed.
```

Owner next fix recommendation:

```text
For the next no-execution config fix, set dataset preprocessing to single-process for the 10-row smoke, for example preprocessing_num_workers: 1 or 0 in the SFT config/template, then have dev_1/test_1 re-gate before any further PM runtime authorization. Keep PR39 diagnostics and /home/xu.yang output paths.
```

## Stop Proof

Stop command:

```bash
FRAME=xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop "${FRAME}"
```

Stop issued:

```text
2026-05-21T09:33:26Z
STOP signal sent
status: 202
```

Post-stop status:

```text
2026-05-21T09:34:08Z
State: STOPPED (Completed)
ExecType: STOP
Submitted: 2026-05-21 09:24:58
Started: 2026-05-21 09:25:02
Completed: 2026-05-21 09:33:57
ExitCode: -210 Failed
task idx 0: STOPPED
```

Endpoint proof:

```text
ssh -p 38445 root@10.100.24.11
result after STOPPED: connection refused
confirmed at 2026-05-21T09:34:08Z, 2026-05-21T09:34:28Z, 2026-05-21T09:34:48Z, and 2026-05-21T09:35:08Z
```

Artifact preservation note:

```text
CephFS output root is preserved:
/home/xu.yang/coding_agent_playground/outputs

After node stop, the same files are visible from shared CephFS:
/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs

No cleanup of runtime artifacts was performed.
No eval was run.
```
