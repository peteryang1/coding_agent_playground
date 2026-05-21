# dev_3 Session 23 PR59 Data Confirmation

Task ID: `M1-S23-PR59-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm whether the PR59 `LLAMAFACTORY_CLI` launcher blocker requires any ShareGPT data or dataset package change.

No LTP submit, GPU command, remote command, transfer command, SFT, dry-run, or eval was run by dev_3.

## Decision

Decision: no data/package change is needed for the PR59 `LLAMAFACTORY_CLI` launcher blocker.

The PR59 runtime cleared source/data/mcore transfer, checksum verification, `mcore_adapter` import check, structured preflight, and dataset config gates. The single authorized SFT attempt then failed before training/checkpoint generation with:

```text
final blocker: BLOCKED_PR59_RUNTIME_LLAMAFACTORY_CLI_COMMAND_STRING
EXIT_STATUS=127
failure signature: scripts/train_qwen3_8b_sft.sh: line 244: python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py: No such file or directory
root cause: LLAMAFACTORY_CLI was set to a space-containing command string, but scripts/train_qwen3_8b_sft.sh executes "${LLAMAFACTORY_CLI}" train ... as a single command path
```

This is launcher command invocation only. It does not implicate ShareGPT JSONL content, row count, schema, provenance, dataset_info, transfer staging, or data package registration.

## Accepted ShareGPT Dataset Contract

Accepted source artifact:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Accepted sha256:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Row count:

```text
10
```

Schema:

```text
coding_agent_playground_sft_v1_sharegpt_messages
messages[*].from
messages[*].value
```

Dataset info entry:

```text
coding_agent_m1_sft_10_sharegpt
```

Required provenance fields to preserve:

```text
example_id
trajectory_id
repo
task
source
```

## PR59 Transfer Result

From `evidence/dev_2_s23_pr59_preflight_sft_runtime.md` and `evidence/gpu_s23_pr59_preflight_sft_tracking.md`:

```text
runtime task: M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2
PR59 merge commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
source bundle sha256: 2f272f210b67ed45b4a7b05592881c8c036fb34de2660645d6f96af76adf4d85
source file count: 131
mcore_adapter bundle sha256: ec0ace00eeca1f4d60710deea59621c868860e34827a5b645122f64f043170e7
frame: xu.yang~coding-agent-playground-m1-s23-pr59-preflight-sft-20260521T163413Z
endpoint: ssh -p 27043 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
output root: /home/xu.yang/coding_agent_playground/outputs
```

Local data preparation:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr59_preflight_sft_20260521T163413Z/train.jsonl
dataset source: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

Post-transfer verification:

```text
remote workspace: /root/workspace
remote repo path: /root/workspace/coding_agent_playground
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source bundle sha256: OK
mcore_adapter bundle sha256: OK
dataset sha256: OK
critical source checksums: OK
mcore_adapter file checksums: OK
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
mcore_adapter import check: PASS
structured preflight: PASS
SFT_ALLOWED: true
remote source/dependency network: not used
```

Interpretation:

- The accepted ShareGPT dataset was transferred from local/provided workspace and verified on the remote node.
- The remote dataset checksum matched the accepted source checksum.
- No evidence indicates data content drift, schema drift, row-count drift, or dataset_info mismatch.
- The SFT blocker happened after transfer/import/preflight success, at launcher command invocation.

## Runtime Data Evidence Interpreted

PR59 used the expected dataset path and name:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

The failure was:

```text
LLAMAFACTORY_CLI command string was treated as a single executable path
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run, not authorized
```

There is no evidence of a data parser, dataloader, tokenizer, LLamaFactory dataset_info, row-count, checksum, schema, or provenance defect.

## Future Data/Transfer Expectations

For any future PM-authorized retry after the PR59 launcher fix, keep the accepted data contract unchanged:

```text
dataset_info remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
```

Runtime owners must keep using local/provided source/data/dependency bundles, no remote GitHub/source/dependency downloads, exact transfer commands, and post-transfer checksum/file-list verification.

Generated temporary data, staging copies, dependency targets, logs, run metadata, checkpoints, eval artifacts, and other intermediates must default under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Allowed runtime compatibility input exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: existing accepted source/runtime input path after checksum verification.

## Data-Side Blocker Status

No current data-side blocker found.

Do not regenerate, duplicate, repack, or convert the accepted ShareGPT dataset for this launcher blocker unless a new PM data task identifies a concrete data defect.

## Completion Marker

Complete for `M1-S23-PR59-DATA-CONFIRM-DEV3`:

- Confirmed the PR59 `LLAMAFACTORY_CLI` launcher blocker does not require data/package changes.
- Cited accepted ShareGPT sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info `coding_agent_m1_sft_10_sharegpt`.
- Cited PR59 transfer/checksum/import/preflight result.
- Found no current data-side blocker.
- No LTP/GPU/SFT/dry-run/eval/remote execution performed by dev_3.
