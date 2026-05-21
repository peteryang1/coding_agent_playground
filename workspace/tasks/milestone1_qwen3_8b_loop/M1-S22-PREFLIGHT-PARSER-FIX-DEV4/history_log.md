# M1-S22-PREFLIGHT-PARSER-FIX-DEV4 History

<!-- METADATA:SESSION=1 -->

## Session 1 - PR #45 Gate Fix - 2026-05-21

- Continued task `M1-S22-PREFLIGHT-PARSER-FIX-DEV4` after PM reported PR #45 NOT READY.
- Addressed dev_1 blocker `BLOCKER_ECC_FALSE_NEGATIVE_RISK_IN_PR45` by refining ECC parsing so fatal ECC always fails and nonzero uncorrected ECC counters are detected even when unrelated standalone zero tokens appear in the same line.
- Addressed test_1 blocker `BLOCKED_STRUCTURED_FIELDS_AND_STORAGE_STATUS` by adding stable top-level fields for preflight result, health result, non-actionable matches, NCCL all-reduce exit, capacity, different-node gate, `/home/xu.yang` storage status, topology, NVLink, direct `sft_allowed`, and `sft_skip_reason`.
- Preserved false-positive suppression for generated command/process/evidence/summary text and preserved real-fault detection for Xid/ECC/NVLink/NCCL invalid peer memory/SIGABRT/collective failures.
- Pushed PR #45 update; GitHub reports open, non-draft, `MERGEABLE` / `CLEAN`, with no required checks reported.
- No LTP/GPU/SFT/eval/dry-run/runtime command was run.
