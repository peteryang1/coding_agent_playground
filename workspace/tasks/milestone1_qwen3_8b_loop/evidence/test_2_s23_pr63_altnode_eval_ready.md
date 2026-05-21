# Test 2 S23 PR63 Alternate-Node Mini-SWE Eval Ready Blocked Package

Task ID: `M1-S23-PR63-ALTNODE-EVAL-READY-TEST2`

Owner: `intern_code_test_2`

Updated: 2026-05-21T18:53:22Z

Scope: prepare mini-swe eval smoke handoff package while dev_2 owns the PR63 alternate-node runtime. No eval, GPU, SFT, dry-run, remote transfer, or remote command was run by test_2.

## Source Evidence Read

- `evidence/dev_2_s23_pr63_altnode_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr63_altnode_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

Upstream runtime task: `M1-S23-PR63-ALTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`, owner `intern_code_dev_2`.

## Current Dev_2 Result State

The current alternate-node runtime evidence is not yet a model handoff.

```text
authorization file: evidence/pm_s23_pr63_altnode_preflight_sft_authorization.md
runtime source commit: 7ad24ae328a350c0be596f41ea143affb4034486
authorized owner: intern_code_dev_2
authorized allocation count: exactly one fresh bounded alternate-node attempt
forbidden nodes: lg-cmc-b7r202-k07u06-h200-000580, lg-cmc-b7r202-q04u06-h200-000725
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download on GPU node
output root: /home/xu.yang/coding_agent_playground/outputs
SFT condition: run SFT only if PREFLIGHT_RESULT=PASS and SFT_ALLOWED=true
eval: not authorized
```

Current dev_2 state from durable evidence:

```text
dev_2 runtime status: LOCAL_PACKAGE_READY_PRE_SUBMIT
gpu tracking state: source/data/mcore local package ready; LTP submit pending
placement decision: pending
CephFS/output root: pending if node is non-forbidden
capacity probe: pending if node is non-forbidden
transfer verification: pending if node is non-forbidden
mcore_adapter import check: pending if node is non-forbidden
structured preflight: pending if node is non-forbidden
conditional SFT: pending; may run only if non-forbidden node, transfer/import/preflight PASS, and SFT_ALLOWED=true
```

Reusable package provenance from dev_2:

```text
source bundle sha256: 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
source file count: 139
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
mcore_adapter file count: 222
LLamaFactory bundle sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
python dependency bundle sha256: e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
flash_attn wheel sha256: c3941d81dd09fd1b39dc3df75097d8aa491250a551c919cd2e3c5df0a514fe0d
```

Current eval handoff status:

```text
checkpoint/model: not present in current alternate-node evidence
trainer_state.json: not present in current alternate-node evidence
all_results.json: not present in current alternate-node evidence
served endpoint/model id: not present in current alternate-node evidence
PM eval gate: absent
eval authorization: absent
```

Current test_2 marker:

```text
READY_BLOCKED_PENDING_PR63_ALTNODE_RESULT
```

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
source/runtime provenance: source commit, bundle checksum, file list, data checksum, mcore_adapter checksum, dependency checksums, transfer command, post-transfer verification, and no-remote-project-code/dependency-network proof
serving handoff: exact serving command/config, resolved model id, port/base URL, logs, and health check
PM authorization: PM explicitly gates this checkpoint/model or resulting endpoint for eval
```

Rejected current forms:

```text
No checkpoint/model path is present in current alternate-node evidence.
No checkpoint files are present in current alternate-node evidence.
No trainer_state.json is present in current alternate-node evidence.
No all_results.json is present in current alternate-node evidence.
No served endpoint/model id is present in current alternate-node evidence.
Eval remains unauthorized.
```

## Eval Paths

All future mini-swe generated logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates must remain under `/home/xu.yang`.

```text
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2
LOG_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/logs
PREDICTIONS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/predictions
RESULTS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/results
METRICS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/metrics
RUN_METADATA_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/run_metadata
INTERMEDIATES_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/intermediates
TMPDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/tmp
HF_HOME=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/cache/hf_home
HF_DATASETS_CACHE=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/cache/hf_datasets
UV_CACHE_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/cache/uv
APPTAINER_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/cache/apptainer
SINGULARITY_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/cache/singularity
```

Expected output files after a future PM-authorized smoke:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/predictions/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/results/results.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/metrics/metrics.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/run_metadata/run_metadata.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2/logs/mini_swe_smoke.log
```

Existing required-path exceptions:

```text
/root/workspace/swe-bench-related/mini-swe-agent
  justification: required mini-swe source checkout on the corrected final workspace.

/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
  justification: required existing SWE-bench/mini-swe config path on the corrected final workspace.
```

## Command Template

Do not run this command until PM explicitly gates a checkpoint/model or served endpoint for eval.

```bash
ssh -p 31787 root@10.100.194.40 '
  set -euo pipefail
  export EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr63_altnode_eval_test2
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

## Exact Unblock Condition From Dev_2 Result

Current dev_2 alternate-node result does not yet provide a model target; it is still pre-submit/pending in durable evidence.

PM may unblock test_2 mini-swe execution only when all of the following are true:

1. Dev_2 updates `evidence/dev_2_s23_pr63_altnode_preflight_sft_runtime.md` and `evidence/gpu_s23_pr63_altnode_tracking.md` with a final result naming a complete checkpoint/model path or a live served endpoint/model id.
2. The upstream final result includes local/provided-workspace source packaging, exact commit/file list/checksums, transfer command, remote destination, post-transfer verification, and no-remote-project-code/dependency-network proof.
3. If the final model form is a checkpoint/model, required config/tokenizer/weight or adapter files are complete, and `trainer_state.json` plus `all_results.json` are present or explicitly replaced by PM-approved provenance/metrics records.
4. If the final model form is a served endpoint, endpoint/base URL is reachable, exact model id is provided, auth requirements are known, and a minimal completion health check passes.
5. PM explicitly states that the named checkpoint/model or endpoint is eval-approved for mini-swe.
6. Eval authorization is explicitly granted by PM after the model/endpoint is named.
7. All generated eval logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates are written under `/home/xu.yang`; any non-`/home/xu.yang` input paths are recorded with justification.

Until then, mini-swe remains blocked-ready and unauthorized; no eval/GPU/SFT/remote commands should be run by test_2.
