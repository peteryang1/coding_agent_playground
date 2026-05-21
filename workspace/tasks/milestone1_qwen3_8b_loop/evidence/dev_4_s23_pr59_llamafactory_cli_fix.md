# M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4

Task ID: `M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4`  
Owner: `intern_code_dev_4`  
Date: 2026-05-21

## Scope

No-execution launcher fix package for the PR59 runtime blocker where `LLAMAFACTORY_CLI` was set to a command string containing a space and `scripts/train_qwen3_8b_sft.sh` executed it as a single quoted path.

No LTP, GPU, preflight, SFT, eval, dry-run, or remote command was run by dev_4 for this task.

## Runtime Evidence Cited

Primary dev_2 evidence:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_pr59_preflight_sft_runtime.md
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_pr59_preflight_sft_tracking.md
```

Key facts from dev_2 evidence:

```text
task: M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2
source commit: PR #59 merge commit 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
frame: xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
endpoint: ssh -p 27043 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
transfer/import/preflight: passed
mcore_adapter import: OK for USE_MCA=1
sft exit status: 127
failure signature: scripts/train_qwen3_8b_sft.sh: line 244: python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py: No such file or directory
root cause: LLAMAFACTORY_CLI was set to `python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`, but the launcher executed `"${LLAMAFACTORY_CLI}" train ...` as one command path.
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run
resource: stopped, endpoint refused connection after stop
```

## Root Cause

The PR57/PR59 launcher contract allowed `LLAMAFACTORY_CLI` to be configurable, but the final invocation treated it as one executable path:

```bash
"${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"
```

That works for a real executable or wrapper path such as `llamafactory-cli`, but fails for a command-plus-args value such as:

```text
python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
```

When quoted as one shell word, Bash attempts to execute a file literally named `python3 /root/.../launcher.py`, causing exit `127`.

## Patch

Files changed:

```text
scripts/train_qwen3_8b_sft.sh
tests/test_train_qwen3_8b_sft_static.py
```

Launcher behavior:

```text
LLAMAFACTORY_CLI still defaults to `llamafactory-cli`.
DEP_TARGET, LF, LLAMAFACTORY_CLI, and MCORE_ADAPTER_DIR remain exported.
LLAMAFACTORY_CLI is parsed into LLAMAFACTORY_CMD with Bash `read -r -a`.
The final train invocation uses `"${LLAMAFACTORY_CMD[@]}" train "${RUNTIME_CONFIG}"`.
The manifest launch command and stdout log render the parsed command with `%q` so evidence remains shell-readable without treating the whole string as one path.
```

This supports both:

```bash
LLAMAFACTORY_CLI=llamafactory-cli
LLAMAFACTORY_CLI="python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py"
```

The patch intentionally does not change:

```text
DEP_TARGET default/export
LF default/export
MCORE_ADAPTER_DIR default/export
MCORE_ADAPTER_DIR/PYTHONPATH mcore import gate when USE_MCA=1
no remote source/dependency download rule
/home/xu.yang/coding_agent_playground/outputs output root default
```

## Future Runtime Rule

Future runtime should continue staging source, data, LLamaFactory, and `mcore_adapter` from local/provided bundles only. Remote GPU/LTP nodes must not run remote GitHub/source fetches or dependency downloads.

If the future run uses a command string, the intended environment is:

```bash
export LLAMAFACTORY_CLI="python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py"
export DEP_TARGET=/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/python_deps
export LF=/root/workspace/coding_agent_playground/code/LLamaFactory
export MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
export OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
```

The launcher should log a rendered command similar to:

```text
LLAMAFACTORY_CMD=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
```

and execute it as:

```text
python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py train <runtime_config>
```

## Static Evidence

Commands run locally only:

```bash
bash -n scripts/train_qwen3_8b_sft.sh
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Result:

```text
bash -n scripts/train_qwen3_8b_sft.sh: exit 0
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 4 passed in 0.01s
```

## Status

```yaml
task_id: M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4
owner: intern_code_dev_4
result: PATCH_READY_FOR_REVIEW
pr: https://github.com/peteryang1/coding_agent_playground/pull/61
pr_state: open_non_draft_mergeable_clean_waiting_for_pm_gate
runtime_authorized_for_dev4: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
recommended_next_gate: dev_1_review_and_test_1_gate_before_any_new_runtime
```
