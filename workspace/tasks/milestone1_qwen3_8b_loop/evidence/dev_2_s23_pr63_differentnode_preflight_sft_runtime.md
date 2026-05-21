# dev_2 S23 PR63 Different-Node Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PR63-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T18:12:07Z

Scope: PM-authorized exactly one fresh bounded different-node preflight plus conditional SFT smoke. Eval is not authorized.

## Authorization

```text
PM evidence commit: 0551dc8
authorization file: evidence/pm_s23_pr63_differentnode_preflight_sft_authorization.md
runtime source commit: 7ad24ae328a350c0be596f41ea143affb4034486
forbidden node: lg-cmc-b7r202-k07u06-h200-000580
authorized owner: intern_code_dev_2
authorized allocation count: exactly one fresh bounded different-node attempt
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download on GPU node
output root: /home/xu.yang/coding_agent_playground/outputs
SFT condition: run SFT only if PREFLIGHT_RESULT=PASS and SFT_ALLOWED=true
eval: not authorized
```

## Local Package Reuse

Reused the local/provided source/data/dependency bundles prepared for the immediately prior PR63 authorized runtime because the source commit and data contract are unchanged.

```text
source bundle: /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486.tar.gz
source bundle sha256: 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
source file list: /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486_file_list.txt
source file count: 139
critical checksum file: /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486_critical_files.sha256
dataset: /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
mcore_adapter bundle: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z.tar.gz
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
mcore_adapter file count: 222
LLamaFactory bundle: /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz
LLamaFactory sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
python dependency bundle: /tmp/cap_pr55_pydeps_20260521T1505.tar.gz
python dependency bundle sha256: e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
flash_attn wheel: /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
flash_attn sha256: c3941d81dd09fd1b39dc3df75097d8aa491250a551c919cd2e3c5df0a514fe0d
```

## LTP Allocation Plan

```text
LTP yaml: /tmp/coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z.yaml
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z
initial no-active-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground -> No jobs found.
```

## LTP Submit, Placement, and Storage

```text
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z.yaml
submit result: HTTP 202 accepted
frame: xu.yang~coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z
started: 2026-05-21 18:34:09
endpoint: ssh -p 27957 root@10.100.22.31
assigned node: lg-cmc-b7r202-q04u06-h200-000725
forbidden node: lg-cmc-b7r202-k07u06-h200-000580
placement decision: PASS, assigned node differs from forbidden node
GPU shape observed: 8 x NVIDIA H200, idle before transfer
```

The remote node initially had `/home/xu.yang` on overlay. I corrected the output-root bootstrap before generated artifacts by removing the empty overlay path and linking `/home/xu.yang -> /mnt/cephfs/home/xu.yang`. Post-correction proof:

```text
HOME_REAL=/mnt/cephfs/home/xu.yang
findmnt target: /mnt/cephfs
source: ceph-fuse
fstype: fuse.ceph-fuse
df: 18P size, 1.8P used, 16P available, 11% used
output root: /home/xu.yang/coding_agent_playground/outputs
```

Capacity probe:

```text
probe dir: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr63_differentnode_preflight_sft_20260521T181207Z
START_UTC=2026-05-21T18:35:22Z
END_UTC=2026-05-21T18:35:42Z
EXPECTED_BYTES=25769803776
ACTUAL_BYTES=25769803776
STATUS=PASS_AND_CLEANED
```

## Transfer and Remote Verification

Exact transfer command:

```bash
scp -P 27957 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cap_s23_pr63_${RUN_ID}_7ad24ae328a350c0be596f41ea143affb4034486.tar.gz \
  /tmp/cap_s23_pr63_${RUN_ID}_7ad24ae328a350c0be596f41ea143affb4034486_remote_bundle.sha256 \
  /tmp/cap_s23_pr63_${RUN_ID}_7ad24ae328a350c0be596f41ea143affb4034486_file_list.txt \
  /tmp/cap_s23_pr63_${RUN_ID}_7ad24ae328a350c0be596f41ea143affb4034486_critical_files.sha256 \
  /tmp/mcore_adapter_${RUN_ID}.tar.gz \
  /tmp/mcore_adapter_${RUN_ID}_remote_bundle.sha256 \
  /tmp/mcore_adapter_${RUN_ID}_file_list.txt \
  /tmp/mcore_adapter_${RUN_ID}_files.sha256 \
  /tmp/cleaned_m1_sft_10_sharegpt_${RUN_ID}/train.jsonl \
  /tmp/train_${RUN_ID}_remote.sha256 \
  /tmp/cap_pr55_pydeps_20260521T1505.tar.gz \
  /tmp/cap_pr55_pydeps_20260521T1505_remote.sha256 \
  /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz \
  /tmp/LLamaFactory_4fa8e1ee_20260507_remote.sha256 \
  /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl \
  /tmp/flash_attn_2.8.3_remote.sha256 \
  root@10.100.22.31:/root/workspace/
```

Remote verification:

```text
source bundle sha256: OK 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
mcore bundle sha256: OK 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
train.jsonl sha256: OK 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
python dependency bundle sha256: OK e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
LLamaFactory sha256: OK f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
flash_attn sha256: OK c3941d81dd09fd1b39dc3df75097d8aa491250a551c919cd2e3c5df0a514fe0d
remote source path: /root/workspace/coding_agent_playground
remote source count: 1115
remote mcore path: /root/workspace/coding_agent_playground/code/mcore_adapter
remote mcore count: 222
remote data path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
critical source checksum verification: PASS
mcore checksum verification: PASS
no remote source/dependency network: preserved; all source/data/deps were transferred from local/provided bundles
```

Local wheel installation used only transferred artifacts with `pip install --no-index --no-deps --break-system-packages`. Import proof:

```text
fire import OK
tyro import OK
peft import OK
trl import OK
typeguard import OK
flash_attn import OK
mcore_adapter import OK for USE_MCA=1
MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
```

Dataset info files written and checksummed:

```text
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json sha256 8af53c474f05a73c39123e5a5f49b3844a8f39898f439e00c19ff1140edb77fe
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json sha256 e2a8f6f1e0cfaee2769b5a669a6cf2cd1827440ed97aa25a9de9c9cd9cd7663e
```

## Structured Preflight

Preflight command:

```text
ssh -p 27957 root@10.100.22.31 /root/workspace/run_pr63_diff_preflight.sh
```

Preflight artifacts:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_differentnode_preflight_sft_20260521T181207Z
health json: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_differentnode_preflight_sft_20260521T181207Z/health_status.json
health text: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_differentnode_preflight_sft_20260521T181207Z/health_status.txt
torch all-reduce log: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_differentnode_preflight_sft_20260521T181207Z/torch_nccl_allreduce.log
```

Structured result:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
SFT_ALLOWED_IF_PM_AUTHORIZED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=allowlisted preflight artifacts passed without actionable health signatures
```

Because structured preflight passed and `SFT_ALLOWED=true`, I ran the single authorized SFT attempt.

## SFT Attempt

SFT command:

```text
ssh -p 27957 root@10.100.22.31 /root/workspace/launch_pr63_diff_sft.sh
```

SFT environment and paths:

```text
RUN_ID=milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
RUN_DIR=/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z
CHECKPOINT_DIR=/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z
TMPDIR=/home/xu.yang/coding_agent_playground/outputs/tmp/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory
MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
USE_MCA=1
FORCE_TORCHRUN=1
NCCL_DEBUG=INFO
NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL
NCCL_ASYNC_ERROR_HANDLING=1
TORCH_NCCL_ASYNC_ERROR_HANDLING=1
CUDA_DEVICE_MAX_CONNECTIONS=1
NCCL_IB_DISABLE=1
NCCL_P2P_LEVEL=NVL
```

Runtime proof:

```text
flash_attn import OK
mcore_adapter import OK for USE_MCA=1
LLAMAFACTORY_CLI=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
LLAMAFACTORY_CMD_ORIGINAL=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
LLAMAFACTORY_CMD_NORMALIZATION=direct_launcher_py_to_module_cli
LLAMAFACTORY_CMD=python3 -m llamafactory.cli
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z/config/qwen3_8b_sft.yaml
runtime config sha256: 1d7b2b4b165477c1b36052129ab447608f5ccda50073c3a2295a28b5bb620d73
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z/run_manifest.json
run manifest sha256: a20fb638644945bb903bcb2b7822689325b7c415a865c61d5ed6ba47e61dca69
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
ShareGPT conversion: 10 examples generated and converted
training reached: mcore_adapter model load, mpu initialization, and "***** Running training *****"
Num examples: 1
Total optimization steps: 2
```

SFT final result:

```text
exit status: 1
failure time: 2026-05-21T18:42:28Z
diagnostic reason: ERR_TRAP
root failure signature: CUDA error: Invalid access of peer GPU memory over nvlink or a hardware error
torch elastic root cause: rank 4 local_rank 4 exitcode -6 SIGABRT
NCCL/process group signatures: DATA_PARALLEL_GROUP_WITH_CP and TENSOR_MODEL_PARALLEL_GROUP watchdog exceptions
classification: BLOCKED_PR63_DIFFERENTNODE_RUNTIME_NCCL_NVLINK_PEER_MEMORY
```

Checkpoint/model/trainer outputs:

```text
checkpoint dir exists: yes
checkpoint/model files: none
trainer_state.json: absent
all_results.json: absent
only checkpoint-side artifact observed: TensorBoard event file under CHECKPOINT_DIR/runs/May22_02-40-49_lg-cmc-b7r202-q04u06-h200-000725/
eval: not run, not authorized
```

Preserved artifact paths:

```text
preflight health json: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_differentnode_preflight_sft_20260521T181207Z/health_status.json
preflight health text: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_differentnode_preflight_sft_20260521T181207Z/health_status.txt
train stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z/logs/train_stdout_stderr.log
train xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z/logs/train_xtrace.log
early exit diagnostics: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z/early_exit_diagnostics.txt
exit status: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z/exit_status.txt
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z/config/qwen3_8b_sft.yaml
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z/run_manifest.json
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr63_differentnode_sft_20260521T181207Z
```

## Stop Proof

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z
stop command time: 2026-05-21T18:42:50Z
stop result: HTTP 202 accepted, "Execute job ... successfully."
post-stop status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr63-differentnode-preflight-sft-20260521T181207Z
final LTP state: STOPPED (Completed)
final LTP completed: 2026-05-21 18:43:25
final task idx state: STOPPED
endpoint proof: ssh -p 27957 root@10.100.22.31 hostname -> Connection refused
no-running-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground -> No jobs found.
artifact preservation: generated artifacts remain under /home/xu.yang/coding_agent_playground/outputs on CephFS
```

Final status: `BLOCKED_WITH_FINAL_RUNTIME_EVIDENCE_STOPPED_NO_RETRY_AUTHORIZED`

Fresh PM authorization is required before any further LTP/GPU/preflight/SFT/eval work.
