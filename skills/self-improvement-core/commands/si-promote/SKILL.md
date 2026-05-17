# /si:promote - 记忆提升命令

**功能**: 将记忆提升到 AGENTS.md/TOOLS.md/SOUL.md

**版本**: v1.0 (2026-04-22 创建)

**来源**: 融合 auto-memory-pro /si:promote + 本地 self-improvement-core v4.0

---

## 🎯 核心能力

### 1. 智能目标识别

自动识别提升目标文件：

- **AGENTS.md** - 行为规范、交互原则、工作流程
- **TOOLS.md** - 工具配置、API Key、环境设置
- **SOUL.md** - 人格定义、核心价值观、身份认同

### 2. 格式转换

将 MEMORY.md 中的记忆条目转换为规则格式：

**输入 (MEMORY.md)**:
```markdown
### 模型路由策略

写作时用 DeepSeek，编码时用 Qwen Coder，通用时用千问 3.5
```

**输出 (TOOLS.md)**:
```markdown
## 📝 模型分工

| 场景 | 模型 | API Key | 说明 |
|------|------|---------|------|
| **小说正文** | DeepSeek Chat | `sk-xxx` | 写小说时用 DeepSeek |
| **日常对话** | Qwen3.5-plus | `sk-sp-xxx` | 默认主模型 |
| **编码任务** | Qwen Coder | - | 代码生成/审查 |
```

### 3. 冲突检测

检测目标文件中是否已存在类似规则：

- **完全重复** → 提示已存在
- **部分冲突** → 提示手动确认
- **互补内容** → 自动合并

### 4. 自动提升

一键将记忆提升到目标文件：

```bash
# 提升到 AGENTS.md
/si:promote 1 --target AGENTS.md

# 提升到 TOOLS.md
/si:promote 2 --target TOOLS.md

# 自动选择目标
/si:promote 1

# 批量提升
/si:promote 1,2,3 --batch
```

### 5. 清理记忆

提升后自动从 MEMORY.md 移除或标记为"已提升"：

```markdown
## ✅ 已提升 (2026-04-22 → AGENTS.md)

原记忆内容...
```

---

## 📋 使用方式

### 命令格式

```bash
/si:promote <id> [--target FILE] [--batch] [--keep]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<id>` | 记忆条目 ID (来自 /si:review 报告) | 必填 |
| `--target FILE` | 目标文件 (AGENTS.md/TOOLS.md/SOUL.md) | 自动识别 |
| `--batch` | 批量提升模式 | false |
| `--keep` | 保留原记忆 (不删除) | false |

### 使用示例

```bash
# 提升单个条目 (自动选择目标)
/si:promote 1

# 提升到指定文件
/si:promote 1 --target TOOLS.md

# 批量提升
/si:promote 1,2,3 --batch

# 提升但保留原记忆
/si:promote 1 --keep

# 预览不执行
/si:promote 1 --dry-run
```

---

## 🔧 实现架构

### 核心类

```python
class SIPromoteCommand:
    """记忆提升命令"""
    
    def __init__(self):
        self.memory_path = "workspace/MEMORY.md"
        self.agents_path = "workspace/AGENTS.md"
        self.tools_path = "workspace/TOOLS.md"
        self.soul_path = "workspace/SOUL.md"
    
    def execute(
        self,
        entry_id: int,
        target: Optional[str] = None,
        batch: bool = False,
        keep: bool = False,
        dry_run: bool = False
    ) -> str:
        """
        执行记忆提升
        
        Args:
            entry_id: 记忆条目 ID
            target: 目标文件
            batch: 批量模式
            keep: 保留原记忆
            dry_run: 预览模式
        
        Returns:
            执行结果
        """
        # 1. 读取 MEMORY.md
        memory_content = self.read_memory()
        
        # 2. 提取指定条目
        entry = self.extract_entry(memory_content, entry_id)
        
        # 3. 自动识别目标文件
        if not target:
            target = self.auto_detect_target(entry)
        
        # 4. 检测冲突
        conflicts = self.detect_conflicts(entry, target)
        
        # 5. 格式转换
        converted = self.convert_format(entry, target)
        
        # 6. 执行提升
        if not dry_run:
            self.do_promote(converted, target, conflicts)
            
            # 7. 清理记忆
            if not keep:
                self.cleanup_memory(entry_id)
        
        # 8. 返回结果
        return self.generate_result(entry_id, target, converted, conflicts, dry_run)
    
    def extract_entry(self, content: str, entry_id: int) -> Dict:
        """提取记忆条目"""
        # 实现逻辑：
        # 1. 解析 MEMORY.md 结构
        # 2. 根据 ID 定位条目
        # 3. 提取内容和元数据
        pass
    
    def auto_detect_target(self, entry: Dict) -> str:
        """自动识别目标文件"""
        # 实现逻辑：
        # 1. 分析条目关键词
        # 2. 应用启发式规则
        # 3. 返回目标文件
        pass
    
    def detect_conflicts(self, entry: Dict, target: str) -> List[Dict]:
        """检测冲突"""
        # 实现逻辑：
        # 1. 读取目标文件
        # 2. 搜索相似内容
        # 3. 计算相似度
        # 4. 返回冲突列表
        pass
    
    def convert_format(self, entry: Dict, target: str) -> str:
        """格式转换"""
        # 实现逻辑：
        # 1. 根据目标文件类型转换格式
        # 2. AGENTS.md → 行为规则格式
        # 3. TOOLS.md → 配置表格格式
        # 4. SOUL.md → 人格定义格式
        pass
    
    def do_promote(self, converted: str, target: str, conflicts: List):
        """执行提升"""
        # 实现逻辑：
        # 1. 追加到目标文件
        # 2. 处理冲突 (如需要)
        # 3. 记录提升日志
        pass
    
    def cleanup_memory(self, entry_id: int):
        """清理记忆"""
        # 实现逻辑：
        # 1. 标记为"已提升"
        # 2. 或移动到归档区
        pass
```

---

## 📊 输出示例

### 成功提升

```markdown
## ✅ 提升成功

**条目 ID**: 1
**条目名称**: 模型路由策略
**目标文件**: TOOLS.md
**提升时间**: 2026-04-22 10:50

### 提升内容

```markdown
## 📝 模型分工

| 场景 | 模型 | API Key | 说明 |
|------|------|---------|------|
| **小说正文** | DeepSeek Chat | `sk-xxx` | 写小说时用 DeepSeek |
| **日常对话** | Qwen3.5-plus | `sk-sp-xxx` | 默认主模型 |
```

### 后续操作

- ✅ 已追加到 `TOOLS.md` 第 3 节
- ✅ 已在 `MEMORY.md` 标记为"已提升"
- ⚠️ 建议：检查 `TOOLS.md` 格式是否符合预期

---

**使用 `/si:review` 查看新的提升候选**
```

### 冲突警告

```markdown
## ⚠️ 检测到冲突

**条目 ID**: 2
**条目名称**: 零用户操作规范
**目标文件**: AGENTS.md

### 冲突内容

**已存在规则** (AGENTS.md 第 5 节):
```markdown
- AI 应自主执行任务，减少用户操作
```

**待提升规则**:
```markdown
- 零用户操作：AI 自主信息获取 + 自动化执行
```

**相似度**: 75%

### 建议操作

1. **跳过** - 保留现有规则
2. **替换** - 用新规则替换旧规则
3. **合并** - 合并两条规则
4. **追加** - 作为补充规则追加

---

**使用 `/si:promote 2 --action merge` 执行合并**
```

---

## 🔗 相关命令

| 命令 | 功能 |
|------|------|
| `/si:review` | 审查记忆，找出提升候选 |
| `/si:status` | 查看记忆健康状态 |
| `/si:extract` | 从模式中提取技能 |

---

## 📈 预期效果

| 指标 | 实施前 | 实施后 | 提升 |
|------|--------|--------|------|
| 规则化时间 | 手动 20 分钟 | 自动 10 秒 | -99% |
| 规则化率 | 20% | 80% | +300% |
| 记忆冗余度 | 高 | 低 | -60% |

---

**创建者**: OpenClaw Assistant  
**创建时间**: 2026-04-22 10:50  
**状态**: ✅ 设计完成，待实现
