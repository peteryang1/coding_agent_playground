#!/usr/bin/env python3
"""Parse S22 GPU/NCCL preflight artifacts into structured health status.

This parser is artifact-aware: it scans hardware/runtime logs for actionable
GPU/NCCL faults while excluding generated command, process, evidence, and
summary text from actionable matching.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ACTIONABLE_NAME_PATTERNS = (
    "dmesg",
    "journal",
    "kernel",
    "nvrm",
    "nvidia_smi_q",
    "nvidia-smi-q",
    "nvidia_smi_nvlink",
    "nvidia-smi-nvlink",
    "nvidia_smi_topo",
    "nvidia-smi-topo",
    "torch_nccl",
    "allreduce",
    "nccl",
    "train_stdout_stderr",
    "train.log",
    "stderr",
    "stdout",
)

EXCLUDED_NAME_PATTERNS = (
    "command",
    "process",
    "evidence",
    "history",
    "task_knowledge",
    "summary",
    "readme",
    "preflight_result",
    "health_status",
    "parser",
    "manifest",
    "xtrace",
)

FAULT_TERMS = re.compile(
    r"Invalid access of peer GPU memory|hardware error|SIGABRT|Xid|"
    r"uncorrected.*[1-9]|fatal|NCCL.*(?:invalid|abort|fail|error|unhandled)|"
    r"(?:collective|all[_ -]?reduce).*(?:fail|error|exception)|"
    r"ChildFailedError",
    re.IGNORECASE,
)

XID_RE = re.compile(r"\bXid(?:\s+\([^)]+\))?:?\s*\d+\b", re.IGNORECASE)
PEER_MEMORY_RE = re.compile(r"Invalid access of peer GPU memory", re.IGNORECASE)
SIGABRT_RE = re.compile(r"\bSIGABRT\b|exitcode\s*[-=]\s*6|Signal\s+6", re.IGNORECASE)
CHILD_FAILED_RE = re.compile(r"ChildFailedError", re.IGNORECASE)
NCCL_FAILURE_RE = re.compile(
    r"NCCL.*(?:invalid|abort|fail|error|unhandled|system error)|"
    r"(?:collective|all[_ -]?reduce).*(?:fail|error|exception)",
    re.IGNORECASE,
)
ECC_RE = re.compile(
    r"(?:fatal\s+)?ECC|uncorrected|volatile.*uncorrect|aggregate.*uncorrect",
    re.IGNORECASE,
)
FATAL_ECC_RE = re.compile(r"fatal.*ECC|ECC.*fatal", re.IGNORECASE)
UNCORRECTED_ECC_RE = re.compile(r"uncorrect(?:ed|able)|volatile.*uncorrect|aggregate.*uncorrect", re.IGNORECASE)
ECC_COUNTER_RE = re.compile(
    r"(?:uncorrect(?:ed|able)|volatile.*uncorrect|aggregate.*uncorrect|ECC[^:\n]*error[^:\n]*)"
    r"[^0-9\n-]*(\d+)",
    re.IGNORECASE,
)
NONZERO_COUNTER_RE = re.compile(r"\b[1-9][0-9]*\b")
NVLINK_RE = re.compile(r"NVLink", re.IGNORECASE)
NVLINK_BAD_RE = re.compile(r"down|inactive|fail|fatal|crc|replay|error", re.IGNORECASE)
TORCHRUN_EXIT_RE = re.compile(r"\bTORCHRUN_EXIT\s*=\s*(\d+)\b")
PREFLIGHT_RESULT_RE = re.compile(r"\bPREFLIGHT_RESULT\s*=\s*([A-Z0-9_]+)\b")
DIFFERENT_NODE_RE = re.compile(r"PASS_DIFFERENT_PHYSICAL_NODE|different-node[^:\n]*:\s*PASS", re.IGNORECASE)

EXPECTED_OUTPUT_ROOT = Path("/home/xu.yang/coding_agent_playground/outputs")


@dataclass(frozen=True)
class SourceDecision:
    path: Path
    role: str
    reason: str


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def classify_source(path: Path) -> SourceDecision:
    name = path.name.lower()
    if any(pattern in name for pattern in EXCLUDED_NAME_PATTERNS):
        return SourceDecision(path, "excluded", "generated_command_process_evidence_or_summary_text")
    if any(pattern in name for pattern in ACTIONABLE_NAME_PATTERNS):
        return SourceDecision(path, "actionable", "hardware_or_runtime_log")
    if path.suffix.lower() in {".log", ".out", ".err"}:
        return SourceDecision(path, "actionable", "generic_log_extension")
    return SourceDecision(path, "excluded", "unrecognized_artifact_name")


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [f"<read_error:{exc}>"]


def has_ecc_fault(line: str) -> bool:
    if not ECC_RE.search(line):
        return False
    if FATAL_ECC_RE.search(line):
        return True

    match = UNCORRECTED_ECC_RE.search(line)
    if not match:
        return False

    # Only numbers tied to the ECC/uncorrected field are counters. This avoids
    # false negatives from unrelated zeros in prefixes such as GPU 0 or timestamps.
    suffix = line[match.start() :]
    counters = [int(value) for value in ECC_COUNTER_RE.findall(suffix)]
    if counters:
        return any(value > 0 for value in counters)

    return bool(NONZERO_COUNTER_RE.search(suffix))


def line_faults(line: str, source_name: str) -> list[str]:
    lowered = source_name.lower()
    faults: list[str] = []
    if XID_RE.search(line) and any(token in lowered for token in ("dmesg", "journal", "kernel", "nvrm")):
        faults.append("xid")
    if PEER_MEMORY_RE.search(line):
        faults.append("invalid_peer_gpu_memory")
    if SIGABRT_RE.search(line):
        faults.append("sigabrt")
    if CHILD_FAILED_RE.search(line):
        faults.append("torch_child_failed")
    if NCCL_FAILURE_RE.search(line) and "NCCL INFO" not in line:
        faults.append("nccl_or_collective_failure")
    if has_ecc_fault(line):
        faults.append("ecc_nonzero_or_fatal")
    if NVLINK_RE.search(line) and NVLINK_BAD_RE.search(line):
        if not re.search(r"(?:error|replay|crc)[^0-9]{0,24}0\b", line, re.IGNORECASE):
            faults.append("nvlink_link_or_counter_fault")
    return faults


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def infer_artifact_checks(root: Path, files: list[Path]) -> dict[str, dict[str, object]]:
    names = {rel(path, root): path for path in files}
    checks: dict[str, dict[str, object]] = {
        "capacity": {
            "status": "UNKNOWN",
            "evidence": [name for name in names if "capacity" in name.lower()],
        },
        "topology": {
            "status": "PRESENT" if any("topo" in name.lower() for name in names) else "MISSING",
            "evidence": [name for name in names if "topo" in name.lower()],
        },
        "nvlink": {
            "status": "PRESENT" if any("nvlink" in name.lower() for name in names) else "MISSING",
            "evidence": [name for name in names if "nvlink" in name.lower()],
        },
        "torch_nccl": {
            "status": "UNKNOWN",
            "evidence": [
                name
                for name in names
                if "torch" in name.lower() or "nccl" in name.lower() or "allreduce" in name.lower()
            ],
        },
        "process_scan": {
            "status": "INFO_ONLY",
            "evidence": [name for name in names if "process" in name.lower()],
        },
        "different_node_gate": {
            "status": "UNKNOWN",
            "evidence": [],
        },
        "home_xu_yang_storage": {
            "status": storage_status(root),
            "expected_root": str(EXPECTED_OUTPUT_ROOT),
            "preflight_dir": str(root),
        },
    }

    for path in files:
        text = "\n".join(read_lines(path))
        if re.search(r"capacity.*PASS|PASS_AND_CLEANED", text, re.IGNORECASE):
            checks["capacity"]["status"] = "PASS"
            checks["capacity"]["source"] = rel(path, root)
        if DIFFERENT_NODE_RE.search(text):
            checks["different_node_gate"]["status"] = "PASS"
            checks["different_node_gate"]["evidence"] = [*checks["different_node_gate"]["evidence"], rel(path, root)]
        match = TORCHRUN_EXIT_RE.search(text)
        if match:
            checks["torch_nccl"]["status"] = "PASS" if match.group(1) == "0" else "FAIL"
            checks["torch_nccl"]["exit_code"] = int(match.group(1))
            checks["torch_nccl"]["exit_source"] = rel(path, root)
        preflight_match = PREFLIGHT_RESULT_RE.search(text)
        if preflight_match:
            checks["legacy_marker"] = {
                "status": preflight_match.group(1),
                "source": rel(path, root),
                "note": "Recorded for audit only; parser status comes from allowlisted actionable sources.",
            }
    return checks


def storage_status(root: Path) -> str:
    try:
        root.relative_to(EXPECTED_OUTPUT_ROOT)
        return "PASS"
    except ValueError:
        return "FAIL_OUTSIDE_HOME_XU_YANG_OUTPUTS"


def top_level_compatibility_fields(
    *,
    status: str,
    checks: dict[str, dict[str, object]],
    ignored_matches: list[dict[str, object]],
) -> dict[str, object]:
    torch_exit = checks.get("torch_nccl", {}).get("exit_code")
    sft_allowed = status == "PASS"
    return {
        "preflight_result": status,
        "health_result": {
            "status": status,
            "actionable_fault": status == "FAIL_HEALTH_SIGNATURE",
        },
        "non_actionable_matches": ignored_matches,
        "torch_nccl_allreduce_exit": torch_exit,
        "capacity_probe_status": checks.get("capacity", {}).get("status", "UNKNOWN"),
        "different_node_gate": checks.get("different_node_gate", {}).get("status", "UNKNOWN"),
        "home_xu_yang_storage_status": checks.get("home_xu_yang_storage", {}).get("status", "UNKNOWN"),
        "topology_capture_status": checks.get("topology", {}).get("status", "UNKNOWN"),
        "nvlink_capture_status": checks.get("nvlink", {}).get("status", "UNKNOWN"),
        "sft_allowed": sft_allowed,
        "sft_skip_reason": "" if sft_allowed else status,
    }


def parse(root: Path) -> dict[str, object]:
    files = list(iter_files(root))
    actionable_faults: list[dict[str, object]] = []
    ignored_matches: list[dict[str, object]] = []
    sources_scanned: list[dict[str, str]] = []
    sources_excluded: list[dict[str, str]] = []

    for path in files:
        decision = classify_source(path)
        source = rel(path, root)
        lines = read_lines(path)
        if decision.role == "actionable":
            sources_scanned.append({"path": source, "reason": decision.reason})
            for line_no, line in enumerate(lines, start=1):
                faults = line_faults(line, path.name)
                if faults:
                    actionable_faults.append(
                        {"path": source, "line": line_no, "faults": sorted(set(faults)), "text": line[:500]}
                    )
        else:
            sources_excluded.append({"path": source, "reason": decision.reason})
            for line_no, line in enumerate(lines, start=1):
                if FAULT_TERMS.search(line):
                    ignored_matches.append(
                        {"path": source, "line": line_no, "reason": decision.reason, "text": line[:500]}
                    )

    checks = infer_artifact_checks(root, files)
    missing_required = [
        key
        for key in ("topology", "nvlink", "torch_nccl")
        if checks.get(key, {}).get("status") in {"MISSING", "UNKNOWN"}
    ]
    if checks.get("home_xu_yang_storage", {}).get("status") != "PASS":
        missing_required.append("home_xu_yang_storage")

    if actionable_faults or checks.get("torch_nccl", {}).get("status") == "FAIL":
        status = "FAIL_HEALTH_SIGNATURE"
    elif missing_required:
        status = "WARN_INCOMPLETE"
    else:
        status = "PASS"

    result = {
        "schema_version": "s22_preflight_health_v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "preflight_dir": str(root),
        "status": status,
        "actionable_fault": bool(actionable_faults),
        "actionable_faults": actionable_faults,
        "ignored_non_actionable_matches": ignored_matches,
        "sources_scanned": sources_scanned,
        "sources_excluded": sources_excluded,
        "checks": checks,
        "decision": {
            "sft_allowed_if_pm_authorized": status == "PASS",
            "reason": (
                ["actionable GPU/NCCL health signature found"]
                if actionable_faults
                else [f"missing_or_unknown_required_artifacts: {','.join(missing_required)}"]
                if missing_required
                else ["allowlisted preflight artifacts passed without actionable health signatures"]
            ),
        },
        "policy": {
            "excluded_from_actionable_scan": [
                "generated command text",
                "process listings",
                "durable evidence/history/task notes",
                "summary/result files that can copy searched terms",
            ],
            "preserved_actionable_detection": [
                "Xid in kernel/dmesg/NVRM logs",
                "fatal or nonzero uncorrected ECC",
                "NVLink link/down/error/replay/CRC faults",
                "NCCL/CUDA invalid peer GPU memory",
                "rank SIGABRT or torch elastic ChildFailedError",
                "NCCL collective/all_reduce failures",
            ],
        },
    }
    result.update(top_level_compatibility_fields(status=status, checks=checks, ignored_matches=ignored_matches))
    if status != "PASS" and not result["sft_skip_reason"]:
        result["sft_skip_reason"] = "preflight_not_passed"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-dir", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-text")
    args = parser.parse_args()

    root = Path(args.preflight_dir).resolve()
    if not root.is_dir():
        raise SystemExit(f"missing preflight dir: {root}")
    result = parse(root)

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.out_text:
        reasons = "; ".join(str(item) for item in result["decision"]["reason"])
        Path(args.out_text).write_text(
            f"PREFLIGHT_RESULT={result['preflight_result']}\n"
            f"PREFLIGHT_STRUCTURED_STATUS={result['status']}\n"
            f"ACTIONABLE_FAULT={str(result['actionable_fault']).lower()}\n"
            f"SFT_ALLOWED={str(result['sft_allowed']).lower()}\n"
            f"SFT_ALLOWED_IF_PM_AUTHORIZED={str(result['decision']['sft_allowed_if_pm_authorized']).lower()}\n"
            f"SFT_SKIP_REASON={result['sft_skip_reason']}\n"
            f"TORCH_NCCL_ALLREDUCE_EXIT={result['torch_nccl_allreduce_exit']}\n"
            f"CAPACITY_PROBE_STATUS={result['capacity_probe_status']}\n"
            f"DIFFERENT_NODE_GATE={result['different_node_gate']}\n"
            f"HOME_XU_YANG_STORAGE_STATUS={result['home_xu_yang_storage_status']}\n"
            f"TOPOLOGY_CAPTURE_STATUS={result['topology_capture_status']}\n"
            f"NVLINK_CAPTURE_STATUS={result['nvlink_capture_status']}\n"
            f"REASON={reasons}\n",
            encoding="utf-8",
        )

    if result["status"] == "PASS":
        return 0
    if result["status"] == "WARN_INCOMPLETE":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
