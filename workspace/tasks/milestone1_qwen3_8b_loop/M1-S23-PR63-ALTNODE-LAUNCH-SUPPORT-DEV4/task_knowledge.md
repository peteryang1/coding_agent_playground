# Task Knowledge - M1-S23-PR63-ALTNODE-LAUNCH-SUPPORT-DEV4

1. PM authorized only dev_2 for one bounded alternate-node preflight plus conditional SFT runtime.
2. dev_4 is not authorized to run LTP/GPU/preflight/SFT/eval/remote commands for this task.
3. Current dev_2 altnode evidence is pre-submit/package-ready only and has no final checkpoint-or-blocker signature.
4. No dev_4 code/config/launcher action is justified until a final signature appears.
5. If a future final signature is hardware, node-health, or checkpoint-success, dev_4 should record no code action. If it is launcher/config/code, dev_4 should prepare a no-execution fix PR with this task id.
6. Final dev_2 altnode signature is forbidden placement on `lg-cmc-b7r202-k07u06-h200-000580`, stopped before transfer/preflight/SFT/eval with no checkpoint. Classification is `FINAL_PLACEMENT_BLOCKER_NO_LAUNCH_FIX_NEEDED`.
7. PR #65 merged at `2026-05-21T19:12:40Z` with merge commit `f71a8f591cdcf6064fdf466744a0e23aa88901f3`; task completion is complete/no-launch-fix-needed, with no runtime authorization.
