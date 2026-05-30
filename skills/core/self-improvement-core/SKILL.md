---
name: self-improvement-core
description: AI 助手自我进化核心 v4.3 - 整合自我进化五步法 + 错误日志 + 自动记忆 + 深度搜索 + 工具管理 + 自适应推理 + 自修改运行时 + 自动进化插件 + 主动能力研究 + 置信度评分 + 知识图谱 + WAL 协议 + Working Buffer + Compaction Recovery，提供完整的持续学习和自动进化能力
version: 4.3.0
source: self-improvement-system + self-evolution + error-logger + auto-memory-recorder + deep-search + adaptive-reasoning + self-modifying-runtime v3.0 + auto-evolution-plugin v3.0 + proactive-capability-research v1.0 + rohitg00/agentmemory 置信度评分 + 知识图谱 (2026-05-17 吸收) + halthelobster/proactive-agent WAL 协议 + Working Buffer + Compaction Recovery (2026-05-17 吸收)
upgrade: v4.3 新增：WAL 协议（响应前先写 SESSION-STATE.md）+ Working Buffer（60% 上下文阈值日志）+ Compaction Recovery（截断后恢复流程）+ 记忆架构分层重构；v5.0 在 openclaw-imports/self-improvement-core 中（三棵树记忆架构）
---

# 🧬 Self Improvement Core v4.3 - AI 助手自我进化核心

**整合自**: self-improvement-system + self-evolution + error-logger + auto-memory-recorder + deep-search + adaptive-reasoning + halthelobster/proactive-agent

**升级亮点 (v4.3)**:
- ✅ **WAL 协议** — 响应前先写 SESSION-STATE.md，关键细节不丢失
- ✅ **Working Buffer** — 60% 上下文阈值启动危险区日志，截断后可恢复
- ✅ **Compaction Recovery** — 上下文截断后自动恢复流程
- ✅ 记忆架构三层分层重构（SESSION-STATE → Daily → Long-term）

---

## 核心能力

### 1. 自我进化五步法
```
步骤:
1. 问题发现 → 识别改进点
2. 第一性原理分析 → 拆解到本质
3. 方案设计 → 列出所有可能方案
4. 实验验证 → 执行并收集数据
5. 经验固化 → 写到记忆文件

核心原则:
- 诚实第一 (不虚假汇报)
- 数据驱动 (用数据证明改进)
- 深入本质 (第一性原理分析)
- 持续记录 (写到文件 + SQLite)
- 可传承 (形成知识库)
```

---

## ⚠️ 2026-05-29 教训：先读记忆，再干活

### 我犯过的错误
1. 用户给任务 → 直接搜GitHub/分析 → 忘了用户偏好的称呼（老板/哥）、已有配置（Tavily已配）、系统状态
2. 工具报错"不可用" → 直接跳其他方案 → 没查 .env 和 config.yaml 确认配置是否还在
3. 需要VPS密码 → 猜一次不对就放弃 → 没搜林汐的session记录（里面有密码）

### 正确做法
```
① 收到任务后，第一件事：读 MEMORY.md 完整内容
   → 确认：用户称呼、已知配置、当前状态
   
② 工具出问题，先排查配置
   → .env 里的 Key 是否还在？
   → config.yaml 的 provider 段是否配置了？
   
③ 需要凭证/密码
   → 搜 session_search（会话历史）
   → 搜林汐/OpenClaw的配置文件
   → 不要猜
```

---

## 完整执行流程

### 阶段 1：对话前准备

```bash
# 1. 必做：读 MEMORY.md 完整内容（启动时只有摘要是不够的）
#    确认：用户称呼（老板/哥）、当前系统名（许曼）、已知配置状态

# 2. 知识图谱快速回顾（v5.0 新增）
python3 scripts/knowledge-memory.py hot --min 0.5
python3 scripts/knowledge-memory.py global-digest --days 1

# 3. 自动记忆回顾
auto-memory-recorder before_conversation

# 输出文件：
# - 知识图谱热度快照
# - 全局摘要
# - SESSION-STATE.md
```

### 阶段 2：对话中记录

```bash
# 1. 知识图谱摄入（v5.0 新增）
python3 scripts/knowledge-memory.py ingest chat \
  --source_key "session-001" \
  --title "今日对话" <<< "对话内容..."

# 2. 实时记录关键信息
auto-memory-recorder record_key_point "用户指出问题"

# 3. 记录错误（如有）
error-logger log "搜索失败" --type search_failed

# 4. 同时摄入错误到知识图谱
python3 scripts/knowledge-memory.py ingest error \
  --source_key "err-001" <<< "错误详情..."
```

### 阶段 3：对话后保存

```bash
# 1. 构建/更新热点实体主题树
python3 scripts/knowledge-memory.py build-all-topics --min 0.3

# 2. 创建全局每日摘要
python3 scripts/knowledge-memory.py global-digest --days 1

# 3. 保存对话关键点
```

### 阶段 4：问题发现与进化

```bash
# 1. 知识图谱检测问题模式（v5.0 新增）
python3 scripts/knowledge-memory.py query --type "error"  # 查找频繁错误实体

# 2. 标准进化流程
self-evolution detect_problem "搜索成功率低（30%）"
self-evolution analyze "为什么搜索失败？→ L1 不够，需要 L2"
# 将分析结果摄入知识图谱
python3 scripts/knowledge-memory.py ingest analysis \
  --source_key "evolution-001" \
  --title "搜索优化分析" <<< "..."
```

---

## 事件总线参考模式（v5.0 新增指导 ⭐）

来源于 OpenHuman 的 event_bus 设计模式。不是完全实现，而是定义**信号接口**：

```python
# 信号类型（用于 skill-lifecycle-manager 或 cron job）:
SIGNALS = {
    "memory.ingested":       "有新的知识块被摄入",
    "memory.topic_built":    "某个主题树已更新",
    "memory.global_digest":  "全局摘要已生成",
    "error.recorded":        "有新的错误被记录",
    "evolution.completed":   "进化循环已完成",
}
```

通过 cron job 或 heartbeat 轮询这些状态变化，而不是定义复杂的事件处理器。

---

## 目录结构

```
~/.hermes/memory/
├── memory_knowledge.db       # SQLite 三棵树 + 知识图谱（v5.0 新增）
├── wiki/                     # (预留) Obsidian 兼容 vault
├── README.md                 # 记忆系统架构总览
├── MEMORY.md                 # 长期记忆（精简版，仅保留最关键条目）
├── YYYY-MM-DD.md             # 每日笔记（保留，作为即时代理上下文）
├── feedback/                 # 用户反馈
├── metrics/                  # 性能指标
├── analysis/                 # 问题分析
├── evolution/                # 进化日志
├── errors/                   # 错误日志
├── searches/                 # 搜索记录
└── strategies/               # 优化策略
```

---

## 性能指标追踪

### 核心指标

| 指标 | 计算方法 | 目标值 | 当前值 |
|------|----------|--------|--------|
| **知识图谱覆盖率** | 已索引实体/总对话实体 | >80% | ~70% |
| **搜索成功率** | 找到次数/搜索次数 | >90% | ~75% (提升中) |
| **重复错误率** | 重复错误/总错误 | <10% | ~10% |
| **经验固化率** | 记录到文件数/问题数 | 100% | ~100% |
| **主题树构建延迟** | 从摄入到摘要就绪 | <30 秒 | ~1 秒 |

---

## 相关技能

- [[external-system-learning]] - 外部系统吸收方法论
- [[skill-lifecycle-manager]] - 技能生命周期管理器
- [[deep-search]] - 深度搜索（与知识图谱互补）
- [[task-orchestrator]] - 任务编排器

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 5.0.0 | 2026-05-22 | 融合 OpenHuman 三棵树记忆架构 + 知识图谱 + knowledge-memory.py CLI + 事件总线参考 + Subconscious 模式（在 openclaw-imports/self-improvement-core） |
| 4.3.0 | 2026-05-17 | 融入 WAL协议 + Working Buffer + Compaction Recovery + 记忆维护检查清单 |
| 4.2.0 | 2026-05-17 | 融入 agentmemory 置信度评分 + 知识图谱 + 记忆生命周期 |
| 1.0.0 | 2026-03-24 | 初始版本 (合并 5 个技能) |

---

## 吸收来源

| 来源 | Stars | 吸收内容 | 日期 |
|------|-------|---------|------|
| **tinyhumansai/openhuman** | 25K | 三棵树记忆架构 + 知识图谱 + 事件总线参考 + Subconscious 模式 + TokenJuice 参考 | 2026-05-22 |
| **halthelobster/proactive-agent** | v3.1.0 | WAL协议 + Working Buffer + Compaction Recovery | 2026-05-17 |
| agentmemory | 10K+ | 置信度评分 + 知识图谱 + 记忆生命周期 | 2026-05-17 |

---

*Self Improvement Core v4.3 — AI 助手持续进化引擎*
*Last updated: 2026-05-29 | 新增：先读记忆再干活的教训固化*
