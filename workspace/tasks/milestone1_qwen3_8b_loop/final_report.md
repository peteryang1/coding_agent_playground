# Milestone 1 Final Report Draft

## Summary

Milestone 1 has completed the rollout and data-cleaning portions of the end-to-end smoke loop on the corrected final workspace `ssh -p 31787 root@10.100.194.40`.

The old 300/100-per-repo rollout was stopped and marked scratch-only. The active scope is 10 total complete coding-process trajectories.

## Data

Selected repos:

| Repo | Category | Final workspace path | Commit |
|------|----------|----------------------|--------|
| `fastapi/fastapi` | Web API framework | `/root/workspace/fastapi` | `f4cafbc` |
| `scikit-learn/scikit-learn` | Machine learning library | `/root/workspace/scikit-learn` | `ffc6cdc` |
| `Textualize/rich` | CLI/terminal rendering library | `/root/workspace/rich` | `46cebbb` |

Rollout artifacts:

```text
/root/workspace/rollouts_m1_10
/root/workspace/rollouts_m1_10/manifest.jsonl
/root/workspace/rollouts_m1_10/complete_process_validation.json
```

Validation result:

```text
manifest_entries 10
checked_count 10
valid_count 10
invalid_count 0
```

Cleaned SFT dataset:

```text
/root/workspace/cleaned_m1_sft_10/train.jsonl
/root/workspace/cleaned_m1_sft_10/rejected.jsonl
/root/workspace/cleaned_m1_sft_10/conversion_summary.json
```

Cleaning result:

```text
input_count 10
kept_count 10
dropped_count 0
error_count 0
fastapi/fastapi 4
scikit-learn/scikit-learn 3
Textualize/rich 3
```

## SFT

SFT command dry-run has passed using the 10-example cleaned dataset.

```text
run_id milestone1_qwen3_8b_sft_smoke_cmd_20260520
manifest /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/run_manifest.json
dataset /root/workspace/cleaned_m1_sft_10/train.jsonl
data.train_sha256 f91d0b096537564f136576dd7f3bb5f54750aafb524c7f890be621d557ddd0c2
artifacts.checkpoint_dir /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_smoke_cmd_20260520
```

Real SFT launch is not yet executed. Current blockers:

- `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is a broken symlink on the corrected final workspace.
- The corrected entry host has no `nvidia-smi`; a GPU node or current milestone `nodes.json` is required.
- Historical Qwen3-8B checkpoints are readable but are not clean base checkpoints unless PM/supervisor explicitly chooses warm-start.
- After Session 6 supervisor correction, PM will not run SFT or remote experiments directly; dev_4 owns execution evidence and PM gates the durable result.

## Evaluation

mini-swe-agent smoke readiness is prepared using the source checkout and Singularity backend.

```text
readiness_metrics /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json
working_dir /root/workspace/swe-bench-related/mini-swe-agent
config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml
backend singularity
subset lite
split dev
slice 0:2
```

Prepared command:

```bash
cd /root/workspace/swe-bench-related/mini-swe-agent
uv run --with datasets mini-extra swebench \
  --config /root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml \
  --subset lite \
  --split dev \
  --slice 0:2 \
  --model "<SFT_SMOKE_MODEL_OR_CHECKPOINT>" \
  --environment-class singularity \
  --workers 1 \
  --output /root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke
```

Evaluation smoke is blocked until an SFT smoke model/checkpoint or endpoint exists.

After Session 6 supervisor correction, test_2 owns mini-swe-agent smoke execution once dev_4 supplies a usable model/checkpoint/endpoint; PM gates the durable evidence rather than running the command directly.

## Metrics

```json
{
  "run_id": "milestone1_mini_swe_smoke_readiness_20260520",
  "model_name_or_path": null,
  "agent": "mini-swe-agent",
  "benchmark": "SWE-bench lite dev slice 0:2",
  "split": "dev",
  "backend": "singularity",
  "total_instances": 2,
  "instances_submitted": 0,
  "instances_completed": 0,
  "instances_resolved": 0,
  "resolution_rate": 0.0,
  "predictions_path": null,
  "results_json_path": null,
  "instance_results_path": null,
  "logs_path": "/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke",
  "status": "blocked"
}
```
