# Task Knowledge - M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4

1. PR61 runtime generated config contained `model_name_or_path`, `dataset: coding_agent_m1_sft_10_sharegpt`, `/home/xu.yang/coding_agent_playground/outputs` output paths, `preprocessing_num_workers: null`, and `max_steps: 2`.
2. The failing runtime command used `LLAMAFACTORY_CLI="python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py"`.
3. In the inspected LLamaFactory source bundle, `cli.py` calls `launcher.launch()`, but `launcher.py` executed directly as `__main__` calls `run_exp()` immediately.
4. LLamaFactory `read_args()` loads a YAML file only when the first parser argument ends in `.yaml` or `.yml`.
5. Direct `launcher.py train config.yaml` makes `train` the first parser argument, so `config.yaml` is not loaded and `model_name_or_path` remains unset.
6. The minimal launcher-side fix is to preserve the parsed command array but normalize direct `llamafactory/launcher.py` commands to `python3 -m llamafactory.cli`, then append `train <runtime_config>`.
7. Future runtime remains separately PM-gated; this task did not run LTP/GPU/preflight/SFT/eval/dry-run/remote commands.
