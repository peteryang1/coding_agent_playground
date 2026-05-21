# dev_2 S23 PR61 Resource Recovery / Readiness

Task ID: `M1-S23-PR61-RESOURCE-READY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T17:41:13Z

Scope: no-submit recovery/readiness after the stopped PR61 runtime. Per PM instruction, this task used existing final evidence only. I did not submit LTP, connect to a GPU endpoint, run remote commands, run preflight, run SFT, run eval, transfer files, or mutate any remote state.

## Prior Runtime Stop / No-Active-Job Proof

Source evidence:

```text
runtime evidence: evidence/dev_2_s23_pr61_preflight_sft_runtime.md
tracking evidence: evidence/gpu_s23_pr61_preflight_sft_tracking.md
```

Final stopped proof from existing evidence:

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr61-preflight-sft-20260521T171551Z
endpoint: ssh -p 33089 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
final LTP state: STOPPED (Completed)
submitted: 2026-05-21 17:22:24
started: 2026-05-21 17:22:28
completed: 2026-05-21 17:32:52
endpoint proof: ssh -p 33089 root@10.100.22.31 refused connection
running coding-agent-playground jobs: No jobs found.
active Milestone GPU held by dev_2: no
```

## PR61 Runtime Summary

Preflight/resource gates that passed:

```text
source/data/mcore local package: PASS
CephFS /home/xu.yang output root: PASS after mount/path repair using LTP bootstrap parameters
capacity probe: PASS_AND_CLEANED, 25769803776 bytes
transfer verification: PASS
mcore_adapter import check: PASS, MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
structured preflight: PASS
SFT_ALLOWED: true
TORCH_NCCL_ALLREDUCE_EXIT: 0
HOME_XU_YANG_STORAGE_STATUS: PASS
TOPOLOGY_CAPTURE_STATUS: PRESENT
NVLINK_CAPTURE_STATUS: PRESENT
```

One authorized SFT attempt ran because transfer/import/preflight passed and `SFT_ALLOWED=true`.

SFT result:

```text
run id: milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
checkpoint dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr61_sft_20260521T171551Z
exit status: EXIT_STATUS=1, END_UTC=2026-05-21T17:31:39Z
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run, not authorized
```

PR61 CLI fix verification:

```text
LLAMAFACTORY_CLI=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
LLAMAFACTORY_CMD=python3 /root/workspace/coding_agent_playground/code/LLamaFactory/src/llamafactory/launcher.py
prior quoted single-path signature: not observed
launcher reached: yes
```

Final blocker:

```text
blocker: BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE
failure signature: ValueError: Please provide `model_name_or_path`.
trace path: llamafactory/launcher.py -> train/tuner.py -> hparams/parser.py -> model_args.py
observed contradiction: generated runtime YAML contains `model_name_or_path: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6`, but LLamaFactory MCA argument parsing still raised `Please provide model_name_or_path` before training/checkpoint work.
classification: SFT launch/config parser blocker, not a resource, data, transfer, preflight, or PR59 CLI quoting blocker.
```

## Preserved Provenance

Source provenance:

```text
PR #61 merge commit: aa426b045b52b71bc23b4a2f73f3ee1c42187037
completion PR #62 merge commit / origin main used: 713862da983f73b165af1cfe27935ccef616a049
source repository: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049
source file count: 135
source bundle: /tmp/cap_s23_pr61_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z_713862da983f73b165af1cfe27935ccef616a049.tar.gz
source bundle sha256: a8aeb73d6f3c69775997b7c4b6cf49344a0e8691a44811b68d5678caaacb83c4
critical source checksums: verified in prior runtime evidence
```

Data provenance:

```text
dataset source: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
remote runtime dataset path: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset_info entry: coding_agent_m1_sft_10_sharegpt
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
schema: ShareGPT messages[*].from/value
```

Dependency provenance:

```text
mcore_adapter source: /mnt/3fs/data/ai4ai/deps/mcore_adapter/src
mcore_adapter file count: 222
mcore_adapter bundle: /tmp/mcore_adapter_milestone1_qwen3_8b_s23_pr61_preflight_sft_20260521T171551Z.tar.gz
mcore_adapter bundle sha256: 4a099495d008e8a9b4d47332c0aee639ab97ecb5a181cb531d7d3ef7ed408fdb
LLamaFactory bundle: /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz
LLamaFactory sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
python dependency bundle: /tmp/cap_pr55_pydeps_20260521T1505.tar.gz
python dependency bundle sha256: e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
flash_attn wheel: /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
flash_attn sha256: c3941d81dd09fd1b39dc3df75097d8aa491250a551c919cd2e3c5df0a514fe0d
```

No-remote-network rule preserved: future GPU/LTP nodes must not run remote `git clone`, `git fetch`, GitHub/source/dependency downloads, `pip download`, or network dependency staging. Prepare source/data/dependency bundles locally or in a provided workspace, verify commit/file list/checksums locally, transfer by `scp`/`rsync`/tar-over-SSH, and verify checksums on-node.

## Future Retry Preconditions

No runtime is authorized by this readiness task. A future retry requires fresh PM authorization after the appropriate owner/gate tasks complete.

Exact preconditions before any future submit:

```text
1. dev_4 or assigned fix owner provides a no-execution fix for BLOCKED_PR61_RUNTIME_MCA_MODEL_NAME_OR_PATH_PARSE.
2. Fix evidence explains why LLamaFactory MCA parsing ignored or failed to bind `model_name_or_path` from generated YAML.
3. Fix preserves PR61 command-string handling: `LLAMAFACTORY_CLI` command strings must parse into `LLAMAFACTORY_CMD`, and the prior quoted single-path signature must remain absent.
4. Fix preserves `DEP_TARGET`, `LF`, `LLAMAFACTORY_CLI`, `MCORE_ADAPTER_DIR`, no-remote-network, local bundle transfer, `/home/xu.yang/coding_agent_playground/outputs`, manifest/logging, and stop-proof guarantees.
5. dev_1 review records PASS_FOR_PM_RETRY or exact blocker.
6. test_1 gate records PASS_FOR_PM_RETRY or exact blocker.
7. dev_3 confirms no data/package change is needed, or provides updated data/package provenance if PM changes the data contract.
8. test_2 remains blocked until a complete checkpoint/model or PM-approved served endpoint exists; eval remains unauthorized unless PM separately authorizes.
9. PM separately authorizes a fresh owner-executed runtime and defines the task id/evidence paths.
```

Future resource/runtime readiness template after PM authorization:

```text
shape: fresh single-node 8 x NVIDIA H200
output root: /home/xu.yang/coding_agent_playground/outputs
preflight path: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>
run path: /home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>
checkpoint path: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<RUN_ID>
tmp/intermediates: /home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>
capacity probe: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>
SFT gate: run SFT only if transfer/import/preflight PASS and SFT_ALLOWED=true
stop conditions: transfer/import/preflight failure, SFT_ALLOWED=false, SFT success, SFT failure, checkpoint/model completed, node health issue, idle/no-progress limit, PM/test stop instruction
stop proof required: LTP stop command/action, UTC timestamp, final STOPPED (Completed) status, endpoint refused, running-list no active coding_agent_playground job, output preservation note
```

## Final Status

```text
status: COMPLETE_FOR_NO_SUBMIT_RESOURCE_READY
new LTP submit: no
remote/GPU command: no
preflight/SFT/eval/dry-run: no
fresh PM authorization required before any new LTP/GPU/preflight/SFT/eval: yes
```
