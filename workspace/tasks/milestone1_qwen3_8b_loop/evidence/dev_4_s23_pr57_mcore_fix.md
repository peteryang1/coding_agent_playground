# M1-S23-PR57-MCORE-FIX-DEV4

Task ID: `M1-S23-PR57-MCORE-FIX-DEV4`  
Owner: `intern_code_dev_4`  
Date: 2026-05-21

## Scope

No-execution fix package for the PR57 runtime blocker:

```text
ImportError: mcore_adapter is required when USE_MCA=1. Please install `mcore_adapter` and its dependencies.
```

No LTP, GPU, preflight, SFT, eval, dry-run, or remote command was run by dev_4 for this task.

## Runtime Evidence Cited

Primary dev_2 evidence:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_pr57_preflight_sft_runtime.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_pr57_preflight_sft_tracking.md
```

Key facts from dev_2 evidence:

```text
runtime task: M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2
source commit: b4ac31ef1e3772953108348bf099818326ed65cc
frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
endpoint: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
preflight result: PASS
sft_allowed: true
sft exit status: 1
failure: ImportError: mcore_adapter is required when USE_MCA=1
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run
resource: stopped, endpoint refused connection after stop
```

The same evidence records that remote GPU/LTP nodes were treated as no-external-network targets and that generated artifacts were under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

## Dependency Path Diagnosis

The SFT launcher defaults to the MCA path:

```text
USE_MCA=1
FORCE_TORCHRUN=1
LLamaFactory train config uses Megatron/MCA parallelism fields
```

When `USE_MCA=1`, LLamaFactory's MCA integration imports `mcore_adapter` during distributed launch. If `mcore_adapter` is absent from the Python environment or not reachable through `PYTHONPATH`, torchrun starts ranks and then fails before training/checkpoint creation.

This is a dependency staging and launch-environment blocker, not a data blocker and not a checkpoint quality failure:

```text
ShareGPT dataset checksum accepted: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
structured preflight passed
all-reduce passed
no checkpoint/model was produced
```

Prior successful dependency guidance in milestone evidence used a local/provided `mcore_adapter` source tree or wheel, for example:

```text
code/mcore_adapter/
pip install --break-system-packages -e code/mcore_adapter/ --no-deps
python3 -c "import flash_attn, mcore_adapter; print('gpu deps ok')"
```

Under the Session 23 supervisor rule, remote nodes must not fetch this dependency from GitHub or external package indexes. The dependency must be prepared from a local/provided workspace or local artifact, checksummed, transferred, and verified.

## Patch

Files changed:

```text
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
tests/test_train_qwen3_8b_sft_static.py
```

Launcher change:

```text
MCORE_ADAPTER_DIR defaults to ${REPO_ROOT}/code/mcore_adapter.
If code/mcore_adapter exists, it is prepended to PYTHONPATH together with LLamaFactory src.
The manifest launch command exports MCORE_ADAPTER_DIR and the resolved PYTHONPATH prefix.
Before invoking LLamaFactory train, USE_MCA=1 performs a Python import gate for mcore_adapter.
If the import fails, the launcher exits early with an explicit no-remote-network dependency-bundle instruction instead of reaching torchrun rank failure.
```

Manifest change:

```text
run_manifest.json records MCORE_ADAPTER_DIR and PYTHONPATH_PREFIX in environment/preflight fields.
```

Static test change:

```text
tests/test_train_qwen3_8b_sft_static.py verifies MCORE_ADAPTER_DIR default/export, USE_MCA=1 import gate, no-remote-network error text, and PYTHONPATH inclusion for local code/mcore_adapter.
```

## Future Runtime Bundle Requirement

The next PM-authorized runtime should stage `mcore_adapter` as a local/provided dependency bundle before transfer. Example command template:

```bash
tar -C /work-agents/<owner_or_provided_workspace>/coding_agent_playground/code \
  -czf /tmp/mcore_adapter_<RUN_ID>.tar.gz mcore_adapter
sha256sum /tmp/mcore_adapter_<RUN_ID>.tar.gz > /tmp/mcore_adapter_<RUN_ID>.tar.gz.sha256
scp -P <PORT> \
  /tmp/mcore_adapter_<RUN_ID>.tar.gz \
  /tmp/mcore_adapter_<RUN_ID>.tar.gz.sha256 \
  root@<HOST>:/root/workspace/
ssh -p <PORT> root@<HOST> \
  'cd /root/workspace && sha256sum -c mcore_adapter_<RUN_ID>.tar.gz.sha256 && mkdir -p coding_agent_playground/code && tar -C coding_agent_playground/code -xzf mcore_adapter_<RUN_ID>.tar.gz && test -d coding_agent_playground/code/mcore_adapter'
```

The SFT launch should then use:

```bash
export MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
export OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
export USE_MCA=1
```

Post-transfer evidence must record:

```text
source commit or local/provided dependency source provenance
file list
bundle sha256
transfer command
destination
remote sha256 verification
MCORE_ADAPTER_DIR
python import check result
```

## Non-MCA Fallback

Non-MCA is not selected by this patch.

Reason:

```text
The current Qwen3-8B smoke package is the MCA/Megatron path with tensor_model_parallel_size=8 and USE_MCA=1.
Changing to USE_MCA=0 would change the training backend and parallelism assumptions, and should require explicit PM/dev_1/test_1 approval as a separate fallback path.
```

Supported fallback only if PM explicitly gates it:

```text
USE_MCA=0
non-MCA LLamaFactory config without Megatron tensor parallel fields
separate memory/resource review for Qwen3-8B on one H200 node
```

## Static Evidence

Commands run locally only:

```bash
bash -n scripts/train_qwen3_8b_sft.sh
python3 -m py_compile scripts/write_sft_run_manifest.py
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Result:

```text
bash -n scripts/train_qwen3_8b_sft.sh: exit 0
python3 -m py_compile scripts/write_sft_run_manifest.py: exit 0
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 3 passed in 0.01s
```

## Status

```yaml
task_id: M1-S23-PR57-MCORE-FIX-DEV4
owner: intern_code_dev_4
result: COMPLETE
pr: https://github.com/peteryang1/coding_agent_playground/pull/59
pr_state: merged
merged_at: 2026-05-21T16:34:13Z
merge_commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
pm_gate_head: b0b54279bcf87add7e617b0c08686c40fac41b48
functional_patch_commit: 92e437cf690b68121b9ad9d2f76b18a60a10a2d6
runtime_authorized_for_dev4: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
recommended_next_gate: dev_1_review_and_test_1_gate_before_any_new_runtime
```
