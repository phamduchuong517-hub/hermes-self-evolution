# 🦞 OpenClaw Core Skills v4.1

**AI 助手自我进化核心系统** — 7 个技能，聚焦行为级进化

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: 4.1.0](https://img.shields.io/badge/Version-4.1.0-green.svg)](https://github.com/phamduchuong517-hub/hermes-self-evolution/releases/tag/v4.1.0)
[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue)](https://github.com/project-hermes/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Core-red)](https://github.com/openclaw)

---

## 🌟 v4.1 新技能: memory-system-v2

> **记忆系统 v2** — 从 CC Harness Skills (LearnPrompt/cc-harness-skills) 吸收的四分类记忆提取 + 主题合并
>
> 4 个行为模式改进: 四分类记忆区块 | 主题合并 | 挑战性验证 | 多代理分工

| 技能 | 版本 | 说明 |
|:-----|:-----|:------|
| **memory-system-v2** ✨ | v1.0.0 | 四分类记忆提取 (user/feedback/project/reference) + 主题合并 + [MEM_APPEND] 标签系统 |
| **self-improvement-core** | v7.0.0 | 读规则表→执行→写WAL |
| **hermes-self-evolution** | v4.3.0 | 读规则表→执行→写规则 |

## 📦 技能包内容（7 个核心）

| 技能 | 类型 | 行数 | 核心能力 |
|:-----|:-----|:-----|:---------|
| **memory-system-v2** | 记忆 | 115 | 四分类记忆提取 + 主题合并 + [MEM_APPEND] 标签 |
| **self-improvement-core** | 核心 | 106 | 自我进化核心：规则表驱动，在线执行 |
| **hermes-self-evolution** | 核心 | N/A | 自我进化：写行为规则 |
| **task-orchestrator** | 流程 | N/A | 任务规划→执行→检查→反思 |
| **token-optimization** | 优化 | N/A | 上下文压缩 + 智能缓存 |
| **error-logger** | 日志 | N/A | 错误记录 + 分析 |
| **TaskBalancer** | 编排 | N/A | 多代理任务分发 |

---

## 快速使用

```bash
# 安装 memory-system-v2
cp skills/hermes-self-evolution/memory-system-v2/scripts/* ~/.hermes/scripts/
chmod +x ~/.hermes/scripts/memory_appender.sh
cat skills/hermes-self-evolution/memory-system-v2/prefill-evolution.txt >> ~/.hermes/prefill-evolution.txt
```

然后在对话中使用 `[MEM_APPEND:user: 内容]` 等标签自动分类保存记忆。

## 更多

- 详细文档: `skills/hermes-self-evolution/memory-system-v2/SKILL.md`
- 组件文件：scripts/ + prefill-evolution.txt + SELF-EVOLUTION.md
