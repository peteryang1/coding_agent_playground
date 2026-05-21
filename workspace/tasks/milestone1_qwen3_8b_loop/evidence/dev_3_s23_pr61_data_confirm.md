# dev_3 Session 23 PR61 Data Confirmation

Task ID: `M1-S23-PR61-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm whether the PR61 `model_name_or_path` runtime blocker is caused by the accepted ShareGPT data artifact or LLamaFactory dataset package.

No LTP, GPU, SFT, eval, dry-run, transfer, or remote command was run by dev_3 for this confirmation. This evidence is based on existing durable PR61 runtime/tracking evidence.

## Decision

No ShareGPT data/package change is implicated for PR61.

The PR61 runtime evidence shows source/data/dependency transfer passed, the remote dataset checksum matched, `mcore_adapter` import passed, structured preflight passed, `SFT_ALLOWED=true`, and the LLamaFactory launcher was reached. The observed blocker is:

```text
final blocker: BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE
failure signature: ValueError: Please provide `model_name_or_path`.
trace path: llamafactory/launcher.py -> train/tuner.py -> hparams/parser.py -> model_args.py
```

The generated runtime YAML already contained both:

```text
model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: coding_agent_m1_sft_10_sharegpt
```

So the failure is an MCA/LLamaFactory model-argument binding or parser path issue after launcher entry, not a ShareGPT JSONL content, row-count, checksum, or dataset_info entry issue.

## Accepted ShareGPT Data Contract

```text
source artifact: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema/version: coding_agent_playground_sft_v1_sharegpt_messages
message schema: messages[*].from / messages[*].value
role values: human / gpt
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

Retained provenance fields remain required:

```text
example_id
trajectory_id
repo
repo_path
task_id
source
metadata
artifacts
```

## Dataset Info Evidence

Known entry name:

```text
coding_agent_m1_sft_10_sharegpt
```

Prior dev_3 package evidence records the LLamaFactory entry body as:

```json
{
  "coding_agent_m1_sft_10_sharegpt": {
    "file_name": "/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl",
    "formatting": "sharegpt",
    "columns": {
      "messages": "messages"
    },
    "tags": {
      "role_tag": "from",
      "content_tag": "value",
      "user_tag": "human",
      "assistant_tag": "gpt",
      "system_tag": "system",
      "observation_tag": "tool"
    }
  }
}
```

Expected LLamaFactory package locations from prior package evidence:

```text
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
```

PR61 runtime evidence records:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
runtime config dataset: coding_agent_m1_sft_10_sharegpt
runtime config path: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z/config/qwen3_8b_sft.yaml
runtime config sha256: 4f22228204bab055c982d2c9046877b26146833be93ea5da0c59b582ee72b75a
run manifest sha256: 210633469ab3dbfed7546ec01d818957c1f73cae2b4ef1f8fd472cbd3c8e7f7c
```

Dataset_info file hash was not separately recorded in the PR61 runtime evidence I found. This is not a data blocker because PR61 reached the LLamaFactory launcher and failed on `model_name_or_path`, while the dataset name and accepted dataset checksum were recorded and transfer-verified.

## PR61 Dataset Transfer Result

PR61 transfer and verification evidence from dev_2:

```text
source commit: 713862da983f73b165af1cfe27935ccef616a049
remote workspace: /root/workspace
remote repo path: /root/workspace/coding_agent_playground
remote dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256 verification: OK, 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
mcore_adapter import check: PASS
structured preflight: PASS
SFT_ALLOWED: true
```

PR61 also followed the no-remote-network staging rule in the recorded runtime evidence: no remote `git clone`, `git fetch`, GitHub/source fetch, dependency download, or `pip download` was run; local/provided bundles and dataset were transferred and checksum-verified.

## Why Data Is Not Implicated

- The accepted JSONL checksum matched after transfer.
- The dataset_info entry name used by runtime was `coding_agent_m1_sft_10_sharegpt`.
- The runtime config recorded `dataset: coding_agent_m1_sft_10_sharegpt`.
- Prior data-format blockers (`KeyError: 'from'`, wrong role/content schema, missing ShareGPT `from/value`) are not the PR61 failure signature.
- Prior data loader/preprocess blockers (`datasets.map(num_proc=4)` / SyncManager EOFError) are not the PR61 failure signature.
- The failure trace occurs in LLamaFactory/MCA model argument parsing and explicitly complains about `model_name_or_path`, not dataset parsing.
- No checkpoint/model, `trainer_state.json`, `all_results.json`, or eval artifact was produced, so there is no downstream artifact requiring data-side remediation.

## Future Data/Package Requirements

Keep the accepted ShareGPT data contract unchanged for any future PR61 follow-up or eval handoff unless a new PM data task identifies a concrete data defect.

Future generated temporary, staged, converted, run metadata, training, or eval artifacts must use:

```text
/home/xu.yang/coding_agent_playground/outputs
```

The existing source artifact path remains an allowed required-input exception when checksum-verified:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Remote GPU/LTP nodes remain no-external-network for project code/dependency staging. Future packages should be prepared from local/provided workspace/dependency artifacts, transferred by `scp`/`rsync`/tar-over-SSH, and verified by file list plus checksums before any PM-authorized runtime.

## Data-Side Blocker Status

```text
data_side_blocker: none found
package_change_needed: no
recommended next owner area: LLamaFactory/MCA model_name_or_path parser/config binding, not data pipeline
completion_marker: COMPLETE_FOR_PR61_DATA_CONFIRM
```
