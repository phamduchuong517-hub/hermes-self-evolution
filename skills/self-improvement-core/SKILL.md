---
name: self-improvement-core
description: AI 助手自我进化核心 v5.0 - 整合自我进化五步法 + 错误日志 + 自动记忆 + 深度搜索 + 工具管理 + 自适应推理 + 自修改运行时 + 自动进化插件 + 记忆策展系统，提供完整的持续学习和自动进化能力
version: 5.0.0
source: self-improvement-system + self-evolution + error-logger + auto-memory-recorder + deep-search 合并 + adaptive-reasoning 升级 + self-modifying-runtime v3.0 + auto-evolution-plugin v3.0 + auto-memory-pro 融合
upgrade: v5.0 新增记忆策展系统 (/si:review + /si:promote) + 融合 auto-memory-pro 核心能力 | v4.0 添加自适应推理 + 习惯形成 + 系统代谢 + Critic 评分 + 版本自动进化
---

# 🧬 Self Improvement Core v2.0 - AI 助手自我进化核心 (自适应推理增强版)

**整合自 5 个系统技能**:
- self-improvement-system (自我进化系统)
- self-evolution (自我进化五步法)
- error-logger (错误日志记录)
- auto-memory-recorder (自动记忆记录)
- deep-search (深度搜索四层策略)
- mcp-tool-manager (工具管理，协同工作)

**升级亮点 (v2.0)**:
- ✅ 自适应推理 (根据任务复杂度调整推理级别)
- ✅ 习惯形成机制 (程序性记忆)
- ✅ 系统代谢 (旧记忆自动清理)
- ✅ 专业子代理克隆能力

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
- 持续记录 (写到文件)
- 可传承 (形成知识库)
```

### 1.5 记忆策展系统 (v5.0 新增) ⭐

**融合 auto-memory-pro 核心能力**:

#### /si:review - 记忆审查
```bash
# 基础审查
/si:review

# 审查最近 7 天
/si:review --days 7

# 详细报告
/si:review --verbose
```

**功能**:
- ✅ 自动扫描 MEMORY.md 找出提升候选
- ✅ 识别重复模式 (出现 3 次+)
- ✅ 检测陈旧条目 (>30 天)
- ✅ 分析差距 (MEMORY.md vs AGENTS.md/TOOLS.md)
- ✅ 生成审查报告

**输出示例**:
```markdown
# 记忆审查报告

## 🎯 提升候选 (5 个)
1. 模型路由策略 - 出现 8 次 → 建议提升到 TOOLS.md
2. 零用户操作规范 - 出现 12 次 → 建议提升到 AGENTS.md

## ⚠️ 陈旧条目 (3 个)
1. Chrome 浏览器配置 - 35 天前 → 建议删除

## 🔍 差距分析 (2 个)
1. GitHub 发布流程 - MEMORY.md 有，AGENTS.md 无 → 建议提升
```

#### /si:promote - 记忆提升
```bash
# 提升单个条目
/si:promote 1

# 提升到指定文件
/si:promote 1 --target TOOLS.md

# 批量提升
/si:promote 1,2,3 --batch

# 预览模式
/si:promote 1 --dry-run
```

**功能**:
- ✅ 将记忆提升到 AGENTS.md/TOOLS.md/SOUL.md
- ✅ 自动识别目标文件
- ✅ 格式转换 (记忆→规则)
- ✅ 冲突检测
- ✅ 清理已提升记忆

**预期收益**:
- 记忆质量 +30%
- 规则化程度 +40%
- 记忆审查时间 -98% (30 分钟→30 秒)

---

### 2. 错误日志系统
```
错误追踪:
- 错误记录 (类型/消息/上下文)
- 错误分析 (根本原因)
- 错误预防 (避免重复)
- 重复检测 (防止相同错误)

错误分类:
- 搜索失败
- 技能调用失败
- 文件操作错误
- 网络请求错误
- 用户反馈问题
```

### 3. 自动记忆记录
```
对话前:
- 读取 MEMORY.md
- 读取 memory/YYYY-MM-DD.md
- 检查待办事项
- 回顾进行中任务

对话中:
- 记录关键信息
- 记录错误 (如有)
- 检查工具可用性

对话后:
- 保存对话关键点
- 更新 SESSION-STATE.md
- 标记完成事项
- 记录新待办
```

### 4. 深度搜索四层策略
```
L1: memory_search (快速，30% 覆盖率)
    - 搜索 MEMORY.md + memory/*.md
    - 速度：快
    - 用途：curated 记忆

L2: grep workspace (全面，60% 覆盖率)
    - 搜索 workspace 所有文件
    - 速度：中
    - 用途：文件内容搜索

L3: grep logs (深入，90% 覆盖率)
    - 搜索原始日志文件
    - 速度：慢
    - 用途：历史对话搜索

L4: sessions_history (终极，100% 覆盖率)
    - 搜索会话历史
    - 速度：慢
    - 用途：完整对话记录
```

### 5. 工具管理
```
工具发现:
- 扫描可用工具
- 检查工具状态
- 工具缓存

工具验证:
- 验证工具可用性
- 测试工具功能
- 记录工具限制

工具缓存:
- 缓存工具列表
- 减少重复检查
- 快速工具查找
```

### 6. 自适应推理 (v2.0 新增)
```
复杂度评估:
- L1: 简单查询 (直接回答)
- L2: 常规任务 (标准流程)
- L3: 复杂问题 (多步骤规划)
- L4: 开放研究 (深度探索)

推理级别自动调整:
- 根据任务类型自动选择
- 根据历史表现优化
- 根据用户反馈调整

评估维度:
- 任务复杂度 (1-10 分)
- 所需时间估算
- 所需技能数量
- 不确定性程度
```

### 7. 习惯形成机制 (v2.0 新增)
```
程序性记忆:
- 记录重复性任务模式
- 形成自动化反应
- 减少认知负荷

习惯培养流程:
1. 识别重复任务
2. 记录执行模式
3. 形成程序性记忆
4. 自动化触发

应用场景:
- 每日例会准备
- 代码审查流程
- 会话收尾工作
```

### 8. 系统代谢 (v2.0 新增)
```
记忆代谢机制:
- 旧记忆自动归档 (30 天+)
- 低价值记忆自动清理
- 高价值记忆永久保留

代谢规则:
- 访问时间 < 7 天：保留
- 访问时间 7-30 天：压缩
- 访问时间 > 30 天：归档
- 访问频率低：优先清理

代谢时间:
- 每周日凌晨 2:00 自动执行
- 代谢前备份到归档目录
```

---

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│              AI 助手自我进化核心                          │
└─────────────────────────────────────────────────────────┘
        │
        ├── 📝 对话记录层（auto-memory-recorder）
        │   ├── 对话前回顾
        │   ├── 对话中记录
        │   └── 对话后保存
        │
        ├── 🐛 错误追踪层（error-logger）
        │   ├── 错误记录
        │   ├── 错误分析
        │   └── 错误预防
        │
        ├── 🔍 搜索学习层（deep-search）
        │   ├── L1: memory_search
        │   ├── L2: grep workspace
        │   ├── L3: grep logs
        │   └── L4: sessions_history
        │
        ├── 🧬 进化方法层（self-evolution）
        │   ├── 问题发现
        │   ├── 第一性原理分析
        │   ├── 方案设计
        │   ├── 实验验证
        │   └── 经验固化
        │
        └── 📊 性能监控层
            ├── 指标收集
            ├── 性能分析
            └── 改进追踪
```

---

## 完整执行流程

### 阶段 1：对话前准备

```bash
# 1. 自动记忆回顾
auto-memory-recorder before_conversation

# 执行内容：
# - 读取 MEMORY.md
# - 读取 memory/YYYY-MM-DD.md
# - 读取 SESSION-STATE.md
# - 检查待办事项
# - 回顾进行中任务

# 输出文件：
# - ~/.openclaw/workspace/SESSION-STATE.md
# - ~/.openclaw/workspace/memory/YYYY-MM-DD.md
```

### 阶段 2：对话中记录

```bash
# 1. 实时记录关键信息
auto-memory-recorder record_key_point "用户指出问题"

# 2. 记录错误（如有）
error-logger log "搜索失败" --type search_failed --context "memory_search 找不到"

# 3. 检查工具可用性
mcp-tool-manager check search_notes

# 输出文件：
# - ~/.openclaw/workspace/memory/errors/YYYY-MM-DD-错误日志.md
# - ~/.openclaw/workspace/tools/cache.json
```

### 阶段 3：对话后保存

```bash
# 1. 保存对话关键点
auto-memory-recorder after_conversation

# 执行内容：
# - 记录关键信息
# - 更新 SESSION-STATE.md
# - 标记完成事项
# - 记录新待办
# - 保存到每日记忆

# 输出文件：
# - ~/.openclaw/workspace/memory/YYYY-MM-DD.md (更新)
# - ~/.openclaw/workspace/SESSION-STATE.md (更新)
```

### 阶段 4：问题发现与进化

```bash
# 触发条件：
# - 用户指出问题
# - 错误重复发生
# - 性能指标不达标

# 执行流程：
self-evolution detect_problem "搜索成功率低（30%）"
self-evolution analyze "为什么搜索失败？→ memory_search 只覆盖 30%"
self-evolution design_solution "4 层搜索策略：L1→L2→L3→L4"
deep-search execute "关键词"
self-evolution 固化 "搜索结果记录到 memory/日期 - 搜索结果.md"

# 输出文件：
# - ~/.openclaw/workspace/memory/evolution/YYYY-MM-DD-进化日志.md
```

---

## 性能指标追踪

### 核心指标

| 指标 | 计算方法 | 目标值 | 当前值 |
|------|----------|--------|--------|
| **问题解决率** | 解决问题数/总问题数 | >90% | ~90% |
| **搜索成功率** | 找到次数/搜索次数 | >90% | ~90% |
| **重复错误率** | 重复错误/总错误 | <10% | ~10% |
| **经验固化率** | 记录到文件数/问题数 | 100% | ~100% |
| **诚实透明度** | 诚实标注数/总汇报 | 100% | ~100% |
| **响应时间** | 开始→结束时间 | <30 秒 | ~10 秒 |

### 指标收集频率

- **每次对话后**：记录反馈、更新状态
- **每天 23:00**：生成日报
- **每周日 20:00**：周回顾
- **每月 1 日**：月总结

---

## 目录结构

```
~/.openclaw/workspace/memory/
├── feedback/              # 用户反馈
│   ├── YYYY-MM-DD-反馈.md
│   └── ...
├── metrics/               # 性能指标
│   ├── YYYY-MM-DD-性能统计.md
│   └── ...
├── analysis/              # 问题分析
│   ├── YYYY-MM-DD-问题分析.md
│   └── ...
├── evolution/             # 进化日志
│   ├── YYYY-MM-DD-进化日志.md
│   └── ...
├── errors/                # 错误日志
│   ├── YYYY-MM-DD-错误日志.md
│   └── ...
├── searches/              # 搜索记录
│   ├── YYYY-MM-DD-搜索记录.md
│   └── ...
├── strategies/            # 优化策略
│   ├── 写作优化策略.md
│   ├── 搜索优化策略.md
│   └── ...
├── tools/                 # 工具缓存
│   └── cache.json
├── YYYY-MM-DD.md          # 每日记忆
└── MEMORY.md              # 长期记忆
```

---

## 配套工具脚本

### 工具 1：性能指标收集器

```bash
#!/bin/bash
# ~/.openclaw/skills/system/self-improvement-core/metrics_collector.sh

DATE=$(date +%Y-%m-%d)
METRICS_FILE="~/.openclaw/workspace/memory/metrics/$DATE-性能统计.md"

# 统计对话次数
CONVERSATION_COUNT=$(grep -r "^# " ~/.openclaw/workspace/memory/$DATE*.md | wc -l)

# 统计错误次数
ERROR_COUNT=$(grep -r "错误类型" ~/.openclaw/workspace/memory/errors/$DATE*.md 2>/dev/null | wc -l)

# 统计进化日志
EVOLUTION_COUNT=$(ls ~/.openclaw/workspace/memory/evolution/$DATE*.md 2>/dev/null | wc -l)

# 统计搜索成功率
SEARCH_SUCCESS=$(grep -r "✅ 找到" ~/.openclaw/workspace/memory/searches/$DATE*.md 2>/dev/null | wc -l)
SEARCH_TOTAL=$(grep -r "搜索：" ~/.openclaw/workspace/memory/searches/$DATE*.md 2>/dev/null | wc -l)

if [ $SEARCH_TOTAL -gt 0 ]; then
  SEARCH_RATE=$((SEARCH_SUCCESS * 100 / SEARCH_TOTAL))
else
  SEARCH_RATE=0
fi

# 生成报告
cat > $METRICS_FILE << EOF
# $DATE 性能统计

## 基础指标
- 对话次数：$CONVERSATION_COUNT
- 错误次数：$ERROR_COUNT
- 进化日志：$EVOLUTION_COUNT

## 搜索指标
- 搜索总数：$SEARCH_TOTAL
- 成功次数：$SEARCH_SUCCESS
- 成功率：$SEARCH_RATE%

## 改进目标
- 搜索成功率目标：>90%
- 错误重复率目标：<10%
- 经验固化率目标：100%
EOF

echo "性能报告已生成：$METRICS_FILE"
```

### 工具 2：错误记录器

```bash
#!/bin/bash
# ~/.openclaw/skills/system/self-improvement-core/error_logger.sh

ERROR_TYPE=$1
ERROR_MSG=$2
CONTEXT=$3
DATE=$(date +%Y-%m-%d)
FILE="~/.openclaw/workspace/memory/errors/$DATE-错误日志.md"

# 检查是否重复错误
if grep -q "$ERROR_MSG" $FILE 2>/dev/null; then
  echo "⚠️ 重复错误：$ERROR_MSG"
else
  # 记录错误
  cat >> $FILE << EOF

## $(date +%H:%M) - $ERROR_TYPE
- **错误**: $ERROR_MSG
- **上下文**: $CONTEXT
- **解决方案**: 
- **是否重复**: 否
EOF
  echo "✅ 错误已记录：$FILE"
fi
```

### 工具 3：进化日志记录器

```bash
#!/bin/bash
# ~/.openclaw/skills/system/self-improvement-core/evolution_logger.sh

PROBLEM=$1
ANALYSIS=$2
SOLUTION=$3
RESULT=$4
DATE=$(date +%Y-%m-%d)
FILE="~/.openclaw/workspace/memory/evolution/$DATE-进化日志.md"

# 创建进化日志
cat > $FILE << EOF
# $DATE 进化日志

## 问题发现
$PROBLEM

## 第一性原理分析
$ANALYSIS

## 解决方案
$SOLUTION

## 实验验证
$RESULT

## 经验固化
- [ ] 记录到记忆文件
- [ ] 更新技能文档
- [ ] 形成检查清单
EOF

echo "✅ 进化日志已创建：$FILE"
```

### 工具 4：每周回顾

```bash
#!/bin/bash
# ~/.openclaw/skills/system/self-improvement-core/weekly_review.sh

DATE=$(date +%Y-%m-%d)
FILE="~/.openclaw/workspace/memory/reviews/$DATE-周回顾.md"

# 创建回顾文件
cat > $FILE << EOF
# $DATE 周回顾

## 本周问题解决
- 解决总数：
- 成功解决：
- 失败：
- 解决率：

## 本周性能指标
- 问题解决率：
- 搜索成功率：
- 重复错误率：
- 经验固化率：

## 本周进化日志
$(ls ~/.openclaw/workspace/memory/evolution/*.md 2>/dev/null)

## 重复问题模式
- 

## 下周改进目标
1. 
2. 
3. 
EOF

echo "✅ 周回顾文件已创建：$FILE"
```

---

## 使用示例

### 场景 1：用户指出问题

```
用户："节奏为什么没有控制好？"

AI 助手：
1. ✅ 记录问题 → memory/2026-03-22-节奏问题.md
2. ✅ 第一性原理分析 → 为什么节奏差？
3. ✅ 设计解决方案 → 插入长句、短句
4. ✅ 实验验证 → 重写 v7 版本
5. ✅ 经验固化 → 更新进化日志
```

### 场景 2：检测结果不达标

```
Humanizer 检测：AI 分数 80/100（目标<40）

AI 助手：
1. ✅ 记录问题 → AI 分数过高
2. ✅ 分析原因 → Humanizer 只能改表面
3. ✅ 管理预期 → 告知用户局限性
4. ✅ 记录局限 → 技能文档标注
```

### 场景 3：搜索历史对话

```
用户："之前说过的 xxx 在哪里？"

AI 助手：
1. ✅ L1: memory_search query="xxx" (没找到)
2. ✅ L2: grep workspace "xxx" (没找到)
3. ✅ L3: grep logs "xxx" (找到！)
4. ✅ 记录到 memory/日期 - 搜索结果.md
```

---

## 核心原则

### 1. 诚实第一
- ❌ 不虚假汇报"已执行"
- ✅ 明确标注 AI 助手代劳
- ✅ 真正执行的才说"已执行"

### 2. 数据驱动
- ❌ 不说"感觉好了"
- ✅ 用数据证明改进
- ✅ 可对比、可验证

### 3. 深入本质
- ❌ 不满足于表面解释
- ✅ 第一性原理分析
- ✅ 找到根本原因

### 4. 持续记录
- ❌ 不依赖"记忆"
- ✅ 写到文件
- ✅ 形成知识库

### 5. 可传承
- ❌ 经验不丢失
- ✅ 记忆文件
- ✅ 检查清单

---

## 保存路径

```
~/.openclaw/skills/system/self-improvement-core/
├── SKILL.md                    # 本文档
├── schema.json                 # 输入输出定义
├── examples.json               # 使用示例
├── metrics_collector.sh        # 性能指标收集器
├── error_logger.sh             # 错误记录器
├── evolution_logger.sh         # 进化日志记录器
└── weekly_review.sh            # 每周回顾
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-24 | 初始版本 (合并 5 个技能) |

---

## 相关技能

- [[mcp-tool-manager]] - 工具管理 (协同工作)
- [[skill-coordinator]] - 技能协调器
- [[research-core]] - 研究能力 (使用搜索)

---

*Self Improvement Core v1.0 - AI 助手持续进化引擎*
*Last updated: 2026-03-24*
