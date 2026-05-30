---
name: memory-system-v2
description: 记忆系统 v2 — 四分类记忆提取（user/feedback/project/reference）+ 主题合并 + [MEM_APPEND] 标签系统。从 CC Harness Skills (LearnPrompt/cc-harness-skills) memory-extractor + dream-memory 吸收的模式级改进
version: 1.0.0
source: CC Harness Skills (memory-extractor + dream-memory) + Hermes Agent 本地适配
tags: [memory, evolution, self-improvement, hermse-agent, classification]
upgrade: v2.0 新增：四分类记忆区块 + 主题合并 + 挑战性验证 + 多代理分工工作流
---

# 🧠 记忆系统 v2 — 四分类提取 + 主题合并

**吸收自**: CC Harness Skills (`memory-extractor` + `dream-memory`) + `verification-gate` + `swarm-coordinator`

> **核心改进**: 从"一条临时日志全塞进去"变为"分类提取 + 主题合并 + 去重归档"

---

## 改进清单

### 1. 四分类记忆提取（memory-extractor）

**文件**: `~/.hermes/scripts/memory_appender.sh` (v2)

标签格式: `[MEM_APPEND:type: content]`
- `[MEM_APPEND:user: ...]` — 用户偏好/角色/协作风格/知识
- `[MEM_APPEND:feedback: ...]` — 纠正/验证过的工作偏好
- `[MEM_APPEND:project: ...]` — 截止日期/动机/约束
- `[MEM_APPEND:reference: ...]` — 外部指向/URL/文档位置

旧格式 `[MEM_APPEND: content]` 兼容，自动归入通用日志。

**区块**: 每个分类独立区块（👤 📝 🎯 🔗），自动创建。

### 2. 主题合并记忆（dream-memory）

**文件**: `~/.hermes/scripts/memory_consolidator.py` (v2)

夜间整理时:
- 分类区块保留独立
- 通用日志做主题识别合并（基于关键词规则）
- 去重（同内容不重复归档）

### 3. 挑战性验证（verification-gate）

**位置**: `SELF-EVOLUTION.md` 🟢 工作流规则

实施完成后做只读挑战:
- 检查"声称完成"有否验证证据
- 找边缘情况（空输入/网络断开/权限不足）
- 区分 ✅已验证 / ⚠️未验证 / ❌验证失败

### 4. 多代理分工（swarm-coordinator）

**位置**: `SELF-EVOLUTION.md` 🟢 工作流规则

复杂任务拆分为:
1. **研究** — delegate_task 独立研究
2. **综合** — 分析结果
3. **实施** — 执行代码
4. **验证** — +挑战性审查

---

## 安装

```bash
# 1. 记忆追加脚本
cp scripts/memory_appender.sh ~/.hermes/scripts/
chmod +x ~/.hermes/scripts/memory_appender.sh

# 2. 记忆合并脚本
cp scripts/memory_consolidator.py ~/.hermes/scripts/
python3 ~/.hermes/scripts/memory_consolidator.py  # 首次运行

# 3. prefill 指令
cat prefill-evolution.txt >> ~/.hermes/prefill-evolution.txt

# 4. SELF-EVOLUTION.md
cp SELF-EVOLUTION.md ~/.hermes/
```

## 依赖

- `bash` + `grep` + `sed` (核心工具，几乎所有 Linux 都有)
- `python3` (memory_consolidator.py 需要)
- 无额外依赖

## 文件清单

| 文件 | 行数 | 作用 |
|------|------|------|
| `scripts/memory_appender.sh` | 100 | 四分类记忆追加 + 区块自动创建 + 旧格式兼容 |
| `scripts/memory_consolidator.py` | 213 | 主题识别合并 + 去重归档 + Cron 夜间运行 |
| `prefill-evolution.txt` | 35 | 启动指令：四分类 + Skill Factory 模式检测 |
| `SELF-EVOLUTION.md` | 52 | 行为规则：挑战性验证 + 多代理分工 |

## Cron 任务

```bash
# 记忆夜间合并（每天 03:00）
hermes cron create --name "记忆夜间归档" \
  --schedule "0 3 * * *" \
  --script "memory_consolidator.py" \
  --no-agent \
  --deliver local
```

## 与上游的差异

| 功能 | CC Harness Skills | 本实现 | 差异原因 |
|------|-------------------|--------|---------|
| 分类提取 | Python SDK 方式 | shell + prefill 指令 | Hermes 无 plugin 系统，用 prefill 更轻量 |
| 主题合并 | 脚本检查 + prompt 模板 | Python 自动化 | 我们不需要交互式检查，cron 全自动 |
| 验证门 | 交互式脚本 | 行为规则硬编码 | 我们不需要对话框，LLM 自己执行 |
| 多代理 | 交互式脚本 | 行为规则 | 同理 |
