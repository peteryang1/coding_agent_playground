# Test 1 SFT + mini-swe Completion Audit Gate

Date: 2026-05-20

Owner: `intern_code_test_1`

Purpose: define the minimum audit evidence PM needs before marking the Milestone 1 SFT + mini-swe loop complete. This gate is based on current milestone evidence and is intentionally stricter than dry-run/readiness checks.

## Scope

This gate covers:

- Real SFT smoke for Qwen3-8B on the cleaned 10-trajectory SFT dataset.
- mini-swe-agent smoke evaluation of the resulting SFT smoke model/checkpoint.
- Required files, commands, artifacts, metrics, pass/fail criteria, and current evidence gaps.

It does not approve the full 300-trajectory rollout, full training, or full benchmark evaluation by itself.

## Inputs Already Available

Current usable evidence:

- SFT input handoff: `/root/workspace/cleaned_m1_sft_10/train.jsonl`
- SFT input checksum from dev_3 handoff: `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`
- SFT input validation: 10 JSONL examples, 10 kept, 0 dropped, 0 rejected, schema `coding_agent_playground_sft_v1`
- Complete-process validation: 10 checked, 10 valid, 0 invalid
- SFT dry-run manifest:
  `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/run_manifest.json`
- mini-swe readiness metrics:
  `/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json`
- mini-swe source path:
  `/root/workspace/swe-bench-related/mini-swe-agent`
- mini-swe backend readiness: `uv run --with datasets mini-extra swebench --help` works from source; Singularity is available.

## Gate A: Pre-SFT Environment And Input Gate

PM must not mark the loop complete until this gate is passed on the corrected final workspace or a documented GPU worker for this milestone.

Corrected final workspace entry:

```bash
ssh -p 31787 root@10.100.194.40
```

Required files:

- `/root/workspace/coding_agent_playground/scripts/train_qwen3_8b_sft.sh`
- `/root/workspace/coding_agent_playground/scripts/write_sft_run_manifest.py`
- `/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft.yaml`
- `/root/workspace/cleaned_m1_sft_10/train.jsonl`
- `/root/workspace/cleaned_m1_sft_10/conversion_summary.json`
- `/root/workspace/cleaned_m1_sft_10/rejected.jsonl`
- A valid base model path:
  - preferred clean base: `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B`
  - or explicitly approved warm-start fallback, clearly labeled as warm-start smoke
- A GPU execution target:
  - single GPU node where `nvidia-smi` works, or
  - current Milestone 1 `nodes.json` for multi-node launch

Required commands and expected results:

```bash
ssh -p 31787 root@10.100.194.40
test -f /root/workspace/cleaned_m1_sft_10/train.jsonl
sha256sum /root/workspace/cleaned_m1_sft_10/train.jsonl
python3 - <<'PY'
import json
from pathlib import Path
p = Path("/root/workspace/cleaned_m1_sft_10/train.jsonl")
rows = [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
assert len(rows) == 10
assert all(r.get("format_version") == "coding_agent_playground_sft_v1" for r in rows)
assert len({r["example_id"] for r in rows}) == 10
assert len({r["trajectory_id"] for r in rows}) == 10
assert all(isinstance(r.get("messages"), list) and len(r["messages"]) >= 2 for r in rows)
print("sft_input_ok", len(rows))
PY
```

GPU/base-model validation:

```bash
command -v nvidia-smi
nvidia-smi -L
test -f "$BASE_MODEL/config.json"
python3 - <<'PY'
import json, os
p = os.environ["BASE_MODEL"] + "/config.json"
d = json.load(open(p))
assert d.get("model_type") == "qwen3"
assert "Qwen3ForCausalLM" in d.get("architectures", [])
print("base_model_ok", d.get("max_position_embeddings"), d.get("vocab_size"))
PY
```

Pass criteria:

- Dataset file exists, hash is recorded, and schema checks pass.
- Base model path resolves to a readable Qwen3-8B-compatible HF config.
- GPU target is real and current for this milestone.
- If warm-start is used, the evidence explicitly says this is a warm-start smoke, not clean-base SFT.

Fail criteria:

- Clean base path is a broken symlink unless a warm-start fallback is explicitly approved.
- No `nvidia-smi` on the actual training target.
- Dataset count/hash/schema differs from the handoff without a new dev_3 handoff.

## Gate B: Real SFT Smoke Gate

Dry-run does not satisfy this gate. A real `DRY_RUN=0` SFT smoke must run.

Required command, clean-base path:

```bash
ssh -p <gpu_port> root@<gpu_host>
cd /root/workspace/coding_agent_playground
mkdir -p code/LLamaFactory code/mcore_adapter
tar -xf /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz -C code/LLamaFactory --strip-components=1
rsync -a /mnt/3fs/data/ai4ai/deps/mcore_adapter/ code/mcore_adapter/
pip install --break-system-packages -e code/LLamaFactory/ --no-deps
pip install --break-system-packages peft accelerate datasets 'trl<=0.24.0,>=0.18.0'
pip install --break-system-packages /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
pip install --break-system-packages -e code/mcore_adapter/ --no-deps
python3 -c "import flash_attn, mcore_adapter; print('gpu deps ok')"
llamafactory-cli version
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_sft_cleanbase_smoke_$(date -u +%Y%m%dT%H%M%SZ) \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Warm-start fallback command, only if PM/supervisor approves:

```bash
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-final
```

Required output artifacts:

Under:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/
```

The real run must produce:

- `runs/train/<run_id>/run_manifest.json`
- `runs/train/<run_id>/config/qwen3_8b_sft.yaml`
- `runs/train/<run_id>/logs/` or equivalent captured stdout/stderr log path
- `training_summary/sft_output/<run_id>/trainer_state.json`
- `training_summary/sft_output/<run_id>/all_results.json` or equivalent LLamaFactory metrics file
- at least one checkpoint directory, e.g. `training_summary/sft_output/<run_id>/checkpoint-*`, or an explicitly exported final model directory
- a final model/checkpoint path that mini-swe can reference

Required manifest fields:

- `run_id`
- `git_commit`
- `base_model`
- `data.train_path`
- `data.train_sha256`
- `config_path`
- `config_sha256`
- `artifacts.checkpoint_dir`
- `commands`
- `environment` or equivalent runtime environment block
- `started_at_utc` and, after completion, `finished_at_utc` or final status timestamp

Required SFT smoke metrics:

At minimum one of `trainer_state.json`, `all_results.json`, or an explicit metrics JSON must include:

- training status: completed or intentionally stopped after a documented smoke step
- number of training examples observed or dataloader examples
- `train_runtime` or elapsed seconds
- `train_loss` or logged loss history
- `global_step`
- checkpoint path
- GPU node identity and GPU count

Pass criteria:

- Command exits 0, or exits after a documented intentional smoke stop that still writes a usable checkpoint.
- `DRY_RUN=0` is recorded in command or manifest.
- Training consumes `/root/workspace/cleaned_m1_sft_10/train.jsonl` with the recorded checksum.
- A checkpoint or exported model exists and can be loaded or referenced by the eval smoke.
- Logs show no infrastructure traceback, missing model files, missing CUDA, missing dataset, or dependency import failure.

Fail criteria:

- Only dry-run manifest exists.
- Training starts from an unapproved historical checkpoint while claiming clean-base SFT.
- No checkpoint/exported model is produced.
- Logs show infrastructure failure, missing GPU, broken base path, missing dataset, missing LLamaFactory, or dependency import error.

## Gate C: mini-swe Smoke Eval Gate

This gate must use the SFT smoke checkpoint/model from Gate B. A readiness file or placeholder model is not enough.

Working directory:

```text
/root/workspace/swe-bench-related/mini-swe-agent
```

Required precheck:

```bash
ssh -p 31787 root@10.100.194.40
cd /root/workspace/swe-bench-related/mini-swe-agent
uv run --with datasets mini-extra swebench --help
singularity --version
test -e "<SFT_SMOKE_MODEL_OR_CHECKPOINT>"
```

Required two-instance smoke command:

```bash
ssh -p 31787 root@10.100.194.40 'cd /root/workspace/swe-bench-related/mini-swe-agent && mkdir -p /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke && uv run --with datasets mini-extra swebench --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml --subset lite --split dev --slice 0:2 --model "<SFT_SMOKE_MODEL_OR_CHECKPOINT>" --environment-class singularity --workers 1 --output /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke'
```

Optional single-instance debug command if batch smoke fails at startup:

```bash
ssh -p 31787 root@10.100.194.40 'cd /root/workspace/swe-bench-related/mini-swe-agent && mkdir -p /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke && uv run --with datasets mini-extra swebench-single --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml --subset lite --split dev --instance 0 --model "<SFT_SMOKE_MODEL_OR_CHECKPOINT>" --environment-class singularity --exit-immediately --output /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/single_instance_0.traj.json'
```

Required mini-swe output artifacts:

Under:

```text
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/
```

The smoke must produce:

- command log: stdout/stderr capture or terminal transcript
- trajectory file(s) for each attempted instance
- predictions file in JSON/JSONL format
- metrics file, recommended name: `metrics.json`
- if local SWE-bench evaluation is run: `results.json` and per-instance result details
- provenance note with mini-swe git SHA, dirty status, backend, model path, and command

Required prediction fields:

Each prediction record must include at least:

- `instance_id`
- `model_name_or_path`
- `model_patch`

Required metrics:

```json
{
  "run_id": "<sft-smoke-eval-run-id>",
  "model_name_or_path": "<SFT checkpoint/model used>",
  "agent": "mini-swe-agent",
  "benchmark": "SWE-bench lite",
  "split": "dev",
  "slice": "0:2",
  "backend": "singularity",
  "total_instances": 2,
  "instances_submitted": 2,
  "instances_completed": 2,
  "instances_resolved": 0,
  "resolution_rate": 0.0,
  "predictions_path": "<path>",
  "results_json_path": "<path or null if not evaluated>",
  "logs_path": "<path>",
  "started_at_utc": "<ISO-8601>",
  "finished_at_utc": "<ISO-8601>",
  "status": "passed"
}
```

Pass criteria:

- The command uses the actual SFT smoke checkpoint/model from Gate B.
- mini-swe command exits without infrastructure traceback.
- `instances_submitted == 2`.
- `instances_completed == 2`, unless a single-instance debug gate is explicitly substituted and marked as partial.
- Predictions file contains two parseable records with required SWE-bench fields.
- Trajectory/log files exist for the attempted instances.
- Model quality failures are allowed for smoke; infrastructure failures are not.

Fail criteria:

- Model placeholder is used instead of real SFT checkpoint/model.
- Output only contains readiness metrics with `instances_submitted=0`.
- mini-swe cannot start due to missing model/API env/Singularity/dataset.
- Predictions file is missing, unparsable, or lacks `instance_id`, `model_name_or_path`, or `model_patch`.
- No trajectory/log provenance exists.

## Gate D: PM Completion Decision Record

Before PM marks the loop complete, a final audit block should exist in milestone evidence or final report with:

- SFT run ID and checkpoint/model path.
- Whether the run is clean-base or warm-start.
- Dataset path and SHA-256.
- SFT command and exit status.
- SFT metrics path and key metrics.
- mini-swe command and exit status.
- mini-swe predictions path.
- mini-swe metrics path.
- Submitted/completed/resolved counts.
- Known caveats.
- Explicit PASS/FAIL for the completion gate.

Minimum final status values:

- `passed`: real SFT smoke and mini-swe smoke both pass.
- `partial`: one gate ran but the other is blocked; PM should not mark loop complete.
- `blocked`: required base model/GPU/model endpoint is unavailable.
- `failed`: real command ran and failed due to infrastructure or artifact contract issue.

## Current Insufficient Evidence

The current milestone evidence is not enough to mark the SFT + mini-swe loop complete.

Insufficient SFT evidence:

- Existing SFT command evidence is dry-run only (`DRY_RUN=1`).
- No real `DRY_RUN=0` SFT smoke has been recorded.
- No current GPU allocation or milestone-specific `nodes.json` exists in evidence.
- Corrected final workspace entry host has no `nvidia-smi`.
- Preferred clean base path `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is a broken symlink.
- Historical Qwen3-8B checkpoints are fallback candidates only; using them requires explicit warm-start approval.
- No SFT smoke checkpoint/exported model has been produced for this milestone.
- No real SFT training metrics (`trainer_state.json`, `all_results.json`, loss/global_step/runtime) exist for a milestone smoke run.

Insufficient mini-swe evidence:

- mini-swe evidence is readiness-only.
- `metrics_readiness.json` has `status: blocked`, `instances_submitted: 0`, `instances_completed: 0`.
- No exact SFT smoke checkpoint/model path or serving endpoint has been provided to mini-swe.
- No mini-swe smoke command has been run against an SFT smoke model.
- No predictions file exists for the SFT smoke model.
- No SWE-bench result JSON/per-instance evaluation exists for this milestone model.
- mini-swe checkout is dirty (`src/minisweagent/environments/apptainer.py` modified, `uv.lock` untracked); this may be intentional for Singularity support but must be recorded in eval provenance.

Insufficient completion evidence:

- Current evidence proves rollout/data conversion readiness and SFT/eval command readiness, not an end-to-end SFT + eval loop.
- PM cannot mark the loop complete until real SFT smoke produces a checkpoint/model and mini-swe smoke consumes that checkpoint/model and writes metrics/predictions.

## Audit Gate Summary

PM can mark the SFT + mini-swe smoke loop complete only when all are true:

1. SFT input is the validated 10-example JSONL or a newer validated dev_3 handoff.
2. A clean-base or explicitly approved warm-start real SFT smoke runs with `DRY_RUN=0`.
3. The SFT smoke produces a durable checkpoint/model, run manifest, config, logs, and metrics.
4. mini-swe smoke runs against that exact SFT checkpoint/model.
5. mini-swe smoke writes trajectories, predictions, logs, and metrics.
6. Metrics show at least two submitted and two completed instances for the two-instance smoke, unless PM explicitly accepts a documented single-instance partial debug gate.
7. All commands, paths, metrics, caveats, and pass/fail status are recorded durably.

