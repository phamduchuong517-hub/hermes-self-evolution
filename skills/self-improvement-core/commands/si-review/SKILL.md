# /si:review - 记忆审查命令

**功能**: 自动扫描 MEMORY.md 找出提升候选

**版本**: v1.0 (2026-04-22 创建)

**来源**: 融合 auto-memory-pro /si:review + 本地 self-improvement-core v4.0

---

## 🎯 核心能力

### 1. 重复模式识别

扫描 MEMORY.md 中重复出现的模式 (出现 3 次+)，识别提升候选：

- 重复的技术决策 (如 "使用 DeepSeek 写小说" 出现多次)
- 重复的工作流程 (如 "夜间自改进" 每日执行)
- 重复的问题解决模式 (如 "Chrome 锁文件清理")

### 2. 陈旧条目检测

识别超过 30 天未更新的记忆条目：

- 过时的配置信息
- 已完成的项目记录
- 失效的临时决策

### 3. 差距分析

对比 MEMORY.md 与 AGENTS.md/TOOLS.md/SOUL.md 的差距：

- MEMORY.md 中有但 AGENTS.md 中无的规则
- 重复出现但未固化的工作流
- 已验证但未提升的最佳实践

### 4. 生成审查报告

输出结构化审查报告：

```markdown
# 记忆审查报告 (2026-04-22)

## 📊 基础统计
- MEMORY.md 总行数：XXX
- 记忆文件数：XX
- 平均更新频率：X 天/次

## 🎯 提升候选 (X 个)

### 1. [模式名称]
- **出现次数**: X 次
- **首次出现**: 2026-XX-XX
- **最近出现**: 2026-XX-XX
- **建议提升目标**: AGENTS.md / TOOLS.md / SOUL.md
- **理由**: 重复出现 X 次，已验证有效

### 2. [模式名称]
...

## ⚠️ 陈旧条目 (X 个)

### 1. [条目名称]
- **最后更新**: 2026-XX-XX (>30 天前)
- **建议**: 归档 / 删除 / 更新

## 🔍 差距分析 (X 个)

### 1. [差距名称]
- **MEMORY.md 中有**: [内容]
- **AGENTS.md 中无**: [缺失]
- **建议**: 提升到 AGENTS.md 第 X 节

## 📋 执行建议

1. 立即提升：[X 个高优先级候选]
2. 本周内提升：[X 个中优先级候选]
3. 归档陈旧：[X 个陈旧条目]
```

---

## 📋 使用方式

### 命令格式

```bash
/si:review [--days N] [--verbose]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--days N` | 审查最近 N 天的记忆 | 30 |
| `--verbose` | 输出详细报告 | false |

### 使用示例

```bash
# 基础审查
/si:review

# 审查最近 7 天
/si:review --days 7

# 详细报告
/si:review --verbose

# 组合使用
/si:review --days 14 --verbose
```

---

## 🔧 实现架构

### 核心类

```python
class SIReviewCommand:
    """记忆审查命令"""
    
    def __init__(self):
        self.memory_path = "workspace/MEMORY.md"
        self.agents_path = "workspace/AGENTS.md"
        self.tools_path = "workspace/TOOLS.md"
        self.soul_path = "workspace/SOUL.md"
    
    def execute(self, days=30, verbose=False):
        """执行记忆审查"""
        
        # 1. 读取记忆文件
        memory_content = self.read_memory()
        
        # 2. 识别重复模式
        patterns = self.find_recurring_patterns(memory_content, min_count=3)
        
        # 3. 检测陈旧条目
        stale_entries = self.find_stale_entries(memory_content, days=30)
        
        # 4. 分析差距
        gaps = self.identify_gaps(memory_content)
        
        # 5. 生成报告
        report = self.generate_report(patterns, stale_entries, gaps, verbose)
        
        return report
    
    def find_recurring_patterns(self, content, min_count=3):
        """识别重复模式"""
        # 实现逻辑：
        # 1. 分词 + 关键词提取
        # 2. 统计模式出现频率
        # 3. 过滤低价值模式
        # 4. 返回高频模式列表
        pass
    
    def find_stale_entries(self, content, days=30):
        """检测陈旧条目"""
        # 实现逻辑：
        # 1. 解析记忆条目的时间戳
        # 2. 计算最后更新时间
        # 3. 标记超过阈值的条目
        # 4. 返回陈旧条目列表
        pass
    
    def identify_gaps(self, memory_content):
        """分析差距"""
        # 实现逻辑：
        # 1. 读取 AGENTS.md/TOOLS.md/SOUL.md
        # 2. 对比 MEMORY.md 中的内容
        # 3. 识别 MEMORY.md 中有但规则文件中无的内容
        # 4. 返回差距列表
        pass
    
    def generate_report(self, patterns, stale_entries, gaps, verbose=False):
        """生成审查报告"""
        # 实现逻辑：
        # 1. 格式化基础统计
        # 2. 列出提升候选
        # 3. 列出陈旧条目
        # 4. 列出差距分析
        # 5. 生成执行建议
        pass
```

### 辅助函数

```python
def extract_keywords(text):
    """提取关键词"""
    # 使用 TF-IDF 或 TextRank 算法
    pass

def parse_memory_entries(content):
    """解析记忆条目"""
    # 解析 Markdown 结构，提取条目和元数据
    pass

def calculate_pattern_frequency(patterns, content):
    """计算模式频率"""
    # 统计每个模式在内容中出现的次数
    pass

def compare_with_rules(memory_content, rules_files):
    """对比规则文件"""
    # 比较记忆内容与 AGENTS.md/TOOLS.md/SOUL.md
    pass
```

---

## 📊 输出示例

### 基础报告

```markdown
# 记忆审查报告 (2026-04-22)

## 📊 基础统计
- MEMORY.md 总行数：1234
- 记忆文件数：37
- 平均更新频率：1.2 天/次

## 🎯 提升候选 (5 个)

### 1. 模型路由策略
- **出现次数**: 8 次
- **首次出现**: 2026-04-16
- **最近出现**: 2026-04-22
- **建议提升目标**: TOOLS.md
- **理由**: 重复出现 8 次，已验证有效

### 2. 零用户操作规范
- **出现次数**: 12 次
- **首次出现**: 2026-04-16
- **最近出现**: 2026-04-22
- **建议提升目标**: AGENTS.md
- **理由**: 核心交互规范，需固化

...

## ⚠️ 陈旧条目 (3 个)

### 1. Chrome 浏览器配置
- **最后更新**: 2026-03-15 (>30 天前)
- **建议**: 删除 (已卸载 Chrome)

...

## 🔍 差距分析 (2 个)

### 1. GitHub 发布流程
- **MEMORY.md 中有**: 完整发布流程记录
- **AGENTS.md 中无**: 发布规范章节
- **建议**: 提升到 AGENTS.md 新增"发布流程"章节

...

## 📋 执行建议

1. 立即提升：模型路由策略、零用户操作规范
2. 本周内提升：GitHub 发布流程、写作规范
3. 归档陈旧：Chrome 浏览器配置、临时目录问题
```

### 详细报告 (--verbose)

```markdown
# 记忆审查报告 (详细版) (2026-04-22)

[基础报告内容] +

## 📝 详细内容

### 提升候选 #1: 模型路由策略

**出现上下文**:
1. 2026-04-16 09:44 - 云服务器 P1 优化对话
2. 2026-04-17 11:34 - 写作风格对话
3. 2026-04-21 13:05 - GitHub Token 配置对话
...

**原始内容**:
> 写作时用 DeepSeek，编码时用 Qwen Coder，通用时用千问 3.5

**建议提升格式**:
```markdown
## 📝 模型分工

| 场景 | 模型 | 说明 |
|------|------|------|
| 小说正文 | DeepSeek Chat | 写小说专用 |
| 编码任务 | Qwen Coder | 代码生成/审查 |
| 通用对话 | Qwen3.5-plus | 默认主模型 |
```

...
```

---

## 🔗 相关命令

| 命令 | 功能 |
|------|------|
| `/si:promote <id>` | 将审查发现的候选提升到规则文件 |
| `/si:status` | 查看记忆健康状态 |
| `/si:extract <id>` | 从模式中提取技能 |

---

## 📈 预期效果

| 指标 | 实施前 | 实施后 | 提升 |
|------|--------|--------|------|
| 记忆审查时间 | 手动 30 分钟 | 自动 30 秒 | -98% |
| 提升候选识别率 | 60% | 95% | +58% |
| 记忆质量 | 基准 | +30% | +30% |

---

**创建者**: OpenClaw Assistant  
**创建时间**: 2026-04-22 10:45  
**状态**: ✅ 设计完成，待实现
