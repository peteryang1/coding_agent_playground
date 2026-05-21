# M1-S23-PR57-LAUNCH-SUPPORT-DEV4

Owner: `intern_code_dev_4`

Date: `2026-05-21`

Scope: no-execution wrapper/launch support standby for the PR57 path. Dev_4 should only recommend or patch another wrapper/launch fix if dev_2 reports a concrete blocker from the PR57 runtime.

Runtime boundary: no LTP/GPU/preflight/SFT/eval/dry-run/runtime command was run by dev_4 for this task.

## Supervisor Correction Recorded

Remote GPU/LTP nodes are no-external-network targets for project code and dependency staging.

Required future runtime behavior:

```text
1. Do not run remote git clone, git fetch, GitHub/source downloads, pip downloads, or project dependency downloads on GPU/LTP nodes.
2. Prepare code/config/scripts/data/dependency bundles in the local or provided workspace first.
3. Verify exact source commit, file list, and checksums locally before transfer.
4. Transfer prepared bundles by rsync, scp, or tar-over-SSH.
5. Record exact transfer command, source path, destination path, file list, bundle checksum, critical-file checksums, and post-transfer verification in runtime evidence/status.
6. Keep generated artifacts, logs, checkpoints, run metadata, temporary converted data, and intermediates under /home/xu.yang/coding_agent_playground/outputs unless an existing required input path is explicitly justified.
```

PM coordinates and gates only; PM will not run transfer, remote, SFT, or eval commands.

## PR57 / PR58 Landed State

```text
PR #57: https://github.com/peteryang1/coding_agent_playground/pull/57
PR #57 mergedAt: 2026-05-21T15:45:10Z
PR #57 merge commit: c450429c2e3369adc723d132396399cd17dba684

PR #58: https://github.com/peteryang1/coding_agent_playground/pull/58
PR #58 mergedAt: 2026-05-21T15:48:30Z
PR #58 merge commit: b4ac31ef1e3772953108348bf099818326ed65cc
```

PR #57 landed the wrapper/env fix for the PR55 SFT launch blocker:

```text
DEP_TARGET default/export
LF default/export
LLAMAFACTORY_CLI default/export
manifest launch command includes explicit DEP_TARGET/LF/PYTHONPATH
final train invocation uses configurable "${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"
```

PR #58 landed the task completion record for `M1-S23-PR55-SFT-WRAPPER-FIX-DEV4`.

## Static Test Provenance

Static checks recorded for PR #57:

```bash
bash -n scripts/train_qwen3_8b_sft.sh
python3 -m py_compile tests/test_train_qwen3_8b_sft_static.py
python3 -m pytest tests/test_train_qwen3_8b_sft_static.py -q
```

Observed result in dev_4 evidence:

```text
2 passed in 0.01s
```

The static test file `tests/test_train_qwen3_8b_sft_static.py` verifies:

```text
DEP_TARGET default is under ${RUN_DIR}/python_deps unless PYTHON_DEPS_DIR overrides it.
LF defaults to ${LLAMAFACTORY_DIR}.
DEP_TARGET, LF, and LLAMAFACTORY_CLI are exported.
LLAMAFACTORY_CLI is configurable.
Manifest command and final train invocation use the configurable LLamaFactory CLI wrapper.
```

## Current Support Recommendation

No new dev_2 PR57 wrapper/launch blocker is present in durable evidence at this recording point.

Current recommendation:

```text
No additional dev_4 code/config patch is recommended unless dev_2 reports a concrete wrapper/launch blocker from the PR57 runtime.
If a blocker appears, preserve PR57 wrapper env contract first and diagnose against the transferred source bundle/checksum evidence, not by running remote code from dev_4.
```

## Status

```yaml
task_id: M1-S23-PR57-LAUNCH-SUPPORT-DEV4
owner: intern_code_dev_4
result: READY_SUPPORT_NO_NEW_FIX
evidence_path: workspace/tasks/milestone1_qwen3_8b_loop/evidence/dev_4_s23_pr57_launch_support.md
pr57_merged: true
pr57_merge_commit: c450429c2e3369adc723d132396399cd17dba684
pr58_merged: true
pr58_merge_commit: b4ac31ef1e3772953108348bf099818326ed65cc
runtime_authorized_for_dev4: false
ltp_gpu_preflight_sft_eval_dry_run_executed_by_dev4: false
next_dev4_action: wait for concrete dev_2 wrapper/launch blocker evidence or PM task
```
