# dev_3 Session 21 ENOSPC Data Confirmation

Task ID: `M1-S21-ENOSPC-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm the next retry should keep the same ShareGPT data contract and that no data-side change is needed for the Session 21 ENOSPC failure.

No SFT, GPU allocation, or eval was run.

## Data Decision

Decision: keep the same ShareGPT dataset and dataset_info contract for the next retry.

No data-side change is needed for ENOSPC.

Reason:

- The Session 21 runtime passed the prior data-format blocker.
- The runtime reached ShareGPT conversion and training progress.
- The final failure was safetensors checkpoint serialization ENOSPC, not dataset parsing, schema, or data loading.

Storage rule update from supervisor:

- The accepted ShareGPT source path below may continue to be referenced as an existing artifact.
- Future temporary converted datasets, staging copies, SFT intermediates, and eval intermediates must default to CephFS under `/home/xu.yang`.
- Any exception must explicitly record a justification in the relevant task evidence.

## Dataset Contract to Keep

Dataset path:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Checksum:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2  /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Row count:

```text
10
```

Schema:

```text
coding_agent_playground_sft_v1_sharegpt_messages
```

Dataset info entry:

```text
coding_agent_m1_sft_10_sharegpt
```

Required message contract:

```text
conversation column: messages
message role key: from
message text key: value
user role value: human
assistant role value: gpt
```

Verified current data shape:

```json
{
  "row_count": 10,
  "repo_split": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "role_values": {
    "human": 10,
    "gpt": 10
  },
  "unique_example_ids": 10,
  "unique_trajectory_ids": 10,
  "message_keys": ["from", "value"],
  "assertion_errors": []
}
```

## dev_2 Runtime Finding

From `evidence/gpu_s21_resource_tracking.md`, Session 21 runtime evidence records:

```text
dataset: coding_agent_m1_sft_10_sharegpt
dataset loaded: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
format conversion: 10/10
total optimization steps: 2
step progress: 1/2
forbidden prior signatures absent: KeyError 'from', missing dataset_info, ZeroDivisionError, scheduler warmup assertion
```

The final runtime blocker was:

```text
BLOCKED_FINAL_RUNTIME: SFT failed during checkpoint-1 safetensors serialization with ENOSPC: "No space left on device (os error 28)".
```

Interpretation: dev_2 evidence shows the dataset entry and ShareGPT data contract were accepted far enough to reach training step progress; the blocker moved to checkpoint storage capacity/path.

## test_1 Gate Finding

From `evidence/test_1_sft_dataformat_gate.md`, test_1 recorded:

```text
LLamaFactory compatibility decision for this artifact: PASS NO-EXECUTION
```

The same evidence states the concrete artifact:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count 10
message_key_sets [["from", "value"]]
```

Interpretation: test_1's data-format gate passed for the ShareGPT artifact before runtime, and dev_2's runtime evidence confirms the data-format blocker did not recur.

## ENOSPC Is Not Data-Side

ENOSPC means the runtime could not write checkpoint safetensors to the configured output device/path.

This is not fixed by:

- changing `messages[*].from/value`;
- changing dataset_info mapping;
- changing row count;
- switching back to OpenAI-style `role/content`;
- regenerating the 10-row artifact.

The next retry should preserve:

- `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`;
- `coding_agent_m1_sft_10_sharegpt`;
- `messages[*].from/value` ShareGPT contract;
- the existing checksum and row count.

The next retry should instead focus on ENOSPC mitigation in config/resource/output path, owned by the assigned ENOSPC config/resource/test tasks. For data-side storage, any newly materialized copy or temporary conversion should use a CephFS path under `/home/xu.yang` by default, not `/root/workspace` or a capacity-limited checkpoint/output path.

## Data-Side Blockers

No current data-side blocker found for the next ENOSPC-fixed retry.

Data-side conditions for next retry:

```text
sha256 matches 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
line_count == 10
dataset_info entry == coding_agent_m1_sft_10_sharegpt
dataset_info maps messages/from/value as recorded in dev_3_s21_datasetinfo_package.md
new temporary/staging/intermediate data artifacts default to /home/xu.yang on CephFS
```

If any of those conditions fail on a new worker, that is a staging/config regression, not a request to change the dataset contract.

## Storage Rule for Future Data Artifacts

Accepted existing artifact:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

This file may continue to be cited by path and checksum as the accepted source artifact for the current ShareGPT data contract.

Future default storage for data-side artifacts:

```text
/home/xu.yang/<project-or-task-specific-subdir>
```

Applies to:

- temporary converted datasets;
- staging copies;
- SFT input copies created for a retry;
- eval input/prediction intermediates if generated by data/eval preparation;
- any regenerated ShareGPT, stripped, packed, repeated, or sidecar provenance files.

Exception rule:

- If a future task stores a temporary or intermediate data artifact outside `/home/xu.yang`, the evidence must state the exact path and justification.
- Referencing the existing accepted artifact under `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl` does not require an exception because it predates this storage directive and is being treated as a stable source artifact, not a new temporary/intermediate.

## Completion Marker

Complete for `M1-S21-ENOSPC-DATA-CONFIRM-DEV3`:

- Confirmed next retry should keep the same ShareGPT data contract.
- Confirmed no data-side change is needed for ENOSPC.
- Cited dataset path, sha256, row count, dataset_info entry, and dev_2/test_1 data-format PASS evidence.
- Applied supervisor storage rule: future temporary converted datasets, staging copies, and SFT/eval intermediates default to CephFS `/home/xu.yang`; exceptions require justification.
- No SFT/GPU/eval execution performed.
