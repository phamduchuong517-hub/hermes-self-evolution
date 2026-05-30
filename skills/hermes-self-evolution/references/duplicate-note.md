# ⚠️ 技能重复说明

**本技能 `self-improvement-core` 存在两个副本：**

| 路径 | 版本 | 状态 |
|------|------|------|
| `/root/.hermes/skills/self-improvement-core/` | v4.3 | 旧版（会被 `skill_view` 匹配） |
| `/root/.hermes/skills/openclaw-imports/self-improvement-core/` | v5.0（三棵树+知识图谱） | **新版，应优先使用** |

## 差异

- **v5.0**: 含 knowledge-memory.py 脚本 + 三棵树记忆架构（SQLite）+ 知识图谱 + Subconscious 模式
- **v4.3**: WAL 协议 + Working Buffer + Compaction Recovery（不包含知识图谱 SQLite 引擎）

## 访问方式

目前只能用 `skill_view(name='openclaw-imports/self-improvement-core')` 访问 v5.0 版本。

## 修复方向

需要 curator 处理：
1. 将 v5.0 内容复制到非 categorized 目录
2. 删除 openclaw-imports 下的副本
3. 或重命名其中一个
