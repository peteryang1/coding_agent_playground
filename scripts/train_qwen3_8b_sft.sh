#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_ID="${RUN_ID:-milestone1_qwen3_8b_sft_$(date -u +%Y%m%dT%H%M%SZ)}"
BASE_MODEL="${BASE_MODEL:-Qwen/Qwen3-8B}"
DATASET_JSONL="${DATASET_JSONL:-${REPO_ROOT}/data/sft/milestone1_coding_agent_sft.jsonl}"
DATASET_NAME="${DATASET_NAME:-}"
PREPROCESSING_NUM_WORKERS="${PREPROCESSING_NUM_WORKERS:-}"
CONFIG_TEMPLATE="${CONFIG_TEMPLATE:-${REPO_ROOT}/configs/train/qwen3_8b_sft.yaml}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/home/xu.yang/coding_agent_playground/outputs}"
RUN_DIR="${RUN_DIR:-${OUTPUT_ROOT}/runs/train/${RUN_ID}}"
CHECKPOINT_DIR="${CHECKPOINT_DIR:-${OUTPUT_ROOT}/training_summary/sft_output/${RUN_ID}}"
LLAMAFACTORY_DIR="${LLAMAFACTORY_DIR:-${REPO_ROOT}/code/LLamaFactory}"
LLAMAFACTORY_CLI="${LLAMAFACTORY_CLI:-llamafactory-cli}"
MCORE_ADAPTER_DIR="${MCORE_ADAPTER_DIR:-${REPO_ROOT}/code/mcore_adapter}"
DRY_RUN="${DRY_RUN:-1}"
TMPDIR="${TMPDIR:-${OUTPUT_ROOT}/tmp/${RUN_ID}}"
DEP_TARGET="${DEP_TARGET:-${PYTHON_DEPS_DIR:-${RUN_DIR}/python_deps}}"
LF="${LF:-${LLAMAFACTORY_DIR}}"

mkdir -p "${RUN_DIR}/logs" "${RUN_DIR}/config" "${CHECKPOINT_DIR}" "${TMPDIR}"

LOG_FILE="${LOG_FILE:-${RUN_DIR}/logs/train_stdout_stderr.log}"
XTRACE_FILE="${XTRACE_FILE:-${RUN_DIR}/logs/train_xtrace.log}"
DIAG_FILE="${DIAG_FILE:-${RUN_DIR}/early_exit_diagnostics.txt}"
EXIT_STATUS_FILE="${EXIT_STATUS_FILE:-${RUN_DIR}/exit_status.txt}"
PREFLIGHT_FILE="${PREFLIGHT_FILE:-${RUN_DIR}/preflight.json}"

export DATASET_NAME PREPROCESSING_NUM_WORKERS OUTPUT_ROOT RUN_DIR CHECKPOINT_DIR TMPDIR LOG_FILE XTRACE_FILE DIAG_FILE
export DEP_TARGET LF LLAMAFACTORY_CLI MCORE_ADAPTER_DIR

exec > >(tee -a "${LOG_FILE}") 2>&1
exec 9>>"${XTRACE_FILE}"
export BASH_XTRACEFD=9

artifact_summary() {
  find "${RUN_DIR}" -maxdepth 3 -type f -printf '%s %p\n' 2>/dev/null | sort || true
}

write_status() {
  local rc="$1"
  printf 'EXIT_STATUS=%s\nEND_UTC=%s\n' "${rc}" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "${EXIT_STATUS_FILE}"
}

write_diagnostics() {
  local rc="$1"
  local reason="$2"
  {
    printf 'DIAGNOSTIC_REASON=%s\n' "${reason}"
    printf 'ERROR_UTC=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'ERROR_EXIT=%s\n' "${rc}"
    printf 'ERROR_LINE=%s\n' "${BASH_LINENO[0]:-unknown}"
    printf 'ERROR_COMMAND=%s\n' "${BASH_COMMAND:-unknown}"
    printf 'RUN_ID=%s\nRUN_DIR=%s\nCHECKPOINT_DIR=%s\nOUTPUT_ROOT=%s\nTMPDIR=%s\n' \
      "${RUN_ID}" "${RUN_DIR}" "${CHECKPOINT_DIR}" "${OUTPUT_ROOT}" "${TMPDIR}"
    printf 'ARTIFACTS_BEGIN\n'
    artifact_summary
    printf 'ARTIFACTS_END\n'
  } | tee -a "${DIAG_FILE}"
}

on_err() {
  local rc=$?
  set +e
  write_diagnostics "${rc}" "ERR_TRAP"
  write_status "${rc}"
  exit "${rc}"
}

on_exit() {
  local rc=$?
  set +e
  if [[ ! -f "${EXIT_STATUS_FILE}" ]]; then
    write_status "${rc}"
  fi
  if [[ "${rc}" != "0" && ! -f "${DIAG_FILE}" ]]; then
    write_diagnostics "${rc}" "EXIT_TRAP"
  fi
}

trap on_err ERR
trap on_exit EXIT
if [[ "${SFT_XTRACE:-1}" == "1" ]]; then
  set -x
fi

printf 'START_UTC=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'RUN_ID=%s\nREPO_ROOT=%s\nOUTPUT_ROOT=%s\nRUN_DIR=%s\nCHECKPOINT_DIR=%s\nTMPDIR=%s\n' \
  "${RUN_ID}" "${REPO_ROOT}" "${OUTPUT_ROOT}" "${RUN_DIR}" "${CHECKPOINT_DIR}" "${TMPDIR}"
printf 'CONFIG_TEMPLATE=%s\nDATASET_JSONL=%s\nDATASET_NAME=%s\nPREPROCESSING_NUM_WORKERS=%s\nBASE_MODEL=%s\nLLAMAFACTORY_DIR=%s\nMCORE_ADAPTER_DIR=%s\nDRY_RUN=%s\n' \
  "${CONFIG_TEMPLATE}" "${DATASET_JSONL}" "${DATASET_NAME}" "${PREPROCESSING_NUM_WORKERS}" "${BASE_MODEL}" "${LLAMAFACTORY_DIR}" "${MCORE_ADAPTER_DIR}" "${DRY_RUN}"
printf 'LLAMAFACTORY_CLI=%s\nDEP_TARGET=%s\nLF=%s\n' "${LLAMAFACTORY_CLI}" "${DEP_TARGET}" "${LF}"
printf 'Mount proof for OUTPUT_ROOT:\n'
findmnt -T "${OUTPUT_ROOT}" || true
df -h "${OUTPUT_ROOT}" || true

python3 - "${PREFLIGHT_FILE}" "${CONFIG_TEMPLATE}" "${DATASET_JSONL}" "${OUTPUT_ROOT}" "${RUN_DIR}" "${CHECKPOINT_DIR}" "${TMPDIR}" "${LOG_FILE}" "${XTRACE_FILE}" <<'PY'
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


out, config, dataset, output_root, run_dir, checkpoint_dir, tmpdir, log_file, xtrace_file = map(Path, sys.argv[1:])
payload = {
    "cwd": os.getcwd(),
    "config_template": {"path": str(config), "exists": config.is_file(), "sha256": sha256_file(config)},
    "dataset": {"path": str(dataset), "exists": dataset.is_file(), "sha256": sha256_file(dataset)},
    "paths": {
        "output_root": str(output_root),
        "run_dir": str(run_dir),
        "checkpoint_dir": str(checkpoint_dir),
        "tmpdir": str(tmpdir),
        "log_file": str(log_file),
        "xtrace_file": str(xtrace_file),
    },
}
out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"Preflight: {out}")
PY

RUNTIME_CONFIG="${RUN_DIR}/config/qwen3_8b_sft.yaml"
python3 - "${CONFIG_TEMPLATE}" "${RUNTIME_CONFIG}" "${BASE_MODEL}" "${CHECKPOINT_DIR}" "${DATASET_NAME}" "${PREPROCESSING_NUM_WORKERS}" <<'PY'
from pathlib import Path
import sys

template, out, base_model, output_dir, dataset_name, preprocessing_num_workers = sys.argv[1:]
lines = Path(template).read_text(encoding="utf-8").splitlines()
rewritten = []
for line in lines:
    if line.startswith("model_name_or_path:"):
        rewritten.append(f"model_name_or_path: {base_model}")
    elif dataset_name and line.startswith("dataset:"):
        rewritten.append(f"dataset: {dataset_name}")
    elif preprocessing_num_workers and line.startswith("preprocessing_num_workers:"):
        rewritten.append(f"preprocessing_num_workers: {preprocessing_num_workers}")
    elif line.startswith("output_dir:"):
        rewritten.append(f"output_dir: {output_dir}")
    else:
        rewritten.append(line)
Path(out).write_text("\n".join(rewritten) + "\n", encoding="utf-8")
PY
printf 'Runtime config: %s\n' "${RUNTIME_CONFIG}"
sha256sum "${RUNTIME_CONFIG}"

export USE_MCA="${USE_MCA:-1}"
export FORCE_TORCHRUN="${FORCE_TORCHRUN:-1}"
export PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"
export TORCH_NCCL_AVOID_RECORD_STREAMS="${TORCH_NCCL_AVOID_RECORD_STREAMS:-1}"
export NCCL_DEBUG="${NCCL_DEBUG:-WARN}"
export DISABLE_VERSION_CHECK="${DISABLE_VERSION_CHECK:-1}"
export NVTE_FLASH_ATTN="${NVTE_FLASH_ATTN:-1}"
export NVTE_FUSED_ATTN="${NVTE_FUSED_ATTN:-0}"
export NVTE_UNFUSED_ATTN="${NVTE_UNFUSED_ATTN:-0}"

PYTHONPATH_PREFIX="${LLAMAFACTORY_DIR}/src"
if [[ -d "${MCORE_ADAPTER_DIR}" ]]; then
  PYTHONPATH_PREFIX="${MCORE_ADAPTER_DIR}:${PYTHONPATH_PREFIX}"
fi
export PYTHONPATH_PREFIX

LAUNCH_COMMAND="cd ${LLAMAFACTORY_DIR} && export DEP_TARGET=\"${DEP_TARGET}\" LF=\"${LF}\" MCORE_ADAPTER_DIR=\"${MCORE_ADAPTER_DIR}\" PYTHONPATH=\"${PYTHONPATH_PREFIX}:\${PYTHONPATH:-}\" && ${LLAMAFACTORY_CLI} train ${RUNTIME_CONFIG}"

python3 "${REPO_ROOT}/scripts/write_sft_run_manifest.py" \
  --run-id "${RUN_ID}" \
  --run-dir "${RUN_DIR}" \
  --config "${RUNTIME_CONFIG}" \
  --dataset "${DATASET_JSONL}" \
  --base-model "${BASE_MODEL}" \
  --output-dir "${CHECKPOINT_DIR}" \
  --checkpoint-dir "${CHECKPOINT_DIR}" \
  --dataset-name "${DATASET_NAME}" \
  --output-root "${OUTPUT_ROOT}" \
  --tmpdir "${TMPDIR}" \
  --log-file "${LOG_FILE}" \
  --xtrace-file "${XTRACE_FILE}" \
  --diag-file "${DIAG_FILE}" \
  --repo-root "${REPO_ROOT}" \
  --command "${LAUNCH_COMMAND}" \
  --notes "Milestone 1 Qwen3-8B SFT launch manifest. Dataset may be produced later by dev_3." \
  --out "${RUN_DIR}/run_manifest.json"
printf 'Run manifest: %s\n' "${RUN_DIR}/run_manifest.json"
sha256sum "${RUN_DIR}/run_manifest.json"

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
sha256sum "${DATASET_JSONL}"
if ! command -v nvidia-smi >/dev/null 2>&1; then
  printf 'nvidia-smi not found; run on allocated GPU node, not CPU login node.\n' >&2
  exit 3
fi
nvidia-smi -L
if [[ ! -d "${LLAMAFACTORY_DIR}" ]]; then
  printf 'Missing LLamaFactory directory: %s\n' "${LLAMAFACTORY_DIR}" >&2
  exit 4
fi
if [[ "${USE_MCA}" == "1" ]]; then
  export PYTHONPATH="${PYTHONPATH_PREFIX}:${PYTHONPATH:-}"
  if ! python3 - <<'PY'
import importlib.util
import sys

if importlib.util.find_spec("mcore_adapter") is None:
    sys.exit(1)
PY
  then
    printf 'mcore_adapter import failed while USE_MCA=1.\n' >&2
    printf 'Provide mcore_adapter via a local/provided dependency bundle, for example code/mcore_adapter or an installed package in the transferred environment.\n' >&2
    printf 'Remote GPU/LTP nodes must not git clone/fetch or download dependencies; prepare and checksum the bundle locally, transfer it, then verify on-node before launching SFT.\n' >&2
    exit 5
  fi
  printf 'mcore_adapter import OK for USE_MCA=1.\n'
fi

cd "${LLAMAFACTORY_DIR}"
export DEP_TARGET="${DEP_TARGET}"
export LF="${LF}"
export MCORE_ADAPTER_DIR="${MCORE_ADAPTER_DIR}"
export PYTHONPATH="${PYTHONPATH_PREFIX}:${PYTHONPATH:-}"
"${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"
