# dev_2 S23 PR61 Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PR61-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T17:15:51Z

Scope: PM-authorized exactly one fresh owner-executed runtime after PR #61 and completion PR #62. Eval is not authorized.

## Authorization

```text
PR #61 merged at: 2026-05-21T17:13:17Z
PR #61 merge commit: aa426b045b52b71bc23b4a2f73f3ee1c42187037
completion PR #62 merged at: 2026-05-21T17:15:51Z
origin/main commit to use: 713862da983f73b165af1cfe27935ccef616a049
authorized owner: intern_code_dev_2
authorized allocation count: exactly one fresh owner-executed runtime
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download on GPU node
output root: /home/xu.yang/coding_agent_playground/outputs
SFT condition: run SFT only if transfer/import/preflight PASS and SFT_ALLOWED=true
PR61 CLI fix verification: LLAMAFACTORY_CLI may be a command string; logs/manifest should show parsed LLAMAFACTORY_CMD and prior quoted single-path signature must not recur
eval: not authorized
```

## Local Source/Data/mcore Preparation

Prepared from local/provided workspace and local/provided dependency paths before any remote transfer.

```text
source repository: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049
commit: 713862da983f73b165af1cfe27935ccef616a049
worktree status: clean
file list: /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049_file_list.txt
file list count: 135
source bundle: /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049.tar.gz
source bundle sha256: a8aeb73d6f3c69775997b7c4b6cf49344a0e8691a44811b68d5678caaacb83c4
critical checksum file: /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049_critical_files.sha256
```

Dataset:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z/train.jsonl
dataset source: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

`mcore_adapter`:

```text
mcore_adapter source: /mnt/3fs/data/ai4ai/deps/mcore_adapter/src
mcore_adapter source type: local/provided source tree
mcore_adapter file list: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_file_list.txt
mcore_adapter file count: 222
mcore_adapter checksum manifest: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_files.sha256
mcore_adapter bundle: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z.tar.gz
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
```

Dependency bundles:

```text
LLamaFactory bundle: /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz
LLamaFactory sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
python dependency bundle: /tmp/cap_pr55_pydeps_20260521T1505.tar.gz
python dependency bundle sha256: e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
flash_attn wheel: /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
flash_attn sha256: c3941d81dd09fd1b39dc3df75097d8aa491250a551c919cd2e3c5df0a514fe0d
```

## LTP Allocation Plan

```text
LTP yaml: /tmp/coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z.yaml
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
shape: single node, 8 x NVIDIA H200
initial no-active-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground -> No jobs found.
```

## LTP Allocation

```text
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z.yaml
submit response: status 202, Update job coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z for user xu.yang successfully.
frame: xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
submitted: 2026-05-21 17:22:24
started: 2026-05-21 17:22:28
endpoint: ssh -p 33089 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
initial GPU sample: all 8 NVIDIA H200 GPUs 0% util, 1 MiB memory used
```

## Storage and Capacity Proof

`/home/xu.yang/coding_agent_playground/outputs` was not present at first SSH check, so I mounted/proved CephFS from the LTP bootstrap parameters before transfer/preflight/SFT.

```text
ceph-fuse: /usr/bin/ceph-fuse
/mnt/cephfs mount: fuse.ceph-fuse
/home/xu.yang: symlink to /mnt/cephfs/home/xu.yang
output root: /home/xu.yang/coding_agent_playground/outputs
df output root: 18P size, 1.8P used, 16P available, 11% used
capacity probe path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z/capacity_probe_status.txt
capacity probe start: 2026-05-21T17:23:57Z
capacity probe end: 2026-05-21T17:24:17Z
expected bytes: 25769803776
actual bytes: 25769803776
status: PASS_AND_CLEANED
```

## Transfer and Verification

Transfer command:

```bash
scp -P 33089 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049.tar.gz \
  /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049_remote_bundle.sha256 \
  /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049_file_list.txt \
  /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049_critical_files.sha256 \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z.tar.gz \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_remote_bundle.sha256 \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_file_list.txt \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_files.sha256 \
  /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z/train.jsonl \
  /tmp/train_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_remote.sha256 \
  /tmp/cap_pr55_pydeps_20260521T1505.tar.gz \
  /tmp/cap_pr55_pydeps_20260521T1505_remote.sha256 \
  /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz \
  /tmp/LLamaFactory_4fa8e1ee_20260507_remote.sha256 \
  /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl \
  /tmp/flash_attn_2.8.3_remote.sha256 \
  root@10.100.22.31:/root/workspace/
```

Post-transfer verification:

```text
remote workspace: /root/workspace
remote repo path: /root/workspace/coding_agent_playground
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
MCORE_ADAPTER_DIR: /root/workspace/coding_agent_playground/code/mcore_adapter
source bundle sha256: OK, a8aeb73d6f3c69775997b7c4b6cf49344a0e8691a44811b68d5678caaacb83c4
mcore_adapter bundle sha256: OK, 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
dataset sha256: OK, 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
python dependency bundle sha256: OK, e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
LLamaFactory bundle sha256: OK, f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
flash_attn wheel sha256: OK, c3941d81dd09fd1b39dc3df75097d8aa491250a551c919cd2e3c5df0a514fe0d
critical source checksums: OK
mcore_adapter file checksums: OK
remote source+dependency file count under repo: 1111
remote mcore_adapter file count: 222
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Remote `mcore_adapter` import check before preflight/SFT:

```text
MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
PYTHONPATH=/root/workspace/coding_agent_playground/code/mcore_adapter:/root/workspace/coding_agent_playground/code/LLamaFactory/src:${PYTHONPATH:-}
result: mcore_adapter import OK for USE_MCA=1
module: /root/workspace/coding_agent_playground/code/mcore_adapter/mcore_adapter/__init__.py
```

No remote `git clone`, `git fetch`, GitHub/source fetch, dependency download, or `pip download` was run. Local/provided wheels were installed with `pip install --no-index --no-deps --break-system-packages` from transferred files only; this was needed because prior CephFS Python dependency extraction was unreliable. Generated outputs/logs/checkpoints/run metadata stayed under `/home/xu.yang/coding_agent_playground/outputs`.

## Structured Preflight Result

Preflight artifacts:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z
health json: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z/health_status.json
health text: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z/health_status.txt
torch NCCL all-reduce fixed log: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z/torch_nccl_allreduce_fixed.log
```

The first preflight wrapper write hit a CephFS file timestamp/append permission issue after producing `ALLREDUCE_OK`; I preserved the generated artifacts, wrote a fixed all-reduce log/status under the same `/home/xu.yang` preflight directory, and ran the structured parser over those artifacts. Final structured result:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
SFT_ALLOWED_IF_PM_AUTHORIZED=true
SFT_SKIP_REASON=
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=UNKNOWN
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=allowlisted preflight artifacts passed without actionable health signatures
```

Because transfer, `mcore_adapter` import, and structured preflight passed with `SFT_ALLOWED=true`, I ran exactly one SFT attempt. Eval was not run.

## SFT Runtime Result

Run metadata:

```text
run id: milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z/logs/train_stdout_stderr.log
xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z/logs/train_xtrace.log
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z/config/qwen3_8b_sft.yaml
runtime config sha256: 4f22228204bab055c982d2c9046877b26146833be93ea5da0c59b582ee72b75a
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z/run_manifest.json
run manifest sha256: 210633469ab3dbfed7546ec01d818957c1f73cae2b4ef1f8fd472cbd3c8e7f7c
exit status: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z/exit_status.txt
early diagnostics: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z/early_exit_diagnostics.txt
final artifact summary: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z/final_artifact_summary.txt
```

Runtime command path:

```text
wrapper: /root/workspace/launch_pr61_sft.sh
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
max_steps=2
save_steps=2
save_total_limit=1
MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
LLAMAFACTORY_CLI=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
```

PR61 CLI fix verification:

```text
log line: LLAMAFACTORY_CLI=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
log line: LLAMAFACTORY_CMD=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
prior quoted single-path signature: not observed
launcher reached: yes, traceback originates in /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
```

Runtime config proof:

```text
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
preprocessing_num_workers: null
dataloader_num_workers: 0
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
save_steps: 2
save_total_limit: 1
max_steps: 2
```

The only authorized SFT attempt failed before checkpoint/training:

```text
EXIT_STATUS=1
END_UTC=2026-05-21T17:31:39Z
failure signature: ValueError: Please provide `model_name_or_path`.
trace path: llamafactory/launcher.py -> train/tuner.py -> hparams/parser.py -> model_args.py
diagnostic reason: DIAGNOSTIC_REASON=ERR_TRAP
error line: ERROR_LINE=266
```

Classification:

```text
final blocker: BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE
root cause observed: generated runtime YAML contains `model_name_or_path`, but LLamaFactory MCA argument parsing still raised `ValueError: Please provide model_name_or_path` before training/checkpoint work. This is distinct from the PR59 quoted single-path CLI bug because `LLAMAFACTORY_CMD` was parsed and launcher.py was reached.
next fix: inspect LLamaFactory MCA parser/config path for why `model_name_or_path` from the generated YAML is not bound for MCA mode, then re-gate before any further runtime.
authorized retry remaining: no
```

Final artifact summary:

```text
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run, not authorized
post-failure train processes: none observed except the artifact-summary command itself
post-failure GPU state: all 8 H200 GPUs idle, 0% util, 1 MiB memory each
outputs preserved: yes, under /home/xu.yang/coding_agent_playground/outputs
```

## Stop Proof

Stop/release command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
```

Stop response:

```text
STOP signal sent to xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
status: 202
message: Execute job xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z successfully.
```

Post-stop status checked after stop:

```text
Name:      coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
User:      xu.yang  (frame; detail endpoint omits username)
State:     STOPPED  (Completed)
ExecType:  STOP
Submitted: 2026-05-21 17:22:24
Started:   2026-05-21 17:22:28
Completed: 2026-05-21 17:32:52
Retries:   0
ExitCode:  -210  Failed
TaskRole idx 0: state=STOPPED, ip=10.100.22.31, ssh port=33089
```

Endpoint and no-active-job proof:

```text
endpoint command: ssh -p 33089 -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@10.100.22.31 'hostname'
endpoint result: ssh: connect to host 10.100.22.31 port 33089: Connection refused
running-list command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
running-list result: No jobs found.
```

Final outcome: `BLOCKED_WITH_FINAL_RUNTIME_EVIDENCE_STOPPED_NO_ACTIVE_GPU`. Fresh PM authorization is required before any further LTP/GPU/preflight/SFT/eval work.
