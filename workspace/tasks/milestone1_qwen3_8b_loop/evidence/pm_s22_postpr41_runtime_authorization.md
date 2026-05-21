# PM S22 Post-PR41 Runtime Authorization

Owner: `intern_code_pm`
Date: 2026-05-21
Task: `M1-S22-POSTPR41-SFT-RUNTIME-DEV2`
Authorized runtime owner: `intern_code_dev_2`

## Decision

`AUTHORIZED_ONE_OWNER_RUN`

PM authorizes only `intern_code_dev_2` to submit one fresh LTP job and run one Qwen3-8B ShareGPT SFT smoke after PR #41 merge.

This authorization does not permit any other owner to run LTP, SFT, GPU, eval, or dry-run launch. It does not authorize mini-swe eval.

## Gate Basis

- PR #41 is merged.
  - URL: `https://github.com/peteryang1/coding_agent_playground/pull/41`
  - mergedAt: `2026-05-21T10:00:25Z`
  - merge commit: `2fc4b797a85c9375c6c5e1171963abe67aab35e8`
- PR #41 fixes the post-PR39 dataset map blocker by forcing the 10-row ShareGPT smoke to in-process/single-process preprocessing.
- `intern_code_dev_1` evidence `evidence/dev_1_s22_dataset_map_review.md` records `PASS_FOR_PM_RETRY`.
- `intern_code_test_1` evidence `evidence/test_1_s22_postpatch_sft_runtime_gate.md` records `PASS_FOR_PM_RETRY`.
- `intern_code_dev_3` evidence `evidence/dev_3_s22_dataset_map_data_confirm.md` confirms no ShareGPT data content/schema change is needed.
- Prior post-PR39 LTP frame is stopped/released, and no complete checkpoint/model exists.

## Required Runtime Contract

- Use merged `main` including PR #41 merge commit `2fc4b797a85c9375c6c5e1171963abe67aab35e8`.
- Dataset: `coding_agent_m1_sft_10_sharegpt`.
- Accepted source data: `/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl`, sha256 `26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2`.
- ShareGPT mapping: `messages[*].from/value`.
- SFT output root: `/home/xu.yang/coding_agent_playground/outputs`.
- Store SFT launch outputs, temporary converted datasets, logs, checkpoints, run metadata, capacity probes, and intermediates under `/home/xu.yang`.
- Non-`/home/xu.yang` paths are allowed only for existing required inputs with explicit justification in evidence.
- Preserve PR #39 diagnostics and PR #41 preprocessing proof in runtime artifacts: preflight, generated config, run manifest, stdout/stderr log, xtrace, diagnostics, exit status, and manifest preprocessing worker fields.

## Required Evidence From dev_2

`intern_code_dev_2` must update:

- `evidence/dev_2_s22_postpr41_sft_runtime.md`
- `evidence/gpu_s22_postpr41_runtime_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`

Evidence must include:

- LTP job/frame id, node id, endpoint, `nodes.json`, submit/status/ssh/stop commands.
- `/home/xu.yang` mount/path proof and capacity/write probe under `/home/xu.yang/coding_agent_playground/outputs`.
- Exact command, environment, config path, generated config, dataset_info entry, base model path, run id, output root, run dir, checkpoint dir, log file, xtrace file, diagnostic file, manifest path, and exit status.
- Runtime proof that preprocessing uses the PR #41 single-process policy.
- Complete checkpoint/model path, file listing, sizes, and checksum or equivalent integrity proof; `trainer_state.json`; `all_results.json`.
- If no checkpoint is produced, a fresh exact runtime blocker with command, logs, node status, owner, stop proof, and next fix.
- Stop/release proof for the LTP frame after success or failure.

## Stop Conditions

dev_2 must stop/release the node when:

- a complete checkpoint/model is produced and evidence is captured;
- the run fails and no fresh PM retry authorization exists;
- the node becomes idle without active owner progress;
- PM/test gate orders stop.

## PM Boundary

PM did not submit LTP, run SFT, occupy GPU, run remote workspace code, or run eval.

## Completion Marker

```yaml
authorization: AUTHORIZED_ONE_OWNER_RUN
task_id: M1-S22-POSTPR41-SFT-RUNTIME-DEV2
authorized_owner: intern_code_dev_2
pr41_merged: true
pr41_merge_commit: 2fc4b797a85c9375c6c5e1171963abe67aab35e8
dataset: coding_agent_m1_sft_10_sharegpt
output_root: /home/xu.yang/coding_agent_playground/outputs
eval_authorized: false
pm_ran_ltp_sft_gpu_eval: false
required_next_result: checkpoint_or_fresh_exact_runtime_blocker
```
