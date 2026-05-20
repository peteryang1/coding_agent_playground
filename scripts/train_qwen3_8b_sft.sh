#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_ID="${RUN_ID:-milestone1_qwen3_8b_sft_$(date -u +%Y%m%dT%H%M%SZ)}"
BASE_MODEL="${BASE_MODEL:-Qwen/Qwen3-8B}"
DATASET_JSONL="${DATASET_JSONL:-${REPO_ROOT}/data/sft/milestone1_coding_agent_sft.jsonl}"
CONFIG_TEMPLATE="${CONFIG_TEMPLATE:-${REPO_ROOT}/configs/train/qwen3_8b_sft.yaml}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/mnt/3fs/data/ai4ai/outputs/coding_agent_playground}"
RUN_DIR="${RUN_DIR:-${OUTPUT_ROOT}/runs/train/${RUN_ID}}"
CHECKPOINT_DIR="${CHECKPOINT_DIR:-${OUTPUT_ROOT}/training_summary/sft_output/${RUN_ID}}"
LLAMAFACTORY_DIR="${LLAMAFACTORY_DIR:-${REPO_ROOT}/code/LLamaFactory}"
DRY_RUN="${DRY_RUN:-1}"

mkdir -p "${RUN_DIR}/logs" "${RUN_DIR}/config" "${CHECKPOINT_DIR}"

RUNTIME_CONFIG="${RUN_DIR}/config/qwen3_8b_sft.yaml"
python3 - "${CONFIG_TEMPLATE}" "${RUNTIME_CONFIG}" "${BASE_MODEL}" "${CHECKPOINT_DIR}" <<'PY'
from pathlib import Path
import sys

template, out, base_model, output_dir = sys.argv[1:]
lines = Path(template).read_text(encoding="utf-8").splitlines()
rewritten = []
for line in lines:
    if line.startswith("model_name_or_path:"):
        rewritten.append(f"model_name_or_path: {base_model}")
    elif line.startswith("output_dir:"):
        rewritten.append(f"output_dir: {output_dir}")
    else:
        rewritten.append(line)
Path(out).write_text("\n".join(rewritten) + "\n", encoding="utf-8")
PY

export USE_MCA="${USE_MCA:-1}"
export FORCE_TORCHRUN="${FORCE_TORCHRUN:-1}"
export PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"
export TORCH_NCCL_AVOID_RECORD_STREAMS="${TORCH_NCCL_AVOID_RECORD_STREAMS:-1}"
export NCCL_DEBUG="${NCCL_DEBUG:-WARN}"
export DISABLE_VERSION_CHECK="${DISABLE_VERSION_CHECK:-1}"
export NVTE_FLASH_ATTN="${NVTE_FLASH_ATTN:-1}"
export NVTE_FUSED_ATTN="${NVTE_FUSED_ATTN:-0}"
export NVTE_UNFUSED_ATTN="${NVTE_UNFUSED_ATTN:-0}"

LAUNCH_COMMAND="cd ${LLAMAFACTORY_DIR} && export PYTHONPATH=\"${LLAMAFACTORY_DIR}/src:\${PYTHONPATH:-}\" && llamafactory-cli train ${RUNTIME_CONFIG}"

python3 "${REPO_ROOT}/scripts/write_sft_run_manifest.py" \
  --run-id "${RUN_ID}" \
  --run-dir "${RUN_DIR}" \
  --config "${RUNTIME_CONFIG}" \
  --dataset "${DATASET_JSONL}" \
  --base-model "${BASE_MODEL}" \
  --output-dir "${CHECKPOINT_DIR}" \
  --checkpoint-dir "${CHECKPOINT_DIR}" \
  --repo-root "${REPO_ROOT}" \
  --command "${LAUNCH_COMMAND}" \
  --notes "Milestone 1 Qwen3-8B SFT launch manifest. Dataset may be produced later by dev_3." \
  --out "${RUN_DIR}/run_manifest.json"

if [[ "${DRY_RUN}" == "1" ]]; then
  printf 'DRY_RUN=1; not launching training.\n'
  printf 'Runtime config: %s\n' "${RUNTIME_CONFIG}"
  printf 'Run manifest: %s\n' "${RUN_DIR}/run_manifest.json"
  printf 'Launch command:\n  %s\n' "${LAUNCH_COMMAND}"
  exit 0
fi

if [[ ! -f "${DATASET_JSONL}" ]]; then
  printf 'Missing DATASET_JSONL: %s\n' "${DATASET_JSONL}" >&2
  exit 2
fi
if ! command -v nvidia-smi >/dev/null 2>&1; then
  printf 'nvidia-smi not found; run on allocated GPU node, not CPU login node.\n' >&2
  exit 3
fi
if [[ ! -d "${LLAMAFACTORY_DIR}" ]]; then
  printf 'Missing LLamaFactory directory: %s\n' "${LLAMAFACTORY_DIR}" >&2
  exit 4
fi

cd "${LLAMAFACTORY_DIR}"
export PYTHONPATH="${LLAMAFACTORY_DIR}/src:${PYTHONPATH:-}"
exec llamafactory-cli train "${RUNTIME_CONFIG}"
