# Dev 1 PR55 SFT Blocker Review - M1-S23-PR55-SFT-BLOCKER-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-PR55-SFT-BLOCKER-REVIEW-DEV1`  
Evidence date: 2026-05-21  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_pr55_sft_blocker_review.md`  
Execution boundary: no LTP, GPU, preflight, SFT, eval, remote commands, remote experiment, or dry-run by `intern_code_dev_1`.

## Result

`PASS_FOR_PM_RETRY`

I refreshed the review against PR #57 and `evidence/dev_4_s23_pr55_sft_wrapper_fix.md`. The prior dev_1 blocker `BLOCKER_MISSING_DEV4_WRAPPER_FIX` is resolved. PR #57 addresses the PR55 SFT launch-wrapper failure `environment: DEP_TARGET: unbound variable` while preserving the `/home/xu.yang` output policy, no-remote-source/dependency-network runtime rule, and manifest/logging behavior.

Runtime remains separately PM-authorized. This review does not authorize LTP/GPU/preflight/SFT/eval/dry-run.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s23_pr55_preflight_sft_runtime.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s23_pr55_preflight_sft_tracking.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr55_sft_wrapper_fix.md`
- PR #57 functional head named by PM: `0253ff99cb1bd595bc68bda5a7a4bf7d5983162c`
- PR #57 fetched ref head: `b94dd93c131b9a6472919c14ae71684d71683a60`

PR #57 note: local fetch of `pull/57/head` resolved to `b94dd93c131b9a6472919c14ae71684d71683a60`, which contains PM-named functional commit `0253ff99cb1bd595bc68bda5a7a4bf7d5983162c`. The delta after `0253ff9` is docs/status/evidence only.

## Prior Runtime Blocker

The PR55 runtime cleared gates up to SFT:

```text
node: lg-cmc-b7r202-q05u06-h200-000722
forbidden-node check: PASS
output root: /home/xu.yang/coding_agent_playground/outputs on fuse.ceph-fuse
capacity probe: PASS_AND_CLEANED
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
PREFLIGHT_RESULT=PASS
SFT_ALLOWED=true
```

The single authorized SFT attempt then exited before GPU training:

```text
EXIT_STATUS=1
blocker: environment: DEP_TARGET: unbound variable
```

No checkpoint/model, `trainer_state.json`, `all_results.json`, or eval artifact was produced.

## Cleared Runtime Gates

Resource/placement: PASS.

- Fresh allocation landed on non-forbidden node `lg-cmc-b7r202-q05u06-h200-000722`.
- Stop proof confirms final `STOPPED (Completed)` and no active Milestone GPU remains.

Storage/capacity: PASS.

- `/mnt/cephfs`: `fuse.ceph-fuse`
- `/home/xu.yang/coding_agent_playground/outputs`: `fuse.ceph-fuse`
- capacity probe wrote and removed `25,769,803,776` bytes.

Source/data/dependency transfer: PASS for current review.

- Source bundle and ShareGPT data were transferred from local/provided artifacts and checksum-verified.
- dev_2 records no remote `git clone`, `git fetch`, GitHub source fetch, or remote dependency download on the GPU node.
- Python deps were bundled locally outside the GPU node, transferred, installed/extracted from local files, and used under the run's `/home/xu.yang` output tree.

Data: PASS.

- dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`
- row count: `10`
- schema: ShareGPT `messages[*].from/value`
- dataset entry: `coding_agent_m1_sft_10_sharegpt`

Preflight: PASS.

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

## PR #57 Fix Review

Status: PASS.

Patch files:

- `scripts/train_qwen3_8b_sft.sh`
- `tests/test_train_qwen3_8b_sft_static.py`

The wrapper now defines and exports the required runtime environment contract:

```text
LLAMAFACTORY_CLI="${LLAMAFACTORY_CLI:-llamafactory-cli}"
DEP_TARGET="${DEP_TARGET:-${PYTHON_DEPS_DIR:-${RUN_DIR}/python_deps}}"
LF="${LF:-${LLAMAFACTORY_DIR}}"
export DEP_TARGET LF LLAMAFACTORY_CLI
```

Before the final training invocation it also re-exports:

```text
export DEP_TARGET="${DEP_TARGET}"
export LF="${LF}"
"${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"
```

This directly addresses the observed `DEP_TARGET` unbound-variable failure.

## Output / Manifest / Logging Preservation

Status: PASS.

The default `DEP_TARGET` is under:

```text
${RUN_DIR}/python_deps
```

Because `RUN_DIR` defaults to:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>
```

the generated dependency target remains under `/home/xu.yang/coding_agent_playground/outputs` by default.

The patch preserves existing durable artifact paths for:

- `RUN_DIR`
- `CHECKPOINT_DIR`
- `TMPDIR`
- stdout/stderr log
- xtrace log
- early-exit diagnostics
- exit status
- preflight JSON
- runtime config
- run manifest

The wrapper now logs:

```text
LLAMAFACTORY_CLI=<value>
DEP_TARGET=<value>
LF=<value>
```

The manifest launch command records explicit `DEP_TARGET`, `LF`, `PYTHONPATH`, configurable `LLAMAFACTORY_CLI`, and `RUNTIME_CONFIG`. This preserves and improves the manifest/logging behavior for future triage.

## No-Remote-Network Rule

Status: PASS.

PR #57 does not add remote fetch, install, clone, or download behavior. The dev_4 evidence states future runtime should continue local bundle transfer and checksum verification for source, ShareGPT data, dependency wheels/extracted dependency tree, and any optional LLamaFactory CLI wrapper.

If a future runtime uses a chmod-capable wrapper under `/root/workspace`, dev_4 evidence scopes that as executable source staging only; generated logs/checkpoints/run metadata/intermediates must remain under `/home/xu.yang/coding_agent_playground/outputs`.

## Static/Test Evidence

dev_4 reports local-only checks:

```bash
bash -n scripts/train_qwen3_8b_sft.sh
python3 -m py_compile tests/test_train_qwen3_8b_sft_static.py
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Observed result:

```text
bash -n scripts/train_qwen3_8b_sft.sh: pass
python3 -m py_compile tests/test_train_qwen3_8b_sft_static.py: pass
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 2 passed in 0.01s
```

I did not run tests, parser, preflight, LTP, GPU, SFT, eval, or dry-run.

## Remaining Conditions For Future Runtime

No dev_1 blocker remains for PM retry gate after PR #57. A future runtime still needs explicit PM authorization and must preserve:

- non-forbidden node gate before transfer;
- no remote source/dependency network on the GPU node;
- local source/data/dependency bundle transfer and checksum verification;
- `/home/xu.yang/coding_agent_playground/outputs` storage/capacity proof;
- structured preflight before SFT;
- SFT only if preflight `PASS` and `sft_allowed=true`;
- stop proof and artifact preservation;
- checkpoint/model, `trainer_state.json`, and `all_results.json` checks after SFT.

## Completion Marker

```yaml
task_id: M1-S23-PR55-SFT-BLOCKER-REVIEW-DEV1
owner: intern_code_dev_1
result: PASS_FOR_PM_RETRY
pass_for_pm_retry: true
runtime_evidence_reviewed: true
dev4_fix_present: true
dev4_fix_evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr55_sft_wrapper_fix.md
pr57_functional_head_reviewed: 0253ff99cb1bd595bc68bda5a7a4bf7d5983162c
pr57_fetched_head_reviewed: b94dd93c131b9a6472919c14ae71684d71683a60
delta_after_functional_head_docs_status_evidence_only: true
resource_gate_cleared: true
assigned_node: lg-cmc-b7r202-q05u06-h200-000722
forbidden_node_gate: PASS_NON_FORBIDDEN
storage_cleared: true
capacity_probe_pass_and_cleaned: true
source_transfer_checksum_cleared: true
data_cleared: true
preflight_result: PASS
sft_allowed: true
prior_runtime_blocker: BLOCKER_PR55_SFT_WRAPPER_ENV_DEP_TARGET_UNBOUND
pr57_fix_addresses_prior_blocker: true
dep_target_env_contract_reviewed: true
lf_env_contract_reviewed: true
llamafactory_cli_env_contract_reviewed: true
home_xu_yang_output_preservation_reviewed: true
no_remote_network_rule_preserved: true
manifest_logging_behavior_preserved: true
sft_run_by_dev1: false
eval_run_by_dev1: false
ltp_gpu_preflight_sft_eval_remote_commands_by_dev1: false
exact_blockers: []
```
