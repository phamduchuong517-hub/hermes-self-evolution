---
name: token-optimization
description: Token 优化技能 v2.1 - 上下文压缩 + 智能缓存 + 流式输出 + 内容路由压缩 + CCR 可逆压缩 + TokenJuice 三层规则覆盖 + CacheAligner，减少 60-95% Token 使用
version: 2.1.0
type: 性能优化
priority: 🟡 高
source: 原有 token-optimization + chopratejas/headroom 内容路由 + CCR 可逆压缩 + CacheAligner + tinyhumansai/openhuman TokenJuice (2026-05-22)
upgrade: 新增 TokenJuice 三层规则覆盖压缩引擎 (tokenjuice-rules.py) + 9 条内置规则（git/log/json/code/docker/ls/cargo/npm）+ 用户层和项目层自定义规则覆盖 + 匹配测试 + 压缩统计
---

# ⚡ Token Optimization v2.0 - Token 优化技能

**减少 60-95% Token 使用**

**来源**: chopratejas/headroom (1,769⭐, 2026-05-17 吸收)

---

## 核心能力

### 1. 上下文压缩
```
压缩方法:
1. 移除冗余信息
   - 重复内容去重
   - 移除无关内容
   - 精简表达

2. 保留关键内容
   - 用户偏好
   - 核心需求
   - 关键决策

3. 使用摘要代替原文
   - 长文本→摘要
   - 对话→要点
   - 日志→结论
```

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

### 4. 内容路由压缩 (v2.0 新增 ⭐)
**来源**: headroom ContentRouter

自动识别内容类型并选择最合适的压缩算法:

| 内容类型 | 压缩器 | 预期节省 |
|---------|--------|---------|
| **JSON/数组** | SmartCrusher (统计压缩) | **70-90%** |
| **代码** | CodeCompressor (AST 感知, tree-sitter) | **60-80%** |
| **文本/日志** | 统计压缩 + 去重 | **50-70%** |
| **搜索/工具输出** | 混合 (结构保持) | **70-92%** |
| **Diff** | 上下文感知压缩 | **60-80%** |

**工作流程**:
```
ContentRouter
  ├─ 检测内容类型 (正则 + 启发式)
  ├─ 选择对应压缩器
  │    ├─ JSON → SmartCrusher (保留结构，压缩值)
  │    ├─ Code → CodeCompressor (保留签名/导入/类型，压缩体)
  │    └─ Text → 统计压缩 (摘要 + 去重)
  └─ 输出 + 原始内容的 CCR 存储
```

### 5. CCR 可逆压缩 (v2.0 新增 ⭐)
**来源**: headroom Compress-Cache-Retrieve

**核心**: 压缩后的内容如果在推理中被 LLM 需要更多细节，可以随时检索原始内容。

**不删原始数据** = LLM 可以在需要时调检索获取完整版本。

```
压缩场景:
  原始: 10,144 tokens → 压缩: 1,260 tokens (节省 88%)
  LLM 觉得某段需要更多细节 → 检索 → 获取原始段落

存储结构:
  [compressed_chunk]: 压缩后的摘要/结构
  [ccr_store]: 本地 SQLite/HNSW 向量存储
     ├─ original_hash → original_content
     ├─ compressed_hash → compressed_content
     └─ metadata: {timestamp, content_type, token_count}
```

### 6. CacheAligner (v2.0 新增 ⭐)
**来源**: headroom

**核心**: 稳定前缀使 LLM 提供商的 KV 缓存能真正命中。

**原理**: 压缩后的内容每次变动前缀会导致 KV 缓存失效。CacheAligner 确保相同类型的内容使用相同的前缀结构，使缓存命中率大幅提升。

```
before: {"tools": [{"name": "search", "args": {...}}]}  ← 每次不同前缀
after:  SYSTEM_PROMPT → TOOL_HEADER → compressed_tool_output  ← 稳定前缀
                                                        ← KV 缓存命中 ↑
```

### 8. 自动化失败学习 (v2.0 新增 ⭐)
**来源**: headroom `headroom learn`

**核心**: 挖掘失败会话，自动将修正写入 AGENTS.md / 技能文档。

```
触发: 连续 2+ 次同类错误
过程:
  1. 分析失败会话模式
  2. 提取根因和修正方案
  3. 自动写入技能文档的"常见错误"或"注意事项"段落
  4. 防止同类错误重复发生
```

### 9. TokenJuice 三层规则覆盖 (v2.1 新增 ⭐⭐)

**来源**: tinyhumansai/openhuman (25K⭐) TokenJuice 设计模式

TokenJuice 是在工具输出到达 LLM 上下文之前运行的**规则覆盖层**。
与 v2.0 的 CCR 内容路由不同，TokenJuice 按工具类型预定义规则，更可配置。

**脚本路径**: `scripts/tokenjuice-rules.py`

#### 三层规则（后覆盖前）

| 层 | 路径 | 用途 |
|---|------|------|
| **Builtin** (内置) | `scripts/tokenjuice-builtin-rules.json` | git/log/json/code/docker/ls 等 9 条默认规则 |
| **User** (用户) | `~/.config/tokenjuice/rules/` | 个人配置，跨项目生效 |
| **Project** (项目) | `.tokenjuice/rules/` | 项目仓库级规则，可 git commit |

#### 9 条内置规则

| 规则 | 匹配 | 策略 | 预期节省 |
|------|------|------|---------|
| `git_status` | git status | truncate_lines(20) | 70-90% |
| `git_diff` | git diff | diff_summary(10 files) | 60-80% |
| `npm_install` | npm install | filter_lines(error/warn) | 80-95% |
| `docker_ps` | docker ps | table_compress(容器名+状态) | 50-70% |
| `ls_la` | ls -la | table_compress(大小+名称) | 40-60% |
| `json_output` | JSON | json_compact(深度3) | 60-80% |
| `log_file` | .log/.txt | log_dedup(去重连续行) | 70-90% |
| `cargo_build` | cargo build | filter_lines(error/warning) | 80-95% |
| `code_output` | def/class/fn | code_signature_only(签名保留) | 50-70% |

#### 核心命令

```bash
# 压缩文本（自动匹配规则）
echo "git status output..." | python3 scripts/tokenjuice-rules.py compress

# 压缩并显示统计
cat big-output.log | python3 scripts/tokenjuice-rules.py compress --stats

# 强制指定策略
echo "some text" | python3 scripts/tokenjuice-rules.py compress --strategy truncate_lines

# 测试匹配（看文本会匹配哪些规则）
python3 scripts/tokenjuice-rules.py match "git status -s"

# 显示规则统计
python3 scripts/tokenjuice-rules.py stats

# 创建用户自定义规则示例
python3 scripts/tokenjuice-rules.py init-user-rules
```

#### 自定义规则示例

创建 `~/.config/tokenjuice/rules/my-rules.json`：

```json
[
  {
    "id": "user_my_app_logs",
    "pattern": "myapp.*\\\\.log",
    "description": "压缩 myapp 应用日志",
    "strategy": "log_dedup",
    "params": {"max_lines": 50, "dedup_consecutive": true}
  }
]
```

#### 实现原理

```
工具输出
   │
   ▼
ContentRouter (v2.0) → 按内容类型路由压缩
   │
   ├── TokenJuice (v2.1) → 按工具/命令匹配规则
   │   ├── 内置 9 条规则
   │   ├── 用户覆盖
   │   └── 项目覆盖
   │
   ▼
CCR Store (v2.0) → 原始内容可检索
   │
   ▼
LLM 上下文
```

TokenJuice 与 ContentRouter 互补：
- ContentRouter：按**内容格式**压缩（JSON/Code/Text）
- TokenJuice：按**工具来源**压缩（git_status/log_file/docker_ps）
- 两者配合：广度+深度覆盖

---

## 工作流程 (v2.0 增强)

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
# 原始对话历史 (2000 tokens)
history = load_conversation_history()

# 压缩后 (800 tokens)
compressed = compress_conversation_history(history)

# 节省：1200 tokens (60%)
```

### 示例 2: 缓存常用回复

```python
# 第 1 次：生成回复 (消耗 500 tokens)
reply = generate_reply("你好")
cache_reply("你好", reply)

# 第 2-10 次：使用缓存 (消耗 0 tokens)
for i in range(9):
    cached = get_cached_reply("你好")
    # 直接使用缓存

# 总节省：500 * 9 = 4500 tokens
```

### 示例 3: 流式输出

```python
# 传统方式：等待全部生成后输出
# 等待时间：10 秒

# 流式方式：边生成边输出
async for chunk in stream_output(response):
    send_to_user(chunk)
    # 用户立即看到内容

# 感知等待时间：2 秒 (首块)
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
| Token 使用 | 100% | **5-40%** | **-60% 到 -95%** |
| 响应时间 | 10 秒 | 3-5 秒 | -50% 到 -70% |
| 缓存命中率 | 0% | >50% | +∞ |
| 上下文大小 | 2000 tokens | 500-1000 tokens | -50% 到 -75% |
| KV 缓存命中 | 随机 | 稳定前缀 | **+300%** |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **2.1.0** | **2026-05-22** | **新增 TokenJuice 三层规则覆盖**: tokenjuice-rules.py 脚本 + 9 条内置规则 + 用户/项目层覆盖 + ContentRouter 互补 |
| 1.0.0 | 2026-03-24 | 初始版本 (上下文压缩 + 缓存 + 流式) |

---

## 吸收来源 (2026-05-17)

| 项目 | Stars | 吸收内容 |
|------|-------|---------|
| **chopratejas/headroom** | 1,769⭐ | 内容路由压缩 + CCR 可逆压缩 + CacheAligner + headroom learn |
| **tinyhumansai/openhuman** | 25K⭐ | TokenJuice 三层规则覆盖 + 匹配-压缩管道 + 用户/项目级自定义规则 |

---

## 相关技能

- [[self-improvement-core]] - 自我进化核心
- [[search-optimization]] - 搜索优化 (新创建)
- [[error-avoidance-mechanism]] - 错误避免 (新创建)

---

*Token Optimization v1.0 - 更快更省*
*Last updated: 2026-03-24*
