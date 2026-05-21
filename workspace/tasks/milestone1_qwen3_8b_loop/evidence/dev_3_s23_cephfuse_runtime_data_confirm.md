# dev_3 Session 23 Ceph-Fuse Runtime Data Confirmation

Task ID: `M1-S23-CEPHFUSE-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm the final ceph-fuse fixed preflight blocker does not require data or dataset package changes.

No LTP submit, GPU allocation, SFT, dry-run, or eval was run by dev_3.

## Decision

Decision: no data/package change is needed for the final ceph-fuse fixed preflight blocker.

The current blocker is structured preflight health status:

```text
PREFLIGHT_RESULT=FAIL_HEALTH_SIGNATURE
SFT_ALLOWED=false
```

SFT was correctly not run by contract. The runtime had already passed storage, `/home/xu.yang` CephFS, capacity, local bundle/data transfer, checksum verification, no-remote-network, different-node, topology/NVLink, and torch NCCL all-reduce gates. The remaining blocker does not implicate ShareGPT JSONL content, row count, schema, dataset_info, or provenance.

## Accepted Dataset Contract

Accepted source:

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

Required provenance fields:

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

## Prior Transfer Verification

From current `task_registry.md` and `evidence/dev_2_s23_cephfuse_preflight_sft_runtime.md`:

```text
runtime task: M1-S23-CEPHFUSE-PREFLIGHT-SFT-RUNTIME-DEV2
frame: xu.yang~coding-agent-playground-m1-s23-cephfuse-preflight-sft-20260521T132628Z
endpoint: ssh -p 38862 root@10.100.22.36
node: lg-cmc-b7r202-q03u26-h200-000730
PR51 merge commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
remote staging path: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging
remote dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
transfer source: local/provided workspace artifact
remote source/dependency network: not used
```

Recorded transfer/checksum commands included:

```text
scp ... /tmp/cleaned_m1_sft_10_sharegpt_s23_cephfuse_20260521T132628Z/train.jsonl root@10.100.22.36:/home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging/
ssh -p 38862 root@10.100.22.36 "cp /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_cephfuse_preflight_sft_20260521T132628Z/staging/train.jsonl /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl && sha256sum /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl"
```

Interpretation:

- The accepted ShareGPT dataset was staged from local/provided workspace, not remote GitHub or external dependency network.
- The transferred dataset checksum matched the accepted source checksum.
- The `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl` remote copy is a runtime input compatibility copy after checksum verification; generated artifacts remained under `/home/xu.yang/coding_agent_playground/outputs`.
- No transfer/checksum evidence indicates content drift or schema drift.

## Ceph-Fuse Fixed Runtime Evidence Interpreted

Current final runtime facts:

```text
ceph-fuse: fixed/proved
/home/xu.yang CephFS: proved
capacity probe: PASS_AND_CLEANED
local bundle/data transfer: passed
checksum verification: passed
no remote source/dependency network: passed
different-node gate: passed
topology/NVLink: captured/present
torch NCCL all-reduce: exit 0
structured preflight: FAIL_HEALTH_SIGNATURE
SFT_ALLOWED: false
SFT: not run
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run
frame final state: STOPPED (Completed)
```

Data interpretation:

- Since SFT was skipped after preflight failure, there is no new training-time data parsing or conversion failure.
- The preflight blocker is health-signature related, not data-contract related.
- The accepted ShareGPT contract should remain unchanged for any future PM-authorized retry.

## Future Data Staging Rule

Future temporary, staged, converted, copied, checksum sidecar, provenance sidecar, data logs, data metadata, run metadata, and other data/intermediate artifacts must default under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Recommended run-specific dataset path:

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

Justification: existing accepted source artifact and runtime compatibility input copy, only after checksum verification. New generated outputs, logs, metadata, and intermediates should remain under `/home/xu.yang/coding_agent_playground/outputs` unless a required-path exception is explicitly justified in owner evidence.

## Data-Side Blocker Status

No current data-side blocker found.

The next retry remains data-ready if:

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

If a future transfer/checksum or generated-config dataset mismatch appears, treat it as a staging/config blocker. Do not regenerate or alter the accepted ShareGPT dataset unless PM assigns a new data task with a concrete data defect.

## Completion Marker

Complete for `M1-S23-CEPHFUSE-DATA-CONFIRM-DEV3`:

- Confirmed the final ceph-fuse fixed preflight blocker does not require data/package changes.
- Cited accepted ShareGPT sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info entry `coding_agent_m1_sft_10_sharegpt`.
- Cited prior transfer/checksum verification from the ceph-fuse fixed runtime.
- Found no current data-side blocker.
- No LTP/GPU/SFT/dry-run/eval execution performed by dev_3.
