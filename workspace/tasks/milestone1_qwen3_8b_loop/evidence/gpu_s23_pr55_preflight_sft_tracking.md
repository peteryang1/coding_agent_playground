# dev_2 S23 PR55 GPU Runtime Tracking

Task ID: `M1-S23-PR55-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T14:52:40Z

Initial state: `LOCAL_PR55_BUNDLE_READY_PRE_SUBMIT`

```text
authorized allocation count: 1 fresh single-node 8 x H200
LTP frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
endpoint: pending
node: pending
forbidden nodes: lg-cmc-b7r202-q03u26-h200-000730, lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
source commit: 1f521b8db54a3e0d1b5c0057d3fafb4a5e20d703
source bundle sha256: db82b9162af2c37d670e568e16002cfc595e9090d578121545827622c3141df7
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
remote network rule: no remote git clone/fetch/GitHub/source/dependency download
preflight: pending
conditional SFT: pending only if PASS and sft_allowed=true
eval: not authorized
```

Stop/release required on forbidden-node assignment, source/data verification fail, storage/capacity fail, preflight fail, `sft_allowed=false`, SFT success/failure, node health issue, idle/no-progress limit, or PM/test stop instruction.

## Final Tracking Update

Final state: `STOPPED_AFTER_PR55_SFT_BLOCKER`

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr55-preflight-sft-20260521T145240Z
endpoint: ssh -p 15535 root@10.100.22.28
node: lg-cmc-b7r202-q05u06-h200-000722
node gate: PASS, non-forbidden
preflight: PASS
sft_allowed: true
SFT attempt: exactly one, started 2026-05-21T15:08:24Z
SFT exit_status: 1, ended 2026-05-21T15:08:25Z
blocker: environment: DEP_TARGET: unbound variable
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not authorized and not run
stop sent UTC: 2026-05-21T15:09:12Z
final LTP state: STOPPED (Completed), completed 2026-05-21 15:09:43
endpoint proof: ssh -p 15535 root@10.100.22.28 refused connection at 2026-05-21T15:10:02Z
active Milestone GPU held by dev_2: no
no-running-job proof command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
no-running-job proof output: No jobs found.
```

Preserved artifact roots:

```text
source/data staging: /home/xu.yang/coding_agent_playground/outputs/runs/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z/staging
preflight: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
SFT run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr55_sft_20260521T145240Z
capacity probe: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/milestone1_qwen3_8b_s23_pr55_preflight_sft_20260521T145240Z
```

Stop/release is complete. Any future LTP/GPU/preflight/SFT/eval work requires a fresh PM task and authorization.
