# Design Principles

## Principle 1: The Minimum Viable Evolution

**"One file + one prefill instruction = complete evolution loop."**

不要混淆"进化"和"复杂性"。Agent 自我进化只有三个要素：

1. **规则存储** — Agent 可以读取的规则表
2. **强制扫描** — 每次回应前确保读取规则表
3. **规则写入** — 被纠正后写入新规则

这就是全部。不需要向量数据库、memory blocks、子 Agent、反思循环。

## Principle 2: Human Corrections > AI Reflection

**"最精准的改进来自人类的纠正，而不是自动生成的幻觉改进。"**

学术方案（Reflexion、Voyager）假设 Agent 可以自我反思并生成有效的改进策略。在现实中：

- Agent 的"自我反思"经常产生**幻觉改进**（"我应该更友好"——然后开始说废话）
- Agent 的"自动规则生成"常常**误判根因**（"因为超时"→其实是因为配置错了）
- 自动反思需要 **10x 以上的 token 成本**，而用户一句批评就能定位根因

所以：**用户纠正 → 唯一可靠的进化信号。**

## Principle 3: Prefill Over Prompt

**"Prefill 指令强制执行优化规则。Prompt 只是‘建议’。"**

- Prompt 中的指令：Agent 可以选择忽略
- Prefill（system prompt 末尾，不可见的指令）：Agent 必须遵循

这不是技术限制，是 LLM 的行为特性。Prefill 的强制力远高于 prompt 中的建议。

## Principle 4: Rules Are Unit Tests for Behavior

规则表 = Agent 行为的单元测试。
- 被纠正一次 = 一个测试用例失败
- 写一条规则 = 添加一个断言
- 下次对话 = 运行测试

```python
# 这是 Agent 的"行为测试"伪代码
def test_agent():
    assert not "长篇推理" in response  # 规则1
    assert response.startswith("老板")  # 规则2
    # ...
```

每次纠正都是对行为模型的测试反馈。规则表就是累积的测试套件。

## Principle 5: Gradual Accumulation

**"从一条规则开始。规则多了就分文件。一来就建系统是灾难。"**

- 第 1 天：1 条规则
- 第 7 天：7 条规则
- 第 30 天：15 条规则（开始分文件）
- 第 90 天：25 条规则（分 2-3 个文件）

当规则到 30-50 条时，才需要考虑"系统化"——在此之前，一个 markdown 文件足够了。

## Principle 6: Token Efficiency

**"自我进化不应该比 Agent 本身更贵。"**

| 方案 | 每轮开销 | 年成本（日均100轮） |
|-----|---------|------------------|
| Letta memory blocks | 2K+ token | ~$365 |
| PraisonAI 多 Agent | 4K+ token | ~$730 |
| **本方案** | **~150 token** | **~$27** |

进化机制不应该消耗比实际工作更多的 token。如果自我进化比日常推理更贵，那就是过度工程。

## Principle 7: Deterministic Not Probabilistic

**"规则扫描是强制性的，不是建议性的。"**

- ❌ 靠 Agent 自己"记得"规则 → 概率性，不可靠
- ❌ 靠向量检索"可能"返回规则 → 概率性，不可靠
- ✅ prefill 指令强制扫描 → 确定性，可靠
