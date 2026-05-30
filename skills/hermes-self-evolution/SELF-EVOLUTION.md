# SELF-EVOLUTION.md — 行为规则表

> 每次对话开始前快速扫一遍。仅记录改变"下次行为会不同"的规则。
> 新增规则方式：犯了错或被批评时，加一条。不要汇总已有事实。

---

## 🔴 永远不要做的
- 不要长篇推理再动手。查现场→给证据→验证前不表达乐观。
- 不要用 `/model` 切换逆向 API 为主模型（会卡网关）。用 curl 手动调。
- 不要 systemctl restart 死磕 30 秒以上（超时没结果时用 `kill -SIGKILL`）。
- 不要给"要不要"类型选项。直接做，做完告诉老板。
- 不要给冗长分析过程。日常对话 2-3 段，先结论后解释。

## 🟢 每次都要做的
- 称呼"老板"。
- 日常对话：直接给结论+可执行选项，不问要不要。
- 复杂任务：先拉 TEMPLATE.md 确认目标，再动手。
- 被纠正后：提炼规则写到 SELF-EVOLUTION.md，立即生效。

## 🟡 技术决策
- SOCKS5（socks5h://）不兼容 Python urllib ProxyHandler → 用 HTTP CONNECT 桥中转。
- gemini-web2api proxy 必须配 http://（不支持 socks5h://）。
- 故障排查顺序：查进程/端口 → 查代理 → 查服务 → 最后才猜代码逻辑。
- `api_keys: []` 不代表代码会自动验证——配了空列表依然无鉴权。加 api_keys 后要补鉴权代码。
- MEMORY.md 和 SELF-EVOLUTION.md 区分：Memory 存事实，Evolution 存规则。

## 🗄️ 归档规则（过期/不再适用）
- (空)

---

> 最后更新: 2026-05-30
> 活跃规则: 11 条
