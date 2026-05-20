# coding_agent_playground Design

版本：v0.1  
状态：Draft  
面向读者：开发团队、研究团队、平台维护者

---

## 1. 设计目标

`coding_agent_playground` 的目标是构建一个端到端的 coding agent 后训练平台，让 LLM 能够通过可执行软件工程任务产生交互轨迹，并将这些轨迹转化为 SFT、preference tuning、RL 和 verifier training 数据。

平台要支持以下完整闭环：

```text
Task Construction
  → Agent Rollout
  → Environment Execution
  → Reward Judging
  → Episode Storage
  → Training Data Construction
  → SFT / Preference / RL
  → Held-out Evaluation
  → Failure Analysis
  → Next-round Data / Reward / Harness Improvement
```

设计上需要特别保证：

1. **环境可执行**：所有任务都必须能在 sandbox 中运行测试或验证逻辑。
2. **轨迹可回放**：每个 episode 都要保存完整上下文、工具调用、观察结果和 patch。
3. **奖励可解释**：reward 必须保留 component-level 细节，而不是只有一个 scalar。
4. **训练评估隔离**：training playground 与 evaluation arena 必须严格隔离。
5. **模型能力与系统能力分离**：固定 harness 比较模型，开放 harness 比较系统。
6. **失败分析驱动迭代**：每轮 eval 之后要输出 failure taxonomy 和改进建议。

---

## 2. 非目标

当前版本不做：

1. 从零训练 foundation model。
2. 一开始支持大规模全参数 RL。
3. 一开始追求公开 leaderboard SOTA。
4. 把复杂 agent scaffold 的提升误认为模型本身提升。
5. 在 evaluation split 上做训练、数据构造或调参。
6. 让 agent 访问 hidden tests、oracle patch、reward scripts 或 evaluation harness。

---

## 3. 总体架构

```text
                                   ┌────────────────────┐
                                   │      Player         │
                                   │   LLM / Policy      │
                                   └─────────┬──────────┘
                                             │
                                             ▼
                                   ┌────────────────────┐
                                   │      Harness        │
                                   │ tools + prompts     │
                                   └─────────┬──────────┘
                                             │
                                             ▼
┌────────────────────┐           ┌────────────────────┐           ┌────────────────────┐
│       Task          │──────────▶│     Playground      │──────────▶│      Episode       │
│ issue + repo + test │           │ executable env      │           │ full trajectory    │
└────────────────────┘           └─────────┬──────────┘           └─────────┬──────────┘
                                           │                                  │
                                           ▼                                  ▼
                                 ┌────────────────────┐           ┌────────────────────┐
                                 │       Judge         │──────────▶│      Coaches       │
                                 │ reward components   │           │ SFT / DPO / RL data│
                                 └─────────┬──────────┘           └─────────┬──────────┘
                                           │                                  │
                                           ▼                                  ▼
                                 ┌────────────────────┐           ┌────────────────────┐
                                 │       Arena         │◀──────────│      Training       │
                                 │ held-out eval       │           │ SFT / DPO / RL      │
                                 └─────────┬──────────┘           └────────────────────┘
                                           │
                                           ▼
                                 ┌────────────────────┐
                                 │      Analysis       │
                                 │ failure reports     │
                                 └────────────────────┘
```

---

## 4. 推荐目录结构

```text
coding_agent_playground/
  README.md
  DESIGN.md
  pyproject.toml
  Makefile

  docs/
    architecture.md
    data_schema.md
    experiment_guide.md
    evaluation_guide.md
    safety.md

  configs/
    model/
    harness/
    playground/
    rollout/
    reward/
    train/
    eval/
    round/

  cap/
    core/
      task.py
      episode.py
      observation.py
      tool_call.py
      patch.py
      reward.py
      registry.py
      config.py
      serialization.py

    players/
      llm_client.py
      policy.py
      decoding.py
      model_registry.py

    harnesses/
      base.py
      bash_edit_harness.py
      search_edit_test_harness.py
      planner_coder_reviewer.py
      adapters/
        swe_agent.py
        openhands.py
        mini_swe_agent.py

    playgrounds/
      base.py
      local_repo_playground.py
      docker_repo_playground.py
      swebench_playground.py
      swegym_playground.py
      synthetic_bug_playground.py

    episodes/
      store.py
      replay.py
      serializer.py
      filters.py

    rollout/
      runner.py
      scheduler.py
      sampler.py
      batch_runner.py
      worker.py

    judges/
      base.py
      patch_apply_judge.py
      unit_test_judge.py
      hidden_test_judge.py
      lint_judge.py
      typecheck_judge.py
      diff_quality_judge.py
      forbidden_edit_judge.py
      security_judge.py
      composite_judge.py

    coaches/
      to_sft.py
      to_preference.py
      to_rl.py
      to_verifier.py
      data_filter.py
      data_mixer.py
      prompt_builder.py

    train/
      sft.py
      preference.py
      rl.py
      verifier.py
      backends/
        trl_backend.py
        verl_backend.py
        axolotl_backend.py
        custom_backend.py

    arenas/
      eval_runner.py
      suites/
      metrics.py
      leaderboard.py
      compare.py

    analysis/
      failure_taxonomy.py
      failure_classifier.py
      failure_report.py
      trace_viewer.py
      reward_hacking.py
      ablation.py

    infra/
      docker/
      storage.py
      logging.py
      resource.py
      ray_runner.py
      slurm_runner.py
      cache.py

    safety/
      sandbox.py
      secret_scanner.py
      network_policy.py
      forbidden_edits.py
      audit.py

  scripts/
    play.py
    judge.py
    build_sft.py
    build_preference.py
    build_rl.py
    train_sft.py
    train_dpo.py
    train_rl.py
    eval.py
    analyze.py

  examples/
    toy_repo/
    toy_tasks/

  tests/
```

内部 package 名建议使用 `cap`，表示 `Coding Agent Playground`。

---

## 5. 核心模块职责

### 5.1 `core/`

负责定义平台中最基础、最稳定的数据结构和接口。

核心对象：

```text
Task
Observation
ToolCall
Episode
Patch
Reward
RunCard
```

要求：

1. 不依赖具体模型。
2. 不依赖具体 playground。
3. 不依赖具体训练框架。
4. 所有对象都支持 JSON / JSONL 序列化。
5. 所有 schema 都要带版本号。

---

### 5.2 `players/`

负责封装模型调用。

支持：

```text
local Hugging Face model
vLLM server
OpenAI-compatible API
SGLang server
teacher model
trained adapter model
```

核心接口：

```python
class Policy:
    def generate(self, messages: list[dict], **kwargs) -> str:
        ...

    def generate_batch(self, batch: list[list[dict]], **kwargs) -> list[str]:
        ...
```

设计原则：

1. Harness 不直接依赖某个模型后端。
2. 所有模型调用都通过 `Policy` 或 `LLMClient`。
3. token usage、latency、cost 必须记录到 episode metadata。

---

### 5.3 `harnesses/`

Harness 定义 agent 如何行动。

核心接口：

```python
class AgentHarness:
    harness_id: str

    def solve(
        self,
        task: Task,
        playground: Playground,
        policy: Policy,
    ) -> Episode:
        ...
```

典型 harness：

```text
bash_edit_harness:
  模型输出工具调用，工具包括 read_file、edit_file、run_tests、submit_patch。

search_edit_test_harness:
  增加 repo search、file localization、test loop。

planner_coder_reviewer:
  planner 负责定位，coder 负责修改，reviewer 负责检查 patch。

adapters:
  适配 SWE-agent、OpenHands、mini-SWE-agent 等外部 harness。
```

设计原则：

1. Harness 决定 prompt 和工具协议。
2. Harness 不直接计算 reward。
3. Harness 不应直接访问 hidden tests。
4. Harness 必须将所有 tool call 和 observation 写入 episode。

---

### 5.4 `playgrounds/`

Playground 是可执行环境。

核心接口：

```python
class Playground:
    playground_id: str

    def reset(self, task: Task) -> Observation:
        ...

    def read_file(self, path: str) -> str:
        ...

    def write_file(self, path: str, content: str) -> None:
        ...

    def run_command(self, command: str, timeout: int | None = None) -> Observation:
        ...

    def run_tests(self, tests: list[str], hidden: bool = False) -> Observation:
        ...

    def apply_patch(self, patch: str) -> Observation:
        ...

    def get_diff(self) -> str:
        ...

    def close(self) -> None:
        ...
```

Playground 类型：

```text
LocalRepoPlayground:
  用于 toy repo、本地开发和快速调试。

DockerRepoPlayground:
  用 Docker 隔离环境执行任务。

SWEBenchPlayground:
  适配 SWE-bench 风格任务。

SWEGymPlayground:
  适配 SWE-Gym 风格任务。

SyntheticBugPlayground:
  用于合成 bug、mutation task 和 curriculum task。
```

设计原则：

1. Playground 负责环境执行，不负责模型推理。
2. Playground 必须支持 reset，保证任务可复现。
3. 所有命令执行必须有 timeout。
4. 默认禁用网络。
5. 必须限制 CPU、内存、磁盘和 wall time。
6. hidden tests 只能被 Judge 或 Arena 调用，不能暴露给 Harness。

---

### 5.5 `episodes/`

负责 episode 的存储、回放、过滤和索引。

Episode store 需要保存：

```text
episodes.jsonl
rewards.jsonl
tool_calls.jsonl
patches/
logs/
metrics.json
run_card.json
```

核心接口：

```python
class EpisodeStore:
    def append(self, episode: Episode) -> None:
        ...

    def load(self, episode_id: str) -> Episode:
        ...

    def iter(self, filters: dict | None = None) -> Iterator[Episode]:
        ...

    def replay(self, episode_id: str) -> None:
        ...
```

设计原则：

1. Episode 是训练数据的来源，不能丢失关键上下文。
2. 所有 episode 必须能追溯到 task、model、harness、playground、config 和 code commit。
3. Episode replay 不要求重新调用模型，但要能展示当时每一步发生了什么。

---

### 5.6 `judges/`

Judge 对 patch 或 episode 打分。

核心接口：

```python
class Judge:
    judge_id: str

    def judge(self, task: Task, episode: Episode, playground: Playground) -> dict:
        ...
```

Judge 类型：

```text
PatchApplyJudge
UnitTestJudge
HiddenTestJudge
LintJudge
TypecheckJudge
DiffQualityJudge
ForbiddenEditJudge
SecurityJudge
CompositeJudge
```

Composite reward 示例：

```python
final_reward = (
    0.10 * patch_applies
  + 0.30 * public_tests_pass
  + 0.35 * hidden_tests_pass
  + 0.10 * no_regression
  + 0.05 * lint_pass
  + 0.05 * diff_minimality
  - 0.50 * forbidden_edit
  - 0.20 * timeout_penalty
)
```

设计原则：

1. Judge 返回 reward vector。
2. RL 使用 `final_scalar`，分析使用所有 components。
3. Judge 必须记录判断依据，例如测试命令、exit code、stdout/stderr 摘要。
4. Evaluation judge 可以使用 hidden tests，但不能把 hidden test 内容写入 episode messages。

---

### 5.7 `coaches/`

Coach 把 episode 转换为训练数据。

支持四类数据：

```text
SFT data
Preference data
RL rollout data
Verifier data
```

#### SFT 数据类型

```text
patch-only SFT:
  prompt → final patch

trajectory SFT:
  observation → next tool call

debugging SFT:
  issue + failed patch + test log → corrected patch
```

#### Preference 数据

同一 task 下，根据多个 episode 构造 chosen / rejected pair：

```text
chosen:
  hidden tests pass + no regression + minimal diff

rejected:
  tests fail / modifies forbidden files / over-edits / reward hacks
```

#### RL 数据

用于 RLVR / GRPO / PPO：

```text
prompt
rollout trajectory
reward vector
final scalar reward
metadata
```

设计原则：

1. Coach 只能使用 training split 的 episode。
2. Coach 不能使用 evaluation hidden test 内容生成训练样本。
3. 数据输出必须包含 data manifest 和 provenance。
4. 数据需要支持去重、过滤、污染检查和质量分层。

---

### 5.8 `train/`

训练模块负责调用具体后训练框架。

支持：

```text
SFT
DPO / IPO / KTO / ORPO / SimPO
RLVR / GRPO / PPO / RLOO
Verifier training
Distillation
```

后端适配：

```text
TRL
verl
Axolotl
custom lightweight trainer
```

设计原则：

1. 平台不重复造完整训练框架，而是提供 adapter。
2. 训练配置必须保存到 run dir。
3. 训练数据必须带 hash 和 manifest。
4. checkpoint 必须记录 base model、adapter、data version 和 trainer version。

---

### 5.9 `arenas/`

Arena 负责严肃评估。

核心接口：

```python
class Arena:
    def evaluate(
        self,
        model: Policy,
        harness: AgentHarness,
        tasks: list[Task],
    ) -> EvalResult:
        ...
```

评估指标：

```text
resolve_rate
patch_apply_rate
public_test_pass_rate
hidden_test_pass_rate
regression_rate
forbidden_edit_rate
avg_steps
avg_tokens
avg_wall_time
avg_cost
avg_files_modified
avg_loc_changed
timeout_rate
failure_type_distribution
```

设计原则：

1. Arena 不允许暴露 oracle patch。
2. Arena 不允许暴露 hidden tests 给 harness。
3. Arena 的 task split 必须和 training split 隔离。
4. 每次 eval 必须输出 eval card、metrics 和 failure report。

---

### 5.10 `analysis/`

分析模块负责失败归类、报告生成、ablation 和 reward hacking 检测。

Failure taxonomy：

```text
problem_understanding_failure
file_localization_failure
context_understanding_failure
wrong_api_usage
test_misinterpretation
patch_format_error
patch_does_not_apply
public_tests_failed
public_pass_hidden_fail
regression_introduced
over_editing
under_editing
timeout
tool_misuse
hallucinated_file
hallucinated_dependency
forbidden_test_modification
reward_hacking
environment_error
flaky_test
```

Failure → Action mapping：

```text
file_localization_failure
  → add file localization SFT data
  → improve repo search tool
  → add retrieval traces

patch_format_error
  → add patch formatting SFT
  → strengthen submit_patch parser
  → add format reward

public_pass_hidden_fail
  → train verifier
  → add mutation tests
  → generate edge-case debugging data

over_editing
  → add minimal-diff DPO pairs
  → add diff-size penalty

tool_misuse
  → add tool-use trajectory SFT
  → refine harness prompt

timeout
  → add cost-aware reward
  → constrain search space
  → improve planning

reward_hacking
  → strengthen forbidden edit policy
  → add negative preference examples
  → add sandbox audit
```

---

## 6. 核心数据结构

### 6.1 Task

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class Task:
    schema_version: str
    task_id: str
    source: str
    split: str

    repo_url: str | None
    repo_path: str | None
    base_commit: str | None

    problem_statement: str

    public_tests: list[str]
    hidden_tests: list[str]

    allowed_files: list[str] | None
    forbidden_files: list[str]

    oracle_patch: str | None
    metadata: dict[str, Any]
```

Required invariants：

1. `task_id` 全局唯一。
2. `split` 必须是 `train`、`val`、`test`、`private` 之一。
3. Eval split 中 `oracle_patch` 不应暴露给 harness。
4. `hidden_tests` 只能被 Judge / Arena 使用。

---

### 6.2 Observation

```python
@dataclass
class Observation:
    schema_version: str
    step_id: int
    tool_name: str
    command: str | None
    stdout: str
    stderr: str
    exit_code: int | None
    duration_seconds: float
    metadata: dict[str, Any]
```

---

### 6.3 ToolCall

```python
@dataclass
class ToolCall:
    schema_version: str
    step_id: int
    tool_name: str
    arguments: dict[str, Any]
    raw_model_output: str
    parsed_ok: bool
    metadata: dict[str, Any]
```

---

### 6.4 Episode

```python
@dataclass
class Episode:
    schema_version: str
    episode_id: str
    task_id: str

    model_id: str
    model_version: str | None
    harness_id: str
    playground_id: str

    messages: list[dict]
    tool_calls: list[ToolCall]
    observations: list[Observation]

    intermediate_patches: list[str]
    final_patch: str | None

    reward: dict[str, float]
    resolved: bool
    failure_type: str | None

    token_usage: dict[str, int]
    wall_time_seconds: float
    metadata: dict[str, Any]
```

Required invariants：

1. `episode_id` 全局唯一。
2. `task_id` 必须能追溯到 Task。
3. `tool_calls[i]` 和 `observations[i]` 应尽可能一一对应。
4. `final_patch` 必须可保存为独立 patch 文件。
5. `reward` 必须包含 `final_scalar` 字段。

---

### 6.5 Reward

Reward vector 示例：

```json
{
  "patch_applies": 1.0,
  "public_tests_pass": 1.0,
  "hidden_tests_pass": 0.0,
  "no_regression": 1.0,
  "lint_pass": 1.0,
  "typecheck_pass": 0.0,
  "diff_minimality": 0.75,
  "forbidden_edit": 0.0,
  "security_ok": 1.0,
  "timeout_penalty": 0.0,
  "final_scalar": 0.62
}
```

---

## 7. Workflow 设计

### 7.1 Play Workflow

```text
load config
load tasks
load model policy
load harness
for task in tasks:
    playground.reset(task)
    episode = harness.solve(task, playground, policy)
    reward = judge.judge(task, episode, playground)
    episode.reward = reward
    episode_store.append(episode)
write run_card
write metrics
```

CLI：

```bash
cap play --config configs/round/mvp_play.yaml
```

---

### 7.2 SFT Workflow

```text
load episodes
filter successful / high-quality episodes
convert to SFT format
write data manifest
train LoRA / full model
save checkpoint
run held-out eval
```

CLI：

```bash
cap build-sft \
  --episodes runs/play/mvp_round_001/episodes \
  --out data/sft/mvp_round_001.jsonl

cap train-sft --config configs/train/mvp_sft.yaml
```

---

### 7.3 Preference Workflow

```text
load episodes grouped by task_id
rank episodes by reward vector and quality heuristics
construct chosen/rejected pairs
filter noisy pairs
train DPO / preference method
run held-out eval
```

CLI：

```bash
cap build-preference \
  --episodes runs/play/round_001/episodes \
  --out data/preference/round_001.jsonl

cap train-dpo --config configs/train/dpo_round_001.yaml
```

---

### 7.4 RL Workflow

```text
load train tasks
for each RL step:
    sample batch of tasks
    rollout K episodes per task
    compute reward with executable judge
    update model with RL backend
periodically eval on held-out arena
save checkpoint and metrics
```

CLI：

```bash
cap train-rl --config configs/train/rl_debugging_round_001.yaml
```

Recommended progression：

```text
Debugging RL
  → Single-file Repair RL
  → Full Repo-level RL
```

---

### 7.5 Evaluation Workflow

```text
load held-out tasks
load fixed harness
load model policy
run episodes
compute metrics
classify failures
write eval_card
write failure_report
```

CLI：

```bash
cap eval --config configs/eval/mvp_eval.yaml
cap analyze --run runs/eval/mvp_after_sft
```

---

## 8. Config 设计

### 8.1 Round Config

```yaml
round_name: mvp_qwen_coder_play_round_001

model:
  model_id: Qwen/Qwen2.5-Coder-7B-Instruct
  backend: vllm
  adapter: null
  temperature: 0.7
  top_p: 0.95
  max_new_tokens: 4096

playground:
  type: local_repo
  sandbox: docker
  network: disabled
  timeout_seconds: 900

harness:
  type: bash_edit
  max_steps: 30
  tools:
    - read_file
    - search_repo
    - edit_file
    - run_tests
    - get_diff
    - submit_patch

tasks:
  source: toy_repo
  split: train
  path: data/tasks/toy_train.jsonl
  limit: 100

rollout:
  samples_per_task: 4
  parallelism: 8

reward:
  type: composite
  components:
    patch_applies: 0.1
    public_tests_pass: 0.4
    hidden_tests_pass: 0.3
    no_regression: 0.1
    diff_minimality: 0.1

output:
  run_dir: runs/play/mvp_round_001
  save_episodes: true
  save_tool_logs: true
  save_patches: true
```

---

### 8.2 SFT Config

```yaml
run_name: sft_mvp_round_001

base_model: Qwen/Qwen2.5-Coder-7B-Instruct

data:
  train_path: data/sft/mvp_round_001_train.jsonl
  val_path: data/sft/mvp_round_001_val.jsonl
  format: chat

training:
  method: lora
  backend: trl
  max_seq_len: 16384
  learning_rate: 0.00002
  batch_size: 1
  gradient_accumulation_steps: 16
  num_epochs: 2
  warmup_ratio: 0.03

lora:
  r: 64
  alpha: 128
  dropout: 0.05
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - up_proj
    - down_proj
    - gate_proj

output:
  output_dir: checkpoints/sft_mvp_round_001
  save_steps: 500
  eval_steps: 500
```

---

### 8.3 Eval Config

```yaml
eval_name: mvp_eval_after_sft

model:
  base_model: Qwen/Qwen2.5-Coder-7B-Instruct
  adapter: checkpoints/sft_mvp_round_001
  backend: vllm
  temperature: 0.2
  top_p: 0.95
  max_new_tokens: 4096

arena:
  type: local_repo
  task_path: data/tasks/toy_holdout.jsonl
  hidden_tests_enabled: true
  oracle_patch_visible: false

harness:
  type: bash_edit
  max_steps: 30
  tools:
    - read_file
    - search_repo
    - edit_file
    - run_tests
    - get_diff
    - submit_patch

metrics:
  - resolve_rate
  - patch_apply_rate
  - public_test_pass_rate
  - hidden_test_pass_rate
  - regression_rate
  - avg_steps
  - avg_tokens
  - avg_wall_time
  - failure_type_distribution

output:
  run_dir: runs/eval/mvp_after_sft
```

---

## 9. Run Artifact 设计

每次 play、train、eval 都要保存可复现实验记录。

### 9.1 Play Run

```text
runs/play/round_001/
  config.yaml
  run_card.json
  episodes.jsonl
  rewards.jsonl
  tool_calls.jsonl
  metrics.json
  patches/
    episode_001.patch
    episode_002.patch
  logs/
    episode_001.log
    episode_002.log
```

### 9.2 Train Run

```text
runs/train/sft_round_001/
  config.yaml
  train_card.json
  data_manifest.json
  metrics.json
  checkpoints/
```

### 9.3 Eval Run

```text
runs/eval/eval_round_001/
  config.yaml
  eval_card.json
  predictions.jsonl
  patches/
  metrics.json
  failure_report.md
  representative_failures/
```

---

## 10. Run Card Schema

```json
{
  "run_id": "round_001_qwen7b_toy_sft",
  "run_type": "play",
  "created_at": "2026-05-20T00:00:00Z",
  "git_commit": "...",
  "base_model": "Qwen/Qwen2.5-Coder-7B-Instruct",
  "trained_model": null,
  "harness": "bash_edit_v1",
  "playground": "toy_repo_train",
  "task_split": "train",
  "num_tasks": 100,
  "samples_per_task": 4,
  "num_episodes": 400,
  "resolved_episodes": 92,
  "reward_version": "composite_v1",
  "metrics": {
    "resolve_rate": 0.23,
    "patch_apply_rate": 0.81,
    "avg_steps": 18.4
  },
  "artifacts": {
    "episodes": "episodes.jsonl",
    "rewards": "rewards.jsonl",
    "patches": "patches/"
  }
}
```

---

## 11. Evaluation 设计细节

### 11.1 Model Leaderboard

用于比较模型本身。

固定：

```text
same harness
same tools
same context budget
same decoding config
same retry count
same verifier setting
same eval task split
```

只更换：

```text
model checkpoint / adapter
```

输出示例：

```text
Base model resolve rate: 12.4%
SFT model resolve rate: 16.8%
Delta: +4.4%
```

---

### 11.2 System Leaderboard

用于比较完整 agent system。

允许变化：

```text
harness
retrieval
verifier
best-of-N
multi-agent workflow
test-time scaling
planning strategy
```

必须额外报告成本：

```text
avg tokens per resolved task
avg wall time per resolved task
avg tool calls per task
avg samples per task
```

---

## 12. Data Governance

### 12.1 Data Manifest

所有训练数据必须保存 manifest：

```json
{
  "data_id": "sft_round_001",
  "created_at": "2026-05-20T00:00:00Z",
  "source_runs": ["runs/play/round_001"],
  "num_examples": 1234,
  "format": "chat",
  "filters": ["resolved_only", "no_forbidden_edit", "max_diff_500_lines"],
  "task_splits": ["train"],
  "hash": "...",
  "contamination_policy": "strict"
}
```

### 12.2 Contamination Rules

禁止：

```text
train examples from eval tasks
oracle patches from eval split
hidden test content in training data
evaluation harness code in model prompt
benchmark answer leakage
```

建议检查：

```text
task_id overlap
repo + commit overlap
issue text overlap
patch overlap
embedding similarity
file path and line overlap
```

---

## 13. Safety / Sandbox 设计

### 13.1 默认策略

```text
network disabled by default
CPU limit
memory limit
disk limit
wall-time timeout
filesystem isolation
no host credential mount
no host write except artifact dir
```

### 13.2 Forbidden Edits

默认禁止修改：

```text
hidden tests
evaluation harness
task metadata
reward scripts
sandbox config
.git directory
```

### 13.3 Secret Scanning

扫描对象：

```text
model output
patches
logs
episode messages
stdout / stderr
```

风险类型：

```text
API keys
access tokens
passwords
private keys
cloud credentials
```

### 13.4 Audit Log

所有危险操作必须写入 audit log：

```text
network access attempt
forbidden file write
large file deletion
hidden test access attempt
credential-like string generation
```

---

## 14. MVP 实现计划

### Phase 0：Project Skeleton

交付：

```text
pyproject.toml
README.md
DESIGN.md
cap/core/*
tests/core/*
```

完成标准：

```text
核心 dataclass 可以序列化 / 反序列化
pytest 可以运行
config loader 可用
```

---

### Phase 1：Toy Playground

交付：

```text
examples/toy_repo/
data/tasks/toy_train.jsonl
data/tasks/toy_holdout.jsonl
cap/playgrounds/local_repo_playground.py
```

完成标准：

```text
可以 reset repo
可以 read / write file
可以 run tests
可以 get diff
可以手动提交 patch 并得到 reward
```

---

### Phase 2：Bash Edit Harness

交付：

```text
cap/harnesses/bash_edit_harness.py
cap/players/llm_client.py
cap/rollout/runner.py
scripts/play.py
```

完成标准：

```text
一个模型可以在 toy task 上生成 episode
episode 包含 tool calls、observations、final patch、reward
```

---

### Phase 3：Judge + Episode Store

交付：

```text
cap/judges/*
cap/episodes/store.py
```

完成标准：

```text
episodes.jsonl
rewards.jsonl
patches/
logs/
metrics.json
run_card.json
```

---

### Phase 4：SFT Data Builder

交付：

```text
cap/coaches/to_sft.py
scripts/build_sft.py
```

完成标准：

```text
成功 episode 可以转换成 chat-format SFT 数据
生成 data_manifest.json
```

---

### Phase 5：SFT Trainer

交付：

```text
cap/train/sft.py
scripts/train_sft.py
configs/train/mvp_sft.yaml
```

完成标准：

```text
可以训练 LoRA adapter
可以保存 checkpoint
可以加载 adapter 做 inference
```

---

### Phase 6：Held-out Evaluation

交付：

```text
cap/arenas/eval_runner.py
cap/arenas/metrics.py
scripts/eval.py
```

完成标准：

```text
base model eval
SFT model eval
before / after metrics
```

---

### Phase 7：Failure Analysis

交付：

```text
cap/analysis/failure_taxonomy.py
cap/analysis/failure_report.py
scripts/analyze.py
```

完成标准：

```text
输出 failure_report.md
按失败类型聚类
展示代表性失败样本
给出下一轮数据 / reward / harness 建议
```

---

## 15. 工程规范

### 15.1 Python 规范

建议：

```text
Python >= 3.10
type hints required
ruff for lint / format
pytest for testing
pydantic or dataclass for schemas
```

### 15.2 依赖方向

```text
core should not depend on other cap modules
playgrounds should not depend on harnesses
harnesses should not depend on train
judges should not depend on train
coaches may depend on core / episodes / judges
train may depend on coaches
arenas may depend on playgrounds / harnesses / judges
analysis may depend on episodes / arenas / judges
```

### 15.3 配置原则

所有实验参数必须来自 config，不能 hardcode：

```text
model id
adapter path
task split
harness type
max steps
temperature
reward weights
train hyperparameters
eval metrics
sandbox policy
```

---

## 16. Testing Strategy

### 16.1 Unit Tests

覆盖：

```text
schema serialization
reward computation
patch parsing
forbidden edit detection
SFT data conversion
preference pair construction
failure taxonomy rules
```

### 16.2 Integration Tests

覆盖：

```text
toy task play
toy task judge
episode save / load
SFT data build
eval metrics computation
```

### 16.3 Regression Tests

每次改动后需要验证：

```text
same task + same mock model → same episode structure
same patch → same reward
same eval output → same metrics
```

---

## 17. Definition of Done

一个功能合入前必须满足：

```text
1. 有清晰 config。
2. 有单元测试或集成测试。
3. 有日志输出。
4. 有错误处理。
5. 能保存可复现 artifacts。
6. 不污染 eval split。
7. 不破坏 sandbox policy。
8. 文档中有使用示例。
```

---

## 18. 风险与防坑

### 18.1 Harness 提升被误认为模型提升

解决：

```text
固定 harness 做 Model Leaderboard
开放 harness 做 System Leaderboard
所有报告必须标注 harness version
```

### 18.2 Reward Hacking

风险：

```text
修改测试
删除功能
hardcode expected output
修改 eval harness
利用环境漏洞
```

解决：

```text
forbidden edit judge
hidden tests
pass-to-pass regression tests
sandbox audit
diff quality judge
negative preference examples
```

### 18.3 Eval Contamination

解决：

```text
split-level isolation
task_id overlap check
repo / commit overlap check
patch similarity check
hidden test access audit
data manifest provenance
```

### 18.4 RL 成本过高或不稳定

解决：

```text
先做 debugging RL
再做 single-file repair RL
最后做 full repo-level RL
保留 SFT / DPO fallback
使用 reward components 做 ablation
```

---

## 19. 后续扩展方向

```text
SWE-bench Lite integration
SWE-Gym integration
synthetic bug generator
mutation-test generation
verifier training
best-of-N patch selection
multi-language tasks
frontend visual bug tasks
CI / DevOps repair tasks
security patch tasks
performance optimization tasks
long-horizon feature development tasks
```

---

## 20. 总结

`coding_agent_playground` 的核心不是单独的 agent harness，也不是单独的训练框架，而是一个后训练闭环系统：

```text
让模型在可执行 coding task 中 play，
让环境和测试给出反馈，
让 episode 成为训练数据，
让 SFT / preference / RL 提升模型，
让 held-out arena 验证提升，
让 failure analysis 驱动下一轮迭代。
```

第一版工程优先级：

```text
Task / Episode / Reward schema
LocalRepoPlayground
BashEditHarness
EpisodeStore
CompositeJudge
Play CLI
SFT data builder
SFT trainer
Eval CLI
Failure report
```

当 MVP 闭环跑通之后，再逐步扩展到：

```text
DPO
RLVR / GRPO
Verifier
SWE-bench / SWE-Gym
Synthetic task generation
System leaderboard
Long-horizon coding agents
```
