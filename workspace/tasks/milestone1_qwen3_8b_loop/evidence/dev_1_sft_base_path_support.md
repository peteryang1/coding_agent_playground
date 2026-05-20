# Dev 1 SFT Base Path Support Evidence

Owner: `intern_code_dev_1`  
Task ID: `M1-SFT-BASEPATH-DEV1`
Date: 2026-05-20  
Scope: read-only support for clean Qwen3-8B base model path selection on corrected workspace host.  
Corrected host: `ssh -p 31787 root@10.100.194.40`  
Status: Completed. Candidate exists that can unblock dev_4, with caveat below.

## Summary

Recommended candidate to unblock dev_4:

```text
/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

Classification: **clean-base candidate**.

Reason: directory is present, contains a complete HF-style Qwen3 8B model layout (`config.json`, tokenizer files, `model.safetensors.index.json`, 5 safetensor shards), config reports `model_type=qwen3`, `architectures=['Qwen3ForCausalLM']`, `num_hidden_layers=36`, `hidden_size=4096`, and no `trainer_state.json`, `training_args.bin`, `adapter_config.json`, `train_results.json`, or `all_results.json` markers were present.

Caveat: this is a local full-weight base candidate, not the broken registry symlink path. The nominal registry/source id remains `Qwen/Qwen3-8B`.

## Commands Checked

All commands were read-only except stopping my own broad `find` probe after it had already produced useful output and was still scanning large shared roots. No model files, caches, rollout outputs, or workspace repos were modified.

```bash
ssh -p 31787 root@10.100.194.40 'ls -la /root/workspace'
ssh -p 31787 root@10.100.194.40 'find /mnt/3fs/data/ai4ai/models/Qwen -maxdepth 3 -mindepth 1 -print'
ssh -p 31787 root@10.100.194.40 'find /root/.cache/huggingface /root/.cache/modelscope -maxdepth 5 \( -iname "*Qwen3*8B*" -o -iname "*qwen3*8b*" -o -iname "*Qwen3-8B*" \) -print'
ssh -p 31787 root@10.100.194.40 'grep -Il "Qwen3\|qwen3\|Qwen/Qwen" ... /root/workspace/axrd /root/workspace/coding_agent_playground /root/workspace/finetune_data'
ssh -p 31787 root@10.100.194.40 'python3 - <<PY ... inspect candidate model directories, marker files, config.json, tokenizer files, safetensor shards ... PY'
ssh -p 31787 root@10.100.194.40 'sed -n "1,220p" /root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft.yaml'
ssh -p 31787 root@10.100.194.40 'sed -n "1,260p" /root/workspace/coding_agent_playground/docs/training/qwen3_8b_sft_pipeline.md'
ssh -p 31787 root@10.100.194.40 'python3 - <<PY ... print /root/workspace/axrd/ai4ai/model_registry.json entry for Qwen/Qwen3-8B ... PY'
```

## Model Registry Evidence

`/root/workspace/axrd/ai4ai/model_registry.json` contains a `Qwen/Qwen3-8B` entry:

- `hf_model_id`: `Qwen/Qwen3-8B`
- `model_type`: `qwen3`
- `architecture`: `Qwen3ForCausalLM`
- `parameter_count`: `8.2B`
- `native_context_len`: `32768`
- `config_max_position_embeddings`: `40960`
- `known_chat_template`: `qwen3`
- `torch_dtype`: `bfloat16`

Training config evidence:

- `/root/workspace/coding_agent_playground/configs/train/qwen3_8b_sft.yaml` sets `model_name_or_path: Qwen/Qwen3-8B`.
- `/root/workspace/coding_agent_playground/docs/training/qwen3_8b_sft_pipeline.md` says the base model is `Qwen/Qwen3-8B` by default, overridable with `BASE_MODEL`.

## Candidate Classification

| Candidate path | Observed evidence | Classification | Use for dev_4? |
|----------------|-------------------|----------------|----------------|
| `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` | Exists. `config.json`, `tokenizer_config.json`, `generation_config.json`, `model.safetensors.index.json`, 5 `model-0000*-of-00005.safetensors` shards. Config: `model_type=qwen3`, `architectures=['Qwen3ForCausalLM']`, `num_hidden_layers=36`, `hidden_size=4096`, `vocab_size=151936`, `transformers_version=4.57.1`. No training/adapter marker files found. | Clean-base candidate | Yes. Recommended local path for `BASE_MODEL` if direct HF id/network is not desired. |
| `Qwen/Qwen3-8B` | Registry/source id in `model_registry.json`, training config, and SFT docs. | Clean base id | Yes if runtime can resolve/download from Hugging Face or local cache is repaired. |
| `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` | Symlink exists but target `/mnt/3fs/data/ai4ai/axis_ref/research_hub/models/qwen3-8b/snapshot` is missing on corrected host. | Broken clean-base alias | No until symlink target is restored. |
| `/root/.cache/huggingface/hub/models--Qwen--Qwen3-8B` | Cache dir exists with `refs/main` and snapshot `b968826d9c46dd6066d109eabc6255188de91218`, but snapshot has only `tokenizer.json`, `tokenizer_config.json`, and `vocab.json`; no `config.json`, no weights. | Incomplete clean-base cache | No. Not sufficient for SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260422_2219_qwen3-8b_1bench_060b-ckpt320` | Full Qwen3 8B-shaped model files, but path contains `ckpt320`. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260423_2332_qwen3-8b_1bench_4fe9-ckpt*` | Full Qwen3 8B-shaped model files, but checkpoint suffixes. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260424_2310_qwen3-8b_1bench_2457` | Full Qwen3 8B-shaped model files with no direct training marker files, but belongs to a historical run family that also has `-ckpt32`, `-sft`, and `-sft-hf` siblings. | Historical/ambiguous warm-start risk | Not recommended while cleaner `ws_20260422_2156...` exists. |
| `/mnt/3fs/data/ai4ai/models/ws_20260424_2310_qwen3-8b_1bench_2457-sft-hf` | Has `train_results.json` / `all_results.json` markers and SFT suffix. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260424_2330_qwen3-8b_1bench_d0e5-sft-lr*` | SFT/lr suffixes and training markers. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260425_0112_qwen3-8b_1bench_6c58_*` | Epoch/lr/full/min/v2 naming, some with training markers. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260425_0128_qwen3-8b_1bench_ef61-ckpt*` | Checkpoint suffixes. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260425_0145_qwen3-8b_1bench_a195-epoch*` | Epoch suffixes and training markers. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-ep1/final/runb-*` | Epoch/final/run naming. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260425_0923_qwen3-8b_0bench_e9b0-step*` | Step suffixes. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260426_0140_qwen3-8b_1bench_ba0f-ckpt*` | Checkpoint suffixes. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260426_0217_qwen3-8b_1bench_29a2-rl-step32` | RL/step suffix. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260426_0217_qwen3-8b_1bench_29a2-sft-hf` | SFT suffix and incomplete tokenizer markers. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260427_0214_qwen3-8b_1bench_bd5d-ckpt*` | Checkpoint suffixes. | Historical/warm-start | No for clean-base SFT. |
| `/mnt/3fs/data/ai4ai/models/ws_20260428_0302_qwen3-8b_1bench_d60f-sft` and `/mnt/3fs/data/ai4ai/models/ws_20260428_0325_qwen3-8b_1bench_e46e-sft` | SFT suffixes; `e46e-sft` has training markers. | Historical/warm-start | No for clean-base SFT. |

## Recommendation for dev_4

Use:

```bash
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

This should unblock the base-model path requirement for SFT pipeline dry-run/config materialization. It does not remove the separate GPU allocation blocker recorded elsewhere.

Do not use these as clean bases:

- `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` until the broken symlink target is restored.
- `/root/.cache/huggingface/hub/models--Qwen--Qwen3-8B` until the snapshot includes config and model weights.
- Any `qwen3-8b` path containing `ckpt`, `sft`, `epoch`, `step`, `lr`, `rl`, `final`, or training result marker files.

## Blockers

No blocker for selecting a usable local clean-base candidate. Remaining known blocker for actual SFT launch is GPU allocation / allocated node availability, not base-model path discovery.
