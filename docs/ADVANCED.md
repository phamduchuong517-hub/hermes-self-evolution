# Advanced Usage — Hermes Self-Evolution

## 1. 主动进化（Agent 自主改进）

Agent 可以主动发现需要改进的地方。当以下情况发生时：

- 同一类任务重复失败（3次+）
- 用户表现出明显的不耐烦（"不说废话"、"直接说完"）
- 某个决策模式导致多次纠正

Agent 可以主动写入规则：

```markdown
## 🟡 ACTIVE — Agent 自主发现
- 用户提问技术问题时，先检查是否在当前文件/记忆中有答案，再发散搜索
```

### 规则标识约定

| 标识 | 含义 | 谁写入 |
|------|------|--------|
| `🔴 PASSIVE` | 被纠正后写入 | 用户/AI |
| `🟡 ACTIVE` | Agent 主动发现 | AI |
| `🟢 ONCE` | 单次任务规则 | AI |
| `🗄️ ARCHIVED` | 过期规则 | AI |

## 2. 多规则表

对于多角色 AI 实例，可以用不同文件管理不同维度的规则：

```
~/.hermes/
├── SELF-EVOLUTION.md          # 主规则表（所有场景通用）
├── self-evolution-tech.md     # 技术决策规则
└── self-evolution-social.md   # 社交风格规则
```

**在 prefill 中指定加载哪个文件：**

```txt
[System Instruction: Before responding, scan ~/.hermes/SELF-EVOLUTION.md and
~/.hermes/self-evolution-tech.md for behavior rules.]
```

## 3. 规则文件锁定

防止 Agent 无意中修改或删除规则：

```bash
# 锁定文件为只读
chmod 444 ~/.hermes/SELF-EVOLUTION.md

# 允许追加但不允许修改（用 append-only 属性，Linux only）
chattr +a ~/.hermes/SELF-EVOLUTION.md
```

如果锁定，规则追加需要用户手动编辑。Agent 只能在建议区（特殊标记段）写入提案：

```markdown
## 💡 AI 建议区（由 AI 写入，由用户确认后合并）
- 建议新规则：...
```

## 4. 规则稽核（影子模式）

不强制 Agent 遵守规则，只记录偏差：

```bash
# 启动影子模式任务
hermes cron create \
  --name audit-evolution \
  --schedule "0 5 * * *" \
  --prompt "Compare last 10 responses against SELF-EVOLUTION.md. List any rule violations."
```

## 5. 配置文件集成

在 Hermes Agent 的 config.yaml 中：

```yaml
# 基础配置：prefill 强制扫描
prefill_messages_file: "~/.hermes/prefill-evolution.txt"

# 进阶：使用 disable_skills 精确控制加载
disabled_skills:
  - self-improvement-core  # 禁用旧版重技能
  # 只保留本轻量技能
```

## 6. 验证闭环是否生效

```bash
# 测试步骤
# 1. 纠正 Agent 一个明确的行为
# 2. 检查 SELF-EVOLUTION.md 是否有新规则
grep -c "规则关键词" ~/.hermes/SELF-EVOLUTION.md

# 3. 启动新对话，看看 Agent 是否遵守
# 4. 再次违规时，检查是否更新了规则
```

## 7. 跨平台部署

该方案不限于 Hermes Agent：

| 平台 | 集成方式 |
|------|---------|
| OpenAI API | 在 system prompt 末尾加 prefill 指令 |
| Claude | 添加到 system prompt 或 prefill |
| OpenClaw | 相同方式：prefill + SELF-EVOLUTION.md |
| 任何 LLM 应用 | 在第一次 user message 前注入 prefill |

**核心原则：** 只要 LLM 能读取 system prompt + 有一个文件/变量存规则表——进化就能工作。
