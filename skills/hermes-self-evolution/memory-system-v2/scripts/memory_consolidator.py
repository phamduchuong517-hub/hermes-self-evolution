#!/usr/bin/env python3
"""
记忆夜间整理脚本 v2 — 主题合并 + 分类归档 + 去重
运行频率: 每天一次 (通过 cron)

改进:
- 识别相同主题的记忆条目，合并为一条主题记忆
- 将带分类的记忆保留在对应分类区块
- 通用日志去重后归档
"""

import re
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path("Path.home() / ".hermes" / MEMORY.md")

# 分类区块定义
CATEGORIES = {
    "👤": "user",
    "📝": "feedback",
    "🎯": "project",
    "🔗": "reference",
    "📋": "general",
}


def categorize_section(section_title: str) -> str:
    """根据区块标题判断分类"""
    for emoji, cat in CATEGORIES.items():
        if emoji in section_title:
            return cat
    return "general"


def clean_timestamp(entry: str) -> str:
    """去除时间戳前缀，返回纯内容"""
    match = re.match(r'\d{4}-\d{2}-\d{2}.*?—\s*(.*)', entry)
    return match.group(1).strip() if match else entry.strip()


def infer_topic(content: str) -> str:
    """
    从记忆内容推断主题。
    规则:
    - 提取第一个关键词(通常是名词性短语)
    - 如果包含"不喜欢/讨厌/厌恶" → 归类"负面反馈"
    - 如果包含"截止日期/D-Day/上线" → 归类"项目时间线"
    """
    # 简单主题推断规则
    negative_patterns = r"(讨厌|厌恶|不喜欢|不要|禁止|避免)"
    time_patterns = r"(截止|到期|上线|发布|deadline|D-Day)"
    tool_patterns = r"(yq|jq|curl|ssh|git|docker|systemd)"

    if re.search(negative_patterns, content, re.IGNORECASE):
        return "负面反馈"
    if re.search(time_patterns, content, re.IGNORECASE):
        return "项目时间线"
    if re.search(tool_patterns, content, re.IGNORECASE):
        match = re.search(tool_patterns, content, re.IGNORECASE)
        return f"工具_{match.group(1)}"
    return None


def merge_by_topic(entries: list[str]) -> list[str]:
    """
    按主题合并记忆条目。
    同一主题的多条条目合并为一条汇总。
    """
    if not entries:
        return []

    # 先提取纯内容（去时间戳）
    cleaned = [(e, clean_timestamp(e)) for e in entries]

    # 分组: 有主题推断的分一组，无主题的保留原样
    topic_groups = {}
    ungrouped = []

    for orig, content in cleaned:
        topic = infer_topic(content)
        if topic:
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append(content)
        else:
            ungrouped.append(orig)

    result = list(ungrouped)

    # 合并主题组
    for topic, items in topic_groups.items():
        if len(items) == 1:
            # 单条主题记忆保持原样（加时间戳）
            result.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} — {items[0]}")
        else:
            # 多条合并: 找到最早的时间戳
            timestamps = []
            for orig, content in cleaned:
                if content in items:
                    match = re.match(r'(\d{4}-\d{2}-\d{2}.*?)—', orig)
                    if match:
                        timestamps.append(match.group(1).strip())

            oldest = timestamps[0] if timestamps else datetime.now().strftime('%Y-%m-%d %H:%M')
            # 合并内容
            merged = "; ".join(set(items))
            result.append(f"{oldest} — [合并] {topic}: {merged}")

    return result


def collect_section_entries(content: str, section_title: str) -> tuple[list[str], str]:
    """从指定区块提取所有条目，返回 (entries, cleaned_content_without_section)"""
    lines = content.split('\n')
    section_start = None
    section_end = None
    entries = []

    for i, line in enumerate(lines):
        if section_title in line:
            section_start = i
        if section_start is not None and i > section_start:
            if line.startswith('##') and line != lines[section_start]:
                section_end = i
                break
            stripped = line.strip()
            if stripped and not stripped.startswith('##') and not stripped.startswith('-') and not stripped.startswith('>') and not stripped.startswith('#'):
                entries.append(stripped)

    if section_end is None:
        section_end = len(lines)

    cleaned_lines = lines[:section_start] + lines[section_end:]
    cleaned = '\n'.join(cleaned_lines).strip()

    return entries, cleaned


def deduplicate(entries: list[str]) -> list[str]:
    """去重 (基于内容去时间戳)"""
    seen = set()
    result = []
    for e in entries:
        key = clean_timestamp(e)
        if key not in seen:
            seen.add(key)
            result.append(e)
    return result


def main():
    if not MEMORY_FILE.exists():
        print("MEMORY.md not found")
        return

    content = MEMORY_FILE.read_text(encoding='utf-8')
    changes = []

    # 处理每个分类区块
    for emoji, cat_name in CATEGORIES.items():
        section_patterns = {
            "👤": "用户偏好与信息",
            "📝": "反馈与纠正",
            "🎯": "项目约束与上下文",
            "🔗": "外部参考与指向",
            "📋": "临时日志",
        }
        section_name = section_patterns.get(emoji, "")
        if not section_name:
            continue

        # 找区块
        marker = f"## {emoji} {section_name}"
        if marker not in content:
            continue

        entries, content = collect_section_entries(content, marker)
        if not entries:
            continue

        # 去重
        deduped = deduplicate(entries)
        if len(deduped) != len(entries):
            changes.append(f"{cat_name}: 去重 {len(entries)}→{len(deduped)}")

        # 通用日志做主题合并，分类区块保持原样
        if cat_name == "general":
            merged = merge_by_topic(deduped)
            if len(merged) != len(deduped):
                changes.append(f"{cat_name}: 主题合并 {len(deduped)}→{len(merged)}")
        else:
            merged = deduped

        # 重新写入区块
        if merged:
            section_block = f"\n{marker}\n" + "\n".join(f"{m}" for m in merged) + "\n"
            content += section_block

    # 去重：移除所有空行区块（如果有条目被完全合并没了的情况）
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 写入
    MEMORY_FILE.write_text(content.strip() + '\n', encoding='utf-8')

    if changes:
        print(f"✅ 整理完成: {'; '.join(changes)}")
    else:
        print("✅ 整理完成: 无变更")


if __name__ == '__main__':
    main()
