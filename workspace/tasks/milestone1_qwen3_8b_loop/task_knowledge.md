# Milestone 1 Task Knowledge

<!-- METADATA:SESSION=1 -->

## Knowledge Entries

1. Test gate fact: `M1-S22-PREFLIGHT-PARSER-GATE-TEST1` is a no-execution parser package gate. The current PR #45 gate status is `BLOCKED_STRUCTURED_FIELDS_AND_STORAGE_STATUS`.
2. Parser acceptance rule: the preflight parser must not classify its own generated command text, process output, copied historical evidence, or pattern-definition text as actionable current-node GPU health failures.
3. Parser safety rule: false-positive suppression must not remove detection for real current-node Xid, fatal/uncorrected ECC, NVLink link/fatal errors, CUDA/NCCL invalid peer memory, rank `SIGABRT`, or NCCL collective failure/nonzero exit.
4. Runtime gate rule: future SFT remains forbidden unless parser-fixed preflight emits a clear PASS with structured fields and `/home/xu.yang/coding_agent_playground/outputs` artifact preservation. Eval handoff remains blocked until checkpoint/model plus `trainer_state.json` and `all_results.json` or accepted replacements exist.
5. PR #45 review fact: dev_4's parser package direction passes false-positive suppression and real-fault source review, but test_1 requires explicit structured fields or compatibility aliases for `different_node_gate`, `home_xu_yang_storage_status`, direct `sft_allowed`/`sft_skip_reason`, and preflight/capacity/topology/NVLink/NCCL status before `PASS_FOR_PM_RETRY`.
