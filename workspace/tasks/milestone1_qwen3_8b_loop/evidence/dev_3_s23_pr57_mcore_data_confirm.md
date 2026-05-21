# dev_3 Session 23 PR57 MCore Data Confirmation

Task ID: `M1-S23-PR57-MCORE-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm whether the PR57 mcore dependency blocker requires any ShareGPT data or dataset package change.

No LTP submit, GPU command, remote command, transfer command, SFT, dry-run, or eval was run by dev_3.

## Decision

Decision: no data/package change is needed for the PR57 mcore dependency blocker.

The PR57 runtime cleared source/data transfer, checksum verification, `/home/xu.yang` storage/capacity, structured preflight, and dataset config gates. The single authorized SFT attempt then failed before checkpoint creation with:

```text
final status: BLOCKED_PR57_RUNTIME_MISSING_MCORE_ADAPTER_STOPPED_NO_CHECKPOINT
EXIT_STATUS=1
failure: ImportError: mcore_adapter is required when USE_MCA=1. Please install `mcore_adapter` and its dependencies.
```

This is a runtime dependency/environment blocker for the MCA path. It does not implicate ShareGPT JSONL content, row count, schema, provenance, dataset_info, or transfer drift.

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

Known aggregate invariants:

```text
line_count == 10
unique_example_ids == 10
unique_trajectory_ids == 10
repo_split == {"fastapi/fastapi": 4, "scikit-learn/scikit-learn": 3, "Textualize/rich": 3}
role_values == {"human": 10, "gpt": 10}
message_keys == ["from", "value"]
```

## PR57 Transfer Result

From `evidence/dev_2_s23_pr57_preflight_sft_runtime.md`, `evidence/gpu_s23_pr57_preflight_sft_tracking.md`, and `task_registry.md`:

```text
runtime task: M1-S23-PR57-PREFLIGHT-SFT-RUNTIME-DEV2
authorized source commit: b4ac31ef1e3772953108348bf099818326ed65cc
source bundle sha256: 1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa
source file count: 122
frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
endpoint: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
remote repo path: /root/workspace/coding_agent_playground
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
remote staging root: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr57_preflight_sft_20260521T155200Z/staging
```

Local data preparation:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_s23_pr57_20260521T155200Z/train.jsonl
dataset source: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

Transfer command recorded by dev_2:

```bash
scp -P 22662 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc.tar.gz \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_remote_bundle.sha256 \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_remote_critical_files.sha256 \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_file_list.txt \
  /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_transfer_manifest.sha256 \
  /tmp/cleaned_m1_sft_10_sharegpt_s23_pr57_20260521T155200Z/train.jsonl \
  root@10.100.22.31:/root/workspace/
```

Post-transfer verification:

```text
bundle sha256: OK
critical file checksums: OK
remote file count: 122
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
additional local dependency bundles transferred and verified: OK
remote project source/dependency network: not used
```

Interpretation:

- The accepted ShareGPT dataset was transferred from local/provided workspace.
- The remote dataset checksum matched the accepted source checksum.
- No transfer evidence indicates data content drift or schema drift.
- The runtime obeyed the no-remote-network rule for project code/dependency staging.

## Runtime Data Evidence Interpreted

PR57 cleared all data-relevant runtime gates before the mcore dependency failure:

```text
/home/xu.yang storage/capacity: PASS_AND_CLEANED
source/data/dependency transfer: passed
checksum verification: passed
structured preflight: PASS
SFT_ALLOWED: true
dataset: coding_agent_m1_sft_10_sharegpt
dataset source sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
preprocessing_num_workers: null
dataloader_num_workers: 0
max_steps: 2
```

The SFT failure occurred after launcher/distributed initialization:

```text
SFT start: 2026-05-21T16:03:06Z
SFT end: 2026-05-21T16:03:28Z
launcher initialized 8 distributed tasks
failure: ImportError: mcore_adapter is required when USE_MCA=1
checkpoint files: none
trainer_state.json: absent
all_results.json: absent
eval: not run
```

There is no evidence of a data parser, dataloader, tokenizer, LLamaFactory dataset_info, row-count, checksum, schema, or provenance defect.

## Future Data/Transfer Expectations

For any future PM-authorized retry after the mcore fix, keep the accepted data contract unchanged:

```text
dataset_info remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
```

The remote GPU/LTP node remains no-external-network for project code and dependency staging. Runtime owners must prepare code/config/scripts/data/dependency materials in a local/provided workspace, verify exact commit, file list, checksums, dataset sha256, and dependency bundle checksums locally, transfer by `rsync`, `scp`, or tar-over-SSH, then verify the bundle/file list/dataset/dependencies after transfer.

Future generated temporary data, staging copies, checksum sidecars, dependency targets, logs, run metadata, checkpoints, eval artifacts, and other intermediates must default under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Allowed runtime compatibility input exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: existing accepted source/runtime input path after checksum verification. New generated artifacts and intermediates should remain under `/home/xu.yang/coding_agent_playground/outputs` unless a required-path exception is explicitly justified.

## Data-Side Blocker Status

No current data-side blocker found.

The current blocker should be handled as an MCA dependency/config/base-image/launch-package issue:

```text
ImportError: mcore_adapter is required when USE_MCA=1
```

Do not regenerate, duplicate, repack, or convert the accepted ShareGPT dataset for this blocker unless a new PM data task identifies a concrete data defect.

## Completion Marker

Complete for `M1-S23-PR57-MCORE-DATA-CONFIRM-DEV3`:

- Confirmed the PR57 mcore dependency blocker does not require data/package changes.
- Cited accepted ShareGPT sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info entry `coding_agent_m1_sft_10_sharegpt`.
- Cited PR57 transfer command/result and remote dataset checksum match.
- Found no current data-side blocker.
- No LTP/GPU/SFT/dry-run/eval/remote execution performed by dev_3.
