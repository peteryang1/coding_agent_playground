# dev_3 Session 21 LLamaFactory Dataset Info Package

Task ID: `M1-S21-DATASETINFO-PACKAGE-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Produce exact LLamaFactory `dataset_info.json` package evidence for the accepted ShareGPT artifact.

No SFT, GPU allocation, or eval was run.

## Accepted Artifact

Corrected host:

```text
ssh -p 31787 root@10.100.194.40
```

Dataset path:

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

Data schema:

```text
coding_agent_playground_sft_v1_sharegpt_messages
```

Verified split and message shape:

```json
{
  "row_count": 10,
  "repo_split": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "role_values": {
    "human": 10,
    "gpt": 10
  },
  "unique_example_ids": 10,
  "unique_trajectory_ids": 10,
  "message_keys": ["from", "value"],
  "assertion_errors": []
}
```

## Dataset Info Entry

Entry name:

```text
coding_agent_m1_sft_10_sharegpt
```

Exact `dataset_info.json` entry body:

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

Required mapping:

- Conversation column: `messages`
- Message role key: `from`
- Message text key: `value`
- Human/user role value: `human`
- Assistant role value: `gpt`
- Optional system role value: `system`
- Optional tool/observation role value: `tool`

## Exact File / Config Locations for dev_2

dev_2 should package or stage the dataset entry at these locations for the next GPU worker handoff:

```text
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
```

If the GPU worker is newly allocated, dev_2 should ensure the following files are present on that worker before dev_4 launch:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
/root/workspace/cleaned_m1_sft_10_sharegpt/conversion_summary.json
/root/workspace/cleaned_m1_sft_10_sharegpt/convert_openai_to_sharegpt.py
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
```

The dataset entry may be added to both LLamaFactory dataset info files to avoid the prior path ambiguity where `data/sft/dataset_info.json` was required by the launcher.

Suggested dataset name for dev_4 config/command:

```text
coding_agent_m1_sft_10_sharegpt
```

Suggested dataset path env if the launcher still takes `DATASET_JSONL`:

```text
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

## Retained Provenance Fields

The ShareGPT artifact keeps these fields from the original `coding_agent_playground_sft_v1` rows:

- `example_id`
- `trajectory_id`
- `repo`
- `repo_path`
- `task_id`
- `source.raw_path`
- `source.run_dir`
- `metadata.repo_commit`
- `metadata.status`
- `metadata.changed_files`
- `metadata.tests`
- `artifacts.last_message`
- `artifacts.stdout`
- `artifacts.stderr`

Added data-format provenance:

```json
{
  "source_format_version": "coding_agent_playground_sft_v1",
  "dataformat_mitigation": "openai_role_content_to_sharegpt_from_value",
  "source_train_path": "/root/workspace/cleaned_m1_sft_10/train.jsonl"
}
```

## How This Avoids `KeyError: 'from'`

The failed retry used data where each message had:

```json
{"role": "user", "content": "..."}
```

The LLamaFactory ShareGPT conversion path expected:

```json
{"from": "human", "value": "..."}
```

This package avoids `KeyError: 'from'` because:

- every training message in `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl` has a `from` key;
- every training message also has a `value` key;
- the `dataset_info.json` entry explicitly maps `role_tag` to `from` and `content_tag` to `value`;
- role values match ShareGPT conventions: `human` and `gpt`.

## Pre-Launch Assertions for dev_2/dev_4/test_1

Before any SFT retry, verify:

```text
sha256sum /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
# expected: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2

wc -l /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
# expected: 10
```

Record check:

```text
all rows have format_version == coding_agent_playground_sft_v1_sharegpt_messages
all rows have messages as a non-empty list
all messages have exactly from/value keys
role value set is human/gpt for current data
unique(example_id) == 10
unique(trajectory_id) == 10
```

Config check:

```text
dataset_info contains entry coding_agent_m1_sft_10_sharegpt
entry file_name == /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
entry formatting == sharegpt
entry columns.messages == messages
entry tags.role_tag == from
entry tags.content_tag == value
entry tags.user_tag == human
entry tags.assistant_tag == gpt
```

## Risks / Limits

- This package fixes the `from`/`value` data-format blocker only. It does not guarantee training completion.
- Scheduler, MCA/Megatron, launcher, GPU, or dependency failures can still happen.
- If the deployed LLamaFactory version has different `dataset_info.json` tag names, dev_4/test_1 must adapt to that version before launch and record the exact resolved mapping.
- Extra provenance top-level fields are intentionally retained. If LLamaFactory rejects extra keys, the next data task should produce a stripped ShareGPT-only artifact while preserving an external provenance manifest.

## Completion Marker

Complete for `M1-S21-DATASETINFO-PACKAGE-DEV3`:

- Exact dataset entry name/body provided.
- Conversation/message mapping to `messages[*].from/value` provided.
- Exact artifact and config locations for dev_2 provided.
- Checksums/counts and provenance fields recorded.
- Explanation for avoiding `KeyError: 'from'` recorded.
- No SFT/GPU/eval execution performed.
