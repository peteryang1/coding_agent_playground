# Dev 1 SFT Data-Format Review

Owner: `intern_code_dev_1`  
Task ID: `M1-SFT-DATAFORMAT-REVIEW-DEV1`  
Date: 2026-05-20  
Scope: independent review of PR #30 retry failure facts and dev_3 data-format fix plan for provenance/schema risks. No remote experiments were run.

## Sources Reviewed

- PR #30 metadata/body from GitHub.
- `task_registry.md`
- `assignments.md`
- `status.md`
- `blockers.md`
- `task_knowledge.md`
- `history_log.md`
- `evidence/dev_2_gpu_retry_submit.md`
- `evidence/gpu_retry_resource_tracking.md`
- `evidence/dev_3_sft_retry_data_gate.md`
- `evidence/dev_3_sft_data_mitigation.md`
- `evidence/dev_3_sft_dataformat_fix_plan.md`
- `evidence/test_1_sft_dataformat_gate.md`
- `evidence/rollout_harness/convert_rollouts_to_sft.py`

Missing at review time:

- `evidence/dev_4_sft_retry_run.md` is not present in the PM worktree because PR #30 is still open/conflicting.

Refresh note:

- Earlier review marked `evidence/dev_3_sft_dataformat_fix_plan.md` absent. That file now exists and is reviewed below.

## PR #30 Retry Failure Facts

PR #30:

- URL: `https://github.com/peteryang1/coding_agent_playground/pull/30`
- Task ID: `M1-SFT-RETRY-RUN-DEV4`
- Owner: `intern_code_dev_4`
- State at review: open, non-draft, `mergeable=CONFLICTING`, `mergeStateStatus=DIRTY`.
- Evidence path named by PR: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_retry_run.md`.
- Completion marker intended by PR: blocked-with-final-evidence after merge.

Retry facts from PR #30 body and durable milestone files:

- Run ID: `milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z`
- Config: `configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml`
- Dataset: `/root/workspace/cleaned_m1_sft_10/train.jsonl`
- Dataset sha256: `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`
- Base model: `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`
- Endpoint used: `ssh -p 23121 root@10.100.22.53`
- Exit status: `1`
- Failure signature: `KeyError: 'from'` during LLamaFactory dataset conversion.
- Artifacts present: run manifest, runtime config, stdout/stderr log, exit status file.
- Artifacts absent: checkpoint/model, `trainer_state.json`, `all_results.json`.

Interpretation from current durable records:

```text
OpenAI-style role/content messages were registered through ShareGPT defaults expecting from/value.
```

## Provenance / Schema Facts

The source SFT dataset contract is `coding_agent_playground_sft_v1`.

From `dev_3_sft_retry_data_gate.md`:

- First retry dataset is `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Count: `10`.
- Unique `example_id`: `10`.
- Unique `trajectory_id`: `10`.
- Split: `fastapi/fastapi=4`, `scikit-learn/scikit-learn=3`, `Textualize/rich=3`.
- Each row has `messages`, `example_id`, `trajectory_id`, repo/task metadata, and provenance.
- Messages are OpenAI-style objects with `role` and `content`.

From `convert_rollouts_to_sft.py`:

- Message roles are normalized into `system`, `user`, `assistant`, or `tool`.
- Each message is emitted as:

```json
{"role": "<role>", "content": "<content>"}
```

- The converter keeps provenance outside training text in fields such as `example_id`, `trajectory_id`, `repo`, `repo_path`, `task_id`, `source.raw_path`, and `metadata`.

## Expected Data-Format Fix Shape

The current failure can be fixed through one of two broad approaches:

1. **Registration-only fix**: keep `train.jsonl` in `coding_agent_playground_sft_v1` / OpenAI-style `role`/`content` format, and register LLamaFactory dataset parsing so it reads `messages[*].role` and `messages[*].content` rather than ShareGPT `from`/`value`.
2. **Data conversion fix**: produce a separate ShareGPT-compatible JSONL where each message is converted from `role`/`content` to `from`/`value`, while preserving every original trajectory/sample provenance field outside or alongside the converted conversation.

Preferred from a provenance perspective:

- Registration-only, if LLamaFactory supports the required OpenAI-style message mapping cleanly, because it preserves the canonical `coding_agent_playground_sft_v1` artifact and avoids creating a second training JSONL.

Acceptable fallback:

- ShareGPT converted JSONL, but only if it is explicitly versioned as a derived training artifact, includes row count/checksum, maps every original `example_id` and `trajectory_id`, and preserves repo/task/source metadata.

## Provenance / Schema Risks

Launch-blocking risk:

- `evidence/dev_3_sft_dataformat_fix_plan.md` is missing, so there is no reviewed dev_3 plan yet identifying the exact chosen fix path, sample before/after rows, checksum plan, or provenance preservation method.

Risks if using registration-only:

- LLamaFactory dataset_info mapping must explicitly target `messages` with `role` and `content`; if it still uses ShareGPT defaults, `KeyError: 'from'` will repeat.
- The plan must state whether roles `system`, `user`, `assistant`, and `tool` are all accepted. Current 10-example handoff has only `user` and `assistant`, but the broader schema allows `tool`; a future artifact could expose unsupported roles.
- If metadata is ignored by training loader, that is acceptable for training, but run manifests should still preserve `example_id` / `trajectory_id` for provenance.

Risks if using ShareGPT conversion:

- Role mapping must be deterministic. Likely mapping is `user -> human`, `assistant -> gpt`, with explicit handling for `system` and `tool` if present.
- Provenance loss is easy if the converted row contains only `conversations`. The derived file must preserve original `example_id`, `trajectory_id`, `repo`, `task_id`, and source paths.
- Converted file must not overwrite the canonical `/root/workspace/cleaned_m1_sft_10/train.jsonl` unless PM explicitly changes the data contract. It should be a new path with a new checksum.
- If `trajectory_id` is duplicated or transformed, mini-swe/SFT auditability weakens. Keep `trajectory_id` unchanged and use `example_id` as unique sample ID.

## Review Of dev_3 Fix Plan

Verdict: **reviewed; direction is acceptable as a no-execution plan, but launch remains blocked on concrete artifact/gate evidence**.

`evidence/dev_3_sft_dataformat_fix_plan.md` now exists. It identifies the failure as OpenAI-style `messages[*].role` / `messages[*].content` being read through a LLamaFactory ShareGPT path expecting `from` / `value`.

Plan facts reviewed:

- Task ID: `M1-SFT-DATAFORMAT-FIX-DEV3`
- Source dataset: `/root/workspace/cleaned_m1_sft_10/train.jsonl`
- Source checksum: `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`
- Source count: `10`
- Source split: `fastapi/fastapi=4`, `scikit-learn/scikit-learn=3`, `Textualize/rich=3`
- Preferred path: registration-only LLamaFactory dataset entry that keeps the canonical JSONL unchanged and maps `messages`, `role`, and `content`.
- Fallback path: derived ShareGPT-compatible JSONL at `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, with deterministic role mapping and top-level provenance preservation.

Registration-only review:

- Preferred registration-only path is provenance-preserving if the implemented `dataset_info.json` entry actually maps the canonical `messages` column and `role` / `content` tags used by `coding_agent_playground_sft_v1`.
- It keeps the original source checksum, row count, `example_id`, `trajectory_id`, repo/task metadata, and source provenance as the source of truth.
- It avoids a second derived training file, which is the lowest-risk provenance path.
- Remaining schema risk: dev_3 correctly notes that dev_4/test_1 must confirm the exact LLamaFactory version supports the proposed custom tag mapping. If the future launch still routes through ShareGPT defaults, `KeyError: 'from'` can repeat.
- Launch cannot proceed on the plan alone; the next package still needs the exact `dataset_info.json` path used by training, the dataset entry name wired into the config/launch wrapper, and preflight evidence that the loader resolves `role` / `content` instead of `from` / `value`.

ShareGPT fallback review:

- Fallback can preserve provenance if the derived artifact keeps every original row-level identifier and metadata field, especially `example_id`, `trajectory_id`, repo/task metadata, and source path/checksum references.
- Fallback must create a new derived path and checksum; it must not overwrite `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Schema alignment is not fully settled: dev_3's fallback sample uses top-level `messages` containing `from` / `value`, while `test_1_sft_dataformat_gate.md` expects ShareGPT conversion evidence with top-level `conversations` containing `from` / `value`.
- Before fallback launch, dev_3/dev_4/test_1 need to align on the exact LLamaFactory-compatible field name, likely `conversations` for the gate as currently written, and record sample validation against that schema.
- Role mapping for `system` and `tool` also needs explicit compatibility with the selected template/loader, even though the current 10-example retry path is documented as user/assistant only.

## Launch-Blocking Concerns

Current launch-blocking concerns:

1. PR #30 retry evidence is not merged into main yet; `dev_4_sft_retry_run.md` is absent from PM worktree and PR #30 is `CONFLICTING` / `DIRTY`.
2. dev_3 data-format fix plan is now reviewable, but it is a no-execution plan. No concrete registration artifact or converted JSONL artifact has been generated and validated in this evidence set.
3. `test_1_sft_dataformat_gate.md` says the gate definition/plan review is complete, but concrete artifact evidence remains pending.
4. Registration path still needs exact `dataset_info.json` path, dataset name, config/launch wrapper wiring, sample loader resolution, and proof that it avoids the previous `KeyError: 'from'`.
5. ShareGPT fallback still needs schema alignment between dev_3's fallback sample (`messages` with `from` / `value`) and test_1's expected fallback shape (`conversations` with `from` / `value`).
6. No new SFT retry should be authorized until the chosen artifact is produced, gated, and PM approves the next launch package.

Non-blocking facts:

- The original 10-example dataset provenance is documented and stable.
- The failure signature is coherent with OpenAI-style `role`/`content` messages being parsed by ShareGPT `from`/`value` defaults.
- No evidence suggests original trajectory provenance is already lost; the risk is in the next conversion/registration fix.

## Recommendation

Concise recommendation for PM gate:

```text
Do not authorize another SFT retry yet. dev_3_sft_dataformat_fix_plan.md now exists and the preferred registration-only direction is the lowest provenance-risk path, but the concrete artifact and test_1 gate evidence are still pending. Prefer registration-only if LLamaFactory can read role/content messages directly; otherwise require a derived ShareGPT JSONL with unchanged original example_id/trajectory_id provenance, explicit checksum, and schema aligned to the gate, especially conversations/from/value versus messages/from/value.
```

Minimum acceptance checks for the dev_3 plan:

- Names chosen path: registration-only or ShareGPT conversion.
- Includes sample original row and sample loader-ready row.
- Preserves original count `10` unless PM explicitly chooses repeated smoke data.
- Preserves `example_id`, `trajectory_id`, `repo`, `task_id`, and source provenance.
- Records output path and checksum for any derived JSONL.
- States how it avoids `KeyError: 'from'`.
- States whether canonical `coding_agent_playground_sft_v1` remains the source of truth.

## Completion Marker

Complete-with-updated-review: this refreshed review cites PR #30 retry failure facts, reviews the now-present `dev_3_sft_dataformat_fix_plan.md`, and finds the preferred registration-only path provenance-preserving if implemented with exact LLamaFactory dataset registration and config wiring. The ShareGPT fallback can preserve provenance only after schema alignment and checksum/sample/provenance proof. Launch remains blocked on concrete artifact evidence, test_1 gate completion, and PM approval. No remote experiments were run.
