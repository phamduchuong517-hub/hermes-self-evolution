---
name: external-system-learning
description: 外部系统学习吸收进化方法论 - 三阶段法 (学习→集成→融合) + 实证验证 + 轻量级优先，从 GitHub 项目/开源系统中提取高价值能力并实施吸收
version: 1.5.0
category: self-improvement-core
tags: [learning, integration, evolution, capability-analysis, empirical-verification]
---

# 🧬 外部系统学习吸收进化方法论

**核心**: 三阶段法 (学习 → 集成 → 融合) + 实证验证 + 轻量级优先

## ⏱️ 时间预算与范围控制（2026-05-26 新增 ⭐）

**核心原则: 用户的"学习吸收"不等于"无限深度探索"。** 必须给每个吸收任务设置硬性时间边界和完成标准。

### 时间预算

| 任务类型 | 预算 | 信号 | 完成标准 |
|---------|------|------|---------|
| 读 README + 提取概要 | **10 min** | 3-5个文件读取 | 200字摘要 |
| 深度分析（读源码+架构） | **20 min** | 10+文件读取 | 能力矩阵 + P0/P1清单 |
| 实施吸收（写脚本+更新技能） | **30 min** | 创建脚本 + 测试 | 可运行脚本 + 验证通过 |
| "继续吸收剩余内容"等模糊任务 | **15 min** | 读核心内容后 | 向用户报告已完成+剩余 |

### 范围控制规则

**当任务描述为"继续吸收剩余内容"、"学习进化"等模糊指令时：**

1. **立即明确范围**: 在第一个回复中就问"核心读哪个文件？只做概要还是需要编写代码？"
2. **不要一次塞多个子任务**: Thinking-Claude 吸收 + agency-orchestrator 研究 + 群聊排查 = 3个独立任务，要分拆或让用户选一个
3. **任务漂移检测**: 当当前操作与最初目标偏离时，主动停止并确认"这和吸收的关联是什么？要切回来吗？"
4. **完成标准预定义**: 读任何项目前先定义"读到什么程度算完成"——读README? 读架构? 读核心代码? 还是全部?

### 用户偏好：结论优先（2026-05-29 新增 ⭐）

**用户明确表达：不喜欢冗长分析报告，期望直接看结论+可执行选项。**

这意味着在吸收/调研任务中：
1. **第一原则：先说结论** — 用一两句话给出最终判断（值得装？不值得装？为什么？）
2. **详细分析放在附录或 reference 文件** — 不要在主回答中堆砌原始数据
3. **可执行选项优先** — 每个结论后面紧跟"你要做什么"
4. **结构化的"深度分析"可以有，但只针对用户明确要求时** — 不要默认输出长篇报告
5. **表格对比可以，但要克制** — 只给关键对比维度，不要给所有维度

**经验来源**: 用户多次在收到长篇分析后反馈"直接给结论就行"。

### 模型速度意识

当前模型 DeepSeek Chat 输出速度 ~30-45 tok/s。每个工具调用完整 round-trip (思考+生成+工具返回) 约 5-15 秒。

| 调用量 | 纯生成时间 | 实际耗时(含网络) |
|--------|-----------|----------------|
| 20次工具调用 | ~5 min | ~8-12 min |
| 50次工具调用 | ~12 min | ~15-30 min |
| 200+次工具调用 | ~50 min | ~1-2h |

### 自检规则

执行"吸收/学习"类任务时，每 **10个工具调用** 检查一次：
- 是否还在主任务路径上？ → 偏离了就停
- 是否超过时间预算？ → 超了就报告
- 用户是否还需要这些信息？ → 不要假设继续有价值

### 经验来源

- **2026-05-25 Thinking-Claude 吸收**: 15小时 370条消息 → 包含3个无关子任务，没有边界控制，没有完成标准
- **用户反馈**: "完成任务时间太长" + "模型算力不行" → 范围控制缺失 + 模型速度认知缺失

---



**效率**: 三阶段能力增强法效率提升 9-14 倍 (实际 3 小时 vs 预期 28-42 小时)

**来源**: 基于 OpenClaw 吸收经验 + PentAGI 吸收实践 (2026-04-26)

---

## 触发条件

以下任一情况触发本技能：
- 用户要求"学习 X 项目" / "吸收 X 能力"
- 用户要求"搜索能提高能力的资源"
- 系统检测到能力差距 (capability gap)
- 发现高价值外部系统 (1K+ stars, 直接可用能力)

---

## 三阶段执行流程

### 阶段 1: 学习 (Learn) - 1-2 小时

**目标**: 深度分析外部系统核心能力，提取可吸收清单

#### 步骤 1.1: 信息收集

**优先使用 GitHub API**（比 web_search 可靠）：

```bash
# 0. gh CLI (最稳定 — 已认证，不走 Cloudflare) — 优先使用
gh api repos/{owner}/{repo} --jq '{stars, lang, created, desc, license}'
gh api repos/{owner}/{repo}/contents/ --jq '.[].name'
gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d

# 1. 备选：GitHub API via curl (当 gh 不可用时)
curl -s --max-time 15 "https://api.github.com/repos/{owner}/{repo}"
curl -s --max-time 15 "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
```

**⚠️ 关键经验**:
- gh CLI 优先于 curl（绕过 Cloudflare 限流，更稳定）
- GitHub API 在隔离环境中可靠，web_search 经常超时
- 优先分析: README > 配置文件 > docker 编排 > 核心代码
- 记录: Stars, Forks, 语言, 许可证, 创建时间, 最近更新

#### 步骤 1.2: 核心能力矩阵分析

创建能力对比矩阵:

| 能力维度 | 外部系统实现 | 我们当前状态 | 学习价值 |
|---------|-------------|-------------|---------|
| 能力 A | 实现细节 | ✅/❌ | ⭐⭐⭐⭐⭐ |
| 能力 B | 实现细节 | ✅/❌ | ⭐⭐⭐⭐ |

**评估标准**:
- ⭐⭐⭐⭐⭐: 我们没有的 + 直接可用 + 高价值
- ⭐⭐⭐⭐: 我们有但可改进的
- ⭐⭐⭐: 特定场景有用的
- ⭐⭐: 低价值/高成本
- ⭐: 不值得学习

#### 步骤 1.3: 提取可吸收能力清单

创建优先级矩阵:

| 优先级 | 能力 | 价值 | 难度 | ROI |
|-------|------|------|------|-----|
| P0 | 能力 A | 高 | 中 | 高 |
| P1 | 能力 B | 高 | 低 | 高 |
| P2 | 能力 C | 中 | 高 | 中 |

**输出**: `memory/{project}-analysis-{date}.md`

---

### 阶段 2: 集成 (Integrate) - 2-4 小时

**目标**: 实施高价值能力 (P0 + P1)

#### 步骤 2.1: 环境检查

```bash
# 检查 Python 版本和可用库
python3 --version
pip3 list | grep -i "vector\|embed\|chroma\|faiss"

# 检查工作空间
ls -la workspace/
```

#### 步骤 2.1.5: 云服务器 pip 安装 (新增)

**云服务器环境特殊挑战** (PEP 668 externally-managed-environment):

```bash
# 标准安装
pip install --break-system-packages <package>

# 遇到系统包冲突 → --ignore-installed
pip install --break-system-packages --ignore-installed <package>

# 依赖地狱 → 先装基础包，再按需装依赖
pip install --break-system-packages --no-deps <package>
# 然后逐个安装缺失依赖
```

**⚠️ 关键经验**:
- 先 `--no-deps` 安装基础包，再按需补依赖，比一次性安装成功率高
- 接受版本警告（如 rich>=15 vs rich<15），只要两个包都能工作
- 每次安装后验证，不要批量安装后才发现失败
- 云服务器 GitHub 网络不稳定，git clone 失败时用 zipball 下载

**详细指南**: 参见 `references/cloud-server-pip-installation.md`

#### 步骤 2.2: 轻量级优先实施原则

**核心原则**: 先用简单方案解决 80% 问题，再考虑完整实现

| 方案 | 适用场景 | 示例 |
|------|---------|------|
| 轻量级 (推荐) | 立即可用，无额外依赖 | 关键词搜索 vs 向量搜索 |
| 完整实现 | 需要高性能/高准确率 | ChromaDB/FAISS |

**PentAGI 吸收实例**:
- 向量记忆: 先用关键词搜索 + 同义词扩展 (轻量级)
- 上下文摘要: 先实现关键句子提取 (轻量级)
- 未来升级: ChromaDB/FAISS (完整实现)

#### 步骤 2.3: 实施并测试

```bash
# 1. 创建工具脚本
write_file scripts/{tool}.py

# 2. 修复路径问题 (相对路径 vs 绝对路径)
patch scripts/{tool}.py

# 3. 测试验证
execute_code: import and test the tool

# 4. 记录测试结果
write_file memory/{project}-absorption-report-{date}.md
```

**⚠️ 关键经验**:
- 路径问题是最常见的错误 (脚本目录 vs workspace 根目录)
- 必须实际测试，不能只写代码
- 记录测试数据和结果

**输出**:
- `scripts/{tool}.py` - 工具脚本
- `memory/{project}-absorption-report-{date}.md` - 验证报告

---

### 阶段 3: 融合 (Fuse) - 1-2 小时

**目标**: 与现有系统整合，自检验证吸收效果

#### 步骤 3.1: 整合到现有系统

- 检查与现有工具/技能的兼容性
- 更新配置文件
- 创建集成文档

#### 步骤 3.2: 自检验证

创建验证报告:

```markdown
# 吸收验证报告

## ✅ 吸收成果清单

### 1. 能力 A ✅ 已实施
- 文件: scripts/tool.py
- 功能验证: ✅ 搜索/添加/列表正常
- 测试结果: 具体数据

### 2. 能力 B ✅ 已实施
- 文件: scripts/tool2.py
- 功能验证: ✅ 通过
- 测试结果: 具体数据
```

#### 步骤 3.3: 更新记忆

- 保存到 `memory/{project}-absorption-{date}.md`
- 更新 MEMORY.md (如有空间)
- 记录经验教训

---

## 搜索策略 (GitHub 环境)

### 搜索类型：按任务区分

本技能覆盖两种搜索模式，根据目标选择：

| 搜索类型 | 目标 | 方法 | 产出 |
|---------|------|------|------|
| **🧩 技能吸收搜索** | 找单个高价值项目来吸收其代码/方法论 | 精确搜索 + deep dive | 吸收脚本 + 技能更新 |
| **🔭 技术调研搜索** | 了解某技术类别全景（API中转、Agent框架等） | 多关键词 + 全景对比 | 排行榜 + 对比表格 + 选型建议 |

两种模式不要混用 —— 调研不吸收、吸收不调研。

### 技术调研搜索（2026-05-24 新增）

**何时用**: 用户问"GitHub 上有什么 X 技术"、"搜一下 X 方案"、"找找 X 方向的开源项目"

#### 搜索流程

```bash
# Step 1: 宽泛搜索（确定主战场）
gh search repos "主关键词" --sort stars --limit 15 --json name,owner,description,stargazersCount,language,updatedAt,url

# Step 2: 变体搜索（覆盖细分方向）
gh search repos "变体关键词1" --sort stars --limit 8 --json ...
gh search repos "变体关键词2" --sort stars --limit 8 --json ...

# Step 3: 当 gh search 不理想时，直接用 gh api
curl -s "https://api.github.com/search/repositories?q=关键词&sort=stars&order=desc&per_page=15" \
  | python3 -c "..."
```

#### 关键词策略（调研模式）

不是搜一个词就够了。一个技术方向至少搜 3 组关键词：

| 方向 | 第一组（核心） | 第二组（细分） | 第三组（生态） |
|------|--------------|--------------|--------------|
| API 中转 | `api 中转` | `LLM API gateway proxy` | `one-api New API` |
| Agent 框架 | `AI agent framework` | `autonomous agent` | `agent orchestration` |
| 记忆系统 | `LLM memory` | `agent memory persistent` | `memory knowledge graph` |

#### 输出格式

调研结果输出结构化排行榜：

```markdown
## 📡 [技术类别] — GitHub 项目全景

### 🥇 第一梯队（万星级）
### 🥈 第二梯队（千星级）  
### 🥉 第三梯队（百星级/专项方案）

| 项目 | ⭐ | 语言 | 特点 |
|------|:--:|:----:|------|
| **owner/repo** | N⭐ | Lang | 一句话关键点 |
```

#### ⚠️ 调研陷阱

- **不要混合调研和吸收** — 调研的目的是了解全景，不是决定安装哪个项目
- **不要在调研中 deep dive** — 每个项目只看 README 摘要，不要读源码
- **不要承诺安装/配置** — 调研结论是"选型参考"，用户自己决策
- **区分"项目不存在"和"搜索结果不精准"** — 中文关键词搜不到时换英文试试

### 优先顺序

```
0. gh CLI (最稳定 — 已认证，不走 Cloudflare)
   ├── gh search repos "query" --sort stars    # 搜索仓库 (gh 1.0+)
   ├── gh api "search/repositories?q=..."       # 搜索 (更灵活)
   ├── gh api "repos/{owner}/{repo}"             # 仓库信息
   └── gh api "repos/{owner}/{repo}/readme"     # README

1. GitHub API via curl (备选)
   ├── repos API: 仓库信息
   ├── search API: 搜索仓库
   ├── users API: 用户/组织信息
   └── contents API: 文件内容

2. 直接文件下载 (备选)
   ├── raw.githubusercontent.com
   └── 需要处理超时

3. web_search (最后)
   └── 在隔离环境中经常超时
```

**⚠️ 关键经验**: `curl` 在隔离云服务器上经常因 DNS/网络超时而失败，`gh api` 直接走已认证的 Git 协议通道，稳定性明显更高。优先使用 `gh api`。

**⚠️ 命令行工具变化**: `gh search repos` 是 gh CLI 原生搜索命令（1.0+ 版本支持），更简洁但功能有限；`gh api "search/repositories?q=..."` 更灵活（可控制排序、per_page、jq 输出）。gh 没有对应结果时自动降级到 curl 或 gh api。

### 搜索超时处理策略

**不要批量并行搜索！** 超时的请求会 block 整个流程。

```
❌ 错误做法: 同时发起 4 个 curl 搜索，一个卡住就全部卡住
✅ 正确做法: gh api 逐一搜索，每搜到一个就判断是否有价值
   └─ 有价值 → 立即进入深度分析，分析完再搜下一个
   └─ 无价值 → 跳过，搜下一个方向，不纠结耗时
```

同样适用于 **execute_code 脚本** 中的批量搜索——多个 `terminal()` 调用在脚本中串行执行，会因单个超时拖垮整个 300s 超时上限。改为在外部逐个调用 `terminal()` 独立判断。

### gh CLI 搜索示例

```bash
# gh api 会自动使用已认证的 token，不走 Cloudflare 防护
gh api "search/repositories?q=agent+skill+lifecycle&sort=stars&order=desc&per_page=5" --jq '.items[] | "\(.stargazers_count)⭐ | \(.full_name) | \(.description[:90] // "None") | \(.updated_at[:10])"'

# 获取仓库内容
gh api "repos/{owner}/{repo}/readme" --jq '.content' | base64 -d

# 获取目录结构
gh api "repos/{owner}/{repo}/contents" --jq '.[].name'
```

### GitHub API 常用端点 (curl 版本，当 gh 不可用时)

```bash
GET /repos/{owner}/{repo}                    # 仓库信息
GET /repos/{owner}/{repo}/contents/{path}    # 目录/文件
GET /orgs/{org}/repos?sort=stars             # 组织仓库
GET /search/repositories?q={query}           # 搜索仓库
GET /users/{username}                        # 用户信息
GET /rate_limit                              # 速率限制
```

---

## 能力评估框架

### 价值评估维度

| 维度 | 说明 | 权重 |
|------|------|------|
| 直接可用性 | 能否直接复制/适配 | 30% |
| 互补性 | 是否弥补现有能力缺口 | 25% |
| 实施成本 | 时间/依赖/复杂度 | 20% |
| 长期价值 | 未来可扩展性 | 15% |
| 风险 | 安全/维护/兼容性 | 10% |

### ⚠️ Star 数陷阱 — 低 Star ≠ 低价值

**不要仅凭 Star 数判断项目价值。** 以下情况会导致 Star 数偏低但实际价值极高：

| 情况 | 实例 | 识别方法 |
|------|------|---------|
| **继承自更高层项目** | skill-conductor (89⭐) 评估体系直接来自 Anthropic 官方 skill-creator | 读 README 的 "Synthesized from" / "Inspired by" 章节 |
| **细分领域专家** | 瞄准特定痛点的小众工具 | 检查 Python 代码实际完成度，而非 Star 数 |
| **新项目但质量好** | 发布 <30 天但代码完整 | 检查 commits 活跃度、代码完整性、文档质量 |
| **企业/学术产出** | Facebook Research / Meta 的非热门项目 | 检查 owner 类型 (organization, user) |

**识别规则**:
1. README 明确写明吸收了哪个高 Star 项目 → 先查上游项目的质量
2. 代码不是 README 吹牛即可验证 — 检查实际文件内容而非标题
3. 代码完整度 > Star 数 — 有完整 scripts/、agents/、references/ 目录结构 > 只有 README 的空壳

**2026-05-17 教训**: skill-conductor (89⭐) 的评估体系直接来自 Anthropic，质量和实用性远超同 Star 数级别的项目。

### 优先级决策矩阵

```
高价值 + 低成本 = P0 (立即实施)
高价值 + 高成本 = P1 (规划实施)
低价值 + 低成本 = P2 (有空再说)
低价值 + 高成本 = 跳过
```

---

## GitHub 热榜/推荐项目验证流程

**触发**: 用户要求分析 GitHub "热榜"、"推荐"、"视频/博客提到的项目"

**核心原则**: **永远不信任第三方声称，必须通过 GitHub API 逐一验证**

### 验证步骤

```bash
# 1. 搜索项目 (批量)
for p in project1 project2 project3; do
  curl -s "https://api.github.com/search/repositories?q=$p&sort=stars&order=desc&per_page=3"
done

# 2. 获取精确仓库信息
curl -s --max-time 10 --connect-timeout 5 "https://api.github.com/repos/{owner}/{repo}"

# 3. 提取关键字段
grep -E '(stargazers_count|forks_count|created_at|pushed_at|language|description)'

# 4. 验证 README (确认功能描述)
curl -s --max-time 10 "https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
```

### ⚠️ 常见虚假信息模式

| 虚假模式 | 实例 | 识别方法 |
|----------|------|---------|
| **Star 数混淆** | "本周+16,579" 实际是周增量，非总量 | 查 API `stargazers_count` 对比 |
| **语言夸大** | "基于 Rust" 实际是 Python/JS | 查 API `language` 字段 |
| **功能虚构** | "专注金融深度研究" 实际是普通爬虫 | 读 README，查实际代码 |
| 项目不存在 | 热榜列出但 GitHub 搜不到 | 精确搜索 + 模糊搜索双验证 |
| 作者冒充 | 声称 "OpenAI 推出" 实际是个人项目 | 查 `owner.login` 和 `owner.type` |
| 付费伪装免费 | 声称开源实际是付费课程/私有仓库 | 查 `private` 字段，尝试 clone |
| **新项目冒充** | 声称"最近两周新发布"实际是半年前/一年前的老项目 | 查 `created_at` 字段，对比声称的发布时间；一个2月创建的项目不可能在5月是"新发布" |
| **Star 增量混淆** | "本周暴涨 X⭐"但项目是旧项目被社区重新发现，而非新项目本身优秀 | 先查 `created_at` 确认新旧，再对比 `stargazers_count` 看真实热度 |

### 验证清单

- [ ] GitHub API 搜索找到匹配仓库
- [ ] Star 数与声称一致（注意"周增量"≠总量）
- [ ] 语言与声称一致
- [ ] README 描述与声称功能一致
- [ ] 仓库为 public（非付费伪装）
- [ ] 创建时间合理（非旧项目重新包装，检查 `created_at` 是否确实在声称的时间段内）

### 输出格式

```markdown
## 验证结果

| # | 项目 | 声称 | 实际验证 | 可信度 |
|---|------|------|----------|--------|
| 1 | project | 描述 | ⭐X | ✅/⚠️/❌ |
```

**教训来源**: 2026-05-10 GitHub 热榜 Top10 验证实践

---

## 常见陷阱与规避

| 陷阱 | 表现 | 规避方法 |
|------|------|---------|
| 路径错误 | FileNotFoundError | 使用绝对路径或相对 workspace 根目录 |
| 依赖缺失 | ImportError | 先检查环境再实施 |
| 过度设计 | 追求完整实现 | 轻量级优先，先解决 80% 问题 |
| 不验证 | 只写代码不测试 | 必须实际测试并记录结果 |
| 重复建设 | 已有能力重新做 | 先验证现有系统能力 |
| 记忆溢出 | 无法保存到 memory tool | 保存到文件，定期清理旧记忆 |
| **SKILL.md 声称需验证** | 文档写"已配置"但实际未配置 | 安装后必须验证环境变量/配置文件 |
| **代码 ≠ 价值**: SKILL.md 可能比 Python 代码更有值 | 大量 Python 文件但大部分是 TODO 占位符 | 分析每个文件的实际完成度，只复制有价值的部分 |
| **热榜/视频信息不可信** | "本周新增 Star"、"基于 Rust" 等声称与实际不符 | 必须通过 GitHub API 逐一验证，不信任第三方来源 |
| **企业级 ≠ 个人需要** | 高 Star 项目明确标注 "enterprise-grade" | 对照用户偏好过滤（个人优先，企业功能不考虑） |
| **搜新项目前不盘点现有工具** (⚠️ 2026-05-29) | 推荐了当前场景不适用的技术（AnyTLS给QUIC）；漏了当前工具自带的未启用功能（端口跳跃） | 详见 `references/audit-before-search.md` — 分析前先做4步盘点：现有工具未用功能 → 可调参数 → 结构性问题 → 报警信号

---

## 输出文件规范

```
memory/
├── {project}-analysis-{date}.md          # 能力对比分析
├── {project}-absorption-plan-{date}.md   # 实施方案
├── {project}-absorption-report-{date}.md # 验证报告
└── vector-index.json                     # (如适用) 数据文件

scripts/
├── {tool1}.py                            # 工具脚本 1
└── {tool2}.py                            # 工具脚本 2
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **1.5.0** | **2026-05-22** | **修复示例矛盾**: Step 1.1 信息收集命令从 curl 改为 gh api 优先；更新"文档吸收=僵尸吸收"为三形态真吸收（代码/架构/方法论） |
| **1.4.0** | **2026-05-22** | **新增完整系统架构模式吸收**: 五步法 + 能力矩阵 + P0/P1/P2 优先级 + 不可吸收项标注。经验来源: tinyhumansai/openhuman (25K⭐) 深度架构分析。参考文档: `references/openhuman-architectural-analysis.md` |
| 1.2.0 | 2026-05-17 | 搜索策略重构: gh CLI 优先于 curl + 搜索超时处理策略 + Star 数陷阱识别规则 (低 Star ≠ 低价值) + 逐一搜索优于批量并行 |
| 1.1.0 | 2026-05-10 | 新增 GitHub 热榜验证流程、虚假信息模式识别、批量验证脚本 |
| 1.0.0 | 2026-04-26 | 初始版本 - 基于 PentAGI 吸收实践 |

---

## 吸收实现的关键原则 (v1.5 更新)

**代码吸收 = 可执行的真吸收，方法论吸收 = 可传承的真吸收，架构模式吸收 = 可复用的真吸收。**

注意吸收形式的验收标准不同：

| 吸收形式 | 产出物 | 验收标准 |
|---------|-------|---------|
| **代码脚本** | scripts/*.py | `python3 script.py --help` 可用 |
| **配置/模板** | evals.json / templates/* | 可被代码脚本消费 |
| **架构模式** | 更新 SKILL.md 架构章节 | "我们的技能是否体现了更好的架构设计？" |
| **方法流程** | 更新 SKILL.md 步骤 | 按步骤走能复现结果 |

⚠️ 纯"概念笔记"（记录理念而没有可复现步骤/可执行代码/可参考架构决策）不算真吸收。

### 脚本标准清单
每个吸收脚本必须：
- ✅ 有 `argparse` 参数解析（CLI 可用）
- ✅ 有 `--verbose` 详细输出
- ✅ 有 `--output` 输出到文件
- ✅ 返回结构化 JSON（可被其他工具消费）
- ✅ 纯 Python stdlib，零外部依赖（除非真需要）
- ✅ 函数有 docstring 说明用途
- ✅ 验证测试可运行（python3 scripts/xxx.py 不报错）

### 吸收类型

| 类型 | 说明 | 示例 | 算真吸收？ |
|------|------|------|:----------:|
| **代码脚本** | 可执行的 Python/Shell 脚本 | grader.py | ✅ 代码吸收 |
| **配置/模板** | 可直接使用的配置文件 | evals.json | ✅ 配置吸收 |
| **架构模式** | SKILL.md 扩展了架构章节，体现了更好的设计 | 三棵树记忆架构 | ✅ 架构吸收 |
| **方法流程** | SKILL.md 给出了可复现的步骤序列 | 五步法 | ✅ 方法论吸收 |
| **概念笔记** | 记录了理念但没有产出 | HyperAgents 理念 | ❌ 纯笔记 |

**2026-05-17 教训**: token-optimization v2.0 吸收了 headroom 的能力，但只写了文档描述（内容路由压缩、CCR）没有写可执行脚本——本质上还是僵尸文档。而 skill-lifecycle-manager v3.0 附带了 3 个可运行脚本（grader.py 262行/comparator.py 297行/analyzer.py 226行），是真正的代码吸收。

**2026-05-22 教训**: tinyhumansai/openhuman 的架构模式吸收（self-improvement-core v5.0）没有创建独立新脚本，而是扩展了现有技能（SKILL.md 升级 + knowledge-memory.py 工具）。架构吸收的检验标准是"技能文档是否体现了这个更好的架构"，不是"有没有新脚本"。

---

## 完整系统架构模式吸收（v1.4 新增 ⭐）

**2026-05-22 经验**: 分析 OpenHuman（25K⭐ Rust 桌面 AI 系统）时发现：有些项目不是单一"技能"，而是**完整系统**。不能安装它，但可以吸收它的**设计模式和架构决策**。

### 触发条件

分析目标是**完整系统**（桌面应用、框架、平台）而非单功能库/技能包时：
- 项目有完整 REST/事件架构、集成层、存储层
- 项目是一个"产品"而非"技能库"
- 与我们的系统有功能重叠，但不兼容到可以直接安装

### 架构模式吸收的五步法

```
Step 1: 系统架构拆解
  将目标系统按层级分解：基础设施层 → 核心引擎层 → 集成层 → UI层
  识别哪些层对我们的系统有参考价值

Step 2: 能力差矩阵
  逐层对比：目标系统的每项能力 vs 我们当前状态的差距
  标注：✅ 我们有 / ⚠️ 我们有但弱 / 🔴 我们没有

Step 3: 分辨可吸收 vs 不可吸收
  可吸收（设计模式/架构决策/API设计）：
  ├── P0: 能直接补最大短板的模式
  ├── P1: 有明显改进空间且实施成本低的
  └── P2: 好的但可以后面再做的
  
  不可吸收（场景不匹配/许可证不兼容/语言依赖）：
  └── 明确标注原因，避免未来重复分析

Step 4: 模式提取 → 动作列表
  每个可吸收模式写清楚：
  现有实现 vs 目标实现 vs 改进方案
  具体动作：更新哪条技能、改哪个文件、加什么功能

Step 5: 优先级排序 + 执行
  P0 → 立即更新相关技能（扩展方法论或加逻辑）
  P1 → 记录待办，标记触发条件
  P2 → 记备注
```

### 实例：OpenHuman 架构模式吸收（2026-05-22）

| 层级 | 能力 | 他们 | 我们 | 差距 | 优先级 |
|------|------|------|------|------|--------|
| **核心引擎** | 记忆系统 | 三棵树(Source/Topic/Global) + SQLite + 层级摘要 + Obsidian 兼容 | 平面MEMORY.md + 每日文件 | 🔴 巨大 | P0 |
| **核心引擎** | 知识图谱 | graph_upsert() + 实体关系提取 | 无 | 🔴 无 | P0 |
| **核心引擎** | 事件总线 | 订阅-发布，模块解耦 | 无（同步调用） | 🔴 无 | P1 |
| **核心引擎** | 后台思考循环 | Subconscious Loop：定期评估任务，skip/act/escalate 决策树 | 心跳(HEARTBEAT_OK) + cron | 🔴 大 | P1 |
| **集成层** | OAuth 集成 | 118+ 第三方，20分钟自动拉取 | 手动配置，无自动拉取 | 🔴 场景不同 | 跳过 |
| **工具层** | Token压缩 | TokenJuice：三层规则覆盖（内置+用户+项目） | token-optimization v2.0 (CCR) | ⚠️ 各有千秋 | P2 |
| **UI层** | 桌面客户端 | Tauri + 吉祥物 + 音视频会议 | CLI/QQBot | 场景不同 | 跳过 |
| **许可** | GPL-3.0 | 严格，不能直接复制代码 | MIT | 法律限制 | 跳过 |

**最大教训**: 平面文件 vs 结构化知识库是记忆系统最根本的缺陷。OpenHuman 的记忆树架构（确定性子分数分块 + 三级摘要树 + 知识图谱 + SQLite）是目前最可行的参考实现。

### 完整系统吸收 vs 单一技能吸收的区别

| 维度 | 完整系统吸收 | 单一技能吸收 |
|------|------------|-------------|
| 目标 | 提取设计模式 + 架构决策 | 提取可执行脚本 + 方法论 |
| 输出 | 扩展现有能力技能的架构部分 | 创建新脚本/新技能 |
| 检验标准 | "我们的技能文档是否体现了这个更好的架构设计？" | "脚本能跑起来吗？" |
| 常见结果 | P0/P1/P2 优先级矩阵，分批执行 | 一次性代码创建+验证 |

### 完整系统分析工具

```bash
# 1. 仓库信息 + 目录结构扫描（一发获取）
gh api repos/{owner}/{repo} --jq '{stars, lang, created, license, topics, forks}'
gh api repos/{owner}/{repo}/contents/ --jq '.[].name'

# 2. 子目录扫描（多次调用）
gh api repos/{owner}/{repo}/contents/src 2>/dev/null --jq '.[] | "\(.type):\(.name)"'

# 3. 关键架构文件 (Cargo.toml / package.json / Dockerfile)
gh api repos/{owner}/{repo}/contents/Cargo.toml --jq '.content' | base64 -d | head -200

# 4. 文档文件（README, docs/ 目录, gitbooks/ 目录）
gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d
```

**⚠️ 经验**: 
- `gh api` 比 `curl` 稳定得多（绕过 Cloudflare 限流）
- README 能读完就不要去解析 Gitbook 文档——docs.tinyhumans.gitbook.io 这类外部文档在云服务器上经常超时
- 系统分析的关键是**识别哪些层是可移植的设计模式**而非代码——Rust 代码不能直接抄，但事件总线、三棵树记忆、三层规则覆盖这些设计思想通用

---

**2026-05-17 经验**: 从 GitHub 吸收 8 个项目后，对比本地技能发现 diagnose 和 systematic-debugging 有 ~40% 重叠。决策模型如下：

**2026-05-29 经验**: 区块链技术全景学习（约30+ API调用，4次大范围搜索）成功产出 skill + reference。关键成功因素：每一步都有明确目的（不是漫无目的探索），中途有阶段性输出（分类清单/对比表），最终产出直接是可用 skill。证明"时间预算+范围控制"的核心不是限制总时长，而是确保每一步都有清晰的下一步。

### 新能力 vs 融合的 3 步判断

```
Step 1: 找本地重叠技能
  └─ 无重叠 → 🆕 独立保留（如 grill-with-docs）
  └─ 有重叠 → Step 2

Step 2: 分析重叠比例和阶段位置
  └─ <30% 或 不同阶段 → 🆕 独立保留（如 doubt-driven-development vs requesting-code-review：事中 vs 事后）
  └─ ≥30% 且 同阶段 → 🔄 融合（如 diagnose vs systematic-debugging）

Step 3: 融合后检查
  └─ 原技能核心内容是否完全覆盖？→ 是 → ❌ 删除原技能
  └─ 原技能有独有文件/脚本？→ 保留文件引用，仍删除技能本体
```

### 阶段对比表（用于 Step 2 判断阶段）

```
编码前 → 编码中 → 编码后 → 提交前
  │         │         │        │
grill     doubt      diagnose  code-review
(with-docs)  (DDD)   (回路构建) (完整验证)
```

同一阶段重叠≥30% → 融合；不同阶段不管重叠多少 → 独立保留。

### 融合后的 5 轴评分验证

融合后对原技能做 5 轴评分，如果总分 <25 → 直接删除。示例：

```
对 diagnose 的评分（融合后）:
Discovery:  2/10 (触发条件已被 systematic-debugging 覆盖)
Clarity:    3/10 (核心内容已转移到 systematic-debugging)
Efficiency: 1/10 (多余技能浪费查找时间)
Robustness: 2/10 (独立存在导致用户困惑选哪个)
Completeness: 3/10 (只剩 HITL 脚本)
总分: 11/50 → ❌ 删除级别
```

---

## 相关技能

- `self-improvement-core` - 自我进化核心 (主动能力研究部分)
- `capability-gap-analysis` - 能力差距分析
- `empirical-system-analysis` - 实证系统分析
- `external-ai-capability-analysis` - 外部 AI 系统能力对比
- `github-skill-absorption` - 具体的搜索→分析→代码实现→验证四阶段流程

---

*External System Learning Methodology v1.1.0*
*Created: 2026-04-26 | Updated: 2026-05-05 | Based on PentAGI + world2agent absorption practice*
