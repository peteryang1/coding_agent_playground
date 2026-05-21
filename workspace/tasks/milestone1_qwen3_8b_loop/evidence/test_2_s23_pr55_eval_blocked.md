# Test 2 S23 PR55 Mini-SWE Eval Blocked Evidence

Task ID: `M1-S23-PR55-EVAL-REBLOCK-TEST2`

Owner: `intern_code_test_2`

Updated: 2026-05-21T15:29:58Z

Scope: refresh mini-swe eval blocked evidence after PR55 SFT failed before checkpoint. No eval was run by test_2.

## Source Evidence Read

- `evidence/dev_2_s23_pr55_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr55_preflight_sft_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

Upstream runtime task: `M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2`, owner `intern_code_dev_2`.

## Upstream Runtime Facts

Final upstream status:

```text
BLOCKED_PR55_SFT_WRAPPER_ENV_DEP_TARGET_UNBOUND_STOPPED_NO_CHECKPOINT
```

PR55/runtime provenance:

```text
PR #55 merge commit: 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
source bundle sha256: db82b9162af2c37d670e568e16002cfc595e9090d578121545827622c3141df7
source file list count: 118
ShareGPT data sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Resource/storage/transfer status:

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
endpoint during run: ssh -p 15535 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
forbidden-node check: PASS, node is not in the forbidden list
/mnt/cephfs: fuse.ceph-fuse
output root: /home/xu.yang/coding_agent_playground/outputs on fuse.ceph-fuse
capacity probe: PASS_AND_CLEANED, wrote and removed 25769803776 bytes
source/data transfer: local PR55 bundle + ShareGPT dataset copied and verified by sha256/file count
remote source network: no remote git clone/fetch/GitHub/source/dependency download was used on the GPU node
```

Structured preflight passed:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
SFT_ALLOWED_IF_PM_AUTHORIZED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=allowlisted preflight artifacts passed without actionable health signatures
```

SFT then failed before checkpoint creation:

```text
SFT start: 2026-05-21T15:08:24Z
run id: milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
EXIT_STATUS=1
END_UTC=2026-05-21T15:08:25Z
blocker line: environment: DEP_TARGET: unbound variable
```

The runtime evidence states this was a launch-wrapper environment bug:

```text
exact blocker: exported bash function referenced non-exported local variable DEP_TARGET
training progress: failed before GPU training
post-failure GPU sample: all 8 H200 at 0% util and 1 MiB memory
post-failure process scan: no torchrun/python3 -m llamafactory/llamafactory-cli/train_qwen3_8b_sft process
```

Stop/release proof:

```text
stop sent UTC: 2026-05-21T15:09:12Z
final LTP state: STOPPED (Completed)
completed: 2026-05-21 15:09:43
endpoint after stop: ssh -p 15535 root@10.100.22.28 refused connection at 2026-05-21T15:10:02Z
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
artifact preservation: outputs/logs/preflight/run metadata/checkpoint directory evidence preserved under /home/xu.yang/coding_agent_playground/outputs
```

## Eval Blocker

Mini-swe eval remains blocked.

Current absent model facts:

```text
checkpoint/model: absent
checkpoint files: none
trainer_state.json: absent
all_results.json: absent
served endpoint: absent; stopped LTP SSH endpoint refuses connection and was not an inference endpoint
eval-approved model id: absent
eval: not authorized and not run
```

Why mini-swe cannot run: mini-swe requires an eval-approved model target, either a live served endpoint/model id or a complete checkpoint/model with a serving handoff. PR55 cleared the preflight gate, but the one authorized SFT launch failed immediately on `DEP_TARGET` before checkpoint/model creation. There is no checkpoint, serving handoff, or inference endpoint to evaluate.

Current test_2 marker:

```text
BLOCKED_PR55_SFT_FAILED_NO_MODEL
```

## Accepted Future Model Forms

Accepted form A, served endpoint:

```text
OPENAI_BASE_URL or equivalent endpoint URL reachable from the corrected mini-swe runner
OPENAI_API_KEY or explicit no-auth instruction
MODEL_NAME or exact served model id
serving provenance: upstream task id, source checkpoint/model, serving command/config, endpoint health log
health check: endpoint responds to a minimal completion request before mini-swe
PM authorization: PM explicitly names this endpoint/model id as eval-approved
```

Accepted form B, complete checkpoint/model plus serving handoff:

```text
SFT_CHECKPOINT_PATH or MODEL_PATH exists and is complete
required model files: config/tokenizer files plus weights or adapter files required by the serving stack
trainer_state.json present, or PM documents an explicit replacement provenance record
all_results.json present, or PM documents an explicit replacement metrics record
serving handoff: exact serving command/config, resolved model id, port/base URL, logs, and health check
PM authorization: PM explicitly gates this checkpoint/model or resulting endpoint for eval
```

Rejected current forms:

```text
No checkpoint/model path.
No checkpoint files.
No trainer_state.json.
No all_results.json.
No served endpoint/model id.
The stopped LTP SSH endpoint is not an inference endpoint.
```

## Future Eval Storage Paths

All future mini-swe generated logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates must remain under `/home/xu.yang`.

Planned eval root for the PR55 runtime lineage:

```text
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2
LOG_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/logs
PREDICTIONS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/predictions
RESULTS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/results
METRICS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/metrics
RUN_METADATA_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/run_metadata
INTERMEDIATES_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/intermediates
TMPDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/tmp
HF_HOME=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/cache/hf_home
HF_DATASETS_CACHE=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/cache/hf_datasets
UV_CACHE_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/cache/uv
APPTAINER_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/cache/apptainer
SINGULARITY_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/cache/singularity
```

Expected output files after a future authorized smoke:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/predictions/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/results/results.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/metrics/metrics.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/run_metadata/run_metadata.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2/logs/mini_swe_smoke.log
```

Existing required-path exceptions to the `/home/xu.yang` rule:

```text
/root/workspace/swe-bench-related/mini-swe-agent
  justification: required mini-swe source checkout on the corrected final workspace.

/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
  justification: required existing SWE-bench/mini-swe config path on the corrected final workspace.
```

## Future Smoke Command Template

Do not run this command until PM explicitly gates a checkpoint/model or served endpoint.

```bash
ssh -p 31787 root@10.100.194.40 '
  set -euo pipefail
  export EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr55_eval_test2
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

## Exact Unblock Condition

PM may unblock test_2 mini-swe execution only when all of the following are true:

1. A future runtime or PM-approved replacement evidence names a complete checkpoint/model path or a live served endpoint/model id.
2. For checkpoint/model form, required config/tokenizer/weight or adapter files are complete, and `trainer_state.json` plus `all_results.json` are present or explicitly replaced by PM-approved provenance/metrics records.
3. For served endpoint form, the endpoint/base URL is reachable, the exact model id is provided, auth requirements are known, and a minimal completion health check passes.
4. PM explicitly states that the named checkpoint/model or endpoint is eval-approved for mini-swe.
5. All generated eval logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates are written under `/home/xu.yang`; any non-`/home/xu.yang` input paths are recorded with justification.

Until then, mini-swe remains blocked and no eval/GPU/SFT/dry-run should be run by test_2.
