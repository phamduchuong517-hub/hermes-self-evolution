# ⚖️ TaskBalancer v2.0.0 - 智能任务分配器 (4种负载算法 + 健康检查 + 动态缩放)
name: TaskBalancer
description: 智能任务分配和负载均衡 v2.0 - 多算法负载均衡 + 健康检查 + 动态缩放 + Worker 团队协作 + Hallucination Gate，为多 Agent 工作流提供生产级任务分发
version: 2.0.0
author: OpenClaw Community + Hermes Agent v0.13.0 Kanban + pilottai multi-agent 启发
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
upgrade: v2.0 注入多算法负载均衡 (Random/Weighted/Load-based/Least-Connections) + 健康检查 + 动态缩放 + Hermes Kanban Worker 调配 + Hallucination Gate + Retry Budgets | v1.0 基础任务分类和 Agent 能力匹配
---

# ⚖️ TaskBalancer v2.0 - 智能任务分配器 (多算法负载均衡版)

**多 Agent 工作流的任务分配和负载均衡 — 支持 4 种调配算法 + Worker 团队协作**

---

## 功能

- ⚖️ 4 种负载均衡算法
- 🔄 健康检查 (Health Check)
- 📈 动态缩放 (Dynamic Scaling)
- 🎯 Agent 能力匹配
- 🔴 Zombie 检测 + 任务回收
- 🛡️ Hallucination Gate (验证 Worker 执行真实性)
- 📊 性能监控 + 实时仪表盘

---

## 架构

```
TaskBalancer/
├── memory.md          # 任务历史统计
├── agents.md          # Agent 能力配置
├── queues/            # 任务队列
├── metrics.md         # 性能指标
└── workers/           # Worker 工作日志 (v2.0 新增)
```

---

## 核心规则

### 0. 负载均衡算法 (v2.0 新注入) ⭐⭐⭐

```bash
/balance algorithm                # 查看当前算法
/balance algorithm --set weighted  # 设置加权轮询
/balance algorithm --set least     # 设置最少连接
/balance algorithm --set load      # 设置基于负载
/balance algorithm --set random    # 设置随机分配
```

| 算法 | 原理 | 适用场景 |
|------|------|----------|
| **Weighted Round-Robin** | 按权重轮询分配 | Agent 能力不均匀 |
| **Least Connections** | 分配给活跃任务最少的 | 任务时长差异大 |
| **Load-based** | 按实时 CPU/内存负载 | 资源敏感型任务 |
| **Random** | 随机分配 | 任务同质化 |

**加权轮询实现**:
```python
def assign_weighted(agents, task):
    """加权轮询分配"""
    total_weight = sum(a.weight for a in agents)
    
    for agent in agents:
        agent.current_weight += agent.weight
    
    # 选最大权重的 Agent
    selected = max(agents, key=lambda a: a.current_weight)
    selected.current_weight -= total_weight
    
    return selected
```

### 0.5 健康检查 (v2.0 新注入) ⭐⭐

```bash
/balance health                 # 查看所有 Agent 健康状态
/balance health --check         # 手动触发健康检查
/balance health --agent worker-1  # 检查单个 Agent
/balance health --auto-interval 300  # 设置自动检查间隔
```

**健康检查项目**:
- ✅ Heartbeat: Agent 活跃状态
- ✅ API Reachable: 模型接口可达
- ✅ Resource OK: CPU/Memory 未过载
- ✅ Queue Depth: 队列未溢出

### 0.6 Zombie 检测 + Hallucination Gate (v2.0 新注入) ⭐⭐⭐

**集成来源**: Hermes Agent v0.13.0 Durable Kanban

```bash
/balance zombies                  # 列出僵尸 Worker
/balance reclaim <zombie-id>     # 回收僵尸任务
/balance verify <worker-id>      # 验证 Worker 完成真实性
/balance budges                  # 查看 Retry Budgets
```

**Zombie 检测**: Worker 超时无心跳 → 标记为 Zombie → 回收任务 → 重新分配
**Hallucination Gate**: 验证 Worker 的完成声明 → 文件/结果真实存在 → 否则回滚

### 0.7 动态缩放 (v2.0 新注入) ⭐⭐

```bash
/balance scale                    # 查看当前缩放状态
/balance scale --up 2             # 扩展 2 个 Worker
/balance scale --down 1           # 缩容 1 个 Worker
/balance scale --auto             # 启用自动缩放
```

**自动缩放规则**:
- 队列深度 > 10 → 扩展 1 个 Worker
- 队列深度 < 2 + 空闲 Worker > 2 → 缩容 1 个
- 最大 Worker: 10 (可配置)
- 最小 Worker: 1

---

## 使用方法

```bash
# 分配任务
/balance assign <task> --priority <high|medium|low>

# 查看负载
/balance status

# 查看队列
/balance queue

# 管理 Worker
/balance workers                  # 查看所有 Worker
/balance workers --add "writer"   # 添加 Worker
/balance workers --remove "coder" # 移除 Worker
```

---

## API 示例

### 加权分配
```python
balancer = TaskBalancer(algorithm="weighted")

# 添加 Agent（带权重）
balancer.register_agent("writer", weight=3)    # 能力高
balancer.register_agent("coder", weight=2)     # 能力中
balancer.register_agent("searcher", weight=1)  # 能力低

# 健康检查
balancer.health_check(agent="writer")
# → {"alive": true, "load": 0.5, "queue_depth": 3}

# 带 Retry Budget 分配
result = balancer.assign(
    task="写报告",
    retry_budget=3,          # 最多重试 3 次
    timeout=300,             # 5 分钟超时
    require_verification=True  # 启用 Hallucination Gate
)
```

---

## 配置

在 `agents.md` 中配置 Agent 能力：

```markdown
# Agent 能力配置

## Writer
- 能力：小说创作、文章写作
- 最大并发：3
- 权重：3 (加权轮询)
- 健康检查：✅

## Searcher
- 能力：网络搜索、信息收集
- 最大并发：5
- 权重：1
- 健康检查：✅
```

---

## 性能指标

记录在 `metrics.md`：

- 任务完成率
- 平均分配时间
- Agent 利用率
- 队列长度
- Zombie 数量
- Hallucination Gate 拦截数

---

*TaskBalancer v2.0 - 智能任务分配 (多算法负载均衡)*
