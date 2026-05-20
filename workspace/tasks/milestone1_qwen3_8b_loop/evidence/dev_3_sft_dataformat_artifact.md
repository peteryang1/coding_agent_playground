# dev_3 SFT Data Format Artifact

Task ID: `M1-SFT-DATAFORMAT-ARTIFACT-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-20

## Scope

Produce concrete no-GPU data-format artifact/preflight evidence for the retry failure:

```text
KeyError: 'from'
```

No SFT, GPU allocation, or eval was run.

## Chosen Mode

Chosen mode: fallback ShareGPT converted JSONL artifact.

Reason:

- The failing path expected `messages[*].from` / `messages[*].value`.
- The current dataset has OpenAI-style `messages[*].role` / `messages[*].content`.
- A concrete ShareGPT artifact removes the missing `from` field directly and does not depend on LLamaFactory version-specific dataset_info tag support.

## Source Artifact

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
```

Source checksum:

```text
5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054  /root/workspace/cleaned_m1_sft_10/train.jsonl
```

Source schema:

```text
coding_agent_playground_sft_v1
```

## Generated Artifact Paths

Corrected host:

```text
ssh -p 31787 root@10.100.194.40
```

Paths:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
/root/workspace/cleaned_m1_sft_10_sharegpt/conversion_summary.json
/root/workspace/cleaned_m1_sft_10_sharegpt/convert_openai_to_sharegpt.py
```

Checksums:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2  /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
825f2116168e76158f344768293eff2957ca6217d69ad9a56608275830457ec1  /root/workspace/cleaned_m1_sft_10_sharegpt/conversion_summary.json
c343bdbe9ab6373ccc2263c673619471c425eab72cb7ed24d25f4562b71e29a3  /root/workspace/cleaned_m1_sft_10_sharegpt/convert_openai_to_sharegpt.py
```

Output schema/version:

```text
coding_agent_playground_sft_v1_sharegpt_messages
```

## Deterministic Command / Script

Run on corrected host:

```bash
python3 /root/workspace/cleaned_m1_sft_10_sharegpt/convert_openai_to_sharegpt.py
```

Script behavior:

- Reads `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Copies each row.
- Sets `format_version` to `coding_agent_playground_sft_v1_sharegpt_messages`.
- Converts every message:
  - `role=user` -> `from=human`
  - `role=assistant` -> `from=gpt`
  - `role=system` -> `from=system`
  - `role=tool` -> `from=tool`
  - `content` -> `value`
- Preserves top-level `example_id`, `trajectory_id`, `repo`, `task_id`, `source`, `metadata`, and `artifacts`.
- Adds source provenance:
  - `source.source_format_version`
  - `source.dataformat_mitigation`
  - `source.source_train_path`
- Writes deterministic JSONL with sorted keys.
- Writes `conversion_summary.json`.

## Counts

```json
{
  "row_count": 10,
  "unique_example_ids": 10,
  "unique_trajectory_ids": 10,
  "repo_split": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {
    "success": 10
  },
  "role_values": {
    "human": 10,
    "gpt": 10
  }
}
```

## Sample Assertions

Validation result:

```json
{
  "row_count": 10,
  "unique_example_ids": 10,
  "unique_trajectory_ids": 10,
  "task_count": 10,
  "message_key_sets": [["from", "value"]],
  "assertion_errors": []
}
```

First sample:

```json
{
  "example_id": "fastapi__fastapi_complete_edit_001",
  "trajectory_id": "fastapi__fastapi_complete_edit_001",
  "repo": "fastapi/fastapi",
  "task_id": "fastapi_complete_edit_001",
  "messages": [
    {
      "from": "human",
      "value": "Milestone 1 high-quality coding trajectory. In /root/workspace/fastapi, make a minimal real code edit related to routing or endpoint metadata..."
    },
    {
      "from": "gpt",
      "value": "**Requirements Understanding**\\nYou asked for a minimal real code edit in `/root/workspace/fastapi` related to routing or endpoint metadata..."
    }
  ]
}
```

## Provenance Preservation

Preserved exactly from the source rows:

- `example_id`
- `trajectory_id`
- `repo`
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

Added provenance:

```json
{
  "source_format_version": "coding_agent_playground_sft_v1",
  "dataformat_mitigation": "openai_role_content_to_sharegpt_from_value",
  "source_train_path": "/root/workspace/cleaned_m1_sft_10/train.jsonl"
}
```

## How This Avoids `KeyError: 'from'`

The previous failure occurs when LLamaFactory's ShareGPT conversion reads each message and expects `message["from"]`.

This artifact guarantees:

- every message object has exactly `from` and `value`;
- every user message uses `from=human`;
- every assistant message uses `from=gpt`;
- no training message depends on `role` or `content` for the ShareGPT reader.

Therefore the failing `message["from"]` lookup should find the expected key.

## Use Contract for dev_4/test_1

If PM gates a data-format-fixed retry with this artifact:

```text
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Pre-run assertions:

```text
sha256 == 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
line_count == 10
unique(example_id) == 10
unique(trajectory_id) == 10
all messages[*] keys == {"from", "value"}
role_values == {"human": 10, "gpt": 10}
```

LLamaFactory registration should use ShareGPT defaults for `from`/`value`, or explicitly map role/content tags to `from`/`value`.

## Risks

- This fixes only the data-format mismatch. It does not prove SFT will complete.
- Scheduler, Megatron/MCA config, GPU resource, or launcher failures can still occur.
- The output schema is a derived schema, `coding_agent_playground_sft_v1_sharegpt_messages`, so reports must name this exact path and checksum.
- If LLamaFactory expects a messages-only record and rejects extra top-level metadata, dev_4 may need a second stripped artifact; this file intentionally preserves provenance first.

## Completion Marker

Complete for `M1-SFT-DATAFORMAT-ARTIFACT-DEV3`:

- Concrete ShareGPT artifact generated.
- Deterministic script path and checksum recorded.
- Row count, checksums, sample assertions, provenance preservation, and `KeyError: 'from'` avoidance documented.
- No SFT/GPU/eval execution performed.
