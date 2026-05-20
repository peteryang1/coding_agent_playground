# dev_3 SFT Input Handoff

Owner: `intern_code_dev_3`
Recipient: `intern_code_dev_4`
Task: `milestone1_qwen3_8b_loop`
Created: 2026-05-20

## Final Workspace

```text
ssh -p 31787 root@10.100.194.40
```

## SFT Input Paths

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
/root/workspace/cleaned_m1_sft_10/conversion_summary.json
/root/workspace/cleaned_m1_sft_10/rejected.jsonl
/root/workspace/rollouts_m1_10/complete_process_validation.json
```

## Checksums

```text
5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054  /root/workspace/cleaned_m1_sft_10/train.jsonl
c822d7d46d3237ef337c8a95629639d240b1ae55212948aa3717692054e7bd9d  /root/workspace/cleaned_m1_sft_10/conversion_summary.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /root/workspace/cleaned_m1_sft_10/rejected.jsonl
```

## Schema

Format version: `coding_agent_playground_sft_v1`

Each line in `train.jsonl` is one JSON object with these top-level keys:

```text
artifacts
example_id
format_version
messages
metadata
repo
repo_path
source
task_id
trajectory_id
```

`messages` is a chat-format list. Each message object has:

```text
role
content
```

Allowed message roles:

```text
system
user
assistant
tool
```

The current 10 examples contain only `user` and `assistant` messages, two messages per example.

## Repo Split

```json
{
  "fastapi/fastapi": 4,
  "scikit-learn/scikit-learn": 3,
  "Textualize/rich": 3
}
```

Status counts:

```json
{
  "success": 10
}
```

## Validation Status

Complete-process quality gate:

```json
{
  "checked_count": 10,
  "valid_count": 10,
  "invalid_count": 0
}
```

Conversion summary:

```json
{
  "input_count": 10,
  "kept_count": 10,
  "dropped_count": 0,
  "error_count": 0,
  "per_repo_kept": {
    "fastapi/fastapi": 4,
    "scikit-learn/scikit-learn": 3,
    "Textualize/rich": 3
  },
  "status_counts": {
    "success": 10
  }
}
```

JSONL validation:

```json
{
  "format_ok": true,
  "train_lines": 10,
  "unique_example_ids": 10,
  "unique_trajectory_ids": 10,
  "rejected_lines": 0,
  "schema_errors": [],
  "cleaning_defects": []
}
```

## Data Contract for dev_4

Use `/root/workspace/cleaned_m1_sft_10/train.jsonl` as the current Milestone 1 smoke SFT input.

Training loader expectations:

- Read as JSONL, one object per line.
- Require `format_version == "coding_agent_playground_sft_v1"` for every record.
- Use `messages` as the supervised chat transcript.
- Preserve message order.
- Treat `messages[*].role` and `messages[*].content` as the only required training conversation fields.
- Use `example_id` or `trajectory_id` as stable sample IDs for manifests, debugging, and loss/error attribution.
- Use `repo`, `task_id`, `metadata.status`, and `source.raw_path` only as metadata, not prompt text, unless dev_4 explicitly needs metadata-conditioned training.
- Do not include `artifacts.stdout`, `artifacts.stderr`, or raw rollout logs in training text; those are provenance/debug pointers.
- Do not train on `rejected.jsonl`; it is empty for this handoff and exists only for count reconciliation.

Recommended loader assertion:

```text
line_count == 10
kept_count == 10
dropped_count == 0
error_count == 0
sha256(train.jsonl) == 5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
```

## Data-Side Blockers

No current data-side blocker for smoke SFT.

Caveats:

- This is a 10-trajectory smoke dataset, not a full-scale 300-trajectory dataset.
- Repo distribution is intentionally small and slightly imbalanced: 4 FastAPI, 3 scikit-learn, 3 Rich.
- Each example currently has a compact two-message transcript. If dev_4 needs command/tool traces for training, that is a new data requirement and should be routed back to dev_3/PM before changing the dataset contract.
