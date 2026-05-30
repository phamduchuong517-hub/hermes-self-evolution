---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task. Creates comprehensive implementation plans with bite-sized tasks, exact file paths, and complete code examples. Now with PACT protocol for contract-driven implementation.
version: 2.0.0
author: Hermes Agent (adapted from obra/superpowers + agentic-coding PACT protocol)
license: MIT
metadata:
  hermes:
    tags: [planning, design, implementation, workflow, documentation, pact]
    related_skills: [subagent-driven-development, test-driven-development, requesting-code-review, systematic-debugging]
---

# Writing Implementation Plans

## Overview

Write comprehensive implementation plans assuming the implementer has zero context for the codebase and questionable taste. Document everything they need: which files to touch, complete code, testing commands, docs to check, how to verify. Give them bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the implementer is a skilled developer but knows almost nothing about the toolset or problem domain. Assume they don't know good test design very well.

**Core principle:** A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.

## PACT Protocol (v2.0) ⭐

Before writing any plan, lock the contract with PACT:

1. **P**roblem framing — Restate objective and assumptions in one sentence
2. **A**cceptance design — Define checks that prove success BEFORE writing code
3. **C**hange set — Produce the smallest useful diff (one goal = one change set)
4. **T**race and test — Show evidence and residual risk

**No contract, no code.** If you can't state the acceptance criteria in one sentence, you don't understand the problem yet.

### PACT Bug Fix Variant ⭐

For bugs and regressions (use when user reports a bug, not a feature):
1. Capture the failing condition first (test, log, or reproduction)
2. Apply minimal fix
3. Re-run the same check to prove resolution

**Never claim fixed without before and after evidence.**

### PACT Time Budget ⭐

For every plan, set a time budget upfront — not an estimate, a HARD MAXIMUM. The budget should match the task's real priority:

| Task Type | Budget | Signal to Stop |
|-----------|--------|----------------|
| Quick analysis / one-shot fetch | **5 min** | 3 tool calls without answer |
| Moderate task (read + summarize) | **15 min** | Hitting scope creep |
| Complex multi-step task | **30 min** | 30+ messages without meaningful progress |
| "Absorb and learn" vague tasks | **20 min** | Content read, now drafting integration |

**When you hit the time budget without finishing:**
1. Stop immediately — do NOT auto-continue
2. Report: "Hit the **{budget}** time budget. So far I've done: {completed}. Left: {remaining}."
3. Propose options for the user: continue, pivot, or reschedule
4. Let the USER decide — do not assume they want to keep going

**Do NOT** assume "absorb and learn" means "unlimited deep dive." Read the core content, identify 1-2 key takeaways, and report. The user will ask for depth if they want it.

**Model speed awareness:** DeepSeek Chat outputs ~30-45 tok/s. Each tool call round-trip adds 5-15s of generation. 50 tool calls = ~10-30 min of pure generation time. Budget accordingly.

### PACT Handoff ⭐

End each cycle with a delivery packet:
- What changed and why
- Files touched and blast radius
- Validation run and results
- Known risks and rollback path

**If handoff is unclear, the task is not finished.**

## When to Use

**Always use before:**
- Implementing multi-step features
- Breaking down complex requirements
- Delegating to subagents via subagent-driven-development
- Fixing bugs (use PACT bug fix variant)

**Don't skip when:**
- Feature seems simple (assumptions cause bugs)
- You plan to implement it yourself (future you needs guidance)
- Working alone (documentation matters)

## Bite-Sized Task Granularity

**Each task = 2-5 minutes of focused work.**

Every step is one action:
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

**Too big:**
```markdown
### Task 1: Build authentication system
[50 lines of code across 5 files]
```

**Right size:**
```markdown
### Task 1: Create User model with email field
[10 lines, 1 file]

### Task 2: Add password hash field to User
[8 lines, 1 file]

### Task 3: Create password hashing utility
[15 lines, 1 file]
```

## Plan Document Structure

### Header (Required)

Every plan MUST start with:

```markdown
# [Feature Name] Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**PACT Contract:**
- **Problem:** [One sentence — what are we solving?]
- **Acceptance:** [Checks that prove success — run these to verify]
- **Non-goals:** [What stays untouched]
- **Constraints:** [Stack, style, limits]

**Architecture:** [2-3 sentences about approach]
**Tech Stack:** [Key technologies/libraries]

---
```

### Task Structure

Each task follows this format:

````markdown
### Task N: [Descriptive Name]

**Objective:** What this task accomplishes (one sentence)

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67` (line numbers if known)
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify failure**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify pass**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Writing Process

### Step 0: PACT Contract (v2.0) ⭐

Before anything else, lock:
- **Problem**: One sentence restating the objective
- **Acceptance**: Concrete checks that prove success
- **Non-goals**: What intentionally stays out of scope
- **Constraints**: Stack, style, limits, deadlines

Write these in the plan header. If you can't, clarify with the user.

### Step 1: Understand Requirements

Read and understand:
- Feature requirements
- Design documents or user description
- Acceptance criteria
- Constraints

### Step 2: Explore the Codebase

Use Hermes tools to understand the project:

```python
# Understand project structure
search_files("*.py", target="files", path="src/")

# Look at similar features
search_files("similar_pattern", path="src/", file_glob="*.py")

# Check existing tests
search_files("*.py", target="files", path="tests/")

# Read key files
read_file("src/app.py")
```

### Step 3: Design Approach

Decide:
- Architecture pattern
- File organization
- Dependencies needed
- Testing strategy

### Step 4: Write Tasks

Create tasks in order:
1. Setup/infrastructure
2. Core functionality (TDD for each)
3. Edge cases
4. Integration
5. Cleanup/documentation

### Step 5: Add Complete Details

For each task, include:
- **Exact file paths** (not "the config file" but `src/config/settings.py`)
- **Complete code examples** (not "add validation" but the actual code)
- **Exact commands** with expected output
- **Verification steps** that prove the task works

### Step 6: Review the Plan

Check:
- [ ] PACT contract is defined (v2.0)
- [ ] Tasks are sequential and logical
- [ ] Each task is bite-sized (2-5 min)
- [ ] File paths are exact
- [ ] Code examples are complete (copy-pasteable)
- [ ] Commands are exact with expected output
- [ ] No missing context
- [ ] DRY, YAGNI, TDD principles applied
- [ ] For bug fixes: Prove failure before fix, re-run after fix (v2.0)

### Step 7: Save the Plan

```bash
mkdir -p docs/plans
# Save plan to docs/plans/YYYY-MM-DD-feature-name.md
git add docs/plans/
git commit -m "docs: add implementation plan for [feature]"
```

## Principles

### DRY (Don't Repeat Yourself)

**Bad:** Copy-paste validation in 3 places
**Good:** Extract validation function, use everywhere

### YAGNI (You Aren't Gonna Need It)

**Bad:** Add "flexibility" for future requirements
**Good:** Implement only what's needed now

```python
# Bad — YAGNI violation
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # Not needed yet!
        self.metadata = {}     # Not needed yet!

# Good — YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### TDD (Test-Driven Development)

Every task that produces code should include the full TDD cycle:
1. Write failing test
2. Run to verify failure
3. Write minimal code
4. Run to verify pass

See `test-driven-development` skill for details.

### PACT Bug Fix (v2.0) ⭐

For bugs (not features), use Prove Failure → Fix → Prove Fix cycle:
1. Capture failing condition (reproduction steps or test)
2. Show it fails ("before" evidence)
3. Apply minimal change
4. Re-run same check ("after" evidence)
5. Only then report fixed

### Frequent Commits

Commit after every task:
```bash
git add [files]
git commit -m "type: description"
```

## Common Mistakes

### Vague Tasks

**Bad:** "Add authentication"
**Good:** "Create User model with email and password_hash fields"

### Incomplete Code

**Bad:** "Step 1: Add validation function"
**Good:** "Step 1: Add validation function" followed by the complete function code

### Missing Verification

**Bad:** "Step 3: Test it works"
**Good:** "Step 3: Run `pytest tests/test_auth.py -v`, expected: 3 passed"

### Missing File Paths

**Bad:** "Create the model file"
**Good:** "Create: `src/models/user.py`"

### Reporting Fix Without Evidence (v2.0) ⭐

**Bad:** "Done, the bug is fixed"
**Good:** "Bug fixed: before = test failed with 'KeyError: name', after = test passes"
**Good:** "Bug fixed: reproduction steps confirmed broken → minimal change applied → reproduction confirms resolved"

## Execution Handoff

After saving the plan, offer the execution approach:

**"Plan complete and saved. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?"**

When executing, use the `subagent-driven-development` skill:
- Fresh `delegate_task` per task with full context
- Spec compliance review after each task
- Code quality review after spec passes
- Proceed only when both reviews approve

## Remember

```
Lock PACT contract first (v2.0)
Bite-sized tasks (2-5 min each)
Exact file paths
Complete code (copy-pasteable)
Exact commands with expected output
Verification steps
Prove failure → fix → prove fix (bugs)
DRY, YAGNI, TDD
Frequent commits
```

**A good plan makes implementation obvious.**
