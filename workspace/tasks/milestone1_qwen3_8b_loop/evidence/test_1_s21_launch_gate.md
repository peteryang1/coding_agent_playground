# Test 1 Session 21 SFT Launch Gate

Date: 2026-05-21

Task ID: `M1-S21-LAUNCH-GATE-TEST1`

Owner: `intern_code_test_1`

Scope: replacement Session 21 no-execution launch gate for the ShareGPT-fixed Qwen3-8B SFT smoke. This gate defines the required preflight checks and post-run evidence before PM can treat a runtime attempt as valid.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s21_launch_gate.md`

## Current Result

Result: **PASS_FOR_PM_AUTHORIZATION / POST-RUN PENDING**

No SFT, GPU, or eval command was run by test_1.

The ShareGPT data artifact itself has already passed test_1 no-execution compatibility in `evidence/test_1_sft_dataformat_gate.md`.

During this gate update, `evidence/dev_3_s21_datasetinfo_package.md` and `evidence/dev_2_s21_sft_runtime.md` appeared in the PM worktree. The dev_3 dataset_info package passes this gate. A later dev_2 refresh corrected the earlier launch-wiring mismatch.

Current preflight decision for PM authorization:

```text
PASS_FOR_PM_AUTHORIZATION
```

Reason: dataset_info mapping, artifact checksum/count, base model, config sanity, and intended dev_2 command/config wiring now match the accepted ShareGPT-fixed path. This is not a post-run PASS; no SFT/GPU/eval has run, no endpoint exists yet, and post-run artifacts remain pending.

Mini-swe status: **BLOCKED** until a later SFT run produces an accepted checkpoint/model or served endpoint and test_1/test_2 gates pass.

## Sources Reviewed

- `task_registry.md`
- `assignments.md`
- `blockers.md`
- `history_log.md`
- `task_knowledge.md`
- `evidence/dev_3_sft_dataformat_artifact.md`
- `evidence/test_1_sft_dataformat_gate.md`
- `evidence/dev_4_sft_config_fix_plan.md`
- `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`
- `evidence/dev_3_s21_datasetinfo_package.md`
- `evidence/dev_2_s21_sft_runtime.md`
- `evidence/dev_1_s21_launch_review.md`

## Required Dataset Artifact

Accepted ShareGPT-fixed artifact:

```text
path=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256=26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
schema=coding_agent_playground_sft_v1_sharegpt_messages
row_count=10
unique_example_ids=10
unique_trajectory_ids=10
role_values={"human": 10, "gpt": 10}
message_key_sets=[["from", "value"]]
```

Artifact evidence source: `evidence/dev_3_sft_dataformat_artifact.md`.

Preflight PASS requires runtime evidence to re-state this exact path, checksum, count, schema, and source artifact provenance. Any alternate data path or checksum is a preflight FAIL unless PM creates a new task and evidence package for that artifact.

## Required Dataset_Info Mapping

Dataset_info package supplied by `M1-S21-DATASETINFO-PACKAGE-DEV3`: **PASS**

Accepted entry:

```text
dataset_name=coding_agent_m1_sft_10_sharegpt
file_name=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
formatting=sharegpt
conversation_column=messages
role_tag=from
content_tag=value
user_tag=human
assistant_tag=gpt
system_tag=system if present
tool/observation tag=tool if present or explicitly unsupported for this 10-row smoke
```

Acceptable JSON shape depends on the local LLamaFactory version, but it must unambiguously tell the loader to read `messages[*].from` and `messages[*].value`. The runtime config must use the same `dataset_name`.

Preflight PASS requires all of:

- `dataset_info.json` path is recorded.
- The file location is the one the launch process will actually read.
- The dataset entry points to `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- The conversation column is `messages`, or an alternate column is explicitly mapped and the artifact supports it.
- The role/content tags are `from` and `value`.
- The runtime config's `dataset:` value matches the dataset_info entry name.

Current dataset_info validation:

```text
dataset_info_package: PASS
entry_name: coding_agent_m1_sft_10_sharegpt
artifact_path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
artifact_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row_count: 10
columns.messages: messages
tags.role_tag: from
tags.content_tag: value
tags.user_tag: human
tags.assistant_tag: gpt
avoid_keyerror_from: yes
```

Preflight FAIL/BLOCKER if any of:

- `dev_3_s21_datasetinfo_package.md` is absent.
- `dataset_info.json` is absent or not copied into the LLamaFactory checkout used by the runtime.
- The entry still references the old OpenAI-style `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- The entry expects `role`/`content`, `conversations`, or another column without matching the chosen artifact.
- The runtime config uses `milestone1_coding_agent_sft` while the dataset_info package names a different entry, or vice versa.

## Required Base Model

Accepted base model:

```text
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

Preflight PASS requires runtime/package evidence to confirm:

- `config.json` exists.
- tokenizer files exist.
- `model.safetensors.index.json` and safetensor shards exist.
- The config is Qwen3 and compatible with `Qwen3ForCausalLM`.
- This path is used as `BASE_MODEL` / `model_name_or_path` in the generated runtime config.

Preflight FAIL if:

- the broken alias `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is used without repair;
- a warm-start/historical checkpoint is used while evidence claims clean base;
- base path is omitted from the command or generated config.

## Required Config Sanity

Required config template:

```text
/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
```

Required safety properties from current evidence:

```yaml
stage: sft
do_train: true
finetuning_type: full
dataset_dir: data/sft
template: qwen3
per_device_train_batch_size: 1
gradient_accumulation_steps: 1
max_steps: 2
warmup_steps: 0
save_steps: 1
logging_steps: 1
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
context_parallel_size: 1
sequence_parallel: false
save_only_model: true
save_hf_model: true
```

Preflight PASS requires the generated runtime config to preserve:

- expected data parallel size `1` on one 8-GPU node;
- `warmup_steps=0` and `max_steps=2`;
- `save_steps=1` and durable output path under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`;
- dataset name matching the accepted dataset_info entry;
- `model_name_or_path` rewritten to the accepted base model path.

Preflight FAIL if:

- runtime config reverts to DP=8 over the 10-example dataset;
- `max_steps=1` or warmup/decay relation can reproduce the scheduler assertion;
- output path is local scratch only;
- generated config points at the old OpenAI-style artifact without matching registration.

## Required Command Package

Expected command shape for a later PM-authorized runtime:

```bash
cd /root/workspace/coding_agent_playground
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_s21_sharegpt_tp8_maxsteps2_<UTC> \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

If the runtime wrapper supports `DATASET_NAME`, it must be:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
```

If the wrapper does not support `DATASET_NAME`, the generated runtime config must be patched before launch so:

```yaml
dataset: coding_agent_m1_sft_10_sharegpt
```

Preflight PASS requires the owner runtime/package evidence to include:

- exact command;
- exact endpoint/node or current `nodes.json`;
- `DRY_RUN=0`;
- unique run ID;
- dataset artifact path and checksum;
- dataset_info path and entry name;
- config template and generated runtime config path;
- base model path;
- output root;
- stop/cleanup conditions.

Preflight FAIL/BLOCKER if:

- command package is absent;
- `DATASET_JSONL` points to `/root/workspace/cleaned_m1_sft_10/train.jsonl`;
- `DRY_RUN` is missing or not `0` for the eventual runtime;
- no current GPU endpoint/resource proof exists at execution time;
- PM authorization is not recorded before runtime.

Current command/package validation:

```text
command_package_status: PASS_FOR_PM_AUTHORIZATION
reason: dev_2 runtime evidence now uses DATASET_NAME=coding_agent_m1_sft_10_sharegpt and requires generated config dataset: coding_agent_m1_sft_10_sharegpt.
remaining_post_auth_requirements: PM authorization, fresh LTP frame/node/endpoint/nodes.json, generated config proof from the staged node, runtime logs, manifest, checkpoint/model/trainer_state/all_results, and stop proof.
```

## Required Log Signatures

The later runtime logs must **not** contain:

```text
KeyError: 'from'
Cannot open data/sft/dataset_info.json
ValueError: Cannot open data/sft/dataset_info.json
ZeroDivisionError: division by zero
steps_in_epoch
optimizer_param_scheduler.py
assert self.lr_warmup_steps < self.lr_decay_steps
```

Data-format PASS requires evidence that runtime progressed beyond LLamaFactory dataset conversion without `KeyError: 'from'`.

If the run fails for another reason, post-run evidence must capture the first failing exception and whether the failure happened:

- before dataset load,
- during dataset conversion,
- during distributed/Megatron initialization,
- during training steps,
- during checkpoint save,
- during cleanup.

## Required Post-Run Artifacts

Post-run evidence from `M1-S21-RUNTIME-DEV2` must record:

- PM authorization reference;
- LTP job/frame id;
- node id and endpoint;
- start and end timestamps;
- exact command and environment;
- dataset_info path and content/entry used;
- dataset artifact path, sha256, row count;
- base model path;
- generated runtime config path;
- run manifest path;
- stdout/stderr log path;
- exit status;
- output root;
- checkpoint/model directory or explicit absence;
- `trainer_state.json` path or explicit absence;
- `all_results.json` path or explicit absence;
- GPU/resource cleanup and stop proof;
- preserved `/mnt/3fs` output paths.

Expected output path pattern:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/run_manifest.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/trainer_state.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/all_results.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<RUN_ID>/checkpoint-*
```

## PASS Criteria

Preflight PASS requires:

- `dev_3_s21_datasetinfo_package.md` exists and matches this gate.
- Launch package/runtime command exists and uses the accepted ShareGPT artifact.
- Artifact checksum/count/schema are restated exactly.
- Base model is the accepted clean Qwen3-8B path.
- Config preserves TP=8/DP=1 tiny-data-safe settings.
- PM authorization and current GPU resource proof are recorded before runtime.

Post-run PASS requires:

- runtime evidence includes all required files/paths above;
- exit status is `0`, or if nonzero, the blocker is a new exact runtime blocker after data-format and prior tiny-data failures are avoided;
- logs do not contain `KeyError: 'from'`;
- logs do not contain prior DP=8 zero-step or TP=8 scheduler signatures;
- checkpoint/model exists if PM wants to unblock mini-swe;
- `trainer_state.json` and/or `all_results.json` are present for a completed training smoke;
- resource cleanup/stop proof is present.

Mini-swe can proceed only if a checkpoint/model or served endpoint exists and test_2 accepts it.

## FAIL Criteria

Preflight FAIL/BLOCKER:

- missing dev_3 Session 21 dataset_info package;
- missing exact command/package;
- wrong dataset path or checksum;
- dataset_info does not map `messages[*].from/value`;
- base model path is wrong or unverified;
- config can reproduce DP=8 zero-step or TP=8 scheduler failure;
- no PM authorization or no current GPU resource proof.

Post-run FAIL:

- `KeyError: 'from'` appears again;
- dataset_info missing or wrong at runtime;
- logs show `Cannot open data/sft/dataset_info.json`;
- logs show `steps_in_epoch`, `ZeroDivisionError`, or scheduler assertion;
- no logs/manifest/config are provided;
- no checkpoint/model exists and no exact new blocker is recorded;
- resource cleanup proof is missing.

## Current Application

Current application result: **POST_RUN_RESULT: BLOCKED_FINAL_RUNTIME**

Checks that currently pass by durable evidence:

- Task `M1-S21-LAUNCH-GATE-TEST1` is registered.
- ShareGPT artifact path/checksum/count/schema are documented in `dev_3_sft_dataformat_artifact.md`.
- Test_1 previously accepted the artifact as `PASS_NO_EXECUTION` for the observed `messages[*].from/value` reader.
- Base model path is known and accepted from previous gates.
- Config template exists and has the expected TP=8/DP=1, `max_steps=2`, `warmup_steps=0`, `save_steps=1` settings.
- `dev_3_s21_datasetinfo_package.md` exists and passes this gate for the expected ShareGPT `messages/from/value` mapping.
- The accepted dataset_info entry name is `coding_agent_m1_sft_10_sharegpt`.
- `dev_2_s21_sft_runtime.md` exists as a pre-submit runtime plan and confirms no active coding_agent_playground / Milestone 1 / Session 21 retry GPU allocation was running at its check time.
- Dev_2's intended runtime command now uses `DATASET_NAME=coding_agent_m1_sft_10_sharegpt`.
- Dev_2's generated config requirement is `dataset: coding_agent_m1_sft_10_sharegpt`.
- `gpu_s21_resource_tracking.md` confirms the same intended runtime command and generated config requirement.

Post-run validation after dev_2 final runtime evidence:

```text
POST_RUN_RESULT: BLOCKED_FINAL_RUNTIME
```

Runtime evidence reviewed:

- `evidence/dev_2_s21_sft_runtime.md`
- `evidence/gpu_s21_resource_tracking.md`

Validated PASS points:

- PM-authorized Session 21 runtime evidence exists for task `M1-S21-RUNTIME-DEV2`.
- Dataset info/data-format passed at runtime.
- Runtime used dataset entry `coding_agent_m1_sft_10_sharegpt`.
- Runtime config includes `dataset: coding_agent_m1_sft_10_sharegpt`.
- Dataset path was `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Dataset sha256 was `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- ShareGPT conversion completed `10/10`.
- Training reached total optimization steps `2` and step progress `1/2`.
- Previous data-format failure signature was absent: no `KeyError: 'from'`.
- Missing dataset_info signatures were absent: no `Cannot open data/sft/dataset_info.json`.
- Previous tiny-data DP failure signatures were absent: no `ZeroDivisionError` / `steps_in_epoch`.
- Previous TP scheduler failure signature was absent: no scheduler warmup assertion.
- LTP lifecycle was stopped and released: `STOPPED (Completed)`.
- Endpoint proof after stop: `ssh -p 16126 root@10.100.16.54` refused connection.

Blocking FAIL points:

- Runtime ended with `EXIT_STATUS=1`.
- Failure occurred during checkpoint save.
- Exact blocker: `safetensors_rust.SafetensorError: Error while serializing: I/O error: No space left on device (os error 28)`.
- Only partial `checkpoint-1` exists.
- Partial files include `checkpoint-1/config.json` and three `model0_*.safetensors` files.
- `checkpoint-2` is absent.
- `trainer_state.json` is absent.
- `all_results.json` is absent.
- No complete accepted checkpoint/model exists.
- The partial checkpoint must not be handed to eval.

Post-run decision:

```text
dataset_info_status: PASS
data_format_status: PASS
old_failure_signatures_status: PASS_ABSENT
runtime_progress_status: REACHED_SHAREGPT_10_OF_10_AND_STEP_1_OF_2
exit_status: 1
checkpoint_status: BLOCKED_PARTIAL_CHECKPOINT_ONLY
final_blocker: safetensors ENOSPC during checkpoint-1 serialization
mini_swe_can_proceed: false
```

Recommended next gate before any additional runtime:

1. Treat this run as final blocked runtime evidence for the authorized Session 21 attempt.
2. Do not use partial `checkpoint-1` for mini-swe.
3. Any retry must be a new PM-authorized task/gate that addresses checkpoint output capacity/path or save behavior before execution.

Completion marker:

```text
task_id: M1-S21-LAUNCH-GATE-TEST1
gate_definition: COMPLETE
dataset_info_status: PASS
command_wiring_status: PASS
preflight_status: PASS_FOR_PM_AUTHORIZATION
post_run_status: BLOCKED_FINAL_RUNTIME
runtime_exit_status: 1
runtime_blocker: SAFETENSORS_ENOSPC_DURING_CHECKPOINT_SAVE
sft_gpu_eval_executed_by_test1: false
mini_swe_can_proceed: false
```
