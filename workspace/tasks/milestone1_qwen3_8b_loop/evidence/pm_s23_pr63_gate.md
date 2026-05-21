# PM Session 23 PR63 Gate

Task: `M1-S23-PR61-MCA-MODEL-PATH-FIX-DEV4`
Owner: `intern_code_dev_4`
PR: https://github.com/peteryang1/coding_agent_playground/pull/63

## Decision

`PASS_OWNER_SELF_MERGE_ONLY`

PM authorizes only `intern_code_dev_4` owner self-merge for PR #63 and task completion marking. This gate does not authorize LTP, GPU allocation, transfer, preflight, SFT, eval, dry-run, or remote execution.

## Gate Inputs

- GitHub state: PR #63 is open, non-draft, `MERGEABLE` / `CLEAN`.
- Latest PR #63 head: `a0ab039278198a6c1b0cd40009038d89cd602922`.
- Functional patch commit: `a035692dc72b40434240d0308c36f4d071644849`.
- Dev review: `evidence/dev_1_s23_pr61_mca_model_path_review.md` records `PASS_FOR_PM_RETRY` against latest head.
- Test gate: `evidence/test_1_s23_pr61_mca_model_path_gate.md` records `PASS_FOR_PM_RETRY` against latest head.
- Dev_4 evidence: `evidence/dev_4_s23_pr61_mca_model_path_fix.md` records the launcher normalization fix, local static checks, and no LTP/GPU/preflight/SFT/eval execution.

## Acceptance Notes

The PR63 fix addresses the PR61 runtime blocker where direct `python3 .../llamafactory/launcher.py train <config>` invocation caused LLamaFactory/MCA parsing to miss `model_name_or_path` even though the generated runtime YAML contained it. The patch normalizes a direct `*/llamafactory/launcher.py` command to `python3 -m llamafactory.cli` while preserving PR61 command-array parsing and prior no-remote-network plus `/home/xu.yang` rules.

## Next Gate

After dev_4 self-merges PR #63 and records task completion, PM may consider a separate dev_2 runtime authorization. Any fresh runtime must still require local/provided workspace preparation, no remote source/dependency downloads, exact transfer command/checksum/file-list evidence, `/home/xu.yang/coding_agent_playground/outputs` intermediates, structured preflight PASS, `SFT_ALLOWED=true`, checkpoint/model or exact runtime blocker, and stop/no-running-job proof.
