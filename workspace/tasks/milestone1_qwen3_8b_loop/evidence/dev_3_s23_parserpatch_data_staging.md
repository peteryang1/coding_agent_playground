# dev_3 Session 23 Parser-Patch Data Staging Confirmation

Task ID: `M1-S23-PARSERPATCH-DATA-STAGING-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm the accepted ShareGPT dataset and future data staging remain compatible with the parser-patch retry.

No SFT, GPU allocation, LTP submit, dry-run, or eval was run.

## Decision

Decision: the accepted ShareGPT dataset remains compatible with the parser-patch retry.

No data-side content, schema, checksum, row-count, or dataset_info change is needed for the Session 23 parser patch path.

Reason:

- The parser-patch work targets preflight parser behavior: stale-vs-actionable Xid/SXid classification and `/home/xu.yang` storage-path normalization.
- The previous parser-fixed failure happened before SFT and did not produce a data parsing, ShareGPT conversion, training, checkpoint, trainer_state, or all_results failure.
- The accepted ShareGPT artifact and dataset_info contract have already cleared prior data-format gates and should be preserved.

## Accepted Source Artifact

Accepted source:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Checksum:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2  /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

This is an existing accepted source artifact. It may continue to be cited by path/checksum as the source of truth.

## Accepted Dataset Contract

```text
schema: coding_agent_playground_sft_v1_sharegpt_messages
dataset_info: coding_agent_m1_sft_10_sharegpt
row_count: 10
conversation column: messages
message object keys: from, value
message role key: messages[*].from
message text key: messages[*].value
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

Expected aggregate invariants:

```text
line_count == 10
unique_example_ids == 10
unique_trajectory_ids == 10
repo_split == {"fastapi/fastapi": 4, "scikit-learn/scikit-learn": 3, "Textualize/rich": 3}
role_values == {"human": 10, "gpt": 10}
message_keys == ["from", "value"]
```

## Parser-Patch Compatibility

The parser-patch retry should keep using:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
generated_config.dataset=coding_agent_m1_sft_10_sharegpt
source_dataset=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
source_sha256=26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Data is not implicated by the parser-patch scope:

- stale historical Xid/SXid parsing is a preflight health-parser concern;
- `/home/xu.yang` vs resolved `/mnt/cephfs/home/xu.yang` normalization is a generated-artifact path classification concern;
- neither requires changing the accepted JSONL content or LLamaFactory dataset_info name.

If a future parser-patch preflight passes and PM authorizes SFT, the runtime owner should stage/copy data without altering the byte content unless PM assigns a new data task.

## Future Storage And Staging Rule

Future temporary, staged, converted, copied, packed, stripped, checksum sidecar, provenance sidecar, data logs, data metadata, run metadata, and other data/intermediate artifacts must default under `/home/xu.yang`.

Recommended stable data staging root:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S23-PARSERPATCH-DATA-STAGING-DEV3
```

Recommended byte-identical staged dataset path, if needed:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S23-PARSERPATCH-DATA-STAGING-DEV3/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Recommended sidecar paths:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S23-PARSERPATCH-DATA-STAGING-DEV3/coding_agent_m1_sft_10_sharegpt/SHA256SUMS
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S23-PARSERPATCH-DATA-STAGING-DEV3/coding_agent_m1_sft_10_sharegpt/provenance_summary.json
```

Runtime-owner run-specific staging may instead use:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Tmp dataset paths should remain under:

```text
/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>/data
```

Data logs, data metadata, and run metadata should remain under:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/
```

Expected checksum for any byte-identical staged copy:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Allowed existing required-path exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: existing accepted source artifact from prior data-format work. It is a source-of-truth input reference, not a newly created temporary/staged/converted data artifact.

Any other non-`/home/xu.yang` temporary, staged, converted, log, metadata, or intermediate path requires explicit path and required-path justification in the owning task evidence before use.

## Data-Side Blocker Status

No current data-side blocker found for the parser-patch retry.

The parser-patch retry remains data-ready if all of the following hold:

```text
dataset_info remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
new temporary/staged/converted data artifacts are under /home/xu.yang unless explicitly justified
data logs, metadata, and intermediates are under /home/xu.yang unless explicitly justified
```

Do not regenerate or alter the accepted ShareGPT dataset for the parser-patch path unless PM assigns a new data task with a concrete data defect.

## Completion Marker

Complete for `M1-S23-PARSERPATCH-DATA-STAGING-DEV3`:

- Confirmed accepted ShareGPT dataset remains compatible with parser-patch retry.
- Cited accepted source `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Cited sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info `coding_agent_m1_sft_10_sharegpt`.
- Preserved provenance fields `example_id`, `trajectory_id`, `repo`, `task`, and `source`.
- Stated future temp/staged/converted data, logs, metadata, and intermediates must use `/home/xu.yang` unless a required-path exception is justified.
- No SFT/GPU/LTP/dry-run/eval execution performed.
