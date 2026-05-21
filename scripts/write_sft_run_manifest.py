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
            "run_dir": str(Path(args.run_dir).resolve()),
            "output_dir": str(Path(args.output_dir).resolve()),
            "checkpoint_dir": str(Path(args.checkpoint_dir).resolve()),
            "manifest": str(out),
            "logs": str(Path(args.run_dir).resolve() / "logs"),
            "metrics": str(Path(args.run_dir).resolve() / "metrics.json"),
            "tensorboard": str(Path(args.output_dir).resolve() / "runs"),
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
            "output_root": os.environ.get("OUTPUT_ROOT"),
            "run_dir": str(Path(args.run_dir).resolve()),
            "checkpoint_dir": str(Path(args.checkpoint_dir).resolve()),
            "tmpdir": os.environ.get("TMPDIR"),
            "dataset_name": os.environ.get("DATASET_NAME"),
            "log_file": str(Path(args.run_dir).resolve() / "logs" / "train_stdout_stderr.log"),
            "xtrace_file": str(Path(args.run_dir).resolve() / "logs" / "train_xtrace.log"),
            "early_exit_diagnostics": str(Path(args.run_dir).resolve() / "early_exit_diagnostics.txt"),
        },
        "environment": {
            "USE_MCA": os.environ.get("USE_MCA"),
            "FORCE_TORCHRUN": os.environ.get("FORCE_TORCHRUN"),
            "PYTORCH_CUDA_ALLOC_CONF": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"),
            "NCCL_DEBUG": os.environ.get("NCCL_DEBUG"),
            "DISABLE_VERSION_CHECK": os.environ.get("DISABLE_VERSION_CHECK"),
            "NVTE_FLASH_ATTN": os.environ.get("NVTE_FLASH_ATTN"),
        },
        "commands": args.command,
        "notes": args.notes,
    }
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
