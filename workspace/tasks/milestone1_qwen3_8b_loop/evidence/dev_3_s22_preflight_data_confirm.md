# dev_3 Session 22 Preflight Parser Data Confirmation

Task ID: `M1-S22-PREFLIGHT-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm the preflight health-parser fix path does not require data or dataset package changes, and restate the accepted ShareGPT dataset contract for any future retry.

No SFT, GPU allocation, LTP submit, dry-run, or eval was run.

## Decision

Decision: no data/package change is needed for the parser-fix path.

The current blocker is a preflight health-parser false-positive/signature-classification problem:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
```

The preflight evidence indicates the health scan matched evidence/command/process/generic text too broadly. SFT was correctly not run because preflight did not pass. This is not a JSONL content, ShareGPT schema, dataset_info mapping, row count, or provenance issue.

Keep the accepted ShareGPT artifact and dataset package unchanged.

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
dataset_info_entry: coding_agent_m1_sft_10_sharegpt
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

## Parser-Fix Interpretation

From current milestone registry and gate evidence:

```text
preflight allocation used /home/xu.yang artifacts
capacity probe passed and cleaned
topology/NVLink evidence was captured
torch 8-rank NCCL all-reduce exited 0
final preflight marker was PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
SFT was not run
no checkpoint/model exists
no trainer_state.json exists
no all_results.json exists
next PM path is preflight health-parser refinement
```

Interpretation:

- The parser fix should refine which preflight logs/process/evidence text count as actionable hardware/NCCL faults.
- It should not alter the accepted ShareGPT dataset content, schema, dataset_info entry, checksum, or provenance contract.
- If a future parser-fixed preflight passes and SFT is authorized, the runtime should continue to use `coding_agent_m1_sft_10_sharegpt` and the accepted 10-row ShareGPT source artifact.

## Future Staging And Tmp Dataset Rule

Future temporary, staging, copied, transformed, packed, stripped, checksum sidecar, or provenance sidecar data artifacts must default under `/home/xu.yang`.

Recommended stable staging root for any future data copy:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-PREFLIGHT-DATA-CONFIRM-DEV3
```

Recommended byte-identical staged copy path, if needed:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-PREFLIGHT-DATA-CONFIRM-DEV3/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Runtime-owner run-specific staging may instead use:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Tmp dataset path should remain under:

```text
/home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>/data
```

Expected checksum for any byte-identical staged copy:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Allowed existing required-path exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: existing accepted source artifact from prior data-format work. It is a source-of-truth input reference, not a newly created temporary/staging/intermediate artifact.

Any other non-`/home/xu.yang` data staging or tmp path requires explicit path and justification in the owning task evidence.

## Data-Side Blocker Status

No current data-side content/schema/package blocker found.

The parser-fix path remains data-ready if all of the following are true:

```text
dataset_info entry remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
PR41 single-process preprocessing remains active or equivalently accepted
new data staging/copy/tmp artifacts are under /home/xu.yang unless explicitly justified
```

Do not regenerate or alter the accepted ShareGPT dataset for the parser-fix blocker unless PM assigns a new data task with a concrete data defect.

## Completion Marker

Complete for `M1-S22-PREFLIGHT-DATA-CONFIRM-DEV3`:

- Confirmed parser-fix path does not require ShareGPT data/package changes.
- Cited accepted source `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Cited sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10 and `messages[*].from/value` ShareGPT schema.
- Preserved dataset entry `coding_agent_m1_sft_10_sharegpt` and provenance fields.
- Stated future staging/tmp data artifacts must use `/home/xu.yang` unless explicitly justified.
- No SFT/GPU/LTP/dry-run/eval execution performed.
