# M1-S23-PARSERFIXED-PARSER-PATCH-DEV4

<!-- METADATA:STATUS=Working,ASSIGNEE=intern_code_dev_4 -->

Owner: `intern_code_dev_4`

Evidence: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_parserfixed_parser_patch.md`

PR: #49 `https://github.com/peteryang1/coding_agent_playground/pull/49` (open, non-draft, `MERGEABLE` / `CLEAN`)

Acceptance:

- Classify Xid/SXid by freshness so stale historical audited records do not block current runs.
- Preserve fresh/current or timestamp-unknown actionable Xid/SXid/ECC/NVLink/NCCL failures.
- Normalize `/home/xu.yang/coding_agent_playground/outputs` and resolved `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs` as valid generated-artifact roots.
- Preserve structured fields.
- Include local/synthetic tests or explicit test attempts.
- Do not run LTP/GPU/preflight/SFT/eval/dry-run/runtime.

Completion marker: ready-for-review; future self-merge requires PM gate.
