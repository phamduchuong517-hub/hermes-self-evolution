---
name: mcp-server-builder
description: 系统化构建生产级 MCP (Model Context Protocol) 服务器 — 设计、实现、测试、部署全流程。支持 TypeScript 和 Python 双栈。吸收自 superpowers-zh mcp-builder skill。
version: 1.0.0
source: jnMetaCode/superpowers-zh mcp-builder (2026-05-18 吸收)
category: software-development
license: MIT
---

# 🏗️ MCP Server Builder — 构建生产级 MCP 工具

## 适用场景

当需要创建一个新的 MCP 服务器工具，让 AI 助手（Hermes/Claude/Cursor 等）能通过 MCP 协议连接外部能力时使用。

---

## 1. 协议核心概念

MCP 定义三种原语：

| 原语 | 用途 | 选择原则 |
|------|------|---------|
| **Tools（工具）** | AI 主动调用的函数，有副作用 | 执行操作 → Tool |
| **Resources（资源）** | 只读数据源，用 URI 标识 | 读取数据 → Resource |
| **Prompts（提示词模板）** | 预定义交互模板 | 引导交互 → Prompt |

## 2. 项目结构

### TypeScript
```
my-mcp-server/
├── src/
│   ├── index.ts          # 入口，注册 tools/resources
│   ├── tools/             # 按功能拆分
│   ├── resources/
│   └── lib/               # 客户端封装
├── tests/
├── package.json
└── tsconfig.json
```
依赖: `@modelcontextprotocol/sdk` + `zod`

### Python
```
my-mcp-server/
├── src/my_mcp_server/
│   ├── server.py
│   ├── tools/
│   └── lib/
├── tests/
└── pyproject.toml
```
依赖: `mcp` + `pydantic`

## 3. Tool 设计原则

### 命名
- `snake_case`，动词开头：`search_users`、`create_issue`、`delete_file`
- 名称自解释，模糊命名导致 AI 误调用

### 参数
```typescript
server.tool("search_issues", {
  query: z.string().describe("搜索关键词"),
  status: z.enum(["open", "closed", "all"]).default("open").describe("状态筛选"),
  limit: z.number().min(1).max(100).default(20).describe("返回上限"),
}, async ({ query, status, limit }) => { ... });
```

- 每个参数有类型约束 + `.describe()` 描述
- 可选参数给默认值
- 用枚举代替布尔开关

### 描述
格式：**用途 + 返回内容 + 限制**
```typescript
server.tool("search_users",
  "根据姓名或邮箱搜索用户。返回 ID、姓名、邮箱列表。模糊匹配，最多 50 条。",
  schema, handler);
```

### 输出
- 结构化数据 → JSON
- 人类可读 → Markdown
- 格式: `{ content: [{ type: "text", text: "..." }] }`

## 4. 错误处理四原则

1. **不让服务器崩溃** — try/catch 包裹所有外部调用
2. **返回可操作错误** — 告诉 AI 问题是什么、能做什么
3. **使用 `isError: true`** — 让 AI 知道调用失败
4. **区分错误类型** — 参数错误/权限不足/资源不存在/服务不可用

```typescript
server.tool("get_user", { id: z.string() }, async ({ id }) => {
  try {
    const user = await db.getUser(id);
    if (!user) {
      return { content: [{ type: "text", text: `用户 ${id} 不存在` }], isError: true };
    }
    return { content: [{ type: "text", text: JSON.stringify(user, null, 2) }] };
  } catch (err) {
    return { content: [{ type: "text", text: `查询失败: ${err.message}` }], isError: true };
  }
});
```

## 5. 生命周期管理

```typescript
const db = await Database.connect(config.dbUrl);
await server.connect(new StdioServerTransport());
process.on("SIGINT", async () => {
  await db.disconnect();
  await server.close();
  process.exit(0);
});
```

关键：连接池 + 超时 + 优雅关闭。

## 6. 测试策略

### 单元测试 — 业务逻辑与 MCP 注册分离
```typescript
// tools/search.ts 导出纯函数
export async function searchUsers(query: string, limit: number) { ... }

// 独立测试
test("返回匹配结果", async () => {
  const results = await searchUsers("alice", 10);
  expect(results[0].name).toContain("Alice");
});
```

### 集成测试 — SDK Client 端到端
```typescript
const [clientT, serverT] = InMemoryTransport.createLinkedPair();
await server.connect(serverT);
const client = new Client({ name: "test", version: "1.0.0" });
await client.connect(clientT);
const result = await client.callTool("search_users", { query: "test" });
expect(result.isError).toBeFalsy();
```

### Inspector 交互式调试
```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

## 7. 安全要点

| 风险 | 防护 |
|------|------|
| SQL 注入 | 参数化查询 |
| 路径遍历 | 校验路径，禁止 `../` |
| 命令注入 | `execFile` 而非 `exec` |
| 密钥泄露 | 环境变量传入，不硬编码 |
| 敏感数据 | 日志脱敏，返回脱敏 |

## 8. 调试警告

> **MCP 用 stdio 通信，不能用 `console.log`，会破坏协议流！**

```typescript
// ❌ 错误
console.log("debug");
// ✅ 正确
console.error("[DEBUG]", info);
// ✅ 更好
server.sendLoggingMessage({ level: "info", data: "处理中" });
```

## 9. 常见问题

| 症状 | 原因 | 解决 |
|------|------|------|
| 启动无响应 | transport 未连接 | 检查 `server.connect()` |
| Tool 不出现 | 注册在 connect 之后 | 先注册再 connect |
| AI 不调用 Tool | 描述不清晰 | 改善名称和描述 |
| 参数总错 | Schema 不明确 | 添加 `.describe()` |
| 调用超时 | 外部服务慢 | 加超时和缓存 |

调试流程: Inspector 验证 → 手动调用 → 真实 AI 客户端测试。

## 10. 构建检查清单

- [ ] Tools vs Resources vs Prompts 分工明确
- [ ] Tool 命名 `动词_名词`，描述含用途+返回
- [ ] 参数简洁，可选参数有默认值
- [ ] 输入用 Zod/Pydantic 校验
- [ ] 外部调用有 try/catch + 超时
- [ ] 错误返回 `isError: true` + 可操作信息
- [ ] 不用 `console.log`（用 stderr / SDK 日志）
- [ ] 敏感数据走环境变量
- [ ] 单元测试覆盖核心逻辑
- [ ] 集成测试验证 MCP 协议交互
- [ ] Inspector 手动验证过
- [ ] README 含配置说明 + 客户端 JSON 示例

---

## 吸收来源

| 项目 | Stars | 吸收内容 | 日期 |
|------|-------|---------|------|
| **jnMetaCode/superpowers-zh** | 3.3K⭐ | mcp-builder 完整方法论（设计原则、测试策略、安全、部署） | 2026-05-18 |

*MCP Server Builder v1.0 — 吸收自 superpowers-zh/mcp-builder (2026-05-18)*
