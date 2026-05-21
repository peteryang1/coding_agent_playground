# dev_3 Session 22 Post-Patch Data Staging Readiness

Task ID: `M1-S22-POSTPATCH-DATA-STAGING-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Refresh ShareGPT data staging/readiness for any post-patch SFT retry under the `/home/xu.yang` intermediate-storage rule.

No SFT, GPU allocation, LTP submit, or eval was run.

## Decision

Decision: no data-side change is needed for the post-patch SFT retry.

The post-patch retry should keep the accepted ShareGPT source artifact and LLamaFactory dataset entry:

```text
source_jsonl: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row_count: 10
schema: coding_agent_playground_sft_v1_sharegpt_messages
dataset_info_entry: coding_agent_m1_sft_10_sharegpt
```

Reason:

- dev_3 prior package converted the 10 accepted trajectories to ShareGPT `messages[*].from/value`.
- test_1 accepted the artifact as LLamaFactory-compatible in the data-format gate.
- dev_2 Session 21 runtime reached dataset conversion/training progress before the ENOSPC checkpoint write failure.
- dev_2 Session 22 runtime blocker happened before durable runtime config/manifest/checkpoint artifacts were produced; it did not show a renewed data-format failure.

## Accepted Source Artifact

The accepted existing source remains:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Checksum:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2  /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

This `/root/workspace` path is an existing accepted artifact and may continue to be cited by path/checksum as the provenance source. It is not the default location for future temporary converted datasets, staging copies, SFT intermediates, or eval intermediates.

## Required Data Contract

LLamaFactory dataset entry:

```text
coding_agent_m1_sft_10_sharegpt
```

Required JSONL row contract:

```text
top-level messages: list[object]
messages[*].from: "human" or "gpt"
messages[*].value: non-empty string
```

Required provenance fields to preserve in every staged copy:

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

## Future Staging Paths Under CephFS

For any post-patch SFT retry that needs a materialized data copy, temporary conversion, stripped copy, packed copy, checksum sidecar, or provenance sidecar, use CephFS under `/home/xu.yang`.

Recommended deterministic staging root:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-POSTPATCH-DATA-STAGING-DEV3
```

Recommended paths:

```text
staged_jsonl: /home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-POSTPATCH-DATA-STAGING-DEV3/coding_agent_m1_sft_10_sharegpt/train.jsonl
checksum_sidecar: /home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-POSTPATCH-DATA-STAGING-DEV3/coding_agent_m1_sft_10_sharegpt/SHA256SUMS
provenance_sidecar: /home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-POSTPATCH-DATA-STAGING-DEV3/coding_agent_m1_sft_10_sharegpt/provenance_summary.json
tmpdir: /home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>/data
```

For a runtime-owned retry, dev_2 may also stage the same file under the run-specific output tree, provided it remains under `/home/xu.yang`, for example:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

The runtime config should continue to set:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
```

and the generated LLamaFactory config should contain:

```yaml
dataset: coding_agent_m1_sft_10_sharegpt
```

## Required Input Exceptions

Allowed existing required-path exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: existing accepted source artifact from the earlier data-format task, already referenced by durable checksum and prior gates. It may be read/cited as the source of truth, but future newly materialized staging/copy/tmp data artifacts should not default back to `/root/workspace`.

Any other non-`/home/xu.yang` data staging path is not approved by this evidence. If a future task requires one, that task must record the exact path and justification before use.

## Suggested No-GPU Staging Assertions

If a future owner creates a staged copy under `/home/xu.yang`, they should record these checks before SFT launch:

```bash
SOURCE=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
STAGED=/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-POSTPATCH-DATA-STAGING-DEV3/coding_agent_m1_sft_10_sharegpt/train.jsonl

sha256sum "${SOURCE}"
sha256sum "${STAGED}"
test "$(sha256sum "${STAGED}" | awk '{print $1}')" = "26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2"
test "$(wc -l < "${STAGED}")" = "10"
```

Expected checksum for any byte-identical staged copy:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

If a future task performs a non-byte-identical transform, such as packing or field stripping, that task must record:

```text
new path under /home/xu.yang
new sha256
new row count
exact transform
preserved provenance fields or explicit loss justification
smoke-only limitation, if applicable
```

## Data-Side Blockers

No current data-side blocker found.

Post-patch retry remains data-ready if all of the following hold:

```text
dataset entry remains coding_agent_m1_sft_10_sharegpt
source checksum remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
new staging/copy/tmp data artifacts are under /home/xu.yang unless explicitly justified
```

If these conditions fail, treat it as a staging/config regression. Do not change the dataset contract unless PM assigns a new data task.

## Completion Marker

Complete for `M1-S22-POSTPATCH-DATA-STAGING-DEV3`:

- Cited accepted source `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Cited sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Preserved row count 10 and provenance requirements.
- Specified future staging/copy/tmp dataset paths under `/home/xu.yang`.
- Recorded `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl` as an existing required source artifact exception, not a future staging default.
- Found no current data-side blocker.
- No SFT/GPU/LTP/eval execution performed.
