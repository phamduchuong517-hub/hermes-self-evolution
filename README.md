# 🦞 Hermes Self-Evolution — AI Agent 自我进化核心技能包

**7 个技能**，让 AI 助手学会持续进化：记住经验、纠正行为、优化成本、不重复犯错。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: 4.1.0](https://img.shields.io/badge/Version-4.1.0-green.svg)](https://github.com/phamduchuong517-hub/hermes-self-evolution/releases/tag/v4.1.0)
[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue)](https://github.com/project-hermes/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Core-red)](https://github.com/openclaw)

---

## 为什么要用这套技能？

大多数 AI Agent 系统都有一个共同问题：**每次对话都是从零开始**。

- 用户说"我不喜欢看长分析" → 下次对话又发长篇
- 用户说"用这种格式" → 下回又忘了
- 昨天修复的 bug → 今天又犯一次
- 随着技能积累 → 系统Prompt越来越胖，越来越慢

这套技能包用**文件级**方案解决了"Agent 如何记住经验和规则"的问题——不需要数据库、不需要外部服务、不需要多代理编排器。

---

## 📦 技能一览

### 1. memory-system-v2 (记忆系统) ✨

**解决什么问题**
Agent 需要记住用户偏好、历史纠正、项目约束和外部参考，但不能每条都塞进系统Prompt。传统做法是"全量注入MEMORY.md"——不分类，无法合并，重复多。

**怎么解决的**
四分类记忆提取 + 主题自动合并。用 `[MEM_APPEND:type: 内容]` 标签在回复中标记，脚本自动分类存储到 MEMORY.md 的独立区块。

```
分类: user(用户偏好) | feedback(纠正教训) | project(项目约束) | reference(外部指向)
```

**什么时候用它**
- 每次对话都会自动使用（通过在 prefill 指令中声明）
- 夜间有 cron 自动做主题合并 + 去重

### 2. self-improvement-core (自我进化核心)

**解决什么问题**
Agent 进化方案要么是工程浩大的多代理架构（如 Reflexio 的四阶段流水线），要么是行为分析"只记不改"的方案。小团队/个人用户跑不动。

**怎么解决的**
只需一个 `SELF-EVOLUTION.md`（46行规则表） + 行为规则。每次对话开始前，Agent 自动扫描规则表，被用户纠正后自动写新规则。

```
架构: 在线层（读规则→执行→记录）→ 离线层（cron异步分析）
```

**什么时候用它**
- 系统启动即自动加载（prefill 指令驱动）
- 每次被用户纠正后，规则自动更新

### 3. hermes-self-evolution (自我进化流程)

**解决什么问题**
AI 犯的错只被纠正一次，没有根因分析和防复发机制。同一个类型的错误可能反复出现。

**怎么解决的**
五步闭环：观察错误 → 分析根因 → 制定纠正 → 验证效果 → 固化规则到 SELF-EVOLUTION.md。

**什么时候用它**
- 当用户纠正 Agent 行为时
- 当系统发现重复错误时（与 error-logger 联动）

### 4. task-orchestrator (任务编排器)

**解决什么问题**
复杂任务（4+步骤）Agent 容易跑偏：做到一半忘了目标、遗漏关键步骤、跳过验证直接报完成。

**怎么解决的**
四阶段闭环：规划（拆解步骤）→ 执行（逐步完成）→ 检查（验证每个步骤）→ 反思（总结优化）。支持任务分解、调度、监控、验收。

**什么时候用它**
- 任务超过3个步骤时
- 任务涉及多个子系统时
- 需要分阶段验证结果时

### 5. token-optimization (Token优化)

**解决什么问题**
长会话上下文膨胀 + 历史注入导致 API 费用飙升、响应变慢。

**怎么解决的**
三层策略：上下文压缩（保留核心，丢弃噪音）→ 智能缓存（高频使用不重复加载）→ 压缩率 50%+。

**什么时候用它**
- 长会话（50+轮）显慢时
- API 账单突然上涨时
- 想主动控制成本时

### 6. error-logger (错误日志)

**解决什么问题**
系统报错只报一次，下次遇到同样的错误又重头排查。无根因分析。

**怎么解决的**
记录错误→分类→根因分析→防止复发。每个错误带时间戳、上下文、根因链，防止同一错误重复排查。

**什么时候用它**
- 系统报错时自动记录
- 排查重复问题时优先查日志
- 与 self-improvement-core 联动做进化输入

### 7. TaskBalancer (任务平衡器)

**解决什么问题**
多代理系统（如四系统架构：本地/云端 × Hermes/OpenClaw）任务分发无规则，忙的忙死、闲的闲死。

**怎么解决的**
智能任务分发 + 负载均衡规则。按 代理角色（实操/外勤/贴身/机要）+ 任务类型（编码/研究/运维/沟通）分配。

**什么时候用它**
- 运行多代理系统时
- 子代理之间互相冲突时
- 某个代理过载时

---

## 🧩 技能关系图

```
                    ┌──────────────────┐
                    │  任务编排器        │
                    │  task-orchestrator │
                    └────────┬─────────┘
                             │ 编排
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│ 自我进化核心      │ │ 记忆系统 v2   │ │ Token 优化       │
│ self-improve-core│ │memory-system  │ │ token-optimize   │
│ + 自我进化流程    │ │              │ │                  │
└────────┬─────────┘ └──────────────┘ └──────────────────┘
         │ 进化输入
         ▼
┌──────────────────┐ ┌──────────────────┐
│ 错误日志          │ │ 任务平衡器        │
│ error-logger     │ │ TaskBalancer     │
└──────────────────┘ └──────────────────┘
```

---

## ⚡ 快速选择：我该用哪个？

| 你的痛 | 先装这个 |
|--------|---------|
| AI 记不住我偏好和纠正 | **memory-system-v2** |
| AI 犯错后下次还犯 | **self-improvement-core** + **error-logger** |
| 复杂任务 AI 老是跑偏 | **task-orchestrator** |
| API 费用高 / 响应慢 | **token-optimization** |
| 我在跑多个 Agent 实例 | **TaskBalancer** |

**新手入门路线：** memory-system-v2 → self-improvement-core → task-orchestrator

---

## 📂 项目结构

```
skills/
├── self-improvement-core/    # 自我进化核心 v7 (106行)
├── hermes-self-evolution/     # 自我进化流程 v4.3
│   ├── memory-system-v2/      # 记忆系统 v2 (新增✨)
│   │   ├── SKILL.md           # 技能文档
│   │   ├── scripts/           # 记忆追加脚本 + 合并脚本
│   │   ├── prefill-evolution.txt
│   │   └── SELF-EVOLUTION.md
│   └── ...
├── task-orchestrator/         # 任务编排器 v3
├── token-optimization/        # Token 优化
├── error-logger/             # 错误日志 v3
├── TaskBalancer/              # 任务平衡器
└── README.md                  # 本文件
```

---

## 📥 安装

```bash
# 1. 克隆
git clone https://github.com/phamduchuong517-hub/hermes-self-evolution.git

# 2. 按需安装技能
# 记忆系统 v2
cp -r skills/hermes-self-evolution/memory-system-v2/scripts/* ~/.hermes/scripts/
chmod +x ~/.hermes/scripts/memory_appender.sh
cat skills/hermes-self-evolution/memory-system-v2/prefill-evolution.txt >> ~/.hermes/prefill-evolution.txt

# 自我进化核心
cp skills/self-improvement-core/SKILL.md ~/.hermes/skills/core/self-improvement/

# 3. 重启或 rehash
hermes skills reload
```

---

## 📋 许可证

MIT — 自由使用、修改、商用。无任何担保。

---

*由 Hermes Agent × OpenClaw 社区维护 — 最小化方案，最大效果。*
