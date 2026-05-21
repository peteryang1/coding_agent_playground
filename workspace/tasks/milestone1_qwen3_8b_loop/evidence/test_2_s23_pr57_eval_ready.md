# Test 2 S23 PR57 Mini-SWE Eval Ready Gate

Task ID: `M1-S23-PR57-EVAL-READY-TEST2`

Owner: `intern_code_test_2`

Updated: 2026-05-21T15:52:00Z

Scope: prepare mini-swe eval handoff gate while dev_2 owns PR57 SFT runtime. No eval, GPU, SFT, dry-run, remote transfer, or remote command was run by test_2.

## Source Evidence Read

- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- `evidence/pm_s23_pr57_preflight_sft_authorization.md`
- `evidence/dev_4_s23_pr55_sft_wrapper_fix.md`

Upstream runtime task: `M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2`, owner `intern_code_dev_2`.

## Current PR57 State

PR57 and completion-marker state from durable evidence:

```text
PR #57 merged at: 2026-05-21T15:45:10Z
PR #57 merge commit: c450429c2e3369adc723d132396399cd17dba684
Completion PR #58 merged at: 2026-05-21T15:48:30Z
origin/main commit authorized for PR57 runtime: b4ac31ef1e3772953108348bf099818326ed65cc
dev_1 PR57 gate: PASS_FOR_PM_RETRY
test_1 PR57 gate: PASS_FOR_PM_RETRY
dev_2 PR55 recovery: no active job
dev_3 data package: no data/package change needed
```

PM authorized dev_2 for exactly one PR57 runtime at `2026-05-21T15:50:00Z`. Eval is explicitly not authorized in that runtime authorization.

As of this evidence update, test_2 found no PR57 runtime result evidence file with a produced checkpoint/model or served endpoint. The required dev_2 output paths are listed by PM as pending:

```text
evidence/dev_2_s23_pr57_preflight_sft_runtime.md
evidence/gpu_s23_pr57_preflight_sft_tracking.md
workspace/interns/intern_code_dev_2/status.md
```

Current test_2 marker:

```text
READY_PACKAGE_BLOCKED_NO_PR57_MODEL
```

## Remote Node No-External-Network Rule

For any future PR57 SFT or eval handoff, remote GPU/LTP nodes must be treated as no-external-network for project code and dependency staging.

Required PR57 upstream runtime transfer/provenance evidence before eval can be considered:

```text
source commit: exact local/provided-workspace commit, expected current PR57 runtime basis b4ac31ef1e3772953108348bf099818326ed65cc unless PM supersedes it
local file list: recorded before transfer
local checksums: source bundle, critical scripts/configs, data, and dependency bundle if used
transfer method: exact rsync/scp/tar-over-SSH command
remote destination: exact path on the allocated node
post-transfer verification: sha256/file count/critical file checks after transfer
remote network proof: no remote git clone/fetch/GitHub/source/dependency download for project code/dependencies
```

This eval package does not replace dev_2's required transfer/runtime evidence. It defines what test_2 will require before mini-swe can run.

## Accepted Future Model Forms

Accepted form A, served endpoint:

```text
OPENAI_BASE_URL or equivalent endpoint URL reachable from the corrected mini-swe runner
OPENAI_API_KEY or explicit no-auth instruction
MODEL_NAME or exact served model id
serving provenance: upstream task id, checkpoint/model source, source commit, serving command/config, endpoint health log
health check: endpoint responds to a minimal completion request before mini-swe
PM authorization: PM explicitly names this endpoint/model id as eval-approved
```

Accepted form B, complete checkpoint/model plus serving handoff:

```text
SFT_CHECKPOINT_PATH or MODEL_PATH exists and is complete
required model files: config/tokenizer files plus weights or adapter files required by the serving stack
trainer_state.json present, or PM documents an explicit replacement provenance record
all_results.json present, or PM documents an explicit replacement metrics record
source/runtime provenance: PR57 runtime task id, source commit, bundle checksum, file list, data checksum, transfer command, post-transfer verification
serving handoff: exact serving command/config, resolved model id, port/base URL, logs, and health check
PM authorization: PM explicitly gates this checkpoint/model or resulting endpoint for eval
```

Rejected current forms:

```text
No PR57 checkpoint/model evidence has landed.
No PR57 trainer_state.json evidence has landed.
No PR57 all_results.json evidence has landed.
No PR57 served endpoint/model id evidence has landed.
Prior PR55 no-model state is not eval-usable.
```

## Future Eval Storage Paths

All future mini-swe generated logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates must remain under `/home/xu.yang`.

Planned eval root for PR57:

```text
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2
LOG_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/logs
PREDICTIONS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/predictions
RESULTS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/results
METRICS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/metrics
RUN_METADATA_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/run_metadata
INTERMEDIATES_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/intermediates
TMPDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/tmp
HF_HOME=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/cache/hf_home
HF_DATASETS_CACHE=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/cache/hf_datasets
UV_CACHE_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/cache/uv
APPTAINER_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/cache/apptainer
SINGULARITY_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/cache/singularity
```

Expected mini-swe output files after a future authorized smoke:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/predictions/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/results/results.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/metrics/metrics.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/run_metadata/run_metadata.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2/logs/mini_swe_smoke.log
```

Existing required-path exceptions to the `/home/xu.yang` rule:

```text
/root/workspace/swe-bench-related/mini-swe-agent
  justification: required mini-swe source checkout on the corrected final workspace.

/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
  justification: required existing SWE-bench/mini-swe config path on the corrected final workspace.
```

## Future Smoke Command Template

Do not run this command until PM explicitly gates a checkpoint/model or served endpoint for eval.

```bash
ssh -p 31787 root@10.100.194.40 '
  set -euo pipefail
  export EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_eval_test2
  export LOG_DIR=$EVAL_ROOT/logs
  export PREDICTIONS_DIR=$EVAL_ROOT/predictions
  export RESULTS_DIR=$EVAL_ROOT/results
  export METRICS_DIR=$EVAL_ROOT/metrics
  export RUN_METADATA_DIR=$EVAL_ROOT/run_metadata
  export INTERMEDIATES_DIR=$EVAL_ROOT/intermediates
  export TMPDIR=$EVAL_ROOT/tmp
  export HF_HOME=$EVAL_ROOT/cache/hf_home
  export HF_DATASETS_CACHE=$EVAL_ROOT/cache/hf_datasets
  export UV_CACHE_DIR=$EVAL_ROOT/cache/uv
  export APPTAINER_CACHEDIR=$EVAL_ROOT/cache/apptainer
  export SINGULARITY_CACHEDIR=$EVAL_ROOT/cache/singularity
  export OPENAI_BASE_URL=<PM_GATED_ENDPOINT_BASE_URL>
  export OPENAI_API_KEY=<PM_GATED_API_KEY_OR_DUMMY_IF_NO_AUTH>
  export MODEL_NAME=<PM_GATED_MODEL_ID>
  mkdir -p "$LOG_DIR" "$PREDICTIONS_DIR" "$RESULTS_DIR" "$METRICS_DIR" "$RUN_METADATA_DIR" "$INTERMEDIATES_DIR" "$TMPDIR" "$HF_HOME" "$HF_DATASETS_CACHE" "$UV_CACHE_DIR" "$APPTAINER_CACHEDIR" "$SINGULARITY_CACHEDIR"
  cd /root/workspace/swe-bench-related/mini-swe-agent
  git rev-parse HEAD | tee "$RUN_METADATA_DIR/mini_swe_git_head.txt"
  git status --short | tee "$RUN_METADATA_DIR/mini_swe_git_status.txt"
  uv run --with datasets mini-extra swebench \
    --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
    --split test \
    --subset verified \
    --workers 1 \
    --instances <PM_GATED_SMOKE_INSTANCE_ID_OR_LIST> \
    --model "$MODEL_NAME" \
    --output "$RESULTS_DIR/results.json" \
    --predictions-path "$PREDICTIONS_DIR/preds.json" \
    2>&1 | tee "$LOG_DIR/mini_swe_smoke.log"
'
```

## Metrics And PASS Criteria

Before execution, test_2 must verify:

```text
PM eval authorization explicitly names checkpoint/model or endpoint.
Model target form is accepted as form A or form B above.
All eval output/cache/temp paths resolve under /home/xu.yang.
mini-swe source git head/status is captured in run metadata.
Endpoint health check or checkpoint serving handoff passes before mini-swe.
```

Smoke PASS requires:

```text
mini-swe command exits 0
predictions file exists and is non-empty
results file exists when SWE-bench scoring is requested
metrics file/run metadata records model id, source task, source commit, checkpoint or endpoint, mini-swe git head/status, instance ids, start/end UTC, exit status, and artifact paths
no generated eval artifact is outside /home/xu.yang
no unauthorized remote project code/dependency clone/fetch/download is recorded for the eval handoff
```

Smoke FAIL requires a reproducible blocker record with:

```text
command
environment
model target
instance id/list
logs path
predictions/results/metrics presence or absence
exit status
first actionable error
```

## Exact Current Blocker

Current blocker:

```text
BLOCKED_NO_PR57_MODEL_OR_ENDPOINT
```

Mini-swe cannot run now because no PM-gated PR57 checkpoint/model or served endpoint is available in durable evidence. PR57 runtime is dev_2-owned and eval remains explicitly unauthorized until PM gates a concrete model target.

## Exact Unblock Condition

PM may unblock test_2 mini-swe execution only when all of the following are true:

1. Dev_2 or a PM-approved replacement evidence names a complete PR57 checkpoint/model path or a live served endpoint/model id.
2. The upstream evidence includes local/provided-workspace source packaging, exact commit/file list/checksums, transfer command, remote destination, post-transfer verification, and no-remote-project-code/dependency-network proof.
3. For checkpoint/model form, required config/tokenizer/weight or adapter files are complete, and `trainer_state.json` plus `all_results.json` are present or explicitly replaced by PM-approved provenance/metrics records.
4. For served endpoint form, the endpoint/base URL is reachable, the exact model id is provided, auth requirements are known, and a minimal completion health check passes.
5. PM explicitly states that the named checkpoint/model or endpoint is eval-approved for mini-swe.
6. All generated eval logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates are written under `/home/xu.yang`; any non-`/home/xu.yang` input paths are recorded with justification.

Until then, mini-swe remains ready-blocked and no eval/GPU/SFT/dry-run should be run by test_2.
