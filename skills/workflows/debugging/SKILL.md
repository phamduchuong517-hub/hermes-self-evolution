---
name: systematic-debugging
description: 4 阶段根因调查 + 10 种反馈回路构建。专治任何 Bug、测试失败、非确定性、性能退化。NO fixes without understanding first。吸收自 mattpocock/skills /diagnose (2026-05-17)
version: 2.0.0
author: Hermes Agent (adapted from obra/superpowers + mattpocock/skills)
license: MIT
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation, feedback-loop]
    related_skills: [test-driven-development, writing-plans, subagent-driven-development, diagnose]
upgrade: v2.0 融合 diagnose 的 10 种反馈回路构建方法 + HITL 脚本 + 5 阶段流程增强
---

# Systematic Debugging v2.0 — 硬 Bug 系统诊断

**v2.0 融合自**: mattpocock/skills /diagnose (87k⭐, 2026-05-17) — 10 种反馈回路构建方法

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 0 (feedback loop), you cannot proceed to Phase 1.

## Phase 0 — Build Feedback Loop (v2.0 新增 ⭐)

**这是整个调试技能里最重要的阶段。** 如果你有一个快速、确定性、Agent 可运行的通过/失败信号——二分查找、假设检验、仪器化都只是消费这个信号。没有信号，盯着代码看没用。

### 10 种构建方法（按顺序试）

| # | 方法 | 说明 | 适用场景 |
|:-|------|------|---------|
| 1 | **失败测试** | 在能触及 Bug 的 seam 处写单元/集成/e2e 测试 | 代码可测试 |
| 2 | **Curl/HTTP 脚本** | 对运行中的 dev server 发请求，检查响应 | API/后端 Bug |
| 3 | **CLI 调用** | 用 fixture 输入调用 CLI，diff stdout 和已知良好快照 | CLI 工具 |
| 4 | **无头浏览器** | Playwright/Puppeteer 驱动 UI，断言 DOM/控制台/网络 | 前端 Bug |
| 5 | **回放 trace** | 保存真实网络请求/载荷/事件日志到磁盘，隔离重放 | 网络/异步问题 |
| 6 | **一次性 harness** | 启动系统最小子集（一个服务+mock），单函数调用 | 微服务 Bug |
| 7 | **属性/fuzz 循环** | Bug 是"偶尔输出错误"→ 跑 1000 随机输入 | 非确定性 Bug |
| 8 | **二分查找 harness** | Bug 在两种已知状态之间→自动化"启动→检查→重复" | 回归问题 |
| 9 | **差分循环** | 新旧版本（或两种配置）跑同样输入，diff 输出 | 配置变更 |
| 10 | **HITL bash 脚本** | 最后手段。如果必须人手动点，用脚本驱动人操作 | 无法自动化 |

### 迭代反馈回路本身

把回路当产品对待。一旦有了*一个*回路：

- 能不能更快？（缓存 setup、跳过无关初始化、缩小测试范围）
- 能不能让信号更 sharp？（断言具体症状，不是"没崩溃"）
- 能不能更确定？（固定时间、seed RNG、隔离文件系统、冻结网络）

**30 秒的 flaky 回路勉强比没有好。2 秒的确定回路是调试超能力。**

### 非确定性 Bug

目标不是完美复现，而是**更高的复现率**。把触发器循环 100 次、并行化、加压力、缩小时机窗口、注入 sleep。

- 50% 的 flake → 可调试
- 1% 的 flake → 不可调试
- 持续提高复现率直到可调试

### 真的无法构建回路时

停，明确说。列出你试过的。问用户要：
(a) 能复现的环境访问权限
(b) 捕获的 artifacts（HAR 文件、日志 dump、core dump、有时间戳的录屏）
(c) 增加临时生产监控的权限

**没有回路不要进入 Phase 1。**

---

## Phase 1: Root Cause Investigation
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 0. Evidence Chain Rule (2026-05-27 用户明确要求)

当用户质疑分析结果或要求"深度分析"时，必须使用证据链追溯法。

**原则**: 每个断言必须有至少两个独立数据源支持。没有日志/代码/命令输出支持的断言 = 幻觉，不允许输出。

**流程**（用户期望的思考顺序）:
```
1. 拉原始数据 — 不从之前的分析结论推导，直接读日志/配置/状态命令
2. 按时间线排列事件 — 识别因果关系链（不是孤立事件）
3. 找对照组 — 有正常运行的系统时做对比（对比日志、配置、环境）
4. 三遍验证 — 标注 ✅ 日志确认 / ⚠️ 推测 / ❌ 无证据
5. 事实列表 → 模式识别 → 根因结论（按此顺序输出）
```

**用户风格**（必须遵守）:
- ❌ "我觉得"、"看起来"、"可能有"、"之前分析过" → 用户直接视为幻觉
- ❌ 从之前的结论推导而不是从原始数据重新分析 → 用户会要求"重查"
- ✅ 直接输出日志时间线、量化对比、具体数字
- ✅ 每个结论后标注数据来源（哪个日志行、哪个配置字段、哪个命令的输出）

**时间线对比法（新增）**:

当用户问"为什么昨天正常今天突然变了"时：

```
步骤 1: 拉出错前/后各1天的完整日志，标记所有关键事件
        （WS连接/断开、重启、配置变更、消息收发、model warmup）
步骤 2: 找第一次出现异常的时间点（第一个4009、第一个warmup）
步骤 3: 在这个时间点之前和之后各找1次正常交互做对照
步骤 4: 识别变化：
        · 配置是否被改过？（对比 bak 文件）
        · 版本是否变了？
        · 进程是否被重启？
        · 会话文件是否损坏？
步骤 5: 建立因果链：A发生了 → B被触发 → C是结果 → D是用户看到的现象
```

**对照组分析法（新增）**:

当有正常运行的系统（如林汐）和出问题的系统（如苏晚）时：

```
步骤 1: 列出两个系统的所有已知差异（版本、配置、环境、运行时长、重启次数）
步骤 2: 对每个差异问"这能解释症状吗？" — 排除无关差异
步骤 3: 找到那个「有差异的系统独有、无差异的系统没有」的关键因子
步骤 4: 验证 — 如果修复了关键因子，症状应该消失
```

**常见陷阱**:
- ❌ **只看一个系统的日志就下结论**: 没有对照组的分析不完整
- ❌ **把症状当时序正常事件**: 每30分钟的4009断开不是"正常"——它说明系统一直在临界状态
- ❌ **忽略"无声的失败"**: 日志显示"200 OK"但用户没收到 → markdown消息问题
- ❌ **混淆API成功和用户可见**: "Sent markdown chunk (c2c)" ≠ 用户在QQ上看到了
- ❌ **误判"之前正常"的原因**: 用户说"以前正常"可能只是没注意到隐藏问题
- ❌ **先发散对比再聚焦用户线索**: 用户给明确线索时，先验证用户线索，再对比差异

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

### 6. Config Trace Rule — Grep, Don't Guess (2026-05-25)

**WHEN debugging a configuration problem (settings not taking effect, wrong behavior):**

**BEFORE guessing the config path, grep the source code.**

```bash
grep -r "config_key_name" /path/to/src/
grep -r "visibleReplies\|message_tool" /path/to/src/
```

**Why this matters:**
- Config docs are often incomplete or wrong
- Config files can have multiple levels (top-level vs channel-level) that look identical
- What you *think* the config path is ≠ what the code actually reads

**Action:**
1. Search the config key name in the source code
2. Read the lines that access it to find the exact path the code expects
3. Compare with your current config
4. Only then edit the config

**Real-world example** (2026-05-25): OpenClaw's `visibleReplies` config. AI tried setting `channels.qqbot.messages.visibleReplies` (channel-level), but the code reads `cfg.messages.visibleReplies` (top-level). Same YAML structure, different tree depth, 6 failed restarts before grep found the truth.

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **0. 反馈回路** | 10 种方法构建确定性信号 | 有快速、可复现的 PASS/FAIL 信号 |
| **1. 根因** | 读错误、复现、查变更、收证据、追踪数据流 | 理解 WHAT 和 WHY |
| **2. 模式** | 找类似代码、对比、识别差异 | 知道什么不同 |
| **3. 假设** | 形成理论、最小测试、一次只变一个变量 | 确认或新假设 |
| **4. 实现** | 创建回归测试、修根因、验证 | Bug 解决、全部测试通过 |

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **2.0.0** | **2026-05-17** | **融合 diagnose**: 新增 Phase 0 反馈回路 (10种方法) + HITL 脚本 + 5 阶段增强。来源: mattpocock/skills /diagnose (87k⭐) |
| 1.1.0 | — | 原版 (obra/superpowers) |
