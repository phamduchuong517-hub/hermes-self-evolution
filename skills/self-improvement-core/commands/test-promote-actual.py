#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实际提升测试 - 从 MEMORY.md 直接提取并提升
"""

import sys
import os

sys.path.insert(0, '/root/.openclaw/workspace/skills/self-improvement-core/commands/si-promote')
from si_promote import SIPromoteCommand

def main():
    print("\n")
    print("=" * 60)
    print("🧪 /si:promote 实际提升测试")
    print("=" * 60)
    print("\n")
    
    cmd = SIPromoteCommand()
    
    # 读取 MEMORY.md
    memory_path = "/root/.openclaw/workspace/MEMORY.md"
    with open(memory_path, 'r', encoding='utf-8') as f:
        memory_content = f.read()
    
    print(f"📖 已读取 MEMORY.md ({len(memory_content)} 字节)")
    print("\n")
    
    # 模拟提升一个条目
    # 从 MEMORY.md 中提取"模型路由策略"相关内容
    test_entry = {
        'id': 1,
        'title': '模型路由策略',
        'content': '''
### 1. 模型路由策略

**出现次数**: 8 次
**关键词**: 模型，DeepSeek, Qwen, 千问
**建议提升目标**: TOOLS.md

**原始内容**:
> 写作时用 DeepSeek，编码时用 Qwen Coder，通用时用千问 3.5
''',
        'metadata': {
            'count': 8,
            'keywords': '模型，DeepSeek, Qwen, 千问',
            'suggested_target': 'TOOLS.md'
        }
    }
    
    print("🎯 测试提升条目:")
    print(f"   ID: {test_entry['id']}")
    print(f"   标题：{test_entry['title']}")
    print(f"   目标：{test_entry['metadata']['suggested_target']}")
    print("\n")
    
    # 执行提升 (预览模式)
    print("📤 执行提升 (预览模式)...")
    print("\n")
    
    # 手动调用内部方法
    target = test_entry['metadata']['suggested_target']
    converted = cmd._convert_format(test_entry, target)
    conflicts = cmd._detect_conflicts(test_entry, cmd._read_file(cmd._get_target_path(target)))
    result = cmd._generate_result(
        test_entry['id'],
        test_entry,
        target,
        converted,
        conflicts,
        dry_run=True
    )
    
    print(result)
    print("\n")
    
    # 验证
    print("=" * 60)
    print("✅ 测试完成!")
    print("=" * 60)
    print("\n")
    print("📝 说明:")
    print("  - 当前为预览模式，未实际写入文件")
    print("  - 移除 dry_run=True 后将实际提升到 TOOLS.md")
    print("  - 提升后内容会追加到目标文件末尾")
    print("\n")

if __name__ == '__main__':
    main()
