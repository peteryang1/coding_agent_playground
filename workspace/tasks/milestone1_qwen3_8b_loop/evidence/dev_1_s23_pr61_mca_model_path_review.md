# Dev 1 Review - M1-S23-PR61-MCA-MODEL-PATH-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-PR61-MCA-MODEL-PATH-REVIEW-DEV1`  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_pr61_mca_model_path_review.md`  
Review timestamp: `2026-05-21T17:59:23Z`  
Result: `PASS_FOR_PM_RETRY`

## Execution Boundary

- Dev_1 did not run LTP, GPU, preflight, SFT, eval, dry-run, transfer, or remote commands.
- Dev_1 reviewed durable local PM evidence, dev_4 PR #63 branch evidence, and PR #63 code statically.
- Local checks run by dev_1 were shell syntax and static pytest only.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- `evidence/pm_s23_pr61_preflight_sft_authorization.md`
- `evidence/dev_2_s23_pr61_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr61_preflight_sft_tracking.md`
- Dev_4 PR #63 branch `intern_code_dev_4/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4`
- PR #63 head reviewed: `a035692dc72b40434240d0308c36f4d071644849`
- Dev_4 fix evidence at PR head: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr61_mca_model_path_fix.md`

Note: at review time, the PM durable worktree did not yet contain `evidence/dev_4_s23_pr61_mca_model_path_fix.md`, but the PR #63 head contains that evidence file and the PM request explicitly asked to refresh against PR #63.

## Runtime Evidence Review

Dev_2 PR61 final runtime evidence remains sufficient to classify the blocker:

- Authorized source:
  - PR #61 merge commit `aa426b045b52b71bc23b4a2f73f3ee1c42187037`
  - PR #62 completion/source commit `713862da983f73b165af1cfe27935ccef616a049`
- Runtime frame: `xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z`.
- Endpoint/node: `ssh -p 33089 root@10.100.22.31`, `lg-cmc-b7r202-q04u06-h200-000725`.
- Source/data/`mcore_adapter` were prepared from local/provided paths before transfer.
- Source bundle sha256: `a8aeb73d6f3c69775997b7c4b6cf49344a0e8691a44811b68d5678caaacb83c4`.
- Source file list count: 135.
- `mcore_adapter` bundle sha256: `4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb`.
- Dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Transfer command and post-transfer verification are recorded.
- Post-transfer verification passed for source bundle, `mcore_adapter` bundle, dataset, Python dependency bundle, LLamaFactory bundle, flash-attn wheel, critical source checksums, and `mcore_adapter` file checksums.
- No remote `git clone`, `git fetch`, GitHub/source fetch, dependency download, or `pip download` was run.
- `/home/xu.yang/coding_agent_playground/outputs` CephFS/capacity proof passed.
- `MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter`.
- `mcore_adapter` import check passed before preflight/SFT.
- Structured preflight passed:
  - `PREFLIGHT_RESULT=PASS`
  - `PREFLIGHT_STRUCTURED_STATUS=PASS`
  - `ACTIONABLE_FAULT=false`
  - `SFT_ALLOWED=true`
  - `TORCH_NCCL_ALLREDUCE_EXIT=0`
  - `CAPACITY_PROBE_STATUS=PASS`
  - `HOME_XU_YANG_STORAGE_STATUS=PASS`
  - `TOPOLOGY_CAPTURE_STATUS=PRESENT`
  - `NVLINK_CAPTURE_STATUS=PRESENT`
- `DIFFERENT_NODE_GATE=UNKNOWN` is recorded, but PM authorization did not name a different-node requirement for this PR61 run; the active blocker is not node-placement related.
- Exactly one SFT attempt ran because transfer/import/preflight gates passed and `SFT_ALLOWED=true`.
- Eval was not authorized and was not run.

## PR61 CLI Fix Verification

The PR61 `LLAMAFACTORY_CMD` parsing fix remained effective in the PR61 runtime:

- `LLAMAFACTORY_CLI=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`.
- Log evidence includes parsed `LLAMAFACTORY_CMD=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`.
- Prior quoted single-path signature from PR59 did not recur.
- Execution reached `launcher.py`; traceback originates under `/root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`.

## Blocker Classification

Runtime result: `BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE`

Failure signature:

```text
EXIT_STATUS=1
failure signature: ValueError: Please provide `model_name_or_path`.
trace path: llamafactory/launcher.py -> train/tuner.py -> hparams/parser.py -> model_args.py
```

Runtime config proof shows the generated YAML did contain:

```text
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
preprocessing_num_workers: null
dataloader_num_workers: 0
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
max_steps: 2
```

Classification:

- This is an MCA/LLamaFactory model-argument binding or config parsing blocker.
- It is distinct from the PR59 quoted `LLAMAFACTORY_CLI` single-path bug because `LLAMAFACTORY_CMD` was parsed and `launcher.py` was reached.
- It is not a source/data transfer, storage, `mcore_adapter`, import, preflight, or stop-proof blocker.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` was produced.
- Eval remains blocked because there is no model/checkpoint/served endpoint.

## Stop Proof

Stop proof is sufficient:

- Stop command was recorded.
- Stop response was status 202.
- Final LTP state was `STOPPED (Completed)`.
- Completed timestamp: `2026-05-21 17:32:52`.
- Endpoint refused connection after stop.
- Running-job proof returned `No jobs found`.
- Dev_2 records no active Milestone GPU is held and fresh PM authorization is required before further LTP/GPU/preflight/SFT/eval.

## PR #63 / Dev_4 Fix Review

PM reports PR #63 is open, non-draft, `MERGEABLE` / `CLEAN`.

Latest reviewed head:

```text
a0ab039278198a6c1b0cd40009038d89cd602922 Record PR63 gate status for MCA model path fix
```

Previously gated functional head:

```text
a035692dc72b40434240d0308c36f4d071644849 Fix LLamaFactory direct launcher path for MCA SFT
```

Functional files changed:

- `scripts/train_qwen3_8b_sft.sh`
- `tests/test_train_qwen3_8b_sft_static.py`

Remaining changed files are task/status/evidence/history documentation for the PR61 MCA model-path fix.

Latest-head delta from `a035692dc72b40434240d0308c36f4d071644849` to `a0ab039278198a6c1b0cd40009038d89cd602922`:

- `workspace/interns/intern_code_dev_4/status.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4/README.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4/history_log.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr61_mca_model_path_fix.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md`
- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`

The latest-head delta is docs/status/evidence only. There is no change to `scripts/train_qwen3_8b_sft.sh` or `tests/test_train_qwen3_8b_sft_static.py` after the prior gated functional head. The evidence delta only updates the completion marker from "PR package prepared locally" to "PR #63 open/non-draft, MERGEABLE/CLEAN; waiting for PM gate".

The fix is acceptable for PM retry gate:

- Cites dev_2 PR61 final runtime logs and runtime config proof.
- Explains why direct `python3 .../llamafactory/launcher.py train <config>` reaches `launcher.py` directly with `sys.argv[1] == "train"`, so LLamaFactory `read_args()` does not load the YAML and `model_name_or_path` is not bound.
- Preserves PR61 command-array parsing: `LLAMAFACTORY_CLI` is still split with `read -r -a LLAMAFACTORY_CMD`.
- Preserves final invocation through `"${LLAMAFACTORY_CMD[@]}" train "${RUNTIME_CONFIG}"`.
- Adds normalization for any `*/llamafactory/launcher.py` element in `LLAMAFACTORY_CMD`, converting the command to the supported module CLI entrypoint `python3 -m llamafactory.cli`.
- Preserves command evidence by logging `LLAMAFACTORY_CMD_ORIGINAL`, `LLAMAFACTORY_CMD_NORMALIZATION`, and normalized `LLAMAFACTORY_CMD`.
- Preserves runtime config rewriting of `model_name_or_path` from `BASE_MODEL`.
- Preserves `DEP_TARGET`, `LF`, `MCORE_ADAPTER_DIR`, and `PYTHONPATH_PREFIX` behavior.
- Preserves `mcore_adapter` import gate for `USE_MCA=1`.
- Preserves the no-remote-source/dependency-download instruction in the wrapper.
- Preserves `/home/xu.yang/coding_agent_playground/outputs` output-root default and generated-output path policy.
- Does not claim checkpoint/eval readiness; it only fixes the launcher/config-parse blocker before a separately authorized retry.

## Dev_1 Static Checks

Commands run locally in dev_4 PR #63 worktree:

```bash
bash -n scripts/train_qwen3_8b_sft.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Results:

```text
bash -n scripts/train_qwen3_8b_sft.sh: exit 0
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 5 passed in 0.01s
```

## Remaining Retry Conditions

`PASS_FOR_PM_RETRY` here means PR #63 is acceptable for PM retry gating. It does not mean eval handoff or checkpoint readiness.

Before any new runtime, the runtime owner evidence must still record:

- PR #63 merge/completion-marked source commit selected by PM.
- Local/provided source/data/`mcore_adapter` provenance.
- File lists, bundle checksums, exact transfer command, destination, and post-transfer verification.
- No remote source/dependency downloads on the GPU/LTP node.
- `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, `LLAMAFACTORY_CMD_ORIGINAL`, `LLAMAFACTORY_CMD_NORMALIZATION`, normalized `LLAMAFACTORY_CMD`, and `MCORE_ADAPTER_DIR`.
- Runtime config proof that `model_name_or_path` is present.
- `mcore_adapter` import check proof.
- `/home/xu.yang/coding_agent_playground/outputs` generated output paths.
- Structured preflight PASS and `SFT_ALLOWED=true` before SFT.
- SFT result, checkpoint/model or exact blocker, and stop/no-running-job proof.

## Decision

`PASS_FOR_PM_RETRY`

PR #63 latest head `a0ab039278198a6c1b0cd40009038d89cd602922` remains acceptable. The latest delta after the previously gated functional head is docs/status/evidence only, so PR #63 still addresses the PR61 MCA/LLamaFactory `model_name_or_path` binding blocker without weakening PR61 `LLAMAFACTORY_CMD` parsing, `mcore_adapter`, no-remote-network, `/home/xu.yang`, preflight/SFT, or stop-proof gates.
