# 环境适配：无 auto-memory-recorder / error-logger CLI

在 Hermes 环境中，`auto-memory-recorder` 和 `error-logger` 不是系统可调用的 CLI 命令。它们出现在 v4.3 / v5.0 SKILL.md 的"完整执行流程"中作为概念步骤。

## 在 Hermes 中的实际实现

### auto-memory-recorder before_conversation → 
1. `memory() action=stats` 获取当前记忆状态
2. 读取 `memory/YYYY-MM-DD.md`（如果存在）
3. 写入当天的 daily note 头

### auto-memory-recorder record_key_point → 
1. 调用 `memory(action='add', ...)` 写入持久记忆
2. 更新 `memory/YYYY-MM-DD.md`

### auto-memory-recorder after_conversation → 
1. 调用 `knowledge-memory.py ingest` 写入知识图谱（如可用）
2. 更新 `memory/YYYY-MM-DD.md` 的总结部分
3. 调用 `memory(action='add', ...)` 保存关键决策

### error-logger log → 
1. `write_file memory/errors/YYYY-MM-DD-错误日志.md` 追加错误
2. 可选：`knowledge-memory.py ingest error` 摄入到知识图谱
