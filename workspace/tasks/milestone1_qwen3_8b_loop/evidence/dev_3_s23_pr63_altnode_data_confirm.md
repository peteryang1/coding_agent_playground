# dev_3 Session 23 PR63 Alternate-Node Data Confirmation

Task ID: `M1-S23-PR63-ALTNODE-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Prepare static ShareGPT data/package confirmation for the PR63 bounded alternate-node path and record whether any data/package change is currently implicated.

No LTP, GPU, SFT, eval, dry-run, transfer, or remote command was run by dev_3. This evidence uses existing durable PM/dev_2 tracking only.

## Decision

No data/package change is currently implicated for the PR63 alternate-node path.

The accepted ShareGPT artifact and LLamaFactory dataset entry remain unchanged from prior gates. The immediately prior PR63 attempts implicate node health and NCCL/NVLink runtime hardware, not data:

```text
first PR63 attempt: BLOCKED_PR63_PREFLIGHT_HEALTH_SIGNATURE_SXID_22013
different-node PR63 attempt: BLOCKED_PR63_DIFFERENTNODE_RUNTIME_NCCL_NVLINK_PEER_MEMORY
```

The PR63 alternate-node dev_2 evidence currently records reuse of the same local/provided source/data/dependency package and the same dataset checksum. If dev_2 later lands final alternate-node runtime evidence with a new data parser, dataset_info, checksum, row-count, or conversion signature, this file should be refreshed. As of this write, no such data-side signature is present.

## Accepted ShareGPT Data Contract

```text
source artifact: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
accepted sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema/version: coding_agent_playground_sft_v1_sharegpt_messages
message schema: messages[*].from / messages[*].value
role values: human / gpt
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

Required retained provenance:

```text
example_id
trajectory_id
repo
repo_path
task_id
source
metadata
artifacts
```

## Dataset Info Package

The dataset_info entry remains:

```json
{
  "coding_agent_m1_sft_10_sharegpt": {
    "file_name": "/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl",
    "formatting": "sharegpt",
    "columns": {
      "messages": "messages"
    },
    "tags": {
      "role_tag": "from",
      "content_tag": "value",
      "user_tag": "human",
      "assistant_tag": "gpt",
      "system_tag": "system",
      "observation_tag": "tool"
    }
  }
}
```

Expected LLamaFactory locations remain:

```text
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
```

This package avoids the old `KeyError: 'from'` path by keeping ShareGPT `messages[*].from/value` records and mapping the conversation column to `messages`.

## PR63 Alternate-Node Data/Package Status

Durable dev_2 alternate-node evidence currently records:

```text
runtime source commit: 7ad24ae328a350c0be596f41ea143affb4034486
source bundle sha256: 5b41b445af97e26b1f70c3853eab8fafa83608f4ea4d5e8e6856d7670f9e097c
source file count: 139
dataset: /tmp/cleaned_m1_sft_10_sharegpt_milestone1_qwen3_8b_s23_pr63_preflight_sft_20260521T181207Z/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
LLamaFactory bundle sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
current dev_2 altnode status in evidence read by dev_3: LOCAL_PACKAGE_READY_PRE_SUBMIT
```

PM task/status evidence additionally records the immediately prior PR63 different-node attempt passed placement, storage, transfer/import, preflight, and reached SFT before a CUDA/NCCL peer-memory hardware failure. That progression further supports that the accepted ShareGPT data package is not the current blocker.

## Staging and Output Rule

Future generated temporary, staged, converted, training, eval, log, metadata, and intermediate artifacts must use:

```text
/home/xu.yang/coding_agent_playground/outputs
```

The accepted source path is a required existing input exception only after checksum verification:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Remote GPU/LTP nodes remain no-external-network for project source/dependency staging. Future runtime owners should prepare local/provided bundles first, transfer by `scp`/`rsync`/tar-over-SSH, and record file lists plus checksums before any PM-authorized runtime.

## Refresh Trigger

Refresh this evidence if dev_2 final alternate-node evidence reports any of:

```text
dataset checksum mismatch
row-count mismatch
missing or wrong dataset_info entry
ShareGPT parser/conversion failure
KeyError: 'from'
messages[*].from/value schema failure
data transfer verification failure
```

## Data-Side Blocker Status

```text
data_side_blocker: none found in current PR63 altnode evidence
package_change_needed: no
refresh_needed_after_dev_2_final: only if final evidence contains a data/package signature listed above
completion_marker: STATIC_CONFIRMATION_READY_FOR_ALTNODE_REFRESH_IF_NEEDED
```
