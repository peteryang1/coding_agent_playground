# dev_3 Session 23 PR57 Data Confirmation

Task ID: `M1-S23-PR57-DATA-CONFIRM-DEV3`
Owner: `intern_code_dev_3`
Date: 2026-05-21

## Scope

Confirm data/package state for the PR57 runtime path and future eval handoff.

No LTP submit, GPU command, remote command, transfer command, SFT, dry-run, or eval was run by dev_3.

## Supervisor Correction Applied

All future remote GPU/LTP nodes must be treated as no-external-network for project code and dependency staging.

Future runtime owners must not run remote `git clone`, `git fetch`, GitHub source download, project-code download, dependency download, or remote package-network staging on the GPU node. Code, config, scripts, data, dependency wheels or extracted dependency tree, and any optional LLamaFactory CLI wrapper must be prepared first in a local/provided workspace, verified locally, transferred by `rsync`, `scp`, or tar-over-SSH, and verified after transfer.

PM coordinates/gates only. PM does not run transfer, remote, SFT, or eval commands.

## Decision

Decision: PR57 needs no ShareGPT data or dataset package change.

PR57 is a wrapper/env fix for the PR55 SFT launch blocker:

```text
prior blocker: environment: DEP_TARGET: unbound variable
PR57 merge commit: c450429c2e3369adc723d132396399cd17dba684
completion PR58 merge commit / authorized origin/main: b4ac31ef1e3772953108348bf099818326ed65cc
```

Reviewed durable evidence records PR57 changes in:

```text
scripts/train_qwen3_8b_sft.sh
tests/test_train_qwen3_8b_sft_static.py
```

The fix defines and exports runtime wrapper variables:

```text
LLAMAFACTORY_CLI="${LLAMAFACTORY_CLI:-llamafactory-cli}"
DEP_TARGET="${DEP_TARGET:-${PYTHON_DEPS_DIR:-${RUN_DIR}/python_deps}}"
LF="${LF:-${LLAMAFACTORY_DIR}}"
export DEP_TARGET LF LLAMAFACTORY_CLI
```

This does not alter the accepted ShareGPT JSONL content, schema, row count, provenance, dataset_info entry, or eval data contract.

## Accepted ShareGPT Dataset Contract

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

## Prior PR55 Data/Transfer State

The PR55 runtime, which PR57 is fixing, cleared data and transfer gates before the wrapper failure:

```text
runtime task: M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2
frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
endpoint: ssh -p 15535 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
forbidden-node gate: PASS
output root: /home/xu.yang/coding_agent_playground/outputs
capacity probe: PASS_AND_CLEANED
source/data transfer: local PR55 source bundle/data only, checksums verified
remote source/dependency network: no remote git clone/fetch/GitHub/source/dependency download
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset entry: coding_agent_m1_sft_10_sharegpt
row count: 10
schema: ShareGPT messages[*].from/value
preflight: PASS
sft_allowed: true
SFT blocker: environment: DEP_TARGET: unbound variable
checkpoint/model/trainer_state/all_results/eval: absent
```

Data interpretation:

- The accepted ShareGPT dataset was already proven compatible through PR55 source/data transfer and checksum verification.
- The PR55 failure happened after preflight pass at wrapper launch, before GPU training.
- There is no evidence of data parser, dataloader, tokenizer, LLamaFactory dataset_info, row-count, checksum, or schema failure.

## PR57 Runtime Input Expectations

For any PR57 PM-authorized runtime, dev_2 should use:

```text
source commit/package: origin/main commit b4ac31ef1e3772953108348bf099818326ed65cc unless PM supersedes it
dataset_info entry: coding_agent_m1_sft_10_sharegpt
dataset source/input: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: messages[*].from/value
```

Required no-remote-network preparation and transfer evidence:

```text
1. Prepare source/config/scripts/data/dependency package in local/provided workspace.
2. Verify exact source commit locally.
3. Record local file list and file count.
4. Record local bundle path and sha256.
5. Record dataset source path and sha256.
6. Transfer by rsync/scp/tar-over-SSH only.
7. Record exact transfer command(s), source path(s), destination path(s), and timestamp(s).
8. Verify remote bundle checksum after transfer.
9. Verify remote file count / file-list match.
10. Verify critical source/config/script checksums after extraction.
11. Verify remote dataset sha256 equals the accepted source sha256.
12. Record that no remote git clone/fetch/GitHub/source/dependency network command was used.
```

Recommended local/provided dataset staging input before transfer:

```text
/tmp/cleaned_m1_sft_10_sharegpt_<RUN_ID>/train.jsonl
```

Recommended remote generated/staged data location:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/data/coding_agent_m1_sft_10_sharegpt/train.jsonl
```

Allowed remote compatibility input exception:

```text
/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
```

Justification: existing accepted source/runtime compatibility input path after checksum verification. Generated outputs, logs, metadata, temporary converted datasets, dependency targets, checkpoints, and eval-ready intermediates must remain under `/home/xu.yang/coding_agent_playground/outputs` unless a required-path exception is explicitly justified.

## Future Eval Handoff Data State

Eval remains blocked until a future authorized runtime produces a complete checkpoint/model or PM-accepted served endpoint. Data/package state for eval handoff is unchanged:

```text
training data provenance remains the 10 accepted ShareGPT examples
dataset_info remains coding_agent_m1_sft_10_sharegpt
dataset sha256 remains 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count remains 10
schema remains messages[*].from/value
provenance fields remain example_id/trajectory_id/repo/task/source
```

Future eval artifacts, prediction files, metrics, logs, run metadata, and temporary intermediates should be under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Data-side eval blocker: none beyond the absence of an accepted model/checkpoint/served endpoint.

## Data-Side Blocker Status

No current data-side blocker found.

PR57 should not regenerate, duplicate, repack, or convert the accepted ShareGPT dataset unless a new PM data task identifies a concrete data defect. The next runtime blocker, if any, should be classified from the actual PR57 runtime evidence; data should only be changed if future evidence shows checksum drift, missing dataset_info registration, row-count mismatch, schema mismatch, LLamaFactory data parser failure, or provenance loss.

## Completion Marker

Complete for `M1-S23-PR57-DATA-CONFIRM-DEV3`:

- Confirmed PR57 needs no data/package change.
- Cited accepted ShareGPT sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Restated row count 10, schema `messages[*].from/value`, and dataset_info entry `coding_agent_m1_sft_10_sharegpt`.
- Restated future no-remote-network transfer/input expectations.
- Restated `/home/xu.yang/coding_agent_playground/outputs` rule for generated data/intermediates and eval-ready artifacts.
- Found no current data-side blocker.
- No LTP/GPU/SFT/dry-run/eval/remote execution performed by dev_3.
