#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/si:review - 记忆审查命令

功能：自动扫描 MEMORY.md 找出提升候选
来源：融合 auto-memory-pro /si:review + self-improvement-core v4.0
版本：v1.0 (2026-04-22)
"""

import os
import re
import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional


class SIReviewCommand:
    """记忆审查命令"""
    
    def __init__(self, workspace_path: str = "/root/.openclaw/workspace"):
        self.workspace_path = workspace_path
        self.memory_path = os.path.join(workspace_path, "MEMORY.md")
        self.agents_path = os.path.join(workspace_path, "AGENTS.md")
        self.tools_path = os.path.join(workspace_path, "TOOLS.md")
        self.soul_path = os.path.join(workspace_path, "SOUL.md")
        self.memory_dir = os.path.join(workspace_path, "memory")
    
    def execute(self, days: int = 30, verbose: bool = False) -> str:
        """
        执行记忆审查
        
        Args:
            days: 审查最近 N 天的记忆
            verbose: 是否输出详细报告
        
        Returns:
            审查报告 (Markdown 格式)
        """
        # 1. 读取记忆文件
        memory_content = self._read_memory()
        
        # 2. 识别重复模式
        patterns = self._find_recurring_patterns(memory_content, min_count=3)
        
        # 3. 检测陈旧条目
        stale_entries = self._find_stale_entries(memory_content, days=days)
        
        # 4. 分析差距
        gaps = self._identify_gaps(memory_content)
        
        # 5. 生成报告
        report = self._generate_report(
            memory_content, patterns, stale_entries, gaps, days, verbose
        )
        
        return report
    
    def _read_memory(self) -> str:
        """读取 MEMORY.md"""
        if not os.path.exists(self.memory_path):
            return ""
        
        with open(self.memory_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _find_recurring_patterns(
        self, content: str, min_count: int = 3
    ) -> List[Dict]:
        """
        识别重复模式
        
        Args:
            content: MEMORY.md 内容
            min_count: 最小出现次数
        
        Returns:
            重复模式列表
        """
        patterns = []
        
        # 1. 提取关键段落 (表格、列表、代码块)
        sections = self._extract_sections(content)
        
        # 2. 统计关键词频率
        keyword_freq = self._count_keywords(content)
        
        # 3. 识别重复主题
        themes = self._identify_themes(sections, keyword_freq)
        
        # 4. 过滤和排序
        for theme in themes:
            if theme['count'] >= min_count:
                patterns.append(theme)
        
        # 5. 按频率排序
        patterns.sort(key=lambda x: x['count'], reverse=True)
        
        return patterns[:20]  # 返回前 20 个
    
    def _extract_sections(self, content: str) -> List[Dict]:
        """提取关键段落"""
        sections = []
        
        # 表格
        table_pattern = r'\|.*?\|\n(?:\|.*?\|\n)*'
        tables = re.findall(table_pattern, content, re.MULTILINE)
        for table in tables:
            sections.append({
                'type': 'table',
                'content': table,
                'keywords': self._extract_keywords(table)
            })
        
        # 列表
        list_pattern = r'(?:^|\n)(?:[-*•]\s.*?)+(?:\n|$)'
        lists = re.findall(list_pattern, content, re.MULTILINE)
        for lst in lists:
            sections.append({
                'type': 'list',
                'content': lst,
                'keywords': self._extract_keywords(lst)
            })
        
        # 代码块
        code_pattern = r'```.*?```'
        codes = re.findall(code_pattern, content, re.DOTALL)
        for code in codes:
            sections.append({
                'type': 'code',
                'content': code,
                'keywords': self._extract_keywords(code)
            })
        
        return sections
    
    def _extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """提取关键词"""
        # 简单实现：移除停用词，统计词频
        stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
            '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall'
        }
        
        # 分词 (简单按空格和标点分割)
        words = re.findall(r'[\w\u4e00-\u9fff]+', text.lower())
        
        # 过滤停用词和短词
        filtered = [
            w for w in words
            if w not in stopwords and len(w) > 1
        ]
        
        # 统计频率
        counter = Counter(filtered)
        
        return [word for word, _ in counter.most_common(top_k)]
    
    def _count_keywords(self, content: str) -> Dict[str, int]:
        """统计关键词频率"""
        # 提取所有关键词
        all_keywords = []
        
        # 按行处理
        for line in content.split('\n'):
            keywords = self._extract_keywords(line, top_k=5)
            all_keywords.extend(keywords)
        
        return dict(Counter(all_keywords))
    
    def _identify_themes(
        self, sections: List[Dict], keyword_freq: Dict[str, int]
    ) -> List[Dict]:
        """识别主题"""
        themes = defaultdict(lambda: {'count': 0, 'examples': [], 'keywords': set()})
        
        # 高频关键词作为主题种子
        top_keywords = sorted(
            keyword_freq.items(),
            key=lambda x: x[1],
            reverse=True
        )[:50]
        
        for keyword, freq in top_keywords:
            if freq >= 3:  # 至少出现 3 次
                themes[keyword]['count'] = freq
                themes[keyword]['keywords'].add(keyword)
        
        # 从段落中提取主题
        for section in sections:
            for keyword in section['keywords']:
                if keyword in themes:
                    themes[keyword]['examples'].append(
                        section['content'][:200]  # 截取前 200 字
                    )
        
        # 转换为列表
        result = []
        for name, data in themes.items():
            result.append({
                'name': name,
                'count': data['count'],
                'keywords': list(data['keywords']),
                'examples': data['examples'][:3]  # 最多 3 个示例
            })
        
        return result
    
    def _find_stale_entries(
        self, content: str, days: int = 30
    ) -> List[Dict]:
        """
        检测陈旧条目
        
        Args:
            content: MEMORY.md 内容
            days: 陈旧阈值 (天)
        
        Returns:
            陈旧条目列表
        """
        stale_entries = []
        threshold_date = datetime.now() - timedelta(days=days)
        
        # 查找带日期的条目
        date_pattern = r'(?:最后更新 | 更新时间 | 日期)[:：]?\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})'
        matches = re.finditer(date_pattern, content)
        
        for match in matches:
            date_str = match.group(1)
            try:
                # 解析日期
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                except ValueError:
                    continue
            
            # 检查是否陈旧
            if date_obj < threshold_date:
                # 提取上下文 (前后 100 字)
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end].strip()
                
                stale_entries.append({
                    'date': date_str,
                    'days_ago': (datetime.now() - date_obj).days,
                    'context': context
                })
        
        # 按陈旧程度排序
        stale_entries.sort(key=lambda x: x['days_ago'], reverse=True)
        
        return stale_entries[:20]  # 返回前 20 个
    
    def _identify_gaps(self, memory_content: str) -> List[Dict]:
        """
        分析差距
        
        对比 MEMORY.md 与 AGENTS.md/TOOLS.md/SOUL.md
        
        Args:
            memory_content: MEMORY.md 内容
        
        Returns:
            差距列表
        """
        gaps = []
        
        # 读取规则文件
        agents_content = self._read_file(self.agents_path)
        tools_content = self._read_file(self.tools_path)
        soul_content = self._read_file(self.soul_path)
        
        # 提取 MEMORY.md 中的关键主题
        memory_themes = self._extract_themes_from_content(memory_content)
        
        # 检查每个主题是否在规则文件中
        for theme in memory_themes[:30]:  # 检查前 30 个主题
            in_agents = theme in agents_content.lower()
            in_tools = theme in tools_content.lower()
            in_soul = theme in soul_content.lower()
            
            if not (in_agents or in_tools or in_soul):
                # 找到差距
                gaps.append({
                    'theme': theme,
                    'in_memory': True,
                    'in_agents': in_agents,
                    'in_tools': in_tools,
                    'in_soul': in_soul,
                    'suggestion': self._suggest_target(theme)
                })
        
        return gaps[:10]  # 返回前 10 个差距
    
    def _extract_themes_from_content(self, content: str) -> List[str]:
        """从内容中提取主题"""
        # 提取标题
        title_pattern = r'#{1,3}\s+(.+?)(?:\n|$)'
        titles = re.findall(title_pattern, content)
        
        # 提取表格标题
        table_header_pattern = r'\|\s*([^|]+?)\s*\|'
        headers = re.findall(table_header_pattern, content)
        
        # 合并并去重
        themes = list(set([t.strip().lower() for t in titles + headers]))
        
        # 过滤短主题
        themes = [t for t in themes if len(t) > 3]
        
        return themes
    
    def _suggest_target(self, theme: str) -> str:
        """建议提升目标"""
        # 简单启发式规则
        if any(kw in theme for kw in ['模型', 'voice', 'tts', 'api']):
            return "TOOLS.md"
        elif any(kw in theme for kw in ['行为', '风格', '规范', '原则']):
            return "AGENTS.md"
        elif any(kw in theme for kw in ['人格', '身份', 'core']):
            return "SOUL.md"
        else:
            return "AGENTS.md 或 TOOLS.md"
    
    def _read_file(self, path: str) -> str:
        """读取文件"""
        if not os.path.exists(path):
            return ""
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().lower()
    
    def _generate_report(
        self,
        memory_content: str,
        patterns: List[Dict],
        stale_entries: List[Dict],
        gaps: List[Dict],
        days: int,
        verbose: bool = False
    ) -> str:
        """
        生成审查报告
        
        Args:
            memory_content: MEMORY.md 内容
            patterns: 重复模式列表
            stale_entries: 陈旧条目列表
            gaps: 差距列表
            days: 审查天数
            verbose: 是否详细输出
        
        Returns:
            Markdown 格式报告
        """
        # 基础统计
        total_lines = len(memory_content.split('\n'))
        memory_files = self._count_memory_files()
        
        # 生成报告
        report = []
        report.append("# 📊 记忆审查报告")
        report.append(f"\n**审查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"**审查范围**: 最近 {days} 天")
        report.append("")
        
        # 基础统计
        report.append("## 📊 基础统计")
        report.append(f"- MEMORY.md 总行数：{total_lines}")
        report.append(f"- 记忆文件数：{memory_files}")
        report.append(f"- 重复模式数：{len(patterns)}")
        report.append(f"- 陈旧条目数：{len(stale_entries)}")
        report.append(f"- 差距数：{len(gaps)}")
        report.append("")
        
        # 提升候选
        report.append("## 🎯 提升候选")
        if patterns:
            for i, pattern in enumerate(patterns[:10], 1):
                report.append(f"\n### {i}. {pattern['name']}")
                report.append(f"- **出现次数**: {pattern['count']} 次")
                report.append(f"- **关键词**: {', '.join(pattern['keywords'][:5])}")
                if pattern['examples']:
                    report.append(f"- **示例**: {pattern['examples'][0][:100]}...")
                report.append(f"- **建议提升目标**: {self._suggest_target(pattern['name'])}")
        else:
            report.append("\n暂无重复模式")
        report.append("")
        
        # 陈旧条目
        report.append("## ⚠️ 陈旧条目")
        if stale_entries:
            for i, entry in enumerate(stale_entries[:10], 1):
                report.append(f"\n### {i}. {entry['date']}")
                report.append(f"- **最后更新**: {entry['days_ago']} 天前")
                report.append(f"- **上下文**: {entry['context'][:150]}...")
                report.append(f"- **建议**: 归档 / 删除 / 更新")
        else:
            report.append("\n暂无陈旧条目")
        report.append("")
        
        # 差距分析
        report.append("## 🔍 差距分析")
        if gaps:
            for i, gap in enumerate(gaps[:10], 1):
                report.append(f"\n### {i}. {gap['theme']}")
                report.append(f"- **MEMORY.md 中有**: ✅")
                report.append(f"- **AGENTS.md 中有**: {'✅' if gap['in_agents'] else '❌'}")
                report.append(f"- **TOOLS.md 中有**: {'✅' if gap['in_tools'] else '❌'}")
                report.append(f"- **建议**: 提升到 {gap['suggestion']}")
        else:
            report.append("\n暂无明显差距")
        report.append("")
        
        # 执行建议
        report.append("## 📋 执行建议")
        report.append("")
        if patterns:
            high_priority = patterns[:3]
            report.append(f"**立即提升** ({len(high_priority)} 个):")
            for p in high_priority:
                report.append(f"- {p['name']}")
            report.append("")
        
        if gaps:
            report.append(f"**本周内提升** ({len(gaps)} 个差距):")
            for g in gaps[:5]:
                report.append(f"- {g['theme']} → {g['suggestion']}")
            report.append("")
        
        if stale_entries:
            report.append(f"**归档陈旧** ({len(stale_entries)} 个):")
            for e in stale_entries[:5]:
                report.append(f"- {e['date']} ({e['days_ago']} 天前)")
        
        report.append("")
        report.append("---")
        report.append("")
        report.append("**使用 `/si:promote <id>` 将候选提升到规则文件**")
        
        return '\n'.join(report)
    
    def _count_memory_files(self) -> int:
        """统计记忆文件数"""
        if not os.path.exists(self.memory_dir):
            return 0
        
        count = 0
        for f in os.listdir(self.memory_dir):
            if f.endswith('.md'):
                count += 1
        
        return count


# 主函数 (供命令行调用)
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='记忆审查命令')
    parser.add_argument('--days', type=int, default=30, help='审查最近 N 天')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    cmd = SIReviewCommand()
    report = cmd.execute(days=args.days, verbose=args.verbose)
    print(report)


if __name__ == '__main__':
    main()
