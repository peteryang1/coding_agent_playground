# dev_2 S23 PR63 Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PR63-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T18:12:07Z

Scope: PM-authorized exactly one fresh owner-executed post-PR63/PR64 preflight plus conditional SFT smoke. Eval is not authorized.

## Authorization

```text
PM evidence commit: 661a35e
authorization file: evidence/pm_s23_pr63_preflight_sft_authorization.md
PR #63 merged at: 2026-05-21T18:08:48Z
PR #63 merge commit: 2f89e9234bb5f9dfdcc433a30bc0f6dcfd9a8689
completion PR #64 merged at: 2026-05-21T18:12:07Z
origin/main commit to use: 7ad24ae328a350c0be596f41ea143affb4034486
authorized owner: intern_code_dev_2
authorized allocation count: exactly one fresh owner-executed runtime
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download on GPU node
output root: /home/xu.yang/coding_agent_playground/outputs
SFT condition: run SFT only if PREFLIGHT_RESULT=PASS and SFT_ALLOWED=true
PR63 launcher verification: direct */llamafactory/launcher.py invocation should normalize to python3 -m llamafactory.cli while preserving command-array parsing
eval: not authorized
```

## Local Source/Data/mcore Preparation

Prepared from local/provided workspace and local/provided dependency paths before any remote transfer.

```text
source repository: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486
commit: 7ad24ae328a350c0be596f41ea143affb4034486
worktree status: clean
file list: /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486_file_list.txt
file list count: 139
source bundle: /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486.tar.gz
source bundle sha256: 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
critical checksum file: /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486_critical_files.sha256
```

Dataset:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z/train.jsonl
dataset source: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

`mcore_adapter`:

```text
mcore_adapter source: /mnt/3fs/data/ai4ai/deps/mcore_adapter/src
mcore_adapter source type: local/provided source tree
mcore_adapter file list: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_file_list.txt
mcore_adapter file count: 222
mcore_adapter checksum manifest: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_files.sha256
mcore_adapter bundle: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z.tar.gz
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
LTP yaml: /tmp/coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z.yaml
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z
shape: single node, 8 x NVIDIA H200
initial no-active-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground -> No jobs found.
```

## LTP Allocation

```text
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z.yaml
submit response: status 202, Update job coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z for user xu.yang successfully.
frame: xu.yang~coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z
submitted: 2026-05-21 18:19:37
started: 2026-05-21 18:19:41
endpoint: ssh -p 17408 root@10.100.18.14
node: lg-cmc-b7r202-k07u06-h200-000580
initial GPU sample: all 8 NVIDIA H200 GPUs 0% util, 1 MiB memory used
```

## Storage and Capacity Proof

```text
ceph-fuse: /usr/bin/ceph-fuse
/mnt/cephfs mount: fuse.ceph-fuse
/home/xu.yang: symlink to /mnt/cephfs/home/xu.yang
output root: /home/xu.yang/coding_agent_playground/outputs
df output root: 18P size, 1.8P used, 16P available, 11% used
capacity probe path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z/capacity_probe_status.txt
capacity probe start: 2026-05-21T18:21:05Z
capacity probe end: 2026-05-21T18:21:31Z
expected bytes: 25769803776
actual bytes: 25769803776
status: PASS_AND_CLEANED
```

## Transfer and Verification

Transfer command:

```bash
scp -P 17408 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486.tar.gz \
  /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486_remote_bundle.sha256 \
  /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486_file_list.txt \
  /tmp/cap_s23_pr63_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_7ad24ae328a350c0be596f41ea143affb4034486_critical_files.sha256 \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z.tar.gz \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_remote_bundle.sha256 \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_file_list.txt \
  /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_files.sha256 \
  /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z/train.jsonl \
  /tmp/train_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z_remote.sha256 \
  /tmp/cap_pr55_pydeps_20260521T1505.tar.gz \
  /tmp/cap_pr55_pydeps_20260521T1505_remote.sha256 \
  /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz \
  /tmp/LLamaFactory_4fa8e1ee_20260507_remote.sha256 \
  /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl \
  /tmp/flash_attn_2.8.3_remote.sha256 \
  root@10.100.18.14:/root/workspace/
```

Post-transfer verification:

```text
remote workspace: /root/workspace
remote repo path: /root/workspace/coding_agent_playground
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
MCORE_ADAPTER_DIR: /root/workspace/coding_agent_playground/code/mcore_adapter
source bundle sha256: OK, 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
mcore_adapter bundle sha256: OK, 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
dataset sha256: OK, 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
python dependency bundle sha256: OK, e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
LLamaFactory bundle sha256: OK, f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
flash_attn wheel sha256: OK, c3941d81dd09fd1b39dc3df75097d8aa491250a551c919cd2e3c5df0a514fe0d
critical source checksums: OK
mcore_adapter file checksums: OK
remote source+dependency file count under repo: 1115
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

No remote `git clone`, `git fetch`, GitHub/source fetch, dependency download, or `pip download` was run. Local/provided wheels were installed with `pip install --no-index --no-deps --break-system-packages` from transferred files only. Generated outputs/logs/checkpoints/run metadata were restricted to `/home/xu.yang/coding_agent_playground/outputs`.

## Structured Preflight Result

Preflight artifacts:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z
health json: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z/health_status.json
health text: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z/health_status.txt
torch NCCL all-reduce log: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z/torch_nccl_allreduce_fixed.log
```

Structured result:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE
ACTIONABLE_FAULT=true
SFT_ALLOWED=false
SFT_ALLOWED_IF_PM_AUTHORIZED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=UNKNOWN
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=actionable GPU/NCCL health signature found
```

Actionable health signature details from `health_status.json`:

```text
source: dmesg_gpu_fault_scan.txt
fault type: sxid
code: 22013
freshness: unknown_time
example line: [Thu Feb  5 13:09:34 2026] nvidia-nvswitch2: SXid (PCI:0000:07:00.0): 22013, Non-fatal, Link 47 Minion Link DLREQ interrupt
node: lg-cmc-b7r202-k07u06-h200-000580
```

NCCL all-reduce itself completed:

```text
TORCHRUN_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
post-preflight GPU sample: all 8 H200 GPUs idle, 0% util, 1 MiB memory each
```

Per PM authorization, SFT may run only if `PREFLIGHT_RESULT=PASS` and `SFT_ALLOWED=true`. Because preflight failed and `SFT_ALLOWED=false`, I did not run SFT.

## SFT / Checkpoint Status

```text
SFT run: not run
reason: structured preflight failed with FAIL_HEALTH_SIGNATURE and SFT_ALLOWED=false
PR63 launcher normalization logs: not produced because SFT was not gateable
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run, not authorized
final blocker: BLOCKED_PR63_PREFLIGHT_HEALTH_SIGNATURE_SXID_22013
authorized retry remaining: no
```

## Stop Proof

Stop/release command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z
```

Stop response:

```text
STOP signal sent to xu.yang~coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z
status: 202
message: Execute job xu.yang~coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z successfully.
```

Post-stop status:

```text
Name:      coding-agent-playground-m1-s23-pr63-preflight-sft-20260521T181207Z
User:      xu.yang  (frame; detail endpoint omits username)
State:     STOPPED  (Completed)
ExecType:  STOP
Submitted: 2026-05-21 18:19:37
Started:   2026-05-21 18:19:41
Completed: 2026-05-21 18:26:03
Retries:   0
ExitCode:  -210  Failed
TaskRole idx 0: state=STOPPED, ip=10.100.18.14, ssh port=17408
```

Endpoint and no-active-job proof:

```text
endpoint command: ssh -p 17408 -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@10.100.18.14 'hostname'
endpoint result: ssh: connect to host 10.100.18.14 port 17408: Connection refused
running-list command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
running-list result: No jobs found.
```

Final outcome: `BLOCKED_WITH_FINAL_PREFLIGHT_EVIDENCE_STOPPED_NO_ACTIVE_GPU`. Fresh PM authorization is required before any further LTP/GPU/preflight/SFT/eval work.
