# Milestone 1 Task Knowledge

<!-- METADATA:SESSION=2 -->

## Knowledge Entries

1. Test gate fact: `M1-S22-PREFLIGHT-PARSER-GATE-TEST1` is a no-execution parser package gate. The current PR #45 gate status is `PASS_FOR_PM_RETRY` for latest head `01eebb7508768cd8b8ba3a1601e4a1f3774c27b4`.
2. Parser acceptance rule: the preflight parser must not classify its own generated command text, process output, copied historical evidence, or pattern-definition text as actionable current-node GPU health failures.
3. Parser safety rule: false-positive suppression must not remove detection for real current-node Xid, fatal/uncorrected ECC, NVLink link/fatal errors, CUDA/NCCL invalid peer memory, rank `SIGABRT`, or NCCL collective failure/nonzero exit.
4. Runtime gate rule: future SFT remains forbidden unless parser-fixed preflight emits a clear PASS with structured fields and `/home/xu.yang/coding_agent_playground/outputs` artifact preservation. Eval handoff remains blocked until checkpoint/model plus `trainer_state.json` and `all_results.json` or accepted replacements exist.
5. Superseded PR #45 review fact: earlier head `84959deac17560995a51a8f9a7be9093624cdf16` was blocked because test_1 required explicit structured fields or compatibility aliases for `different_node_gate`, `home_xu_yang_storage_status`, direct `sft_allowed`/`sft_skip_reason`, and preflight/capacity/topology/NVLink/NCCL status before `PASS_FOR_PM_RETRY`.
6. PR #45 latest-head fact: dev_4 added the required top-level compatibility fields and `home_xu_yang_storage_status`; `sft_allowed` remains false unless parser status is PASS, and eval handoff remains blocked until checkpoint/model plus `trainer_state.json` and `all_results.json` or accepted replacements exist.
