# Test 1 SFT Data-Format Gate

Date: 2026-05-20

Task ID: `M1-SFT-DATAFORMAT-GATE-TEST1`

Owner: `intern_code_test_1`

Scope: define and apply the no-execution test gate for any future SFT retry that claims to fix the LLamaFactory data-format failure from the previous retry. This gate does not authorize SFT, GPU allocation, or mini-swe evaluation.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_sft_dataformat_gate.md`

## Current State

Current result: **GATE DEFINED / ARTIFACT PASS NO-EXECUTION / RUN PENDING**

The task registry contains `M1-SFT-DATAFORMAT-GATE-TEST1` with owner, acceptance criteria, evidence path, PR state, and completion marker. The previous authorized retry failed before checkpoint creation with `KeyError: 'from'` in LLamaFactory dataset conversion. Current PM evidence says the OpenAI-style `role`/`content` messages were registered through ShareGPT defaults expecting `from`/`value`.

During this gate update, `evidence/dev_3_sft_dataformat_fix_plan.md` appeared in the PM worktree and was reviewed by test_1. It identifies the exact mismatch and proposes a preferred LLamaFactory OpenAI-style `role`/`content` registration path plus a ShareGPT `from`/`value` fallback. `evidence/dev_1_sft_dataformat_review.md` also appeared, but its content records that dev_3's plan was absent at dev_1 review time, so it is not yet a review of the now-present dev_3 fix plan.

Therefore test_1 can mark the gate definition complete and the dev_3 plan direction acceptable as a no-execution plan.

PM follow-up evidence from `evidence/dev_3_sft_dataformat_artifact.md` now provides a concrete ShareGPT converted artifact:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256=26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
schema=coding_agent_playground_sft_v1_sharegpt_messages
row_count=10
```

This artifact is compatible with the known failing LLamaFactory reader shape because the failed path expected `messages[*].from` / `messages[*].value`, and the artifact provides exactly those keys under `messages`. My earlier fallback sample used top-level `conversations`; that was too narrow for this project because the observed failure and dev_3 evidence both point to a `messages` conversation column. The corrected gate accepts either `messages` or another column name only if the future `dataset_info.json` maps the chosen column explicitly.

The concrete artifact passes test_1 no-execution compatibility checks. It still does not authorize SFT/GPU/eval, and it does not by itself prove a future run will pass; dev_4 must wire the exact artifact path and dataset_info/config entry in a later PM-authorized command.

Mini-swe status: **BLOCKED** until a later SFT retry is authorized, runs, passes this gate, and produces an accepted checkpoint/model or served endpoint.

## Sources Reviewed

- `task_registry.md`
- `history_log.md`
- `task_knowledge.md`
- `blockers.md`
- `evidence/test_1_sft_retry_gate.md`
- `evidence/test_1_sft_retry_validation.md`
- `evidence/dev_2_gpu_retry_submit.md`
- `evidence/gpu_retry_resource_tracking.md`
- `evidence/dev_3_sft_dataformat_fix_plan.md`
- `evidence/dev_1_sft_dataformat_review.md`
- `evidence/dev_3_sft_dataformat_artifact.md`

## Failure Signature To Fix

The prior retry failure to avoid is:

```text
KeyError: 'from'
```

Required interpretation for this gate:

- The current source SFT JSONL uses `coding_agent_playground_sft_v1`.
- Its conversation messages are OpenAI-style objects with `role` and `content`.
- The failing LLamaFactory path treated the data as ShareGPT-style records and attempted to read `from` and `value`.
- A valid fix must either register the OpenAI-style message schema correctly in LLamaFactory `dataset_info`, or produce a PM-approved ShareGPT-converted JSONL with `from` and `value`.

## No-Execution Rule

This is a no-execution gate.

Test_1 must not:

- run SFT,
- submit or occupy a GPU/LTP job,
- run mini-swe eval,
- mutate remote training state,
- treat this gate as authorization for dev_4 to launch.

PM can use this file only as test criteria for a later data-format fix package.

## Required Fix Package Before Any Future Retry

A future data-format-fixed retry is not gate-ready until dev_3 or the owning implementation task records one of these two concrete paths.

### Path A: LLamaFactory Dataset Registration For OpenAI-Style Messages

Required evidence:

- exact dataset path, expected to derive from `/root/workspace/cleaned_m1_sft_10/train.jsonl` unless PM approves a replacement;
- exact dataset checksum and row count;
- exact `dataset_info.json` path used by the training process;
- exact dataset entry name used by the config or launch wrapper;
- mapping that tells LLamaFactory to read messages as OpenAI-style `role`/`content`, not ShareGPT default `from`/`value`;
- sample input record from the dataset;
- sample resolved message object after registration mapping;
- command or static check used to verify the registration file exists before launch;
- statement that no trajectory provenance, `example_id`, or `trajectory_id` was dropped.

Pass criteria:

- Dataset registration explicitly maps the existing OpenAI-style fields.
- `dataset_info.json` is in the path the actual launcher reads.
- The training config/wrapper references the registered dataset name, not an unrelated placeholder.
- The sample record contains `messages[].role` and `messages[].content`.
- The sample check proves the conversion code will not access `messages[].from`.

Fail criteria:

- `dataset_info.json` is absent, generated in the wrong LLamaFactory checkout, or not referenced by the launch config.
- The registration leaves LLamaFactory on ShareGPT defaults for a `role`/`content` dataset.
- Evidence does not include a sample record and the exact dataset entry.
- Any required field is described only as a placeholder.

### Path B: ShareGPT JSONL Conversion

Required evidence:

- exact source dataset path and checksum;
- exact converted dataset path and checksum;
- exact row count before and after conversion;
- schema/version label for the converted artifact;
- deterministic conversion command or script path;
- before/after sample pair for at least one record;
- preserved `example_id`, `trajectory_id`, `repo`, and original task/provenance fields either as top-level metadata or a documented sidecar;
- role mapping table:
  - `system` to `system`, if supported by the selected LLamaFactory template, otherwise explicitly folded into the first human/user turn with evidence;
  - `user` to `human`;
  - `assistant` to `gpt`;
  - no empty `value` fields;
- statement that the converted artifact is smoke-training input, not new trajectory evidence.

Accepted after-conversion sample shape for this project:

```json
{
  "messages": [
    {"from": "human", "value": "task prompt..."},
    {"from": "gpt", "value": "assistant response..."}
  ],
  "example_id": "preserved",
  "trajectory_id": "preserved"
}
```

Compatibility note:

- The earlier generic fallback shape used top-level `conversations`; that is not required for this milestone if LLamaFactory `dataset_info.json` maps the conversation column to `messages`.
- The current failure was `message["from"]`, which means the loader had already reached each item inside a message list. A top-level `messages` list with `from`/`value` therefore addresses the observed missing-key failure, provided the launch config/dataset_info points at this artifact and maps the conversation column correctly.

Pass criteria:

- Every training conversation item has string `from` and string `value`.
- No conversation item has only `role`/`content` in the ShareGPT artifact.
- Row count matches the source row count unless PM explicitly approves filtering.
- The converted artifact has a recorded sha256 and deterministic generation command.
- Provenance fields are preserved.

Fail criteria:

- Any conversation item lacks `from` or `value`.
- Any `from` value is outside the accepted mapping for the selected LLamaFactory template.
- Row count changes without explicit PM approval.
- Conversion drops original trajectory provenance.

## Sample-Record Assertions

The fix package must include at least one concrete sample from the exact future training dataset and must satisfy the appropriate assertion set.

For OpenAI-style registration:

```python
import json
from pathlib import Path

p = Path("<dataset_jsonl>")
row = json.loads(p.read_text().splitlines()[0])
assert row["format_version"] == "coding_agent_playground_sft_v1"
assert isinstance(row["messages"], list) and len(row["messages"]) >= 2
for msg in row["messages"]:
    assert isinstance(msg.get("role"), str) and msg["role"]
    assert isinstance(msg.get("content"), str) and msg["content"]
    assert "from" not in msg
    assert "value" not in msg
print("openai_style_sample_ok", row.get("example_id"), row.get("trajectory_id"))
```

For ShareGPT conversion:

```python
import json
from pathlib import Path

p = Path("<converted_jsonl>")
row = json.loads(p.read_text().splitlines()[0])
conversation_column = "messages" if "messages" in row else "conversations"
assert isinstance(row[conversation_column], list) and len(row[conversation_column]) >= 2
for msg in row[conversation_column]:
    assert isinstance(msg.get("from"), str) and msg["from"]
    assert isinstance(msg.get("value"), str) and msg["value"]
    assert "role" not in msg
    assert "content" not in msg
assert row.get("example_id")
assert row.get("trajectory_id")
print("sharegpt_sample_ok", row["example_id"], row["trajectory_id"])
```

## Schema, Count, And Checksum Preservation

Required source identity unless PM approves a different artifact:

```text
source_dataset=/root/workspace/cleaned_m1_sft_10/train.jsonl
source_sha256=5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
source_count=10
source_format=coding_agent_playground_sft_v1
```

Any future fix package must record:

- source path,
- source sha256,
- source row count,
- output path if a converted dataset is produced,
- output sha256,
- output row count,
- deterministic command or script commit/source path,
- whether the output is registration-only or a new JSONL artifact,
- exact acceptance statement for row-count preservation.

Pass criteria:

- Count is 10 for registration-only use of the original dataset.
- Count is 10 for ShareGPT conversion unless PM explicitly approves a smoke-only expansion or filtering.
- Checksums are recorded for both source and output when output differs from source.
- Each output row preserves original `example_id` and `trajectory_id`.

Fail criteria:

- Checksum is missing.
- Row count is missing or unexplained.
- Source and converted artifacts are mixed up in the command.
- Expanded smoke-only data is silently substituted for the original 10 examples.

## Dataset Info Or Conversion Checks

A future package must include one of these evidence blocks.

Registration-only evidence block:

```text
fix_mode=dataset_info_registration
llamafactory_dir=<path>
dataset_info_path=<path>/data/dataset_info.json
dataset_name=<name-used-by-config>
dataset_jsonl=<path>
dataset_format=openai_messages_role_content
sample_assertion=PASS
checksum_assertion=PASS
```

ShareGPT conversion evidence block:

```text
fix_mode=sharegpt_conversion
source_jsonl=<path>
converted_jsonl=<path>
conversion_command=<exact command>
converted_format=sharegpt_messages_from_value
conversation_column=<messages-or-conversations>
sample_assertion=PASS
checksum_assertion=PASS
provenance_preserved=PASS
```

Fail if both blocks are absent. Fail if the package claims both modes but the launch command does not identify which dataset/config is actually used.

## Expected Log Assertions

For a later authorized SFT retry, post-run logs must not contain:

```text
KeyError: 'from'
Cannot open data/sft/dataset_info.json
ValueError: Cannot open data/sft/dataset_info.json
ZeroDivisionError: division by zero
steps_in_epoch
optimizer_param_scheduler.py
assert self.lr_warmup_steps < self.lr_decay_steps
```

If the run fails for a new reason, test_1 must record the first failing exception, exit status, artifact presence/absence, and whether the failure happened before or after dataset conversion.

For this data-format gate specifically, a later run is data-format PASS only if the logs show the dataset was loaded or training setup progressed beyond LLamaFactory dataset conversion without `KeyError: 'from'`.

## Post-Run Criteria If Later Authorized

A later SFT retry cannot pass this gate unless dev_4 or the owning run task records:

- fresh PM authorization for the retry task;
- endpoint or current `nodes.json`;
- exact command and environment;
- run ID;
- dataset path and checksum;
- config path;
- `dataset_info.json` path or converted ShareGPT JSONL path;
- stdout/stderr log paths;
- exit status;
- checkpoint/model path or explicit absence;
- `trainer_state.json` and/or `all_results.json` path if produced;
- resource cleanup/stop proof.

Post-run PASS requires:

- `KeyError: 'from'` absent from logs;
- dataset registration/conversion evidence matches the command actually run;
- source provenance and row count remain accepted;
- no previous DP=8 tiny-data or TP=8 scheduler failure signature appears;
- at least one checkpoint/model or an explicitly accepted smoke output exists if PM wants to unblock mini-swe.

Post-run FAIL requires any of:

- `KeyError: 'from'` appears again;
- dataset_info missing or wrong dataset entry;
- converted ShareGPT artifact malformed;
- command used a different unreviewed dataset;
- no logs/artifacts are provided;
- retry produces no checkpoint/model and PM needs a model for mini-swe.

## Current Application Of Gate

Current application result: **ARTIFACT PASS NO-EXECUTION / RUN BLOCKED**

Applied checks:

- `dev_3_sft_dataformat_fix_plan.md` exists and names task `M1-SFT-DATAFORMAT-FIX-DEV3`.
- The dev_3 plan identifies the exact mismatch: OpenAI-style `role`/`content` messages parsed through ShareGPT defaults expecting `from`/`value`.
- The dev_3 plan preserves the current source dataset identity:
  `/root/workspace/cleaned_m1_sft_10/train.jsonl`,
  count `10`,
  sha256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`.
- The preferred fix path is registration-only and keeps the canonical `coding_agent_playground_sft_v1` artifact unchanged.
- The fallback path is a derived ShareGPT JSONL with `from`/`value`, row-count/checksum plan, and provenance-preservation requirements.
- The plan includes before/after sample shapes and explicitly expects `KeyError: 'from'` to be absent after the fix.
- `dev_3_sft_dataformat_artifact.md` exists and names concrete artifact path:
  `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- Artifact sha256 is recorded as:
  `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Artifact row count is `10`, with `10` unique `example_id` and `10` unique `trajectory_id`.
- Artifact schema is `coding_agent_playground_sft_v1_sharegpt_messages`.
- Artifact sample assertions report `message_key_sets: [["from", "value"]]` and no assertion errors.
- Artifact sample uses top-level `messages` containing `from=human` and `from=gpt`, preserving provenance fields.
- LLamaFactory compatibility decision for this artifact: **PASS NO-EXECUTION**, because the observed failing reader expected `messages[*].from` and the artifact supplies `messages[*].from` and `messages[*].value`.

Open blockers:

- No exact future launch command identifies the converted JSONL path.
- No concrete future-run `dataset_info.json` entry is recorded for `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`.
- If the future `dataset_info.json` uses a conversation column other than `messages`, it must map that column explicitly or the artifact must be regenerated with the expected top-level key.
- If LLamaFactory rejects extra top-level metadata, dev_3/dev_4 must provide a second stripped artifact plus a sidecar preserving `example_id`, `trajectory_id`, repo, task, and source provenance.
- No future SFT retry is authorized by this no-execution gate.

Exact fixes required before launch if PM treats the remaining blockers as launch-blocking:

1. Add or record the exact LLamaFactory `dataset_info.json` entry for the converted artifact, with file path `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, formatting `sharegpt`, conversation column `messages`, role tag `from`, and content tag `value`.
2. Update the future dev_4 command/config to use `DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl` and record sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
3. If the deployed LLamaFactory template requires top-level `conversations` rather than mapped `messages`, regenerate a deterministic artifact with `conversations[*].from/value`, record checksum/count/sample assertions, and preserve provenance in top-level fields or a sidecar.
4. If the loader rejects extra top-level metadata, produce a training-only stripped JSONL and a provenance sidecar; both need checksums and row-id reconciliation.

Completion marker for this task:

```text
task_id: M1-SFT-DATAFORMAT-GATE-TEST1
gate_definition: COMPLETE
dev3_fix_plan_direction: PASS_NO_EXECUTION
fix_artifact_validation: PASS_NO_EXECUTION
llamafactory_compatibility: PASS_FOR_OBSERVED_MESSAGES_FROM_VALUE_READER
sft_retry_authorized_by_test1: false
mini_swe_can_proceed: false
blocking_reason: no exact future command, no concrete future-run dataset_info entry, and no later post-run SFT evidence are present
```
