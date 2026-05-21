# dev_3 Session 23 PR53 Data Confirmation

Task ID: `M1-S23-PR53-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm whether the PR53 parser/preflight blocker requires any ShareGPT data or dataset package change.

No LTP submit, GPU command, SFT, dry-run, or eval was run by dev_3.

## Decision

Decision: no data/package change is needed for the PR53 parser/preflight blocker.

The PR53 runtime reached local bundle/data transfer and checksum verification, then failed before SFT at structured preflight:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
PREFLIGHT_STRUCTURED_STATUS=FAIL_HEALTH_SIGNATURE
ACTIONABLE_FAULT=true
SFT_ALLOWED=false
SFT_SKIP_REASON=FAIL_HEALTH_SIGNATURE
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
```

The exact blocker recorded by dev_2 is `BLOCKED_PR53_PREFLIGHT_HEALTH_SIGNATURE`: PR53 still classified `NCCL_ASYNC_ERROR_HANDLING` deprecation warnings in `torch_nccl_allreduce.log` as actionable `nccl_or_collective_failure` even though the functional torch/NCCL all-reduce passed with `TORCHRUN_EXIT=0` and `ALLREDUCE_OK world_size=8 value=36.0`.

This blocker is parser/preflight health classification, not ShareGPT JSONL content, row count, schema, dataset_info, provenance, or transfer drift.

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

## PR53 Transfer Result

From `evidence/dev_2_s23_pr53_placementprobe_preflight_sft_runtime.md` and `task_registry.md`:

```text
runtime task: M1-S23-PR53-PLACEMENTPROBE-PREFLIGHT-SFT-RUNTIME-DEV2
PR53 merge commit: e29c93736be3384663cad953cd18da68c30070fb
frame: xu.yang~coding-agent-playground-m1-s23-pr53-placementprobe-preflight-sft-20260521T142358Z
endpoint: ssh -p 30073 root@10.100.24.12
assigned node: lg-cmc-b7r401-a05u06-h200-000770
forbidden-node gate: PASS_NON_FORBIDDEN
remote staging path: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z/staging
remote data path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote source/dependency network: not used
```

Transfer and verification summary:

```text
source transfer: local PR #53 bundle + dataset copied and verified by sha256/file count
remote bundle sha256: 34c5655cc8d7003ef3855b7ef5d285311794ab2fcad435dc4d52a3c80c10de77
remote file count: 111
remote file-list count: 111
critical source/config/script checksums: OK
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
```

Interpretation:

- The PR53 runtime used the accepted ShareGPT dataset.
- The transferred dataset checksum matched the accepted source checksum.
- No transfer evidence indicates data content drift or schema drift.
- No remote `git clone`, `git fetch`, GitHub/source fetch, remote source download, or project dependency download was used on the GPU node.

## Runtime Evidence Interpreted

The PR53 placement-probe runtime passed the data-relevant prerequisites:

```text
ceph-fuse proof: PASS
/home/xu.yang output proof: PASS
capacity proof: PASS_AND_CLEANED
forbidden-node gate: PASS_NON_FORBIDDEN
source/data transfer: passed
checksum verification: passed
remote source/dependency network: not used
```

It then blocked before SFT:

```text
structured preflight: FAIL_HEALTH_SIGNATURE
SFT_ALLOWED: false
SFT: not run
checkpoint/model: absent because SFT was not run
trainer_state.json: absent because SFT was not run
all_results.json: absent because SFT was not run
eval: not authorized and not run
frame final state: STOPPED (Completed)
```

Because SFT did not run, there is no new training-time dataset conversion, dataloader, tokenizer, or LLamaFactory dataset_info failure to remediate. The preflight failure is upstream of the data package.

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

Complete for `M1-S23-PR53-DATA-CONFIRM-DEV3`:

- Confirmed no data/package change is needed for the PR53 parser/preflight blocker.
- Cited accepted ShareGPT sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info entry `coding_agent_m1_sft_10_sharegpt`.
- Cited PR53 transfer/checksum verification and remote dataset checksum match.
- Found no current data-side blocker.
- No LTP/GPU/SFT/dry-run/eval execution performed by dev_3.
