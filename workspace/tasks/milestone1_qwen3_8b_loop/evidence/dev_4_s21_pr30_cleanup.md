# Dev 4 Session 21 PR 30 Cleanup Evidence

Task ID: `M1-S21-PR30-CLEANUP-DEV4`
Owner: `intern_code_dev_4`
Status: complete by superseding/closing archival PR #30
Evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s21_pr30_cleanup.md`

## Scope

PM Session 21 replacement task changed PR #30 from checkpoint-critical work to archival cleanup.

Allowed owner actions:

- refresh PR #30 against current main and make it mergeable for archival failed-retry evidence; or
- close/supersede PR #30 with durable status explaining that the Session 21 replacement path owns the next runtime.

Boundary:

- Do not run SFT.
- Do not use GPU.
- Do not self-merge PR #30 without a fresh PM gate.
- Do not peer-send PM routine status.

## Decision

Chosen action: close/supersede PR #30.

Reason:

- PR #30 repeatedly conflicted with PM coordination and stop-proof records on main.
- PM explicitly reclassified PR #30 as archival cleanup, not the checkpoint critical path.
- The failed-retry evidence is already durable in `evidence/dev_4_sft_retry_run.md`.
- Main contains dev_2 stop proof and later data-format unblock planning/artifact gates.
- Keeping PR #30 open as a merge target would not unblock the next runtime path and would keep consuming conflict-resolution cycles.

## PR 30 Closure

```text
PR: https://github.com/peteryang1/coding_agent_playground/pull/30
closedAt: 2026-05-21T07:23:06Z
mergedAt: null
final GitHub state after close: CLOSED, CONFLICTING / DIRTY
closure comment: https://github.com/peteryang1/coding_agent_playground/pull/30#issuecomment-4505715612
```

PR #30 was not merged.

## Preserved Retry Evidence

Retry evidence remains in:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_sft_retry_run.md
```

Key facts:

```text
task: M1-SFT-RETRY-RUN-DEV4
run id: milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z
endpoint used: ssh -p 23121 root@10.100.22.53
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
dataset: /root/workspace/cleaned_m1_sft_10/train.jsonl
dataset sha256: 5bbae5e25f121810c0b7c94738b6aa990f11b67d1f87f7d3b5071b98555a7054
config: configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml
exit status: 1
failure: KeyError: 'from' during LLamaFactory dataset conversion
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
extra retry: none
```

Durable run artifacts remain under:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_retry_tp8_maxsteps2_20260520T111830Z/
```

## Preserved Stop Proof

dev_2 stop proof is on main through the stop-proof path:

```text
frame: xu.yang~coding-agent-playground-m1-qwen3-8b-retry-20260520T110615Z
LTP final state: STOPPED (Completed)
completed: 2026-05-20 11:23:29
endpoint after stop: ssh -p 23121 root@10.100.22.53 refused connection
output preservation: /mnt/3fs artifacts preserved
dev_2 did not run SFT
```

## Replacement Runtime Path

PR #30 is superseded for runtime purposes.

Next runtime is owned by PM Session 21 replacement path and later explicit tasks, including data-format artifact/gate and launch-package work. A future SFT execution must be separately PM-gated and must address the observed LLamaFactory data-format mismatch:

```text
observed blocker: OpenAI-style role/content messages were registered with ShareGPT defaults expecting from/value
required future fix: exact dataset_info/config command wiring for a compatible artifact or PM-approved equivalent
current rule: no SFT/GPU retry is authorized by this cleanup task
```

## Completion Marker

`M1-S21-PR30-CLEANUP-DEV4` is complete:

- PR #30 is closed, not merged.
- Archival failed-retry evidence is identified and preserved.
- dev_2 stop proof from main is identified and preserved.
- Replacement path ownership is explicit.
- No SFT/GPU command was run for this cleanup.
