#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能搜索引擎

支持：
1. 本地技能语义搜索
2. 关键词匹配
3. 能力类型匹配
4. 历史使用记录

作者：AI Agent
日期：2026-04-14
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# 导入 Embedding 搜索 (可选)
try:
    from embedding_search import EmbeddingSearchEngine
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False


@dataclass
class SkillMatch:
    """技能匹配结果"""
    skill_path: str
    skill_name: str
    match_score: float
    match_reasons: List[str]
    required_capabilities: List[str]
    skill_description: str


class SkillSearchEngine:
    """技能搜索引擎 (增强版 - 支持 Embedding 语义搜索 + 名称映射)"""
    
    # 名称映射表 (支持中英文映射)
    NAME_MAPPING = {
        "search-yesterday-task": ["搜索昨天", "查找任务", "历史记录", "记忆查询", "昨日任务", "搜索任务"],
        "ai-video-generation": ["生成视频", "抖音", "短视频", "视频创作", "AI 视频", "视频生成", "TikTok", "Reels"],
        "translation-bot": ["翻译", "多语言", "语言转换", "translate", "multilingual"],
        "plugin-system": ["插件", "系统扩展", "功能增强", "plugin", "extension"],
        "deep-search": ["深度搜索", "搜索", "信息收集", "search", "deep search"],
        "task-orchestrator": ["任务编排", "任务规划", "任务分解", "orchestrator", "task plan"],
        "planner-agent": ["规划", "计划", "planner", "planning", "任务规划"],
        "skill-evaluator": ["技能评估", "技能评分", "evaluator", "evaluation", "评分"],
        "skill-first-executor": ["技能优先", "技能执行", "skill first", "executor"],
        "embedding_search": ["语义搜索", "embedding", "向量搜索", "semantic search"],
    }
    
    def __init__(self, workspace_root: str = "/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root)
        self.skills_dir = self.workspace_root / "skills"
        self.index_file = self.skills_dir / "skill_index.json"
        self.skills_cache = {}
        
        # 初始化 Embedding 搜索引擎 (如果可用)
        self.embedding_engine = None
        if EMBEDDING_AVAILABLE:
            try:
                self.embedding_engine = EmbeddingSearchEngine(workspace_root)
                print("✅ Embedding 语义搜索已启用")
            except Exception as e:
                print(f"⚠️  Embedding 引擎初始化失败：{e}")
        
    def search_local_skills(self, query: str, threshold: float = 0.8) -> List[SkillMatch]:
        """
        搜索本地技能
        
        Args:
            query: 任务描述
            threshold: 匹配度阈值 (默认 0.8)
        
        Returns:
            匹配技能列表 (按匹配度降序)
        """
        print(f"\n🔍 搜索本地技能...")
        print(f"   查询：{query}")
        print(f"   阈值：{threshold}")
        
        # 1. 构建/更新索引
        self._build_index()
        
        # 2. 计算匹配度 (混合模式：关键词 + Embedding)
        matches = []
        
        # 2a. 关键词匹配
        keyword_matches = []
        for skill_path, skill_info in self.skills_cache.items():
            match_score, match_reasons = self._calculate_match_score(query, skill_info)
            
            if match_score >= threshold:
                keyword_matches.append({
                    "skill_path": skill_path,
                    "skill_info": skill_info,
                    "match_score": match_score,
                    "match_reasons": match_reasons,
                })
        
        # 2b. Embedding 语义匹配 (如果可用)
        embedding_matches = {}
        if self.embedding_engine:
            try:
                print("   🧠 使用 Embedding 语义搜索...")
                emb_results = self.embedding_engine.search_similar_skills(query, top_k=10, threshold=0.3)
                for emb_result in emb_results:
                    embedding_matches[emb_result["skill_path"]] = emb_result["similarity"]
                print(f"   ✅ Embedding 找到 {len(embedding_matches)} 个语义相似技能")
            except Exception as e:
                print(f"   ⚠️  Embedding 搜索失败：{e}")
        
        # 2c. 合并结果 (关键词 60% + Embedding 40%)
        all_skill_paths = set(m["skill_path"] for m in keyword_matches) | set(embedding_matches.keys())
        
        for skill_path in all_skill_paths:
            # 获取关键词匹配分数
            keyword_match = next((m for m in keyword_matches if m["skill_path"] == skill_path), None)
            keyword_score = keyword_match["match_score"] if keyword_match else 0.0
            keyword_reasons = keyword_match["match_reasons"] if keyword_match else []
            
            # 获取 Embedding 匹配分数
            embedding_score = embedding_matches.get(skill_path, 0.0)
            
            # 混合分数 (关键词 60% + Embedding 40%)
            if keyword_match and embedding_score > 0:
                mixed_score = 0.6 * keyword_score + 0.4 * embedding_score
                match_reasons = keyword_reasons + [f"语义匹配：{embedding_score:.2f}"]
            elif keyword_match:
                mixed_score = keyword_score
                match_reasons = keyword_reasons
            else:
                # 仅 Embedding 匹配
                skill_info = self.skills_cache.get(skill_path, {})
                mixed_score = embedding_score * 0.8  # 仅 Embedding 时降低分数
                match_reasons = [f"语义匹配：{embedding_score:.2f}"]
            
            if mixed_score >= threshold:
                skill_info = self.skills_cache.get(skill_path, {})
                matches.append(SkillMatch(
                    skill_path=skill_path,
                    skill_name=skill_info.get("name", "unknown"),
                    match_score=mixed_score,
                    match_reasons=match_reasons,
                    required_capabilities=skill_info.get("capabilities", []),
                    skill_description=skill_info.get("description", ""),
                ))
        
        # 3. 按匹配度排序
        matches.sort(key=lambda m: m.match_score, reverse=True)
        
        print(f"   ✅ 找到 {len(matches)} 个匹配技能")
        for i, match in enumerate(matches[:5]):  # 显示前 5 个
            print(f"      {i+1}. {match.skill_name} ({match.match_score:.2f})")
        
        return matches
    
    def _build_index(self):
        """构建技能索引 (增强版 - 支持 SKILL_FRONTMATTER.md)"""
        if not self.skills_dir.exists():
            print(f"⚠️  技能目录不存在：{self.skills_dir}")
            return
        
        # 遍历所有技能目录
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            # 优先读取 SKILL_FRONTMATTER.md (包含丰富关键词)
            skill_frontmatter = skill_dir / "SKILL_FRONTMATTER.md"
            skill_md = skill_dir / "SKILL.md"
            
            if skill_frontmatter.exists():
                # 解析 SKILL_FRONTMATTER.md
                skill_info = self._parse_skill_frontmatter(skill_frontmatter)
            elif skill_md.exists():
                # 解析 SKILL.md
                skill_info = self._parse_skill_md(skill_md)
            else:
                continue
            
            if skill_info:
                self.skills_cache[str(skill_dir)] = skill_info
        
        print(f"   📚 技能索引：{len(self.skills_cache)} 个技能")
    
    def _parse_skill_frontmatter(self, skill_frontmatter_path: Path) -> Optional[Dict[str, Any]]:
        """解析 SKILL_FRONTMATTER.md 文件 (包含丰富关键词)"""
        try:
            with open(skill_frontmatter_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            info = {}
            
            # 提取 name
            name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
            if name_match:
                info["name"] = name_match.group(1).strip()
            else:
                info["name"] = skill_frontmatter_path.parent.name
            
            # 提取 description (包含关键词)
            desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
            if desc_match:
                info["description"] = desc_match.group(1).strip()
            else:
                info["description"] = ""
            
            # 提取 capabilities
            cap_match = re.search(r'^capabilities:\s*(.+)$', content, re.MULTILINE)
            if cap_match:
                info["capabilities"] = [c.strip() for c in cap_match.group(1).split(',')]
            else:
                info["capabilities"] = []
            
            # 提取完整内容 (用于语义搜索)
            info["full_content"] = content
            
            return info
            
        except Exception as e:
            print(f"⚠️  解析 SKILL_FRONTMATTER.md 失败：{skill_frontmatter_path} - {e}")
            return None
    
    def _parse_skill_md(self, skill_md_path: Path) -> Optional[Dict[str, Any]]:
        """解析 SKILL.md 文件"""
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取 front matter
            info = {}
            
            # 提取 name (支持 --- front matter 格式)
            name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
            if name_match:
                info["name"] = name_match.group(1).strip()
            else:
                # 从路径提取名称
                info["name"] = skill_md_path.parent.name
            
            # 提取 description
            desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
            if desc_match:
                info["description"] = desc_match.group(1).strip()
            else:
                info["description"] = ""
            
            # 提取 capabilities (从核心能力章节)
            capabilities = []
            if "核心能力" in content or "能力" in content:
                # 简单提取：能力类型关键词
                capability_keywords = [
                    "browser", "analysis", "writing", "data_processing",
                    "automation", "decision", "search", "planning",
                    "execution", "evaluation", "creation"
                ]
                for keyword in capability_keywords:
                    if keyword.lower() in content.lower():
                        capabilities.append(keyword)
            
            info["capabilities"] = capabilities[:10]  # 限制数量
            
            # 提取完整内容 (用于语义搜索)
            info["full_content"] = content
            
            return info
            
        except Exception as e:
            print(f"⚠️  解析 SKILL.md 失败：{skill_md_path} - {e}")
            return None
    
    def _calculate_match_score(self, query: str, skill_info: Dict[str, Any]) -> tuple:
        """
        计算技能与任务的匹配度 (优化版 - 名称权重提升)
        
        Returns:
            (match_score, match_reasons)
        """
        score = 0.0
        reasons = []
        
        query_lower = query.lower()
        skill_name = skill_info.get("name", "").lower()
        skill_desc = skill_info.get("description", "").lower()
        full_content = skill_info.get("full_content", "").lower()
        
        # 1. 名称精准匹配 (权重 0.5 - 提升) + 名称映射
        query_keywords = self._extract_keywords(query)
        matched_keywords = []
        
        # 名称映射匹配 (新增 - 支持中英文)
        name_match_found = False
        for mapped_name, aliases in self.NAME_MAPPING.items():
            if skill_name.lower() == mapped_name.lower():
                # 检查查询是否包含任何别名
                for alias in aliases:
                    if alias.lower() in query_lower or alias.lower() in query:
                        score += 0.5
                        reasons.append(f"名称映射匹配：{skill_name} (匹配：{alias})")
                        name_match_found = True
                        break
                if name_match_found:
                    break
        
        # 名称完全匹配或包含 (最高 0.5 分)
        if not name_match_found:
            if skill_name and skill_name in query_lower:
                score += 0.5
                reasons.append(f"名称完全匹配：{skill_name}")
            elif skill_name and any(kw in skill_name for kw in query_keywords):
                score += 0.3
                matched_keywords.append(f"名称包含：{skill_name}")
        
        # 2. 关键词匹配 (权重 0.4 - 提升)
        for keyword in query_keywords:
            # 降低词长限制 (>1 字符即可)
            if len(keyword) < 1:
                continue
            
            if keyword in skill_name and f"名称包含：{skill_name}" not in str(matched_keywords):
                score += 0.2
                matched_keywords.append(f"名称：{keyword}")
            elif keyword in skill_desc:
                score += 0.15
                matched_keywords.append(f"描述：{keyword}")
            elif keyword in full_content:
                score += 0.08
                matched_keywords.append(f"内容：{keyword}")
        
        if matched_keywords:
            reasons.append(f"关键词匹配：{', '.join(matched_keywords[:5])}")
        
        # 2. 语义匹配 (权重 0.3)
        semantic_patterns = {
            "搜索": ["search", "find", "lookup", "query"],
            "任务": ["task", "job", "work", "plan"],
            "记录": ["record", "log", "trace", "memory"],
            "生成": ["generate", "create", "make", "produce"],
            "视频": ["video", "movie", "clip"],
            "规划": ["plan", "planning", "orchestrate"],
            "分解": ["decompose", "breakdown", "split"],
            "评估": ["evaluate", "assess", "score", "rate"],
            "分析": ["analyze", "analysis"],
            "股票": ["stock", "finance", "trading"],
        }
        
        for cn_word, en_words in semantic_patterns.items():
            if cn_word in query_lower:
                for en_word in en_words:
                    if en_word in full_content:
                        score += 0.1
                        reasons.append(f"语义匹配：{cn_word}→{en_word}")
                        break
        
        # 3. 描述相似度 (权重 0.2)
        if skill_desc and any(kw in skill_desc for kw in query_keywords):
            score += 0.2
            reasons.append(f"描述相关：{skill_desc[:40]}")
        
        # 4. 能力类型匹配 (权重 0.1)
        capabilities = skill_info.get("capabilities", [])
        for cap in capabilities:
            if cap.lower() in query_lower:
                score += 0.05
                reasons.append(f"能力匹配：{cap}")
        
        # 限制最高分 1.0
        score = min(1.0, score)
        
        return score, reasons
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词 (增强版 - 支持中文分词)"""
        # 移除常见停用词 (精简版)
        stopwords = {
            "的", "了", "是", "在", "我", "有", "和", "就", "不", "都",
            "一", "上", "也", "很", "到", "说", "要", "去",
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "to", "have", "has", "had", "do", "does", "did"
        }
        
        # 中文分词 (简单版本 - 按字符和英文单词)
        keywords = []
        
        # 1. 提取英文单词
        en_words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        keywords.extend([w for w in en_words if w not in stopwords and len(w) > 1])
        
        # 2. 提取中文字符 (连续 2-4 个中文字符作为一个词)
        cn_words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        keywords.extend([w for w in cn_words if w not in stopwords])
        
        # 3. 单个重要中文字 (生成、视频、搜索等)
        important_single_chars = {
            "搜", "索", "生", "成", "视", "频", "任", "务", "记", "录",
            "规", "划", "分", "解", "评", "估", "分", "析", "股", "票"
        }
        single_chars = re.findall(r'[\u4e00-\u9fa5]', text)
        keywords.extend([c for c in single_chars if c in important_single_chars])
        
        # 去重和限制数量
        unique_keywords = list(dict.fromkeys(keywords))
        return unique_keywords[:20]


def main():
    """测试函数"""
    print("="*60)
    print("  技能搜索引擎测试")
    print("="*60)
    
    engine = SkillSearchEngine()
    
    # 测试查询
    test_queries = [
        "搜索昨天的任务记录",
        "生成一个抖音视频",
        "分析股票走势并预测",
        "任务规划和分解",
        "技能评估和评分"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"测试查询：{query}")
        print("="*60)
        
        matches = engine.search_local_skills(query, threshold=0.5)
        
        if matches:
            print(f"\n最佳匹配：")
            print(f"  技能：{matches[0].skill_name}")
            print(f"  匹配度：{matches[0].match_score:.2f}")
            print(f"  原因：{matches[0].match_reasons}")
        else:
            print(f"\n❌ 无匹配技能")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
