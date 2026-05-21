# Test 1 S23 PR61 MCA Model Path Gate

Task ID: `M1-S23-PR61-MCA-MODEL-PATH-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Future fix owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_pr61_mca_model_path_gate.md`
Status timestamp: `2026-05-21T17:59:51Z`

## Result

`PASS_FOR_PM_RETRY`

No LTP, GPU, preflight, SFT, eval, dry-run, transfer command, remote command, parser execution, or PR code execution was run by `intern_code_test_1`.

The PR61 runtime cleared transfer, `mcore_adapter` import, structured preflight, and the PR61 `LLAMAFACTORY_CLI` command-string fix. The single authorized SFT attempt reached LLamaFactory launcher code, then failed before checkpoint/training with `ValueError: Please provide model_name_or_path`. PR #63 now provides a no-execution launcher normalization package that addresses this specific MCA/direct-launcher argument binding blocker while preserving PR61 command-array parsing and prior transfer, import, storage, diagnostics, and no-remote-download gates. Latest-head refresh keeps `PASS_FOR_PM_RETRY`: the delta from previously gated head `a035692dc72b40434240d0308c36f4d071644849` to latest head `a0ab039278198a6c1b0cd40009038d89cd602922` is docs/status/evidence/task-registry only, with no functional changes under `scripts/`, `tests/`, or `configs/`.

## Inputs Reviewed

- `evidence/pm_s23_pr61_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr61_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr61_preflight_sft_tracking.md`
- `evidence/dev_1_s23_pr59_llamafactory_cli_review.md`
- `evidence/test_1_s23_pr59_llamafactory_cli_gate.md`
- PR #63 metadata and diff for `intern_code_dev_4/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4`
- PR #63 file `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr61_mca_model_path_fix.md`

PM worktree note:

- `/work-agents/intern_code_pm/.../evidence/dev_4_s23_pr61_mca_model_path_fix.md` was not materialized in the PM worktree at this check.
- The required evidence file is present in PR #63 diff and was reviewed there.

PR #63 metadata observed by `intern_code_test_1`:

```text
PR: https://github.com/peteryang1/coding_agent_playground/pull/63
state: OPEN
draft: false
mergeable: MERGEABLE
base: main
head branch: intern_code_dev_4/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4
latest head: a0ab039278198a6c1b0cd40009038d89cd602922
previously gated functional head: a035692dc72b40434240d0308c36f4d071644849
files changed: scripts/train_qwen3_8b_sft.sh; tests/test_train_qwen3_8b_sft_static.py; dev_4 status/task/evidence/history/knowledge/task_registry docs
```

Latest-head delta reviewed:

```text
range: a035692dc72b40434240d0308c36f4d071644849..a0ab039278198a6c1b0cd40009038d89cd602922
commit: a0ab039278198a6c1b0cd40009038d89cd602922 Record PR63 gate status for MCA model path fix
changed files: workspace/interns/intern_code_dev_4/status.md; task README/history/evidence/task_knowledge/task_registry docs
functional paths changed under scripts/tests/configs: none
decision impact: no functional change from prior gate; PASS_FOR_PM_RETRY remains valid
```

## Runtime Gate Findings

### Authorization / Scope

PASS.

```text
task: M1-S23-PR61-PREFLIGHT-SFT-RUNTIME-DEV2
authorization status: AUTHORIZED_EXACTLY_ONCE
authorized owner: intern_code_dev_2
PR61 merge commit: aa426b045b52b71bc23b4a2f73f3ee1c42187037
completion PR62 merge commit / origin main commit: 713862da983f73b165af1cfe27935ccef616a049
eval authorized: false
```

`intern_code_test_1` did not run any runtime command.

### Transfer / Import / Storage

PASS.

Durable dev_2 evidence records:

```text
source commit: 713862da983f73b165af1cfe27935ccef616a049
source file count: 135
source bundle sha256: a8aeb73d6f3c69775997b7c4b6cf49344a0e8691a44811b68d5678caaacb83c4
mcore_adapter source type: local/provided source tree
mcore_adapter file count: 222
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
transfer command: scp to root@10.100.22.31:/root/workspace/
post-transfer verification: source bundle OK, mcore bundle OK, dataset OK, dependency bundles OK, critical source checksums OK, mcore file checksums OK
remote project/dependency network: no remote git clone/fetch/GitHub/source/dependency download/pip download
MCORE_ADAPTER_DIR: /root/workspace/coding_agent_playground/code/mcore_adapter
mcore_adapter import check: PASS
output root: /home/xu.yang/coding_agent_playground/outputs
capacity probe: PASS_AND_CLEANED, 25769803776 bytes
```

### Structured Preflight

PASS.

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
SFT_ALLOWED_IF_PM_AUTHORIZED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=UNKNOWN
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=allowlisted preflight artifacts passed without actionable health signatures
```

SFT was allowed because transfer, `mcore_adapter` import, and structured preflight passed with `SFT_ALLOWED=true`.

### PR61 CLI Fix

PASS.

The runtime verifies the prior PR59 quoted single-path blocker did not recur:

```text
LLAMAFACTORY_CLI=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
LLAMAFACTORY_CMD=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
prior quoted single-path signature: not observed
launcher reached: yes, traceback originates in /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
```

This confirms the PR61 launcher fix is intact for this runtime gate.

### SFT Runtime Blocker

BLOCKED.

Run metadata:

```text
run id: milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
runtime config sha256: 4f22228204bab055c982d2c9046877b26146833be93ea5da0c59b582ee72b75a
run manifest sha256: 210633469ab3dbfed7546ec01d818957c1f73cae2b4ef1f8fd472cbd3c8e7f7c
```

Runtime config proof shows the intended field exists in generated YAML:

```text
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
preprocessing_num_workers: null
dataloader_num_workers: 0
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
save_steps: 2
save_total_limit: 1
max_steps: 2
```

Final failure:

```text
EXIT_STATUS=1
END_UTC=2026-05-21T17:31:39Z
failure signature: ValueError: Please provide `model_name_or_path`.
trace path: llamafactory/launcher.py -> train/tuner.py -> hparams/parser.py -> model_args.py
diagnostic reason: DIAGNOSTIC_REASON=ERR_TRAP
error line: ERROR_LINE=266
```

Classification:

```text
final blocker: BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE
root cause observed: generated runtime YAML contains model_name_or_path, but LLamaFactory MCA argument parsing still raised ValueError before training/checkpoint work.
distinct from prior blocker: PR61 CLI command-string fix worked because launcher.py was reached and LLAMAFACTORY_CMD was logged.
```

### Checkpoint / Eval State

PASS for expected absence under blocker; eval remains blocked.

```text
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
post-failure train processes: none observed except artifact-summary command itself
post-failure GPU state: all 8 H200 GPUs idle, 0% util, 1 MiB memory each
outputs preserved: yes, under /home/xu.yang/coding_agent_playground/outputs
```

No checkpoint/model exists for mini-swe/eval handoff.

### Stop / No-Running-Job Proof

PASS.

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
endpoint: ssh -p 33089 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
stop response: status 202, Execute job successfully
final LTP state: STOPPED (Completed)
completed: 2026-05-21 17:32:52
endpoint proof: ssh refused connection
running coding-agent-playground jobs: No jobs found.
active Milestone GPU held by dev_2: no
```

## dev_4 Fix Gate

PASS.

Reviewed fix package:

```text
PR #63 latest head a0ab039278198a6c1b0cd40009038d89cd602922
previously gated functional head a035692dc72b40434240d0308c36f4d071644849
PR file workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr61_mca_model_path_fix.md
```

Gate findings:

```text
root cause explained: PASS
direct launcher.py normalization covers model_name_or_path parse blocker: PASS
PR61 command-array parsing remains intact: PASS
LLAMAFACTORY_CMD_ORIGINAL / LLAMAFACTORY_CMD_NORMALIZATION / LLAMAFACTORY_CMD logging added: PASS
DEP_TARGET/LF/MCORE_ADAPTER_DIR exports preserved: PASS
PYTHONPATH_PREFIX/mcore import gate preserved: PASS
no remote source/dependency download rule preserved: PASS
/home/xu.yang/coding_agent_playground/outputs default preserved: PASS
static evidence present: PASS
dev_4 no LTP/GPU/preflight/SFT/eval/dry-run statement: PASS
```

Source-level evidence from PR #63 diff:

```text
scripts/train_qwen3_8b_sft.sh preserves:
  read -r -a LLAMAFACTORY_CMD <<< "${LLAMAFACTORY_CLI}"
  "${LLAMAFACTORY_CMD[@]}" train "${RUNTIME_CONFIG}"

scripts/train_qwen3_8b_sft.sh adds direct launcher normalization:
  if any command word matches */llamafactory/launcher.py, replace it with -m llamafactory.cli
  LLAMAFACTORY_CMD_NORMALIZATION=direct_launcher_py_to_module_cli

The intended PR61 command:
  python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py train <config>

is normalized before appending train/config to:
  python3 -m llamafactory.cli train <config>
```

Why this covers the observed blocker:

```text
dev_4 evidence explains direct launcher.py execution with "train config.yaml" made LLamaFactory's parser see sys.argv[1] == "train", so YAML was not loaded and model_name_or_path was missing.
The module CLI path routes through llamafactory.cli -> launcher.launch(), preserving the train subcommand handling so the torchrun child receives the YAML as the parser's first argument.
```

Static test evidence recorded by dev_4:

```text
bash -n scripts/train_qwen3_8b_sft.sh
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
result: 5 passed in 0.01s
```

`intern_code_test_1` did not execute those commands; this gate only reviewed durable/runtime evidence and PR #63 diff.

## Future Retry Acceptance

Before PM can authorize another runtime:

1. dev_4 MCA/model-path fix package or PR exists.
2. PR #63 must be PM-gated/merged or PM must otherwise name an exact accepted source commit/package.
3. Fresh PM authorization names owner, source commit/package, allocation count, and runtime scope.
4. Runtime repeats local/provided source/data/mcore packaging, transfer, and post-transfer verification.
5. Runtime preserves no remote source/dependency downloads.
6. Runtime proves `MCORE_ADAPTER_DIR` and `mcore_adapter import OK for USE_MCA=1`.
7. Runtime preserves PR61 `LLAMAFACTORY_CMD` behavior with no quoted single-path regression.
8. Runtime logs `LLAMAFACTORY_CMD_NORMALIZATION=direct_launcher_py_to_module_cli` or an equivalent accepted path when using direct `launcher.py`.
9. Structured preflight is `PASS` with `SFT_ALLOWED=true`.
10. SFT logs show no `model_name_or_path` parse/binding blocker and no regression to prior blockers.
11. Eval handoff requires complete checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM-approved replacements, plus stop proof.

## Completion Marker

```yaml
task_id: M1-S23-PR61-MCA-MODEL-PATH-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
runtime_blocker: BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE
pr: 63
pr_state: open_non_draft_mergeable_clean
pr_latest_head: a0ab039278198a6c1b0cd40009038d89cd602922
previously_gated_functional_head: a035692dc72b40434240d0308c36f4d071644849
latest_head_delta: docs_status_evidence_only
functional_paths_changed_since_prior_gate: false
transfer_import_preflight_passed: true
pr61_cli_fix_intact: true
direct_launcher_py_normalization_gate: PASS
checkpoint_model_present: false
trainer_state_json_present: false
all_results_json_present: false
eval_handoff: BLOCKED_NO_MODEL
stop_proof_complete: true
dev4_fix_package_present: true_in_pr63_diff_not_pm_worktree
fresh_pm_authorization_required: true
no_ltp_gpu_preflight_sft_eval_remote_by_test1: true
```
