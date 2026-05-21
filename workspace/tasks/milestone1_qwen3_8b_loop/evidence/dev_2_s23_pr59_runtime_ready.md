# dev_2 S23 PR59 Runtime Readiness

Task ID: `M1-S23-PR59-RUNTIME-READY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T16:25:00Z

Scope: no-submit/no-runtime readiness while PR #59 owner merge is pending. This file is a future-runtime checklist only. It does not authorize LTP, GPU use, remote commands, transfer, preflight, SFT, eval, dry-run, or endpoint probing.

## Current Authorization State

```text
runtime authorized: no
PR #59 owner merge: pending at task assignment time
LTP submit authorized: no
remote commands authorized: no
transfer authorized: no
preflight authorized: no
SFT authorized: no
eval authorized: no
dry-run authorized: no
```

This readiness package is based on durable evidence only:

```text
dev_2 PR57 runtime evidence: evidence/dev_2_s23_pr57_preflight_sft_runtime.md
dev_2 PR57 recovery evidence: evidence/dev_2_s23_pr57_resource_recovery.md
dev_4 mcore fix evidence: evidence/dev_4_s23_pr57_mcore_fix.md
dev_1 mcore review: evidence/dev_1_s23_pr57_mcore_review.md
test_1 mcore gate: evidence/test_1_s23_pr57_mcore_gate.md
```

## Readiness Summary

Current readiness status: `READY_PACKAGE_ONLY_NO_SUBMIT`

The prior PR57 runtime reached:

```text
preflight: PASS
sft_allowed: true
sft blocker: ImportError: mcore_adapter is required when USE_MCA=1
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
eval: not run
resource: stopped/released
```

The PR59 path must preserve the successful PR57 gates and add explicit local/provided `mcore_adapter` provenance plus import-check evidence before any SFT starts.

## Source and Dependency Provenance Requirements

Future PM-authorized runtime must record:

```text
source commit: PR #59 merged/completion-marked commit selected by PM
source repository/worktree: local/provided workspace only
source worktree status: clean at packaging time
source file list: absolute local path to file list
source file count: exact count
source bundle: absolute local path
source bundle sha256: recorded before transfer
critical checksum file: script/config/test checksums recorded before transfer
dataset path: local/provided ShareGPT train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset row/schema proof: 10 rows, ShareGPT messages[*].from/value
```

`mcore_adapter` must be prepared from local/provided source or a local/provided artifact. It must not be cloned, fetched, downloaded, or installed from a remote network on the GPU/LTP node.

Required `mcore_adapter` provenance fields:

```text
mcore_adapter source type: local/provided source tree or local/provided package artifact
mcore_adapter source path: /work-agents/<owner_or_provided_workspace>/coding_agent_playground/code/mcore_adapter or PM-provided equivalent
mcore_adapter source commit/provenance: commit, artifact id, or PM-provided path provenance
mcore_adapter file list: /tmp/mcore_adapter_<RUN_ID>_file_list.txt
mcore_adapter file count: exact count
mcore_adapter bundle: /tmp/mcore_adapter_<RUN_ID>.tar.gz
mcore_adapter bundle sha256: /tmp/mcore_adapter_<RUN_ID>.tar.gz.sha256
mcore_adapter checksum manifest: /tmp/mcore_adapter_<RUN_ID>_files.sha256
```

Local preparation template only:

```bash
RUN_ID=<future_pm_authorized_run_id>
MCORE_SRC=/work-agents/<owner_or_provided_workspace>/coding_agent_playground/code/mcore_adapter
test -d "${MCORE_SRC}"
find "${MCORE_SRC}" -type f | sort > /tmp/mcore_adapter_${RUN_ID}_file_list.txt
tar -C "$(dirname "${MCORE_SRC}")" -czf /tmp/mcore_adapter_${RUN_ID}.tar.gz "$(basename "${MCORE_SRC}")"
sha256sum /tmp/mcore_adapter_${RUN_ID}.tar.gz > /tmp/mcore_adapter_${RUN_ID}.tar.gz.sha256
(cd "$(dirname "${MCORE_SRC}")" && find "$(basename "${MCORE_SRC}")" -type f -print0 | sort -z | xargs -0 sha256sum) > /tmp/mcore_adapter_${RUN_ID}_files.sha256
```

## Future Transfer Template

No transfer may run until fresh PM runtime authorization exists and an LTP endpoint has been allocated. Future transfer must use local bundles only.

Destination layout:

```text
remote workspace: /root/workspace
remote repo destination: /root/workspace/coding_agent_playground
remote dependency destination: /root/workspace/coding_agent_playground/code/mcore_adapter
remote dataset destination: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
generated output root: /home/xu.yang/coding_agent_playground/outputs
```

Transfer command template:

```bash
scp -P <PORT> -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cap_s23_pr59_<RUN_ID>_<COMMIT>.tar.gz \
  /tmp/cap_s23_pr59_<RUN_ID>_<COMMIT>.tar.gz.sha256 \
  /tmp/cap_s23_pr59_<RUN_ID>_<COMMIT>_file_list.txt \
  /tmp/cap_s23_pr59_<RUN_ID>_<COMMIT>_critical_files.sha256 \
  /tmp/mcore_adapter_<RUN_ID>.tar.gz \
  /tmp/mcore_adapter_<RUN_ID>.tar.gz.sha256 \
  /tmp/mcore_adapter_<RUN_ID>_file_list.txt \
  /tmp/mcore_adapter_<RUN_ID>_files.sha256 \
  /tmp/cleaned_m1_sft_10_sharegpt_<RUN_ID>/train.jsonl \
  root@<HOST>:/root/workspace/
```

Tar-over-SSH alternate template:

```bash
tar -C /tmp -cf - \
  cap_s23_pr59_<RUN_ID>_<COMMIT>.tar.gz \
  cap_s23_pr59_<RUN_ID>_<COMMIT>.tar.gz.sha256 \
  cap_s23_pr59_<RUN_ID>_<COMMIT>_file_list.txt \
  cap_s23_pr59_<RUN_ID>_<COMMIT>_critical_files.sha256 \
  mcore_adapter_<RUN_ID>.tar.gz \
  mcore_adapter_<RUN_ID>.tar.gz.sha256 \
  mcore_adapter_<RUN_ID>_file_list.txt \
  mcore_adapter_<RUN_ID>_files.sha256 \
  | ssh -p <PORT> -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@<HOST> \
      'mkdir -p /root/workspace && tar -C /root/workspace -xf -'
scp -P <PORT> -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  /tmp/cleaned_m1_sft_10_sharegpt_<RUN_ID>/train.jsonl \
  root@<HOST>:/root/workspace/train.jsonl
```

No remote `git clone`, `git fetch`, GitHub/source fetch, `pip download`, dependency download, or package-index install may be used on the GPU/LTP node for project code or dependencies.

## Post-Transfer Verification Plan

Post-transfer verification command template:

```bash
ssh -p <PORT> -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@<HOST> 'set -euo pipefail
cd /root/workspace
sha256sum -c cap_s23_pr59_<RUN_ID>_<COMMIT>.tar.gz.sha256
sha256sum -c mcore_adapter_<RUN_ID>.tar.gz.sha256
rm -rf coding_agent_playground
mkdir -p coding_agent_playground
tar -C coding_agent_playground --strip-components=1 -xzf cap_s23_pr59_<RUN_ID>_<COMMIT>.tar.gz
mkdir -p coding_agent_playground/code
tar -C coding_agent_playground/code -xzf mcore_adapter_<RUN_ID>.tar.gz
test -d coding_agent_playground/code/mcore_adapter
test -f /root/workspace/train.jsonl
sha256sum /root/workspace/train.jsonl
find coding_agent_playground -type f | wc -l
(cd coding_agent_playground && sha256sum -c /root/workspace/cap_s23_pr59_<RUN_ID>_<COMMIT>_critical_files.sha256)
(cd coding_agent_playground/code && sha256sum -c /root/workspace/mcore_adapter_<RUN_ID>_files.sha256)
'
```

Required evidence fields after transfer:

```text
exact transfer command
remote destination
source bundle sha256 verification result
source file count
critical file checksum result
mcore_adapter bundle sha256 verification result
mcore_adapter file count
mcore_adapter file checksum result
dataset sha256 verification result
no remote source/dependency download proof statement
```

## Runtime Environment Requirements

Required environment:

```bash
export OUTPUT_ROOT=/home/xu.yang/coding_agent_playground/outputs
export MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
export USE_MCA=1
```

`MCORE_ADAPTER_DIR` must point to the transferred local/provided dependency path:

```text
MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
```

Python import-check command template:

```bash
ssh -p <PORT> -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@<HOST> 'set -euo pipefail
cd /root/workspace/coding_agent_playground
export MCORE_ADAPTER_DIR=/root/workspace/coding_agent_playground/code/mcore_adapter
export PYTHONPATH="${MCORE_ADAPTER_DIR}:/root/workspace/coding_agent_playground/code/LLamaFactory/src:${PYTHONPATH:-}"
python3 - <<'"'"'PY'"'"'
import os
import importlib
path = os.environ["MCORE_ADAPTER_DIR"]
assert os.path.isdir(path), path
mod = importlib.import_module("mcore_adapter")
print("mcore_adapter import OK for USE_MCA=1")
print("mcore_adapter module:", getattr(mod, "__file__", "namespace"))
PY'
```

The import-check output must be recorded before SFT. If it fails, SFT must not run; stop/release the node and record an exact blocker.

## Output and Path Plan

All generated artifacts must be under:

```text
/home/xu.yang/coding_agent_playground/outputs
```

Expected future path layout:

```text
capacity probes: /home/xu.yang/coding_agent_playground/outputs/capacity_probes/<RUN_ID>
preflight: /home/xu.yang/coding_agent_playground/outputs/preflight/<RUN_ID>
run metadata: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>
training run: /home/xu.yang/coding_agent_playground/outputs/runs/train/<SFT_RUN_ID>
logs: /home/xu.yang/coding_agent_playground/outputs/runs/train/<SFT_RUN_ID>/logs
tmp/converted data: /home/xu.yang/coding_agent_playground/outputs/tmp/<RUN_ID>
checkpoints/model: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/<SFT_RUN_ID>
stop proof/evidence copies: /home/xu.yang/coding_agent_playground/outputs/runs/<RUN_ID>/resource_stop
```

Existing required read-only input exceptions must be justified in runtime evidence if used, for example the base model under `/mnt/3fs/data/ai4ai/models/...` or pre-existing local dependency tarballs under `/mnt/3fs/data/ai4ai/deps/...`.

## Future Preflight and SFT Gate

Future runtime must run structured preflight first. SFT may run only if:

```text
PREFLIGHT_RESULT=PASS
SFT_ALLOWED=true
mcore_adapter import check: PASS
home/output capacity probe: PASS
source/data/dependency verification: PASS
PM authorization: fresh and explicit
```

If any gate fails, do not run SFT. Stop/release the node and record exact blocker evidence.

## Stop Conditions

Future PM-authorized runtime must stop/release the LTP allocation on any of:

```text
assigned node fails PM placement/health criteria
/home/xu.yang/coding_agent_playground/outputs unavailable or capacity probe fails
source/data/dependency transfer or checksum verification fails
mcore_adapter import check fails
structured preflight fails or SFT_ALLOWED is not true
SFT exits success or failure
checkpoint/model created and artifact summary recorded
training process hangs or no fresh artifacts progress within PM-defined idle limit
node health becomes unhealthy
PM/test stop instruction
hard stop/review deadline from PM authorization
```

Stop proof must include:

```text
LTP stop command
timestamp UTC
post-stop LTP status
endpoint refusal proof
no-running-job proof
artifact preservation note under /home/xu.yang/coding_agent_playground/outputs
```

## Completion

Completion marker: `READY_NO_SUBMIT_PR59_RUNTIME_PACKAGE`

No LTP submit, remote command, transfer, preflight, SFT, eval, dry-run, or GPU-node mutation was performed for this readiness task. Fresh PM authorization after PR #59 owner merge/completion is required before any runtime action.
