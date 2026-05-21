# Test 1 S23 PR57 MCore Gate

Task ID: `M1-S23-PR57-MCORE-GATE-TEST1`
Gate owner: `intern_code_test_1`
Runtime owner: `intern_code_dev_2`
Fix owner: `intern_code_dev_4`
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s23_pr57_mcore_gate.md`
Status timestamp: `2026-05-21T16:20:08Z`

## Result

`PASS_FOR_PM_RETRY`

No LTP, GPU, preflight, SFT, eval, dry-run, transfer command, remote command, parser execution, or PR code execution was run by `intern_code_test_1`.

This is a no-execution PM retry gate only. It does not authorize a new runtime by itself. Fresh PM authorization remains required after PR #59 is merged and completion-marked.

## Inputs Reviewed

- `evidence/pm_s23_pr57_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr57_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr57_preflight_sft_tracking.md`
- `evidence/dev_4_s23_pr57_mcore_fix.md`
- PR #59: `https://github.com/peteryang1/coding_agent_playground/pull/59`
- PM-named functional head: `92e437cf690b68121b9ad9d2f76b18a60a10a2d6`
- Fetched PR head observed by test_1: `6b92490d0e9db32da3380a38ada27d75ed529970`

GitHub metadata reviewed by test_1:

```text
state: OPEN
draft: false
mergeable: MERGEABLE
merge_state_status: CLEAN
```

Diff from `92e437cf690b68121b9ad9d2f76b18a60a10a2d6` to `6b92490d0e9db32da3380a38ada27d75ed529970` changes only task/evidence/status/history files. The functional source changes are in `92e437cf690b68121b9ad9d2f76b18a60a10a2d6`.

## Runtime Findings Retained

The prior PR57 runtime remains blocked for model/eval output:

```text
runtime task: M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2
source commit: b4ac31ef1e3772953108348bf099818326ed65cc
frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
endpoint: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
preflight: PASS
SFT_ALLOWED: true
SFT attempt count: 1 of 1 authorized
SFT exit: EXIT_STATUS=1, END_UTC=2026-05-21T16:03:28Z
runtime blocker: ImportError: mcore_adapter is required when USE_MCA=1
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
stop proof: STOPPED (Completed), endpoint refused, no running coding-agent-playground job
```

Transfer/no-network/storage findings remain accepted:

```text
source bundle sha256: 1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa
source file count: 122
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
transfer method: scp to root@10.100.22.31:/root/workspace/
post-transfer verification: bundle sha256 OK, critical files OK, file count OK, dataset sha256 OK
remote project source/dependency network: no remote git clone/fetch/GitHub/source/dependency download recorded
output root: /home/xu.yang/coding_agent_playground/outputs
capacity probe: PASS_AND_CLEANED, 25769803776 bytes written and removed
```

## PR #59 MCore Fix Gate

PASS.

Reviewed functional commit `92e437cf690b68121b9ad9d2f76b18a60a10a2d6` for:

```text
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
tests/test_train_qwen3_8b_sft_static.py
```

The patch covers the `mcore_adapter` / `USE_MCA=1` blocker without adding remote dependency downloads:

- Adds `MCORE_ADAPTER_DIR="${MCORE_ADAPTER_DIR:-${REPO_ROOT}/code/mcore_adapter}"`.
- Exports `MCORE_ADAPTER_DIR` with the existing wrapper environment contract.
- Builds `PYTHONPATH_PREFIX` from `LLAMAFACTORY_DIR/src` and prepends `MCORE_ADAPTER_DIR` when that directory exists.
- Records `MCORE_ADAPTER_DIR` in logs.
- Records `MCORE_ADAPTER_DIR` and `PYTHONPATH_PREFIX` in `run_manifest.json`.
- Records `MCORE_ADAPTER_DIR` in the manifest launch command.
- When `USE_MCA=1`, runs a Python import gate for `mcore_adapter` before LLamaFactory training launch.
- If the import gate fails, exits early with explicit instructions to provide `mcore_adapter` via local/provided dependency bundle, not remote clone/fetch/download.
- Leaves non-MCA fallback unselected, which is correct for this gate because changing away from MCA would alter the backend/parallelism path and needs separate PM/dev_1/test_1 approval.

Static evidence reported by dev_4:

```text
bash -n scripts/train_qwen3_8b_sft.sh: exit 0
python3 -m py_compile scripts/write_sft_run_manifest.py: exit 0
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 3 passed in 0.01s
```

test_1 did not run these commands; test_1 reviewed durable evidence and source diff only.

## Required Future Runtime Conditions

PM can consider a fresh retry only after PR #59 is merged and completion-marked, with a separate PM authorization. The next runtime must prove:

1. `mcore_adapter` source/tree or package is prepared in a local/provided workspace before remote use.
2. Dependency provenance, file list, and checksum are recorded locally.
3. Dependency bundle is transferred by `scp`, `rsync`, or tar-over-SSH.
4. Remote post-transfer verification records sha256, destination, and `MCORE_ADAPTER_DIR`.
5. Remote GPU/LTP node does not run project source/dependency `git clone`, `git fetch`, GitHub/source download, pip download, or equivalent external dependency retrieval.
6. `MCORE_ADAPTER_DIR` points to the transferred local/provided dependency location.
7. `USE_MCA=1` import gate records `mcore_adapter import OK for USE_MCA=1` before SFT starts.
8. `/home/xu.yang/coding_agent_playground/outputs` remains the generated output/log/tmp/checkpoint/run-metadata/intermediate root.
9. Structured preflight is `PASS` with `SFT_ALLOWED=true` before SFT.
10. SFT logs show no regression to prior blockers, including `DEP_TARGET: unbound variable`, missing dataset info, `KeyError: 'from'`, ENOSPC, dataset-map SyncManager EOF, NCCL/NVLink peer-memory failure, preflight parser false positive, or `mcore_adapter is required when USE_MCA=1`.
11. Eval handoff remains blocked until a complete checkpoint/model plus `trainer_state.json` and `all_results.json`, or PM-approved replacements, exist with stop proof.

## Completion Marker

```yaml
task_id: M1-S23-PR57-MCORE-GATE-TEST1
owner: intern_code_test_1
result: PASS_FOR_PM_RETRY
pr: 59
pm_named_functional_head: 92e437cf690b68121b9ad9d2f76b18a60a10a2d6
observed_pr_head: 6b92490d0e9db32da3380a38ada27d75ed529970
mcore_adapter_use_mca_fix: PASS
no_remote_dependency_download_rule_preserved: true
checkpoint_model_present_current_runtime: false
trainer_state_json_present_current_runtime: false
all_results_json_present_current_runtime: false
eval_handoff: BLOCKED_NO_MODEL
fresh_pm_authorization_required: true
no_ltp_gpu_preflight_sft_eval_by_test1: true
```
