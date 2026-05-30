---
name: task-orchestrator
description: 任务编排器 v3.0 - 整合任务规划 + 任务执行 + 任务检查 + 自进化反思，提供完整的任务分解、调度、执行、监控、验收、反思进化能力
version: 3.0.0
source: planner-agent + executor-agent 合并 + checkmate 升级 + auto-evolution-plugin v3.0
upgrade: 添加任务完成检查 (通过/失败标准) + 会话收尾工作流 + 自进化反思机制 (任务分解/资源分配/执行过程/结果追踪)
---

# 🎯 Task Orchestrator v2.0 - 任务编排器 (任务检查增强版)

**整合自 2 个 Agent 技能**:
- planner-agent (任务规划专家)
- executor-agent (任务执行调度)

**升级亮点 (v3.0)**:
- ✅ 任务完成检查 (通过/失败标准)
- ✅ 会话收尾工作流 (自动总结)
- ✅ 心跳驱动执行 (长任务支持)
- ✅ 任务质量评分
- ✅ **自进化反思机制** (任务分解/资源分配/执行过程/结果追踪)
- ✅ **自动优化策略** (基于反思自动调整)
- ✅ **版本进化** (v3.0.0→v3.0.1→...)

---

## 核心能力

### 1. 任务规划
```
核心能力:
- 目标理解
- 任务分解
- 依赖分析
- 资源评估
- 时间估算
- 风险识别

输出:
- 任务清单
- 执行顺序
- 所需能力
- 预计时间
```

### 2. 任务执行
```
核心能力:
- 任务调度
- 技能调用
- 进度跟踪
- 错误处理
- 结果整合

执行模式:
- 顺序执行
- 并行执行
- 条件执行
- 循环执行
```

### 3. 任务监控
```
监控指标:
- 进度百分比
- 已用时间
- 剩余时间
- 成功/失败计数
- 资源使用

告警机制:
- 超时告警
- 失败告警
- 资源不足告警
```

### 4. 任务完成检查 (v2.0 新增)
```
检查机制:
- 定义通过/失败标准
- 自动验证输出质量
- 失败时自动重试或反馈

检查流程:
1. 定义验收标准 (任务开始时)
2. 执行任务
3. 验证输出是否符合标准
4. 通过→完成任务 / 失败→重试或反馈

质量标准:
- 完整性检查 (所有子任务完成)
- 正确性检查 (输出符合预期)
- 时效性检查 (在截止时间内)
```

### 5. 会话收尾工作流 (v2.0 新增)
```
收尾流程:
1. 汇总本次会话完成的任务
2. 提取关键决策和经验
3. 更新记忆系统
4. 生成会话总结
5. 准备下次会话上下文

自动执行:
- 提交未推送的代码
- 提取学习要点
- 检测模式并固化规则
- 应用自我改进
```

---

## 工作流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 接收任务                                            │
│     - 理解用户目标                                      │
│     - 识别任务类型                                      │
│     - 评估复杂度                                        │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  2. 任务分解                                            │
│     - 拆解为子任务                                      │
│     - 识别依赖关系                                      │
│     - 标注能力类型                                      │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  3. 任务规划                                            │
│     - 确定执行顺序                                      │
│     - 分配执行者 (技能/Agent)                           │
│     - 估算时间                                          │
│     - 识别风险                                          │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  4. 任务执行                                            │
│     - 按顺序调用技能                                    │
│     - 跟踪进度                                          │
│     - 处理错误                                          │
│     - 记录日志                                          │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  5. 结果整合                                            │
│     - 收集各步骤结果                                    │
│     - 整合为最终输出                                    │
│     - 质量检查                                          │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  6. 任务完成                                            │
│     - 返回结果                                          │
│     - 记录经验                                          │
│     - 更新状态                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 输入 Schema

```json
{
  "type": "object",
  "required": ["goal"],
  "properties": {
    "goal": {
      "type": "string",
      "description": "用户目标"
    },
    "constraints": {
      "type": "array",
      "items": { "type": "string" },
      "description": "约束条件"
    },
    "deadline": {
      "type": "string",
      "description": "截止时间 (可选)"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high", "urgent"],
      "default": "medium",
      "description": "优先级"
    },
    "acceptance_criteria": {
      "type": "array",
      "items": { "type": "string" },
      "description": "验收标准 (v2.0 新增)"
    },
    "options": {
      "type": "object",
      "properties": {
        "parallel": { "type": "boolean", "default": false },
        "retry_on_failure": { "type": "boolean", "default": true },
        "max_retries": { "type": "number", "default": 3 },
        "timeout_per_task": { "type": "number", "default": 300 }
      }
    }
  }
}
```

---

## 输出 Schema

```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "goal": { "type": "string" },
    "plan": {
      "type": "object",
      "properties": {
        "tasks": { "type": "array" },
        "total_tasks": { "type": "number" },
        "estimated_time": { "type": "number" }
      }
    },
    "execution": {
      "type": "object",
      "properties": {
        "completed": { "type": "number" },
        "failed": { "type": "number" },
        "progress": { "type": "number" },
        "results": { "type": "array" }
      }
    },
    "error": { "type": "string" },
    "execution_time": { "type": "number" }
  }
}
```

---

## 任务分解示例

### 示例 1: 研究任务

**用户目标**: "研究这个项目并生成报告"

**任务分解**:
```
1. 需求分析 (能力：analysis)
   - 明确研究目标
   - 确定研究范围

2. 信息收集 (能力：research)
   - L1: memory_search
   - L2: grep workspace
   - L3: grep logs
   - L4: sessions_history

3. 数据分析 (能力：analysis)
   - 数据清洗
   - 数据统计
   - 趋势分析

4. 报告生成 (能力：writing)
   - 结构化大纲
   - 内容撰写
   - 格式调整

5. 质量审查 (能力：review)
   - 准确性检查
   - 完整性检查
   - 格式检查
```

### 示例 2: 内容创作任务

**用户目标**: "把这个文章转成播客和 PPT"

**任务分解**:
```
1. 内容分析 (能力：analysis)
   - 提取核心观点
   - 识别关键信息

2. 播客脚本创作 (能力：writing)
   - 转换为对话体
   - 添加主持人互动

3. PPT 大纲设计 (能力：design)
   - 确定页数
   - 设计布局

4. 播客生成 (能力：creative-core)
   - 语音合成
   - 音频处理

5. PPT 生成 (能力：creative-core)
   - 幻灯片制作
   - 图片生成

6. 质量审查 (能力：review)
   - 播客试听
   - PPT 预览
```

### 示例 3: 数据处理任务

**用户目标**: "分析这个 Excel 文件并生成可视化报告"

**任务分解**:
```
1. 数据读取 (能力：data-processing-core)
   - 读取 Excel 文件
   - 验证数据完整性

2. 数据清洗 (能力：data-processing-core)
   - 去除空值
   - 修复格式
   - 数据类型转换

3. 数据分析 (能力：research-core)
   - 统计摘要
   - 趋势分析
   - 相关性分析

4. 图表生成 (能力：visual-core)
   - 选择合适的图表类型
   - 生成图表

5. 报告撰写 (能力：writing)
   - 分析结果描述
   - 洞察提取
   - 建议提出

6. 报告整合 (能力：assembly)
   - 整合文字 + 图表
   - 格式调整
```

---

## 执行模式

### 1. 顺序执行
```python
orchestrator = TaskOrchestrator(mode='sequential')

tasks = [
    {'name': '任务 1', 'skill': 'skill-a'},
    {'name': '任务 2', 'skill': 'skill-b'},
    {'name': '任务 3', 'skill': 'skill-c'}
]

# 按顺序执行：任务 1 → 任务 2 → 任务 3
result = await orchestrator.execute(tasks)
```

### 2. 并行执行
```python
orchestrator = TaskOrchestrator(mode='parallel')

tasks = [
    {'name': '任务 1', 'skill': 'skill-a'},
    {'name': '任务 2', 'skill': 'skill-b'},
    {'name': '任务 3', 'skill': 'skill-c'}
]

# 并行执行：任务 1 + 任务 2 + 任务 3
result = await orchestrator.execute(tasks)
```

### 3. 条件执行
```python
orchestrator = TaskOrchestrator(mode='conditional')

tasks = [
    {'name': '任务 1', 'skill': 'skill-a'},
    {
        'name': '任务 2',
        'skill': 'skill-b',
        'condition': lambda r: r['success']
    },
    {
        'name': '任务 3',
        'skill': 'skill-c',
        'condition': lambda r: not r['success']
    }
]

# 任务 1 成功 → 执行任务 2，否则执行任务 3
result = await orchestrator.execute(tasks)
```

### 4. 循环执行
```python
orchestrator = TaskOrchestrator(mode='loop')

tasks = [
    {'name': '处理批次', 'skill': 'data-processor'},
]

# 循环执行直到完成所有批次
result = await orchestrator.execute(
    tasks,
    loop_condition=lambda r: r['has_more']
)
```

---

## 错误处理

### 重试机制
```python
orchestrator = TaskOrchestrator(
    retry=3,              # 最多重试 3 次
    retry_delay=2,        # 重试间隔 2 秒
    retry_on=['timeout', 'network_error']
)
```

### 回滚机制
```python
orchestrator = TaskOrchestrator(rollback=True)

# 如果任务失败，自动回滚已完成的任务
result = await orchestrator.execute(tasks)
```

### 降级机制
```python
orchestrator = TaskOrchestrator(fallback=True)

# 如果主技能失败，使用备用技能
tasks = [
    {
        'name': '搜索',
        'skill': 'deep-search',
        'fallback': 'web-search-pro'
    }
]
```

---

## 进度跟踪

### 实时进度
```python
orchestrator = TaskOrchestrator(progress_callback=on_progress)

async def on_progress(current, total, task_name, status):
    print(f"进度：{current}/{total} - {task_name}: {status}")

await orchestrator.execute(tasks)
```

### 进度报告
```json
{
  "total_tasks": 5,
  "completed": 3,
  "failed": 0,
  "in_progress": 1,
  "pending": 1,
  "progress_percentage": 60,
  "estimated_remaining": "2 分钟"
}
```

---

## 使用示例

### 示例 1: 简单任务
```python
orchestrator = TaskOrchestrator()

result = await orchestrator.run(
    goal="搜索关于写作技巧的资料",
    constraints=["只搜索中文资料"],
    priority="high"
)

print(f"找到 {result['found_count']} 篇相关文章")
```

### 示例 2: 复杂任务
```python
orchestrator = TaskOrchestrator()

result = await orchestrator.run(
    goal="分析销售数据并生成可视化报告",
    constraints=[
        "使用 2026 年数据",
        "包含月度趋势",
        "生成 PPT 格式"
    ],
    deadline="2026-03-25 18:00",
    priority="high",
    options={
        'parallel': True,
        'retry_on_failure': True
    }
)

# 下载报告
download_link = result['report_url']
```

### 示例 3: 定时任务
```python
orchestrator = TaskOrchestrator()

# 每天 9:00 执行
orchestrator.schedule(
    goal="检查系统状态并发送日报",
    cron="0 9 * * *",
    target="qqbot:c2c:user123"
)
```

---

## 保存路径

```
~/.openclaw/skills/system/task-orchestrator/
├── SKILL.md                    # 本文档
├── schema.json                 # 输入输出定义
├── examples.json               # 使用示例
└── task_orchestrator.py        # 核心实现
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-24 | 初始版本 (合并 planner-agent + executor-agent) |

---

## 相关技能

- [[skill-coordinator]] - 技能协调器
- [[self-improvement-core]] - 自我进化核心
- [[skill-lifecycle-manager]] - 技能生命周期管理

---

*Task Orchestrator v1.0 - 智能任务编排引擎*
*Last updated: 2026-03-24*
