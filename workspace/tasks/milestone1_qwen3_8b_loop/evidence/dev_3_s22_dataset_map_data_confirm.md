# dev_3 Session 22 Dataset Map Data Confirmation

Task ID: `M1-S22-DATASET-MAP-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm whether the accepted ShareGPT data artifact needs content or schema changes for the post-PR39 runtime blocker:

```text
datasets.map(num_proc=4) / SyncManager EOFError
```

No SFT, GPU allocation, LTP submit, or eval was run.

## Decision

Decision: no ShareGPT data artifact content/schema change is needed for this blocker.

The next fix should be config/launcher-side single-process dataset preprocessing for the 10-row smoke, not a data conversion/regeneration task.

Reason:

- The failure is reported in multiprocessing startup/IPC for `datasets.map(num_proc=4)` with `SyncManager EOFError`.
- The runtime failed before training/checkpoint save, but after the accepted ShareGPT dataset/config path was selected.
- The old data-format signature `KeyError: from` was absent.
- The old checkpoint storage signature `ENOSPC` was absent.
- A 10-row JSONL smoke dataset does not require 4-way multiprocessing; single-process preprocessing is the safer mitigation without changing sample content.

## Accepted Source Artifact

Keep the accepted source artifact:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Checksum:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2  /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

This is an existing accepted source artifact. It may continue to be cited by path/checksum, but future materialized staging/copy/tmp data artifacts should be under `/home/xu.yang`.

## Data Contract to Preserve

```text
schema: coding_agent_playground_sft_v1_sharegpt_messages
dataset_info_entry: coding_agent_m1_sft_10_sharegpt
row_count: 10
conversation column: messages
message role key: from
message text key: value
user role value: human
assistant role value: gpt
```

Required provenance fields to preserve in any staged copy:

```text
example_id
trajectory_id
repo
task
source
```

Expected aggregate invariants remain:

```text
line_count == 10
unique_example_ids == 10
unique_trajectory_ids == 10
repo_split == {"fastapi/fastapi": 4, "scikit-learn/scikit-learn": 3, "Textualize/rich": 3}
role_values == {"human": 10, "gpt": 10}
message_keys == ["from", "value"]
```

## Runtime Evidence Interpreted

From `task_registry.md` and dev_2/test_1 durable evidence for the post-PR39 run:

```text
attempt failed during dataset conversion with multiprocessing EOFError at datasets.map(num_proc=4)
failure happened before training/checkpoint save
no complete checkpoint/model
no trainer_state.json
no all_results.json
old KeyError: from signature absent
old ENOSPC signature absent
PR39 diagnostics worked
LTP reached STOPPED (Completed)
```

Interpretation:

- The observed blocker implicates the dataset preprocessing execution mode, specifically multiprocessing manager startup/IPC.
- The evidence does not implicate the JSONL content, ShareGPT role/text keys, row count, provenance fields, or dataset_info entry.
- A content/schema change would add churn and provenance risk without addressing `SyncManager EOFError`.

## Future Staging Rule

Future staging, copy, tmp, transformed, packed, stripped, checksum sidecar, or provenance sidecar data artifacts must default under `/home/xu.yang`.

Recommended stable staging root for any future data copy:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-DATASET-MAP-DATA-CONFIRM-DEV3
```

Recommended byte-identical staged copy path, if needed:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-DATASET-MAP-DATA-CONFIRM-DEV3/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Runtime-owner run-specific staging may instead use:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Expected checksum for any byte-identical staged copy:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Allowed existing required-path exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: existing accepted source artifact from the prior data-format artifact task. It is a source-of-truth input reference, not a newly created temporary/staging/intermediate artifact.

Any other non-`/home/xu.yang` data staging path requires an explicit path and justification in the owning task evidence.

## Data-Side Blocker Status

No current data-side content/schema blocker found.

Do not regenerate or alter the accepted ShareGPT dataset for this blocker unless PM assigns a new data task with a concrete data defect.

The next retry remains data-ready if all of the following are true:

```text
dataset_info entry remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
new data staging/copy/tmp artifacts are under /home/xu.yang unless explicitly justified
preprocessing multiprocessing is reduced to single-process or otherwise fixed by the config/launcher owner
```

If a future run still fails at dataset preprocessing after single-process preprocessing, collect the new diagnostics first. Do not infer a data-content defect from the current `num_proc=4` `SyncManager EOFError`.

## Completion Marker

Complete for `M1-S22-DATASET-MAP-DATA-CONFIRM-DEV3`:

- Confirmed no ShareGPT content/schema change is needed for the `datasets.map(num_proc=4)` / `SyncManager EOFError` blocker.
- Cited accepted source `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Cited sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Preserved row count 10, schema `coding_agent_playground_sft_v1_sharegpt_messages`, dataset entry `coding_agent_m1_sft_10_sharegpt`, and provenance fields.
- Stated future staging/copy/tmp data artifacts must use `/home/xu.yang` unless explicitly justified.
- No SFT/GPU/LTP/eval execution performed.
