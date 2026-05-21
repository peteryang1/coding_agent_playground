# Test 2 S23 Ceph-Fuse Runtime Mini-SWE Eval Blocked Evidence

Task ID: `M1-S23-CEPHFUSE-EVAL-REBLOCK-TEST2`

Owner: `intern_code_test_2`

Updated: 2026-05-21T13:55:28Z

Scope: refresh mini-swe eval blocked evidence after the ceph-fuse fixed preflight runtime failed before SFT. No eval, GPU, SFT, or dry-run was run by test_2.

## Source Evidence Read

- `evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md`
- `evidence/gpu_s23_cephfuse_preflight_sft_tracking.md`

Upstream runtime task: `M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2`, owner `intern_code_dev_2`.

## Upstream Runtime Facts

Final upstream status:

```text
BLOCKED_PREFLIGHT_HEALTH_SIGNATURE_STOPPED_NO_SFT
```

The ceph-fuse bootstrap blocker from the prior parser-patch attempt was fixed for this runtime:

```text
command -v ceph-fuse: /usr/bin/ceph-fuse
/mnt/cephfs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
/home/xu.yang/coding_agent_playground/outputs findmnt: SOURCE ceph-fuse, FSTYPE fuse.ceph-fuse
capacity probe: PASS_AND_CLEANED
source/data transfer: verified by sha256/file count
```

The runtime then failed at structured preflight before SFT:

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
exact blocker: BLOCKED_PREFLIGHT_HEALTH_SIGNATURE
```

Representative upstream health records cited by dev_2:

```text
dmesg_gpu_fault_scan.txt line 446: SXid 20009, "Non-fatal, Link 57 RX Short Error Rate"
dmesg_gpu_fault_scan.txt line 447: SXid 20009 severity record for Engine instance 57
dmesg_gpu_fault_scan.txt line 448: SXid 20009 data payload record
torch_nccl_allreduce.log lines 5-22: NCCL_ASYNC_ERROR_HANDLING warnings classified by the current parser as nccl_or_collective_failure
```

Runtime stop/release facts:

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
node: lg-cmc-b7r202-q03u26-h200-000730
endpoint during run: ssh -p 38862 root@10.100.22.36
final state: STOPPED (Completed)
completed: 2026-05-21 13:39:48
endpoint after stop: ssh connect refused
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
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
served endpoint: absent; stopped runtime endpoint refuses connection
eval-approved model id: absent
```

Why mini-swe cannot run: mini-swe requires an eval-approved model target, either a live served endpoint/model id or a complete checkpoint/model with a serving handoff. The ceph-fuse fixed runtime produced neither because SFT was correctly skipped after preflight failed. Running mini-swe now would only validate the absence of a target, not Qwen3-8B post-SFT behavior.

Current test_2 marker:

```text
BLOCKED_PREFLIGHT_FAILED_NO_MODEL
```

## Accepted Future Model Forms

Accepted form A, served endpoint:

```text
OPENAI_BASE_URL or equivalent endpoint URL reachable from the mini-swe runner
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

Rejected current form:

```text
No checkpoint/model path.
No served endpoint/model id.
The stopped LTP SSH endpoint is not an inference endpoint.
```

## Future Eval Storage Paths

All future mini-swe generated logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates must remain under `/home/xu.yang`.

Planned eval root for this runtime lineage:

```text
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2
LOG_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/logs
PREDICTIONS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/predictions
RESULTS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/results
METRICS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/metrics
RUN_METADATA_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/run_metadata
INTERMEDIATES_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/intermediates
TMPDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/tmp
HF_HOME=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/cache/hf_home
HF_DATASETS_CACHE=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/cache/hf_datasets
UV_CACHE_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/cache/uv
APPTAINER_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/cache/apptainer
SINGULARITY_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/cache/singularity
```

Expected output files after a future authorized smoke:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/predictions/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/results/results.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/metrics/metrics.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/run_metadata/run_metadata.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2/logs/mini_swe_smoke.log
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
  export EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_cephfuse_runtime_eval_test2
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
