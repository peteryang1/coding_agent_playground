# dev_3 Session 22 NCCL Data Confirmation

Task ID: `M1-S22-NCCL-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm whether the fresh post-PR41 CUDA/NCCL/NVLink runtime blocker requires any data or dataset package change.

No SFT, GPU allocation, LTP submit, dry-run, or eval was run.

## Decision

Decision: no data/package change is implicated by the fresh NCCL/NVLink blocker.

Keep the accepted ShareGPT artifact, dataset_info entry, schema, row count, and provenance contract unchanged.

Reason:

- dev_2/test_1 evidence records ShareGPT conversion completed `10/10`.
- dev_2/test_1 evidence records PR41 single-process preprocessing was active with `preprocessing_num_workers: null`.
- Training startup was reached after dataset conversion.
- The fresh blocker is CUDA/NCCL/NVLink peer GPU memory or hardware/backend failure, not JSONL parsing, dataset_info mapping, schema, row count, or provenance.
- Old data-side/runtime signatures were absent: `KeyError: from`, `datasets.map(num_proc=4)` / `SyncManager EOFError`, and ENOSPC did not recur.

## Accepted Source Artifact

Keep the accepted source artifact:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Checksum:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2  /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

This is an existing accepted source artifact. It may continue to be cited by path/checksum as the source of truth, but future temporary/staging/intermediate data artifacts must default under `/home/xu.yang`.

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

Expected aggregate invariants:

```text
line_count == 10
unique_example_ids == 10
unique_trajectory_ids == 10
repo_split == {"fastapi/fastapi": 4, "scikit-learn/scikit-learn": 3, "Textualize/rich": 3}
role_values == {"human": 10, "gpt": 10}
message_keys == ["from", "value"]
```

## Runtime Evidence Interpreted

From `task_registry.md`, `evidence/dev_2_s22_postpr41_sft_runtime.md`, and `evidence/test_1_s22_postpr41_runtime_gate.md`:

```text
PR41 merge commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
preprocessing_num_workers: null
ShareGPT conversion: 10/10
training startup: reached
fresh blocker: CUDA/NCCL Invalid access of peer GPU memory over nvlink or a hardware error
local rank: 5 SIGABRT
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
old KeyError: from: absent
old datasets.map(num_proc=4) SyncManager EOFError: absent
old ENOSPC: absent
LTP status: STOPPED (Completed)
```

Interpretation:

- Data loading/conversion succeeded for the accepted 10-row ShareGPT artifact.
- PR41's single-process preprocessing setting cleared the prior `datasets.map(num_proc=4)` multiprocessing blocker.
- The new failure occurs in distributed CUDA/NCCL/NVLink runtime behavior after data conversion, so changing data content, ShareGPT schema, or dataset_info mapping would not address the observed blocker.

## Future Staging Rule

Future staging, copy, tmp, transformed, packed, stripped, checksum sidecar, or provenance sidecar data artifacts must default under `/home/xu.yang`.

Recommended stable staging root for any future data copy:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-NCCL-DATA-CONFIRM-DEV3
```

Recommended byte-identical staged copy path, if needed:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-NCCL-DATA-CONFIRM-DEV3/coding_agent_m1_sft_10_sharegpt/train.jsonl
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

Justification: existing accepted source artifact from prior data-format work. It is a source-of-truth input reference, not a newly created temporary/staging/intermediate artifact.

Any other non-`/home/xu.yang` data staging path requires explicit path and justification in the owning task evidence.

## Data-Side Blocker Status

No current data-side content/schema/package blocker found.

The next retry remains data-ready if all of the following are true:

```text
dataset_info entry remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
PR41 single-process preprocessing remains active or equivalently accepted
new data staging/copy/tmp artifacts are under /home/xu.yang unless explicitly justified
```

Do not regenerate or alter the accepted ShareGPT dataset for the NCCL/NVLink blocker unless PM assigns a new data task with a concrete data defect.

## Completion Marker

Complete for `M1-S22-NCCL-DATA-CONFIRM-DEV3`:

- Confirmed no ShareGPT data/package change is implicated by the CUDA/NCCL/NVLink blocker.
- Cited accepted source `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Cited sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Preserved row count 10, schema `coding_agent_playground_sft_v1_sharegpt_messages`, dataset entry `coding_agent_m1_sft_10_sharegpt`, and provenance fields.
- Cited dev_2/test_1 facts: ShareGPT conversion `10/10`, `preprocessing_num_workers: null`, and training startup reached.
- Stated future staging/copy/tmp data artifacts must use `/home/xu.yang` unless explicitly justified.
- No SFT/GPU/LTP/dry-run/eval execution performed.
