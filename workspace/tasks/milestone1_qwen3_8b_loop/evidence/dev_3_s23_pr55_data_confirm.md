# dev_3 Session 23 PR55 Data Confirmation

Task ID: `M1-S23-PR55-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm whether the PR55 SFT wrapper blocker requires any ShareGPT data or dataset package change.

No LTP submit, GPU command, SFT, dry-run, or eval was run by dev_3.

## Decision

Decision: no data/package change is needed for the PR55 wrapper blocker.

The PR55 runtime passed the data-relevant path before SFT:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
```

The one authorized SFT attempt then failed before GPU training due a launch-wrapper environment bug:

```text
final status: BLOCKED_PR55_SFT_WRAPPER_ENV_DEP_TARGET_UNBOUND_STOPPED_NO_CHECKPOINT
exit_status: 1
blocker line: environment: DEP_TARGET: unbound variable
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
```

This blocker is wrapper/env wiring, not ShareGPT JSONL content, row count, schema, dataset_info, provenance, or transfer drift.

## Accepted Dataset Contract

Accepted source artifact:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Accepted sha256:

```text
26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Row count:

```text
10
```

Schema:

```text
coding_agent_playground_sft_v1_sharegpt_messages
messages[*].from
messages[*].value
```

Dataset info entry:

```text
coding_agent_m1_sft_10_sharegpt
```

Required provenance fields to preserve:

```text
example_id
trajectory_id
repo
task
source
```

Known aggregate invariants:

```text
line_count == 10
unique_example_ids == 10
unique_trajectory_ids == 10
repo_split == {"fastapi/fastapi": 4, "scikit-learn/scikit-learn": 3, "Textualize/rich": 3}
role_values == {"human": 10, "gpt": 10}
message_keys == ["from", "value"]
```

## PR55 Transfer Result

From `evidence/dev_2_s23_pr55_preflight_sft_runtime.md`, `evidence/gpu_s23_pr55_preflight_sft_tracking.md`, and `task_registry.md`:

```text
runtime task: M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2
PR55 merge commit: 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
endpoint: ssh -p 15535 root@10.100.22.28
assigned node: lg-cmc-b7r202-q05u06-h200-000722
forbidden-node gate: PASS, node is not in the forbidden list
remote staging root: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z/staging
remote data path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
remote source/dependency network: not used for project source/data
```

Transfer and verification summary:

```text
source transfer: local PR #55 bundle + dataset copied and verified by checksum/file count
bundle sha256: db82b9162af2c37d670e568e16002cfc595e9090d578121545827622c3141df7
remote repo file count: 118
critical file checks: OK for parser, tests, train script, config templates, and manifest writer
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Interpretation:

- The PR55 runtime used the accepted ShareGPT dataset.
- The transferred dataset checksum matched the accepted source checksum.
- No transfer evidence indicates data content drift or schema drift.
- The runtime dataset name was `coding_agent_m1_sft_10_sharegpt`.
- The SFT runtime config and manifest were generated under `/home/xu.yang/coding_agent_playground/outputs`.

## Runtime Evidence Interpreted

The PR55 runtime cleared data, storage, and preflight gates:

```text
/mnt/cephfs: fuse.ceph-fuse
output root: /home/xu.yang/coding_agent_playground/outputs on fuse.ceph-fuse
capacity probe: PASS_AND_CLEANED
source/data transfer: passed
checksum verification: passed
structured preflight: PASS
sft_allowed: true
```

SFT launch evidence used the expected dataset contract:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
dataset: coding_agent_m1_sft_10_sharegpt
dataset source: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/config/qwen3_8b_sft.yaml
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z/run_manifest.json
```

The failure occurred before GPU training:

```text
SFT start: 2026-05-21T15:08:24Z
SFT end: 2026-05-21T15:08:25Z
exit_status: 1
blocker: environment: DEP_TARGET: unbound variable
post-failure GPU sample: all 8 H200 at 0% util and 1 MiB memory
post-failure process scan: no torchrun/python3 -m llamafactory/llamafactory-cli/train_qwen3_8b_sft process
```

Because the failure is an exported bash wrapper/local-variable issue, there is no current evidence of a data parser, dataloader, tokenizer, LLamaFactory dataset_info, row-count, or schema defect.

## Future Data Staging Rule

Future generated temporary, staged, converted, copied, checksum sidecar, provenance sidecar, data logs, metadata, SFT outputs, checkpoints, eval outputs, and other intermediates must default under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Recommended future run-specific dataset staging path:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Recommended checksum sidecar:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/SHA256SUMS
```

Allowed input exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: this is the accepted source artifact and remote compatibility input path after checksum verification. New generated outputs, logs, metadata, and intermediates should remain under `/home/xu.yang/coding_agent_playground/outputs` unless a required-path exception is explicitly justified in owner evidence.

## Data-Side Blocker Status

No current data-side blocker found.

The data package remains ready for a future PM-authorized retry if:

```text
dataset_info remains coding_agent_m1_sft_10_sharegpt
source sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
messages[*].from/value ShareGPT contract is preserved
example_id/trajectory_id/repo/task/source provenance fields are preserved
local/provided-workspace dataset is verified before transfer
remote post-transfer checksum equals accepted source checksum
generated data artifacts/logs/metadata/intermediates are under /home/xu.yang/coding_agent_playground/outputs unless explicitly justified
```

If a future run exposes a transfer/checksum mismatch, missing `dataset_info` entry, row-count mismatch, or LLamaFactory data parser error, treat that as a new data/staging blocker. Do not regenerate or alter the accepted ShareGPT dataset without a new explicit PM data task.

## Completion Marker

Complete for `M1-S23-PR55-DATA-CONFIRM-DEV3`:

- Confirmed no data/package change is needed for the PR55 wrapper blocker.
- Cited accepted ShareGPT sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info entry `coding_agent_m1_sft_10_sharegpt`.
- Cited PR55 source/data transfer and checksum verification.
- Found no current data-side blocker.
- No LTP/GPU/SFT/dry-run/eval execution performed by dev_3.
