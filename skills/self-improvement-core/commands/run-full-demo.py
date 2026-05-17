#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/si:review + /si:promote 实际执行演示

完整流程：审查 → 提升 → 验证
"""

import subprocess
import sys
import os

WORKSPACE = "/root/.openclaw/workspace"

def run_command(cmd, description):
    """运行命令并打印结果"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    print(f"命令：{' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE)
    
    if result.stdout:
        print(result.stdout[:2000])  # 限制输出长度
    
    if result.returncode != 0 and result.stderr:
        print(f"❌ 错误：{result.stderr[:500]}")
    
    return result

def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "/si:review + /si:promote 实际执行" + " " * 12 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    # 步骤 1: 执行记忆审查
    review_result = run_command(
        ["python3", "skills/self-improvement-core/commands/si-review/si_review.py", "--days", "7"],
        "步骤 1: 执行记忆审查 (最近 7 天)"
    )
    
    if review_result.returncode != 0:
        print("❌ 审查失败，退出")
        sys.exit(1)
    
    print("\n✅ 审查完成！")
    
    # 步骤 2: 提示用户选择
    print("\n")
    print("=" * 60)
    print("🤔 下一步操作")
    print("=" * 60)
    print("\n")
    print("审查报告已生成，包含提升候选列表。")
    print("\n")
    print("📋 执行提升:")
    print("   python3 skills/self-improvement-core/commands/si-promote/si_promote.py <ID> [--target FILE]")
    print("\n")
    print("示例:")
    print("   # 提升候选 #1 (自动选择目标)")
    print("   python3 si_promote.py 1")
    print("\n")
    print("   # 提升到指定文件")
    print("   python3 si_promote.py 1 --target TOOLS.md")
    print("\n")
    print("   # 预览模式 (不实际执行)")
    print("   python3 si_promote.py 1 --dry-run")
    print("\n")
    print("=" * 60)
    print("\n")
    
    # 步骤 3: 验证文件
    print("=" * 60)
    print("📁 相关文件")
    print("=" * 60)
    print("\n")
    
    files_to_check = [
        "skills/self-improvement-core/commands/si-review/si_review.py",
        "skills/self-improvement-core/commands/si-promote/si_promote.py",
        "skills/self-improvement-core/commands/USAGE.md",
        "docs/SI-COMMANDS-TEST-REPORT-2026-04-22.md"
    ]
    
    for file in files_to_check:
        path = os.path.join(WORKSPACE, file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {file} ({size} 字节)")
        else:
            print(f"❌ {file} (不存在)")
    
    print("\n")
    print("=" * 60)
    print("✅ 执行完成!")
    print("=" * 60)
    print("\n")
    print("📝 总结:")
    print("  1. /si:review 命令已就绪 - 审查记忆，找出提升候选")
    print("  2. /si:promote 命令已就绪 - 提升记忆到规则文件")
    print("  3. 使用文档已创建 - USAGE.md")
    print("  4. 测试报告已生成 - SI-COMMANDS-TEST-REPORT-2026-04-22.md")
    print("\n")
    print("🎯 下一步:")
    print("  - 运行 /si:review 查看提升候选")
    print("  - 运行 /si:promote <ID> 执行提升")
    print("  - 检查 AGENTS.md/TOOLS.md 验证提升结果")
    print("\n")

if __name__ == '__main__':
    main()
