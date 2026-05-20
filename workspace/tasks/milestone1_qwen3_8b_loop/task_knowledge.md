# Milestone 1 Task Knowledge

<!-- METADATA:SESSION=8 -->

## Knowledge Entries

1. Supervisor requirement: Milestone 1 must run an end-to-end smoke loop across three high-star repo types with 10 total Codex trajectories, cleaning to `coding_agent_playground` format, Qwen3-8B SFT smoke/path, mini-swe-agent eval smoke/report, and final report.
2. Technical fact: final large-scale workspace machine is `ssh -p 31787 root@10.100.194.40`, with repo clones under `/root/workspace/{repo}`.
3. Technical fact: selected repositories are `fastapi/fastapi` at `f4cafbc`, `scikit-learn/scikit-learn` at `ffc6cdc`, and `Textualize/rich` at `46cebbb`.
4. Technical fact: corrected final workspace has `/usr/local/bin/codex`, `codex-cli 0.130.0`, and `~/.codex/auth.json`; rollout harness preflight passes with this default.
5. Communication rule: dev/test routine status, blockers, reports, and test results must be written to durable evidence paths, not peer-sent to PM.
6. Communication rule: PM routine milestone reports, status, blockers, summaries, and completion notes for secretary/supervisor must be written to durable task files, not peer-sent to secretary.
7. Technical fact: mini-swe-agent source checkout, SWE-bench source, `uv`, and Singularity are present on the corrected final workspace; global `mini-extra` is absent, so smoke eval should run from `/root/workspace/swe-bench-related/mini-swe-agent` with `uv run --with datasets`.
8. Blocker: Qwen3-8B SFT real launch still needs a valid clean base/checkpoint path plus GPU allocation/current milestone `nodes.json`; corrected entry host has no `nvidia-smi`.
9. Test finding: rollout harness dry-run basics pass, and corrected final-workspace smoke under `/root/workspace/rollouts_smoke_v3` includes the dev_3-required artifact set.
10. Technical fact: PM tiny non-dry rollout on corrected final workspace passed for `fastapi/fastapi` under `/root/workspace/rollouts_nondry_new_machine_tiny`, closing the non-dry harness/auth gate.
11. Technical fact: dev_2 harness v2 outputs include execution artifacts, `raw_trajectory.json`, stable `trajectory_id`, full repo IDs, and a manifest-reconciled `summary.json`.
12. PM priority: every dev/test intern must keep non-waiting durable work in their evidence path; upstream gaps should produce assumptions, sample data, validators, launch commands, smoke plans, or blocker evidence rather than idle time.
13. Technical fact: Session 4 superseded the old 300/100-per-repo rollout. Old roots `/root/workspace/rollouts_m1_300`, `/root/workspace/rollouts_m1_300_scikit_learn`, and `/root/workspace/rollouts_m1_300_rich` are scratch-only.
14. Technical fact: old 300 rollout parent PIDs `1208139`, `1270557`, `1270562` and observed codex child PIDs are dead; scratch markers are written under `/root/workspace/rollout_harness/`.
15. Technical fact: active rollout input is `/root/workspace/rollout_harness/tasks_m1_10.jsonl` with exactly 10 total prompts: `fastapi=4`, `scikit-learn=3`, `rich=3`.
16. Quality rule: a final accepted trajectory must include requirements understanding, repo/file localization, code inspection, actual code edit/patch attempt, test/check attempt, observed result/error, and final changed-files/tests/blockers.
17. Technical fact: Session 5 final 10-total rollout finished at `/root/workspace/rollouts_m1_10` with 10 manifest entries.
18. Technical fact: `validate_complete_coding_trajectories.py` is the Session 4 quality gate for complete coding-process trajectory acceptance.
19. Technical fact: final 10-rollout validation has 10 checked, 10 valid, and 0 invalid complete-process trajectories.
20. Technical fact: `/root/workspace/cleaned_m1_sft_10/train.jsonl` contains 10 `coding_agent_playground_sft_v1` examples with 0 rejects and 0 conversion errors; split is `fastapi/fastapi=4`, `scikit-learn/scikit-learn=3`, `Textualize/rich=3`.
21. Technical fact: Dev_4 validated an SFT dry-run command using `/root/workspace/cleaned_m1_sft_10/train.jsonl`; manifest path is `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/run_manifest.json`.
22. Technical fact: Test_2 prepared mini-swe-agent smoke commands using Singularity backend; execution is blocked until an SFT smoke model/checkpoint or endpoint exists.
23. Coordination fact: PM used exact `/esc` interrupt for all six dev/test interns; durable `assignments.md` remains source of truth when follow-up delivery was busy/unconfirmed.
24. Technical fact: eval readiness metrics are written at `/root/workspace/swe-bench-related/output/qwen3_8b_sft_smoke/metrics_readiness.json` with status `blocked` and the prepared mini-swe-agent command.
25. Reporting fact: `final_report.md` now reflects current evidence instead of pending placeholders; it is not a completion report because SFT real smoke and mini-swe-agent execution remain blocked on model/GPU path.
26. Technical fact: corrected final workspace still has no `nvidia-smi`, no current Milestone 1 `nodes.json`, and `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is still a broken symlink.
27. Technical fact: historical Qwen3-8B checkpoints with valid `config.json` exist under `/mnt/3fs/data/ai4ai/models/ws_202604...`, but using them would be a warm-start decision and not a clean-base SFT smoke.
28. PM operating rule: PM must only assign tasks, set gates, collect durable evidence, and make decisions; PM must not directly modify code or execute code/experiments, including on the supervisor final workspace.
29. Delegation rule: any further final-workspace execution, code changes, SFT/GPU/model probing, or mini-swe-agent eval smoke must be owned and executed by the assigned dev/test intern and recorded in the named durable evidence file.
30. Coordination fact: for Session 6, peer assignment delivery succeeded for dev_3/test_1; dev_1/dev_2/dev_4/test_2 required `/esc` plus tmux direct assignment because normal peer messages remained unconfirmed or busy.
31. Communication rule: PM -> dev/test task and correction messages should now default to direct tmux injection into the target intern pane with Enter; `peer_send` is not the primary notification channel.
32. Communication rule: PM should avoid interrupts by default; use `C-c`, `/esc`, or equivalent only when the supervisor explicitly requires urgent interruption or when the target's current behavior would keep wasting resources or continue an incorrect execution.
33. Communication rule: after tmux injection, PM must run `tmux capture-pane` to verify the message was submitted and is not just sitting in the target input line.
34. Gate decision: Milestone 1 is not complete until there is durable evidence of real SFT smoke output or an explicit accepted fallback plus mini-swe-agent smoke output/metrics; current dry-run manifest and readiness metrics alone are insufficient.
35. PM decision: do not silently treat historical Qwen3-8B checkpoints as clean base; dev_4 must document whether clean base can be repaired/located or recommend a warm-start fallback for explicit PM/supervisor acceptance.
36. Coordination fact: while waiting for dev_4/test_2 primary decision packages, PM assigned dev_1/dev_2/test_1 parallel support evidence for clean-base candidates, GPU/current `nodes.json`, and SFT+mini-swe completion gates by non-interrupt tmux injection.
37. Gate fact: absence of the new support evidence files means PM cannot yet decide clean-base vs warm-start or GPU routing; keep the goal active and continue collecting durable evidence.
38. PR gate rule: ready and mergeable PRs that pass PM gate should be merged by their owner without waiting for the whole milestone to complete; PM gates readiness and uses tmux inject to notify the owner to self-merge.
39. PR audit fact: PR #1 is open, non-draft, mergeable, scoped to Qwen3-8B SFT pipeline artifacts, and passes PM gate for self-merge by dev_4; PR #2 was mergeability `UNKNOWN` with local PM durable changes pending at the initial Session 8 audit.
