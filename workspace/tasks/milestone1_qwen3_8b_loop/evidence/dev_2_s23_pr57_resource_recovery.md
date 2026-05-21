# dev_2 S23 PR57 Resource Recovery

Task ID: `M1-S23-PR57-RESOURCE-RECOVERY-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T16:17:00Z

Scope: no-submit recovery/readiness after stopped PR57 runtime. No LTP submit, GPU use, preflight, SFT, eval, dry-run, or GPU-node mutation is authorized for this task.

## Control-Plane Checks

Commands run from local/control-plane workspace only:

```bash
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground
```

Frame status:

```text
frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
state: STOPPED (Completed)
exec type: STOP
submitted: 2026-05-21 15:55:39
started: 2026-05-21 15:55:45
completed: 2026-05-21 16:06:06
retries: 0
exit code: -210 Failed
task idx 0 state: STOPPED
endpoint while active: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
```

No-active-job proof:

```text
ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found.
```

Prior endpoint stop proof is recorded in `evidence/dev_2_s23_pr57_preflight_sft_runtime.md` and `evidence/gpu_s23_pr57_preflight_sft_tracking.md`: after stop, `ssh -p 22662 root@10.100.22.31` returned `connect to host 10.100.22.31 port 22662: Connection refused`.

## Runtime Summary

Final runtime status: `BLOCKED_PR57_RUNTIME_MISSING_MCORE_ADAPTER_STOPPED_NO_CHECKPOINT`

The PM-authorized PR57 runtime completed exactly one fresh LTP allocation and one conditional SFT attempt:

```text
source commit: b4ac31ef1e3772953108348bf099818326ed65cc
PR #57 merge commit: c450429c2e3369adc723d132396399cd17dba684
PR #58 merge commit: b4ac31ef1e3772953108348bf099818326ed65cc
frame: xu.yang~coding-agent-playground-m1-s23-pr57-preflight-sft-20260521T155200Z
endpoint: ssh -p 22662 root@10.100.22.31
node: lg-cmc-b7r202-q04u06-h200-000725
output root: /home/xu.yang/coding_agent_playground/outputs
eval: not authorized and not run
```

Structured preflight passed:

```text
PREFLIGHT_RESULT=PASS
PREFLIGHT_STRUCTURED_STATUS=PASS
ACTIONABLE_FAULT=false
SFT_ALLOWED=true
SFT_ALLOWED_IF_PM_AUTHORIZED=true
TORCH_NCCL_ALLREDUCE_EXIT=0
CAPACITY_PROBE_STATUS=PASS
DIFFERENT_NODE_GATE=PASS
HOME_XU_YANG_STORAGE_STATUS=PASS
TOPOLOGY_CAPTURE_STATUS=PRESENT
NVLINK_CAPTURE_STATUS=PRESENT
REASON=allowlisted preflight artifacts passed without actionable health signatures
```

The single authorized SFT attempt failed before producing a checkpoint/model:

```text
sft run id: milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
checkpoint/output dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
exit status: EXIT_STATUS=1
end utc: 2026-05-21T16:03:28Z
blocker: ImportError: mcore_adapter is required when USE_MCA=1. Please install `mcore_adapter` and its dependencies.
secondary failure wrapper: torch.distributed.elastic.multiprocessing.errors.ChildFailedError
checkpoint/model: absent
trainer_state.json: absent
all_results.json: absent
```

## Preserved Provenance

Source and code provenance:

```text
source repository used for packaging: /work-agents/intern_code_dev_4/coding_agent_playground
detached worktree: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc
commit: b4ac31ef1e3772953108348bf099818326ed65cc
worktree status at packaging: clean
file list: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_file_list.txt
file count: 122
source bundle: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc.tar.gz
source bundle sha256: 1393a6c155e265bce6ee99e9507aaae75c3b04c958c2acf1f9760557a14d2baa
critical checksum file: /tmp/cap_s23_pr57_20260521T155200Z_b4ac31ef1e3772953108348bf099818326ed65cc_remote_critical_files.sha256
remote source path during runtime: /root/workspace/coding_agent_playground
remote file count verified: 122
remote critical checksums: OK
```

Dataset provenance:

```text
dataset source: /tmp/cleaned_m1_sft_10_sharegpt/train.jsonl
runtime local copy: /tmp/cleaned_m1_sft_10_sharegpt_s23_pr57_20260521T155200Z/train.jsonl
remote dataset path during runtime: /root/workspace/cleaned_m1_sft_10_sharegpt/train.jsonl
dataset_info entry: coding_agent_m1_sft_10_sharegpt
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
```

Dependency/package provenance:

```text
python dependency bundle: /tmp/cap_pr55_pydeps_20260521T1505.tar.gz
python dependency bundle sha256: e44eeb709ae9224d406c392e9ab277eeb5209677b973e9e7a5869b7aa278666b
LLamaFactory bundle: /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz
LLamaFactory bundle sha256: f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e
remote verification: both bundles verified OK before SFT attempt
observed missing runtime dependency: mcore_adapter when USE_MCA=1
```

Transfer/no-remote-network provenance:

```text
remote GPU/LTP node rule: no external network for project code/dependency staging
remote git clone/fetch/GitHub/source/dependency download: not run
transfer method: local/provided source/data/dependency bundles copied by scp to /root/workspace, then verified on node
source/data/dependency artifacts: preserved locally at the paths listed above
generated runtime artifacts: preserved under /home/xu.yang/coding_agent_playground/outputs
```

Output artifact locations preserved from the stopped runtime:

```text
preflight dir: /home/xu.yang/coding_agent_playground/outputs/preflight/milestone1_qwen3_8b_s23_pr57_preflight_sft_20260521T155200Z
train run dir: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
checkpoint/output dir: /home/xu.yang/coding_agent_playground/outputs/training_summary/sft_output/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z
stdout/stderr log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_stdout_stderr.log
xtrace log: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/logs/train_xtrace.log
run manifest: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/run_manifest.json
runtime config: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/config/qwen3_8b_sft.yaml
final artifact summary: /home/xu.yang/coding_agent_playground/outputs/runs/train/milestone1_qwen3_8b_s23_pr57_sft_20260521T155200Z/final_artifact_summary.txt
```

## Recovery Readiness

No active Milestone/coding_agent_playground GPU is held by dev_2 after the stopped PR57 runtime.

Future retry criteria before any new runtime:

```text
1. Fresh PM authorization is required.
2. dev_4/dev_1/test_1 gates should classify and approve the mcore_adapter/USE_MCA dependency fix or an explicitly supported non-MCA path.
3. Future GPU/LTP nodes must still be treated as no-external-network targets: prepare code/config/scripts/data/dependency bundles locally or in provided workspaces, verify commit/file list/checksums locally, transfer by scp/rsync/tar-over-SSH, and verify after transfer.
4. Generated outputs, logs, temporary datasets, checkpoints, run metadata, preflight artifacts, and capacity probes must remain under /home/xu.yang/coding_agent_playground/outputs unless PM explicitly approves and evidence justifies an existing required input exception.
5. Structured preflight must run before SFT, and SFT may run only if the structured result is PASS and SFT_ALLOWED=true.
```

No new LTP/GPU/preflight/SFT/eval may run without fresh PM authorization.

Completion marker: `COMPLETE_FOR_NO_SUBMIT_RECOVERY`.
