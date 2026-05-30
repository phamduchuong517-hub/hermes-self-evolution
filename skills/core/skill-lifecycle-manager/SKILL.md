---
name: skill-lifecycle-manager
description: 技能生命周期管理器 (v3.1 事件总线增强版) - 整合技能创建 + 自主选择 + 自主生成 + 技能补全 + 技能工厂 + 3 专精评估 Agent + 5 轴评分 + TDD 基线 + 5 种架构模式 + 事件总线信号
version: 3.1.0
source: selector-agent + skill-completer + skill-generator-pro + skill-factory-master + autonomous-skill-generation + Skill Conductor 评估体系 (Grader/Comparator/Analyzer) + 5 轴评分 + 5 架构模式 + TDD 基线 + tinyhumansai/openhuman 事件总线 (2026-05-22)
upgrade: 新增事件总线模块 (event-bus.py) + 12 种标准信号定义 + 文件轮询通信模式，使 skill-lifecycle-manager 支持跨组件事件驱动
---

# 🛠️ Skill Lifecycle Manager v3.0 - 技能生命周期管理器 (专业评估版)

**整合自 5 个 Agent 技能 + Skill Conductor 评估体系 (2026-05-17 吸收)**:

**基础引擎**:
- selector-agent (技能选择专家)
- skill-completer (技能补全 Agent)
- skill-generator-pro (技能生成器)
- skill-factory-master (技能工厂主控)
- autonomous-skill-generation (自主技能生成)

**评估引擎 (v3.0 新增，来自 Skill Conductor)**:
- **Grader Agent** — 断言检查 + 声明提取，验证每次执行是否真正完成了任务
- **Comparator Agent** — 盲 A/B 测试，不知道哪个技能产生的，消除偏见
- **Analyzer Agent** — 事后根因分析，解构胜因和败因

**依赖技能**:
- skill-creator (测试框架 + 打包发布)

---

## 核心能力

### 1. 技能发现与选择 (独有)
### 2. 技能创建与生成 (增强)
### 3. 自主技能生成
### 4. 技能补全 (独有)
### 5. 技能评估 (v3.0 大幅增强 ⭐)
### 6. 技能工厂 - GitHub 学习 (独有)
### 7. 测试与打包 (依赖 skill-creator)

### 8. 5 种架构模式预选 (v3.0 新增 ⭐)
### 9. TDD 基线验证 (v3.0 新增 ⭐)
### 10. 事件总线系统 (v3.1 新增 ⭐)

**来源**: tinyhumansai/openhuman (25K⭐) event_bus 设计模式

事件总线是轻量级的**跨组件通信机制**，基于文件轮询信号，零外部依赖。
任何 Hermes 组件（cron job、heartbeat、knowledge-memory、subconscious）都可以通过事件总线通信。

### 脚本路径

`scripts/event-bus.py`

### 信号定义 (12 种标准信号)

| 信号类型 | 优先级 | 说明 | 触发场景 |
|---------|--------|------|---------|
| `memory.ingested` | info | 新知识块被摄入 | knowledge-memory ingest |
| `memory.topic_built` | info | 主题树已更新 | knowledge-memory build-topic |
| `memory.global_digest` | info | 全局摘要已生成 | knowledge-memory global-digest |
| `error.recorded` | warn | 错误被记录 | 错误日志系统 |
| `error.repeated` | crit | 重复错误出现 | 错误检测 |
| `evolution.completed` | info | 进化循环完成 | 自我进化完成 |
| `skill.updated` | info | 技能被更新 | 技能修改 |
| `knowledge.entity_new` | info | 新实体被发现 | 知识图谱实体提取 |
| `system.heartbeat` | debug | 心跳信号 | 周期性心跳 |
| `task.pending` | info | 有待处理的任务 | Subconscious 评估 |
| `task.completed` | info | 任务完成 | 任务执行完成 |
| `task.escalated` | warn | 任务需要升级处理 | Subconscious 决策树 |

### 核心命令

```bash
# 发送信号
python3 scripts/event-bus.py emit memory.ingested '{"source":"chat","chunks":3}'

# 轮询未处理信号
python3 scripts/event-bus.py poll

# 轮询警告级以上信号
python3 scripts/event-bus.py poll --min-priority warn

# 确认信号已处理
python3 scripts/event-bus.py ack 20260522_memory_ingested_xxx

# 批量确认所有 memory 相关信号
python3 scripts/event-bus.py ack-all --type memory

# 查看统计
python3 scripts/event-bus.py stats

# 清理过期信号（默认保留 48 小时）
python3 scripts/event-bus.py cleanup --max-age 24
```

### 信号生命周期

```
emit → poll → ack → cleanup (48h TTL)

信号文件存储在 ~/.hermes/memory/signals/ 目录
未被 ack 的信号不会被 cleanup 删除
```

### 11. 5 轴评分体系 (v3.0 新增 ⭐)
## 工作流程

### 模式 A: 标准创建流程 (v3.0 增强)
```
1. 需求分析 → 2. 架构预选 (5 种模式) → 3. TDD 基线 → 4. 写技能 → 5. Evals 定义 → 6. 并行评估 (Grader + Comparator + Analyzer) → 7. 5 轴评分 → 8. 入库/迭代
```

### 模式 B: 自主生成流程
```
1. 接收需求 → 2. 需求分析 → 3. 检查是否已有 → 4. 架构预选 → 5. TDD 基线 → 6. 生成技能代码 → 7. 三阶段评估 → 8. 用户确认 → 9. 技能注入
```

### 模式 C: 技能选择流程
```
1. 理解任务 → 2. 扫描技能库 → 3. 5 轴评分匹配 → 4. 选择最佳 → 5. 准备备选
```

### 模式 D: GitHub 学习流程
```
1. 获取项目 → 2. 分析功能 → 3. 提取模块 → 4. 架构分类 → 5. 抽象能力 → 6. 生成技能 → 7. 5 轴评分 → 8. 入库
```

### 模式 E: 迭代改进流程 (v3.0 新增 ⭐)
```
1. 发现问题 → 2. 定义 evals.json → 3. 盲 A/B 对比 (旧 vs 新) → 4. Analyzer 分析胜因 → 5. 定向改进 → 6. 生成报告
```

---

## 5 种架构模式预选 (v3.0 新增 ⭐)

**来源**: Skill Conductor (smixs, 2026-05-17 吸收)

### 核心原则

**先选架构再写代码**。写错了架构重写比一开始选对贵得多。不要根据"听起来好听"选，根据技能实际做什么选。

| 模式 | 适用场景 | 反模式 |
|------|---------|--------|
| **1. Sequential Workflow** | 有依赖关系的多步骤流程 (onboarding、pipeline) | 平行执行的步骤强加顺序 |
| **2. Iterative Refinement** | 质量敏感的输出 (内容生成、报告) | 无迭代上限导致无限循环 |
| **3. Context-Aware Selection** | 同一目标可通过不同工具/方法实现 | 靠"感觉"选方法而非条件判断 |
| **4. Domain Intelligence** | 合规、专业知识、专家系统 | 先做再查规则 (违规后才被发现) |
| **5. Multi-MCP Coordination** | 工作流跨多个服务 | 单个 MCP 能搞定的场景过度设计 |

### 模式详解

#### 模式 1: Sequential Workflow
**最佳**: onboarding、流水线、多步骤过程
**关键**: 显式排序 + 步骤间依赖 + 每阶段验证 + 失败回滚
```markdown
## Step 1: [Action]
Call tool/script. Expected output: [describe success].

## Step 2: [Action]
Depends on Step 1 output. If [condition], skip to Step 3.

## Step 3: [Action]
Validate result. On failure: [rollback instructions].
```

#### 模式 2: Iterative Refinement
**最佳**: 内容生成、报告、质量敏感输出
**关键**: 显式质量标准 + 迭代上限 + 验证脚本
```markdown
## Draft
Generate initial output.

## Quality Check
Run `scripts/validate.py`. Criteria:
- [ ] Required sections present
- [ ] Data validated
- [ ] Formatting consistent

## Refine
Address each issue. Re-validate. Max iterations: 3.
```

#### 模式 3: Context-Aware Selection
**最佳**: 多种工具/方法可实现同一目标
**关键**: 清晰决策条件 + 透明度 + 兜底选项
```markdown
## Decision Tree
- If [condition A]: use approach X
- If [condition B]: use approach Y
- Default: use approach Z
```

#### 模式 4: Domain Intelligence
**最佳**: 合规、专业知识、专家系统
**关键**: 行动前先检查规则，而非行动后
```markdown
## Pre-flight Checks (MANDATORY before any action)
1. [ ] Check compliance rule A
2. [ ] Verify data integrity
3. [ ] Validate input constraints
```

#### 模式 5: Multi-MCP Coordination
**最佳**: 跨多个服务的工作流
**关键**: 服务编排 + 状态管理 + 错误传导
```markdown
## Orchestration Plan
1. MCP-A: Fetch data
2. MCP-B: Process data
3. MCP-C: Store result
4. Handle partial failures gracefully
```

---

## TDD 基线验证 (v3.0 新增 ⭐)

**核心**: 写技能之前先验证 Agent 在没有技能时是否能/不能处理该任务。

**为什么重要**: 如果 Agent 没有技能也能搞定——你就不需要这个技能。Skill Conductor 的做法是在并行执行技能测试的同时跑基线，而 Conductor 在写任何代码之前就跑基线。

### 执行步骤

1. **定义 Evals**: 在 `evals/evals.json` 中定义测试用例
```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户典型请求",
      "expected_output": "预期结果描述",
      "expectations": ["输出包含 X", "工具调用了 Y"]
    }
  ]
}
```

2. **跑基线**: 不用技能直接跑 eval，确认 Agent 失败
   - ❌ 基线失败 → 技能有价值，继续
   - ✅ 基线通过 → 不需要技能，或者拆错了需求

3. **写技能**: 以基线的失败模式作为指引

4. **跑技能测试**: 使用技能跑同样的 eval
   - ✅ 技能通过 → 证明技能确实填补了能力缺口
   - ❌ 技能失败 → 检查技能质量或需求定义

---

## 3 专精评估 Agent (v3.0 新增 ⭐)

**来源**: Skill Conductor (Anthropic eval engine 改进版, 2026-05-17 吸收)

### Grader Agent — 断言检查专家

**角色**: 根据执行记录和输出文件，判断每个断言是否通过。注意表面合规——文件存在但内容空也算失败。

**流程**:
1. 读取完整执行记录
2. 检查输出文件的实际内容（不只是文件名存在）
3. 对每条断言：搜索证据 → 判 PASS/FAIL → 引用具体证据
4. **提取声明**: 从输出中提取隐式声明并验证（事实声明、过程声明、质量声明）
5. **评价 Evals 本身**: 断言是否太容易满足？重要结果是否有断言覆盖？
6. 读取 user_notes.md 中的不确定性标记

**评分维度**:
| 级别 | 说明 |
|------|------|
| PASS | 有明确证据，且证据反映真正的任务完成 |
| FAIL | 无证据 / 证据矛盾 / 证据表面化 |

### Comparator Agent — 盲 A/B 测试

**角色**: 在不知道哪个技能产出的情况下（A/B 匿名），纯靠输出质量评判优劣。

**流程**:
1. 读取 A 和 B 两种输出
2. 根据 eval_prompt 生成评估框 (Content Rubric + Structure Rubric)
3. 对每项标准打分 1-5
4. 给出孰优孰劣结论 + 详细理由

**Content Rubric**:
| 标准 | 1 (差) | 3 (可接受) | 5 (优秀) |
|------|--------|-----------|---------|
| 正确性 | 重大错误 | 少量错误 | 完全正确 |
| 完整性 | 缺关键要素 | 基本完整 | 全部要素 |
| 准确性 | 显著偏差 | 微小偏差 | 全程精确 |

**Structure Rubric**:
| 标准 | 1 (差) | 3 (可接受) | 5 (优秀) |
|------|--------|-----------|---------|
| 组织性 | 混乱 | 合理组织 | 清晰逻辑结构 |
| 格式 | 不一致/破损 | 基本一致 | 专业精致 |
| 可用性 | 难以使用 | 可用但有阻力 | 易于使用 |

### Analyzer Agent — 事后根因分析

**角色**: 盲测得出胜负后，"解盲"并分析为什么胜者赢了、败者输了。

**流程**:
1. 读取盲测结果
2. 对比两个技能的 SKILL.md 和关键文件
3. 对比两个执行记录
4. 评估指令遵循度 (1-10)
5. 识别胜者的核心策略差异
6. 生成定向改进建议

**核心问题**:
- Agent 是否遵循了技能的显式指令？
- Agent 是否使用了技能提供的工具/脚本？
- 是否有错失利用技能内容的机会？
- Agent 是否添加了技能中不存在的多余步骤？
- 胜者的什么具体差异导致了更好的输出？

---

## 5 轴评分体系 (v3.0 新增 ⭐)

### 评分框架 (每轴 1-10 分)

| 轴 | 1 分 (差) | 5 分 (可接受) | 10 分 (优秀) |
|----|----------|-------------|------------|
| **Discovery** (触发能力) | 无法被正确触发 | 大部分场景可触发 | 所有场景准确触发，无漏激活或误激活 |
| **Clarity** (清晰度) | 步骤模糊、全凭猜测 | 步骤清晰但可优化 | 每一步都有明确标准、验证节点、兜底 |
| **Efficiency** (效率) | 冗余步骤多，token 浪费 | 合理但可精简 | 每一步最小化，无冗余，流式输出 |
| **Robustness** (鲁棒性) | 无法处理异常 | 常见异常有处理 | 完整错误处理 + 降级 + 回滚 + 重试 |
| **Completeness** (完整性) | 缺关键功能 | 核心功能齐全 | 核心 + 边界 + 所有预期输出都覆盖 |

### 总分评级

| 总分 | 评级 | 行动 |
|------|------|------|
| 45-50 | 🏆 **Production** | 可直接发布 |
| 35-44 | ✅ **Good** | 小修后可用 |
| 25-34 | ⚠️ **Needs Work** | 需迭代改进 |
| <25 | ❌ **Rewrite** | 架构或需求有问题，重写 |

### 评分示例

```json
{
  "skill": "my-skill",
  "scores": {
    "discovery": 8,
    "clarity": 7,
    "efficiency": 6,
    "robustness": 5,
    "completeness": 7
  },
  "total": 33,
  "rating": "⚠️ Needs Work",
  "summary": "核心功能完整但鲁棒性不足，缺少异常处理。建议增加重试逻辑和降级方案。"
}
```

---

## 输入 Schema (v3.0 增强)

```json
{
  "type": "object",
  "required": ["action"],
  "properties": {
    "action": {
      "type": "string",
      "enum": [
        "select", "create", "autonomous_create", "complete", 
        "evaluate", "evaluate_grader", "evaluate_comparator", "evaluate_analyzer",
        "analyze_github", "batch_generate", "iterate_improve", "check_baseline"
      ],
      "description": "操作类型: evaluate=完整三阶段评估; evaluate_grader/comparator/analyzer=单 Agent; iterate_improve=迭代改进循环; check_baseline=TDD 基线验证"
    },
    "evals": {
      "type": "array",
      "description": "Eval 定义 (用于 evaluate 和 check_baseline 模式)",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "number" },
          "prompt": { "type": "string" },
          "expected_output": { "type": "string" },
          "expectations": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "architecture_pattern": {
      "type": "string",
      "enum": ["sequential", "iterative", "context_aware", "domain_intelligence", "multi_mcp"],
      "description": "预选的架构模式 (v3.0 新增)"
    },
    "task": { "type": "string", "description": "任务描述" },
    "skill_requirement": { "type": "string", "description": "技能需求" },
    "github_url": { "type": "string", "description": "GitHub 项目链接" },
    "auto_mode": { "type": "boolean", "default": false, "description": "自主模式 (跳过确认)" },
    "options": { "type": "object" }
  }
}
```

---

## 自主生成模式 (新增 ⭐)

### 配置选项
```yaml
autonomous_mode:
  enabled: true
  auto_generate_code: true
  auto_generate_docs: true
  auto_generate_tests: false
  quality_check:
    enabled: true
    min_score: 0.7
  confirmation:
    required: true
    show_preview: true
  injection:
    auto_inject: false
    update_index: true
    save_to_memory: true
```

### 生成模板
- SKILL.md 模板
- schema.json 模板
- examples.json 模板
- Python/JS 代码模板

### 效率提升
- 传统方式：8 小时
- 自主生成：30 分钟
- 提升：**16 倍**

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **3.0.0** | **2026-05-17** | **大规模评估能力增强**: 融入 Skill Conductor 评估体系 (3 专精 Agent + 5 轴评分 + TDD 基线 + 5 种架构模式 + 迭代改进流程) |
| 2.1.0 | 2026-04-22 | 添加多阶段增强模式 + ROI 追踪 (基于全球新闻技能增强实战) |
| 2.0.0 | 2026-03-25 | 专家版融合 (合并 autonomous-skill-generation) |
| 1.0.0 | 2026-03-24 | 初始版本 (合并 4 个 Agent) |

---

## 吸收来源 (2026-05-17)

本版本吸收自以下 GitHub 项目:

| 项目 | Stars | 吸收内容 |
|------|-------|---------|
| **smixs/skill-conductor** | 89⭐ | 3 专精评估 Agent + 5 轴评分 + TDD 基线 + 5 架构模式 + SOP 实践 |
| **Anthropic skill-creator** (上游) | — | grader/comparator/analyzer Agent 设计模式 |
| **chopratejas/headroom** | 1,769⭐ | 可逆压缩 (CCR) 概念参考 (已记录到 token-optimization 相关技能) |

注意: skill-conductor 虽只有 89⭐，但其评估体系直接来自 Anthropic 官方 skill-creator 改进版，质量经过验证，非普通社区项目可比。

---

## 多阶段增强模式 (新增 v2.1.0 ⭐)

**来源**: 2026-04-22 全球新闻技能增强实战经验

**核心模式**:
```
阶段 1 (本周): 基础能力
- 快速见效 (4-6 小时)
- 核心缺失补齐
- 预期收益 +50%

阶段 2 (本月): 增强能力
- 中等投入 (6-8 小时)
- 可增强领域
- 预期收益 +30%

阶段 3 (下月): 完善能力
- 可选功能 (4-6 小时)
- 锦上添花
- 预期收益 +20%

总 ROI: 投入 14-20 小时，总收益 +100%
```

**ROI 追踪模板**:
```markdown
| 阶段 | 投入时间 | 预期收益 | 实际收益 | ROI |
|------|----------|----------|----------|-----|
| 阶段 1 | 4-6 小时 | +50% | +55% | ⭐⭐⭐⭐⭐ |
| 阶段 2 | 6-8 小时 | +30% | +35% | ⭐⭐⭐⭐ |
| 阶段 3 | 4-6 小时 | +20% | +25% | ⭐⭐⭐⭐ |
| **总计** | **14-20 小时** | **+100%** | **+115%** | **⭐⭐⭐⭐⭐** |
```

**实战案例**:
- 阶段 1 (向量检索): 实际 30 分钟，收益 +50%, ROI 超预期
- 阶段 2 (群体推理): 实际 1 小时，收益 +30%, ROI 超预期
- 新闻技能增强：实际 1 小时，收益 +1200% 覆盖，ROI 超预期

**关键洞察**:
- 先易后难，快速见效
- 每阶段有明确交付物
- ROI 递减时停止
- 实际用时往往远低于预期 (准备充分)

---

*Skill Lifecycle Manager v3.0 - 专业评估版完整技能生命周期管理*
*Last updated: 2026-05-17*

---

## 保存路径

```
~/.hermes/skills/openclaw-imports/skill-lifecycle-manager/
├── SKILL.md                    # 本文档 (v3.0)
├── scripts/
│   ├── grader.py               # Grader Agent — 断言检查评估
│   ├── comparator.py           # Comparator Agent — 盲 A/B 测试
│   └── analyzer.py             # Analyzer Agent — 事后根因分析
├── evals/
│   └── evals.json              # Eval 定义示例
└── README.md                   # 使用说明
```

---

## 使用方法

### 1. 定义 Evals（先）
```bash
# 编辑 evals/evals.json，定义你的测试用例

# 跑 TDD 基线（确认没有技能时确实做不了）
# 直接让 Agent 执行 eval prompt，看能否完成
```

### 2. 评估技能质量
```bash
# Grader: 检查断言通过率
python3 scripts/grader.py evals/evals.json transcript.md outputs/ --verbose

# Comparator: 盲 A/B 对比新旧版本
python3 scripts/comparator.py output_v1 output_v2 "任务描述" --dirs --verbose

# Analyzer: 分析对比结果
python3 scripts/analyzer.py comparison.json skill_v1.md skill_v2.md -tw transcript_v1.md -tl transcript_v2.md --verbose
```

### 3. 5 轴评分
使用 5 轴评分体系评估技能后，记录结果到技能文档的 `<!-- eval: {...} -->` 注释中。
