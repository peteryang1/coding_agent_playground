# Dev 1 Session 21 Launch Review

Owner: `intern_code_dev_1`  
Task ID: `M1-S21-LAUNCH-REVIEW-DEV1`  
Date: 2026-05-21  
Scope: refreshed no-execution review of Session 21 next-retry launch inputs for the ShareGPT-fixed Qwen3-8B SFT smoke. No remote experiments, SFT, GPU, or eval were run.

## Sources Reviewed

Commands/files checked from local durable evidence and GitHub metadata:

```text
sed -n '1,260p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_3_s21_datasetinfo_package.md
sed -n '1,520p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_1_s21_launch_gate.md
sed -n '1,620p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s21_sft_runtime.md
sed -n '1,240p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/gpu_s21_resource_tracking.md
sed -n '1,260p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_3_sft_dataformat_artifact.md
sed -n '1,220p' workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_1_sft_base_path_support.md
grep -n 'M1-S21-*' workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
gh pr view 30 --repo peteryang1/coding_agent_playground --json number,state,isDraft,mergeable,mergeStateStatus,headRefName,baseRefName,url,updatedAt,closedAt,mergedAt,title
```

## Refresh Summary

The prior dev_1 review was complete with missing-input blockers. Those specific missing files now exist:

```text
evidence/dev_3_s21_datasetinfo_package.md: present
evidence/test_1_s21_launch_gate.md: present
evidence/dev_2_s21_sft_runtime.md: present
evidence/gpu_s21_resource_tracking.md: present
```

Current result:

```text
runtime_gate_status: PASS_FOR_PM_AUTHORIZATION
primary_blocker: none for PM pre-runtime authorization
post_authorization_requirements: PM authorization, fresh Session 21 LTP frame/node/endpoint/nodes.json, final generated config proof, post-run evidence
```

## dev_3 Dataset_Info Package Review

Status: **PASS**

Reviewed path:

```text
evidence/dev_3_s21_datasetinfo_package.md
```

Accepted artifact:

```text
dataset_jsonl=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
sha256=26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row_count=10
schema=coding_agent_playground_sft_v1_sharegpt_messages
```

Accepted dataset_info entry:

```text
dataset_name=coding_agent_m1_sft_10_sharegpt
formatting=sharegpt
columns.messages=messages
tags.role_tag=from
tags.content_tag=value
tags.user_tag=human
tags.assistant_tag=gpt
tags.system_tag=system
tags.observation_tag=tool
```

Required staging locations:

```text
/root/workspace/coding_agent_playground/code/LLamaFactory/data/dataset_info.json
/root/workspace/coding_agent_playground/code/LLamaFactory/data/sft/dataset_info.json
```

Review:

- The package maps the accepted ShareGPT artifact through `messages[*].from/value`, which addresses the previous `KeyError: 'from'` signature.
- It cites the accepted artifact path, checksum, row count, schema, role values, and provenance fields.
- It records exact file/config locations for dev_2.
- It preserves the original 10 trajectory provenance through retained top-level fields such as `example_id`, `trajectory_id`, repo/task/source metadata, and conversion provenance.

## test_1 Launch Gate Review

Status: **PASS FOR DATASET_INFO / PRIOR COMMAND WIRING BLOCKER CORRECTED BY DEV_2 UPDATE**

Reviewed path:

```text
evidence/test_1_s21_launch_gate.md
```

test_1 current result before dev_2 refresh:

```text
GATE DEFINED / DATASET_INFO PASS / LAUNCH WIRING BLOCKED
```

Important gate findings:

- dev_3 dataset_info package passes test_1 validation.
- Accepted dataset entry name is `coding_agent_m1_sft_10_sharegpt`.
- Accepted artifact remains `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl` with sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- Base/config sanity expectations are documented.
- Runtime was blocked because dev_2's command template used a mismatched dataset name. dev_2 has since refreshed `dev_2_s21_sft_runtime.md` and `gpu_s21_resource_tracking.md` to use the accepted dataset name.

Prior mismatch identified by test_1:

```text
dev_3 accepted dataset_name: coding_agent_m1_sft_10_sharegpt
dev_2 runtime template DATASET_NAME: coding_agent_playground_sft_v1_sharegpt_messages
```

dev_2 refresh now records the required fix:

```text
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
generated runtime config must contain: dataset: coding_agent_m1_sft_10_sharegpt
```

## dev_2 Runtime Plan / Resource Tracking Review

Status: **PASS FOR PM AUTHORIZATION / PRE-SUBMIT UNTIL PM AUTHORIZES**

Reviewed paths:

```text
evidence/dev_2_s21_sft_runtime.md
evidence/gpu_s21_resource_tracking.md
```

Positive evidence:

- dev_2 recorded a Session 21 runtime plan and blocker file.
- dev_2 verified the accepted base model path at least to `config.json` existence with `base_ok`.
- dev_2 verified the ShareGPT artifact checksum and 10-line count.
- dev_2 recorded LTP submit/status/ssh/stop templates.
- dev_2 recorded output paths and expected runtime artifacts.
- `gpu_s21_resource_tracking.md` records no active Session 21 GPU and no LTP submitted by dev_2 for Session 21.

Current dev_2 pre-submit state:

- `ready_to_submit: no`
- `ready_to_run_sft: no`
- no current Session 21 LTP frame/job id;
- no current node id/endpoint;
- no current `nodes.json`;
- no PM runtime authorization;
- intended command now uses `DATASET_NAME=coding_agent_m1_sft_10_sharegpt`;
- generated config requirement now states `dataset: coding_agent_m1_sft_10_sharegpt`.

The runtime plan's initial missing-input list is now stale because dev_3/test_1/dev_1 files have appeared. The prior dataset-name wiring blocker is corrected. The remaining `ready_to_submit: no` / `ready_to_run_sft: no` state is expected before PM authorization and fresh LTP allocation.

## Base Model Review

Status: **PASS BY DURABLE EVIDENCE**

Accepted path:

```text
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

Evidence:

```text
evidence/dev_1_sft_base_path_support.md
evidence/dev_2_s21_sft_runtime.md
```

Review:

- Prior dev_1 evidence classifies this path as a clean-base candidate with complete HF-style Qwen3-8B layout.
- dev_2 evidence verified `config.json` exists on the corrected host.
- This remains acceptable for the Session 21 runtime package.
- No new remote model probe was run by dev_1 for this refresh.

## PR #30 Archival Status

Status: **BLOCKER FOR ARCHIVAL MERGE / NOT CRITICAL PATH FOR SESSION 21 RUNTIME**

GitHub metadata checked on 2026-05-21:

```json
{
  "number": 30,
  "state": "OPEN",
  "isDraft": false,
  "mergeable": "CONFLICTING",
  "mergeStateStatus": "DIRTY",
  "headRefName": "intern_code_dev_4/M1-SFT-RETRY-RUN-DEV4",
  "baseRefName": "main",
  "updatedAt": "2026-05-20T11:36:42Z",
  "closedAt": null,
  "mergedAt": null,
  "url": "https://github.com/peteryang1/coding_agent_playground/pull/30"
}
```

Review:

- PR #30 remains stale archival evidence for the failed original retry.
- It cannot be merged while `CONFLICTING` / `DIRTY`.
- It should remain under `M1-S21-PR30-CLEANUP-DEV4`; it is not the runtime critical path for Session 21.

## Runtime Gate PASS / BLOCKER List

PASS:

- dev_3 Session 21 dataset_info package exists and is internally consistent.
- Accepted dataset entry is `coding_agent_m1_sft_10_sharegpt`.
- Accepted artifact path/checksum/count are documented and match the prior ShareGPT artifact evidence.
- test_1 launch gate exists and accepts the dev_3 dataset_info package.
- Base model path `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` passes by durable evidence.
- dev_2 runtime/resource files exist and document no active Session 21 GPU, intended LTP shape, output paths, stop proof, and runtime artifact expectations.
- dev_2 updated the intended command to `DATASET_NAME=coding_agent_m1_sft_10_sharegpt`.
- dev_2 updated the generated config requirement to `dataset: coding_agent_m1_sft_10_sharegpt`.

BLOCKER for PM pre-runtime authorization:

- None identified in the refreshed durable evidence.

Expected remaining requirements after PM authorization:

1. PM records explicit runtime authorization.
2. dev_2 allocates a fresh Session 21 LTP frame/node/endpoint and writes `nodes.json`.
3. dev_2 stages repo/data/dataset_info files and records final generated config proof showing `dataset: coding_agent_m1_sft_10_sharegpt`.
4. dev_2 records run manifest, logs, exit status, checkpoint/model or exact runtime blocker, `trainer_state.json` / `all_results.json` presence or absence, and stop proof.
5. PR #30 remains archival cleanup and is not launch-critical for Session 21.

## Recommendation For PM Runtime Gate

```text
PASS_FOR_PM_AUTHORIZATION. The previous dataset-name mismatch is corrected in dev_2 evidence: intended command uses DATASET_NAME=coding_agent_m1_sft_10_sharegpt and generated config must contain dataset: coding_agent_m1_sft_10_sharegpt. PM can decide whether to authorize Session 21 LTP submit/SFT runtime. After authorization, dev_2 must still record fresh endpoint/nodes, final generated config proof, runtime logs/artifacts, and stop proof. PR #30 should remain archival cleanup and not block the replacement Session 21 path.
```

## Completion Marker

PASS_FOR_PM_AUTHORIZATION: refreshed `M1-S21-LAUNCH-REVIEW-DEV1` against updated dev_2 Session 21 evidence. Dataset_info package and test gate pass for data-format mapping, and the prior dataset-name mismatch is corrected. Remaining items are expected post-authorization runtime evidence requirements: PM authorization, fresh LTP endpoint/nodes, final generated config proof, runtime artifacts, and stop proof. No remote experiments, SFT, GPU, or eval were run.
