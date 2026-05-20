# coding_agent_playground

`coding_agent_playground` 是一个面向 **Coding Agent 后训练** 的闭环实验平台。

它让 LLM 接入 coding agent harness，在可执行的软件工程任务中读代码、改代码、跑测试、看反馈，并将完整交互过程转化为 SFT、偏好优化和 RL 训练数据。目标是让模型通过真实环境中的反复试错，逐步成长为更强的 coding agent。

> The environment is the teacher.  
> The test suite is the reward.  
> The trajectory is the dataset.  
> The failure report drives the next round.

中文表达：

> 环境是老师。  
> 测试是奖励。  
> 轨迹是数据。  
> 失败分析驱动下一轮训练。

---

## 这个平台解决什么问题？

传统 coding LLM 后训练通常依赖静态代码数据，例如函数补全、题解、commit diff 或问答数据。但真正的软件工程任务并不是一次性输出代码，而是一个交互式过程：

1. 理解 issue 或需求。
2. 搜索 repo。
3. 阅读相关文件。
4. 修改代码。
5. 运行测试。
6. 查看失败日志。
7. 继续修复。
8. 生成最终 patch。

`coding_agent_playground` 的目标是把这个过程系统化：让模型在真实或合成的软件工程任务中“play”，收集它的行为轨迹和环境反馈，再把这些反馈转化为后训练信号。

核心闭环：

```text
play → judge → learn → eval → analyze → evolve
```

具体来说：

```text
Base LLM
  → Agent Harness
  → Executable Coding Playground
  → Episodes / Trajectories / Rewards
  → SFT / Preference Tuning / RL
  → Stronger Coding Agent
  → Harder Playground Levels
  → Next Round
```

---

## 核心能力

### 1. Play：让模型进入 coding playground

模型可以通过 agent harness 使用工具：

```text
read_file
search_repo
edit_file
run_tests
run_command
get_diff
submit_patch
```

每个任务都在可执行环境中运行，通常包括：

```text
repo checkout
sandbox setup
test execution
patch collection
reward computation
```

---

### 2. Judge：用测试和规则给 episode 打分

平台会对模型生成的 patch 和完整 episode 进行评分。

Reward 不只是一个标量，而是一组可解释的 reward components：

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
  "final_scalar": 0.62
}
```

这样做的好处是：既能给 RL 一个 scalar reward，也能让开发者分析模型到底强在哪里、弱在哪里。

---

### 3. Learn：把 episode 转化为训练数据

平台支持从 agent episode 中构造多种后训练数据。

#### SFT 数据

从成功轨迹中学习：

```text
issue + repo context → final patch
observation → next tool action
failed patch + test log → corrected patch
```

#### Preference 数据

从同一任务的多个 episode 中构造 chosen / rejected pair：

```text
chosen: tests pass + minimal diff + no regression
rejected: tests fail / modifies tests / over-edits / hacks reward
```

#### RL 信号

使用可执行环境反馈进行 RLVR / GRPO / PPO 等强化学习：

```text
task → rollout → run tests → compute reward → update model
```

---

### 4. Eval：区分模型能力和系统能力

平台区分两种评估视角。

#### Model Leaderboard

固定 harness、工具、上下文预算、decode 参数和 retry 次数，只比较模型本身：

```text
base model + fixed harness
SFT model + same fixed harness
RL model + same fixed harness
```

用于回答：

> 后训练是否真的让模型本身变强？

#### System Leaderboard

允许改变 harness、retrieval、verifier、best-of-N、多 agent workflow 等系统组件：

```text
model + harness + verifier + best-of-N + retrieval
```

用于回答：

> 完整 coding agent system 是否更强？

---

### 5. Analyze：从失败中生成下一轮训练策略

每次评估后，平台会对失败样本进行归类：

```text
file_localization_failure
context_understanding_failure
wrong_api_usage
test_misinterpretation
patch_format_error
patch_does_not_apply
public_pass_hidden_fail
regression_introduced
over_editing
timeout
tool_misuse
hallucinated_file
reward_hacking
forbidden_test_modification
environment_error
```

失败分析会映射到下一轮改进动作：

```text
file_localization_failure → 增加 file localization SFT 数据
public_pass_hidden_fail → 训练 verifier，加入 mutation tests
over_editing → 构造 minimal-diff preference pairs
patch_format_error → 增加 patch formatting SFT
tool_misuse → 增加 tool-use trajectory SFT
timeout → 加入 cost-aware reward
reward_hacking → 加强 sandbox policy 和 negative examples
```

---

## 项目适合谁？

`coding_agent_playground` 适合以下使用者：

- 想研究 coding LLM 后训练的研究员。
- 想构建 coding agent eval / training pipeline 的工程团队。
- 想比较 SFT、DPO、RLVR 对 repo-level coding 能力影响的人。
- 想构建 SWE-bench / SWE-Gym / synthetic repo tasks 训练闭环的人。
- 想分析 coding agent failure modes 并自动生成下一轮训练数据的人。

---

## 推荐使用场景

### 场景 1：验证 SFT 是否提升 coding agent 能力

```bash
cap play --config configs/round/mvp_play.yaml
cap build-sft --episodes runs/play/mvp_round_001/episodes --out data/sft/mvp.jsonl
cap train-sft --config configs/train/mvp_sft.yaml
cap eval --config configs/eval/mvp_eval.yaml
cap analyze --run runs/eval/mvp_after_sft
```

目标：比较 base model 和 SFT model 在同一个 harness 下的表现。

---

### 场景 2：从多次 rollout 中构造 preference 数据

```bash
cap play --config configs/round/preference_play.yaml
cap build-preference --episodes runs/play/preference_round/episodes --out data/preference/round_001.jsonl
cap train-dpo --config configs/train/dpo_round_001.yaml
cap eval --config configs/eval/dpo_eval.yaml
```

目标：让模型偏好更小、更稳定、更符合软件工程习惯的 patch。

---

### 场景 3：用测试反馈做 RL

```bash
cap train-rl --config configs/train/rl_debugging_round_001.yaml
cap eval --config configs/eval/rl_eval.yaml
```

目标：让模型通过环境反馈学习调试、修复和验证代码。

---

## 核心概念

### Task / Level

一个 coding task，也可以理解为 playground 中的一个 level。它包含：

```text
repo
base commit
problem statement
public tests
hidden tests
allowed files
forbidden files
metadata
```

---

### Playground

可执行环境，负责：

```text
reset repo
read files
write files
run commands
run tests
collect diff
apply patch
```

---

### Harness

agent 的行动方式。它决定模型能使用哪些工具、如何组织 prompt、如何进行多步交互。

常见 harness：

```text
bash_edit_harness
search_edit_test_harness
planner_coder_reviewer_harness
swe_agent_adapter
openhands_adapter
mini_swe_agent_adapter
```

---

### Episode

模型完成一个 task 的完整交互记录。

包括：

```text
messages
tool calls
observations
file edits
test logs
intermediate patches
final patch
reward
failure type
token usage
wall time
```

Episode 是整个系统最重要的数据资产。

---

### Judge

对 episode 或 patch 进行评分的模块。

Judge 可以基于：

```text
patch apply
unit tests
hidden tests
lint
typecheck
diff quality
forbidden edit
security scan
```

---

### Coach

把 episode 转成训练数据的模块。

支持：

```text
SFT data
preference data
RL rollout data
verifier data
failure-driven data
```

---

### Arena

严肃评估环境。它与 training playground 隔离，用来进行 held-out evaluation。

Arena 中不允许：

```text
暴露 hidden tests
暴露 oracle patch
使用训练集中出现过的 task
在 eval 数据上调参
修改 evaluation harness
```

---

## 推荐目录结构

```text
coding_agent_playground/
  README.md
  DESIGN.md
  pyproject.toml
  configs/
  cap/
    core/
    players/
    harnesses/
    playgrounds/
    episodes/
    rollout/
    judges/
    coaches/
    train/
    arenas/
    analysis/
    infra/
    safety/
  scripts/
  examples/
  tests/
```

其中 `cap` 是 `Coding Agent Playground` 的缩写。

---

## 项目状态

当前目标是先完成 MVP 闭环：

```text
local toy repo task
→ agent play
→ episode collection
→ reward judging
→ SFT data construction
→ LoRA training
→ held-out evaluation
→ failure report
```

MVP 不追求 SOTA，目标是让完整闭环可运行、可复现、可分析。

---

## Roadmap

### Phase 0：Project Skeleton

- 定义 Task / Episode / Observation / Reward schema。
- 建立 config、logging、serialization 基础设施。
- 支持单元测试。

### Phase 1：Playable MVP

- 支持 local repo playground。
- 支持 bash edit harness。
- 支持基本工具调用。
- 支持 episode store。

### Phase 2：SFT Loop

- 从成功 episode 构造 SFT 数据。
- 支持 LoRA / SFT 训练。
- 支持 before / after 评估。

### Phase 3：Preference Loop

- 支持多 episode 采样。
- 构造 chosen / rejected pair。
- 支持 DPO 或其他 preference optimization。

### Phase 4：RL Loop

- 支持 debugging RL。
- 支持 executable reward。
- 支持小规模 RLVR / GRPO。

### Phase 5：Repo-level Benchmarks

- 接入 SWE-bench Lite / SWE-Gym 风格任务。
- 支持 Docker sandbox。
- 支持 batch rollout 和标准 eval report。

### Phase 6：Synthetic Data Engine

- 支持 synthetic bug injection。
- 支持 PR revert tasks。
- 支持 mutation tests。
- 支持 failure-driven task generation。

---

## Safety

因为 coding agent 会执行命令，平台默认采用 sandbox policy：

```text
network disabled by default
CPU / memory / disk limits
wall-time timeout
filesystem isolation
forbidden host writes
secret scanning
forbidden edit policy
```

默认禁止模型修改：

```text
hidden tests
evaluation harness
task metadata
reward scripts
sandbox config
.git directory
```

---

## 一句话总结

`coding_agent_playground` 是一个 coding agent 后训练平台：让 LLM 在可执行的软件工程任务中通过 agent harness 反复试错，利用测试反馈和交互轨迹进行 SFT、偏好优化和 RL，从而成长为更强的 coding agent。
