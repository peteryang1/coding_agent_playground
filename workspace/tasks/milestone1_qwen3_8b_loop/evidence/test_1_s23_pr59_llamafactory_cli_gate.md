# Test 1 S23 PR59 LLamaFactory CLI Gate

Task ID: `M1-S23-PR59-LLAMAFACTORY-CLI-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Fix owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_pr59_llamafactory_cli_gate.md`
Status timestamp: `2026-05-21T17:05:33Z`

## Result

`PASS_FOR_PM_RETRY`

No LTP, GPU, preflight, SFT, eval, dry-run, transfer command, remote command, parser execution, or PR code execution was run by `intern_code_test_1`.

The final PR59 runtime cleared transfer, `mcore_adapter` import, and preflight gates, then failed before checkpoint/training because `LLAMAFACTORY_CLI` was set to a space-containing command string and the launcher executed it as a single quoted path. PR #61 now provides a no-execution launcher fix package that addresses this specific blocker while preserving prior transfer, import, storage, diagnostics, and no-remote-download gates.

## Inputs Reviewed

- `evidence/pm_s23_pr59_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr59_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr59_preflight_sft_tracking.md`
- `evidence/dev_4_s23_pr59_llamafactory_cli_fix.md`
- `task_registry.md`

PR metadata observed by `intern_code_test_1`:

```text
PR: https://github.com/peteryang1/coding_agent_playground/pull/61
state: OPEN
draft: false
mergeable: MERGEABLE
base: main
head branch: intern_code_dev_4/M1-S23-PR59-LLAMAFACTORY-CLI-FIX-DEV4
latest head: d4f3340d1f7b32d91553cbe18d7effce533276c7
functional commit: 59524d9a905b07e4940ec17de277d862dcd99900
files changed: scripts/train_qwen3_8b_sft.sh; tests/test_train_qwen3_8b_sft_static.py; dev_4 status/task/evidence/history/knowledge/task_registry docs
```

## Runtime Gate Findings

### Authorization / Scope

PASS.

PM authorized exactly one owner-executed runtime:

```text
task: M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2
owner: intern_code_dev_2
PR59 merge commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
authorization status: AUTHORIZED_EXACTLY_ONCE
eval authorized: false
```

test_1 did not run any runtime command.

### Transfer / Import / Storage

PASS.

dev_2 evidence records:

```text
source commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
source file count: 131
source bundle sha256: 2f272f210b67ed45b4a7b05592881c8c036fb34de2660645d6f96af76adf4d85
mcore_adapter bundle sha256: ec0ace00eeca1f4d60710deea59621c868860e34827a5b645122f64f043170e7
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
transfer command: scp to root@10.100.22.28:/root/workspace/
post-transfer verification: source bundle OK, mcore bundle OK, dataset OK, critical source checksums OK, mcore file checksums OK
remote project/dependency network: no remote git clone/fetch/GitHub/source/dependency download/pip download
MCORE_ADAPTER_DIR: /root/workspace/coding_agent_playground/code/mcore_adapter
mcore_adapter import check: PASS
output root: /home/xu.yang/coding_agent_playground/outputs
capacity probe: PASS_AND_CLEANED, 25769803776 bytes
```

### Structured Preflight

PASS.

Durable structured result:

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
```

SFT was allowed because transfer/import/preflight gates passed.

### SFT Runtime Blocker

BLOCKED.

Run metadata:

```text
run id: milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr59_sft_20260521T163413Z
runtime config sha256: 0425900e30a5e043cb8447850d9e35cef1ed340a1ff76b040bebf82cddb02353
run manifest sha256: 57cd77b1b58702f4b57415c7c8d3f63a98fdb5efd2e535d83a707323b2c0d932
```

Final failure:

```text
EXIT_STATUS=127
END_UTC=2026-05-21T16:51:05Z
failure signature: scripts/train_qwen3_8b_sft.sh: line 244: python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py: No such file or directory
diagnostic reason: DIAGNOSTIC_REASON=ERR_TRAP
error line: ERROR_LINE=244
```

Classification:

```text
final blocker: BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING
root cause: LLAMAFACTORY_CLI was set to the space-containing command string `python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`, but scripts/train_qwen3_8b_sft.sh executes `"${LLAMAFACTORY_CLI}" train ...` as a single command path.
```

### Checkpoint / Eval State

PASS for expected absence under blocker; eval remains blocked.

```text
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
post-failure train processes: none observed
post-failure GPU state: idle
```

No checkpoint/model exists for mini-swe handoff.

### Stop / No-Running-Job Proof

PASS.

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
endpoint: ssh -p 27043 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
final LTP state: STOPPED (Completed)
completed: 2026-05-21 16:52:02
endpoint proof: ssh refused connection
running coding-agent-playground jobs: No jobs found.
```

## dev_4 Fix Gate

PASS.

Reviewed fix package:

```text
evidence/dev_4_s23_pr59_llamafactory_cli_fix.md
PR #61 latest head d4f3340d1f7b32d91553cbe18d7effce533276c7
```

Gate findings:

```text
root cause explained: PASS
command-plus-args support: PASS
single quoted path removed: PASS
DEP_TARGET/LF/MCORE_ADAPTER_DIR exports preserved: PASS
PYTHONPATH_PREFIX/mcore import gate preserved: PASS
manifest/log rendered command preserved with shell-readable quoting: PASS
no remote source/dependency download rule preserved: PASS
/home/xu.yang/coding_agent_playground/outputs default preserved: PASS
static evidence present: PASS
dev_4 no LTP/GPU/preflight/SFT/eval/dry-run statement: PASS
```

Source-level evidence from PR #61 diff:

```text
scripts/train_qwen3_8b_sft.sh adds read_llamafactory_command:
  read -r -a LLAMAFACTORY_CMD <<< "${LLAMAFACTORY_CLI}"
  empty command exits 6

scripts/train_qwen3_8b_sft.sh changes final invocation from:
  "${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"
to:
  "${LLAMAFACTORY_CMD[@]}" train "${RUNTIME_CONFIG}"

manifest/log command now uses:
  $(format_llamafactory_command_for_log) train ${RUNTIME_CONFIG}
```

Static test evidence recorded by dev_4:

```text
bash -n scripts/train_qwen3_8b_sft.sh: exit 0
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 4 passed in 0.01s
```

`intern_code_test_1` did not execute those commands; this gate only reviewed durable evidence and PR diff.

## Future Retry Acceptance

Before PM can authorize another runtime:

1. PR #61 must be PM-gated/merged or PM must otherwise name an exact accepted source commit/package.
2. Fresh PM authorization must name owner, source commit/package, allocation count, and runtime scope.
3. Runtime repeats local/provided source/data/mcore packaging, transfer, and post-transfer verification.
4. Runtime preserves no remote source/dependency downloads.
5. Runtime proves `MCORE_ADAPTER_DIR` and `mcore_adapter import OK for USE_MCA=1`.
6. Structured preflight is `PASS` with `SFT_ALLOWED=true`.
7. SFT logs/manifest show `LLAMAFACTORY_CMD` or equivalent command rendering and no `LLAMAFACTORY_CLI` command-string single-path blocker.
8. Eval handoff requires complete checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM-approved replacements, plus stop proof.

## Completion Marker

```yaml
task_id: M1-S23-PR59-LLAMAFACTORY-CLI-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
runtime_blocker: BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING
pr: 61
pr_state: open_non_draft_mergeable_clean
pr_latest_head: d4f3340d1f7b32d91553cbe18d7effce533276c7
functional_commit: 59524d9a905b07e4940ec17de277d862dcd99900
transfer_import_preflight_passed: true
dev4_fix_package_present: true
llamafactory_cli_fix_gate: PASS
checkpoint_model_present: false
trainer_state_json_present: false
all_results_json_present: false
eval_handoff: BLOCKED_NO_MODEL
stop_proof_complete: true
fresh_pm_authorization_required: true
no_ltp_gpu_preflight_sft_eval_by_test1: true
```
