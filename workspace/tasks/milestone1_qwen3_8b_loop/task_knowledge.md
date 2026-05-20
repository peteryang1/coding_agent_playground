# Milestone 1 Task Knowledge

<!-- METADATA:SESSION=11 -->

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
39. PR audit fact: PR #1 is open, non-draft, mergeable, scoped to Qwen3-8B SFT pipeline artifacts, and passes PM gate for self-merge by dev_4; PR #2 mergeability later resolved to `MERGEABLE`, so PM gate passes for owner self-merge of the coordination/evidence PR without waiting for whole-milestone completion.
40. PR fact: PR #2 merged at `2026-05-20T07:51:54Z` with merge commit `07b0dd167b9004af1c6994652966b7e1de5f2084`; further PM updates need a continuation branch/PR.
41. PR fact: PR #3 was opened for continuation PM durable coordination, is mergeable, and passes PM gate for owner self-merge because it does not claim milestone completion.
42. Gate fact: after PR #3 merge, PR #1 is still open/mergeable and the SFT/eval support evidence files remain missing, so SFT/eval smoke is still unproven.
43. PR fact: PR #4 merged at `2026-05-20T08:01:24Z` with merge commit `002155e6295461871544cfc267863facc5570dd5`.
44. PR gate fact: latest audit still shows PR #1 `OPEN`, non-draft, mergeable `MERGEABLE`, `mergedAt=null`; PM gate passes for dev_4 owner self-merge of scoped Qwen3-8B SFT pipeline artifacts, but PM must not merge it for dev_4.
45. Coordination fact: PM used non-interrupt tmux inject plus capture-pane verification to notify dev_4 again that PR #1 should be self-merged by the owner and recorded in durable evidence/status.
46. Gate fact: latest evidence check still lacks `dev_1_sft_base_path_support.md`, `dev_2_gpu_nodes_support.md`, and `test_1_sft_eval_completion_gate.md`; without these or dev_4/test_2 decision packages, PM cannot close the SFT/eval smoke gate.
47. PR fact: PR #5 merged at `2026-05-20T08:07:31Z` with merge commit `8f5b7736939453c15ffb802c42a0ee9c875b531d`.
48. PR gate fact: after PR #5, PR #1 is still `OPEN` and `MERGEABLE` with no merge commit; dev_4 remains the owner who must self-merge or write a concrete blocker.
49. Coordination fact: PM resent non-interrupt active-gate follow-ups by tmux to dev_4/dev_1/dev_2/test_1 and verified them with `capture-pane`; no peer_send or secretary report was used.
50. Gate fact: PM should not mark the active goal complete until owner evidence proves SFT smoke output plus mini-swe eval smoke output/metrics, or an explicit accepted fallback path plus eval output is documented.
51. PR fact: PR #6 merged at `2026-05-20T08:14:18Z` with merge commit `9f43d16932098010b12a138d661f90a383ff2d0a`.
52. Coordination fact: PM expanded active non-interrupt tmux follow-up to all six dev/test owners so no intern is idle: dev_4 PR/SFT blocker, dev_1 base path, dev_2 GPU/nodes, dev_3 SFT input handoff, test_1 completion gate, and test_2 eval acceptance gate.
53. Gate fact: current completion remains unproven because PR #1 is still open and evidence for SFT unblock, GPU route, SFT completion gate, and mini-swe acceptance gate is missing or stale.
54. PM boundary fact: even when support evidence is missing repeatedly, PM must not fill it by running remote probes or experiments directly; PM should assign, gate, collect durable files, and decide from owner evidence.
55. PR fact: PR #1 was self-merged by dev_4 at `2026-05-20T08:23:54Z` with merge commit `882d1642884e82d1a40674266f244a52cf69defc`.
56. PM decision: for the next Qwen3-8B SFT smoke, use clean-base candidate `BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`; do not use the broken alias `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B`.
57. Technical fact: dev_4 verified the clean-base candidate has `config.json`, tokenizer files, `generation_config.json`, `model.safetensors.index.json`, 5 safetensors shards, and no missing index shards.
58. Technical fact: current SFT input for dev_4 is `/root/workspace/cleaned_m1_sft_10/train.jsonl` with SHA-256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`.
59. Current blocker: real SFT smoke launch remains blocked on GPU endpoint or current Milestone 1 `nodes.json`; the corrected final workspace entry host has no `nvidia-smi`.
60. PR conflict fact: PR #11 conflicted with current `origin/main`; dev_4 resolved the only conflict in `workspace/tasks/milestone1_qwen3_8b_loop/history_log.md` by preserving both dev_4 Session 9 records and PM/test_1/test_2 post-PR10 gate records.
55. PR fact: PR #7 merged at `2026-05-20T08:20:50Z` with merge commit `98eb9d3573e24a732a7de354e8ecbf1c0173c2c3`.
56. PR fact: dev_4 self-merged PR #1 at `2026-05-20T08:23:54Z` with merge commit `882d1642884e82d1a40674266f244a52cf69defc`.
57. Gate fact: dev_3 SFT input handoff is sufficient for data-side SFT readiness: `/root/workspace/cleaned_m1_sft_10/train.jsonl`, format `coding_agent_playground_sft_v1`, 10 examples, SHA-256 `5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054`.
58. Gate fact: dev_2 GPU/nodes evidence is sufficient to prove the corrected entry host has no visible GPU and no current Milestone 1 `nodes.json`; SFT launch still requires a new GPU allocation or explicit reuse approval for historical allocation.
59. SFT decision fact: dev_4 recommends warm-start fallback `/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-final` only if PM/supervisor explicitly accepts warm-start smoke instead of clean-base smoke.
60. Base-model gate fact: dev_1 found a usable local clean-base candidate `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`; PM decision is to prefer this clean-base candidate over warm-start fallback for the next SFT smoke once GPU/current `nodes.json` exists.
61. Remaining blocker fact: no current GPU endpoint or Milestone 1 `nodes.json`, no real SFT smoke checkpoint/output, and no mini-swe eval smoke metrics exist yet; test_1 completion gate and test_2 eval acceptance package remain missing.
62. PR fact: PR #8 merged at `2026-05-20T08:33:38Z` with merge commit `97cff0dddfb460585b62193b4f567470b047ffd5`.
63. Coordination fact: PM sent non-interrupt required-now tmux follow-ups to test_1/test_2 for missing completion/eval gates and to dev_4 for a no-launch clean-base SFT smoke launch package; capture-pane verified the messages were submitted.
64. Gate fact: next SFT execution is not authorized yet because the GPU/current `nodes.json` requirement remains unsatisfied even though the clean-base candidate and SFT input are ready enough.
65. PR fact: PR #9 merged at `2026-05-20T08:39:36Z` with merge commit `e876c755d92f8c39fc862daaec8ac7968dfac845`.
66. Gate fact: after waiting and rechecking, test_1 completion gate, test_2 eval acceptance/provenance package, and dev_4 clean-base no-launch launch package remain missing or stale.
67. Coordination fact: PM must keep using durable owner evidence for these remaining gates; do not fill missing test/dev artifacts by writing them as PM or by running SFT/eval directly.
68. PR fact: PR #10 merged at `2026-05-20T08:45:07Z` with merge commit `ce59c983372ac12dc3433091278efb6eec1876eb`.
69. Gate fact: test_1 completion audit gate is now present and passes PM gate for criteria definition, but it explicitly proves the milestone is still incomplete until real SFT and mini-swe smoke artifacts exist.
70. Gate fact: test_2 mini-swe acceptance/provenance package is now present and passes PM gate; mini-swe should use a served OpenAI-compatible endpoint/model string, not a raw checkpoint path alone.
71. Gate fact: dirty mini-swe checkout state (`M src/minisweagent/environments/apptainer.py`, `?? uv.lock`) is acceptable only for Milestone 1 smoke when recorded in provenance; it must not be silent state in final eval evidence.
72. Blocker fact: dev_4's no-launch SFT smoke package using clean-base candidate `/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6` is still not landed in PM worktree; dev_4 is owner and was observed working through a local status.md conflict.
73. PR fact: PR #12 merged at `2026-05-20T08:56:29Z` with merge commit `1e32de047754e376f107b727ddf7349417696db9`.
74. PR gate fact: dev_4 PR #11 is open/non-draft but `CONFLICTING`, so it is not ready for owner self-merge; dev_4 must rebase/resolve against current `origin/main` and preserve PM/test_1/test_2 gate records.
75. PR fact: PR #13 merged at `2026-05-20T09:00:25Z` with merge commit `9a6de432919102c17fdd839e5544d46c98a8f1f7`.
76. PR fact: dev_4 self-merged PR #11 at `2026-05-20T09:10:26Z` with merge commit `93c4efaaff3e50220f7bb8583070321e65289efa`; no-launch clean-base SFT package is now on main.
77. GPU route fact: dev_2 route acquisition evidence found two live H200 candidate endpoints, `ssh -p 27094 root@10.100.10.20` and `ssh -p 31403 root@10.100.8.24`, but neither is approved Milestone 1 allocation; both show high memory use and lack local SFT paths.
78. PM decision before GPU approval: do not authorize SFT launch until compute/PM approves a discovered endpoint or provides fresh GPU endpoint/current `nodes.json`; dev_4 owns execution only after that route is approved.
79. PR fact: PR #15 merged at `2026-05-20T09:19:31Z` with merge commit `21c59cd013e6d8c1a736483cc91864b11325f417`.
80. GPU route fact: compute manager approved fresh single-node H200 route `ssh -p 39314 root@10.100.20.37`, LTP frame `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130`, with one-node `compute_gpu_route_nodes.json`.
81. PM decision update: use the approved current GPU route `ssh -p 39314 root@10.100.20.37` with `nodes.json` at `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/compute_gpu_route_nodes.json`, staged remotely at `/root/workspace/coding_agent_playground/nodes.json` and `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_nodes.json`.
82. PM decision: dev_4 is authorized to run only the short Qwen3-8B SFT smoke on the approved route after resolving PR #14 conflict; test_2 owns mini-swe after SFT model/checkpoint exists.
83. PR conflict fact: PR #14 conflicted after PR #15 merged and again after GPU-route authorization records landed; dev_4 must merge current `origin/main`, preserve PR #15 GPU route evidence and PM records, push PR #14, and self-merge only after PR #14 is mergeable.
84. Resource rule: coding_agent_playground interns must use LTP directly for GPU resources instead of routing routine requests through axrd interns. PM only gates/tracks; dev/test owners submit/status/ssh/stop and write durable evidence.
85. GPU lifecycle fact: active H200 job `xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130` at `ssh -p 39314 root@10.100.20.37` is tracked in `evidence/gpu_resource_tracking.md`; dev_2 owns lifecycle/stop proof and dev_4 owns SFT workload.
86. Stop condition: the active H200 node must be stopped after SFT smoke completion/failure, if idle for 15 minutes without owner progress, or by 2026-05-20T10:30:00Z unless dev_2 writes a durable extension reason.
