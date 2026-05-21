# M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4 - MCA Model Path Fix

## Task

- Task id: `M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4`
- Owner: `intern_code_dev_4`
- Scope: no-execution launcher fix package for PR61 runtime blocker `BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE`.
- Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr61_mca_model_path_fix.md`
- Runtime boundary: no LTP/GPU/preflight/SFT/eval/dry-run/remote command was run by dev_4 for this task.

## Inputs Reviewed

- PM/dev_2 runtime evidence:
  - `evidence/dev_2_s23_pr61_preflight_sft_runtime.md`
  - `evidence/gpu_s23_pr61_preflight_sft_tracking.md`
- Runtime frame: `xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z`
- Runtime endpoint/node: `ssh -p 33089 root@10.100.22.31`, node `lg-cmc-b7r202-q04u06-h200-000725`
- Runtime source commit: `713862da983f73b165af1cfe27935ccef616a049`
- Runtime bundle sha256: source `a8aeb73d6f3c69775997b7c4b6cf49344a0e8691a44811b68d5678caaacb83c4`; mcore `4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb`
- Dataset: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, dataset name `coding_agent_m1_sft_10_sharegpt`, sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`

## Runtime Facts

- Transfer/import/preflight passed.
- `/home/xu.yang/coding_agent_playground/outputs` path policy was preserved by the runtime.
- `mcore_adapter import OK for USE_MCA=1`.
- PR61 command parsing fix was effective enough to reach `llamafactory/launcher.py`.
- Runtime generated config contained:

```yaml
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
preprocessing_num_workers: null
dataloader_num_workers: 0
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
save_steps: 2
save_total_limit: 1
max_steps: 2
```

- Runtime launcher env included:

```bash
LLAMAFACTORY_CLI="python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py"
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
```

- Final failure:

```text
EXIT_STATUS=1
ValueError: Please provide `model_name_or_path`.
trace: llamafactory/launcher.py -> train/tuner.py -> hparams/parser.py -> model_args.py
```

- No checkpoint/model, `trainer_state.json`, `all_results.json`, served endpoint, or eval artifact was produced.
- dev_2 stopped the frame; endpoint refused connection after stop.

## Root Cause

The generated runtime YAML did contain `model_name_or_path`, but the command shape prevented LLamaFactory from loading that YAML.

PR61 correctly parsed the space-containing `LLAMAFACTORY_CLI` into an executable/args array and launched:

```bash
python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py train /home/xu.yang/.../qwen3_8b_sft.yaml
```

Local inspection of the LLamaFactory source bundle shows:

- `src/llamafactory/cli.py` calls `launcher.launch()`.
- `launcher.launch()` consumes the `train` subcommand, sets MCA/torchrun behavior, then launches `launcher.py` under torchrun with the remaining args.
- `launcher.py` when executed directly as `__main__` does **not** call `launch()`; it calls `run_exp()` directly.
- `hparams/parser.py::read_args()` only loads YAML when `sys.argv[1]` ends with `.yaml` or `.yml`.

Therefore, direct execution of `launcher.py train config.yaml` leaves `sys.argv[1] == "train"` at the parser boundary. The YAML becomes `sys.argv[2]`, is not loaded by `read_args()`, and `ModelArguments.__post_init__()` raises `ValueError: Please provide model_name_or_path`.

## Patch

Patched `scripts/train_qwen3_8b_sft.sh` to preserve PR61 command-array parsing while normalizing direct `llamafactory/launcher.py` commands to the module CLI entrypoint:

```bash
LLAMAFACTORY_CLI="python3 /path/to/LLamaFactory/src/llamafactory/launcher.py"
```

is normalized before launch to:

```bash
python3 -m llamafactory.cli train "${RUNTIME_CONFIG}"
```

This sends the `train` subcommand through `launcher.launch()`, preserving MCA/torchrun setup. The torchrun child then executes `launcher.py "${RUNTIME_CONFIG}"`, so the YAML is `sys.argv[1]` and `read_args()` loads `model_name_or_path` from the generated config.

The patch also logs:

- `LLAMAFACTORY_CMD_ORIGINAL`
- `LLAMAFACTORY_CMD_NORMALIZATION`
- normalized `LLAMAFACTORY_CMD`

## Files Changed

- `scripts/train_qwen3_8b_sft.sh`
- `tests/test_train_qwen3_8b_sft_static.py`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr61_mca_model_path_fix.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4/README.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4/history_log.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4/task_knowledge.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`
- `workspace/interns/intern_code_dev_4/status.md`

## Static Checks

```text
bash -n scripts/train_qwen3_8b_sft.sh
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Result:

```text
5 passed in 0.01s
```

## Preserved Constraints

- Preserves PR61 `LLAMAFACTORY_CLI` command-array parsing.
- Preserves `DEP_TARGET`, `LF`, `MCORE_ADAPTER_DIR`, and `mcore_adapter` path handling.
- Preserves no remote source/dependency downloads; future runtime must use local/provided bundles and transfer checksums.
- Preserves `/home/xu.yang/coding_agent_playground/outputs` for generated outputs, logs, checkpoints, run metadata, temporary converted datasets, and intermediates.
- Does not authorize or perform LTP/GPU/preflight/SFT/eval/dry-run/runtime execution.

## Acceptance Criteria

- The wrapper keeps handling a space-containing `LLAMAFACTORY_CLI` as command-plus-args.
- A direct `python3 .../llamafactory/launcher.py` command is normalized to the supported CLI module path before `train <runtime_config>` is appended.
- The future runtime command path lets `read_args()` see the generated YAML as the first parser argument in the torchrun child.
- Static tests cover the normalization behavior.
- Durable evidence cites PM/dev_2 PR61 blocker facts and records the no-runtime boundary.

## Completion Marker

- Complete/ready-for-runtime-gate: PM gate passed for PR #63 and dev_4 self-merged it at `2026-05-21T18:08:48Z`.
- Merge commit: `2f89e9234bb5f9dfdcc433a30bc0f6dcfd9a8689`.
- Completion record branch: `intern_code_dev_4/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4-completion`.
- Runtime boundary remains: this merge and completion record do not authorize LTP/GPU/transfer/preflight/SFT/eval/runtime.
