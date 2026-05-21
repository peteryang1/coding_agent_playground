# dev_2 S23 SXid Different-Node Preflight + Conditional SFT Runtime

Task ID: `M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2`

Owner: `intern_code_dev_2`

Created: 2026-05-21T14:01:55Z

Scope: PM-authorized exactly one fresh owner-executed single-node 8 x H200 LTP runtime. Avoid `lg-cmc-b7r202-q03u26-h200-000730` and prior failed nodes if selectable; if the same SXid node is assigned, stop/release and record blocker instead of running preflight/SFT. Run structured preflight first; run SFT only if preflight `PASS` and `sft_allowed=true`. Eval is not authorized.

## Authorization / Boundaries

```text
authorized owner: intern_code_dev_2
authorized fresh allocations: 1
task id: M1-S23-SXID-DIFFERENTNODE-PREFLIGHT-SFT-RUNTIME-DEV2
avoid nodes: lg-cmc-b7r202-q03u26-h200-000730, lg-cmc-b7r202-p07u16-h200-000708, lg-cmc-b7r401-a04u26-h200-000769, lg-cmc-b7r202-q04u06-h200-000725
same SXid node handling: stop/release and do not run preflight/SFT
output root: /home/xu.yang/coding_agent_playground/outputs
remote network rule: no remote git clone/fetch/GitHub/source/dependency download
eval: not authorized
```

## Local Bundle / Data Preparation

Source package reused from the previously verified local/provided PR #51 merge-commit bundle, copied into a new run-specific name for this task.

```text
source commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
source provenance: PR #51 merge commit available locally from /work-agents/intern_code_dev_4/coding_agent_playground
run id: milestone1_qwen3_8b_s23_sxid_differentnode_preflight_sft_20260521T140155Z
bundle: /tmp/cap_s23_sxid_differentnode_20260521T140155Z_c02a53a344f2ad7a33b04f529d5125677237d4cb.tar.gz
bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
file list: /tmp/cap_s23_sxid_differentnode_20260521T140155Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_file_list.txt
file list count: 106
remote bundle sha file: /tmp/cap_s23_sxid_differentnode_20260521T140155Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_remote_bundle.sha256
critical checksum file: /tmp/cap_s23_sxid_differentnode_20260521T140155Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_remote_critical_files.sha256
```

Dataset:

```text
local dataset: /tmp/cleaned_m1_sft_10_sharegpt_s23_sxid_differentnode_20260521T140155Z/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
row count: 10
schema: ShareGPT messages[*].from/value
dataset_info entry: coding_agent_m1_sft_10_sharegpt
```

Critical file checksum provenance from the verified package:

```text
scripts/parse_s22_preflight_health.py sha256: 4bf4843adfee7f169ce9bcc99a2e67fd2cd149467a031cfa81d1b548da193084
scripts/train_qwen3_8b_sft.sh sha256: 9dd84e02bea54915a613159012b0981070ba03e5d3b9cbd8fcda1047957b3cc5
configs/train/qwen3_8b_sft_smoke_tp8_maxsteps2.yaml sha256: 6493c82d54025d9c7bf6f3afe6e37cb9ea4e5bfe850af9643411f6d6d2591614
scripts/write_sft_run_manifest.py sha256: f0f80d88452c26dc46866316b2946f419c5eabd6ab2b41ab2d7c9a4b394f997f
```

## LTP Submit Plan

```text
LTP yaml: /tmp/coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z.yaml
LTP frame: xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
shape: single node, 8 x H200, h200agentic virtual cluster
submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z.yaml
status command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py status xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
```

Initial status: `LOCAL_BUNDLE_READY_PRE_SUBMIT`

## Final Runtime Result

Final status: `BLOCKED_SAME_SXID_NODE_STOPPED_NO_PREFLIGHT_NO_SFT`

The single authorized fresh allocation was assigned to the exact SXid node that PM instructed dev_2 to avoid. Per authorization, I stopped/released the frame and did not run structured preflight or SFT.

```text
LTP frame: xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
LTP submit command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py submit /tmp/coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z.yaml
LTP submit result: HTTP 202
LTP wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z --state RUNNING --timeout 1800 --interval 15
RUNNING observed: 2026-05-21T14:03:41Z
endpoint: ssh -p 39629 root@10.100.22.36
node identity command: ssh -p 39629 root@10.100.22.36 'hostname'
assigned node: lg-cmc-b7r202-q03u26-h200-000730
avoid/SXid node: lg-cmc-b7r202-q03u26-h200-000730
node decision: SAME_SXID_NODE_BLOCKER
preflight: not run
SFT: not run
eval: not authorized and not run
```

The node identity check also observed bootstrap still in OS package setup at the time of stop:

```text
checked UTC: 2026-05-21T14:03:48Z
process sample: apt update -y
```

No source/data transfer to the GPU node was performed for this runtime because the avoid-node gate failed before transfer/preflight.

## Preserved Local Provenance

The local/provided workspace package remains available for a future PM-authorized retry:

```text
source commit: c02a53a344f2ad7a33b04f529d5125677237d4cb
bundle: /tmp/cap_s23_sxid_differentnode_20260521T140155Z_c02a53a344f2ad7a33b04f529d5125677237d4cb.tar.gz
bundle sha256: 59dcaa7dc67473501b900563c4cd90873bf1f0912a5d5ef3a0808b1a15c35a5a
file list: /tmp/cap_s23_sxid_differentnode_20260521T140155Z_c02a53a344f2ad7a33b04f529d5125677237d4cb_file_list.txt
file list count: 106
dataset: /tmp/cleaned_m1_sft_10_sharegpt_s23_sxid_differentnode_20260521T140155Z/train.jsonl
dataset sha256: 26a93abae6f125f4c6bc8e572dd1b0e63085ac805b238128a2d66c24910c1ea2
dataset rows: 10
```

No remote `git clone`, `git fetch`, GitHub/source fetch, remote source download, or project dependency download occurred.

## Stop Proof

```text
stop timestamp UTC: 2026-05-21T14:04:01Z
stop command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py stop xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z
stop result: HTTP 202, stop signal sent
post-stop wait command: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py wait xu.yang~coding-agent-playground-m1-s23-sxid-differentnode-preflight-sft-20260521T140155Z --state STOPPED --timeout 600 --interval 10
post-stop state: STOPPED (Completed)
completed: 2026-05-21 14:04:32
endpoint proof: ssh -p 39629 root@10.100.22.36 => connect to host 10.100.22.36 port 39629: Connection refused
no-running-job proof: python3 /work-agents/axrd/workspace/.skill_sources/intern_agent_skills/intern_ltp_skill/scripts/ltp.py list --user xu.yang --state RUNNING --keyword coding-agent-playground => No jobs found
```

## Artifact / Output Status

```text
generated /home/xu.yang artifacts: none from this runtime; stopped before transfer/preflight
checkpoint/model: absent; SFT was not run
trainer_state.json: absent; SFT was not run
all_results.json: absent; SFT was not run
eval output: absent; eval was not authorized
```

Final next routing recommendation: a future retry needs fresh PM authorization and a mechanism to avoid scheduling onto `lg-cmc-b7r202-q03u26-h200-000730` and the prior failed nodes, or a compute/LTP placement route that can guarantee a different physical node before dev_2 consumes another runtime attempt.
