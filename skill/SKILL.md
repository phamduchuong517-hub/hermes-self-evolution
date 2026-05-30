---
name: hermes-skill-pack
title: Hermes Agent Skill Pack
description: >
  15 production-grade Hermes Agent skills — self-evolution, task orchestration,
  token optimization, debugging, writing plans, brainstorming, MCP builder, and more.
  Zero dependencies. Drop into ~/.hermes/skills/ and they just work.
version: 1.0.0
source: https://github.com/phamduchuong517-hub/hermes-self-evolution
tags: [hermes-agent, skills, self-evolution, task-orchestration, token-optimization, mcp, debugging]
---

# Hermes Agent Skill Pack

15 production-grade Hermes Agent skills. Drop into `~/.hermes/skills/` and they just work.

## Quick Install

```bash
# Download the pack
git clone https://github.com/phamduchuong517-hub/hermes-self-evolution.git /tmp/hermes-pack

# Install all skills
cp -r /tmp/hermes-pack/skills/* ~/.hermes/skills/

# Reload Hermes
hermes reload
```

## Skills Index

### Core Infrastructure
- **self-improvement-core** (v4.3) — Self-evolution engine
- **task-orchestrator** (v3.0) — Task lifecycle manager
- **token-optimization** (v2.1) — 60-95% token compression
- **skill-lifecycle-manager** (v3.1) — Skill creation + factory + event bus

### Plugins
- **external-system-learning** (v1.6) — Absorb capabilities from GitHub projects
- **deep-search** (v2.0) — Multi-layer search with academic sources
- **mcp-server-builder** (v1.0) — MCP server construction (Python + TypeScript)

### Workflows
- **systematic-debugging** (v2.0) — 4-stage root cause analysis
- **writing-plans** (v2.0) — PACT contract-driven implementation plans
- **brainstorming** (v1.0) — Pre-coding design refinement
- **grill-with-docs** (v1.0) — Deep questioning + terminology alignment + ADRs
- **doubt-driven-development** (v1.0) — Zero-context review for critical decisions
- **git-workflow-complete** (v1.0) — Feature branch workflow with git worktrees
- **subagent-driven-development** (v1.0) — Parallel subagent dispatch + 2-stage review

## License

MIT
