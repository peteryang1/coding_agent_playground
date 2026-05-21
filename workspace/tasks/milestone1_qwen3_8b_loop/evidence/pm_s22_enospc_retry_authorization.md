# PM Session 22 ENOSPC-Fixed Retry Authorization

Task ID: `M1-S22-ENOSPC-RETRY-RUNTIME-DEV2`

Owner authorized to execute: `intern_code_dev_2`

PM role boundary:

```text
PM does not submit LTP.
PM does not run SFT, GPU commands, remote workspace code, or eval.
PM only gates evidence, assigns the owner, and records the decision.
```

## Gate Inputs

Accepted pre-run evidence:

- `evidence/dev_4_s21_enospc_config_fix.md`
- `evidence/dev_2_s21_enospc_resource_plan.md`
- `evidence/dev_3_s21_enospc_data_confirm.md`
- `evidence/dev_1_s21_enospc_review.md`
- `evidence/test_1_s21_enospc_retry_gate.md`
- `evidence/test_2_s21_eval_package.md`

Gate result:

```text
dev_1 review: PASS_FOR_PM_RETRY
test_1 pre-run gate: PASS_FOR_PM_RETRY
data contract: keep coding_agent_m1_sft_10_sharegpt
storage rule: future SFT/eval intermediates default to /home/xu.yang
```

## Authorized Scope

`intern_code_dev_2` is authorized to perform exactly one ENOSPC-fixed Session 22 SFT smoke attempt:

```text
dataset: coding_agent_m1_sft_10_sharegpt
source dataset artifact: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
base model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
output root: /home/xu.yang/coding_agent_playground/outputs
checkpoint root: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
run metadata/log root: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>
capacity probe root: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>
save strategy: save_steps=2, save_total_limit=1, max_steps=2
```

Before SFT launch, dev_2 must record fresh LTP node/job details and `/home/xu.yang` mount/path/write proof. The capacity probe must target `/home/xu.yang/coding_agent_playground/outputs`, not `/mnt/3fs`, unless PM records a new exception.

## Required Runtime Evidence

dev_2 must write:

- `evidence/dev_2_s22_enospc_retry_runtime.md`
- `evidence/gpu_s22_enospc_retry_tracking.md`
- `workspace/interns/intern_code_dev_2/status.md`

Required fields:

- LTP submit/status/ssh/stop commands
- frame/job id, node id, endpoint, start/end timestamps
- `/home/xu.yang` mount/path proof
- capacity probe command and result under `/home/xu.yang`
- exact SFT command and generated config path
- stdout/stderr log path
- exit status
- checkpoint/model path or exact runtime blocker
- `trainer_state.json` and `all_results.json` presence or absence
- absence/presence of old failure signatures
- stop proof and endpoint-after-stop proof

## Stop Conditions

dev_2 must stop/release the LTP node after any of these conditions:

- complete checkpoint/model is produced;
- SFT run fails and no PM-authorized retry remains;
- capacity probe fails;
- runtime health/idle limit triggers;
- PM/test gate orders stop.

mini-swe eval remains blocked until PM gates a complete checkpoint/model or served endpoint.
