# dev_2 S23 PR57 Preflight + Conditional SFT Runtime

Task ID: `M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T15:52:00Z

Scope: PM-authorized exactly one fresh owner-executed LTP/GPU runtime using `origin/main` commit `b4ac31ef1e3772953108348bf099818326ed65cc` after PR #57 and PR #58 merged. Remote GPU/LTP node is treated as no-external-network for project code/dependency staging: no remote `git clone`, `git fetch`, GitHub/source fetch, or project/dependency download on the remote node. Eval is not authorized.

## Authorization

```text
authorization evidence: evidence/pm_s23_pr57_preflight_sft_authorization.md
authorized owner: intern_code_dev_2
authorized allocation count: exactly one fresh runtime
authorized commit: b4ac31ef1e3772953108348bf099818326ed65cc
PR #57 merge commit: c450429c2e3369adc723d132396399cd17dba684
PR #58 merge commit: b4ac31ef1e3772953108348bf099818326ed65cc
output root: /home/xu.yang/coding_agent_playground/outputs
SFT condition: run exactly one SFT only if structured preflight reports PREFLIGHT_RESULT=PASS and SFT_ALLOWED=true
eval: not authorized
```

## Local Source/Data Preparation

Prepared locally from the provided dev_4 workspace; no PM shared dirty worktree was modified for source packaging.

```text
source repository: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc
commit: b4ac31ef1e3772953108348bf099818326ed65cc
worktree status: clean
file list: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_file_list.txt
file list count: 122
bundle: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc.tar.gz
bundle sha256: 1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa
critical checksum file: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_remote_critical_files.sha256
```

Critical file checksums:

```text
scripts/parse_s22_preflight_health.py sha256: 75bb354295d9d497d74e3e1b5bff596b0f33fdb0ce0f2100adfee42631851aea
tests/test_parse_s22_preflight_health.py sha256: 979592c73453e6c46da7776c81afaa6fbc7f8147eb075de232c386bd324b64c4
tests/test_train_qwen3_8b_sft_static.py sha256: f2cddbe28ce242cb31451fd6bb201371c5046be7f560c3198320a7044fb2068e
scripts/train_qwen3_8b_sft.sh sha256: cc1f53db797bc0c263e77ba3d197195089ede163812422ebf2744575407f47bc
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml sha256: 6493c82d54025d9c7bf6f3afe6e37cb9ea4e5bfe850af9643411f6d6d2591614
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml sha256: b841ff72532eb30d9fd2cabfde4b5f119ddb2679694b3b231e8facf016f8b465
scripts/write_sft_run_manifest.py sha256: f0f80d88452c26dc46866316b2946f419c5eabd6ab2b41ab2d7c9a4b394f997f
```

Dataset:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_s23_pr57_20260521T155200Z/train.jsonl
dataset source: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

## LTP Submit Plan

```text
run id: milestone1_qwen3_8b_s23_pr57_preflight_sft_20260521T155200Z
LTP yaml: /tmp/coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z.yaml
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
shape: single node, 8 x H200, h200agentic virtual cluster
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z.yaml
status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
```

Initial status: `LOCAL_PR57_BUNDLE_READY_PRE_SUBMIT`

## Final Runtime Result

Final status: `BLOCKED_PR57_RUNTIME_MISSING_MCORE_ADAPTER_STOPPED_NO_CHECKPOINT`

The one authorized LTP allocation, structured preflight, and conditional SFT attempt are complete. Structured preflight passed and allowed SFT. The single authorized SFT attempt then failed before training/checkpoint creation because LLamaFactory/MCA import required `mcore_adapter` while `USE_MCA=1`.

## LTP Allocation

```text
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z.yaml
frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
submitted: 2026-05-21 15:55:39
started: 2026-05-21 15:55:45
endpoint: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
shape: single node, 8 x NVIDIA H200
initial gpu sample: all 8 GPUs 0% util, 1 MiB used
```

## Storage and Capacity Proof

```text
/mnt/cephfs mount: fuse.ceph-fuse
/home/xu.yang: /mnt/cephfs/home/xu.yang
output root: /home/xu.yang/coding_agent_playground/outputs
df output root: 18P size, 1.8P used, 16P available, 10% used
capacity probe path: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr57_preflight_sft_20260521T155200Z/capacity_probe_status.txt
capacity probe start: 2026-05-21T15:57:37Z
capacity probe end: 2026-05-21T15:57:57Z
expected bytes: 25769803776
actual bytes: 25769803776
status: PASS_AND_CLEANED
```

## Transfer and Verification

Remote GPU node was treated as no-external-network for project code/dependency staging. I did not run remote `git clone`, `git fetch`, GitHub/source fetch, or project/dependency download. Source/config/scripts/data were prepared locally or from provided local workspaces and transferred to the node.

Transfer command:

```bash
scp -P 22662 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc.tar.gz \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_remote_bundle.sha256 \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_remote_critical_files.sha256 \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_file_list.txt \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_transfer_manifest.sha256 \
  /tmp/cleaned_m1_sft_10_sharegpt_s23_pr57_20260521T155200Z/train.jsonl \
  root@10.100.22.31:/root/workspace/
```

Post-transfer verification:

```text
remote repo path: /root/workspace/coding_agent_playground
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
remote staging root: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr57_preflight_sft_20260521T155200Z/staging
bundle sha256: OK
critical file checksums: OK
remote file count: 122
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Additional local dependency bundles transferred for the SFT launch:

```text
/tmp/cap_pr55_pydeps_20260521T1505.tar.gz sha256: e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
/mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
remote verification: both OK
```

## Structured Preflight

Preflight artifacts:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr57_preflight_sft_20260521T155200Z
remote script: /root/workspace/run_pr57_preflight.sh
```

Structured result:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
SFT_ALLOWED_IF_PM_AUTHORIZED=true
SFT_SKIP_REASON=
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=allowlisted preflight artifacts passed without actionable health signatures
torch all-reduce: ALLREDUCE_OK
```

Because preflight passed and `SFT_ALLOWED=true`, I ran exactly one SFT attempt as authorized. Eval was not run.

## SFT Attempt

SFT launch:

```text
remote launch script: /root/workspace/launch_pr57_sft.sh
tmux session: pr57_sft_FIXED_SETUP
start: 2026-05-21T16:03:06Z
run id: milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
checkpoint/output dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_stdout_stderr.log
xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_xtrace.log
exit status: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/exit_status.txt
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/run_manifest.json
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/config/qwen3_8b_sft.yaml
final artifact summary: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/final_artifact_summary.txt
```

Config proof:

```text
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
dataset source sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
preprocessing_num_workers: null
dataloader_num_workers: 0
max_steps: 2
save_steps: 2
save_total_limit: 1
tensor_model_parallel_size: 8
```

Exit status:

```text
EXIT_STATUS=1
END_UTC=2026-05-21T16:03:28Z
```

Failure signature from `train_stdout_stderr.log`:

```text
ImportError: mcore_adapter is required when USE_MCA=1. Please install `mcore_adapter` and its dependencies.
torch.distributed.elastic.multiprocessing.errors.ChildFailedError
/root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py FAILED
local_rank: 7 exitcode 1
```

The launcher initialized 8 distributed tasks before the import failure:

```text
[INFO|2026-05-22 00:03:18] llamafactory.launcher:144 >> Initializing 8 distributed tasks at: 127.0.0.1:47509
```

Artifact status at `2026-05-21T16:05:21Z`:

```text
process scan: no torchrun, llamafactory, launcher.py, train_qwen3_8b, or python training process
gpu sample: all 8 NVIDIA H200 GPUs 0% util, 1 MiB used
checkpoint files: none
trainer_state.json: absent
all_results.json: absent
checkpoint/model: absent
eval: not run
```

## Stop Proof

Stop command:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
```

Stop response:

```text
STOP signal sent to xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
status: 202
message: Execute job xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z successfully.
```

Post-stop LTP status:

```text
checked: 2026-05-21T16:06:06Z
State: STOPPED (Completed)
ExecType: STOP
Completed: 2026-05-21 16:06:06
ExitCode: -210 Failed
task idx 0 state: STOPPED
endpoint: ssh -p 22662 root@10.100.22.31
endpoint proof: ssh returned "connect to host 10.100.22.31 port 22662: Connection refused"
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

Artifact preservation note: generated preflight, run metadata, logs, config, dependency bundles staged in the run dir, final artifact summary, and failed-run outputs are preserved under `/home/xu.yang/coding_agent_playground/outputs`. No checkpoint/model was produced.

Next fix recommendation: treat this as a runtime dependency/environment blocker for MCA path. Before any further runtime authorization, the launch package or base image must provide `mcore_adapter` and dependencies when `USE_MCA=1`, or the runtime/config must explicitly select a supported non-MCA path if PM/dev_4/dev_1/test_1 approve that change. Fresh PM authorization is required for any new LTP/GPU/preflight/SFT/eval work.
