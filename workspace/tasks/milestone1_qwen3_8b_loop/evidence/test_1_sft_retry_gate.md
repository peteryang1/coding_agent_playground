# Test 1 SFT Retry Gate

Date: 2026-05-20

Task ID: `M1-SFT-RETRY-GATE-TEST1`

Owner: `intern_code_test_1`

Scope: define the test gate for any proposed SFT retry after the failed Milestone 1 Qwen3-8B smoke.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_sft_retry_gate.md`

## Prior Failure Summary

Source evidence: `evidence/dev_4_sft_smoke_run.md`

The previous approved SFT smoke ran on the H200 route and reached training, but did not produce a checkpoint, `trainer_state.json`, or `all_results.json`.

Known failed attempts:

1. `milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z`
   - Dataset loaded: 10 examples.
   - Distributed tasks initialized: 8.
   - Total optimization steps: 2.
   - Failure: `ZeroDivisionError` in `mcore_adapter/trainer/trainer.py`.
   - Root cause to avoid: baseline data-parallel layout effectively produced `steps_in_epoch=0` with tiny data and MCA `drop_last=True`.

2. `milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z`
   - Dataset loaded: 10 examples.
   - Tensor model parallel initialized with size 8.
   - Failure: `AssertionError` in `megatron/core/optimizer_param_scheduler.py`.
   - Root cause to avoid: one-step bounded smoke violated scheduler invariant `lr_warmup_steps < lr_decay_steps`.

## Retry Authorization Rule

PM should not authorize a new GPU SFT retry unless all three packages exist and are gate-ready:

- Config fix package from `M1-SFT-CONFIG-FIX-DEV4`.
- Resource plan from `M1-GPU-RETRY-RESOURCE-DEV2`.
- This test gate, `M1-SFT-RETRY-GATE-TEST1`.

The retry must be treated as a new task-scoped run. It must not reuse old PR/task completion evidence as proof that the retry is safe.

## Pre-Run Checks

The proposed retry package must include exact values and commands for these checks before any GPU job starts.

### Task And Evidence Checks

Required:

- Task ID in evidence/PR/status: `M1-SFT-RETRY-GATE-TEST1` for this gate and the corresponding dev/resource task ids for implementation.
- Retry run ID, output root, config path, dataset path, base model path, GPU endpoint or current `nodes.json`.
- Explicit statement whether retry is clean-base or approved warm-start.
- Stop/rollback condition if either prior failure signature appears.

Pass criteria:

- Evidence names all paths and task IDs.
- Retry is tied to current Milestone 1 task registry.
- No placeholder model/config/resource path remains.

Fail criteria:

- Any command uses `<placeholder>` values.
- Retry lacks a task id or durable evidence path.
- Retry does not cite the prior DP=8/TP=8 failures.

### Dataset Checks

Required commands:

```bash
test -f /root/workspace/cleaned_m1_sft_10/train.jsonl
sha256sum /root/workspace/cleaned_m1_sft_10/train.jsonl
python3 - <<'PY'
import json
from pathlib import Path
p = Path("/root/workspace/cleaned_m1_sft_10/train.jsonl")
rows = [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
assert len(rows) == 10
assert all(r["format_version"] == "coding_agent_playground_sft_v1" for r in rows)
assert len({r["example_id"] for r in rows}) == 10
assert len({r["trajectory_id"] for r in rows}) == 10
assert all(len(r.get("messages", [])) >= 2 for r in rows)
print("dataset_ok", len(rows))
PY
```

Required baseline dataset identity:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
sha256 5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
```

If a data-side mitigation is used, it must have a separate dev_3 evidence file that records:

- source dataset path and checksum,
- expanded/mitigated dataset path and checksum,
- exact expansion rule,
- original trajectory provenance preservation,
- statement that the expanded data is smoke-only and not quality metrics evidence.

Pass criteria:

- Dataset is either the validated 10-example file or a PM-approved dev_3 mitigation artifact.
- Line count, checksum, schema, and unique IDs are recorded.

Fail criteria:

- Dataset changed without dev_3 handoff.
- Expanded data is used without smoke-only labeling.
- Rejected examples or malformed JSONL are present.

### Base Model Checks

Required clean-base candidate from current evidence:

```text
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

Required command:

```bash
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
test -f "$BASE_MODEL/config.json"
test -f "$BASE_MODEL/tokenizer.json"
test -f "$BASE_MODEL/model.safetensors.index.json"
python3 - <<'PY'
import json, os
d = json.load(open(os.environ["BASE_MODEL"] + "/config.json"))
assert d.get("model_type") == "qwen3"
assert "Qwen3ForCausalLM" in d.get("architectures", [])
print("base_ok", d.get("num_hidden_layers"), d.get("hidden_size"), d.get("vocab_size"))
PY
```

Pass criteria:

- Base path is a readable clean-base candidate or explicitly approved warm-start.
- Config matches Qwen3 8B shape.

Fail criteria:

- Broken symlink `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is used without repair.
- Historical/warm-start path is used while evidence claims clean-base.

### GPU Resource Checks

Required:

- Fresh current GPU endpoint or current Milestone 1 `nodes.json`.
- Proof no stale previous H200 allocation is being reused accidentally.
- `nvidia-smi` output for every node before launch.

Required single-node command:

```bash
hostname
command -v nvidia-smi
nvidia-smi -L
nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader
```

Required multi-node command:

```bash
NODES_JSON=<current-milestone-nodes.json>
python3 - <<'PY'
import json, os
d = json.load(open(os.environ["NODES_JSON"]))
assert d.get("nodes")
for n in d["nodes"]:
    assert "ip" in n and "port" in n and "node_rank" in n, n
print("node_count", len(d["nodes"]))
PY
```

Pass criteria:

- GPU endpoint is current and reachable.
- GPU count and memory are recorded.
- Output path is shared and durable under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.

Fail criteria:

- Retry runs on CPU/login host only.
- No current GPU endpoint or no current `nodes.json`.
- Existing active/stale resource state is ambiguous.

## Tiny-Data-Safe Config Requirements

Any proposed config must state the following values explicitly in a config diff or generated runtime config.

### Data Parallel Safety

The retry must avoid the previous DP=8 tiny-data failure:

- Effective data-parallel size must be 1 for the 10-example smoke, or the dataset must be PM-approved expanded/mitigated so every DP rank has at least one full batch after `drop_last`.
- Evidence must compute or state:
  - dataset examples,
  - micro batch size,
  - gradient accumulation,
  - world size,
  - tensor parallel size,
  - pipeline parallel size if any,
  - data parallel size,
  - expected effective samples per DP rank,
  - expected `steps_in_epoch` or equivalent.

Pass criteria:

- `steps_in_epoch > 0` by config reasoning before launch.
- Config does not create DP=8 over the original 10 examples with `drop_last=True`.

Fail criteria:

- Proposed config leaves DP=8 with 10 examples and no validated data mitigation.
- Evidence does not show why `steps_in_epoch` is positive.

### Scheduler Safety

The retry must avoid the previous TP=8/max_steps=1 scheduler assertion:

- `lr_warmup_steps < lr_decay_steps` must be true.
- If using `max_steps`, then decay steps must be greater than warmup steps and compatible with the trainer.
- One-step smoke is rejected unless dev_4 proves the scheduler accepts it.
- Recommended minimum: `max_steps >= 2` with `warmup_steps=0`, or a documented scheduler setting that makes the invariant pass.

Pass criteria:

- Runtime config includes explicit warmup/decay/max step values.
- Evidence states the computed relation, e.g. `warmup_steps=0 < lr_decay_steps=2`.

Fail criteria:

- `max_steps=1` with default scheduler values.
- Runtime log repeats `assert self.lr_warmup_steps < self.lr_decay_steps`.

### Checkpoint And Metrics Safety

Config must write a minimal checkpoint/metrics artifact quickly:

- `save_steps` must be compatible with smoke length, e.g. `save_steps <= max_steps`.
- `logging_steps <= max_steps`.
- `output_dir` must be under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<run_id>`.
- `overwrite_output_dir` must not delete previous evidence unless run ID is unique.

Pass criteria:

- A successful smoke can produce at least one checkpoint or exported model.
- Logs and metrics are flushed before stop.

Fail criteria:

- No checkpoint can be produced because save interval exceeds smoke steps.
- Output path collides with prior failed run without explicit cleanup/provenance.

## Required Retry Command Shape

The retry command must be fully materialized in evidence before launch.

Template:

```bash
cd /root/workspace/coding_agent_playground
CONFIG_TEMPLATE=<tiny-data-safe-config-path> \
DATASET_JSONL=<validated-or-approved-mitigated-train-jsonl> \
BASE_MODEL=<validated-clean-base-or-approved-warmstart> \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=<unique-m1-sft-retry-run-id> \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Required command assertions:

- `DRY_RUN=0`
- unique `RUN_ID`
- `CONFIG_TEMPLATE` is not the previously failed baseline unless patched.
- `BASE_MODEL` is validated.
- `DATASET_JSONL` is validated and checksummed.
- `OUTPUT_ROOT` is durable.

## Required Artifacts For PASS/FAIL

Every retry, successful or failed, must produce or explicitly explain these paths.

Required command evidence:

- exact command,
- host and GPU endpoint,
- run ID,
- start/end UTC timestamps,
- exit code,
- environment variables relevant to distributed training,
- runtime config path,
- run manifest path,
- stdout/stderr log path.

Required files:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<run_id>/run_manifest.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<run_id>/config/qwen3_8b_sft.yaml
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/<run_id>/logs/train_stdout_stderr.log
```

PASS must additionally include at least one:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<run_id>/trainer_state.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<run_id>/all_results.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<run_id>/checkpoint-*
```

PASS also needs:

- final checkpoint/model path suitable for mini-swe,
- metrics with `global_step >= 1`,
- either `train_loss` or logged loss history,
- no infrastructure traceback in logs.

FAIL evidence must include:

- exact first failing exception and stack frame,
- whether any checkpoint/metrics were produced,
- GPU process cleanup check,
- recommendation: retry again, change config/data/resource, or stop.

## Required Log Assertions

The tester must check logs for both positive and negative assertions.

### Positive assertions

Logs should show:

- dataset loaded,
- base model loaded,
- distributed layout initialized,
- training entered,
- at least one training/logging step completed,
- checkpoint or metrics write if PASS is claimed.

Acceptable examples:

```text
Loaded 10 examples
Loaded clean-base Qwen3 config
Initialized tensor model parallel
total optimization steps
global_step
Saving model checkpoint
```

### Negative assertions

The retry must FAIL the test gate if logs contain any of:

```text
ZeroDivisionError: division by zero
steps_in_epoch
self.state.epoch = epoch + (...) / steps_in_epoch
AssertionError
optimizer_param_scheduler.py
assert self.lr_warmup_steps < self.lr_decay_steps
Cannot open data/sft/dataset_info.json
No such file or directory
CUDA out of memory
No CUDA GPUs are available
nvidia-smi: command not found
```

The retry must also fail if it repeats either prior signature:

- DP/tiny-data failure: `steps_in_epoch=0` or division by zero in MCA trainer epoch calculation.
- TP/scheduler failure: scheduler assertion requiring `lr_warmup_steps < lr_decay_steps`.

## Retry PASS Criteria

A retry is PASS only if all are true:

1. Pre-run dataset, base model, GPU, task ID, and config checks pass.
2. Runtime config is tiny-data-safe and explicitly avoids DP=8/10-example `steps_in_epoch=0`.
3. Scheduler settings explicitly satisfy `lr_warmup_steps < lr_decay_steps`.
4. Command runs with `DRY_RUN=0`.
5. Logs show at least one training step completed.
6. No prior failure signature appears.
7. A checkpoint/model or equivalent mini-swe-usable model artifact exists.
8. `trainer_state.json`, `all_results.json`, or an equivalent metrics file exists.
9. Exit status is 0, or an intentional bounded smoke stop is documented and still produced usable checkpoint/metrics.

## Retry FAIL Criteria

A retry is FAIL if any are true:

- Missing or placeholder pre-run config/resource/model/data.
- Uses old baseline config without explicit tiny-data fix.
- Uses DP=8 over original 10 examples without approved data mitigation.
- Uses `max_steps=1` without proving scheduler validity.
- Repeats `steps_in_epoch=0` / division-by-zero failure.
- Repeats `lr_warmup_steps < lr_decay_steps` assertion.
- Produces no checkpoint/model and no metrics.
- Infrastructure failure prevents training from entering at least one step.
- Evidence does not record exact logs/command/exit code.

## Final Criteria Before PM Can Allow mini-swe

PM should allow mini-swe only after a retry PASS exists and test evidence verifies:

- accepted SFT run ID,
- accepted model/checkpoint path,
- whether clean-base or approved warm-start,
- dataset path and checksum,
- runtime config path,
- log path,
- metrics path,
- checkpoint/model path,
- explicit PASS against this retry gate.

mini-swe remains blocked if:

- retry is not run,
- retry fails,
- retry produces no mini-swe-usable checkpoint/model,
- retry evidence is incomplete,
- model path is a placeholder or points to an old non-retry model.

## Current State

Current status: retry gate defined; no retry is authorized by this file alone.

Open dependencies before PM can authorize a retry:

- dev_4 config fix package must show tiny-data-safe config and prior-failure avoidance.
- dev_2 resource plan must provide current GPU route and stop conditions.
- dev_3 must approve any data mitigation if the retry changes dataset size/content.

