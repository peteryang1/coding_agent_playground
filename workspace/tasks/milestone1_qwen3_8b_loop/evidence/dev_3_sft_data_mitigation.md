# dev_3 SFT Data Mitigation Evidence

Task ID: `M1-SFT-DATA-MITIGATION-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-20

## Scope

Evaluate data-side mitigations for the SFT tiny-data failure without adding new trajectories:

- repetition;
- packing/loader-safe expansion;
- or explicit rejection of data-side fix.

## Failure Context

From `evidence/dev_4_sft_smoke_run.md`:

- Baseline SFT with `/root/workspace/cleaned_m1_sft_10/train.jsonl` loaded 10 examples, initialized 8 distributed tasks, entered training, then failed with `ZeroDivisionError` from `steps_in_epoch=0`.
- dev_4 interpretation: MCA trainer uses `drop_last=True`; with 10 examples and baseline DP=8 layout, the tiny smoke dataset yields zero effective steps per epoch on ranks.
- TP=8/DP=1 bounded retry with `max_steps=1` failed with Megatron scheduler assertion `lr_warmup_steps < lr_decay_steps`; this is config-side, not solved by data repetition alone.

## Original Provenance

Original SFT smoke input:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
```

Checksum:

```text
5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054  /root/workspace/cleaned_m1_sft_10/train.jsonl
```

Original count and split:

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

Original trajectory IDs:

```text
fastapi__fastapi_complete_edit_001
fastapi__fastapi_complete_edit_002
fastapi__fastapi_complete_edit_003
fastapi__fastapi_complete_edit_004
rich__rich_complete_edit_001
rich__rich_complete_edit_002
rich__rich_complete_edit_003
scikit-learn__sklearn_complete_edit_001
scikit-learn__sklearn_complete_edit_002
scikit-learn__sklearn_complete_edit_003
```

## Mitigation Decision

Data-side repetition is acceptable for an SFT smoke run only.

It is not acceptable for model quality evaluation, generalization claims, benchmark reporting, or final training-quality conclusions.

Reasoning:

- The observed baseline data-side failure is consistent with too few examples under DP=8 plus `drop_last=True`.
- Repeating the existing 10 trajectories can create enough loader-visible samples to avoid zero-step epochs without inventing new trajectory content.
- This preserves the original 10-trajectory provenance if every repeated row carries original ID metadata.
- It does not address scheduler assertions from a 1-step TP=8/DP=1 config. dev_4 still owns config-side mitigation for scheduler-safe step counts/warmup/decay.

## Generated Artifact

Generated on corrected final workspace:

```text
ssh -p 31787 root@10.100.194.40
```

Output:

```text
/root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/train.jsonl
/root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/mitigation_summary.json
```

Checksums:

```text
f79d1e5843541faeb9789e4c4b24b10f1e10f60002af24173a9d039bcb370d87  /root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/train.jsonl
7a93f053974c3ead13dc8a122053f9d75371d7f3a74b93c9a7a32132a5767b49  /root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/mitigation_summary.json
```

Schema:

```text
coding_agent_playground_sft_v1
```

Expansion summary:

```json
{
  "mitigation": "repeat_smoke_x16",
  "repeat_factor": 16,
  "original_count": 10,
  "expanded_count": 160,
  "unique_original_trajectory_ids": 10,
  "unique_expanded_example_ids": 160,
  "repo_split_original": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "repo_split_expanded": {
    "fastapi/fastapi": 64,
    "scikit-learn/scikit-learn": 48,
    "Textualize/rich": 48
  },
  "status_counts_expanded": {
    "success": 160
  }
}
```

Provenance preservation:

- `trajectory_id` remains the original trajectory ID.
- `example_id` is made unique as `<original_example_id>__repeat_XX`.
- `source.original_example_id` records the original example ID.
- `source.original_trajectory_id` records the original trajectory ID.
- `source.mitigation` is `repeat_smoke_x16`.
- `source.repeat_index` and `source.repeat_factor` record repeat placement.
- `metadata.original_example_id`, `metadata.original_trajectory_id`, `metadata.is_repeated_smoke_sample`, and `metadata.repeat_index` mirror the provenance for loaders/manifests.

## Validation

Validation result for generated artifact:

```json
{
  "rows": 160,
  "unique_example_ids": 160,
  "unique_original_trajectory_ids": 10,
  "repo_split": {
    "fastapi/fastapi": 64,
    "scikit-learn/scikit-learn": 48,
    "Textualize/rich": 48
  },
  "status_counts": {
    "success": 160
  },
  "schema_errors": [],
  "defects": []
}
```

## Data Contract for dev_4

If PM/dev_4 choose a data-side smoke retry, use:

```text
/root/workspace/cleaned_m1_sft_10_repeated_smoke_x16/train.jsonl
```

Loader expectations:

- Read as JSONL.
- Require `format_version == "coding_agent_playground_sft_v1"`.
- Use `messages` as the training conversation.
- Preserve message order.
- Treat `trajectory_id` as original trajectory provenance, not as a unique sample key.
- Use `example_id` as the unique sample key.
- Keep `source.original_trajectory_id` and `metadata.original_trajectory_id` in run manifests if possible.
- Do not mix this repeated smoke dataset into any metric-bearing evaluation or final training report without labeling it as repeated smoke data.

Recommended loader assertions:

```text
line_count == 160
unique(example_id) == 160
unique(source.original_trajectory_id) == 10
sha256(train.jsonl) == f79d1e5843541faeb9789e4c4b24b10f1e10f60002af24173a9d039bcb370d87
```

## Risks

- Repetition may overfit immediately; loss curves are not meaningful as quality evidence.
- Repetition does not add code/task diversity and must not be counted as 160 independent trajectories.
- Repetition may mask a config bug by creating enough batches, while scheduler/warmup/decay issues still require dev_4 config fixes.
- Keeping original `trajectory_id` repeated across rows may confuse loaders that require globally unique trajectory IDs; dev_4 should use `example_id` as sample ID.
- If the training stack deduplicates by `trajectory_id` or message content, this mitigation may not increase effective sample count.
- If global batch size or `drop_last` requirements exceed 160 examples, repeat factor may still be too small; dev_4 should confirm expected global batch and steps before requesting another artifact.

## Completion Marker

Complete for `M1-SFT-DATA-MITIGATION-DEV3`:

- Original 10-trajectory provenance preserved.
- Repeated smoke-only artifact generated.
- Exact path, schema, count, checksum, validation result, acceptability, and risks recorded.
- No current data-side blocker for a smoke-only retry using the repeated artifact; remaining scheduler/config retry gate belongs to dev_4/test_1/PM.
