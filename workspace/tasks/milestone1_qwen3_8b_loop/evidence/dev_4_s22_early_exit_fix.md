# Dev 4 Session 22 Early-Exit Fix Package

Task ID: `M1-S22-EARLY-EXIT-FIX-DEV4`

Owner: `intern_code_dev_4`

Created: 2026-05-21T08:36:45Z

Scope: no-execution diagnosis and fix package for the Session 22 Qwen3-8B SFT retry that exited with status 1 before durable training artifacts were produced.

Execution boundary:

```text
No SFT command was run.
No GPU command was run.
No eval command was run.
No peer_send was sent to PM.
```

## Sources Reviewed

```text
evidence/dev_2_s22_enospc_retry_runtime.md
evidence/gpu_s22_enospc_retry_tracking.md
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
```

## Session 22 Runtime Facts

Run:

```text
run_id: milestone1_qwen3_8b_s22_enospcfix_sharegpt_tp8_maxsteps2_20260521T082037Z
frame: xu.yang~coding-agent-playground-m1-s22-enospc-qwen3-8b-runtime-20260521T082037Z
endpoint: ssh -p 31346 root@10.100.16.69
output_root: /home/xu.yang/coding_agent_playground/outputs
dataset: coding_agent_m1_sft_10_sharegpt
dataset_jsonl: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
base_model: /mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

Successful pre-run facts from dev_2:

```text
/home/xu.yang resolved to CephFS /mnt/cephfs/home/xu.yang.
24GiB real-write capacity probe passed under /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>.
repo and ShareGPT dataset were staged.
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset rows: 10
dataset_info entry: coding_agent_m1_sft_10_sharegpt
config template: /tmp/qwen3_8b_sft_s22_enospc.yaml
config template assertions: dataset, output_dir, save_steps=2, save_total_limit=1, max_steps=2, warmup_steps=0, TP=8
```

Final result:

```text
EXIT_STATUS=1
END_UTC=2026-05-21T08:27:52Z
log content: START_UTC=2026-05-21T08:27:52Z
run_manifest.json: absent
generated runtime config: absent
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
GPU after failure: idle; no torchrun/llamafactory/python training process observed
```

Old failure signatures were not observed because the durable log contains only the launch start line:

```text
KeyError: 'from': not observed
No space left on device: not observed
safetensors ENOSPC: not observed
ShareGPT conversion: not observed
training step progress: not observed
```

## Diagnosis

The failure happened before the current durable capture boundary could record the useful stderr/stdout or before the training script reached its first durable artifact writes.

Reasoning from `scripts/train_qwen3_8b_sft.sh`:

```text
1. The script computes REPO_ROOT/RUN_ID/OUTPUT_ROOT/RUN_DIR/CHECKPOINT_DIR.
2. It runs mkdir -p "${RUN_DIR}/logs" "${RUN_DIR}/config" "${CHECKPOINT_DIR}".
3. It writes "${RUN_DIR}/config/qwen3_8b_sft.yaml".
4. It writes "${RUN_DIR}/run_manifest.json".
5. Only after those steps does it check DATASET_JSONL, nvidia-smi, LLamaFactory, and launch llamafactory-cli.
```

Because the generated config and run_manifest are absent, the failure boundary is before or inside steps 1-3, not during ShareGPT conversion, training, or checkpoint save.

Most likely classes:

```text
1. Outer tmux/launch wrapper failure before invoking scripts/train_qwen3_8b_sft.sh, such as cd/path/env/quoting/set -u failure.
2. stderr/stdout redirection established after a fragile prelude, so the real shell error was not appended to train_stdout_stderr.log.
3. Early script prelude failure before durable logging is owned by scripts/train_qwen3_8b_sft.sh, for example dirname/BASH_SOURCE/path resolution, mkdir, reading CONFIG_TEMPLATE, or Python config rewrite.
4. The current train script does not itself redirect all stdout/stderr to the durable log; it relies on the caller to capture logs, leaving pre-redirection errors invisible.
```

This is distinct from prior blockers:

```text
Not the old KeyError: 'from' blocker: data conversion never started.
Not the old safetensors ENOSPC blocker: checkpoint save never started.
Not the old DP=8 steps_in_epoch=0 blocker: training loop never started.
Not the old TP scheduler assertion: optimizer scheduler never initialized.
```

## Required Preservation

Future retry must keep:

```text
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
DATASET_NAME=coding_agent_m1_sft_10_sharegpt
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6
```

`/mnt/3fs` remains a required-path exception only for the selected base model and dependency archives/wheels. Future launch outputs, logs, checkpoints, run metadata, temporary converted datasets, and intermediates must stay under `/home/xu.yang/coding_agent_playground/outputs`.

## Proposed No-Execution Fix

Primary fix: make the repository wrapper own durable logging from the first executable line, then write a preflight report before any training launch.

Patch scope:

```text
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml or a Session 22 replacement config with the same fields
```

Required `scripts/train_qwen3_8b_sft.sh` changes:

```text
1. Change default OUTPUT_ROOT to /home/xu.yang/coding_agent_playground/outputs.
2. Create RUN_DIR/logs before any fragile operation after variable initialization.
3. Redirect all stdout/stderr inside the script:
   exec > >(tee -a "${RUN_DIR}/logs/train_stdout_stderr.log") 2>&1
4. Enable xtrace into a separate durable file:
   exec 9>>"${RUN_DIR}/logs/train_xtrace.log"
   export BASH_XTRACEFD=9
   set -x
5. Add ERR/EXIT traps that always write:
   - exit code
   - failing command
   - line number
   - UTC timestamp
   - RUN_ID/RUN_DIR/CHECKPOINT_DIR/OUTPUT_ROOT
   - artifact presence summary
   to "${RUN_DIR}/early_exit_diagnostics.txt" and "${RUN_DIR}/exit_status.txt".
6. Before config rewrite, log and assert:
   - pwd
   - REPO_ROOT
   - bash version
   - CONFIG_TEMPLATE path/readability/sha256
   - OUTPUT_ROOT/RUN_DIR/CHECKPOINT_DIR mount proof
   - DATASET_JSONL path/readability/sha256/count
   - LLAMAFACTORY_DIR path
   - nvidia-smi location and nvidia-smi -L only after the log is active
7. If DATASET_NAME is set, rewrite top-level dataset: in the runtime config to DATASET_NAME.
8. After runtime config and manifest writes, print their paths and sha256 values to the durable log.
9. Do not exec llamafactory-cli directly; run it normally so the EXIT trap can record status after trainer failure.
```

Recommended wrapper skeleton:

```bash
mkdir -p "${RUN_DIR}/logs" "${RUN_DIR}/config" "${CHECKPOINT_DIR}"
LOG="${RUN_DIR}/logs/train_stdout_stderr.log"
XTRACE="${RUN_DIR}/logs/train_xtrace.log"
DIAG="${RUN_DIR}/early_exit_diagnostics.txt"
STATUS="${RUN_DIR}/exit_status.txt"

exec > >(tee -a "${LOG}") 2>&1
exec 9>>"${XTRACE}"
export BASH_XTRACEFD=9
set -x

on_err() {
  local rc=$?
  {
    date -u +%Y-%m-%dT%H:%M:%SZ
    printf 'ERROR_EXIT=%s\n' "${rc}"
    printf 'ERROR_LINE=%s\n' "${BASH_LINENO[0]:-unknown}"
    printf 'ERROR_COMMAND=%s\n' "${BASH_COMMAND:-unknown}"
    printf 'RUN_ID=%s\nRUN_DIR=%s\nCHECKPOINT_DIR=%s\nOUTPUT_ROOT=%s\n' "${RUN_ID}" "${RUN_DIR}" "${CHECKPOINT_DIR}" "${OUTPUT_ROOT}"
    find "${RUN_DIR}" -maxdepth 3 -type f -printf '%s %p\n' 2>/dev/null || true
  } | tee -a "${DIAG}"
  printf 'EXIT_STATUS=%s\nEND_UTC=%s\n' "${rc}" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "${STATUS}"
  exit "${rc}"
}
trap on_err ERR
```

Use a final status writer for successful completion too:

```bash
printf 'EXIT_STATUS=0\nEND_UTC=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "${STATUS}"
```

Required generated artifacts before any training starts:

```text
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_stdout_stderr.log
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/logs/train_xtrace.log
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/early_exit_diagnostics.txt
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/config/qwen3_8b_sft.yaml
/home/xu.yang/coding_agent_playground/outputs/runs/train/<RUN_ID>/run_manifest.json
```

Required `scripts/write_sft_run_manifest.py` changes:

```text
Record the actual runtime config save policy instead of static save_steps=150/save_total_limit=4.
Include OUTPUT_ROOT, RUN_DIR, CHECKPOINT_DIR, DATASET_NAME, and TMPDIR if set.
Include a "preflight" object with config_exists, dataset_exists, dataset_sha256, output_root, and log paths.
```

Required config scope:

```yaml
dataset: coding_agent_m1_sft_10_sharegpt
save_steps: 2
save_total_limit: 1
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
context_parallel_size: 1
sequence_parallel: false
```

## Exact Future Command Template

No execution is authorized from this package. If PM later authorizes one retry after review/test gates, use the same contract with the patched wrapper:

```bash
cd /root/workspace/coding_agent_playground
RUN_ID="milestone1_qwen3_8b_s22_earlyexitfix_sharegpt_tp8_maxsteps2_$(date -u +%Y%m%dT%H%M%SZ)"
CONFIG_TEMPLATE=/root/workspace/coding_agent_playground/configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml \
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl \
DATASET_NAME=coding_agent_m1_sft_10_sharegpt \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/ws_20260422_2156_qwen3-8b_1bench_61f6 \
OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs \
CHECKPOINT_DIR=/home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/${RUN_ID} \
TMPDIR=/home/xu.yang/coding_agent_playground/outputs/tmp/${RUN_ID} \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

## PR Scope If Needed

If PM wants this converted into a code/config PR, use:

```text
Task ID: M1-S22-EARLY-EXIT-FIX-DEV4
Owner: intern_code_dev_4
Acceptance criteria:
  - train wrapper captures stderr/stdout/xtrace from the first durable point;
  - failure before config/manifest creation produces early_exit_diagnostics.txt and exit_status.txt;
  - /home/xu.yang/coding_agent_playground/outputs remains default output root;
  - DATASET_NAME=coding_agent_m1_sft_10_sharegpt is preserved in generated config;
  - no SFT/GPU/eval execution in the PR.
Evidence path:
  - workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_early_exit_fix.md
Completion marker:
  - Ready-for-review: no-execution early-exit wrapper fix package recorded; retry still requires PM/test/resource gate.
```

Files:

```text
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_early_exit_fix.md
workspace/interns/intern_code_dev_4/status.md
workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
```

## Stop / Rollback Conditions

Do not launch a future retry unless:

```text
early-exit logging patch is landed or staged on the worker;
generated runtime config proof exists before training starts;
run_manifest.json exists before training starts;
/home/xu.yang path and capacity proof pass;
dataset_info entry remains coding_agent_m1_sft_10_sharegpt;
PM explicitly authorizes a new attempt.
```

Stop after launch if:

```text
exit_status is nonzero and early_exit_diagnostics.txt identifies a wrapper/preflight failure;
train_stdout_stderr.log remains only a START line after the patched wrapper, because that means the wrapper was bypassed;
old data-format, ENOSPC, tiny-data, or scheduler failures recur;
no complete checkpoint/model is produced within the PM/test bounded window.
```

## Current Completion Marker

```text
Complete-for-plan: M1-S22-EARLY-EXIT-FIX-DEV4 records a no-execution diagnosis and fix package. The current blocker is earlier than LLamaFactory data conversion/training/checkpointing; future work should patch the launcher/training wrapper to own durable logging, xtrace, config/manifest preflight, DATASET_NAME rewrite, and exit diagnostics under /home/xu.yang/coding_agent_playground/outputs before any PM-authorized retry. No SFT/GPU/eval command was run.
```

## Session 28 No-Execution Patch PR Package

Patch branch:

```text
intern_code_dev_4/M1-S22-EARLY-EXIT-FIX-DEV4
```

Files changed:

```text
scripts/train_qwen3_8b_sft.sh
scripts/write_sft_run_manifest.py
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_early_exit_fix.md
workspace/interns/intern_code_dev_4/status.md
workspace/tasks/milestone1_qwen3_8b_loop/history_log.md
workspace/tasks/milestone1_qwen3_8b_loop/task_knowledge.md
workspace/tasks/milestone1_qwen3_8b_loop/task_registry.md
```

Implemented wrapper changes:

```text
default OUTPUT_ROOT is /home/xu.yang/coding_agent_playground/outputs
TMPDIR defaults under /home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>
script creates run/log/config/checkpoint/tmp directories before fragile work
script redirects stdout/stderr through tee to logs/train_stdout_stderr.log from the first durable point
script writes xtrace to logs/train_xtrace.log by default
ERR trap writes early_exit_diagnostics.txt and exit_status.txt with failing command, line, paths, and artifact summary
EXIT trap writes exit_status.txt for success or non-ERR exits
preflight.json records config/dataset/path/log facts before config rewrite
runtime config rewrite supports DATASET_NAME for top-level dataset:
runtime config and run_manifest paths plus sha256 are printed before training
llamafactory-cli is no longer invoked through exec, allowing traps to record trainer failure status
```

Implemented manifest changes:

```text
scripts/write_sft_run_manifest.py reads simple top-level runtime config scalars.
Manifest checkpoint_policy records actual save_steps, save_total_limit, save_only_model, save_hf_model, and output_dir from generated config.
Manifest preflight section records config/dataset existence, output root, run dir, checkpoint dir, tmpdir, DATASET_NAME, log path, xtrace path, and early_exit_diagnostics path.
```

Implemented config/template addition:

```text
configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
dataset: coding_agent_m1_sft_10_sharegpt
output_dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/qwen3_8b_milestone1_s21_sharegpt_tiny_smoke
save_steps: 2
save_total_limit: 1
max_steps: 2
warmup_steps: 0
tensor_model_parallel_size: 8
pipeline_model_parallel_size: 1
context_parallel_size: 1
sequence_parallel: false
```

Local checks performed:

```text
bash -n scripts/train_qwen3_8b_sft.sh
python3 -m py_compile scripts/write_sft_run_manifest.py
```

Execution boundary for patch PR:

```text
No SFT command was run.
No GPU command was run.
No eval command was run.
No dry-run launch command was run.
```

PR metadata requirement:

```text
Task ID: M1-S22-EARLY-EXIT-FIX-DEV4
Owner: intern_code_dev_4
Acceptance criteria: wrapper captures stdout/stderr/xtrace from the first durable point; early failures produce early_exit_diagnostics.txt and exit_status.txt; generated config preserves DATASET_NAME=coding_agent_m1_sft_10_sharegpt; future outputs remain under /home/xu.yang/coding_agent_playground/outputs; no SFT/GPU/eval execution in PR.
Evidence path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_early_exit_fix.md
Completion marker: Ready-for-review after PR opens; future retry still requires PM/test/resource gate.
```

PR status:

```text
PR #39: https://github.com/peteryang1/coding_agent_playground/pull/39
state: OPEN
draft: false
initial mergeability after open: CONFLICTING / DIRTY
conflict files after merging origin/main locally: history_log.md, task_knowledge.md, task_registry.md
resolution: preserved current origin/main PM/data-format/Session 21/22 records and re-applied Session 28 task evidence/status entries
latest GitHub mergeability after push: MERGEABLE / CLEAN
required checks: none reported
```

## Session 29 PM Follow-Up Verification

PM follow-up scope:

```text
Continue M1-S22-EARLY-EXIT-FIX-DEV4 as a no-execution patch PR.
PR must cite task id, owner, acceptance criteria, evidence path, and completion marker.
Future SFT intermediates/log/checkpoint/run metadata defaults remain under /home/xu.yang.
Do not run SFT/GPU/eval.
```

PR #39 verification:

```text
PR URL: https://github.com/peteryang1/coding_agent_playground/pull/39
state: OPEN
draft: false
base: main
head: intern_code_dev_4/M1-S22-EARLY-EXIT-FIX-DEV4
mergeability: MERGEABLE / CLEAN
required checks: none reported
```

PR body fields verified:

```text
Task ID: M1-S22-EARLY-EXIT-FIX-DEV4
Owner: intern_code_dev_4
Acceptance criteria: present
Evidence path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s22_early_exit_fix.md and workspace/interns/intern_code_dev_4/status.md
Completion marker: Ready-for-review; future retry remains blocked until PM/test/resource gate explicitly authorizes it
Execution boundary: no SFT/GPU/eval or dry-run launch
```

Current durable status:

```text
Ready-for-PM-gate: PR #39 is open, pushed, non-draft, and MERGEABLE/CLEAN. No SFT/GPU/eval command was run in this follow-up.
```

## Session 30 PM Gate Hold

PM gate note:

```text
PR #39 is open, non-draft, and GitHub reports MERGEABLE/CLEAN, but PM gate is not passed yet.
Do not self-merge PR #39 until dev_1 and test_1 review/gate evidence lands and PM explicitly authorizes owner self-merge.
No SFT/GPU/eval or dry-run launch is authorized.
```

Current owner status:

```text
Waiting for PM gate. No self-merge performed. No SFT/GPU/eval or dry-run launch performed.
```

## Session 31 PM Gate Fix Update

PM gate result:

```text
PR #39: NOT READY
dev_1 blocker: BLOCKER_MANIFEST_ENV_CAPTURE
test_1 blocker: BLOCKED_SCOPE_HISTORICAL_EVIDENCE_DIFF
```

`BLOCKER_MANIFEST_ENV_CAPTURE` resolution:

```text
scripts/train_qwen3_8b_sft.sh now exports the resolved values before calling scripts/write_sft_run_manifest.py:
- DATASET_NAME
- OUTPUT_ROOT
- RUN_DIR
- CHECKPOINT_DIR
- TMPDIR
- LOG_FILE
- XTRACE_FILE
- DIAG_FILE

The wrapper also passes those same values explicitly to scripts/write_sft_run_manifest.py.
scripts/write_sft_run_manifest.py accepts --dataset-name, --output-root, --tmpdir, --log-file, --xtrace-file, and --diag-file and records them in run_manifest.json preflight.
Expected future manifest effect: DATASET_NAME=coding_agent_m1_sft_10_sharegpt and /home/xu.yang/coding_agent_playground/outputs-derived preflight paths are captured even if subprocess environment handling changes.
```

`BLOCKED_SCOPE_HISTORICAL_EVIDENCE_DIFF` handling:

```text
Archival justification: PR #39 keeps the durable history/status/task_knowledge evidence records that were required by PM process and conflict-resolution gates for this same task. Splitting them out now would either create a second task/PR without a new PM assignment or remove provenance showing how PR #39 became mergeable after resolving conflicts against current main.

The implementation scope remains limited to:
- scripts/train_qwen3_8b_sft.sh
- scripts/write_sft_run_manifest.py
- configs/train/qwen3_8b_s21_sharegpt_tp8_maxsteps2_finalsave.yaml
- directly required task/status/history/knowledge/evidence records for M1-S22-EARLY-EXIT-FIX-DEV4

No unrelated runtime evidence, checkpoint artifact, GPU result, or eval result is added by this PR.
```

Execution boundary:

```text
No self-merge performed.
No SFT/GPU/eval or dry-run launch performed.
```
