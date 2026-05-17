#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/si:review + /si:promote 测试演示

演示完整的记忆审查 → 提升流程
"""

import subprocess
import sys

def run_review():
    """执行记忆审查"""
    print("=" * 60)
    print("📊 步骤 1: 执行记忆审查 /si:review")
    print("=" * 60)
    
    cmd = [
        "python3",
        "/root/.openclaw/workspace/skills/self-improvement-core/commands/si-review/si_review.py",
        "--days", "30"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"❌ 审查失败：{result.stderr}")
        return None
    
    return result.stdout

def parse_candidates(review_output):
    """从审查报告中解析提升候选"""
    candidates = []
    
    # 简单解析：查找 "### {id}. " 格式
    import re
    pattern = r'###\s*(\d+)\.\s+(.+?)(?=\n###|\n##|\Z)'
    matches = re.findall(pattern, review_output, re.DOTALL)
    
    for match in matches:
        entry_id = int(match[0])
        title = match[1].strip().split('\n')[0]  # 只取第一行作为标题
        
        # 跳过太短的标题 (可能是噪声)
        if len(title) > 3 and not title.isdigit():
            candidates.append({
                'id': entry_id,
                'title': title
            })
    
    return candidates[:5]  # 返回前 5 个候选

def run_promote(entry_id, target=None):
    """执行记忆提升"""
    print("=" * 60)
    print(f"📤 步骤 2: 执行记忆提升 /si:promote {entry_id}")
    print("=" * 60)
    
    cmd = [
        "python3",
        "/root/.openclaw/workspace/skills/self-improvement-core/commands/si-promote/si_promote.py",
        str(entry_id),
        "--dry-run"  # 预览模式，不实际执行
    ]
    
    if target:
        cmd.extend(["--target", target])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"❌ 提升失败：{result.stderr}")
        return False
    
    return True

def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "/si:review + /si:promote 测试演示" + " " * 11 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    # 步骤 1: 执行记忆审查
    review_output = run_review()
    
    if not review_output:
        print("❌ 审查失败，退出")
        sys.exit(1)
    
    # 解析提升候选
    candidates = parse_candidates(review_output)
    
    if not candidates:
        print("❌ 未找到提升候选")
        sys.exit(1)
    
    print(f"\n✅ 找到 {len(candidates)} 个提升候选:\n")
    for i, candidate in enumerate(candidates, 1):
        print(f"  {i}. #{candidate['id']} - {candidate['title']}")
    
    # 步骤 2: 测试提升第一个候选
    print("\n\n")
    first_candidate = candidates[0]
    print(f"🎯 选择提升候选 #1: #{first_candidate['id']} - {first_candidate['title']}")
    print("\n")
    
    success = run_promote(first_candidate['id'])
    
    if success:
        print("\n")
        print("=" * 60)
        print("✅ 测试完成!")
        print("=" * 60)
        print("\n")
        print("📝 说明:")
        print("  - 当前使用 --dry-run 预览模式，未实际执行提升")
        print("  - 移除 --dry-run 参数即可实际提升")
        print("  - 提升后内容会追加到 AGENTS.md/TOOLS.md/SOUL.md")
        print("\n")
    else:
        print("\n")
        print("❌ 提升失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
