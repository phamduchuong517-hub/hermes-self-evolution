# ⚡ Token Optimization v2.6.0 - Token 优化技能 (上下文压缩 + 模型路由 + 级联故障转移 + 智能摘要替换 + TokenJuice 三层规则覆盖版)
name: token-optimization
description: Token 优化技能 v2.6 - 上下文压缩 + 智能缓存 + 流式输出 + 会话管理 (50KB→8KB) + Provider Profile 模型路由 + cost-based routing + OpenRouter 缓存 + Context Budget + 健康检查 + 级联故障转移 + Trajectory式智能摘要替换 + TokenJuice 三层规则覆盖，减少 50%+ Token 使用，响应时间 10 秒→5 秒
version: 2.6.0
type: 性能优化
priority: 🟡 高
source: token-optimization v2.5 + tinyhumansai/openhuman TokenJuice (三层规则覆盖)
upgrade: v2.6 注入 TokenJuice 三层规则覆盖 (内置/用户/项目规则叠加) + /opt:rules 命令 + 规则优先级继承 | v2.5 注入 级联故障转移 + 场景化切换策略 + Trajectory式智能摘要替换 (保护首尾→压缩中间→LLM摘要) | v2.0 会话管理(50KB→8KB) + 预算控制 + Provider Profile | v1.0 基础压缩
---

# ⚡ Token Optimization v2.0 - Token 优化技能 (模型路由 + 会话管理增强版)

**减少 50%+ Token 使用，响应时间 10 秒→5 秒 — 会话管理 + 智能路由 + 预算控制**

---

## 核心能力

### -2. TokenJuice 三层规则覆盖 (v2.6 新注入) ⭐⭐⭐

**集成来源**: tinyhumansai/openhuman TokenJuice (vincentkoc/tokenjuice 移植, GNU GPL3)

**核心思路**: OpenHuman 的 TokenJuice 在工具输出进入 LLM 前插一层规则覆盖, 实现分类→匹配→精简。我们在已有会话压缩基础上吸收这个**规则分层+策略映射**设计。

```bash
/opt:rules                      # 查看所有激活规则
/opt:rules --builtin            # 查看内置规则
/opt:rules --user               # 查看用户自定义规则
/opt:rules --project            # 查看项目级规则
/opt:rules --match "git diff"   # 测试某工具输出匹配哪些规则
/opt:rules add --tool "git diff" --strategy "summary"  # 添加规则
/opt:rules remove --tool "cargo build"                  # 删除规则
```

**三层规则覆盖** (按层叠加, 后层覆盖前层):

| 层 | 位置 | 用途 |
|----|------|------|
| 🏗 Builtin | 技能内置 | git/npm/cargo/docker/ls 等常用命令的默认规则 |
| 👤 User | `~/.config/tokenjuice/rules/` | 用户全局覆盖 |
| 📁 Project | `.tokenjuice/rules/` (项目内) | 项目级规则, 可团队共享 |

**规则结构**:
```json
{
  "tool_pattern": "git diff",
  "strategy": "summary",        // truncate | dedup | fold | drop_regex | summary | passthrough
  "max_lines": 20,
  "max_tokens": 500,
  "drop_regex": ["^index ", "^@@"],
  "summary_prompt": "只返回文件变更摘要, 不要细节"
}
```

**策略类型**:
| 策略 | 效果 | 适用场景 |
|------|------|----------|
| `truncate` | 截断到 max_lines/tokens | 长列表、日志 |
| `dedup` | 去重连续重复行 | 循环输出、进度条 |
| `fold` | 合并空白/wrap | 格式化输出 |
| `drop_regex` | 删除匹配行 | git diff header、时间戳 |
| `summary` | LLM 摘要 (用廉价模型) | git diff、长报错 |
| `passthrough` | 不压缩 | 小输出、错误信息 |

**与现有压缩的配合**:
- 会话管理 (50KB→8KB): 粗粒度, 按文件级别
- 智能摘要替换 (Trajectory): 按轮次
- **TokenJuice**: 按工具调用级别, 最细粒度
- 三层互补: 会话级 → 轮次级 → 调用级

**规则匹配流程**:
```
工具输出
   │
   ▼
分类器 (工具名 + 参数模式)
   │
   ▼
匹配规则链: builtin → user → project
   │  (project 覆盖 user, user 覆盖 builtin)
   ▼
执行策略 (truncate/dedup/...)
   │
   ▼
压缩后的输出 → LLM 上下文
```

**预期效果**: 在现有 50KB→8KB 基础上再减少工具调用层 20-40% token (取决于工具类型)

---

### -1. 会话管理优化 (v2.0 新注入) ⭐⭐⭐

**集成来源**: smartpeopleconnected/openclaw-token-optimizer Session Management + Context Analysis

```bash
/opt:analyze                    # 当前配置分析 + 优化机会
/opt:session                    # 查看会话上下文大小
/opt:session --trim             # 精简当前会话到 8KB
/opt:session --dump             # 按大小排序所有源文件
```

**上下文瘦身策略** (50KB → 8KB):

| 文件 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| SOUL.md | 15KB | 3KB | 80% |
| USER.md | 8KB | 2KB | 75% |
| MEMORY.md | 20KB | 2KB (仅摘要) | 90% |
| 历史消息 | 7KB | 1KB (仅最近) | 85% |
| **总计** | **50KB** | **8KB** | **84%** |

**规则**:
- 启动时仅加载 SOUL.md + USER.md + MEMORY.md 摘要
- 历史消息按需加载 (仅当用户引用时才加载完整历史)
- 每日记忆文件取代完整历史回溯
- 文件超过 10KB 自动生成摘要

### -0.5 健康检查 + 验证 (v2.0 新注入) ⭐⭐

```bash
/opt:health                     # 全面健康检查
/opt:verify                     # 验证所有优化是否生效
/opt:health --report            # 生成优化状态报告
```

**健康检查项**:
- ✅ 模型路由已配置 (default = cheap)
- ✅ 工作空间文件 < 10KB
- ✅ 日预算已设置 ($5)
- ✅ Prompt 缓存功能已启用
- ✅ 会话上下文 < 10KB
- ✅ 日志保留策略合理

---

### 0. Provider Profile 模型路由 (v2.0 新注入) ⭐⭐⭐

**集成来源**: Hermes Agent v0.13.0 ProviderPlugin + Model Router

```bash
/opt:profile                    # 查看 Provider Profile
/opt:route "翻译这段文字"       # 测试路由决策
/opt:route --cheap             # 强制使用经济模型
/opt:route --premium           # 强制使用高性能模型
/opt:route --dry-run           # 预览路由结果（不执行）
```

**路由决策引擎**:
```
╔══════════════════════════════════════╗
║          Model Router                ║
║   ┌──────────────────────────┐       ║
║   │ 任务分析                  │       ║
║   │ ├── Complexity Score (1-10)│       ║
║   │ ├── Required Capabilities │       ║
║   │ └── Context Budget Needed │       ║
║   └──────────┬───────────────┘       ║
║              ▼                        ║
║   ┌──────────────────────────┐       ║
║   │ 模型选择                  │       ║
║   │ ├── Cost Score           │       ║
║   │ ├── Context Capacity     │       ║
║   │ ├── Capability Match     │       ║
║   │ └── Latency Requirement  │       ║
║   └──────────┬───────────────┘       ║
║              ▼                        ║
║   ┌──────────────────────────┐       ║
║   │ 最优模型决策              │       ║
║   └──────────────────────────┘       ║
╚══════════════════════════════════════╝
```

**模型分级**:
| 级别 | 模型 | 成本/Tok | 适用场景 |
|------|------|----------|----------|
| 🟢 Free | Qwen-Turbo | $0.0 | 简单问答/翻译 |
| 🟡 Cheap | DeepSeek-Chat | $0.15/M | 常规任务/搜索 |
| 🟠 Medium | Qwen3.5-Plus | $0.5/M | 写作/分析 |
| 🔴 Premium | Qwen3.6-Plus | $1.5/M | 复杂创作/代码 |

### 0.5 Cost-based Routing (v2.0 新注入) ⭐⭐⭐

```bash
/opt:cost                       # 查看当前会话成本
/opt:cost --daily               # 查看日成本
/opt:cost --budget "daily=5.0"  # 设置日预算 $5
/opt:cost --alert "80%"         # 预算 80% 时告警
```

**预算分配**:
```yaml
budget:
  daily: 5.0                    # 每日 $5
  warning_threshold: 0.8        # 80% 预警
  critical_threshold: 0.95      # 95% 紧急
  
  # 模型切换规则
  rules:
    - budget_percent < 50: [premium, medium, cheap]  # 全模型可用
    - budget_percent < 80: [medium, cheap]            # 砍掉 premium
    - budget_percent < 95: [cheap]                    # 仅经济模型
    - budget_percent >= 95: [free]                    # 仅免费模型
```

### 0.6 OpenRouter 响应缓存 (v2.0 新注入) ⭐⭐

```bash
/opt:cache                      # 查看缓存状态
/opt:cache --enable             # 启用 OpenRouter 缓存
/opt:cache --clear              # 清空缓存
/opt:cache --stats              # 缓存统计
```

**缓存策略**:
- 相同 Prompt + 相同模型 → 命中缓存
- TTL: 1 小时
- 仅缓存幂等请求（翻译/格式化/简单问答）
- 创作类请求不缓存

### 0.7 CC-Switch 精炼吸收：级联故障转移 (v2.5 新注入) ⭐⭐

**吸收来源**: farion1231/cc-switch (906⭐)

**必要性判定**:
- ✅ **中**: 级联故障转移 (主→中继→备用) — 已有Provider路由但缺少故障降级链
- ❌ **低 → 跳过**: Provider代理路由表 (在OpenClaw环境可用性有限)
- ❌ **低 → 跳过**: 多模型一键切换 (路由引擎已有)

**级联故障转移**:
```
请求 → 主模型(DeepSeek-Chat)
         ↓ 403/429/500?
         → 中继模型(Qwen3.5-Plus)
              ↓ 失败?
              → 备用模型(Qwen3.6-Plus)
                   ↓ 均失败
                   → 返回错误 + Provider+建议
```

```bash
/opt:switch --fallback on      # 开启故障转移
/opt:switch --fallback-off     # 关闭
/opt:switch --fallback-status  # 查看故障转移状态
```

**切换策略**:
| 场景 | 推荐模型 | 路由方式 |
|------|----------|----------|
| 快速问答 | DeepSeek-Chat | 直接 (最快) |
| 编码任务 | Qwen-Coder-Plus | 直接 (专用) |
| 写作任务 | Qwen3.6-Plus | 直接 (质量最高) |
| 主模型不可用 | 自动降级 | 级联故障转移 |
| 预算紧张 | DeepSeek-Chat | 强制廉价路由 |

---

### 0.8 Context Budget 分配器 (v2.0 新注入) ⭐⭐

```bash
/opt:budget                     # 查看当前 Context Budget
/opt:budget --set "context=2000, response=1500"  # 手工分配
/opt:budget --auto              # 自动分配
```

**自动分配策略**:
```
总预算: 4000 tokens
├── System Prompt: 500 tokens (固定)
├── Context History: 按复杂度和模型动态
│   ├── 简单任务: 500 tokens
│   ├── 常规任务: 1000 tokens
│   └── 复杂任务: 2000 tokens
├── Active Tools: 300 tokens (固定)
├── Memory Context: 500 tokens (固定)
└── Response Budget: 剩余
```

---

### 0.9 Trajectory 式智能摘要替换 (v2.5 新注入) ⭐⭐⭐

**吸收来源**: Hermes Agent trajectory_compressor.py (1462行Python) 的训练轨迹压缩策略

**原理**: Hermes 的压缩策略专为训练信号优化, 但其'保护首尾→压缩中间→摘要替换'模式直接适用于实时会话瘦身。

```bash
/opt:compress                   # 智能压缩当前会话
/opt:compress --aggressive      # 激进模式 (保护更少)
/opt:compress --conservative    # 保守模式 (保护更多)
/opt:compress --stats           # 查看压缩统计
```

**策略细节**:
```
1. 保护首尾:
   - system prompt 不压缩 (完整保留)
   - 最后 N 轮对话不压缩 (当前上下文)
   - 第1次工具结果不压缩 (建立上下文)

2. 压缩中间:
   - 只处理中间轮次 (非首/非尾)
   - 从第2次工具结果开始压缩
   - 只压缩到必要程度 (满足预算即可)

3. 摘要替换:
   - 压缩区域 → 替换成单条human摘要消息
   - 替换后保持结构化完整性
   - 附加通知: "一些早期工具结果已被压缩以节省上下文"
```

**与原有压缩的关系**:
| 原有压缩 | 智能摘要替换 | 两者配合 |
|----------|------------|---------|
| 按大小截断 (50KB→8KB) | 按轮次保留语义 | 先摘要再精简 |
| 移除冗余 | 替换为摘要 | 摘要+去重 |
| 不考虑时间顺序 | 保护最近轮次 | 新旧交织更合理 |
| 简单剪枝 | LLM摘要 (可选) | 灵活切换 |

**配置**:
```yaml
intelligent_compression:
  enabled: false                 # 默认关闭 (保守策略)
  protect_first_system: true
  protect_first_human: true
  protect_first_tool: true
  protect_last_turns: 4          # 最后 N 轮不压缩
  use_llm_summary: false         # 使用LLM做摘要? (增token)
  summary_model: deepseek-chat   # 摘要用廉价模型
  summary_target_tokens: 750     # 摘要目标大小
```

**预期效果**: 在同等上下文预算下, 保留更完整的语义连续性, 减少信息丢失。

### 2. 智能缓存
```
缓存内容:
1. 常用回复
   - 问候语
   - 常见问题回复
   - 标准流程

2. 搜索结果
   - 用户画像
   - 核心需求
   - 常用工具

3. 工具执行结果
   - 文件读取
   - 命令执行
   - API 调用
```

### 3. 流式输出
```
流式策略:
1. 边生成边输出
   - 减少等待时间
   - 提升用户体验

2. 分块输出
   - 按段落分块
   - 按逻辑分块

3. 优先级输出
   - 关键信息优先
   - 结论优先
```

---

## 工作流程

### 上下文压缩流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 收集上下文                                          │
│     - 对话历史                                          │
│     - 用户信息                                          │
│     - 工具结果                                          │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  2. 去重                                                │
│     - 移除重复内容                                      │
│     - 合并相似内容                                      │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  3. 筛选                                                │
│     - 保留关键信息                                      │
│     - 移除无关信息                                      │
│     - 优先级排序                                        │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  4. 压缩                                                │
│     - 长文本→摘要                                       │
│     - 对话→要点                                         │
│     - 日志→结论                                         │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  5. 输出                                                │
│     - 压缩后的上下文                                    │
│     - Token 统计                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 上下文压缩策略

### 策略 1: 对话历史压缩

```python
def compress_conversation_history(history, max_tokens=1000):
    """压缩对话历史"""
    
    # 1. 提取关键对话
    key_dialogs = []
    for dialog in history:
        if is_key_dialog(dialog):
            key_dialogs.append(dialog)
    
    # 2. 生成摘要
    if len(key_dialogs) > 10:
        # 只保留最近 10 轮
        key_dialogs = key_dialogs[-10:]
    
    # 3. 压缩每轮对话
    compressed = []
    for dialog in key_dialogs:
        summary = summarize_dialog(dialog, max_tokens=100)
        compressed.append(summary)
    
    return compressed
```

### 策略 2: 用户信息压缩

```python
def compress_user_info(user_profile):
    """压缩用户信息"""
    
    # 只保留核心字段
    compressed = {
        'scenario': user_profile['scenario'],  # 个人/企业
        'budget': user_profile['budget'],      # 免费/付费
        'core_needs': user_profile['core_needs'][:3],  # 前 3 个需求
        'avoid': user_profile['avoid'][:3]     # 前 3 个不需要
    }
    
    return compressed
```

### 策略 3: 工具结果压缩

```python
def compress_tool_result(result, max_tokens=500):
    """压缩工具执行结果"""
    
    # 1. 提取关键信息
    key_info = extract_key_info(result)
    
    # 2. 如果超长则摘要
    if count_tokens(key_info) > max_tokens:
        key_info = summarize(key_info, max_tokens)
    
    # 3. 移除技术细节
    key_info = remove_technical_details(key_info)
    
    return key_info
```

---

## 智能缓存策略

### 缓存配置

```yaml
cache:
  enabled: true
  
  # 缓存内容
  content:
    - common_replies      # 常用回复
    - search_results      # 搜索结果
    - tool_results        # 工具结果
  
  # 缓存 TTL
  ttl:
    common_replies: 86400    # 24 小时
    search_results: 3600     # 1 小时
    tool_results: 300        # 5 分钟
  
  # 最大缓存数
  max_size:
    common_replies: 100
    search_results: 50
    tool_results: 20
```

### 缓存操作

```python
# 缓存回复
def cache_reply(query, reply):
    key = generate_key(query)
    cache.set(key, {
        'reply': reply,
        'timestamp': now(),
        'ttl': 86400,
        'hit_count': 0
    })

# 读取缓存
def get_cached_reply(query):
    key = generate_key(query)
    cached = cache.get(key)
    
    if cached and not is_expired(cached):
        cached['hit_count'] += 1
        return cached['reply']
    
    return None

# 缓存统计
def get_cache_stats():
    total = 0
    hits = 0
    for key in cache.keys():
        item = cache.get(key)
        total += 1
        hits += item['hit_count']
    
    return {
        'total_items': total,
        'total_hits': hits,
        'hit_rate': hits / total if total > 0 else 0
    }
```

---

## 流式输出策略

### 流式配置

```yaml
streaming:
  enabled: true
  
  # 分块大小
  chunk_size: 200  # 每块 200 tokens
  
  # 输出间隔
  interval: 0.1    # 0.1 秒
  
  # 优先级
  priority:
    - conclusion    # 结论优先
    - key_points    # 要点次之
    - details       # 细节最后
```

### 流式输出

```python
async def stream_output(content):
    """流式输出内容"""
    
    # 1. 分块
    chunks = split_into_chunks(content, chunk_size=200)
    
    # 2. 按优先级排序
    sorted_chunks = sort_by_priority(chunks)
    
    # 3. 流式输出
    for chunk in sorted_chunks:
        yield chunk
        await asyncio.sleep(0.1)  # 间隔 0.1 秒
```

---

## Token 统计

### 统计方法

```python
def count_tokens(text):
    """统计 Token 数"""
    # 中文：1 字≈1.5 tokens
    # 英文：1 词≈1 token
    
    chinese_chars = count_chinese_chars(text)
    english_words = count_english_words(text)
    
    total_tokens = chinese_chars * 1.5 + english_words
    
    return total_tokens
```

### Token 预算

```yaml
token_budget:
  # 每次对话总预算
  per_conversation: 4000
  
  # 分配
  allocation:
    context: 2000      # 上下文
    response: 1500     # 回复
    buffer: 500        # 缓冲
  
  # 优化目标
  target:
    context: 1000      # 压缩后
    response: 1000     # 精简后
    savings: 50%       # 节省 50%
```

---

## 使用示例

### 示例 1: 对话历史压缩

```python
history = load_conversation_history()

compressed = compress_conversation_history(history)

```

### 示例 2: 缓存常用回复

```python
reply = generate_reply("你好")
cache_reply("你好", reply)

for i in range(9):
    cached = get_cached_reply("你好")
    # 直接使用缓存

```

### 示例 3: 流式输出

```python

async for chunk in stream_output(response):
    send_to_user(chunk)
    # 用户立即看到内容

```

---

## 性能监控

### 监控指标

```python
metrics = {
    # Token 使用
    'total_tokens': count_total_tokens(),
    'avg_tokens_per_request': avg_tokens(),
    'token_savings': calculate_savings(),
    
    # 缓存性能
    'cache_hit_rate': cache_hits / total_requests,
    'cache_size': cache.size(),
    
    # 响应时间
    'avg_response_time': avg_time(),
    'p95_response_time': p95_time(),
    
    # 压缩效果
    'compression_ratio': original_size / compressed_size
}
```

### 性能目标

```yaml
targets:
  token_savings: 0.5        # 节省 50%
  cache_hit_rate: 0.5       # 缓存命中率>50%
  avg_response_time: 5.0    # 平均响应<5 秒
  compression_ratio: 0.5    # 压缩率 50%
```

---

## 配置选项

```yaml
token_optimization:
  enabled: true
  
  # 上下文压缩
  compression:
    enabled: true
    max_context_tokens: 1000
    compression_ratio: 0.5
  
  # 智能缓存
  cache:
    enabled: true
    ttl: 3600
    max_size: 100
  
  # 流式输出
  streaming:
    enabled: true
    chunk_size: 200
    interval: 0.1
  
  # Token 预算
  budget:
    per_conversation: 4000
    alert_threshold: 0.8  # 80% 时预警
```

---

## 保存路径

```
~/.openclaw/skills/token-optimization/
├── SKILL.md                    # 本文档
├── schema.json                 # 输入输出定义
├── examples.json               # 使用示例
├── context_compressor.py       # 上下文压缩模块
├── smart_cache.py              # 智能缓存模块
├── stream_output.py            # 流式输出模块
└── token_counter.py            # Token 统计模块
```

---

## 预期效果

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| Token 使用 | 100% | 50% | -50% |
| 响应时间 | 10 秒 | 5 秒 | -50% |
| 缓存命中率 | 0% | >50% | +∞ |
| 上下文大小 | 2000 tokens | 1000 tokens | -50% |

---

## 相关技能

- [[self-improvement-core]] - 自我进化核心
- [[search-optimization]] - 搜索优化 (新创建)
- [[error-avoidance-mechanism]] - 错误避免 (新创建)

---

*Token Optimization v2.6 - 更快更省 + 智能路由 + 会话管理 + 级联故障转移 + 智能摘要替换 + TokenJuice三层规则*
*Last updated: 2026-05-22 (v2.6 OpenHuman TokenJuice融合版)*
