# Test 1 S23 PR55 SFT Blocker Gate

Task ID: `M1-S23-PR55-SFT-BLOCKER-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Wrapper fix owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_pr55_sft_blocker_gate.md`
Status timestamp: `2026-05-21T15:37:40Z`

## Result

`PASS_FOR_PM_RETRY`

No LTP, GPU, preflight, SFT, eval, dry-run, parser execution, or remote runtime command was run by `intern_code_test_1`.

This is a no-execution gate result only. It does not authorize a new runtime by itself; any retry still requires fresh PM authorization naming owner, source commit/package, allocation count, and scope.

## Inputs Reviewed

Runtime evidence:

- `evidence/pm_s23_pr55_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr55_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr55_preflight_sft_tracking.md`

Wrapper fix evidence and PR:

- `evidence/dev_4_s23_pr55_sft_wrapper_fix.md`
- PR #57: `https://github.com/peteryang1/coding_agent_playground/pull/57`
- PM-named functional head: `0253ff99cb1bd595bc68bda5a7a4bf7d5983162c`
- GitHub PR state checked by test_1: open, non-draft, `MERGEABLE` / `CLEAN`
- Current fetched PR ref observed by test_1: `b94dd93c131b9a6472919c14ae71684d71683a60`
- Diff from `0253ff99cb1bd595bc68bda5a7a4bf7d5983162c` to `b94dd93c131b9a6472919c14ae71684d71683a60`: docs/status/evidence/task files only; no additional changes to `scripts/train_qwen3_8b_sft.sh` or `tests/test_train_qwen3_8b_sft_static.py`

## Prior Runtime Findings

The PR55 runtime gate findings remain accepted:

```text
source commit: PR #55 merge commit 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
endpoint: ssh -p 15535 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
forbidden-node check: PASS, node is not in the forbidden list
output root: /home/xu.yang/coding_agent_playground/outputs
capacity probe: PASS_AND_CLEANED, wrote and removed 25769803776 bytes
remote source/dependency network: none recorded on GPU node
local source/data/dependency transfer: PASS with checksums
structured preflight: PASS
SFT_ALLOWED: true
SFT attempt: exactly one
EXIT_STATUS: 1
blocker: environment: DEP_TARGET: unbound variable
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
stop proof: STOPPED (Completed), endpoint refused, no running coding-agent-playground job
```

The blocker occurred before GPU training/checkpoint. Its absence is required in the next retry logs.

## PR #57 Wrapper Fix Gate

PASS.

Reviewed functional commit `0253ff99cb1bd595bc68bda5a7a4bf7d5983162c` for:

```text
scripts/train_qwen3_8b_sft.sh
tests/test_train_qwen3_8b_sft_static.py
```

The patch covers the concrete runtime blocker:

```text
DEP_TARGET="${DEP_TARGET:-${PYTHON_DEPS_DIR:-${RUN_DIR}/python_deps}}"
LF="${LF:-${LLAMAFACTORY_DIR}}"
LLAMAFACTORY_CLI="${LLAMAFACTORY_CLI:-llamafactory-cli}"
export DEP_TARGET LF LLAMAFACTORY_CLI
export DEP_TARGET="${DEP_TARGET}"
export LF="${LF}"
"${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"
```

Gate findings:

- `DEP_TARGET` now has a stable default under `${RUN_DIR}/python_deps`, so the default generated dependency target remains under `/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/python_deps`.
- `DEP_TARGET`, `LF`, and `LLAMAFACTORY_CLI` are exported before logging, manifest generation, and training launch.
- The run log records `LLAMAFACTORY_CLI`, `DEP_TARGET`, and `LF`.
- The manifest launch command records explicit `DEP_TARGET` and `LF` values and uses the configurable `LLAMAFACTORY_CLI`.
- The final training invocation uses `"${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"`, allowing a runtime-provided local wrapper without hard-coding `llamafactory-cli`.
- The patch does not add remote `git clone`, `git fetch`, GitHub source fetch, dependency install, or dependency download behavior.
- The patch preserves `/home/xu.yang/coding_agent_playground/outputs` as the generated output/log/tmp/checkpoint/run-metadata/intermediate root.
- If a future runtime uses a chmod-capable wrapper staged under `/root/workspace`, it must remain executable-source staging only and must keep generated outputs under `/home/xu.yang/coding_agent_playground/outputs`.

## Static Test Evidence

dev_4 reports local-only static/test evidence:

```text
bash -n scripts/train_qwen3_8b_sft.sh: pass
python3 -m py_compile tests/test_train_qwen3_8b_sft_static.py: pass
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 2 passed in 0.01s
```

test_1 did not run these commands; test_1 only reviewed the durable evidence and source diff.

## No Checkpoint / Eval State

PASS for current state.

The prior runtime still has no accepted model output:

```text
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
served endpoint/model id: absent
eval artifact: absent
```

Eval handoff remains blocked until a future authorized runtime produces a complete checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM explicitly accepts a documented replacement.

## Future Retry Acceptance Criteria

Before PM can authorize another runtime:

1. PR #57 or an equivalent accepted package is the named source for the retry.
2. PM authorization names owner, commit/package, allocation count, and scope.
3. Runtime uses a non-forbidden node and records node/job/endpoint/stop proof.
4. Generated outputs, logs, checkpoints, run metadata, temporary converted datasets, and intermediates use `/home/xu.yang/coding_agent_playground/outputs`.
5. Any non-`/home/xu.yang` path is either existing-required input path or explicitly justified executable/source staging.
6. Source, ShareGPT data, and dependency bundle transfer are local/provided and checksum-verified.
7. No remote GitHub/source/dependency network command runs on the GPU node.
8. Structured preflight must be `PASS` with `sft_allowed=true` before SFT starts.
9. SFT logs must show no `DEP_TARGET: unbound variable` and no regression to prior blockers.
10. PASS for eval handoff requires checkpoint/model plus `trainer_state.json` and `all_results.json`, or an accepted replacement, plus stop proof.

## Completion Marker

```yaml
task_id: M1-S23-PR55-SFT-BLOCKER-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
pr: 57
pm_named_functional_head: 0253ff99cb1bd595bc68bda5a7a4bf7d5983162c
observed_fetched_pr_ref: b94dd93c131b9a6472919c14ae71684d71683a60
dep_target_wrapper_fix: PASS
static_tests_reported_by_dev4: "bash -n pass; py_compile pass; pytest 2 passed in 0.01s"
no_checkpoint_model_eval_current_state: true
home_xu_yang_outputs_required_for_retry: true
no_remote_source_dependency_network_required: true
runtime_authorized_by_this_gate: false
fresh_pm_authorization_required: true
eval_handoff: BLOCKED_NO_MODEL
no_ltp_gpu_preflight_sft_eval_by_test1: true
```
