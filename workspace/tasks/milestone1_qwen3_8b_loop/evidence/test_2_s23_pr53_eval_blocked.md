# Test 2 S23 PR53 Mini-SWE Eval Blocked Evidence

Task ID: `M1-S23-PR53-EVAL-REBLOCK-TEST2`

Owner: `intern_code_test_2`

Updated: 2026-05-21T14:37:29Z

Scope: refresh mini-swe eval blocked evidence after PR53 placement-probe preflight failed before SFT. No eval, GPU, SFT, or dry-run was run by test_2.

## Source Evidence Read

- `evidence/dev_2_s23_pr53_placementprobe_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr53_placementprobe_preflight_sft_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

Upstream runtime task: `M1-S23-PR53-PLACEMENTPROBE-PREFLIGHT-SFT-RUNTIME-DEV2`, owner `intern_code_dev_2`.

## Upstream Runtime Facts

Final upstream status:

```text
BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT
```

PR53/runtime provenance:

```text
PR #53 merge commit: e29c93736be3384663cad953cd18da68c30070fb
source bundle sha256: 34c5655cc8d7003ef3855b7ef5d285311794ab2fcad435dc4d52a3c80c10de77
source file list count: 111
parser checksum scripts/parse_s22_preflight_health.py: b90ead39614dd127e9a27de3433a648acbf37bcd9f008637bfb43ccb5aad9a69
ShareGPT data sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Placement/storage/transfer status:

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
endpoint during run: ssh -p 30073 root@10.100.24.12
assigned node: lg-cmc-b7r401-a05u06-h200-000770
forbidden-node gate: PASS_NON_FORBIDDEN
ceph-fuse proof: /usr/bin/ceph-fuse; /mnt/cephfs FSTYPE fuse.ceph-fuse
/home/xu.yang output proof: /home/xu.yang/coding_agent_playground/outputs resolved on fuse.ceph-fuse
capacity proof: 24 GiB real-write probe PASS_AND_CLEANED
source/data transfer: local PR #53 bundle + dataset copied and verified by sha256/file count
remote source network: no remote git clone/fetch/GitHub/source/dependency download was run
```

Structured preflight failed before SFT:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE
ACTIONABLE_FAULT=true
SFT_ALLOWED=false
SFT_ALLOWED_IF_PM_AUTHORIZED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
exact blocker: BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE
```

The runtime evidence states PR53 still classified NCCL async deprecation warnings as actionable:

```text
fault_count: 8
representative match: torch_nccl_allreduce.log line 5, "Warning: Environment variable NCCL_ASYNC_ERROR_HANDLING is deprecated; use TORCH_NCCL_ASYNC_ERROR_HANDLING instead"
TORCHRUN_EXIT=0
ALLREDUCE_OK world_size=8 value=36.0
```

Stop/release proof:

```text
stop timestamp UTC: 2026-05-21T14:30:11Z
post-stop state: STOPPED (Completed)
completed: 2026-05-21 14:30:42
endpoint after stop: ssh -p 30073 root@10.100.24.12 refused connection
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
artifact preservation: generated artifacts remain under /home/xu.yang/coding_agent_playground/outputs on CephFS
```

## Eval Blocker

Mini-swe eval remains blocked.

Current absent model facts:

```text
SFT command: not run
reason SFT not run: structured preflight FAIL_HEALTH_SIGNATURE and sft_allowed=false
checkpoint/model: absent; SFT was not run
trainer_state.json: absent; SFT was not run
all_results.json: absent; SFT was not run
served endpoint: absent; stopped LTP SSH endpoint refuses connection and was not an inference endpoint
eval-approved model id: absent
eval: not authorized and not run
```

Why mini-swe cannot run: mini-swe requires an eval-approved model target, either a live served endpoint/model id or a complete checkpoint/model with a serving handoff. PR53 preflight failed before SFT, so no checkpoint, model, serving handoff, or inference endpoint exists. Running mini-swe now would test only the missing target state, not Qwen3-8B post-SFT behavior.

Current test_2 marker:

```text
BLOCKED_PR53_PREFLIGHT_FAILED_NO_MODEL
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
No trainer_state.json.
No all_results.json.
No served endpoint/model id.
The stopped LTP SSH endpoint is not an inference endpoint.
```

## Future Eval Storage Paths

All future mini-swe generated logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates must remain under `/home/xu.yang`.

Planned eval root for the PR53 runtime lineage:

```text
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2
LOG_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/logs
PREDICTIONS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/predictions
RESULTS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/results
METRICS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/metrics
RUN_METADATA_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/run_metadata
INTERMEDIATES_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/intermediates
TMPDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/tmp
HF_HOME=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/cache/hf_home
HF_DATASETS_CACHE=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/cache/hf_datasets
UV_CACHE_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/cache/uv
APPTAINER_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/cache/apptainer
SINGULARITY_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/cache/singularity
```

Expected output files after a future authorized smoke:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/predictions/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/results/results.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/metrics/metrics.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/run_metadata/run_metadata.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2/logs/mini_swe_smoke.log
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
  export EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr53_eval_test2
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
