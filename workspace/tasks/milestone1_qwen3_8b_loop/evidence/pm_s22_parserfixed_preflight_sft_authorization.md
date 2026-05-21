# PM Authorization - M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2

Owner: `intern_code_dev_2`
Task: `M1-S22-PARSERFIXED-PREFLIGHT-SFT-RUNTIME-DEV2`
Timestamp: 2026-05-21T11:42:20Z basis

## Authorization

PM authorizes exactly one owner-executed runtime attempt after PR #45 merge:

- Submit one fresh 8 x H200 LTP allocation, preferably on a different node from the failed preflight node `lg-cmc-b7r401-a04u26-h200-000769`.
- Run the parser-fixed NCCL/NVLink/capacity health preflight.
- Run one Qwen3-8B ShareGPT SFT smoke only if the parser-fixed preflight emits structured PASS and `sft_allowed=true`.
- Do not run eval.

## Gate Basis

- PR #45 `M1-S22-PREFLIGHT-PARSER-FIX-DEV4` merged at `2026-05-21T11:42:20Z`.
- PR #45 merge commit: `6f61489e85fcf7e129699061c9ddcb6e8db80926`.
- dev_1 gate: `PASS_FOR_PM_RETRY` against head `01eebb7508768cd8b8ba3a1601e4a1f3774c27b4`.
- test_1 gate: `PASS_FOR_PM_RETRY` against head `01eebb7508768cd8b8ba3a1601e4a1f3774c27b4`.
- dev_2 no-submit resource readiness is present in `evidence/dev_2_s22_preflight_resource_ready.md`.

## Required Storage

All generated artifacts must be under:

`/home/xu.yang/coding_agent_playground/outputs`

This includes preflight outputs, parser `health_status.json` and `health_status.txt`, temporary converted datasets, logs, checkpoints, run metadata, trainer output, and any intermediate files. Existing required inputs may remain outside `/home/xu.yang` only when explicitly justified in owner evidence.

## Required Evidence

dev_2 must write:

- `evidence/dev_2_s22_parserfixed_preflight_sft_runtime.md`
- `evidence/gpu_s22_parserfixed_preflight_sft_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`

Evidence must include LTP frame/job id, node id, endpoint, nodes.json, exact submit/status/stop commands, different-node check, `/home/xu.yang` paths, capacity probe, topology/NVLink capture, torch NCCL all-reduce status, parser-fixed health JSON/text, exact SFT command/env/config if run, checkpoint/model or exact blocker, `trainer_state.json` and `all_results.json` presence/absence, and stop proof.

## Stop Conditions

dev_2 must stop/release the allocation after the preflight/SFT attempt completes, if preflight fails and SFT is skipped, if a runtime blocker is reached, if idle without progress, or if PM later revokes authorization.

PM did not submit LTP, use GPU, run preflight, run SFT, run eval, or execute remote runtime commands.
