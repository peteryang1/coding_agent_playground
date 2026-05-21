# dev_3 Session 23 Ceph-Fuse Data Transfer Staging

Task ID: `M1-S23-CEPHFUSE-DATA-TRANSFER-STAGING-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Refresh the data and transfer staging contract for the next parser-patch retry after the `ceph-fuse: command not found` bootstrap failure.

No LTP submit, GPU allocation, SFT, dry-run, or eval was run.

## Current Blocker Interpretation

The failed parser-patch runtime attempt did not reach a usable endpoint for source or dataset transfer.

Current blocker:

```text
frame: xu.yang~coding-agent-playground-m1-s23-parserpatch-preflight-sft-20260521T124736Z
node: lg-cmc-b7r202-q04u06-h200-000725
endpoint: ssh -p 36822 root@10.100.22.31
state: FAILED (Completed)
exit: 220
log: /usr/local/pai/runtime.d/user.sh: line 45: ceph-fuse: command not found
```

Data impact:

- no dataset transfer occurred;
- no post-transfer checksum verification occurred;
- no parser preflight occurred;
- no SFT occurred;
- no checkpoint/model, `trainer_state.json`, or `all_results.json` exists.

Decision: this is a storage bootstrap/image blocker, not a data-side blocker.

## Accepted Source Dataset

Accepted source:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Checksum:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2  /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
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

Required provenance fields:

```text
example_id
trajectory_id
repo
task
source
```

Expected aggregate invariants:

```text
line_count == 10
unique_example_ids == 10
unique_trajectory_ids == 10
repo_split == {"fastapi/fastapi": 4, "scikit-learn/scikit-learn": 3, "Textualize/rich": 3}
role_values == {"human": 10, "gpt": 10}
message_keys == ["from", "value"]
```

## Local / Provided-Workspace Dataset Preparation

Before any future PM-authorized parser-patch retry, prepare and verify the dataset from the local/provided workspace side first. Do not depend on remote GitHub, remote package downloads, or remote source/dependency network access on the LTP node.

Required local preparation artifacts:

```text
local_dataset_source: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
local_dataset_sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
local_dataset_line_count: 10
local_dataset_schema: coding_agent_playground_sft_v1_sharegpt_messages
dataset_info_entry: coding_agent_m1_sft_10_sharegpt
```

Required local checks before transfer:

```bash
SOURCE=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256sum "${SOURCE}"
test "$(sha256sum "${SOURCE}" | awk '{print $1}')" = "26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2"
test "$(wc -l < "${SOURCE}")" = "10"
```

The code/config bundle and the accepted dataset may be transferred together or as separate local-to-remote artifacts, but both must be prepared and checksummed before remote transfer.

## Future Remote Transfer Contract

After the storage bootstrap/image fix provides a usable endpoint and proves `/home/xu.yang`, transfer the accepted dataset from the local/provided workspace to a run-specific path under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Recommended run-specific dataset path:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Recommended run-specific checksum sidecar:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/SHA256SUMS
```

Recommended run-specific provenance sidecar:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/provenance_summary.json
```

Recommended tmp/intermediate root:

```text
/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>/data
```

Acceptable transfer methods:

```text
tar-over-SSH
scp
rsync
```

Example transfer template, to be filled by the runtime owner after PM authorization:

```bash
RUN_ID=<RUN_ID>
PORT=<SSH_PORT>
HOST=<NODE_IP>
REMOTE_DATA_DIR=/home/xu.yang/coding_agent_playground/outputs/runs/train/${RUN_ID}/data/coding_agent_m1_sft_10_sharegpt
SOURCE=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl

ssh -p "${PORT}" root@"${HOST}" "mkdir -p '${REMOTE_DATA_DIR}'"
scp -P "${PORT}" "${SOURCE}" root@"${HOST}":"${REMOTE_DATA_DIR}/train.jsonl"
ssh -p "${PORT}" root@"${HOST}" "sha256sum '${REMOTE_DATA_DIR}/train.jsonl' | tee '${REMOTE_DATA_DIR}/SHA256SUMS'"
```

Example post-transfer verification:

```bash
ssh -p "${PORT}" root@"${HOST}" "
  test -f '${REMOTE_DATA_DIR}/train.jsonl' &&
  test \"\$(sha256sum '${REMOTE_DATA_DIR}/train.jsonl' | awk '{print \$1}')\" = '26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2' &&
  test \"\$(wc -l < '${REMOTE_DATA_DIR}/train.jsonl')\" = '10'
"
```

The future runtime evidence must record:

```text
source path used for transfer
destination path
exact transfer command
post-transfer sha256
post-transfer line count
dataset_info entry used by generated config
any data-side exception or blocker
```

## Required-Path Exceptions

Allowed input exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: existing accepted source artifact from prior data-format work. It may be used as the local/provided-workspace source input.

Future generated, temporary, staged, converted, copied, checksum sidecar, provenance sidecar, log, metadata, and intermediate artifacts should be under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Any other non-`/home/xu.yang` generated or staging path requires explicit required-path justification in the owning evidence before use.

## Data-Side Blocker Status

No current data-side blocker found.

The next parser-patch retry remains data-ready if all of the following hold:

```text
dataset_info remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
local/provided-workspace dataset is verified before transfer
remote transferred dataset is under /home/xu.yang/coding_agent_playground/outputs unless explicitly justified
remote post-transfer checksum equals accepted source checksum
```

If transfer or checksum verification fails in a future retry, treat that as a transfer/staging blocker, not a request to change dataset content.

Do not regenerate or alter the accepted ShareGPT dataset unless PM assigns a new data task with a concrete data defect.

## Completion Marker

Complete for `M1-S23-CEPHFUSE-DATA-TRANSFER-STAGING-DEV3`:

- Refreshed data/transfer staging contract after `ceph-fuse: command not found` bootstrap failure.
- Cited accepted source `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Cited sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info entry `coding_agent_m1_sft_10_sharegpt`.
- Required local/provided-workspace dataset preparation and checksum verification before transfer.
- Required future transfer/post-transfer checksum verification into `/home/xu.yang/coding_agent_playground/outputs` unless a required-path exception is justified.
- Found no current data-side blocker.
- No LTP/GPU/SFT/dry-run/eval execution performed.
