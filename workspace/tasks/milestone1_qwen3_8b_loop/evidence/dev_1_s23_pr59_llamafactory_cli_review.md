# Dev 1 Review - M1-S23-PR59-LLAMAFACTORY-CLI-REVIEW-DEV1

Owner: `intern_code_dev_1`  
Task: `M1-S23-PR59-LLAMAFACTORY-CLI-REVIEW-DEV1`  
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_s23_pr59_llamafactory_cli_review.md`  
Review timestamp: `2026-05-21T17:05:18Z`  
Result: `PASS_FOR_PM_RETRY`

## Execution Boundary

- Dev_1 did not run LTP, GPU, preflight, SFT, eval, dry-run, transfer, or remote commands.
- Dev_1 reviewed durable local PM evidence and PR #61 code statically.
- Local checks run by dev_1 were shell syntax and static pytest only.

## Inputs Reviewed

- `workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md`
- `evidence/dev_2_s23_pr59_preflight_sft_runtime.md`
- `evidence/gpu_s23_pr59_preflight_sft_tracking.md`
- `evidence/pm_s23_pr59_preflight_sft_authorization.md`
- `evidence/dev_4_s23_pr59_llamafactory_cli_fix.md`
- PR #61 latest local/remote head: `d4f3340d1f7b32d91553cbe18d7effce533276c7`
- PR #61 functional patch commit: `59524d9`

## Runtime Evidence Review

Dev_2 PR59 final runtime evidence remains sufficient to classify the blocker:

- Authorized source commit: PR #59 merge commit `8ed6248cd7bd56b89ac1124689fed0b56e4eba02`.
- Runtime frame: `xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z`.
- Endpoint/node: `ssh -p 27043 root@10.100.22.28`, `lg-cmc-b7r202-q05u06-h200-000722`.
- Source/data/`mcore_adapter` were prepared from local/provided paths before transfer.
- Source bundle sha256: `2f272f210b67ed45b4a7b05592881c8c036fb34de2660645d6f96af76adf4d85`.
- `mcore_adapter` bundle sha256: `ec0ace00eeca1f4d60710deea59621c868860e34827a5b645122f64f043170e7`.
- Dataset sha256: `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Transfer and post-transfer verification passed for source, data, `mcore_adapter`, and dependency bundles.
- No remote `git clone`, `git fetch`, GitHub/source fetch, dependency download, or `pip download` was run.
- `/home/xu.yang/coding_agent_playground/outputs` CephFS/capacity proof passed.
- `MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter`.
- `mcore_adapter` import check passed before SFT.
- Structured preflight passed:
  - `PREFLIGHT_RESULT=PASS`
  - `PREFLIGHT_STRUCTURED_STATUS=PASS`
  - `ACTIONABLE_FAULT=false`
  - `SFT_ALLOWED=true`
  - `TORCH_NCCL_ALLREDUCE_EXIT=0`
  - `CAPACITY_PROBE_STATUS=PASS`
  - `DIFFERENT_NODE_GATE=PASS`
  - `HOME_XU_YANG_STORAGE_STATUS=PASS`
  - `TOPOLOGY_CAPTURE_STATUS=PRESENT`
  - `NVLINK_CAPTURE_STATUS=PRESENT`
- Exactly one SFT attempt ran because transfer/import/preflight gates passed and `SFT_ALLOWED=true`.
- Eval was not authorized and was not run.

## Blocker Classification

Runtime result: `BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING_STOPPED`

Failure signature:

```text
EXIT_STATUS=127
failure signature: scripts/train_qwen3_8b_sft.sh: line 244: python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py: No such file or directory
```

Root cause recorded by dev_2:

```text
LLAMAFACTORY_CLI was set to the space-containing command string `python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`, but `scripts/train_qwen3_8b_sft.sh` executes `"${LLAMAFACTORY_CLI}" train ...` as a single command path.
```

Classification:

- This is a launcher invocation/quoting blocker.
- It is not a data, storage, `mcore_adapter`, preflight, NCCL, stop-proof, or eval blocker.
- No checkpoint/model, `trainer_state.json`, or `all_results.json` was produced.
- Eval remains blocked because there is no model/checkpoint/served endpoint.

## Stop Proof

Stop proof remains sufficient:

- Stop command was recorded.
- Stop response was status 202.
- Final LTP state was `STOPPED (Completed)`.
- Endpoint refused connection after stop.
- Running-job proof returned `No jobs found`.
- Dev_2 records no active Milestone GPU is held and fresh PM authorization is required before further LTP/GPU/preflight/SFT/eval.

## PR #61 / Dev_4 Fix Review

PM reports PR #61 is open, non-draft, `MERGEABLE` / `CLEAN`.

Reviewed head:

```text
d4f3340d1f7b32d91553cbe18d7effce533276c7 Record PR61 LLamaFactory CLI gate state
```

Functional patch commit:

```text
59524d9 Fix LLamaFactory CLI command invocation
```

PR #61 changed functional files:

- `scripts/train_qwen3_8b_sft.sh`
- `tests/test_train_qwen3_8b_sft_static.py`

Remaining changes are task/status/evidence/history documentation for the PR59 LLamaFactory CLI fix.

The fix is acceptable for PM retry gate:

- Cites dev_2 PR59 final runtime evidence and the exact `EXIT_STATUS=127` launcher command-string failure.
- Keeps `LLAMAFACTORY_CLI` default as `llamafactory-cli`.
- Preserves `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, and `MCORE_ADAPTER_DIR` export behavior.
- Parses `LLAMAFACTORY_CLI` into a Bash array `LLAMAFACTORY_CMD` using `read -r -a`.
- Rejects an empty parsed command with an explicit launcher error.
- Renders the parsed command for manifest/logging with `%q`, so command evidence remains shell-readable.
- Uses `"${LLAMAFACTORY_CMD[@]}" train "${RUNTIME_CONFIG}"` for final invocation, which supports both `llamafactory-cli` and `python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py`.
- Removes the prior failing pattern `"${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"`.
- Preserves the PR59 `MCORE_ADAPTER_DIR`/PYTHONPATH import gate for `USE_MCA=1`.
- Preserves no-remote-source/dependency-download and `/home/xu.yang/coding_agent_playground/outputs` requirements by leaving those paths/rules intact.
- Does not claim checkpoint/eval readiness; it only fixes the launcher invocation blocker before a separately authorized retry.

## Dev_1 Static Checks

Commands run locally in dev_4 worktree:

```bash
bash -n scripts/train_qwen3_8b_sft.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Results:

```text
bash -n scripts/train_qwen3_8b_sft.sh: exit 0
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q: 4 passed in 0.01s
```

## Remaining Retry Conditions

`PASS_FOR_PM_RETRY` here means PR #61 is acceptable for PM retry gating. It does not mean eval handoff or checkpoint readiness.

Before any new runtime, the runtime owner evidence must still record:

- PR #61 merge/completion-marked source commit selected by PM.
- Local/provided source/data/`mcore_adapter` provenance.
- File lists, bundle checksums, exact transfer command, destination, and post-transfer verification.
- No remote source/dependency downloads on the GPU/LTP node.
- `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, `MCORE_ADAPTER_DIR`, and rendered `LLAMAFACTORY_CMD`.
- `mcore_adapter` import check proof.
- `/home/xu.yang/coding_agent_playground/outputs` generated output paths.
- Structured preflight PASS and `SFT_ALLOWED=true` before SFT.
- SFT result, checkpoint/model or exact blocker, and stop/no-running-job proof.

## Decision

`PASS_FOR_PM_RETRY`

PR #61 addresses the PR59 `LLAMAFACTORY_CLI` command-string blocker without weakening prior wrapper env, local bundle/no-remote-network, `mcore_adapter`, preflight, SFT gating, `/home/xu.yang` output, or stop-proof requirements.
