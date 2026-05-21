from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import parse_s22_preflight_health as parser  # noqa: E402


def write_required_pass_artifacts(root: Path) -> None:
    (root / "capacity_probe.txt").write_text("capacity PASS_AND_CLEANED\n", encoding="utf-8")
    (root / "nvidia_smi_topo.txt").write_text("topology present\n", encoding="utf-8")
    (root / "nvidia_smi_nvlink.txt").write_text("NVLink status captured\n", encoding="utf-8")


def allow_tmp_output_root(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(parser, "EXPECTED_OUTPUT_ROOT", tmp_path)
    monkeypatch.setattr(parser, "ACCEPTED_RESOLVED_OUTPUT_ROOTS", (tmp_path.resolve(),))


def test_nccl_deprecation_warning_is_non_actionable_when_allreduce_passes(tmp_path: Path, monkeypatch) -> None:
    allow_tmp_output_root(monkeypatch, tmp_path)
    root = tmp_path / "milestone1_qwen3_8b_s23_hygiene_20260521T140000Z"
    root.mkdir()
    write_required_pass_artifacts(root)
    (root / "torch_nccl_allreduce.log").write_text(
        "\n".join(
            [
                "Warning: NCCL_ASYNC_ERROR_HANDLING is deprecated; use TORCH_NCCL_ASYNC_ERROR_HANDLING instead",
                "TORCHRUN_EXIT=0",
                "ALLREDUCE_OK world_size=8 value=36.0",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = parser.parse(root)

    assert result["status"] == "PASS"
    assert result["sft_allowed"] is True
    assert not [
        fault
        for fault in result["actionable_faults"]
        if "nccl_or_collective_failure" in fault.get("faults", [])
    ]
    assert any(
        match["reason"] == "benign_nccl_async_error_handling_deprecation_warning"
        for match in result["non_actionable_matches"]
    )


def test_nccl_deprecation_warning_is_non_actionable_when_status_is_split(tmp_path: Path, monkeypatch) -> None:
    allow_tmp_output_root(monkeypatch, tmp_path)
    root = tmp_path / "milestone1_qwen3_8b_s23_pr53_placementprobe_preflight_sft_20260521T142358Z"
    root.mkdir()
    write_required_pass_artifacts(root)
    (root / "torch_nccl_allreduce.log").write_text(
        "\n".join(
            [
                "Warning: Environment variable NCCL_ASYNC_ERROR_HANDLING is deprecated; use TORCH_NCCL_ASYNC_ERROR_HANDLING instead",
                "Warning: Environment variable NCCL_ASYNC_ERROR_HANDLING is deprecated; use TORCH_NCCL_ASYNC_ERROR_HANDLING instead",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "torch_nccl_allreduce_status.txt").write_text(
        "TORCHRUN_EXIT=0\nALLREDUCE_OK world_size=8 value=36.0\n",
        encoding="utf-8",
    )

    result = parser.parse(root)

    assert result["status"] == "PASS"
    assert result["sft_allowed"] is True
    assert not [
        fault
        for fault in result["actionable_faults"]
        if "nccl_or_collective_failure" in fault.get("faults", [])
    ]
    assert sum(
        match["reason"] == "benign_nccl_async_error_handling_deprecation_warning"
        for match in result["non_actionable_matches"]
    ) == 2


def test_sxid_20009_still_blocks(tmp_path: Path, monkeypatch) -> None:
    allow_tmp_output_root(monkeypatch, tmp_path)
    root = tmp_path / "milestone1_qwen3_8b_s23_hygiene_20260521T140000Z"
    root.mkdir()
    write_required_pass_artifacts(root)
    (root / "torch_nccl_allreduce.log").write_text("TORCHRUN_EXIT=0\nALLREDUCE_OK world_size=8 value=36.0\n")
    (root / "dmesg_gpu_fault_scan.txt").write_text(
        "kernel: NVRM: SXid 20009 Non-fatal, Link 57 RX Short Error Rate\n",
        encoding="utf-8",
    )

    result = parser.parse(root)

    assert result["status"] == "FAIL_HEALTH_SIGNATURE"
    assert result["sft_allowed"] is False
    assert any(
        fault.get("code") == 20009 and "sxid" in fault.get("faults", [])
        for fault in result["actionable_faults"]
    )


def test_real_nccl_failure_still_blocks(tmp_path: Path, monkeypatch) -> None:
    allow_tmp_output_root(monkeypatch, tmp_path)
    root = tmp_path / "milestone1_qwen3_8b_s23_hygiene_20260521T140000Z"
    root.mkdir()
    write_required_pass_artifacts(root)
    (root / "torch_nccl_allreduce.log").write_text(
        "NCCL unhandled system error during all_reduce\nTORCHRUN_EXIT=1\n",
        encoding="utf-8",
    )

    result = parser.parse(root)

    assert result["status"] == "FAIL_HEALTH_SIGNATURE"
    assert any(
        "nccl_or_collective_failure" in fault.get("faults", [])
        for fault in result["actionable_faults"]
    )
