# Test 2 Eval Validation Evidence

Owner: `intern_code_test_2`
Area: Validate mini-swe-agent evaluation setup and final report metrics format; define smoke eval before full run.

## 2026-05-20T05:55:38Z - Assignment Acknowledgement

Received Milestone 1 test assignment from PM. I will only validate the PM-specified owner area and will write confirmations, status, findings, blockers, and results to this file plus my own `status.md`. I will not use peer_send or `/esc` to PM for routine updates.

## Inputs Reviewed

- `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/assignments.md`
- `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/README.md`
- `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/status.md`
- `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/final_report.md`
- `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/blockers.md`
- mini-SWE-agent docs: `https://mini-swe-agent.com/latest/usage/swebench/`
- SWE-bench evaluation docs: `https://www.swebench.com/SWE-bench/guides/evaluation/`

## 2026-05-20T06:22:09Z - Critical Address Correction

PM corrected the final workspace address to:

```text
ssh -p 31787 root@10.100.194.40
```

Previous checks against the earlier scratch host are scratch only and must not be used as the current Milestone 1 eval readiness result.

## Reproducible Setup Checks On Correct Final Workspace

Commands run from `/work-agents/intern_code_test_2/coding_agent_playground`:

```bash
ssh -p 31787 -o BatchMode=yes -o ConnectTimeout=8 root@10.100.194.40 \
  'set -u; echo "## identity"; hostname; pwd; echo "## workspace"; ls -la /root/workspace || true; echo "## repo dirs"; for r in fastapi scikit-learn rich; do if [ -d "/root/workspace/$r" ]; then echo "$r=present"; else echo "$r=missing"; fi; done; echo "## commands"; for c in python3 python pip pip3 uv docker apptainer singularity sb sb-cli mini mini-extra mini-swe-agent; do printf "%s=" "$c"; command -v "$c" || true; done; echo "## python modules"; python3 - <<'"'"'PY'"'"'
import importlib.util
for m in ["mini_swe_agent", "sweagent"]:
    print(f"{m}={bool(importlib.util.find_spec(m))}")
PY
 echo "## versions"; python3 --version || true; docker --version || true; docker info --format "{{.ServerVersion}}" 2>&1 || true; apptainer --version 2>&1 || true; singularity --version 2>&1 || true; sb --version 2>&1 || true; sb-cli --version 2>&1 || true; mini-extra --help 2>&1 | head -40 || true; echo "## disk"; df -h /root/workspace 2>/dev/null | tail -1 || df -h /root | tail -1'
```

Observed:

```text
hostname: lg-cmc-b7r201-k10u23-cpu-000158
/root/workspace exists
fastapi=present
scikit-learn=present
rich=present
python3=/usr/bin/python3
python=/usr/bin/python
pip=/usr/local/bin/pip
pip3=/usr/local/bin/pip3
uv=/usr/local/bin/uv
docker=
apptainer=
singularity=/usr/bin/singularity
sb=
sb-cli=
mini=
mini-extra=
mini-swe-agent=
mini_swe_agent=False
sweagent=False
Python 3.12.3
singularity-ce version 4.1.1
overlay 7.0T 2.7T 4.0T 41% /
```

Supplemental source-tree checks:

```bash
ssh -p 31787 -o BatchMode=yes -o ConnectTimeout=8 root@10.100.194.40 \
  'cd /root/workspace/swe-bench-related/mini-swe-agent && git rev-parse --short HEAD && git status --short && sed -n "/\[project.scripts\]/,/^\[/p" pyproject.toml && uv run --with datasets mini-extra swebench --help 2>&1 | head -100'
```

Observed:

```text
mini-swe-agent source exists at /root/workspace/swe-bench-related/mini-swe-agent
git rev-parse --short HEAD => 0e47fb4
git status --short => M src/minisweagent/environments/apptainer.py
project scripts include mini, mini-swe-agent, mini-extra, mini-e
uv run --with datasets mini-extra swebench --help displays the swebench CLI help
```

SWE-bench-related paths observed:

```text
/root/workspace/swe-bench-related/SWE-bench
/root/workspace/swe-bench-related/mini-swe-agent
/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
/root/workspace/swe-bench-related/output/minisweagent/preds.json
/root/workspace/swe-bench-related/output/minisweagent/astropy__astropy-12907/astropy__astropy-12907.traj.json
```

## Findings On Correct Final Workspace

- Final workspace SSH is reachable and the three selected repos exist under `/root/workspace/{fastapi,scikit-learn,rich}`.
- mini-swe-agent is not installed globally on PATH, and the global Python environment does not expose `mini_swe_agent`/`sweagent`.
- mini-swe-agent source is present at `/root/workspace/swe-bench-related/mini-swe-agent`; from that directory, `uv run --with datasets mini-extra swebench --help` works.
- Local Docker is absent, but Singularity is available: `singularity-ce version 4.1.1`.
- `sb-cli` is absent, so cloud SWE-bench submission is not currently available by CLI.
- SWE-bench source is present at `/root/workspace/swe-bench-related/SWE-bench`; Python import check from that repo reports `swebench=True` and `datasets=True`.
- Existing historical mini-swe-agent output files exist under `/root/workspace/swe-bench-related/output`, but they are not evidence for the current Qwen3-8B checkpoint.
- Disk capacity is sufficient for a smoke attempt at this checkpoint: `/root/workspace` reports 4.0T available.

## Blocker

Current blocker is no longer "missing backend" because Singularity is available on the corrected machine. Current blocker is that the Qwen3-8B checkpoint/model endpoint and exact invocation config have not been provided in this evidence path. A real smoke eval should wait for the intended model string/API environment/checkpoint path, then run from `/root/workspace/swe-bench-related/mini-swe-agent` using `uv run --with datasets mini-extra ... --environment-class singularity`.

## Proposed Smoke Eval Gate Before Full Run

Run this on `ssh -p 31787 root@10.100.194.40` after PM/Dev provides the intended Qwen3-8B model string/API environment/checkpoint path.

1. Environment gate:
   - From `/root/workspace/swe-bench-related/mini-swe-agent`, `uv run --with datasets mini-extra swebench --help` exits 0.
   - Singularity remains available: `singularity --version` exits 0.
   - Qwen3-8B checkpoint/model endpoint is reachable by the exact model string intended for full eval.
2. Agent smoke:
   - Run `uv run --with datasets mini-extra swebench-single` on one SWE-bench Lite or Verified instance with `--environment-class singularity`, `--exit-immediately`, and an explicit output path.
   - Acceptance: trajectory JSON is created, includes the instance id, model name, messages/actions or equivalent trajectory steps, and no infrastructure traceback.
3. Batch smoke:
   - Run `uv run --with datasets mini-extra swebench --subset lite --split dev --slice 0:2 --model <qwen3-8b-model> --environment-class singularity`.
   - Acceptance: two predictions are emitted in SWE-bench JSONL-compatible format.
4. Evaluation smoke:
   - Evaluate the two predictions using the local SWE-bench/Singularity path, or install/authenticate `sb-cli` and submit to SWE-bench cloud.
   - Acceptance: evaluation output includes `results.json`, per-instance results, and logs; failures due to model quality are allowed, infrastructure failures are not.

## Final Metrics Format Requirement

The final report should include a machine-readable metrics block with these fields:

```json
{
  "run_id": "qwen3-8b-mini-swe-agent-<date-or-sha>",
  "model_name_or_path": "<checkpoint-or-serving-model>",
  "agent": "mini-swe-agent",
  "benchmark": "<SWE-bench subset or custom dataset path>",
  "split": "<split>",
  "backend": "<docker|singularity|apptainer|sb-cli|other>",
  "total_instances": 0,
  "instances_submitted": 0,
  "instances_completed": 0,
  "instances_resolved": 0,
  "resolution_rate": 0.0,
  "predictions_path": "<path>",
  "results_json_path": "<path>",
  "instance_results_path": "<path>",
  "logs_path": "<path>",
  "started_at_utc": "<ISO-8601>",
  "finished_at_utc": "<ISO-8601>",
  "status": "<passed|failed|blocked>"
}
```

For SWE-bench compatibility, each prediction line must include at minimum `instance_id`, `model_name_or_path`, and `model_patch`.

## Current Status

Corrected-machine readiness is partial: repos, mini-swe-agent source, SWE-bench source, `uv`, and Singularity are present; global mini-swe-agent CLI and `sb-cli` are absent. Real smoke eval is blocked on PM/Dev-provided Qwen3-8B model endpoint/checkpoint and exact API/config environment. No full eval should start before the corrected-machine smoke gate passes.

## 2026-05-20T06:28:47Z - Session 3 Top-Priority Recheck

Confirmation: rechecked only the corrected final workspace, `ssh -p 31787 root@10.100.194.40`. Did not wait for SFT completion and did not peer_send PM.

Command:

```bash
ssh -p 31787 -o BatchMode=yes -o ConnectTimeout=8 root@10.100.194.40 \
  'set -u; echo "## identity"; hostname; echo "## mini-swe-agent dir"; test -d /root/workspace/swe-bench-related/mini-swe-agent && echo present || echo missing; cd /root/workspace/swe-bench-related/mini-swe-agent && echo "## git"; git rev-parse --short HEAD; git status --short; echo "## scripts"; sed -n "/\[project.scripts\]/,/^\[/p" pyproject.toml; echo "## singularity"; command -v singularity; singularity --version; echo "## uv"; command -v uv; uv --version; echo "## global cli"; command -v mini-extra || true; command -v mini-swe-agent || true; echo "## help"; uv run --with datasets mini-extra swebench --help 2>&1 | head -120'
```

Observed:

```text
hostname: lg-cmc-b7r201-k10u23-cpu-000158
/root/workspace/swe-bench-related/mini-swe-agent: present
mini-swe-agent git sha: 0e47fb4
mini-swe-agent git status:
  M src/minisweagent/environments/apptainer.py
  ?? uv.lock
project scripts: mini, mini-swe-agent, mini-extra, mini-e
singularity: /usr/bin/singularity
singularity-ce version 4.1.1
uv: /usr/local/bin/uv
uv 0.10.4
global mini-extra: absent
global mini-swe-agent: absent
uv run --with datasets mini-extra swebench --help: exits 0 and shows options including --subset, --split, --slice, --output, --workers, --model, --config, --model-class, --environment-class
```

Readiness result:

- mini-swe-agent backend readiness is sufficient to define and launch a smoke once the Qwen3-8B model/checkpoint is available, using the source checkout plus `uv run --with datasets`.
- Singularity is the available local execution backend; Docker and `sb-cli` are not required for the immediate local smoke path.
- Do not rely on global `mini-extra`; run from `/root/workspace/swe-bench-related/mini-swe-agent`.
- The mini-swe-agent checkout is not clean (`src/minisweagent/environments/apptainer.py` modified, `uv.lock` untracked). This is a watch item because eval behavior may depend on the local apptainer/singularity patch.

Exact smoke command once Qwen3-8B is available:

```bash
ssh -p 31787 root@10.100.194.40 'cd /root/workspace/swe-bench-related/mini-swe-agent && mkdir -p /root/workspace/swe-bench-related/output/qwen3_8b_smoke && uv run --with datasets mini-extra swebench --subset lite --split dev --slice 0:2 --model "<QWEN3_8B_MODEL_OR_ENDPOINT>" --environment-class singularity --workers 1 --output /root/workspace/swe-bench-related/output/qwen3_8b_smoke'
```

Optional single-instance debug command before the two-instance batch smoke:

```bash
ssh -p 31787 root@10.100.194.40 'cd /root/workspace/swe-bench-related/mini-swe-agent && mkdir -p /root/workspace/swe-bench-related/output/qwen3_8b_smoke && uv run --with datasets mini-extra swebench-single --subset lite --split dev --instance 0 --model "<QWEN3_8B_MODEL_OR_ENDPOINT>" --environment-class singularity --exit-immediately --output /root/workspace/swe-bench-related/output/qwen3_8b_smoke/single_instance_0.traj.json'
```

Recommended acceptance criteria for the smoke:

- Command exits without mini-swe-agent/Singularity infrastructure traceback.
- Output directory contains trajectory files plus a predictions file.
- Predictions are SWE-bench-compatible JSON/JSONL records with `instance_id`, `model_name_or_path`, and `model_patch`.
- Any model-quality failure is acceptable for smoke; infrastructure failure is not.

Current blocker:

- Missing exact Qwen3-8B model/checkpoint/API configuration. Smoke command is ready except for replacing `<QWEN3_8B_MODEL_OR_ENDPOINT>` and exporting any required API/base URL/token environment variables.

## 2026-05-20T07:07:13Z - Session 5 Eval Smoke Preparation

Scope: prepared mini-swe-agent eval smoke for the eventual SFT smoke model/checkpoint path on corrected final workspace `ssh -p 31787 root@10.100.194.40`. Did not interrupt or modify `/root/workspace/rollouts_m1_10`; only checked that the path exists.

Readiness command:

```bash
ssh -p 31787 -o BatchMode=yes -o ConnectTimeout=8 root@10.100.194.40 \
  'set -u; echo "## rollouts path check no-touch"; if [ -e /root/workspace/rollouts_m1_10 ]; then ls -ld /root/workspace/rollouts_m1_10; else echo missing; fi; echo "## eval paths"; test -d /root/workspace/swe-bench-related/mini-swe-agent && echo mini_swe_agent_dir=present; test -d /root/workspace/swe-bench-related/SWE-bench && echo swebench_dir=present; cd /root/workspace/swe-bench-related/mini-swe-agent && echo "## git"; git rev-parse --short HEAD; git status --short; echo "## runtime config exists"; test -f /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml && echo yes || echo no; echo "## help check"; uv run --with datasets mini-extra swebench --help >/tmp/m1_swebench_help.out 2>/tmp/m1_swebench_help.err; echo help_exit=$?; sed -n "1,40p" /tmp/m1_swebench_help.out; sed -n "1,20p" /tmp/m1_swebench_help.err; echo "## backend"; singularity --version; echo "## output parent"; ls -ld /root/workspace/swe-bench-related/output'
```

Evidence:

```text
/root/workspace/rollouts_m1_10 exists; no-touch check only
mini_swe_agent_dir=present
swebench_dir=present
mini-swe-agent git sha: 0e47fb4
mini-swe-agent git status:
  M src/minisweagent/environments/apptainer.py
  ?? uv.lock
runtime config: /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml exists
help_exit=0
mini-swe-agent version: 1.9.1
singularity-ce version 4.1.1
output parent: /root/workspace/swe-bench-related/output exists
```

Prepared config:

```text
Working directory:
  /root/workspace/swe-bench-related/mini-swe-agent

Config file:
  /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml

Backend:
  --environment-class singularity

Dataset:
  --subset lite --split dev

Smoke size:
  --slice 0:2 --workers 1

Output directory:
  /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke

Model placeholder:
  <SFT_SMOKE_MODEL_OR_CHECKPOINT>

Required model environment placeholders if endpoint-backed:
  OPENAI_API_KEY=<token or dummy token required by endpoint>
  OPENAI_BASE_URL=<serving endpoint base URL>
  optional model class flag if needed: --model-class <mini-swe-agent model class>
```

Exact two-instance smoke command once the SFT smoke model/checkpoint is available:

```bash
ssh -p 31787 root@10.100.194.40 'cd /root/workspace/swe-bench-related/mini-swe-agent && mkdir -p /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke && uv run --with datasets mini-extra swebench --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml --subset lite --split dev --slice 0:2 --model "<SFT_SMOKE_MODEL_OR_CHECKPOINT>" --environment-class singularity --workers 1 --output /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke'
```

Exact single-instance debug command if the two-instance smoke fails at startup:

```bash
ssh -p 31787 root@10.100.194.40 'cd /root/workspace/swe-bench-related/mini-swe-agent && mkdir -p /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke && uv run --with datasets mini-extra swebench-single --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml --subset lite --split dev --instance 0 --model "<SFT_SMOKE_MODEL_OR_CHECKPOINT>" --environment-class singularity --exit-immediately --output /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/single_instance_0.traj.json'
```

Recommendation:

- Use the two-instance batch smoke as the gate before any full mini-swe-agent evaluation.
- Run from source with `uv run --with datasets`; do not rely on global `mini-extra`, because it is not installed on PATH.
- Use Singularity for the corrected final workspace backend.
- Keep `/root/workspace/rollouts_m1_10` untouched while the rollout job is active.

Current blockers:

- Exact SFT smoke model/checkpoint path or endpoint model name is not yet available.
- Required serving/API environment variables are not yet specified.
- mini-swe-agent checkout is dirty (`src/minisweagent/environments/apptainer.py` modified, `uv.lock` untracked); this may be intentional for Singularity support but should be preserved and called out in final eval provenance.

## 2026-05-20T07:17:30Z - Machine-Readable Readiness Metrics

PM wrote the current eval-readiness metrics file on the corrected final workspace:

```text
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json
```

Current metrics status:

```json
{
  "run_id": "milestone1_mini_swe_smoke_readiness_20260520",
  "agent": "mini-swe-agent",
  "backend": "singularity",
  "benchmark": "SWE-bench lite dev slice 0:2",
  "total_instances": 2,
  "instances_submitted": 0,
  "instances_completed": 0,
  "instances_resolved": 0,
  "resolution_rate": 0.0,
  "status": "blocked"
}
```

Blockers in the metrics file:

- SFT smoke model/checkpoint or endpoint is not available yet.
- Required model serving/API environment variables are not specified.

## 2026-05-20T08:47:18Z - Current Mini-SWE Eval Acceptance Gate Package

Scope: current gate package for mini-swe-agent smoke while dev_4 continues SFT. PM is gating/deciding and will not run eval; this package defines what test_2 will accept and verify before marking the mini-swe smoke ready/pass.

### Accepted SFT Artifact Forms

Accepted form A: served endpoint.

- `SFT_SMOKE_MODEL` is a model name usable by mini-swe-agent/litellm, for example `hosted_vllm/<served-model-name>` or another litellm-compatible model string.
- `OPENAI_BASE_URL` points at the OpenAI-compatible `/v1` endpoint for the served SFT smoke checkpoint.
- `OPENAI_API_KEY` is exported if the endpoint requires it; a dummy token is acceptable only if the endpoint explicitly ignores auth.
- Optional: `MINI_SWE_MODEL_CLASS` can be provided if the default litellm model class is not correct.

Accepted form B: raw checkpoint path, only if accompanied by serving instructions.

- `SFT_SMOKE_CHECKPOINT_PATH` points to a readable HF-compatible model directory or a pinned training output checkpoint, for example a durable path under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/<run_id>/checkpoint-*` or `training_summary/model`.
- The raw checkpoint path alone is not directly acceptable to mini-swe-agent, because mini-swe-agent calls a model endpoint/model API. It must be served first, then converted into accepted form A by providing `SFT_SMOKE_MODEL`, `OPENAI_BASE_URL`, and any auth/env values.
- The checkpoint path must be recorded in final eval provenance even when evaluation runs through an endpoint.

### Required Env And Config Checks

Run on corrected final workspace:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
test -d /root/workspace/swe-bench-related/mini-swe-agent
test -d /root/workspace/swe-bench-related/SWE-bench
test -f /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
command -v uv
command -v singularity
singularity --version
uv run --with datasets mini-extra swebench --help >/tmp/m1_mini_swe_help.out
test -n "${SFT_SMOKE_MODEL:-}"
test -n "${OPENAI_BASE_URL:-}"
python3 - <<PY
import os
print("SFT_SMOKE_MODEL=", os.environ.get("SFT_SMOKE_MODEL"))
print("OPENAI_BASE_URL=", os.environ.get("OPENAI_BASE_URL"))
print("OPENAI_API_KEY_present=", bool(os.environ.get("OPENAI_API_KEY")))
print("SFT_SMOKE_CHECKPOINT_PATH=", os.environ.get("SFT_SMOKE_CHECKPOINT_PATH", ""))
PY'
```

If a raw checkpoint path is provided, also run:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
test -n "${SFT_SMOKE_CHECKPOINT_PATH:-}"
test -d "$SFT_SMOKE_CHECKPOINT_PATH"
test -f "$SFT_SMOKE_CHECKPOINT_PATH/config.json"
test -f "$SFT_SMOKE_CHECKPOINT_PATH/tokenizer_config.json" || test -f "$SFT_SMOKE_CHECKPOINT_PATH/tokenizer.json"
find "$SFT_SMOKE_CHECKPOINT_PATH" -maxdepth 1 \( -name "*.safetensors" -o -name "pytorch_model*.bin" \) | head -1 | grep -q .'
```

### Exact Smoke Commands

Two-instance batch gate:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
export SFT_SMOKE_MODEL="<served-litellm-model-name>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-endpoint-ignores-auth>"
export SFT_SMOKE_CHECKPOINT_PATH="<optional-durable-checkpoint-path-for-provenance>"
OUT=/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
mkdir -p "$OUT"
uv run --with datasets mini-extra swebench \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --slice 0:2 \
  --model "$SFT_SMOKE_MODEL" \
  --environment-class singularity \
  --workers 1 \
  --output "$OUT"'
```

Single-instance debug fallback:

```bash
ssh -p 31787 root@10.100.194.40 'set -euo pipefail
cd /root/workspace/swe-bench-related/mini-swe-agent
export SFT_SMOKE_MODEL="<served-litellm-model-name>"
export OPENAI_BASE_URL="<openai-compatible-base-url>/v1"
export OPENAI_API_KEY="<token-or-dummy-if-endpoint-ignores-auth>"
OUT=/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
mkdir -p "$OUT"
uv run --with datasets mini-extra swebench-single \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --instance 0 \
  --model "$SFT_SMOKE_MODEL" \
  --environment-class singularity \
  --exit-immediately \
  --output "$OUT/single_instance_0.traj.json"'
```

### Prediction, Result, And Metrics Files To Verify

Expected output root:

```text
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
```

Required mini-swe output checks:

- At least one trajectory JSON exists under the output root or its instance subdirectories.
- `preds.json` or an equivalent predictions JSON/JSONL file exists after the batch run.
- Every prediction record for the smoke slice has `instance_id`, `model_name_or_path`, and `model_patch`.
- `model_name_or_path` equals the accepted `SFT_SMOKE_MODEL`.
- Logs exist under the output root or mini-swe-agent output log path and contain no infrastructure traceback from mini-swe-agent, litellm auth/config, dataset loading, or Singularity startup.

Required result/metrics checks:

- If local SWE-bench scoring is run, verify `results.json` or equivalent per-instance result output and record:
  - total instances
  - completed instances
  - resolved instances
  - resolution rate
  - results path
- If scoring is not run in the same smoke, write `metrics_readiness.json` with `status="blocked"` or `status="predictions_only"` and explicit reason.
- Final metrics file path for this smoke remains:

```text
/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json
```

Minimum metrics schema:

```json
{
  "run_id": "milestone1_mini_swe_smoke_<timestamp>",
  "model_name_or_path": "<SFT_SMOKE_MODEL>",
  "checkpoint_path": "<SFT_SMOKE_CHECKPOINT_PATH or empty>",
  "agent": "mini-swe-agent",
  "backend": "singularity",
  "benchmark": "SWE-bench lite dev slice 0:2",
  "total_instances": 2,
  "instances_submitted": 2,
  "instances_completed": 0,
  "instances_resolved": 0,
  "resolution_rate": 0.0,
  "predictions_path": "<path-to-preds>",
  "results_json_path": "<path-to-results-or-empty>",
  "logs_path": "<path-to-logs>",
  "status": "<passed|failed|blocked|predictions_only>",
  "blockers": []
}
```

### Pass/Fail Criteria

Pass:

- Corrected final workspace is used: `ssh -p 31787 root@10.100.194.40`.
- Endpoint or served checkpoint satisfies accepted form A.
- Required env/config checks pass.
- `uv run --with datasets mini-extra swebench --help` exits 0 from `/root/workspace/swe-bench-related/mini-swe-agent`.
- Singularity backend starts without infrastructure failure.
- Two smoke predictions are produced for `--slice 0:2`.
- Prediction records include required SWE-bench fields.
- Metrics/readiness JSON is written with artifact paths and `status="passed"` if scoring ran, or `status="predictions_only"` if prediction generation passed but scoring is intentionally deferred.

Fail:

- Wrong host or scratch host is used.
- Raw checkpoint path is provided without serving endpoint/model name.
- Endpoint auth/base URL/model string fails before any prediction is produced.
- mini-swe-agent, dataset loading, or Singularity fails with infrastructure traceback.
- Predictions file is missing or lacks required `instance_id`, `model_name_or_path`, or `model_patch`.
- Metrics/readiness JSON is missing after the attempt.

Blocked:

- SFT checkpoint or endpoint is not yet available.
- Required serving env vars are not specified.
- Provided checkpoint path is unreadable or not HF-compatible.
- Endpoint exists but is not reachable from corrected final workspace.

### Dirty Mini-SWE Checkout Provenance Decision

Decision: acceptable for smoke only with explicit provenance note; not acceptable as silent state.

Current dirty state to record with every smoke result:

```text
/root/workspace/swe-bench-related/mini-swe-agent
git sha: 0e47fb4
dirty files:
  M src/minisweagent/environments/apptainer.py
  ?? uv.lock
```

Reasoning:

- The modified `src/minisweagent/environments/apptainer.py` may be the local compatibility patch enabling Singularity/Apptainer backend behavior on this machine.
- Since the active backend is Singularity, this dirty state can affect eval behavior and must be treated as part of the evaluation environment.
- For Milestone 1 smoke, proceed if PM/dev_4 accepts this provenance note.
- For a formal final report, either commit/pin the patch, export a diff next to eval artifacts, or rerun on a clean pinned checkout with an equivalent committed Singularity backend.
