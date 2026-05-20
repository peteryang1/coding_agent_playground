# Dev 1 SFT Failure Review

Owner: `intern_code_dev_1`
Task ID: `M1-SFT-FAILURE-REVIEW-DEV1`
Date: 2026-05-20
Scope: independent durable review of merged SFT failure evidence after PR #18/#23. No remote experiments were run.

## Sources Reviewed

- `evidence/dev_4_sft_smoke_run.md`
- `evidence/dev_3_sft_input_handoff.md`
- `evidence/dev_2_gpu_lifecycle.md`
- `blockers.md`
- `task_registry.md`
- `status.md`

PR/task state cited by durable files:

- PR #18 merged at `2026-05-20T10:18:04Z`, merge commit `1c3a3e23921dd3fc91b340f9b67f83c747d42948`.
- PR #23 merged at `2026-05-20T10:20:28Z`, merge commit `3ccabb573aecccdb71fe8d296643e6816b3ed22e`.
- Task `M1-SFT-SMOKE-DEV4` is blocked-with-final-evidence: real SFT smoke was attempted, but no checkpoint/model, `trainer_state.json`, or `all_results.json` was produced.

## Failure Summary

`dev_4_sft_smoke_run.md` records three attempts:

| Attempt | Run ID | Result | Root failure |
|---------|--------|--------|--------------|
| 1 | `milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T093916Z` | Exit `1`; no checkpoint/model | `ValueError: Cannot open data/sft/dataset_info.json` |
| 2 | `milestone1_qwen3_8b_sft_cleanbase_smoke_20260520T094003Z` | Exit `1`; no checkpoint/model | `ZeroDivisionError` in `mcore_adapter/trainer/trainer.py` when computing epoch progress; tiny 10-example dataset with DP=8/drop_last yields zero effective steps per epoch |
| 3 | `milestone1_qwen3_8b_sft_cleanbase_smoke_tp8_20260520T094336Z` | Exit `1`; no checkpoint/model | Megatron scheduler assertion: `assert self.lr_warmup_steps < self.lr_decay_steps` for TP=8/DP=1/max_steps=1 bounded retry |

## Sanity Check By Axis

### Data Side

Evidence from `dev_3_sft_input_handoff.md`:

- `/root/workspace/cleaned_m1_sft_10/train.jsonl` exists as the Milestone 1 smoke SFT input.
- SHA-256: `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`.
- 10 kept examples, 0 dropped, 0 errors, 0 rejects.
- Complete-process gate: 10 checked, 10 valid, 0 invalid.
- Format: `coding_agent_playground_sft_v1`.

Conclusion: no evidence of malformed data or conversion failure. Data quantity is intentionally tiny and can trigger trainer/drop-last behavior, but that is not a data correctness defect. Data-side mitigation may be useful only as a smoke-specific workaround if config-side changes cannot make tiny data safe.

### Resource Side

Evidence from `dev_4_sft_smoke_run.md` and `dev_2_gpu_lifecycle.md`:

- Approved GPU endpoint `ssh -p 39314 root@10.100.20.37` was reachable during SFT.
- 8 H200 GPUs were present and initialized.
- Attempt 2 entered training with 8 distributed tasks and total optimization steps `2`.
- Attempt 3 initialized tensor model parallel size `8`.
- GPU processes were cleaned up after failures.
- Dev_2 released the LTP allocation and preserved outputs under `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground`.

Conclusion: no evidence that the failure was caused by missing GPU resource, bad node health, or stale process cleanup. A new GPU allocation is required only after config/test gates approve a retry; it is not the next root-cause work item.

### Config / Trainer Side

Evidence from `dev_4_sft_smoke_run.md`:

- Attempt 1 was a missing dataset registration/config path issue.
- Attempt 2 progressed past data/model/dependency checks and failed inside MCA trainer epoch math because effective steps per epoch became zero under DP=8/drop_last with 10 examples.
- Attempt 3 deliberately changed to TP=8/DP=1/max_steps=1 and progressed farther, then failed because Megatron scheduler rejects the 1-step LR schedule.

Conclusion: current blocker is config-side, specifically tiny-data-safe MCA/Megatron/LLamaFactory smoke configuration.

## Inconsistencies / Ambiguities

- `dev_4_sft_smoke_run.md` says under "Dependency setup" that dataset registration was added on the GPU endpoint, but Attempt 1 later failed with `ValueError: Cannot open data/sft/dataset_info.json` and records registration as the action taken after that failure. The likely interpretation is that registration was completed after Attempt 1, then documented in the precheck/setup section. This is a documentation-order ambiguity, not a contradiction affecting root cause.
- Attempt 2 says "Entered training with total optimization steps = 2" but also fails because `steps_in_epoch=0`. This is plausible if the global scheduler/optimization-step estimate differs from per-rank dataloader steps after DP/drop_last. It should be explicitly verified in any config-fix plan by logging per-rank dataloader length/effective batch math.
- Attempt 3 rationale says TP=8/DP=1 and `max_steps=1` avoids data-parallel splitting, but the scheduler assertion proves `max_steps=1` is not a valid MCA/Megatron smoke setting. This is not an evidence inconsistency; it is a failed mitigation.

## Recommendation For Next PM Gate

Primary next gate: **config-side**.

PM should gate `M1-SFT-CONFIG-FIX-DEV4` before authorizing any fresh GPU job. Required acceptance points for that package:

- Cite the two post-registration root failures: DP=8/drop_last zero effective epoch steps and TP=8/max_steps=1 scheduler assertion.
- Provide a tiny-data-safe config diff or command that avoids both prior failures.
- Include explicit expected scheduler values, effective DP/TP layout, global batch/gradient accumulation, and per-rank minimum dataloader steps.
- Use at least `max_steps>=2` or an equivalent scheduler setting where warmup steps are strictly less than decay steps; if warmup is zero, state the exact LLamaFactory/MCA field used.
- Preserve clean base path `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` and dataset path `/root/workspace/cleaned_m1_sft_10/train.jsonl`.
- Define stop conditions and expected artifacts: run manifest, copied config, log, checkpoint/model or explicit failed assertion.

Secondary gates:

- **Data-side**: keep `M1-SFT-DATA-MITIGATION-DEV3` open as a fallback or supporting option. Data expansion/repetition can make DP=8/drop_last safer, but should be smoke-only and must preserve the 10 original trajectory provenance. It should not be the first gate because Attempt 3 shows a config scheduler issue even after avoiding DP=8 splitting.
- **Resource-side**: keep `M1-GPU-RETRY-RESOURCE-DEV2` blocked until config/test gates pass. The prior resource worked and was correctly released; starting another GPU job before a config fix would likely reproduce failure.
- **Test gate**: require `M1-SFT-RETRY-GATE-TEST1` to assert the retry config avoids the exact prior log signatures before PM authorizes the GPU run.

Concise PM decision recommendation:

```text
Next attempt should be config-side first. Do not authorize a fresh GPU resource until dev_4 provides a tiny-data-safe MCA/Megatron config package and test_1 defines retry pass/fail gates. Data mitigation is fallback/supporting; resource is not root cause.
```

## Completion Marker

Complete: this review cites merged SFT evidence, identifies documentation ambiguities, classifies the blocker as config-side first, and provides a next PM gate recommendation without running remote experiments.
