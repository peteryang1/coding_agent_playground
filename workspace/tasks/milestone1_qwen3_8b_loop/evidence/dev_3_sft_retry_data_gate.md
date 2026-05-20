# dev_3 SFT Retry Data Gate

Task ID: `M1-SFT-RETRY-DATA-GATE-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-20

## Gate Decision

First SFT retry should use the original 10-trajectory dataset:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
```

Reason:

- PM default is original data for first retry.
- I found no concrete data-side blocker requiring repeated data before the first retry.
- The previous TP=8/DP=1 failure was a scheduler/config assertion, not a data-count failure.
- Repeated x16 data remains fallback/supporting only if the retry again hits a concrete loader/data-count blocker such as `steps_in_epoch=0`, `drop_last` eliminating batches, or an explicit minimum-sample requirement.

## Default Retry Dataset

Path:

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

Count and split:

```json
{
  "count": 10,
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
  "message_count_min": 2,
  "message_count_max": 2
}
```

Use limits:

- Acceptable as current Milestone 1 smoke SFT input.
- Not enough for quality metrics, model-quality claims, or generalization conclusions.
- If the trainer uses DP=8 with `drop_last=True`, this 10-example file can still be too small for that specific loader layout. That is a known config/data-layout interaction, not a provenance defect.

## Fallback / Supporting Dataset

Path:

```text
/root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/train.jsonl
```

Checksum:

```text
f79d1e5843541faeb9789e4c4b24b10f1e10f60002af24173a9d039bcb370d87  /root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/train.jsonl
```

Schema/version:

```text
coding_agent_playground_sft_v1
```

Count and split:

```json
{
  "count": 160,
  "unique_example_ids": 160,
  "unique_trajectory_ids": 10,
  "repo_split": {
    "fastapi/fastapi": 64,
    "scikit-learn/scikit-learn": 48,
    "Textualize/rich": 48
  },
  "status_counts": {
    "success": 160
  },
  "message_count_min": 2,
  "message_count_max": 2
}
```

Fallback use rule:

- Use only for SFT smoke loader/config validation if original data produces a concrete data-side loader blocker.
- Do not use for quality metrics, benchmark claims, or final training conclusions.
- Treat `example_id` as unique sample key.
- Treat `trajectory_id` and `source.original_trajectory_id` as original provenance, not unique expanded samples.

## Data Contract for dev_4/test_1

For the first retry:

- Use `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Assert all rows have `format_version == "coding_agent_playground_sft_v1"`.
- Read `messages` as the chat transcript.
- Preserve message order.
- Use `example_id` as sample ID.
- Keep `repo`, `task_id`, `trajectory_id`, `metadata.status`, and `source.raw_path` as metadata/provenance.
- Do not include `artifacts.stdout`, `artifacts.stderr`, or rollout logs in training text.

Acceptance checks before run:

```text
sha256(train.jsonl) == 5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
line_count == 10
unique(example_id) == 10
schema == coding_agent_playground_sft_v1
```

If switching to fallback:

```text
sha256(train.jsonl) == f79d1e5843541faeb9789e4c4b24b10f1e10f60002af24173a9d039bcb370d87
line_count == 160
unique(example_id) == 160
unique(original_trajectory_id) == 10
schema == coding_agent_playground_sft_v1
```

## Limits and Risks

- Original 10-example data may still fail under DP=8 + `drop_last=True` if config does not guarantee at least one step per rank.
- Repeated x16 data can mask a loader/batch-size issue but cannot fix scheduler/warmup/decay assertions.
- Repeated data is duplicated content and can overfit immediately.
- Neither dataset should be interpreted as enough evidence for model quality.
- Any retry report must state which dataset path and sha256 was used.

## Completion Marker

Complete for `M1-SFT-RETRY-DATA-GATE-DEV3`:

- First retry data choice gated to original `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Repeated x16 data remains fallback/supporting only.
- Checksums, schema, counts, splits, limits, risks, and loader contract recorded.
