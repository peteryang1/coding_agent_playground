# dev_3 SFT Data Format Fix Plan

Task ID: `M1-SFT-DATAFORMAT-FIX-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-20

## Scope

Produce a no-execution SFT unblock plan for the retry failure:

```text
KeyError: 'from'
```

No SFT, GPU, or eval commands were run for this task.

## Current Blocker

The authorized retry reached LLamaFactory dataset conversion and failed with `KeyError: 'from'`.

Exact mismatch:

- Current Milestone 1 data is `coding_agent_playground_sft_v1`.
- Records store chat messages as OpenAI-style objects:
  - `role`
  - `content`
- The failing LLamaFactory conversion path was reading the dataset as ShareGPT-style conversations and expected message objects with:
  - `from`
  - `value`
- Therefore the converter tried to access `message["from"]` and failed on our `message["role"]` records.

This is a dataset registration/format mapping mismatch, not evidence that the 10 trajectories are corrupt.

## Current Input Contract

Default retry input:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
```

Checksum:

```text
5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054  /root/workspace/cleaned_m1_sft_10/train.jsonl
```

Schema/version:

```text
coding_agent_playground_sft_v1
```

Count/split:

```json
{
  "count": 10,
  "repo_split": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {
    "success": 10
  }
}
```

## Preferred Fix: LLamaFactory OpenAI role/content Registration

Preferred path: keep `/root/workspace/cleaned_m1_sft_10/train.jsonl` unchanged and register it in LLamaFactory as an OpenAI-style messages dataset.

Rationale:

- Preserves the existing `coding_agent_playground_sft_v1` artifact and checksum.
- Avoids creating a second canonical training file.
- Keeps current evidence paths, provenance, repo split, and validation unchanged.
- Fixes the exact mismatch by telling LLamaFactory to read `messages[*].role` and `messages[*].content`.

Planned dataset registration shape:

```json
{
  "coding_agent_m1_sft_10_openai": {
    "file_name": "/root/workspace/cleaned_m1_sft_10/train.jsonl",
    "formatting": "sharegpt",
    "columns": {
      "messages": "messages"
    },
    "tags": {
      "role_tag": "role",
      "content_tag": "content",
      "user_tag": "user",
      "assistant_tag": "assistant",
      "system_tag": "system",
      "observation_tag": "tool"
    }
  }
}
```

Notes for dev_4/test_1:

- Confirm the exact LLamaFactory version accepts custom `tags` names for ShareGPT formatting.
- If the local LLamaFactory build has an explicit OpenAI/alpaca/messages formatting mode, prefer its official field names over this generic mapping, but the contract remains: `messages` list, `role` role field, `content` text field.
- The gate should inspect the resolved `dataset_info.json` on the GPU node before launching SFT.

Expected post-fix condition:

- LLamaFactory dataset conversion no longer attempts `message["from"]` on this dataset.
- Logs should not contain `KeyError: 'from'`.
- Dataset should still load 10 examples from `/root/workspace/cleaned_m1_sft_10/train.jsonl`.

## Fallback Fix: ShareGPT from/value Converted JSONL

Fallback path: create a derived JSONL that converts only the message wrapper keys:

- `role=user` -> `from=human`
- `role=assistant` -> `from=gpt`
- `role=system` -> `from=system`
- `role=tool` -> `from=tool`
- `content` -> `value`

All other top-level fields should be preserved for provenance unless LLamaFactory requires a messages-only file.

Proposed fallback path:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Proposed fallback schema/version marker:

```text
coding_agent_playground_sft_v1_sharegpt_messages
```

Checksum plan:

- Do not invent a checksum in this no-execution plan.
- If PM gates fallback generation, dev_3 should write the converted artifact, then record:
  - row count;
  - sha256 of `train.jsonl`;
  - conversion summary path;
  - first/last sample validation;
  - unique `example_id` / `trajectory_id` counts;
  - repo split.

Expected fallback count:

```json
{
  "count": 10,
  "unique_example_ids": 10,
  "unique_trajectory_ids": 10,
  "repo_split": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  }
}
```

## Sample Records

Before: current OpenAI-style `coding_agent_playground_sft_v1` message shape:

```json
{
  "example_id": "fastapi__fastapi_complete_edit_001",
  "messages": [
    {
      "role": "user",
      "content": "Milestone 1 high-quality coding trajectory. In /root/workspace/fastapi, make a minimal real code edit related to routing or endpoint metadata..."
    },
    {
      "role": "assistant",
      "content": "**Requirements Understanding**\\nYou asked for a minimal real code edit in `/root/workspace/fastapi` related to routing or endpoint metadata..."
    }
  ]
}
```

After, preferred path: no data rewrite; LLamaFactory registration maps:

```json
{
  "messages": "messages",
  "role_tag": "role",
  "content_tag": "content",
  "user_tag": "user",
  "assistant_tag": "assistant"
}
```

After, fallback ShareGPT-converted message shape:

```json
{
  "example_id": "fastapi__fastapi_complete_edit_001",
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

## Validation Plan

Before any new SFT retry, test_1/dev_4 should verify one of these gates:

Preferred registration gate:

```text
dataset_info entry exists for /root/workspace/cleaned_m1_sft_10/train.jsonl
entry maps messages -> messages
entry maps role field -> role
entry maps content field -> content
sample row has messages[0].role and messages[0].content
dry dataset parse or preflight conversion does not raise KeyError: 'from'
```

Fallback conversion gate:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl exists
line_count == 10
unique(example_id) == 10
unique(trajectory_id) == 10
every messages[*] has from/value
no messages[*] relies on role/content for LLamaFactory conversion
sha256 recorded after generation
```

## Risks

- LLamaFactory version-specific dataset_info keys may differ. dev_4/test_1 must confirm exact supported field names before another GPU run.
- If LLamaFactory ignores custom tags and still uses default ShareGPT keys, preferred registration will still fail with `KeyError: 'from'`; then fallback conversion should be used.
- Fallback conversion creates a second training artifact; reports must clearly identify which path and checksum was used.
- A messages-only fallback file could lose top-level provenance unless we preserve `example_id`, `trajectory_id`, `repo`, `task_id`, and `source` fields.
- Fixing `KeyError: 'from'` does not guarantee SFT success; scheduler, Megatron/MCA tiny-data, or GPU resource blockers can still occur.

## Recommendation

Use the preferred registration fix first if dev_4/test_1 can confirm LLamaFactory supports role/content tag mapping in the deployed version.

Use fallback ShareGPT conversion only if:

- the deployed LLamaFactory cannot map role/content fields; or
- a local preflight still produces `KeyError: 'from'` after registration.

## Completion Marker

Complete for `M1-SFT-DATAFORMAT-FIX-DEV3`:

- Exact mismatch identified.
- Preferred OpenAI role/content registration plan provided.
- Fallback ShareGPT from/value conversion plan provided.
- Sample before/after records included.
- Schema/version, row count/checksum plan, validation gate, and risks recorded.
- No SFT/GPU/eval execution performed.
