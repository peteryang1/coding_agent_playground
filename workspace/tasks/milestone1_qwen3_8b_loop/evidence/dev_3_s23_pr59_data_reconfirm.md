# dev_3 Session 23 PR59 Data Reconfirmation

Task ID: `M1-S23-PR59-DATA-RECONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Reconfirm accepted ShareGPT data and `dataset_info` state for the PR59 path and any future PR59 retry.

No LTP submit, GPU command, remote command, transfer command, SFT, dry-run, or eval was run by dev_3.

## Decision

The accepted ShareGPT dataset and LLamaFactory `dataset_info` entry remain unchanged for PR59 and any future PR59 retry.

PR59 added runtime launch/dependency support around `mcore_adapter` and later exposed a launcher invocation blocker. It does not require data regeneration, data conversion, row-count changes, schema changes, or a different `dataset_info` entry.

## Accepted Data Contract

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

## PR59 Runtime Data Evidence

From `evidence/dev_2_s23_pr59_preflight_sft_runtime.md`:

```text
runtime task: M1-S23-PR59-PREFLIGHT-SFT-RUNTIME-DEV2
PR59 merge commit: 8ed6248cd7bd56b89ac1124689fed0b56e4eba02
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

Post-transfer data verification:

```text
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: OK
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
source/data/mcore transfer: PASS
remote source/dependency network: not used
```

Data interpretation:

- The transferred dataset checksum matched the accepted source checksum.
- No transfer evidence indicates data content drift or schema drift.
- The runtime continued to use `coding_agent_m1_sft_10_sharegpt`.
- The current blocker does not require data/package changes.

## Transfer And Staging Requirements

For any future PR59 retry, runtime owners must prepare source/config/scripts/data/dependency materials in a local/provided workspace first. Remote GPU/LTP nodes remain no-external-network for project code and dependency staging.

Required future transfer evidence:

```text
source commit / package id
local source file list and file count
local source bundle sha256
local dataset path and sha256
local mcore_adapter/dependency provenance and sha256
exact transfer command by scp, rsync, or tar-over-SSH
remote destination paths
post-transfer source bundle checksum verification
post-transfer file-list/checksum verification
post-transfer dataset sha256 verification
post-transfer mcore_adapter/dependency verification
proof statement that no remote git clone/fetch/GitHub/source/dependency download or pip download was used
```

Generated temporary data, staging copies, checksum sidecars, dependency targets, logs, run metadata, checkpoints, eval artifacts, and other intermediates must default under:

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

Future retry should keep:

```text
dataset_info: coding_agent_m1_sft_10_sharegpt
sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: messages[*].from/value
provenance fields: example_id/trajectory_id/repo/task/source
```

Do not regenerate, duplicate, repack, or convert the accepted ShareGPT dataset unless a new PM data task identifies a concrete data defect.

## Completion Marker

Complete for `M1-S23-PR59-DATA-RECONFIRM-DEV3`:

- Reconfirmed accepted ShareGPT data and `dataset_info` remain unchanged.
- Cited sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info `coding_agent_m1_sft_10_sharegpt`.
- Recorded future transfer/staging requirements under `/home/xu.yang/coding_agent_playground/outputs`.
- Found no data-side blocker.
- No LTP/GPU/SFT/dry-run/eval/remote execution performed by dev_3.
