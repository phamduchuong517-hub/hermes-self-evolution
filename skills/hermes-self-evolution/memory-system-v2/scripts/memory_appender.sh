#!/usr/bin/env bash
# 记忆自动追加 Gateway v2 — 支持四分类记忆提取
# 用法: 消息处理管道: some_program | memory_appender.sh
#
# 标签格式: [MEM_APPEND:type: content]
#   type=user|feedback|project|reference (省略则写入通用日志)
#
# 测试:
#   echo "[MEM_APPEND:user: 老板喜欢简洁] [MEM_APPEND:feedback: 不要冗长分析]" | memory_appender.sh

MEMORY_FILE="~/.hermes/MEMORY.md"

# 分类定义 (显示名称 -> 区块标记)
declare -A SECTIONS=(
    ["user"]="## 👤 用户偏好与信息"
    ["feedback"]="## 📝 反馈与纠正"
    ["project"]="## 🎯 项目约束与上下文"
    ["reference"]="## 🔗 外部参考与指向"
)
GENERAL_MARKER="## 📋 临时日志 (通用)"

INPUT=$(cat)

# 提取所有 [MEM_APPEND:...] 标签 (支持 type: 格式和旧格式)
APPENDS=$(echo "$INPUT" | grep -oP '\[MEM_APPEND:[^\]]*\]')

if [ -z "$APPENDS" ]; then
    echo "$INPUT"
    exit 0
fi

# 确保 MEMORY.md 存在
if [ ! -f "$MEMORY_FILE" ]; then
    echo "ERROR: MEMORY.md not found at $MEMORY_FILE" >&2
    echo "$INPUT"
    exit 1
fi

TODAY=$(date '+%Y-%m-%d %H:%M')

# 处理每个标签
while IFS= read -r tag; do
    [ -z "$tag" ] && continue

    # 提取标签内容: [MEM_APPEND:type: content] 或 [MEM_APPEND: content]
    tag_content="${tag#\[MEM_APPEND:}"
    tag_content="${tag_content%\]}"

    # 判断是否有分类前缀
    type=""
    content=""
    if echo "$tag_content" | grep -qP '^(user|feedback|project|reference):\s*'; then
        type=$(echo "$tag_content" | sed -n 's/^\(user\|feedback\|project\|reference\):.*/\1/p')
        content=$(echo "$tag_content" | sed 's/^\(user\|feedback\|project\|reference\):\s*//')
    else
        content="$tag_content"
    fi

    [ -z "$content" ] && continue

    if [ -n "$type" ] && [ -n "${SECTIONS[$type]}" ]; then
        # 分类写入
        SECTION="${SECTIONS[$type]}"
        ENTRY="$TODAY — $content"

        # 确保区块存在
        if ! grep -qF "$SECTION" "$MEMORY_FILE"; then
            # 在通用日志前插入（如果通用日志已存在）或在文件末尾追加
            if grep -qF "$GENERAL_MARKER" "$MEMORY_FILE"; then
                sed -i "/^$GENERAL_MARKER$/i $SECTION\n" "$MEMORY_FILE"
            else
                echo "" >> "$MEMORY_FILE"
                echo "$SECTION" >> "$MEMORY_FILE"
                echo "" >> "$MEMORY_FILE"
            fi
            echo "✅ 新区块: $type" >&2
        fi

        # 检查重复
        if ! grep -qF "$ENTRY" "$MEMORY_FILE"; then
            sed -i "/^$SECTION$/a $ENTRY" "$MEMORY_FILE"
            echo "✅ [$type] $content" >&2
        fi
    else
        # 通用日志
        if ! grep -qF "$GENERAL_MARKER" "$MEMORY_FILE"; then
            echo "" >> "$MEMORY_FILE"
            echo "$GENERAL_MARKER" >> "$MEMORY_FILE"
            echo "" >> "$MEMORY_FILE"
        fi

        ENTRY="$TODAY — $content"
        if ! grep -qF "$ENTRY" "$MEMORY_FILE"; then
            sed -i "/^$GENERAL_MARKER$/a $ENTRY" "$MEMORY_FILE"
            echo "✅ [通用] $content" >&2
        fi
    fi
done <<< "$APPENDS"

echo "$INPUT"
