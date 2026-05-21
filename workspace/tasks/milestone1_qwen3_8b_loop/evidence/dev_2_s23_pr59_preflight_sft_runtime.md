# dev_2 S23 PR59 Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T16:34:13Z

Scope: PM-authorized exactly one fresh owner-executed runtime after PR #59 merge. Eval is not authorized.

## Authorization

```text
PR #59 merged at: 2026-05-21T16:34:13Z
merge commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
authorized owner: intern_code_dev_2
authorized allocation count: exactly one fresh runtime
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download on GPU node
output root: /home/xu.yang/coding_agent_playground/outputs
SFT condition: run SFT only if transfer/import/preflight PASS and SFT_ALLOWED=true
eval: not authorized
```

## Local Source/Data/mcore Preparation

Prepared from local/provided workspace and local/provided dependency paths before remote transfer.

```text
source repository: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr59_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_8ed6248cd7bd56b89ac1124689fed0b56e4eba02
commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
worktree status: clean
file list: /tmp/cap_s23_pr59_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_8ed6248cd7bd56b89ac1124689fed0b56e4eba02_file_list.txt
file list count: 131
source bundle: /tmp/cap_s23_pr59_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_8ed6248cd7bd56b89ac1124689fed0b56e4eba02.tar.gz
source bundle sha256: 2f272f210b67ed45b4a7b05592881c8c036fb34de2660645d6f96af76adf4d85
critical checksum file: /tmp/cap_s23_pr59_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_8ed6248cd7bd56b89ac1124689fed0b56e4eba02_critical_files.sha256
```

Dataset:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z/train.jsonl
dataset source: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

`mcore_adapter`:

```text
mcore_adapter source: /mnt/3fs/data/ai4ai/deps/mcore_adapter/src
mcore_adapter source type: local/provided source tree
mcore_adapter file list: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_file_list.txt
mcore_adapter file count: 222
mcore_adapter checksum manifest: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_files.sha256
mcore_adapter bundle: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z.tar.gz
mcore_adapter bundle sha256: ec0ace00eeca1f4d60710deea59621c868860e34827a5b645122f64f043170e7
```

Dependency bundles:

```text
LLamaFactory bundle: /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz
LLamaFactory sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
python dependency bundle: /tmp/cap_pr55_pydeps_20260521T1505.tar.gz
python dependency bundle sha256: e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
```

## LTP Allocation

```text
LTP yaml: /tmp/coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z.yaml
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
submitted: 2026-05-21 16:39:38
started: 2026-05-21 16:39:44
endpoint: ssh -p 27043 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
shape: single node, 8 x NVIDIA H200
initial gpu sample: all 8 GPUs 0% util, 1 MiB used
```

## Storage and Capacity Proof

`/home/xu.yang/coding_agent_playground/outputs` was not present at first SSH check, so I mounted/proved CephFS from the LTP bootstrap parameters before transfer/preflight/SFT.

```text
ceph-fuse: /usr/bin/ceph-fuse
/mnt/cephfs mount: fuse.ceph-fuse
/home/xu.yang: symlink to /mnt/cephfs/home/xu.yang
output root: /home/xu.yang/coding_agent_playground/outputs
df output root: 18P size, 1.8P used, 16P available, 10% used
capacity probe path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z/capacity_probe_status.txt
capacity probe start: 2026-05-21T16:41:01Z
capacity probe end: 2026-05-21T16:41:22Z
expected bytes: 25769803776
actual bytes: 25769803776
status: PASS_AND_CLEANED
```

## Transfer and Verification

Transfer command for source/data/mcore:

```bash
scp -P 27043 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cap_s23_pr59_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_8ed6248cd7bd56b89ac1124689fed0b56e4eba02.tar.gz \
  /tmp/cap_s23_pr59_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_8ed6248cd7bd56b89ac1124689fed0b56e4eba02_remote_bundle.sha256 \
  /tmp/cap_s23_pr59_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_8ed6248cd7bd56b89ac1124689fed0b56e4eba02_file_list.txt \
  /tmp/cap_s23_pr59_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_8ed6248cd7bd56b89ac1124689fed0b56e4eba02_critical_files.sha256 \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z.tar.gz \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_remote_bundle.sha256 \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_file_list.txt \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_files.sha256 \
  /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z/train.jsonl \
  /tmp/train_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z_remote.sha256 \
  root@10.100.22.28:/root/workspace/
```

Transfer command for local dependency bundles:

```bash
scp -P 27043 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cap_pr55_pydeps_20260521T1505.tar.gz \
  /tmp/cap_pr55_pydeps_20260521T1505_remote.sha256 \
  /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz \
  /tmp/LLamaFactory_4fa8e1ee_20260507_remote.sha256 \
  root@10.100.22.28:/root/workspace/
```

Post-transfer verification:

```text
remote workspace: /root/workspace
remote repo path: /root/workspace/coding_agent_playground
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
MCORE_ADAPTER_DIR: /root/workspace/coding_agent_playground/code/mcore_adapter
source bundle sha256: OK
mcore_adapter bundle sha256: OK
dataset sha256: OK
critical source checksums: OK
mcore_adapter file checksums: OK
remote source file count before mcore overlay: 131
remote source+workspace file count after mcore overlay: 347
remote mcore_adapter file count: 217
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Remote `mcore_adapter` import check before SFT:

```text
MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
PYTHONPATH=/root/workspace/coding_agent_playground/code/mcore_adapter:/root/workspace/coding_agent_playground/code/LLamaFactory/src:${PYTHONPATH:-}
result: mcore_adapter import OK for USE_MCA=1
module: /root/workspace/coding_agent_playground/code/mcore_adapter/mcore_adapter/__init__.py
```

No remote `git clone`, `git fetch`, GitHub/source fetch, dependency download, or `pip download` has been run.

Current status: `BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING_STOPPED`

## Structured Preflight Result

Preflight artifacts:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z
health json: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z/health_status.json
health text: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z/health_status.txt
torch NCCL all-reduce fixed log: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z/torch_nccl_allreduce_fixed.log
```

Final structured health result after preserving the successful all-reduce exit marker:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
SFT_ALLOWED_IF_PM_AUTHORIZED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=allowlisted preflight artifacts passed without actionable health signatures
```

Because transfer, `mcore_adapter` import, and structured preflight passed with `SFT_ALLOWED=true`, I ran exactly one SFT attempt. Eval was not run.

## SFT Runtime Result

Run metadata:

```text
run id: milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/logs/train_stdout_stderr.log
xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/logs/train_xtrace.log
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/config/qwen3_8b_sft.yaml
runtime config sha256: 0425900e30a5e043cb8447850d9e35cef1ed340a1ff76b040bebf82cddb02353
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/run_manifest.json
run manifest sha256: 57cd77b1b58702f4b57415c7c8d3f63a98fdb5efd2e535d83a707323b2c0d932
exit status: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/exit_status.txt
early diagnostics: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/early_exit_diagnostics.txt
final artifact summary: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/final_artifact_summary.txt
```

Runtime command path:

```text
wrapper: /root/workspace/launch_pr59_sft_systemdeps.sh
invocation: PYTHONPATH=/root/workspace/coding_agent_playground/code/mcore_adapter:${PYTHONPATH:-} /root/workspace/launch_pr59_sft_systemdeps.sh
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
CONFIG_TEMPLATE=configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
max_steps=2
save_steps=2
save_total_limit=1
MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
```

Before invoking training, the wrapper proved:

```text
flash_attn import OK /usr/local/lib/python3.12/dist-packages/flash_attn/__init__.py
mcore_adapter import OK /root/workspace/coding_agent_playground/code/mcore_adapter/mcore_adapter/__init__.py
mcore_adapter import OK for USE_MCA=1.
```

The only authorized SFT attempt failed before training/checkpoint generation:

```text
EXIT_STATUS=127
END_UTC=2026-05-21T16:51:05Z
failure signature: scripts/train_qwen3_8b_sft.sh: line 244: python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py: No such file or directory
diagnostic reason: DIAGNOSTIC_REASON=ERR_TRAP
error line: ERROR_LINE=244
```

Classification:

```text
final blocker: BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING
root cause: LLAMAFACTORY_CLI was set to the space-containing command string `python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`, but `scripts/train_qwen3_8b_sft.sh` executes `"${LLAMAFACTORY_CLI}" train ...` as a single command path.
next fix: make the launcher support command-plus-args safely, or set LLAMAFACTORY_CLI to a real executable/wrapper path without embedded spaces.
authorized retry remaining: no
```

Final artifact summary:

```text
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run, not authorized
post-failure train processes: none observed
post-failure GPU state: all 8 H200 GPUs idle, 0% util, 1 MiB memory each
outputs preserved: yes, under /home/xu.yang/coding_agent_playground/outputs
```

Dependency staging note: all source/data/dependency artifacts were transferred from local/provided paths. No remote source/dependency network fetch was run. The wrapper installed already-transferred local wheel artifacts into system Python with `--no-index --no-deps --break-system-packages` because CephFS did not allow reliable pip/tar metadata extraction for the dependency tree. SFT outputs/logs/checkpoints/run metadata remained under `/home/xu.yang/coding_agent_playground/outputs`.

## Stop Proof

Stop/release command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
```

Stop response:

```text
STOP signal sent for frame xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
status: 202
message: Execute job xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z successfully.
```

Post-stop status checked at `2026-05-21T16:53:07Z`:

```text
Name:      coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
User:      xu.yang  (frame; detail endpoint omits username)
State:     STOPPED  (Completed)
ExecType:  STOP
Submitted: 2026-05-21 16:39:38
Started:   2026-05-21 16:39:44
Completed: 2026-05-21 16:52:02
Retries:   0
ExitCode:  -210  Failed
TaskRole idx 0: state=STOPPED, ip=10.100.22.28, ssh port=27043
```

Endpoint and no-active-job proof:

```text
endpoint command: ssh -p 27043 -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@10.100.22.28 'hostname'
endpoint result: ssh: connect to host 10.100.22.28 port 27043: Connection refused
running-list command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
running-list result: No jobs found.
```

Final outcome: `BLOCKED_WITH_FINAL_RUNTIME_EVIDENCE_STOPPED_NO_ACTIVE_GPU`. Fresh PM authorization is required before any further LTP/GPU/preflight/SFT/eval work.
