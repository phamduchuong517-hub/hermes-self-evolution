# 📝 Error Logger v4.0.0 - 错误日志技能 (Agent SRE + Tenacity + 结构化分级增强版)
name: error-logger
description: 错误日志技能 v4.0 - 记录和分析错误，避免重复错误，集成自进化反思机制 + Hermes Tenacity 持久运行 + 结构化错误分级 + 上下文快照 + 主动预防 + Agent SRE (SLO/Error Budget/Circuit Breaker)
version: 4.1.0
type: 系统核心技能
source: error-logger v3.0 + Hermes Agent v0.13.0 checkpoint state persistence + post-write delta lint + Hermes Dojo session analysis pattern + structured error grading + microsoft/agent-sre SLO + Error Budget + Circuit Breaker
upgrade: v4.0 注入 Agent SRE 三件套 (SLO/Error Budget/Circuit Breaker) + 错误预算仪表盘 + OWASP 可靠性映射 | v3.0 添加自进化反思机制 (错误捕获/原因分析/解决方案/修改执行/预防机制)
---

# 📝 Error Logger v4.0 - 错误日志技能 (Tenacity + SRE 增强版)

**记录和分析错误，避免重复错误 — 跨重启持久化 + SLO/Error Budget/Circuit Breaker**

---

## 功能

### 0. Agent SRE 三件套 (v4.0 新注入) ⭐⭐⭐

**集成来源**: microsoft/agent-governance-toolkit Agent SRE + OWASP ASI08/ASI09

```bash
/error:slo                        # 查看当前 SLO 状态
/error:slo --set "24h=95%"       # 设置目标 SLO (24h 窗口 95% 成功率)
/error:budget                    # 查看 Error Budget 仪表盘
/error:budget --set "5%"        # 设置 Error Budget (SLO 容差)
/error:circuit                   # 查看 Circuit Breaker 状态
/error:circuit --reset           # 手动重置 Circuit Breaker
```

**SLO 引擎 (Service Level Objective)**
```
指标类型         目标        窗口       当前状态
TaskSuccessRate  95%         24h        ✅ 96.2%
ToolCallLatency  <5s p95    1h         ⚠️ 6.1s (接近阈值)
ErrorRecovery    <15min p90  24h        ✅ 8min
MemoryRetention  >90%        7d         ✅ 93%
```

**Error Budget 仪表盘**
```
┌─────────────────────────────────────┐
│  Error Budget: 5% 容差              │
│  ─────────────────────────           │
│  ✅ 已使用: 1.8% (12次错误)          │
│  ✅ 剩余: 3.2%                       │
│  └── 预计耗尽: 16天 (当前速率)       │
│                                      │
│  🟢 状态: HEALTHY                    │
│  ( > 30% budget remaining)          │
└─────────────────────────────────────┘
```

**Circuit Breaker 状态机**
```
🟢 CLOSED     → 正常操作，请求通过
   ↓ 超出 Error Budget
🟡 HALF-OPEN  → 限流 50%，探测恢复
   ↓ 恢复成功 → CLOSED
   ↓ 再次失败  
🔴 OPEN       → 熔断，自动降级到备用路径
   ↓ 冷却时间 (60s) → HALF-OPEN
```

**OWASP 可靠性映射**:
| OWASP 风险 | Agent SRE 覆盖 |
|------------|---------------|
| ASI08: 级联故障 | Circuit Breaker + 错误隔离 |
| ASI09: 缺乏可观测性 | SLO + Error Budget + 仪表盘 |
| ASI10: 测试不足 | 错误预算消耗速率为混沌测试提供触发 |

---

### 0.5 持久运行模式 (v4.0 新注入) ⭐⭐⭐

**集成来源**: Hermes Agent v0.13.0 Checkpoints v2 + auto-resume

```bash
/error:persist                  # 打开持久模式
/error:persist --status        # 查看持久状态
/error:persist --checkpoint    # 手动创建检查点
/error:recover                 # 从检查点恢复
```

**核心机制**:
```
- Auto-resume: Gateway 重启后自动恢复错误追踪状态
- Checkpoints v2: 真实修剪 + Disk Guardrails + Orphan Cleanup
- 重启后自动扫描 active.json 中的未处理错误
- 跨会话错误追踪（不因重启丢失）
- 错误处理进度保存：已分析/待解决/已修复
```

### 1. 结构化错误分级 (v4.0 新注入) ⭐⭐⭐

| 级别 | 标签 | 说明 | 响应时间 |
|------|------|------|----------|
| P0 | 🔴 CRITICAL | 系统不可用/数据丢失 | 立即处理 |
| P1 | 🟠 HIGH | 功能不可用/用户受阻 | 15 分钟内 |
| P2 | 🟡 MEDIUM | 功能降级/性能下降 | 4 小时内 |
| P3 | 🔵 LOW | 可用但不理想 | 下次维护窗口 |

```bash
/error:log --level P0 "系统无法连接 MCP 服务器"
/error:log --level P1 "搜索功能 30% 成功率"
/error:log --level P2 "响应时间增加 2 倍"
/error:log --level P3 "某个边缘功能不可用"
```

### 2. 上下文快照 (v4.0 新注入) ⭐⭐

每次错误记录自动保存：
```json
{
  "error_id": "err_abc123",
  "timestamp": "2026-05-17T15:03:00+08:00",
  "level": "P1",
  "type": "search_failed",
  "message": "web_search provider timeout",
  "snapshot": {
    "conversation_id": "qqbot:c2c:xxx",
    "last_5_messages": [...],
    "active_tools": ["web_search", "web_fetch"],
    "system_state": {
      "load": "0.5",
      "memory": "78%",
      "uptime": "12d 4h"
    }
  },
  "root_cause": "Tavily API timeout > 10s",
  "workaround": "使用 web_fetch 替代",
  "fix_url": "https://github.com/..."
}
```

### 3. 主动预防 - Post-write Delta Lint (v4.0 新注入) ⭐⭐⭐

```bash
# 写入文件后自动检查
/error:lint --mode python    # 检查 Python 语法
/error:lint --mode yaml     # 检查 YAML 格式
/error:lint --mode json     # 检查 JSON 有效性
/error:lint --mode toml     # 检查 TOML 格式
/error:lint --all           # 全部检查
```

**执行流程**:
```
写入文件 → auto-lint → 语法错误? → 是 → 立即回滚 + 记录错误
                      → 否 → 继续
```

**支持的格式**: Python / JSON / YAML / TOML

### 4. 错误根因回溯 (v4.0 新注入) ⭐⭐

```bash
/error:trace "某个重复错误"     # 回溯根因
/error:trace --deep            # 深入追踪 3 层
/error:trace --graph           # 生成错误依赖图
```

**回溯输出示例**:
```
错误: "web_search provider timeout" (P1)
├── 直接原因: Tavily API 响应 >10s
├── 根本原因: 网络线路拥堵 (晚间高峰期)
│   └── 根因类型: 网络基础设施
├── 影响范围: 3 次搜索请求超时
├── 预防措施: 添加备用 API + 超时重试
└── 已修复: ✅ 添加 web_fetch 降级方案
```

---

### 5. 错误记录 (原有功能保留)

1. **错误记录**
   - 记录错误详情
   - 记录错误上下文
   - 记录解决方案

2. **错误分析**
   - 分析错误模式
   - 识别重复错误
   - 统计错误频率

3. **错误预防**
   - 执行前检查错误日志
   - 提供避免建议
   - 推荐替代方案

---

## 错误格式

```json
{
  "timestamp": "2026-03-20 21:39:00",
  "error_type": "cookie_invalid",
  "error_message": "Cookie 缺少创作者凭证",
  "context": {
    "skill": "xiaohongshu-mcp",
    "action": "search_notes"
  },
  "solution": "使用昨天的 Cookie (/tmp/yesterday_cookie.txt)",
  "repeated": false,
  "repeat_count": 0
}
```

---

## 使用方法

```bash
# 记录错误
python3 error_logger.py log "Cookie 无效" --type cookie_invalid

# 查看错误日志
python3 error_logger.py show

# 分析错误模式
python3 error_logger.py analyze

# 检查是否重复错误
python3 error_logger.py check "Cookie 无效"
```

---

## 错误分类

| 类型 | 说明 | 解决方案 |
|------|------|----------|
| cookie_invalid | Cookie 无效 | 验证 Cookie 完整性 |
| tool_not_found | 工具不存在 | 检查可用工具列表 |
| screenshot_failed | 截图失败 | 安装截图工具 |
| search_failed | 搜索失败 | 使用备用搜索方案 |
| vnc_failed | VNC 失败 | 检查 VNC 配置 |

---

**创建时间**: 2026-03-20 21:39
**最后更新**: 2026-05-17 (v4.0 Tenacity + SRE 增强版)

---

## 附录：技能结晶化机制（v4.1 新增）

**来源**：GenericAgent Skill Crystallization + Odysseus skill_extractor.py
**目的**：错误模式自动提取为可复用技能，不是人工写技能，而是从错误经验中自动生成

### 核心思想
```
错误发生 → 分析根因 → 判断是否可抽象为技能 → 生成技能草案 → 审核 → 写入SKILL.md
```

### 触发条件
错误发生满足以下任一条件时，触发技能结晶化：
- 同一错误重复 ≥ 3次（说明有模式可提炼）
- 复杂错误涉及 ≥ 5个步骤才解决（说明流程可标准化）
- 错误首次解决但花了 ≥ 10分钟（说明需要提速）

### 提取Prompt模板
```
## 技能提取分析
错误类型：{error_type}
错误消息：{error_message}
解决步骤：{solution_steps}
成功要素：{why_it_worked}

请提炼成可复用的SKILL.md格式，包含：
- name: 技能名（动词短语）
- description: 一句话说明
- trigger: 何时使用（警告信号）
- steps: 核心步骤（3-5步）
- example: 示例场景
- warning: 常见失败原因

如果无法提炼成通用技能，请说明原因。
```

### 结晶化输出位置
- 技能草案保存到：`workspace/skills/generated/{skill-name}/SKILL.md`
- 技能审核队列：追加到 skill-vetter-plugin 评估队列

### 与现有机制的关系
| 机制 | 作用 | 与结晶化的关系 |
|------|------|--------------|
| error-logger | 记录错误 | 输入错误数据 |
| skill-vetter | 审核技能 | 审核结晶化输出的草案 |
| self-improvement-core | 规则进化 | 结晶化后触发版本升级 |
| **技能结晶化** | 从错误生成技能 | **新增**，连接error-logger和skill-vetter |

### 示例：从"QQ文件发送失败"提取技能
```
错误：QQ文件附件看不到，消息显示发送成功
根因：QQBot文件功能对某些用户不可见（channel限制）
解决：用纯文本分批发送

提取后的技能草案：
name: qqbot文本分批发送
trigger: 当需要传递完整文件内容给QQ用户时
steps:
  1. 识别文件类型（txt/md/json）
  2. 拆分为300字段落
  3. 按顺序标注[1/N][2/N]...
  4. 每批间隔500ms
example: 发送小说章节给用户
warning: 不要用分隔线，会触发QQ过滤
```
