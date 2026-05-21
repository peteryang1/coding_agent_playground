# dev_2 S23 PR55 Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T14:52:40Z

Scope: PM-authorized exactly one fresh LTP runtime using PR #55 merge commit `1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703`. Check hostname before transfer; stop/release before transfer/preflight/SFT/eval if forbidden node assigned. If non-forbidden, use `/home/xu.yang/coding_agent_playground/outputs`, transfer local bundle/data, run structured preflight, and run SFT only if preflight `PASS` and `sft_allowed=true`. Eval is not authorized.

## Authorization / Hard Gates

```text
authorization file: evidence/pm_s23_pr55_preflight_sft_authorization.md
authorization time: 2026-05-21T14:52:00Z
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
source commit: 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
forbidden nodes: lg-cmc-b7r202-q03u26-h200-000730, lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
remote network rule: no remote git clone/fetch/GitHub/source/dependency download
eval authorized: false
```

## Local Source/Data Preparation

PR #55 merge commit was available locally in `/work-agents/intern_code_dev_4/coding_agent_playground`; no network fetch was used. I created a detached local worktree and run-specific source bundle.

```text
source repository: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr55_20260521T145240Z_1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
commit: 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
worktree status: clean
file list: /tmp/cap_s23_pr55_20260521T145240Z_1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703_file_list.txt
file list count: 118
bundle: /tmp/cap_s23_pr55_20260521T145240Z_1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703.tar.gz
bundle sha256: db82b9162af2c37d670e568e16002cfc595e9090d578121545827622c3141df7
remote bundle sha file: /tmp/cap_s23_pr55_20260521T145240Z_1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703_remote_bundle.sha256
critical checksum file: /tmp/cap_s23_pr55_20260521T145240Z_1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703_remote_critical_files.sha256
```

Critical file checksums:

```text
scripts/parse_s22_preflight_health.py sha256: 75bb354295d9d497d74e3e1b5bff596b0f33fdb0ce0f2100adfee42631851aea
tests/test_parse_s22_preflight_health.py sha256: 979592c73453e6c46da7776c81afaa6fbc7f8147eb075de232c386bd324b64c4
scripts/train_qwen3_8b_sft.sh sha256: 9dd84e02bea54915a613159012b0981070ba03e5d3b9cbd8fcda1047957b3cc5
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml sha256: 6493c82d54025d9c7bf6f3afe6e37cb9ea4e5bfe850af9643411f6d6d2591614
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml sha256: b841ff72532eb30d9fd2cabfde4b5f119ddb2679694b3b231e8facf016f8b465
scripts/write_sft_run_manifest.py sha256: f0f80d88452c26dc46866316b2946f419c5eabd6ab2b41ab2d7c9a4b394f997f
```

Dataset:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_s23_pr55_20260521T145240Z/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

## LTP Submit Plan

```text
run id: milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
LTP yaml: /tmp/coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z.yaml
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
shape: single node, 8 x H200, h200agentic virtual cluster
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z.yaml
status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
```

Initial status: `LOCAL_PR55_BUNDLE_READY_PRE_SUBMIT`

## Final Runtime Result

Final status: `BLOCKED_PR55_SFT_WRAPPER_ENV_DEP_TARGET_UNBOUND_STOPPED_NO_CHECKPOINT`

### LTP Allocation / Node

```text
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
started: 2026-05-21 14:54:40
endpoint: ssh -p 15535 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
forbidden-node check: PASS, node is not in the forbidden list
```

### Storage / Capacity / Transfer

```text
bootstrap ready: 2026-05-21T14:56:13Z
/mnt/cephfs: fuse.ceph-fuse
output root: /home/xu.yang/coding_agent_playground/outputs on fuse.ceph-fuse
df sample: 18P size, 16P available, 10% used
capacity probe: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
capacity probe result: PASS_AND_CLEANED, wrote and removed 25769803776 bytes
remote repo: /root/workspace/coding_agent_playground
remote dataset: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
remote staging evidence root: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z/staging
```

Transfer used local/provided source and data only. No remote `git clone`, `git fetch`, GitHub source fetch, or remote dependency download was used on the GPU node. The PR55 source bundle and data checksums verified on the node:

```text
bundle sha256: db82b9162af2c37d670e568e16002cfc595e9090d578121545827622c3141df7
remote repo file count: 118
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
critical file checks: OK for parser, tests, train script, config templates, and manifest writer
```

### Structured Preflight

Preflight artifacts are preserved under:

```text
/home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
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
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=allowlisted preflight artifacts passed without actionable health signatures
```

### Offline Dependency Handling

The PR55 source package was staged exactly from local/provided workspace. The remote node lacked `peft`, `trl`, `fire`, `tyro`, `shtab`, `typeguard`, and `termcolor`; a local wheel bundle was prepared outside the GPU node and transferred to the node. The remote node installed/extracted from the transferred local files only, with `--no-index` attempted and then direct wheel extraction under this run's `/home/xu.yang` output tree. This preserves the no-remote-source/dependency-network rule for the GPU node.

```text
local dependency bundle directory: /tmp/cap_pr55_pydeps_20260521T1505
remote dependency bundle: /root/workspace/cap_pr55_pydeps_20260521T1505.tar.gz
staged dependency evidence: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z/staging/python_deps
runtime python deps: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/python_deps
verified imports: peft 0.18.0, trl 0.24.0, llamafactory 0.9.5.dev0
```

Dependency wheel checksums:

```text
fire-0.7.0-py3-none-any.whl sha256: 0b69b95b986d9c2db1fbd6446b5c5bca8cee2ab17b54f6c4ab17dbd391574e69
peft-0.18.0-py3-none-any.whl sha256: 624f69ca6393b765ccc6734adda7ca57d80b238f0900a42c357d8b67a03d62ff
shtab-1.7.2-py3-none-any.whl sha256: 858a5805f6c137bb0cda4f282d27d08fd44ca487ab4a6a36d2a400263cd0b5c1
termcolor-3.2.0-py3-none-any.whl sha256: a10343879eba4da819353c55cb8049b0933890c2ebf9ad5d3ecd2bb32ea96ea6
trl-0.24.0-py3-none-any.whl sha256: a9145b7d4a4a33778de117bda48530f0cf5b2ac25acc07db80ad04836f490dfc
typeguard-4.4.4-py3-none-any.whl sha256: b5f562281b6bfa1f5492470464730ef001646128b180769880468bd84b68b09e
tyro-0.8.14-py3-none-any.whl sha256: 1904bffb0e4d5e16c5eb50c518c89a368a44d56405f79b316c58e1206c102e87
```

### SFT Attempt

Exactly one conditional SFT launch was attempted after structured preflight `PASS` and `sft_allowed=true`. Eval was not run.

```text
SFT start: 2026-05-21T15:08:24Z
run id: milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
tmp dir: /home/xu.yang/coding_agent_playground/outputs/tmp/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
dataset source: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
config template: /root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/config/qwen3_8b_sft.yaml
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/run_manifest.json
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/logs/train_stdout_stderr.log
xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/logs/train_xtrace.log
diagnostics: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/early_exit_diagnostics.txt
exit status file: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/exit_status.txt
final summary: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/final_artifact_summary.txt
```

Runtime env/command evidence:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
DRY_RUN=0
NCCL_DEBUG=INFO
NCCL_DEBUG_SUBSYS=INIT,GRAPH,COLL
NCCL_ASYNC_ERROR_HANDLING=1
TORCH_NCCL_ASYNC_ERROR_HANDLING=1
CUDA_DEVICE_MAX_CONNECTIONS=1
launch command recorded by manifest: cd /root/workspace/coding_agent_playground/code/LLamaFactory && export PYTHONPATH="/root/workspace/coding_agent_playground/code/LLamaFactory/src:${PYTHONPATH:-}" && llamafactory-cli train /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/config/qwen3_8b_sft.yaml
```

The attempt failed before GPU training due a launch-wrapper environment bug:

```text
exit_status.txt:
EXIT_STATUS=1
END_UTC=2026-05-21T15:08:25Z

train_stdout_stderr.log blocker line:
environment: DEP_TARGET: unbound variable
```

Because this was the one authorized SFT attempt, I did not rerun after identifying the wrapper-variable fix. No checkpoint/model was produced:

```text
checkpoint files: none
trainer_state.json: absent
all_results.json: absent
post-failure GPU sample: all 8 H200 at 0% util and 1 MiB memory
post-failure process scan: no torchrun/python3 -m llamafactory/llamafactory-cli/train_qwen3_8b_sft process
eval: not authorized and not run
```

Next fix for any future PM-authorized runtime: avoid an exported bash function that references non-exported local variables. Use an executable wrapper in a chmod-capable local path with explicit environment values, or export `DEP_TARGET`/`LF` before invoking `scripts/train_qwen3_8b_sft.sh`. Because CephFS rejected `chmod` on `/home/xu.yang/.../bin/llamafactory-cli`, a wrapper on `/root/workspace` or direct script patching may be needed, with justification recorded if outside `/home/xu.yang`.

### Stop Proof

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
stop sent UTC: 2026-05-21T15:09:12Z
post-stop status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
final LTP state: STOPPED (Completed)
completed: 2026-05-21 15:09:43
exit code shown by LTP after stop: -210 Failed
endpoint proof: ssh -p 15535 root@10.100.22.28 returned "Connection refused" at 2026-05-21T15:10:02Z
no-running-job proof command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
no-running-job proof output: No jobs found.
artifact preservation: outputs/logs/preflight/run metadata/checkpoint directory evidence preserved under /home/xu.yang/coding_agent_playground/outputs
```
