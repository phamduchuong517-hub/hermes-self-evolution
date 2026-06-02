# 🧬 Self Improvement Core v7.0 AI 助手自我进化核心（在线精简版）
> name: self-improvement-core
> description: AI 助手自我进化核心 v7.0 — 在线层只做三件事：读 SELF-EVOLUTION.md 规则表、按规则执行、写 WAL 记录问题。所有分析层（WAL分析/置信度评分/记忆压缩/知识图谱）迁移至离线 cron 异步执行。核心框架来自 Hermes 验证过的单文件进化路线。
> version: 7.0.0

## 架构总览

```
┌────── 在线层（每轮对话）──────┐
│                              │
│  ① 读 SELF-EVOLUTION.md     │ ← 行为规则表
│  ② 按规则框架执行            │ ← 三列式：触发→禁忌→正确
│  ③ 发现问题时写 WAL          │ ← 最小化记录
│                              │
└────── 离线层（cron 异步）─────┘
│  WAL分析 → 模式识别           │
│  置信度评分 → 规则有效性评估    │
│  记忆压缩 → TTL归档           │
└─────────────────────────────┘
```

## 在线层（每轮对话执行）

### ① 加载 SELF-EVOLUTION.md

在每轮对话开始时，读取 `workspace/SELF-EVOLUTION.md` 中的活动规则表。

规则表有四列：
```
| 触发场景 | 禁忌行为 | 正确行为 | 版本 |
```

命中触发场景 → 跳过禁忌行为 → 执行正确行为。

### ② 按规则执行

每轮对话的输出必须满足当前 SELF-EVOLUTION.md 中的所有活动规则。规则冲突时优先级：
1. 最新添加的规则优先
2. 用户当面指出的指令优先于离线规则
3. 场景隔离标签（编码/写作/分析）决定风格规则是否激活

### ③ 写 WAL（最小化问题记录）

当以下情况发生时，追加写一条 WAL 记录：
- 发现自己回答中存在逻辑矛盾
- 用户指出的 Bug/错误确认属实
- 用户给出明确的行为修正指令
- 连续两次犯同类型错误

WAL 记录格式（写入 `workspace/memory/wal.log`）：
```
[2026-05-30 17:49] | 问题: 混淆了A和B的因果关系 | 触发源: 用户指正 | 规则建议: 输出前先检查因果方向
一行写完，不展开，不写代码块。
```

### 在线层禁止的行为
- ❌ 运行 Confidence Scoring（离线）
- ❌ 运行知识图谱推理（离线）
- ❌ 运行 MoA 多模型聚合（离线）
- ❌ 运行海马体压缩（离线）
- ❌ 运行 8 技能记忆架构中的非必要步骤（离线）
- ❌ 任何超过 3 行的问题分析（留到离线做）

### ④ 技能结晶化机制（v7.1 新增）⭐

**来源**：GenericAgent 的 Skill Crystallization 机制
**触发条件**：复杂任务完成后（≥10分钟执行/多步骤/首次遇到该类问题）
**目的**：从任务经验中自动提取可复用技能，写入 SKILL.md

**流程**：
```
任务完成 → 判断触发条件 → 生成技能提取prompt → LLM生成技能草案 → 保存到skills/
```

**触发判断**：
```python
if (
    task.execution_time_minutes >= 10 or
    task.step_count >= 5 or
    task.is_first_occurrence and task.outcome == 'success'
):
    trigger_skill_crystallization(task)
```

**技能提取prompt模板**：
```
## 技能提取
任务描述：{task.description}
执行步骤：{task.steps}
成功要素：{task.success_factors}
请提炼成可复用的SKILL.md格式，包含：
- name: 技能名（动词短语）
- description: 一句话说明
- trigger: 何时使用
- steps: 核心步骤（3-5步）
- example: 示例场景
如果无法提炼成通用技能，请说明原因。
```

**保存位置**：`workspace/skills/generated/`
**命名**：`{skill-name}/SKILL.md`
**首次保存后**：追加到 skill_evaluator_plugin 评估队列

**与现有机制的关系**：
- 补充 self-improvement-core 的"从经验生成技能"短板
- 区别于 error-logger（错误记录）和 skill-vetter（审核验证）
- 结晶化 = 把成功经验变成技能，不是把失败写成错误日志

## 离线层（cron 异步执行）

离线层不在此文件中定义。它们在 cron job 中独立运行：

| cron job | 频率 | 功能 |
|:---------|:-----|:-----|
| wal-analysis | 每6小时 | 读 WAL 日志，发现重复错误模式 |
| confidence | 每天 | 评估每条约规的有效性评分 |
| memory-compress | 每天 | 15天前的日志脱水为月度摘要 |
| self-evolution-update | 每天 | 合并新规则到 SELF-EVOLUTION.md |

## Thinking Protocol（保留，压缩版）

> 完整版见 `skills/thinking-claude/`。

每次深度分析时，按以下顺序思考：
1. **问题分析** → 拆解到本质，找到真实约束
2. **多假设** → 最少2个方案，不默认第一个
3. **测试验证** → 如果结论有假设，标注"待验证"
4. **错误修正** → 遇矛盾不坚持先前立场
5. **综合输出** → 结论前置，证据在后

长上下文时，在执行过程中标记进度（[1/5] 问题分析... [3/5] 测试...）。

## 核心原则

1. **诚实第一** — 不知道就说不知道，不确定就说不确定
2. **证据驱动** — 先说结论，后面跟着证据，不写"我认为"，写"数据表明"
3. **场景隔离** — 技术对话是技术对话，写作是写作，不同场景不同规则
4. **最小化在线** — 只在对话中做必须做的事，分析留给离线

## 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v7.0.0 | 2026-05-30 | 在线/离线分离重写，在线层压缩至三件事，SELF-EVOLUTION.md 独立，会计层全部离线 |

## 相关技能

| 技能 | 关系 |
|:-----|:-----|
| skills/thinking-claude/ | Thinking Protocol 完整版 |
| workspace/SELF-EVOLUTION.md | 在线层行为规则表（v7.0 核心输出） |
| workspace/memory/ | WAL 日志 + 每日记忆 |
| skills/error-logger/ | 错误日志记录 |
