# M1-S23-PR55-SFT-WRAPPER-FIX-DEV4

Owner: `intern_code_dev_4`

Date: `2026-05-21`

Scope: no-execution SFT launcher wrapper fix package after dev_2's PR55 runtime passed preflight, then the SFT launch exited before GPU training with `environment: DEP_TARGET: unbound variable`.

Runtime boundary: no LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run by dev_4 for this task.

## Inputs Reviewed

Dev_2 runtime evidence:

```text
evidence/dev_2_s23_pr55_preflight_sft_runtime.md
evidence/gpu_s23_pr55_preflight_sft_tracking.md
```

Key facts cited:

```text
source commit: PR #55 merge commit 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
endpoint: ssh -p 15535 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
forbidden-node gate: PASS, non-forbidden
output root: /home/xu.yang/coding_agent_playground/outputs
capacity: PASS_AND_CLEANED
transfer: local PR55 source bundle/data only, checksums verified
remote source/dependency network: no remote git clone/fetch/GitHub/source/dependency download
preflight: PASS
sft_allowed: true
SFT attempt: exactly one, started 2026-05-21T15:08:24Z
exit status: 1, ended 2026-05-21T15:08:25Z
blocker: environment: DEP_TARGET: unbound variable
checkpoint/model/trainer_state/all_results/eval: absent
stop proof: STOPPED (Completed), endpoint refused after stop, no running coding-agent-playground job
```

Preserved artifact paths from dev_2 evidence:

```text
source/data staging: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z/staging
preflight: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
SFT run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
capacity probe: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
```

## Diagnosis

The SFT wrapper reached `scripts/train_qwen3_8b_sft.sh`, wrote durable diagnostics, generated runtime config and run manifest, and then exited before GPU training. The observed blocker was:

```text
environment: DEP_TARGET: unbound variable
```

Dev_2 evidence notes that the GPU node used a local transferred dependency bundle and a LLamaFactory wrapper/exported environment path. The exported wrapper referenced `DEP_TARGET`, but `DEP_TARGET` was not exported into the environment seen by the wrapper under `set -u`, so the launch failed immediately.

This is distinct from previous blockers:

```text
preflight health parser: resolved; PR55 preflight PASS
dataset schema: not reached in this run
dataset multiprocessing: not reached in this run
NCCL/NVLink training failure: not reached in this run
ENOSPC checkpoint save: not reached in this run
```

## Patch

Files changed:

```text
scripts/train_qwen3_8b_sft.sh
tests/test_train_qwen3_8b_sft_static.py
```

Launcher changes:

```text
1. Add LLAMAFACTORY_CLI="${LLAMAFACTORY_CLI:-llamafactory-cli}" so runtime can point to a chmod-capable local wrapper path if needed.
2. Add DEP_TARGET="${DEP_TARGET:-${PYTHON_DEPS_DIR:-${RUN_DIR}/python_deps}}" so transferred dependency targets have a stable default under /home/xu.yang outputs.
3. Add LF="${LF:-${LLAMAFACTORY_DIR}}" for wrappers that expect the LLamaFactory root.
4. Export DEP_TARGET, LF, and LLAMAFACTORY_CLI before logging, manifest generation, and training launch.
5. Record DEP_TARGET/LF/LLAMAFACTORY_CLI in stdout/stderr logs.
6. Record the same explicit env contract in the run manifest launch command.
7. Invoke "${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}" instead of hard-coding llamafactory-cli.
```

The default `DEP_TARGET` remains under:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/python_deps
```

This preserves the `/home/xu.yang/coding_agent_playground/outputs` generated-artifact policy. If a future runtime uses a chmod-capable wrapper under `/root/workspace`, that path should be used only for executable source staging and must keep generated logs/checkpoints/run metadata/intermediates under `/home/xu.yang/coding_agent_playground/outputs`.

## No-Remote-Network Rule

The patch does not add any remote fetch, install, clone, or download. Future runtime should continue to use local bundle transfer and checksum verification for:

```text
source bundle
ShareGPT data
dependency wheels or extracted dependency tree
optional LLamaFactory CLI wrapper
```

No GPU node should run remote GitHub/source/dependency network commands as part of this fix.

## Static/Test Evidence

Commands run locally only:

```bash
bash -n scripts/train_qwen3_8b_sft.sh
python3 -m py_compile tests/test_train_qwen3_8b_sft_static.py
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Observed local result:

```text
bash -n scripts/train_qwen3_8b_sft.sh: pass
python3 -m py_compile tests/test_train_qwen3_8b_sft_static.py: pass
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 2 passed in 0.01s
```

## PR / Completion Status

```yaml
task_id: M1-S23-PR55-SFT-WRAPPER-FIX-DEV4
owner: intern_code_dev_4
result: READY_FOR_PR
evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr55_sft_wrapper_fix.md
patch_files:
  - scripts/train_qwen3_8b_sft.sh
  - tests/test_train_qwen3_8b_sft_static.py
runtime_authorized: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
completion_marker: ready-for-review; owner self-merge requires PM gate
```
