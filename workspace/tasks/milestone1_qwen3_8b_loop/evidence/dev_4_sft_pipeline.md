# dev_4 SFT Pipeline Evidence

## 2026-05-20 Assignment Acknowledgement

- Owner: `intern_code_dev_4`.
- Assignment accepted: Qwen3-8B SFT pipeline, GPU workflow, training command templates, checkpoint layout, and run manifest.
- Durable update rule acknowledged: no routine `peer_send` to PM; confirmations, status, findings, blockers, and test evidence go here plus own `status.md`.
- Initial context read:
  - `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/assignments.md`
  - `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/README.md`
  - `/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/status.md`
- Initial finding: local dev worktree tracks `main`; milestone task docs are currently present in PM worktree, while local `origin/main` does not contain `workspace/tasks/milestone1_qwen3_8b_loop`.
- Active blocker/risk to resolve in this owner area: PM task records note that GPU/SFT allocation workflow and exact launcher need confirmation from axrd records or compute manager before full Qwen3-8B SFT.

## 2026-05-20 Findings and Artifacts

### Axrd References Used

- `/work-agents/intern_rd_dev_1/axrd/ai4ai/statics/skills/developer/dskill_llamafactory-mca-sft/SKILL.md`
- `/work-agents/intern_rd_dev_1/axrd/ai4ai/statics/skills/developer/dskill_gpu_deps/SKILL.md`
- `/work-agents/intern_rd_dev_1/axrd/ai4ai/statics/skills/developer/dskill_train_eval/SKILL.md`
- `/work-agents/intern_rd_dev_1/axrd/ai4ai/statics/skills/developer/dskill_multinode_training/reference/path-discipline.md`
- `/work-agents/intern_rd_dev_1/axrd/ai4ai/statics/skills/developer/dskill_multinode_training/reference/nodes-json.md`

### Final Workspace Probe

- `ssh -p 31787 root@10.100.194.40` succeeded.
- `/root/workspace/{fastapi,scikit-learn,rich}` exist.
- `/mnt/3fs/data/ai4ai/deps` includes:
  - `LLamaFactory_4fa8e1ee_20260507.tar.gz`
  - `flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl`
  - `mcore_adapter`
- `nvidia-smi` is not installed/available on the reached host (`zsh:1: command not found: nvidia-smi`), so this endpoint appears to be CPU/login context rather than an allocated GPU training node.
- Found one historical axrd-style `nodes.json` under `/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json`; no milestone-specific `nodes.json` found.

### Repo Artifacts Added on Branch `intern_code_dev_4/milestone1_qwen3_8b_loop`

- PR: https://github.com/peteryang1/coding_agent_playground/pull/1
- `configs/train/qwen3_8b_sft.yaml`: LLamaFactory/MCA full-SFT template for Qwen3-8B coding-agent ShareGPT data.
- `scripts/train_qwen3_8b_sft.sh`: launch wrapper with dry-run mode, runtime config copy, MCA/NCCL/TransformerEngine env defaults, and prelaunch checks for dataset/GPU/LLamaFactory.
- `scripts/write_sft_run_manifest.py`: dependency-free run manifest writer with config/dataset hashing and checkpoint/output paths.
- `docs/training/qwen3_8b_sft_pipeline.md`: GPU workflow, dependency setup, dataset registration, single-node/multi-node command templates, checkpoint layout, and current GPU blocker.

### Verification

- `bash -n scripts/train_qwen3_8b_sft.sh` passed.
- `python3 -m py_compile scripts/write_sft_run_manifest.py` passed.
- `OUTPUT_ROOT=/tmp/cap_sft_dryrun DRY_RUN=1 RUN_ID=test_manifest bash scripts/train_qwen3_8b_sft.sh` passed and wrote a valid JSON manifest at `/tmp/cap_sft_dryrun/runs/train/test_manifest/run_manifest.json`.

### Active Blockers

- Full training cannot start until a GPU node/allocation is provided or a milestone-specific `nodes.json` is available.
- Final dataset path is pending dev_3 normalized SFT JSONL output; current script supports dry-run before that file exists and fails fast for real launch if `DATASET_JSONL` is missing.

## 2026-05-20 Critical Address Correction Re-Evaluation

### Correction Applied

- Correct final workspace is `ssh -p 31787 root@10.100.194.40`.
- Earlier probes against the previous scratch host are treated as scratch-only and are no longer used for final GPU/SFT assumptions.
- PR artifact `docs/training/qwen3_8b_sft_pipeline.md` was updated to use `31787/root@10.100.194.40` and explicitly mark the old address as scratch-only.

### New Machine Probe Results

- `ssh -p 31787 root@10.100.194.40` succeeded.
- Hostname: `lg-cmc-b7r201-k10u23-cpu-000158`.
- `nvidia-smi` is not available on this entry host (`command -v nvidia-smi` returned empty), so the corrected final workspace entry point still appears to be CPU/login context rather than the actual GPU training node.
- `/mnt/3fs/data/ai4ai/deps` is visible and includes:
  - `LLamaFactory_4fa8e1ee_20260507.tar.gz`
  - `LLamaFactory_4fa8e1ee_20260507.tar.gz.sha256`
  - `flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl`
  - `mcore_adapter`
  - `mcore_adapter-0.9.0-fixed.whl`
  - `mcore_adapter-0.9.0-py3-none-any.whl`
- `/root/workspace/{fastapi,scikit-learn,rich}` exist on the corrected machine:
  - `fastapi` at `f4cafbc`
  - `scikit-learn` at `ffc6cdc`
  - `rich` at `46cebbb`
- `/root/workspace/coding_agent_playground` is missing on the corrected machine. The SFT launch wrapper assumes the repo/scripts/configs are present wherever it is run, so this repo must be cloned or copied there before dry-run/full launch.
- Historical axrd `nodes.json` still found at `/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json` with 4 nodes, but it is not milestone-specific and should not be used as the Milestone 1 allocation without compute/PM confirmation.

### Updated Assumptions

- LLamaFactory/MCA dependency assumptions remain valid for the corrected machine because the same `/mnt/3fs/data/ai4ai/deps` artifacts are visible there.
- GPU availability is still unconfirmed. The corrected entry host does not expose GPUs; full Qwen3-8B SFT requires a GPU allocation or milestone-specific `nodes.json`.
- Before launch on the corrected machine, ensure `/root/workspace/coding_agent_playground` exists and contains PR #1 artifacts, or run from an equivalent copied repo path and set `LLAMAFACTORY_DIR`, `DATASET_JSONL`, and `OUTPUT_ROOT` explicitly.

## 2026-05-20 PM Session 3 Top-Priority SFT Planning

### Confirmation

- Received Session 3 assignment.
- Continuing Qwen3-8B SFT planning immediately; not waiting for rollout completion.
- Durable-only update rule followed: no routine `peer_send`, no `/esc`; evidence written here and own `status.md`.
- Correct final workspace remains `ssh -p 31787 root@10.100.194.40`.

### Base Model and Checkpoint Path Validation

- Axrd model registry on the corrected machine confirms `Qwen/Qwen3-8B` facts:
  - model type: `qwen3`
  - architecture: `Qwen3ForCausalLM`
  - parameter count: `8.2B`
  - native context: `32768`
  - config max positions: `40960`
  - YaRN context reference: `131072`
  - chat template: `qwen3`
  - dtype: `bfloat16`
- Local intended base path exists only as a symlink:
  - `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B -> /mnt/3fs/data/ai4ai/axis_ref/research_hub/models/qwen3-8b/snapshot`
- That symlink target is missing on the corrected machine:
  - `/mnt/3fs/data/ai4ai/axis_ref/research_hub/models/qwen3-8b/snapshot` does not exist.
  - No `config.json` is readable through `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B`.
- `/root/workspace/evalscope/base_8b_model` and `/root/workspace/evalscope/new_model` do not expose `config.json`; not valid as confirmed HF model paths.
- Historical Qwen3-8B SFT/HF artifacts are readable and validate checkpoint shape, but are not clean base checkpoints unless PM explicitly chooses warm-start:
  - `/mnt/3fs/data/ai4ai/models/ws_20260428_0325_qwen3-8b_1bench_e46e-sft`
  - `/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-final`
  - `/mnt/3fs/data/ai4ai/models/ws_20260426_0217_qwen3-8b_1bench_29a2-sft-hf`
- Historical configs checked above have `model_type=qwen3`, `architectures=["Qwen3ForCausalLM"]`, `max_position_embeddings=40960`, and `vocab_size=151936`.

### GPU Machine Options from Axrd Records

- Corrected final workspace entry host:
  - `ssh -p 31787 root@10.100.194.40`
  - hostname `lg-cmc-b7r201-k10u23-cpu-000158`
  - no `nvidia-smi`; treat as CPU/login entry point.
- Axrd records say GPU workspaces use `nodes.json` as source of truth for node count, rank, IP, user, and SSH port.
- Only historical `nodes.json` found under `/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json`; it has 4 nodes but is not Milestone 1 allocation and must not be reused without compute/PM confirmation.
- Viable launch options once compute is allocated:
  - Single-node 8-GPU H200 style: no `nodes.json` required; run from allocated GPU node after verifying `nvidia-smi`.
  - Multi-node: require current milestone `nodes.json`; use the recorded ports and ranks, keep configs/data/checkpoints on `/mnt/3fs`, and launch workers via SSH/tmux pattern from axrd `dskill_multinode_training`.
- GPU sidecar/gpu-sampler references exist in axrd, but no current Milestone 1 GPU sample path exists yet.

### LLamaFactory/MCA Assumptions

- Corrected machine has `/mnt/3fs/data/ai4ai/deps` with:
  - `LLamaFactory_4fa8e1ee_20260507.tar.gz`
  - `LLamaFactory_4fa8e1ee_20260507.tar.gz.sha256`
  - `flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl`
  - `mcore_adapter`
- LLamaFactory archive SHA-256 validated manually:
  - expected file records hash `f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e`
  - actual archive hash is `f85745450e5c929191bb122ee916edc1d15a0debb0eb46dec470791aea78347e`
  - note: the `.sha256` file names `/tmp/LLamaFactory_4fa8e1ee_20260507.tar.gz`, so `sha256sum -c` fails by path even though the hash matches.
- Axrd SFT skill requires workspace-local `code/LLamaFactory/` and `code/mcore_adapter/`; do not run directly from shared source trees.
- Required pins/guards remain:
  - install with `--break-system-packages`
  - install `trl<=0.24.0,>=0.18.0`
  - install real `mcore_adapter` from copied source, not internal mirror stub
  - install flash-attn wheel if `neat_packing=true`
  - set `USE_MCA=1`, `FORCE_TORCHRUN=1`, `DISABLE_VERSION_CHECK=1`, and `NVTE_FLASH_ATTN=1`

### Launcher Commands

Prepare repo/scripts on corrected final workspace before launch:

```bash
cd /root/workspace
git clone git@github.com:peteryang1/coding_agent_playground.git coding_agent_playground
cd coding_agent_playground
git fetch origin intern_code_dev_4/milestone1_qwen3_8b_loop
git checkout intern_code_dev_4/milestone1_qwen3_8b_loop
```

Materialize LLamaFactory/MCA in that workspace:

```bash
cd /root/workspace/coding_agent_playground
mkdir -p code
tar -xf /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz -C code/LLamaFactory --strip-components=1
rsync -a /mnt/3fs/data/ai4ai/deps/mcore_adapter/ code/mcore_adapter/
pip install --break-system-packages -e code/LLamaFactory/ --no-deps
pip install --break-system-packages peft accelerate datasets 'trl<=0.24.0,>=0.18.0'
pip install --break-system-packages /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
pip install --break-system-packages -e code/mcore_adapter/ --no-deps
python3 -c "import flash_attn, mcore_adapter; print('gpu deps ok')"
llamafactory-cli version
```

Dry-run manifest generation can run before dataset/base/GPU are ready:

```bash
DRY_RUN=1 \
RUN_ID=milestone1_qwen3_8b_sft_dryrun \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B \
DATASET_JSONL=/root/workspace/coding_agent_playground/data/sft/milestone1_coding_agent_sft.jsonl \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
bash scripts/train_qwen3_8b_sft.sh
```

Real launch template, after base path, dataset, and GPU allocation are fixed:

```bash
DRY_RUN=0 \
RUN_ID=milestone1_qwen3_8b_sft_$(date -u +%Y%m%dT%H%M%SZ) \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B \
DATASET_JSONL=/root/workspace/coding_agent_playground/data/sft/milestone1_coding_agent_sft.jsonl \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
bash scripts/train_qwen3_8b_sft.sh
```

Multi-node launch adjustment:

- Put runtime config, dataset, and output under `/mnt/3fs`.
- Parse current milestone `nodes.json` for `MASTER_ADDR`, `NNODES`, and worker SSH ports.
- Use `llamafactory-cli train <runtime_config>` on all ranks; do not call LLamaFactory launcher paths directly.

### Output Manifest and Checkpoint Layout

Proposed durable output root:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/
  runs/train/<run_id>/
    config/qwen3_8b_sft.yaml
    logs/
    metrics.json
    run_manifest.json
  training_summary/
    sft_output/<run_id>/
      checkpoint-*/
      trainer_state.json
      all_results.json
      runs/
    model -> final exported/durable HF model
    pinned_checkpoints/
    checkpoint_registry.json
```

Manifest contract from PR #1:

- script writes `runs/train/<run_id>/run_manifest.json` before launch;
- manifest records git commit, base model, dataset path/hash, runtime config path/hash, output/checkpoint dirs, MCA/NCCL env, launch command, and checkpoint retention policy;
- dataset SHA-256 is `null` until dev_3 SFT JSONL exists.

Checkpoint retention:

- `save_steps=150`, `save_total_limit=4` in current template;
- pin any evaluated intermediate checkpoint before resume if it may be reused;
- final model should be finalized under a durable models path and linked from `training_summary/model` before formal eval.

### Current Blockers

- Clean local base model path for `Qwen/Qwen3-8B` is missing: `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is a broken symlink on the corrected machine.
- Corrected entry host has no GPU (`nvidia-smi` absent); need allocated GPU node or current milestone `nodes.json`.
- `/root/workspace/coding_agent_playground` is missing on the corrected final workspace; clone/copy PR #1 artifacts before launch.
- Final SFT JSONL from dev_3 is not available yet; real launch must wait for `DATASET_JSONL`.
- If PM chooses a historical Qwen3-8B SFT/HF artifact as warm-start instead of clean base, that is a scope/experiment decision and should be recorded before using it.

## 2026-05-20 PM Session 5 SFT Smoke/GPU Path

### Confirmation

- Received Session 5 assignment.
- Did not interrupt `/root/workspace/rollouts_m1_10`; only listed its directory/process state.
- Used current cleaned SFT file `/root/workspace/cleaned_m1_sft_10/train.jsonl` for command validation.
- Durable-only update rule followed: no routine `peer_send`, no `/esc`.

### Cleaned SFT File Validation

- File exists on corrected final workspace:
  - `/root/workspace/cleaned_m1_sft_10/train.jsonl`
  - size: `34816` bytes
  - SHA-256 in generated manifest: `f91d0b096537564f136576dd7f3bb5f54750aafb524c7f890be621d557ddd0c2`
- JSONL parsed successfully:
  - rows: `10`
  - roles: `user=10`, `assistant=10`
  - first record keys: `artifacts`, `example_id`, `format_version`, `messages`, `metadata`, `repo`, `repo_path`, `source`, `task_id`, `trajectory_id`
  - first record message count: `2`
- `rejected.jsonl` exists and is `0` bytes.

### Remote Repo/Artifact Setup

- `/root/workspace/coding_agent_playground` was missing at start of Session 5.
- SSH git clone failed because GitHub host key verification failed on the corrected final workspace:
  - `Host key verification failed.`
  - `fatal: Could not read from remote repository.`
- Retried with HTTPS clone successfully:
  - cloned `https://github.com/peteryang1/coding_agent_playground.git`
  - checked out branch `intern_code_dev_4/milestone1_qwen3_8b_loop`
  - checked out commit `dc7b268`

Exact setup commands that succeeded:

```bash
ssh -p 31787 root@10.100.194.40
cd /root/workspace
git clone https://github.com/peteryang1/coding_agent_playground.git coding_agent_playground
cd coding_agent_playground
git fetch origin intern_code_dev_4/milestone1_qwen3_8b_loop
git checkout -B intern_code_dev_4/milestone1_qwen3_8b_loop origin/intern_code_dev_4/milestone1_qwen3_8b_loop
git rev-parse --short HEAD
```

### Command Validation Run

Dry-run command executed on corrected final workspace:

```bash
cd /root/workspace/coding_agent_playground
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
RUN_ID=milestone1_qwen3_8b_sft_smoke_cmd_20260520 \
DRY_RUN=1 \
bash scripts/train_qwen3_8b_sft.sh
```

Dry-run result:

- Passed; no training launched.
- Runtime config written:
  - `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/config/qwen3_8b_sft.yaml`
- Run manifest written and JSON-validated:
  - `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/run_manifest.json`
- Manifest records:
  - repo commit: `dc7b2686ec0866ddb1103956ce84ecfb073733c0`
  - base model: `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B`
  - dataset path: `/root/workspace/cleaned_m1_sft_10/train.jsonl`
  - dataset SHA-256: `f91d0b096537564f136576dd7f3bb5f54750aafb524c7f890be621d557ddd0c2`
  - output dir: `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_smoke_cmd_20260520`
  - launch command: `cd /root/workspace/coding_agent_playground/code/LLamaFactory && export PYTHONPATH="/root/workspace/coding_agent_playground/code/LLamaFactory/src:${PYTHONPATH:-}" && llamafactory-cli train /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/config/qwen3_8b_sft.yaml`

### Exact Real-Launch Preparation Commands

These commands are the current real-launch path once GPU and base model blockers are cleared:

```bash
ssh -p 31787 root@10.100.194.40
cd /root/workspace/coding_agent_playground
mkdir -p code/LLamaFactory code/mcore_adapter
tar -xf /mnt/3fs/data/ai4ai/deps/LLamaFactory_4fa8e1ee_20260507.tar.gz -C code/LLamaFactory --strip-components=1
rsync -a /mnt/3fs/data/ai4ai/deps/mcore_adapter/ code/mcore_adapter/
pip install --break-system-packages -e code/LLamaFactory/ --no-deps
pip install --break-system-packages peft accelerate datasets 'trl<=0.24.0,>=0.18.0'
pip install --break-system-packages /mnt/3fs/data/ai4ai/deps/flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl
pip install --break-system-packages -e code/mcore_adapter/ --no-deps
python3 -c "import flash_attn, mcore_adapter; print('gpu deps ok')"
llamafactory-cli version
```

Single-node real launch command after `nvidia-smi` and base model path are valid:

```bash
cd /root/workspace/coding_agent_playground
DATASET_JSONL=/root/workspace/cleaned_m1_sft_10/train.jsonl \
BASE_MODEL=/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B \
OUTPUT_ROOT=/mnt/3fs/data/ai4ai/outputs/coding_agent_playground \
LLAMAFACTORY_DIR=/root/workspace/coding_agent_playground/code/LLamaFactory \
RUN_ID=milestone1_qwen3_8b_sft_smoke_gpu_$(date -u +%Y%m%dT%H%M%SZ) \
DRY_RUN=0 \
bash scripts/train_qwen3_8b_sft.sh
```

Multi-node real launch needs a current Milestone 1 `nodes.json`; do not reuse historical axrd `nodes.json`. Once provided, use it for `MASTER_ADDR`, `NNODES`, `NODE_RANK`, and worker SSH ports, with config/dataset/output on `/mnt/3fs`.

### GPU/Machine Needs

- Need a shell on an allocated GPU node where `nvidia-smi` is available, or a current Milestone 1 `nodes.json` that points to allocated GPU nodes.
- For single-node smoke: one 8-GPU H200-style node is enough for command smoke after dependencies are installed.
- For multi-node smoke/full run: current `nodes.json` is mandatory; worker setup must install LLamaFactory, `trl<=0.24.0,>=0.18.0`, flash-attn wheel, and real `mcore_adapter` on every worker.
- Output must stay on shared `/mnt/3fs/data/ai4ai/outputs/coding_agent_playground` so checkpoints/manifests are visible across nodes and later eval.

### Session 5 Blockers

- Corrected final workspace entry host still has no `nvidia-smi`; no GPU launch attempted.
- Clean base model path is still invalid: `/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B` is a broken symlink to missing `axis_ref/.../qwen3-8b/snapshot`.
- `code/LLamaFactory` and `code/mcore_adapter` are not yet materialized in `/root/workspace/coding_agent_playground`; only dry-run command validation was executed.
- SSH clone is blocked by GitHub host key verification on the final machine; HTTPS clone worked for this setup.
- Historical `nodes.json` remains non-milestone and must not be used for this run without PM/compute confirmation.

## 2026-05-20 PM Continuation - SFT Blocker Audit

PM rechecked the corrected final workspace after the SFT dry-run:

```text
ssh -p 31787 root@10.100.194.40
hostname lg-cmc-b7r201-k10u23-cpu-000158
nvidia-smi absent
```

Current milestone-specific GPU allocation:

```text
No current Milestone 1 nodes.json found.
Only historical nodes.json found:
/mnt/3fs/data/ai4ai/outputs/ws_20260512_1931_qwen3-4b-thinking-2507_1bench_f327/nodes.json
```

Clean base path status:

```text
/mnt/3fs/data/ai4ai/models/Qwen/Qwen3-8B
  -> /mnt/3fs/data/ai4ai/axis_ref/research_hub/models/qwen3-8b/snapshot
target missing on corrected final workspace
```

Readable historical Qwen3-8B checkpoints exist, for example:

```text
/mnt/3fs/data/ai4ai/models/ws_20260428_0325_qwen3-8b_1bench_e46e-sft
/mnt/3fs/data/ai4ai/models/ws_20260425_0208_qwen3-8b_1bench_3fdf-final
/mnt/3fs/data/ai4ai/models/ws_20260426_0217_qwen3-8b_1bench_29a2-sft-hf
```

Those configs validate as `model_type=qwen3`, `architectures=["Qwen3ForCausalLM"]`, and `vocab_size=151936`, but they are historical checkpoints, not a clean Milestone 1 base. They should only be used if PM/supervisor explicitly accepts a warm-start SFT smoke.

Dry-run manifest schema was verified:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/runs/train/milestone1_qwen3_8b_sft_smoke_cmd_20260520/run_manifest.json
run_id milestone1_qwen3_8b_sft_smoke_cmd_20260520
data.train_path /root/workspace/cleaned_m1_sft_10/train.jsonl
data.train_sha256 f91d0b096537564f136576dd7f3bb5f54750aafb524c7f890be621d557ddd0c2
artifacts.checkpoint_dir /mnt/3fs/data/ai4ai/outputs/coding_agent_playground/training_summary/sft_output/milestone1_qwen3_8b_sft_smoke_cmd_20260520
commands[0] cd /root/workspace/coding_agent_playground/code/LLamaFactory && export PYTHONPATH=... && llamafactory-cli train ...
```

Conclusion: SFT smoke has a validated dataset and launch manifest, but real training remains blocked by the missing clean base path plus missing GPU allocation/current `nodes.json`.
