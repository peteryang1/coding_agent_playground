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
