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
            "save_steps": 150,
            "save_total_limit": 4,
            "pin_best_before_resume": True,
            "final_model_symlink": "training_summary/model",
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
