# Test 2 S23 PR57 MCore Mini-SWE Eval Blocked Evidence

Task ID: `M1-S23-PR57-MCORE-EVAL-REBLOCK-TEST2`

Owner: `intern_code_test_2`

Updated: 2026-05-21T16:10:45Z

Scope: refresh mini-swe eval blocked evidence after PR57 SFT failed before checkpoint on the MCore/MCA dependency path. No eval, GPU, SFT, dry-run, remote transfer, or remote command was run by test_2.

## Source Evidence Read

- `evidence/dev_2_s23_pr57_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr57_preflight_sft_tracking.md`

Upstream runtime task: `M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2`, owner `intern_code_dev_2`.

## Upstream Runtime Facts

Final upstream status:

```text
BLOCKED_PR57_RUNTIME_MISSING_MCORE_ADAPTER_STOPPED_NO_CHECKPOINT
```

Runtime provenance:

```text
authorized commit: b4ac31ef1e3772953108348bf099818326ed65cc
PR #57 merge commit: c450429c2e3369adc723d132396399cd17dba684
PR #58 merge commit: b4ac31ef1e3772953108348bf099818326ed65cc
source bundle sha256: 1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa
source file count: 122
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Remote GPU/LTP node was treated as no-external-network for project code/dependency staging:

```text
no remote git clone
no remote git fetch
no GitHub/source fetch
no project/dependency download on the remote node
source/config/scripts/data prepared locally or from provided local workspaces
transfer command recorded by dev_2 as scp to root@10.100.22.31:/root/workspace/
post-transfer verification: bundle sha256 OK, critical file checksums OK, remote file count 122, dataset sha256 OK
```

Resource/storage/preflight facts:

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
endpoint during run: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
/mnt/cephfs mount: fuse.ceph-fuse
output root: /home/xu.yang/coding_agent_playground/outputs
capacity probe: PASS_AND_CLEANED, actual bytes 25769803776
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
```

Exactly one SFT attempt was run by dev_2 because preflight passed:

```text
remote launch script: /root/workspace/launch_pr57_sft.sh
tmux session: pr57_sft_FIXED_SETUP
start: 2026-05-21T16:03:06Z
run id: milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
checkpoint/output dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/config/qwen3_8b_sft.yaml
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/run_manifest.json
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_stdout_stderr.log
xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_xtrace.log
EXIT_STATUS=1
END_UTC=2026-05-21T16:03:28Z
```

Exact SFT blocker:

```text
ImportError: mcore_adapter is required when USE_MCA=1. Please install `mcore_adapter` and its dependencies.
torch.distributed.elastic.multiprocessing.errors.ChildFailedError
/root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py FAILED
local_rank: 7 exitcode 1
```

The launcher initialized distributed workers before failing on import:

```text
Initializing 8 distributed tasks at: 127.0.0.1:47509
```

Artifact status from dev_2 evidence:

```text
process scan: no torchrun, llamafactory, launcher.py, train_qwen3_8b, or python training process
gpu sample: all 8 NVIDIA H200 GPUs 0% util, 1 MiB used
checkpoint files: none
trainer_state.json: absent
all_results.json: absent
checkpoint/model: absent
eval: not run
```

Stop/release proof:

```text
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
post-stop state: STOPPED (Completed)
completed: 2026-05-21 16:06:06
endpoint after stop: ssh -p 22662 root@10.100.22.31 refused connection
no-running-job proof: ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
outputs preserved: /home/xu.yang/coding_agent_playground/outputs
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

Why mini-swe cannot run: mini-swe requires an eval-approved model target, either a live served endpoint/model id or a complete checkpoint/model with a serving handoff. PR57 cleared transfer/storage/preflight and launched exactly one SFT attempt, but that SFT failed before checkpoint creation because `mcore_adapter` was missing while `USE_MCA=1`. There is no checkpoint, serving handoff, or inference endpoint to evaluate.

Current test_2 marker:

```text
BLOCKED_PR57_MCORE_NO_MODEL
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
source/runtime provenance: source commit, bundle checksum, file list, data checksum, transfer command, post-transfer verification, and no-remote-project-code/dependency-network proof
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

Planned eval root for this PR57 MCore runtime lineage:

```text
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2
LOG_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/logs
PREDICTIONS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/predictions
RESULTS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/results
METRICS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/metrics
RUN_METADATA_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/run_metadata
INTERMEDIATES_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/intermediates
TMPDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/tmp
HF_HOME=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/cache/hf_home
HF_DATASETS_CACHE=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/cache/hf_datasets
UV_CACHE_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/cache/uv
APPTAINER_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/cache/apptainer
SINGULARITY_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/cache/singularity
```

Expected mini-swe output files after a future authorized smoke:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/predictions/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/results/results.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/metrics/metrics.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/run_metadata/run_metadata.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2/logs/mini_swe_smoke.log
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
  export EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr57_mcore_eval_test2
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
2. The upstream evidence includes local/provided-workspace source packaging, exact commit/file list/checksums, transfer command, remote destination, post-transfer verification, and no-remote-project-code/dependency-network proof.
3. For checkpoint/model form, required config/tokenizer/weight or adapter files are complete, and `trainer_state.json` plus `all_results.json` are present or explicitly replaced by PM-approved provenance/metrics records.
4. For served endpoint form, the endpoint/base URL is reachable, the exact model id is provided, auth requirements are known, and a minimal completion health check passes.
5. PM explicitly states that the named checkpoint/model or endpoint is eval-approved for mini-swe.
6. All generated eval logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates are written under `/home/xu.yang`; any non-`/home/xu.yang` input paths are recorded with justification.

Until then, mini-swe remains blocked and no eval/GPU/SFT/dry-run should be run by test_2.
