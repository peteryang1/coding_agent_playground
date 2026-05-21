#!/usr/bin/env python3
"""Write a reproducible SFT run manifest without third-party dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit(repo: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None


def read_simple_yaml_scalars(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            values[key] = value
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--checkpoint-dir", required=True)
    parser.add_argument("--dataset-name", default=None)
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--tmpdir", default=None)
    parser.add_argument("--log-file", default=None)
    parser.add_argument("--xtrace-file", default=None)
    parser.add_argument("--diag-file", default=None)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--launcher", default="llamafactory-cli train")
    parser.add_argument("--command", action="append", default=[])
    parser.add_argument("--notes", default="")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    config = Path(args.config).resolve()
    dataset = Path(args.dataset).resolve()
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    config_values = read_simple_yaml_scalars(config)
    run_dir = Path(args.run_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    checkpoint_dir = Path(args.checkpoint_dir).resolve()
    output_root = Path(args.output_root).resolve() if args.output_root else None
    tmpdir = Path(args.tmpdir).resolve() if args.tmpdir else None
    log_file = Path(args.log_file).resolve() if args.log_file else run_dir / "logs" / "train_stdout_stderr.log"
    xtrace_file = Path(args.xtrace_file).resolve() if args.xtrace_file else run_dir / "logs" / "train_xtrace.log"
    diag_file = Path(args.diag_file).resolve() if args.diag_file else run_dir / "early_exit_diagnostics.txt"

    manifest = {
        "run_id": args.run_id,
        "run_type": "sft",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo_root),
        "git_commit": git_commit(repo_root),
        "base_model": args.base_model,
        "trainer": {
            "backend": "LLamaFactory",
            "launcher": args.launcher,
            "template": "qwen3",
            "finetuning_type": "full",
            "uses_mca": True,
        },
        "data": {
            "train_path": str(dataset),
            "train_sha256": sha256_file(dataset),
            "format": "sharegpt",
            "source": "coding_agent_playground normalized trajectories",
        },
        "config": {
            "path": str(config),
            "sha256": sha256_file(config),
        },
        "artifacts": {
            "run_dir": str(run_dir),
            "output_dir": str(output_dir),
            "checkpoint_dir": str(checkpoint_dir),
            "manifest": str(out),
            "logs": str(run_dir / "logs"),
            "metrics": str(run_dir / "metrics.json"),
            "tensorboard": str(output_dir / "runs"),
        },
        "checkpoint_policy": {
            "save_steps": config_values.get("save_steps"),
            "save_total_limit": config_values.get("save_total_limit"),
            "save_only_model": config_values.get("save_only_model"),
            "save_hf_model": config_values.get("save_hf_model"),
            "output_dir": config_values.get("output_dir"),
            "pin_best_before_resume": True,
            "final_model_symlink": "training_summary/model",
        },
        "preflight": {
            "config_exists": config.is_file(),
            "dataset_exists": dataset.is_file(),
            "output_root": str(output_root) if output_root else os.environ.get("OUTPUT_ROOT"),
            "run_dir": str(run_dir),
            "checkpoint_dir": str(checkpoint_dir),
            "tmpdir": str(tmpdir) if tmpdir else os.environ.get("TMPDIR"),
            "dataset_name": args.dataset_name if args.dataset_name is not None else os.environ.get("DATASET_NAME"),
            "preprocessing_num_workers": config_values.get("preprocessing_num_workers"),
            "log_file": str(log_file),
            "xtrace_file": str(xtrace_file),
            "early_exit_diagnostics": str(diag_file),
        },
        "environment": {
            "USE_MCA": os.environ.get("USE_MCA"),
            "FORCE_TORCHRUN": os.environ.get("FORCE_TORCHRUN"),
            "PYTORCH_CUDA_ALLOC_CONF": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"),
            "NCCL_DEBUG": os.environ.get("NCCL_DEBUG"),
            "DISABLE_VERSION_CHECK": os.environ.get("DISABLE_VERSION_CHECK"),
            "NVTE_FLASH_ATTN": os.environ.get("NVTE_FLASH_ATTN"),
            "PREPROCESSING_NUM_WORKERS": os.environ.get("PREPROCESSING_NUM_WORKERS"),
        },
        "commands": args.command,
        "notes": args.notes,
    }
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
