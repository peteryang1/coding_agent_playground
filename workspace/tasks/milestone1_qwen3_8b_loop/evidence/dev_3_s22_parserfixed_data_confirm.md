# dev_3 Session 22 Parser-Fixed Preflight Data Confirmation

Task ID: `M1-S22-PARSERFIXED-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

No-execution data confirmation after the parser-fixed preflight failed before SFT.

Confirm whether the current `FAIL_HEALTH_SIGNATURE` / storage-status blocker requires any data or dataset package change, and restate the accepted ShareGPT dataset contract.

No SFT, GPU allocation, LTP submit, dry-run, or eval was run.

## Decision

Decision: no data-side content/schema/package change is needed for the current parser-fixed preflight blocker.

The current blocker is preflight health/storage status, not data:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
SFT_ALLOWED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
```

SFT was correctly not run because parser-fixed preflight did not pass. Therefore this runtime produced no new dataset parsing, ShareGPT conversion, training, checkpoint, trainer_state, or all_results evidence that would implicate the data artifact.

The next fix path should address actionable health-signal interpretation and storage-path classification for `/home/xu.yang` artifacts, not regenerate or alter the accepted ShareGPT dataset.

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
dataset_info_name: coding_agent_m1_sft_10_sharegpt
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

## Parser-Fixed Runtime Evidence Interpreted

From current `task_registry.md`, dev_1 review, and test_1 parser-fixed runtime gate:

```text
runtime task: M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2
PR45 merge commit staged: 6f61489e85fcf7e129699061c9ddcb6e8db80926
preflight artifacts preserved under /home/xu.yang/coding_agent_playground/outputs/preflight/...
torch NCCL all-reduce exited 0
parser-fixed health status: FAIL_HEALTH_SIGNATURE
sft_allowed: false
storage status: HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS
SFT: not run
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run
LTP: STOPPED (Completed)
```

Interpretation:

- The preflight failed before SFT, so the accepted ShareGPT dataset was not newly consumed by training in this parser-fixed attempt.
- The blocker is in health/storage preflight classification and/or the selected node's actionable health signals.
- `HOME_XU_YANG_STORAGE_STATUS=FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS` is a storage-status/preflight blocker to resolve in parser/resource evidence. It does not indicate a defect in `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- No evidence points to a broken `messages[*].from/value` schema, wrong dataset_info name, wrong row count, missing provenance, or checksum drift.

## Future Temp And Staging Dataset Rule

Future temporary, staging, copied, transformed, packed, stripped, checksum sidecar, or provenance sidecar data artifacts must default under `/home/xu.yang`.

Recommended stable staging root for any future data copy:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-PARSERFIXED-DATA-CONFIRM-DEV3
```

Recommended byte-identical staged copy path, if needed:

```text
/home/xu.yang/coding_agent_playground/intermediates/milestone1_qwen3_8b_loop/M1-S22-PARSERFIXED-DATA-CONFIRM-DEV3/coding_agent_m1_sft_10_sharegpt/train.jsonl
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

Any other non-`/home/xu.yang` temp or staging dataset path requires explicit path and justification in the owning task evidence.

## Data-Side Blocker Status

No current data-side blocker found.

The parser-fixed follow-up path remains data-ready if all of the following hold:

```text
dataset_info name remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
PR41 single-process preprocessing remains active or equivalently accepted
new data temp/staging/copy artifacts are under /home/xu.yang unless explicitly justified
```

Do not regenerate or alter the accepted ShareGPT dataset for the current `FAIL_HEALTH_SIGNATURE` / storage-status blocker unless PM assigns a new data task with a concrete data defect.

## Completion Marker

Complete for `M1-S22-PARSERFIXED-DATA-CONFIRM-DEV3`:

- Confirmed current `FAIL_HEALTH_SIGNATURE` / storage-status blocker does not require data-side content/schema/package changes.
- Cited accepted source `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Cited sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info name `coding_agent_m1_sft_10_sharegpt`.
- Preserved provenance fields `example_id`, `trajectory_id`, `repo`, `task`, and `source`.
- Stated future temp/staging dataset artifacts must use `/home/xu.yang` unless explicitly justified.
- No SFT/GPU/LTP/dry-run/eval execution performed.
