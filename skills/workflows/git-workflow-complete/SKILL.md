---
name: git-workflow-complete
description: 完整特性分支工作流 — 隔离开发 + 任务完成决策。吸收自 obra/superpowers (195K⭐) using-git-worktrees + finishing-a-development-branch。适配 Hermes 云端环境。
version: 1.0.0
source: obra/superpowers (2026-05-18 吸收)
category: software-development
license: MIT
---

# 🔀 Git Workflow Complete — 特性分支全生命周期

## 适用场景

当开发一个新功能/修复，需要：
1. 与主分支隔离，不影响现有工作
2. 完成后决定合并/PR/保留/丢弃

## 核心原则

- **先检测现有隔离，再创建新隔离** — 不重复造轮子
- **测试通过才能完成** — 合并不通过测试的代码是 bugs 的来源
- **给出结构化选项，不要开放提问** — 用户选 1/2/3/4，不用想"下一步怎么办"

---

## Phase 1: 创建隔离工作区

### 步骤 0: 检测现有隔离

```bash
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null)
GIT_COMMON=$(git rev-parse --git-common-dir 2>/dev/null)
BRANCH=$(git branch --show-current 2>/dev/null)
```

- **如果 `GIT_DIR != GIT_COMMON`**（且不在 submodule）→ 已在工作树，直接跳到 Phase 2
- **如果 `GIT_DIR == GIT_COMMON`** → 需要创建隔离

### 步骤 1: 创建隔离

优先用 native 工具（如果有），否则用 `git worktree`：

```bash
git worktree add .worktrees/$BRANCH_NAME -b $BRANCH_NAME
cd .worktrees/$BRANCH_NAME
```

**安全验证**: 确保 `.worktrees/` 在 `.gitignore` 中，防止误提交。

### 步骤 2: 项目设置 + 基础测试

```bash
# 自动检测并运行 setup
[ -f package.json ] && npm install
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f Cargo.toml ] && cargo build

# 验证基准测试通过
npm test / pytest / cargo test
```

基准测试失败时先报告，不要直接开始工作。

---

## Phase 2: 完成任务

### 步骤 1: 验证测试

**任何完成操作前，先跑测试确认全部通过。**

```bash
npm test / cargo test / pytest / go test ./...
```

如果测试失败 → 不能继续，必须先修复。

### 步骤 2: 检测状态

```bash
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null)
GIT_COMMON=$(git rev-parse --git-common-dir 2>/dev/null)
```

确定是正常 repo、命名分支工作树、还是 detached HEAD。

### 步骤 3: 确定基准分支

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master
```

### 步骤 4: 展示选项

**正常 repo / 命名分支工作树:** 精确展示 4 个选项：

```
实现完成。请选择：

1. Merge 回 <base-branch>（本地合并）
2. Push 并创建 Pull Request
3. 保留当前分支（之后再处理）
4. 丢弃这个分支的工作
```

**Detached HEAD:** 展示 3 个选项（无 Merge）：

```
1. Push 为新分支并创建 PR
2. 保留
3. 丢弃
```

### 步骤 5: 执行选择

| 选项 | 操作 |
|------|------|
| **1. Merge** | `git checkout <base> && git pull && git merge <branch>` → 验证测试 → 清理工作树 → 删除分支 |
| **2. Push + PR** | `git push -u origin <branch> && gh pr create` → **保留工作树**（还需要迭代 PR） |
| **3. 保留** | 什么都不做，告知分支和工作树位置 |
| **4. 丢弃** | 🔴 **必须精确确认**: 用户输入 "discard" 后才执行 → 清理工作树 → force delete 分支 |

### 步骤 6: 清理工作区

**只在选项 1 和 4 时执行。** 选项 2 和 3 保留工作树。

```bash
cd <main-repo-root>
git worktree remove <worktree-path>
git worktree prune
```

**安全原则**: 只清理 `.worktrees/`、`worktrees/` 下的工作树。其他位置的工作树不要动（可能是宿主环境创建的）。

---

## 快速参考

```bash
# 创建隔离工作区
git worktree add .worktrees/my-feature -b my-feature
cd .worktrees/my-feature

# 完成时合并
git checkout main
git pull
git merge my-feature
git branch -d my-feature
git worktree remove .worktrees/my-feature
git worktree prune

# 完成时创建 PR
git push -u origin my-feature
gh pr create --title "feature" --body "summary"

# 完成时丢弃（需确认）
git branch -D my-feature
git worktree remove .worktrees/my-feature
git worktree prune
```

## 常见陷阱

- **不要在尚未 `cd` 出工作树的情况下执行 `git worktree remove`** — 会失败
- **先合并成功再清理工作树** — 顺序颠倒会导致丢失工作
- **选项 4 必须用户输入 "discard" 确认** — 不能只是回答"是"
- **先检查 `GIT_DIR != GIT_COMMON` 再创建** — 避免在工作树内嵌套工作树
- **`git worktree prune` 自愈** — 删除后运行清理脏注册

---

## 吸收来源

| 项目 | Stars | 吸收内容 | 日期 |
|------|-------|---------|------|
| **obra/superpowers** | 195K⭐ | using-git-worktrees（隔离工作区全流程）+ finishing-a-development-branch（完成任务决策矩阵） | 2026-05-18 |

*Git Workflow Complete v1.0 — 吸收自 obra/superpowers (2026-05-18)*
