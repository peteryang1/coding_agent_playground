# Test 2 S23 PR59 Mini-SWE Eval Blocked Evidence

Task ID: `M1-S23-PR59-EVAL-REBLOCK-TEST2`

Owner: `intern_code_test_2`

Updated: 2026-05-21T16:59:51Z

Scope: refresh mini-swe eval blocked evidence after PR59 runtime produced no checkpoint/model. No eval, GPU, SFT, dry-run, remote transfer, or remote command was run by test_2.

## Source Evidence Read

- `evidence/dev_2_s23_pr59_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr59_preflight_sft_tracking.md`

Upstream runtime task: `M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2`, owner `intern_code_dev_2`.

## Upstream Runtime Facts

Final upstream result:

```text
BLOCKED_WITH_FINAL_RUNTIME_EVIDENCE_STOPPED_NO_ACTIVE_GPU
final blocker: BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING
```

Preparation and transfer facts:

```text
PR #59 merge commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
source file list count: 131
source bundle sha256: 2f272f210b67ed45b4a7b05592881c8c036fb34de2660645d6f96af76adf4d85
mcore_adapter file count: 222 local, 217 remote
mcore_adapter bundle sha256: ec0ace00eeca1f4d60710deea59621c868860e34827a5b645122f64f043170e7
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote transfer: scp to root@10.100.22.28:/root/workspace/
post-transfer verification: source bundle OK, mcore_adapter bundle OK, dataset OK, critical source checksums OK, mcore_adapter file checksums OK
remote network rule: no remote git clone/fetch/GitHub/source/dependency download/pip download
```

Runtime and preflight facts:

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
endpoint during run: ssh -p 27043 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
output root: /home/xu.yang/coding_agent_playground/outputs
capacity probe: PASS_AND_CLEANED, 25769803776 bytes
mcore_adapter import check: PASS
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

Exactly one SFT attempt ran and failed before checkpoint/model creation:

```text
run id: milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/config/qwen3_8b_sft.yaml
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z/run_manifest.json
EXIT_STATUS=127
END_UTC=2026-05-21T16:51:05Z
failure signature: scripts/train_qwen3_8b_sft.sh: line 244: python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py: No such file or directory
diagnostic reason: DIAGNOSTIC_REASON=ERR_TRAP
root cause: LLAMAFACTORY_CLI was set to a space-containing command string but executed as a single command path
```

Absent eval handoff artifacts:

```text
checkpoint/model: absent
checkpoint files: none recorded
trainer_state.json: absent
all_results.json: absent
served endpoint: absent; stopped LTP SSH endpoint refuses connection and was not an inference endpoint
eval-approved model id: absent
eval: not run, not authorized
```

Stop/release proof:

```text
post-stop state: STOPPED (Completed)
completed: 2026-05-21 16:52:02
endpoint proof: ssh -p 27043 root@10.100.22.28 refused connection
running coding-agent-playground jobs: No jobs found.
outputs preserved: /home/xu.yang/coding_agent_playground/outputs
active Milestone GPU held by dev_2: no
```

## Eval Blocker

Mini-swe eval remains blocked.

Why mini-swe cannot run: mini-swe requires an eval-approved model target, either a live served endpoint/model id or a complete checkpoint/model with a serving handoff. PR59 cleared transfer/import/preflight and launched exactly one SFT attempt, but that SFT failed before checkpoint/model creation due the `LLAMAFACTORY_CLI` command-string launcher blocker. There is no checkpoint, serving handoff, or inference endpoint to evaluate.

Current test_2 marker:

```text
BLOCKED_PR59_NO_MODEL
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
source/runtime provenance: source commit, bundle checksum, file list, data checksum, mcore_adapter checksum, transfer command, post-transfer verification, and no-remote-project-code/dependency-network proof
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

## Future Eval Paths

All future mini-swe generated logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates must remain under `/home/xu.yang`.

```text
EVAL_ROOT=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2
LOG_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/logs
PREDICTIONS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/predictions
RESULTS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/results
METRICS_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/metrics
RUN_METADATA_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/run_metadata
INTERMEDIATES_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/intermediates
TMPDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/tmp
HF_HOME=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/hf_home
HF_DATASETS_CACHE=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/hf_datasets
UV_CACHE_DIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/uv
APPTAINER_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/apptainer
SINGULARITY_CACHEDIR=/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/cache/singularity
```

Expected output files after a future authorized smoke:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/predictions/preds.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/results/results.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/metrics/metrics.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/run_metadata/run_metadata.json
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s23_pr59_eval_test2/logs/mini_swe_smoke.log
```

Existing required-path exceptions:

```text
/root/workspace/swe-bench-related/mini-swe-agent
  justification: required mini-swe source checkout on the corrected final workspace.

/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
  justification: required existing SWE-bench/mini-swe config path on the corrected final workspace.
```

## Exact Unblock Condition

PM may unblock test_2 mini-swe execution only when all of the following are true:

1. A future runtime or PM-approved replacement evidence names a complete checkpoint/model path or a live served endpoint/model id.
2. The upstream evidence includes local/provided-workspace source packaging, exact commit/file list/checksums, transfer command, remote destination, post-transfer verification, and no-remote-project-code/dependency-network proof.
3. For checkpoint/model form, required config/tokenizer/weight or adapter files are complete, and `trainer_state.json` plus `all_results.json` are present or explicitly replaced by PM-approved provenance/metrics records.
4. For served endpoint form, endpoint/base URL is reachable, exact model id is provided, auth requirements are known, and a minimal completion health check passes.
5. PM explicitly states that the named checkpoint/model or endpoint is eval-approved for mini-swe.
6. All generated eval logs, predictions, results, metrics, run metadata, caches, temporary datasets, and intermediates are written under `/home/xu.yang`; any non-`/home/xu.yang` input paths are recorded with justification.

Until then, mini-swe remains blocked and no eval/GPU/SFT/remote commands should be run by test_2.
