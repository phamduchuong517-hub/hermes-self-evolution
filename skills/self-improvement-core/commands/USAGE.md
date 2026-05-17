# /si:review + /si:promote 使用指南

**版本**: v1.0 (2026-04-22 创建)  
**来源**: 融合 auto-memory-pro + self-improvement-core v5.0

---

## 🚀 快速开始

### 1. 执行记忆审查

```bash
# 基础审查 (最近 30 天)
python3 skills/self-improvement-core/commands/si-review/si_review.py

# 审查最近 7 天
python3 skills/self-improvement-core/commands/si-review/si_review.py --days 7

# 详细报告
python3 skills/self-improvement-core/commands/si-review/si_review.py --verbose

# 组合使用
python3 skills/self-improvement-core/commands/si-review/si_review.py --days 14 --verbose
```

### 2. 查看提升候选

审查报告会列出所有提升候选，例如：

```markdown
## 🎯 提升候选 (20 个)

### 1. workspace
- **出现次数**: 18 次
- **关键词**: workspace, 文件，目录
- **建议提升目标**: TOOLS.md

### 2. memory
- **出现次数**: 15 次
- **关键词**: memory, 记忆，MEMORY.md
- **建议提升目标**: AGENTS.md
```

### 3. 执行记忆提升

```bash
# 提升单个条目 (自动选择目标)
python3 skills/self-improvement-core/commands/si-promote/si_promote.py 1

# 提升到指定文件
python3 skills/self-improvement-core/commands/si-promote/si_promote.py 1 --target TOOLS.md

# 批量提升
python3 skills/self-improvement-core/commands/si-promote/si_promote.py 1,2,3 --batch

# 预览模式 (不实际执行)
python3 skills/self-improvement-core/commands/si-promote/si_promote.py 1 --dry-run

# 保留原记忆
python3 skills/self-improvement-core/commands/si-promote/si_promote.py 1 --keep
```

---

## 📋 完整工作流

### 工作流 1: 每周记忆审查

```bash
# 每周一执行
python3 si_review.py --days 7 --verbose > weekly-review.md

# 查看报告
cat weekly-review.md

# 提升高优先级候选
python3 si_promote.py 1
python3 si_promote.py 2

# 验证提升结果
cat AGENTS.md | tail -50
cat TOOLS.md | tail -50
```

---

### 工作流 2: 月度记忆整理

```bash
# 月末执行
python3 si_review.py --days 30 > monthly-review.md

# 批量提升
python3 si_promote.py 1,2,3,4,5 --batch

# 检查提升日志
cat docs/PROMOTE-LOG.md
```

---

### 工作流 3: 项目结束后整理

```bash
# 项目完成后立即审查
python3 si_review.py --days 14

# 提升项目相关规则
python3 si_promote.py 1 --target TOOLS.md

# 清理临时记忆
# (提升后自动标记为"已提升")
```

---

## 🎯 最佳实践

### 1. 定期审查

**频率建议**:
- 高频用户：每周审查 (--days 7)
- 中频用户：每两周审查 (--days 14)
- 低频用户：每月审查 (--days 30)

**最佳时间**:
- 周一上午：规划本周
- 周五下午：复盘本周
- 月末：月度整理

---

### 2. 智能提升

**提升优先级**:
1. **高优先级** - 出现 10 次+ 的模式
2. **中优先级** - 出现 5-9 次的模式
3. **低优先级** - 出现 3-4 次的模式

**提升目标选择**:
- **AGENTS.md** - 行为规范、交互原则、工作流程
- **TOOLS.md** - 工具配置、API Key、环境设置
- **SOUL.md** - 人格定义、核心价值观

---

### 3. 冲突处理

当检测到冲突时 (相似度 >60%)：

```bash
# 方案 1: 跳过
python3 si_promote.py 1 --action skip

# 方案 2: 替换
python3 si_promote.py 1 --action replace

# 方案 3: 合并
python3 si_promote.py 1 --action merge

# 方案 4: 追加
python3 si_promote.py 1 --action append
```

---

### 4. 记忆清理

**提升后自动清理**:
- 默认行为：标记为"已提升"
- 可选行为：移动到归档区

**手动清理**:
```bash
# 归档陈旧记忆 (>30 天)
python3 si_review.py --days 30 | grep "陈旧条目"

# 手动删除或归档
```

---

## 📊 输出示例

### 审查报告示例

```markdown
# 📊 记忆审查报告

**审查时间**: 2026-04-22 11:20
**审查范围**: 最近 30 天

## 📊 基础统计
- MEMORY.md 总行数：493
- 记忆文件数：47
- 重复模式数：20
- 陈旧条目数：0
- 差距数：10

## 🎯 提升候选

### 1. workspace
- **出现次数**: 18 次
- **关键词**: workspace, 文件，目录
- **示例**: 核心记忆：`workspace/MEMORY.md`...
- **建议提升目标**: TOOLS.md

## ⚠️ 陈旧条目

暂无陈旧条目

## 🔍 差距分析

### 1. 待办事项 (todo)
- **MEMORY.md 中有**: ✅
- **AGENTS.md 中有**: ❌
- **建议**: 提升到 AGENTS.md

## 📋 执行建议

**立即提升** (3 个):
- workspace → TOOLS.md
- memory → AGENTS.md
- skills → AGENTS.md
```

---

### 提升结果示例

```markdown
## ✅ 提升成功

**条目 ID**: 1
**条目名称**: workspace
**目标文件**: TOOLS.md
**提升时间**: 2026-04-22 11:20

### 提升内容

## 💼 工作区配置

- 工作目录：`/root/.openclaw/workspace`
- 技能目录：`/root/.openclaw/workspace/skills`
- 文档目录：`/root/.openclaw/workspace/docs`

### 后续操作

- ✅ 已追加到 `TOOLS.md` 第 3 节
- ✅ 已在 `MEMORY.md` 标记为"已提升"
- ⚠️ 建议：检查 `TOOLS.md` 格式是否符合预期
```

---

## 🔧 高级用法

### 1. 自定义审查规则

创建 `.si-config.json`:

```json
{
  "review": {
    "default_days": 30,
    "min_pattern_count": 3,
    "stale_threshold_days": 30
  },
  "promote": {
    "auto_detect_target": true,
    "conflict_threshold": 0.6,
    "cleanup_after_promote": true
  },
  "keywords": {
    "stopwords": ["2026", "04", "v3"],
    "min_word_length": 2
  }
}
```

使用配置:

```bash
python3 si_review.py --config .si-config.json
```

---

### 2. 集成到自动化流程

**Cron 定时任务**:

```bash
# 每周一 9:00 执行审查
0 9 * * 1 python3 /root/.openclaw/workspace/skills/self-improvement-core/commands/si-review/si_review.py --days 7 >> /var/log/si-review.log

# 每月 1 号执行提升
0 9 1 * * python3 /root/.openclaw/workspace/skills/self-improvement-core/commands/si-promote/si_promote.py 1,2,3 --batch >> /var/log/si-promote.log
```

---

### 3. 与其他命令配合

```bash
# 审查 → 提升 → 查看状态
python3 si_review.py
python3 si_promote.py 1
python3 si_status.py  # 待实现

# 审查 → 提取技能
python3 si_review.py
python3 si_extract.py 1  # 待实现
```

---

## ❓ 常见问题

### Q1: 为什么识别出很多无意义关键词？

**A**: 当前使用简单词频统计，建议：
- 添加停用词过滤
- 增加最小词长度限制
- 使用 TF-IDF 算法 (待实现)

---

### Q2: 提升后原记忆会删除吗？

**A**: 默认标记为"已提升"，不会删除。
如需删除，使用 `--remove` 参数 (待实现)。

---

### Q3: 如何回滚提升操作？

**A**: 
1. 查看提升日志：`cat docs/PROMOTE-LOG.md`
2. 手动从目标文件删除
3. 从 MEMORY.md 取消标记

---

### Q4: 提升后格式不对怎么办？

**A**: 
1. 手动调整目标文件格式
2. 反馈问题，优化转换规则
3. 使用 `--dry-run` 预览

---

### Q5: 支持批量提升吗？

**A**: 支持！使用 `--batch` 参数：
```bash
python3 si_promote.py 1,2,3 --batch
```

---

## 📈 效果追踪

### 提升统计

```bash
# 查看提升日志
cat docs/PROMOTE-LOG.md

# 统计提升次数
grep "提升成功" docs/PROMOTE-LOG.md | wc -l

# 查看最近提升
tail -50 docs/PROMOTE-LOG.md
```

---

### 记忆健康度

```bash
# 待实现：/si:status 命令
python3 si_status.py

# 输出示例:
# 记忆文件数：47
# 总行数：493
# 已提升数：15
# 陈旧率：0%
# 健康度：95%
```

---

## 🔗 相关链接

- **技能文档**: `skills/self-improvement-core/commands/si-review/SKILL.md`
- **技能文档**: `skills/self-improvement-core/commands/si-promote/SKILL.md`
- **提升日志**: `docs/PROMOTE-LOG.md`
- **测试报告**: `docs/SI-COMMANDS-TEST-REPORT-2026-04-22.md`

---

**创建者**: OpenClaw Assistant  
**创建时间**: 2026-04-22 11:20  
**状态**: ✅ 完成
