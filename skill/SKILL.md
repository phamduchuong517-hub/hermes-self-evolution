---
name: self-evolution
title: Self-Evolution — Behavior Rule Engine
description: >
  Hermes Agent self-evolution via SELF-EVOLUTION.md rule table.
  No dependencies. No databases. No external API calls.
  Just one file + one prefill instruction = Agent learns from corrections.
version: 1.0.0
author: Hermes Self-Evolution
tags: [self-improvement, behavior, evolution, rules, minimal]
source: https://github.com/yourname/hermes-self-evolution
---

# Self-Evolution Skill

**Purpose:** Enable Hermes Agent to learn from user corrections and permanently change behavior.

## How It Works

1. **SELF-EVOLUTION.md** — A markdown rule table at `~/.hermes/SELF-EVOLUTION.md`
2. **prefill-evolution.txt** — Prefill instruction that forces reading the rule table before every response
3. **config.yaml prefill_messages_file** — Injects the prefill into every conversation automatically

## Installation

```bash
# Copy the rule table
cp examples/self-evolution.md ~/.hermes/SELF-EVOLUTION.md

# Copy the prefill instruction
cp examples/prefill-evolution.txt ~/.hermes/prefill-evolution.txt

# Add to config.yaml
echo 'prefill_messages_file: "~/.hermes/prefill-evolution.txt"' >> ~/.hermes/config.yaml
```

## Rule Table Format

```
## 🔴 NEVER DO
- rule description here

## 🟢 ALWAYS DO
- rule description here

## 🟡 TECHNICAL DECISIONS
- rule description here

## 🗄️ ARCHIVED (outdated)
- rule description here
```

## Lifecycle

```
User correction → Skill writes rule to SELF-EVOLUTION.md
                → Next conversation starts
                → prefill forces scan of rules
                → Agent changes behavior accordingly
```

## Verification

To verify the skill is active:

```bash
# Check file exists
ls -la ~/.hermes/SELF-EVOLUTION.md

# Check prefill is configured
grep prefill_messages_file ~/.hermes/config.yaml
```
