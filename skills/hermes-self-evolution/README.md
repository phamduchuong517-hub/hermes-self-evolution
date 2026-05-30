# hermes-self-evolution

> Hermes Agent 轻量行为进化系统 — 单文件规则表 + 进化引擎模块
> **版本**: v7.2.0 — 新增零幻觉自检协议 + VOYAGER 反思循环

## 核心变更 v7.2.0

- **零幻觉自检协议** — ScienceClaw 适配，每条事实断言必须 4 问前置检查
- **VOYAGER 反思循环** — 5 维自评 + 模式存储 + 自动进化触发

## 设计哲学

与 self-improvement-core 的"多阶段架构"不同，hermes-self-evolution 遵循极简原则：

- **行为改变优先**：每次反思必须输出一个行为规则，否则不算进化
- **单文件 SELF-EVOLUTION.md**：每次对话前读一遍，即时生效
- **零 Token 浪费**：不跑 WAL/Working Buffer/Confidence Scoring 等会计层

## 文件结构

```
hermes-self-evolution/
├── SELF-EVOLUTION.md        ← 行为规则表 v7.2.0（核心文件，每次对话前读）
├── SKILL.md                 ← 技能定义 v7.2.0
├── README.md                ← 本文件
├── core/
│   ├── auto_evolution_plugin.py
│   └── self_modifying_runtime.py
├── evolution/
│   ├── agent_loop.py
│   ├── hermes_phase2_expansion.py
│   ├── path_rule.py
│   ├── self_modifying_runtime_v3.py
│   ├── skill_first_executor.py
│   ├── skill_search_engine.py
│   └── trace_review.py
└── references/
    ├── duplicate-note.md
    └── hermes-environment-adaptation.md
```

## 规则表内容（v7.2.0）

| 章节 | 内容 | 来源 |
|:-----|:-----|:-----|
| 一、框架自主规则 | 零用户操作/请示/直接执行三场景 | 原始 |
| 二、场景隔离规则 | 编码vs小说vs架构分析三场景 | 原始 |
| 三、沟通规则 | Bug修复/时间敏感/批评应对 | 原始 |
| 四、零幻觉自检协议 | 4问前置检查 + 禁止用语表 | **ScienceClaw** |
| 五、进化规则 | 问题→记录→规则→禁止模式 | 扩充 |
| 六、任务反思循环 | VOYAGER 5维自评 + 模式进化 | **ScienceClaw** |

## 来源追溯

- 零幻觉协议：adapted from [beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw) SCIENCE.md
- VOYAGER 反思：adapted from ScienceClaw skill-evolution/SKILL.md
- 其余规则：来自 OpenClaw 实战经验积累
