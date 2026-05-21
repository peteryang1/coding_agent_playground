# dev_2 S23 PR63 Placement Retry 2 Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PR63-PLACEMENTRETRY2-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T18:59:30Z

Scope: PM-authorized exactly one fresh bounded placement-retry allocation, then preflight plus conditional SFT only if placement and gates pass. Eval is not authorized.

## Authorization

```text
PM evidence commit: 9790169
authorization file: evidence/pm_s23_pr63_placementretry2_preflight_sft_authorization.md
runtime source commit: 7ad24ae328a350c0be596f41ea143affb4034486
forbidden nodes:
- lg-cmc-b7r202-k07u06-h200-000580
- lg-cmc-b7r202-q04u06-h200-000725
authorized owner: intern_code_dev_2
authorized allocation count: exactly one fresh bounded placement retry
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download on GPU node
output root: /home/xu.yang/coding_agent_playground/outputs
SFT condition: run SFT only if PREFLIGHT_RESULT=PASS and SFT_ALLOWED=true
eval: not authorized
```

## Local Package Reuse

Reused the local/provided source/data/dependency bundles prepared for the PR63/PR64 runtime path because the source commit and data contract are unchanged.

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
LTP yaml: /tmp/coding-agent-playground-m1-s23-pr63-placementretry2-preflight-sft-20260521T185930Z.yaml
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr63-placementretry2-preflight-sft-20260521T185930Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr63-placementretry2-preflight-sft-20260521T185930Z
initial no-active-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground -> No jobs found.
```

## LTP Submit and Placement Gate

```text
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr63-placementretry2-preflight-sft-20260521T185930Z.yaml
submit result: HTTP 202 accepted
frame: xu.yang~coding-agent-playground-m1-s23-pr63-placementretry2-preflight-sft-20260521T185930Z
submitted: 2026-05-21 19:02:36
started: 2026-05-21 19:02:42
endpoint: ssh -p 25986 root@10.100.22.31
assigned node: lg-cmc-b7r202-q04u06-h200-000725
forbidden nodes:
- lg-cmc-b7r202-k07u06-h200-000580
- lg-cmc-b7r202-q04u06-h200-000725
placement decision: FAIL_FORBIDDEN_NODE
```

Immediate hostname/GPU probe:

```text
command: ssh -p 25986 -o ConnectTimeout=5 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@10.100.22.31 'echo HOSTNAME=$(hostname); nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used --format=csv,noheader'
HOSTNAME=lg-cmc-b7r202-q04u06-h200-000725
0, NVIDIA H200, 0 %, 1 MiB
1, NVIDIA H200, 0 %, 1 MiB
2, NVIDIA H200, 0 %, 1 MiB
3, NVIDIA H200, 0 %, 1 MiB
4, NVIDIA H200, 0 %, 1 MiB
5, NVIDIA H200, 0 %, 1 MiB
6, NVIDIA H200, 0 %, 1 MiB
7, NVIDIA H200, 0 %, 1 MiB
```

Because LTP assigned forbidden node `lg-cmc-b7r202-q04u06-h200-000725`, I stopped/released the allocation before transfer, `/home/xu.yang` capacity probing, mcore import, structured preflight, SFT, or eval. This consumed the one authorized fresh placement-retry2 attempt.

## Skipped Gates Due Placement Blocker

```text
transfer/checksum verification on remote: not run; forbidden placement
remote source/dependency network: not used
/home/xu.yang capacity probe: not run; forbidden placement
mcore_adapter import for USE_MCA=1: not run; forbidden placement
structured preflight: not run; forbidden placement
SFT: not run; forbidden placement
eval: not run, not authorized
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
```

## Stop Proof

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr63-placementretry2-preflight-sft-20260521T185930Z
stop command result: HTTP 202 accepted, "Execute job ... successfully."
post-stop status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr63-placementretry2-preflight-sft-20260521T185930Z
final LTP state: STOPPED (Completed)
final LTP completed: 2026-05-21 19:03:32
final task idx state: STOPPED
endpoint proof: ssh -p 25986 root@10.100.22.31 hostname -> Connection refused
no-running-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground -> No jobs found.
artifact preservation: no runtime artifacts were generated on the forbidden node beyond the transient hostname/GPU probe; local/provided bundles remain preserved at the paths listed above
```

Final status: `BLOCKED_PLACEMENT_FORBIDDEN_NODE_STOPPED_NO_TRANSFER_NO_PREFLIGHT_NO_SFT`

Fresh PM authorization is required before any further LTP/GPU/preflight/SFT/eval work.
