# hermes-self-evolution

> Hermes Agent 轻量行为进化系统 — 单文件规则表 + 进化引擎模块

## 设计哲学

与 self-improvement-core 的"多阶段架构"不同，hermes-self-evolution 遵循极简原则：

- **行为改变优先**：每次反思必须输出一个行为规则，否则不算进化
- **单文件 SELF-EVOLUTION.md**：每次对话前读一遍，即时生效
- **零 Token 浪费**：不跑 WAL/Working Buffer/Confidence Scoring 等会计层

## 文件结构

```
hermes-self-evolution/
├── SELF-EVOLUTION.md        ← 行为规则表（核心文件，每次对话前读）
├── SKILL.md                 ← 技能定义
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
