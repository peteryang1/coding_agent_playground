# Test 2 Session 22 Mini-SWE Eval Blocker

Timestamp: 2026-05-21T08:36:13Z

## Task Attachment

Task id: `M1-S22-EVAL-BLOCKED-TEST2`

Owner: `intern_code_test_2`

Scope: refresh mini-swe blocked evidence after Session 22 early-exit SFT failure. This is evidence/status-only test work. No eval run is authorized.

Durable evidence path: `workspace/tasks/milestone1_qwen3_8b_loop/evidence/test_2_s22_eval_blocked.md`

Status path: `workspace/interns/intern_code_test_2/status.md`

Registry acceptance: cite Session 22 runtime facts, keep future eval outputs/intermediates under `/home/xu.yang`, and state no eval can run without a complete checkpoint/model or served endpoint.

Completion marker: `BLOCKED_FINAL_EVAL_EVIDENCE`.

## Runtime Evidence Read

Source runtime evidence:

```text
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_2_s22_enospc_retry_runtime.md
```

Relevant runtime task:

```text
M1-S22-ENOSPC-RETRY-RUNTIME-DEV2
```

S22 runtime summary from dev_2 evidence:

- PM-authorized SFT attempt count: 1.
- Attempts started: 1.
- Attempts completed: 1.
- Additional retries run: 0.
- Eval run by runtime owner: false.
- Run id: `milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z`.
- Runtime status: `EXIT_STATUS=1`.
- Final result: failed before training produced manifest/config/checkpoint artifacts.
- Log path: `/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/logs/train_stdout_stderr.log`.
- Exit status path: `/home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z/exit_status.txt`.
- CephFS preserved files are visible after node stop via `/mnt/cephfs/home/xu.yang/...`.

Artifact presence from dev_2 evidence:

```text
run_manifest.json: absent
generated runtime config under run dir: absent
checkpoint files: absent
trainer_state.json: absent
all_results.json: absent
complete checkpoint/model: absent
```

Endpoint/worker status from dev_2 evidence:

```text
frame: xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
post-stop state: STOPPED (Completed)
endpoint: ssh -p 31346 root@10.100.16.69
endpoint result after STOPPED: connection refused
```

Old signature observations from dev_2 evidence:

```text
KeyError: 'from': not observed
No space left on device: not observed
safetensors ENOSPC: not observed
ShareGPT conversion progress: not observed
training step progress: not observed
```

Interpretation: S22 did not reach data conversion, training progress, or checkpoint save. It also did not produce a checkpoint/model, trainer state, results file, model id, or served endpoint usable by mini-swe.

## Eval Decision

Status: `BLOCKED_FINAL_EVAL_EVIDENCE`

mini-swe remains blocked because no accepted model form exists:

- no complete checkpoint/model directory;
- no `trainer_state.json`;
- no `all_results.json`;
- no model id;
- no served endpoint;
- stopped runtime endpoint now refuses connection;
- no PM-gated eval handoff exists.

No mini-swe eval was run for this task.

## Why Mini-SWE Cannot Run

mini-swe requires an eval-usable model target. The current S22 runtime evidence provides neither accepted form:

- Served endpoint form: absent. There is no reachable OpenAI-compatible endpoint, no model id, and the former LTP endpoint refuses connection after stop.
- Checkpoint plus serving handoff form: absent. There are no checkpoint files and no complete model directory to serve.

Running mini-swe now would test infrastructure against a missing model target rather than evaluate the SFT output, so it would not satisfy the milestone eval gate.

## Accepted Future Model Forms

Future unblock requires PM-gated evidence for one of these forms.

Accepted served endpoint form:

```text
OPENAI_BASE_URL=<reachable OpenAI-compatible /v1 endpoint>
OPENAI_API_KEY=<token or explicit no-auth marker>
MODEL_NAME=<served model id>
health check result for /models or equivalent
simple completion response proof
serving owner
serving command/log path/manifest
source runtime task id and run id
```

Accepted checkpoint plus serving handoff form:

```text
SFT checkpoint/model path
config files present
tokenizer files present
complete weight shards or adapter files present
shard index present if applicable
trainer_state.json or PM-approved replacement completion proof
all_results.json or PM-approved replacement metrics
serving command or endpoint handoff
model id exposed to mini-swe
PM gate approving the artifact for eval
```

## Future Eval Storage Rule

Future mini-swe eval generated artifacts must default to CephFS under `/home/xu.yang`.

Default task eval root:

```text
/home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2
```

Future mini-swe eval paths:

```text
logs: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/logs
predictions: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/output/preds.json
metrics: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/output/metrics_readiness.json
results: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/output/results.json, if scoring runs
run metadata: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/metadata
temporary datasets/intermediates: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/tmp
HF cache: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/hf_home
HF datasets cache: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/hf_datasets_cache
uv cache: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/uv_cache
Apptainer/Singularity cache: /home/xu.yang/milestone1_qwen3_8b_loop/m1_s22_eval_blocked_test2/apptainer_cache
```

Existing required path exceptions, if a future eval is authorized:

- `/root/workspace/swe-bench-related/mini-swe-agent` may be used as the existing required mini-swe source checkout.
- `/root/workspace/swe-bench-related/.runtime/swebench_lite_config.yaml` may be used as the existing required mini-swe/SWE-bench config path.

Exception justification: those `/root/workspace/...` paths are pre-existing source/config inputs on the corrected final workspace. Future generated eval logs, predictions, metrics, run metadata, temporary datasets, caches, and intermediates must remain under `/home/xu.yang`.

## Fields To Verify When A Model Exists

When PM gates a complete checkpoint/model or served endpoint, test_2 should verify:

- source task id and run id;
- PM gate approval for eval;
- endpoint URL/model id/auth and health response, if served endpoint form;
- checkpoint path, config/tokenizer/weights, and completion artifacts, if checkpoint form;
- serving handoff from checkpoint to endpoint, if checkpoint form;
- mini-swe checkout path, git sha, and dirty-state provenance;
- backend: Singularity/Apptainer availability on corrected final workspace;
- CephFS output root under `/home/xu.yang`;
- `preds.json`, `metrics_readiness.json`, optional `results.json`, and trajectory/log files after an authorized eval;
- required prediction fields: `instance_id`, `model_name_or_path`, `model_patch`.

## Current Result

Result: `BLOCKED_FINAL_EVAL_EVIDENCE`

Reason: Session 22 runtime evidence has `EXIT_STATUS=1` and produced no checkpoint/model, no `trainer_state.json`, no `all_results.json`, no model id, and no served endpoint. The stopped endpoint refuses connection. Future eval artifacts remain defaulted to `/home/xu.yang`. No mini-swe eval was run.
