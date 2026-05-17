#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/si:promote - 记忆提升命令

功能：将记忆提升到 AGENTS.md/TOOLS.md/SOUL.md
来源：融合 auto-memory-pro /si:promote + self-improvement-core v4.0
版本：v1.0 (2026-04-22)
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher


class SIPromoteCommand:
    """记忆提升命令"""
    
    def __init__(self, workspace_path: str = "/root/.openclaw/workspace"):
        self.workspace_path = workspace_path
        self.memory_path = os.path.join(workspace_path, "MEMORY.md")
        self.agents_path = os.path.join(workspace_path, "AGENTS.md")
        self.tools_path = os.path.join(workspace_path, "TOOLS.md")
        self.soul_path = os.path.join(workspace_path, "SOUL.md")
        self.promote_log_path = os.path.join(workspace_path, "docs/PROMOTE-LOG.md")
    
    def execute(
        self,
        entry_id: int,
        target: Optional[str] = None,
        batch: bool = False,
        keep: bool = False,
        dry_run: bool = False
    ) -> str:
        """
        执行记忆提升
        
        Args:
            entry_id: 记忆条目 ID
            target: 目标文件 (AGENTS.md/TOOLS.md/SOUL.md)
            batch: 批量模式
            keep: 保留原记忆
            dry_run: 预览模式
        
        Returns:
            执行结果
        """
        # 1. 读取 MEMORY.md
        memory_content = self._read_file(self.memory_path)
        
        # 2. 提取指定条目
        entry = self._extract_entry(memory_content, entry_id)
        if not entry:
            return f"❌ 未找到条目 #{entry_id}"
        
        # 3. 自动识别目标文件
        if not target:
            target = self._auto_detect_target(entry)
        
        # 4. 检测冲突
        target_content = self._read_file(self._get_target_path(target))
        conflicts = self._detect_conflicts(entry, target_content)
        
        # 5. 格式转换
        converted = self._convert_format(entry, target)
        
        # 6. 执行提升
        if not dry_run:
            success, message = self._do_promote(converted, target, conflicts)
            if not success:
                return f"❌ 提升失败：{message}"
            
            # 7. 清理记忆
            if not keep:
                self._cleanup_memory(entry_id)
            
            # 8. 记录日志
            self._log_promotion(entry_id, entry, target, converted)
        else:
            message = "预览模式，未执行"
        
        # 9. 返回结果
        return self._generate_result(
            entry_id, entry, target, converted, conflicts, dry_run
        )
    
    def _read_file(self, path: str) -> str:
        """读取文件"""
        if not os.path.exists(path):
            return ""
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_entry(self, content: str, entry_id: int) -> Optional[Dict]:
        """
        提取记忆条目
        
        支持三种格式:
        1. /si:review 报告格式 (### {id}. 标题)
        2. MEMORY.md 直接格式 (按章节标题)
        3. 简化格式 (仅标题)
        """
        # 方案 1: 从审查报告格式解析
        # 匹配 "### {id}. 标题" 格式
        pattern = rf'###\s*{entry_id}\.\s+([^\n]+)(.*?)(?=\n###\s*\d+\.|\n##\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            title = match.group(1).strip()
            rest_content = match.group(2).strip()
            entry_content = f"### {entry_id}. {title}\n{rest_content}"
            
            # 提取元数据
            metadata = self._extract_metadata(entry_content)
            
            return {
                'id': entry_id,
                'title': title,
                'content': entry_content,
                'metadata': metadata
            }
        
        # 方案 2: 如果 entry_id 是简单数字，尝试从 MEMORY.md 查找
        # 这需要在 execute 方法中传入 MEMORY.md 内容
        return None
    
    def _extract_metadata(self, content: str) -> Dict:
        """提取元数据"""
        metadata = {}
        
        # 出现次数
        count_match = re.search(r'\*\*出现次数\*\*:\s*(\d+)', content)
        if count_match:
            metadata['count'] = int(count_match.group(1))
        
        # 关键词
        keywords_match = re.search(r'\*\*关键词\*\*:\s*(.+?)(?:\n|$)', content)
        if keywords_match:
            metadata['keywords'] = keywords_match.group(1).strip()
        
        # 建议目标
        target_match = re.search(r'\*\*建议提升目标\*\*:\s*(.+?)(?:\n|$)', content)
        if target_match:
            metadata['suggested_target'] = target_match.group(1).strip()
        
        # 示例
        example_match = re.search(r'\*\*示例\*\*:\s*(.+?)(?:\n|$)', content)
        if example_match:
            metadata['example'] = example_match.group(1).strip()
        
        return metadata
    
    def _auto_detect_target(self, entry: Dict) -> str:
        """
        自动识别目标文件
        
        启发式规则:
        - 模型/工具/API → TOOLS.md
        - 行为/规范/流程 → AGENTS.md
        - 人格/身份/核心 → SOUL.md
        """
        title = entry['title'].lower()
        content = entry['content'].lower()
        keywords = entry['metadata'].get('keywords', '').lower()
        
        # TOOLS.md 关键词
        tools_keywords = [
            '模型', 'model', 'api', 'key', 'token', '工具', 'tool',
            '配置', 'config', '环境', 'environment', 'voice', 'tts'
        ]
        
        # SOUL.md 关键词
        soul_keywords = [
            '人格', 'persona', '身份', 'identity', '核心', 'core',
            '价值观', 'value', '本质', 'nature'
        ]
        
        # AGENTS.md 关键词 (默认)
        agents_keywords = [
            '行为', 'behavior', '规范', 'rule', '流程', 'workflow',
            '交互', 'interaction', '原则', 'principle', '风格', 'style'
        ]
        
        # 检查匹配
        all_text = f"{title} {content} {keywords}"
        
        if any(kw in all_text for kw in tools_keywords):
            return "TOOLS.md"
        elif any(kw in all_text for kw in soul_keywords):
            return "SOUL.md"
        elif any(kw in all_text for kw in agents_keywords):
            return "AGENTS.md"
        else:
            # 默认 AGENTS.md
            return "AGENTS.md"
    
    def _get_target_path(self, target: str) -> str:
        """获取目标文件路径"""
        target_map = {
            "AGENTS.md": self.agents_path,
            "TOOLS.md": self.tools_path,
            "SOUL.md": self.soul_path
        }
        return target_map.get(target, self.agents_path)
    
    def _detect_conflicts(self, entry: Dict, target_content: str) -> List[Dict]:
        """
        检测冲突
        
        检查目标文件中是否已有相似内容
        """
        conflicts = []
        
        # 提取目标文件的章节标题
        section_pattern = r'#{2,4}\s+(.+?)(?:\n|$)'
        sections = re.findall(section_pattern, target_content)
        
        # 检查每个章节
        for section in sections:
            similarity = self._calculate_similarity(entry['title'], section)
            if similarity > 0.6:  # 相似度 > 60%
                conflicts.append({
                    'type': 'similar_section',
                    'section': section,
                    'similarity': similarity
                })
        
        # 检查关键词重复
        entry_keywords = entry['metadata'].get('keywords', '').split(',')
        for keyword in entry_keywords:
            keyword = keyword.strip()
            if keyword and keyword in target_content:
                conflicts.append({
                    'type': 'keyword_exists',
                    'keyword': keyword
                })
        
        return conflicts
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _convert_format(self, entry: Dict, target: str) -> str:
        """
        格式转换
        
        根据目标文件类型转换格式
        """
        title = entry['title']
        content = entry['content']
        
        if target == "TOOLS.md":
            # 转换为配置表格格式
            converted = self._convert_to_tools_format(entry)
        elif target == "AGENTS.md":
            # 转换为行为规则格式
            converted = self._convert_to_agents_format(entry)
        elif target == "SOUL.md":
            # 转换为人格定义格式
            converted = self._convert_to_soul_format(entry)
        else:
            converted = content
        
        return converted
    
    def _convert_to_tools_format(self, entry: Dict) -> str:
        """转换为 TOOLS.md 格式"""
        title = entry['title']
        
        # 尝试提取表格内容
        table_pattern = r'\|.*?\|'
        if re.search(table_pattern, entry['content']):
            # 已有表格，直接提取
            tables = re.findall(table_pattern, entry['content'], re.MULTILINE)
            return f"\n## {title}\n\n" + '\n'.join(tables)
        else:
            # 转换为列表格式
            return f"\n## {title}\n\n{entry['content']}\n"
    
    def _convert_to_agents_format(self, entry: Dict) -> str:
        """转换为 AGENTS.md 格式"""
        title = entry['title']
        
        # 转换为规则列表格式
        return f"\n## {title}\n\n- {entry['content']}\n"
    
    def _convert_to_soul_format(self, entry: Dict) -> str:
        """转换为 SOUL.md 格式"""
        title = entry['title']
        
        # 转换为人格定义格式
        return f"\n## {title}\n\n{entry['content']}\n"
    
    def _do_promote(
        self, converted: str, target: str, conflicts: List[Dict]
    ) -> Tuple[bool, str]:
        """
        执行提升
        
        Returns:
            (成功标志，消息)
        """
        target_path = self._get_target_path(target)
        
        # 检查文件存在
        if not os.path.exists(target_path):
            # 创建文件
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(f"# {target}\n\n")
        
        # 追加内容
        try:
            with open(target_path, 'a', encoding='utf-8') as f:
                f.write(f"\n<!-- Added by /si:promote on {datetime.now().strftime('%Y-%m-%d %H:%M')} -->\n")
                f.write(converted)
            
            return True, f"已追加到 {target}"
        except Exception as e:
            return False, str(e)
    
    def _cleanup_memory(self, entry_id: int):
        """
        清理记忆
        
        标记为"已提升"
        """
        memory_content = self._read_file(self.memory_path)
        
        # 查找条目并标记
        pattern = rf'(###\s*{entry_id}\..+?)(?=\n###\s*\d+\.|$)'
        
        def mark_as_promoted(match):
            original = match.group(1)
            marked = f"\n## ✅ 已提升 ({datetime.now().strftime('%Y-%m-%d')})\n\n{original}\n"
            return marked
        
        new_content = re.sub(pattern, mark_as_promoted, memory_content, flags=re.DOTALL)
        
        # 写回文件
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    def _log_promotion(
        self, entry_id: int, entry: Dict, target: str, converted: str
    ):
        """记录提升日志"""
        log_entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M')} - 提升 #{entry_id}

- **条目**: {entry['title']}
- **目标**: {target}
- **状态**: ✅ 成功

### 提升内容

{converted}

---
"""
        
        # 确保日志目录存在
        os.makedirs(os.path.dirname(self.promote_log_path), exist_ok=True)
        
        # 追加日志
        with open(self.promote_log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def _generate_result(
        self,
        entry_id: int,
        entry: Dict,
        target: str,
        converted: str,
        conflicts: List[Dict],
        dry_run: bool = False
    ) -> str:
        """生成结果报告"""
        result = []
        
        if dry_run:
            result.append("## 🔍 预览模式\n")
        else:
            result.append("## ✅ 提升成功\n")
        
        result.append(f"**条目 ID**: {entry_id}")
        result.append(f"**条目名称**: {entry['title']}")
        result.append(f"**目标文件**: {target}")
        result.append(f"**提升时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        result.append("")
        
        # 冲突警告
        if conflicts:
            result.append("## ⚠️ 检测到冲突\n")
            for conflict in conflicts:
                if conflict['type'] == 'similar_section':
                    result.append(f"- 相似章节：{conflict['section']} (相似度：{conflict['similarity']:.0%})")
                elif conflict['type'] == 'keyword_exists':
                    result.append(f"- 关键词已存在：{conflict['keyword']}")
            result.append("")
        
        # 提升内容
        result.append("### 提升内容\n")
        result.append(converted)
        result.append("")
        
        # 后续操作
        if not dry_run:
            result.append("### 后续操作\n")
            result.append(f"- ✅ 已追加到 `{target}`")
            result.append(f"- ✅ 已在 `MEMORY.md` 标记为'已提升'")
            result.append(f"- ⚠️ 建议：检查 `{target}` 格式是否符合预期")
        
        result.append("")
        result.append("---")
        result.append("")
        result.append("**使用 `/si:review` 查看新的提升候选**")
        
        return '\n'.join(result)


# 主函数 (供命令行调用)
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='记忆提升命令')
    parser.add_argument('entry_id', type=int, help='记忆条目 ID')
    parser.add_argument('--target', choices=['AGENTS.md', 'TOOLS.md', 'SOUL.md'],
                       help='目标文件 (默认自动识别)')
    parser.add_argument('--batch', action='store_true', help='批量模式')
    parser.add_argument('--keep', action='store_true', help='保留原记忆')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    
    args = parser.parse_args()
    
    cmd = SIPromoteCommand()
    result = cmd.execute(
        entry_id=args.entry_id,
        target=args.target,
        batch=args.batch,
        keep=args.keep,
        dry_run=args.dry_run
    )
    print(result)


if __name__ == '__main__':
    main()
