#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TraceReview 轻量化真实复盘模块

OpenHarness 核心移植 - 解决假学习终极模块
每一次任务结束强制输出固定 JSON 复盘，禁止段落聊天总结
自动存入本地 trace_memory/ 目录，uuid 命名，永久保存
下一次启动任务，自动检索相似任务记忆载入上下文

作者：AI Agent (移植 OpenHarness)
日期：2026-04-14
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib


@dataclass
class TraceReview:
    """
    结构化复盘记录
    
    判定真学习唯一标准：
    1. 写入本地结构化文件
    2. 数据库记录
    3. 下次任务自动读取复用
    """
    task_id: str
    task_summary: str  # 任务摘要
    operation_pattern: str  # 操作模式
    mistake_record: str  # 错误记录
    reusable_knowledge: str  # 可复用知识
    next_time_strategy: str  # 下次策略
    created_at: str
    tags: List[str]
    success: bool
    duration_seconds: float = 0.0
    tools_used: List[str] = None
    
    def __post_init__(self):
        if self.tools_used is None:
            self.tools_used = []
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class TraceReviewManager:
    """
    复盘记录管理器
    
    核心能力：
    1. 强制结构化输出 JSON 复盘
    2. 自动存入 trace_memory/ 目录
    3. 下次任务自动检索相似记忆
    """
    
    def __init__(self, storage_dir: str = "/root/.openclaw/workspace/trace_memory"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_dir / "trace_index.json"
        self.index = self._load_index()
    
    def _load_index(self) -> Dict[str, Any]:
        """加载索引文件"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"traces": [], "last_updated": None}
    
    def _save_index(self):
        """保存索引文件"""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def create_review(
        self,
        task_summary: str,
        operation_pattern: str,
        mistake_record: str = "",
        reusable_knowledge: str = "",
        next_time_strategy: str = "",
        tags: List[str] = None,
        success: bool = True,
        duration_seconds: float = 0.0,
        tools_used: List[str] = None,
    ) -> TraceReview:
        """
        创建复盘记录
        
        强制结构化字段，禁止自由发挥
        """
        task_id = str(uuid.uuid4())[:8]
        
        review = TraceReview(
            task_id=task_id,
            task_summary=task_summary.strip(),
            operation_pattern=operation_pattern.strip(),
            mistake_record=mistake_record.strip(),
            reusable_knowledge=reusable_knowledge.strip(),
            next_time_strategy=next_time_strategy.strip(),
            created_at=datetime.now().isoformat(),
            tags=tags or [],
            success=success,
            duration_seconds=duration_seconds,
            tools_used=tools_used or [],
        )
        
        # 保存到文件
        self._save_review(review)
        
        # 更新索引
        self._add_to_index(review)
        
        return review
    
    def _save_review(self, review: TraceReview):
        """保存复盘到独立文件"""
        filename = f"trace_{review.task_id}_{review.created_at[:10]}.json"
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(review.to_json())
        
        return filepath
    
    def _add_to_index(self, review: TraceReview):
        """添加到索引"""
        self.index["traces"].append({
            "task_id": review.task_id,
            "task_summary": review.task_summary,
            "created_at": review.created_at,
            "tags": review.tags,
            "success": review.success,
            "filename": f"trace_{review.task_id}_{review.created_at[:10]}.json",
        })
        self._save_index()
    
    def search_similar(
        self,
        query: str,
        limit: int = 5,
        min_similarity: float = 0.6,
    ) -> List[TraceReview]:
        """
        搜索相似任务的复盘记录
        
        下一次启动任务时自动调用，载入相似任务记忆
        """
        results = []
        query_hash = self._text_hash(query)
        
        for trace_info in self.index["traces"]:
            # 加载完整复盘
            filepath = self.storage_dir / trace_info["filename"]
            if not filepath.exists():
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    review = TraceReview(**data)
            except Exception:
                continue
            
            # 简单相似度计算 (基于关键词匹配)
            similarity = self._calculate_similarity(query, review.task_summary)
            
            if similarity >= min_similarity:
                results.append((similarity, review))
        
        # 按相似度排序
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [review for _, review in results[:limit]]
    
    def _text_hash(self, text: str) -> str:
        """文本哈希"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度 (简化版 Jaccard 相似度)
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def get_all_reviews(self, limit: int = 50) -> List[TraceReview]:
        """获取所有复盘记录"""
        results = []
        
        for trace_info in reversed(self.index["traces"][-limit:]):
            filepath = self.storage_dir / trace_info["filename"]
            if not filepath.exists():
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    review = TraceReview(**data)
                    results.append(review)
            except Exception:
                continue
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = len(self.index["traces"])
        success_count = sum(1 for t in self.index["traces"] if t.get("success", True))
        
        return {
            "total_traces": total,
            "success_count": success_count,
            "failure_count": total - success_count,
            "success_rate": success_count / total if total > 0 else 0.0,
            "last_updated": self.index.get("last_updated"),
        }


class TaskExecutor:
    """
    任务执行器 (集成 TraceReview)
    
    在 OpenClaw 主任务中调用：
    1. 任务开头：search_similar() 载入相似记忆
    2. 任务结尾：create_review() 强制写入复盘
    """
    
    def __init__(self, review_manager: TraceReviewManager = None):
        self.review_manager = review_manager or TraceReviewManager()
    
    def execute_task(self, task_description: str) -> Dict[str, Any]:
        """
        执行任务 (示例)
        
        真实使用时需要集成到 OpenClaw 主循环
        """
        start_time = datetime.now()
        
        # 步骤 1: 任务开头 - 检索相似记忆
        similar_memories = self.review_manager.search_similar(task_description, limit=3)
        
        context = {
            "task": task_description,
            "similar_memories": [m.to_dict() for m in similar_memories],
        }
        
        # 步骤 2: 执行任务 (这里是示例，实际需要集成到 OpenClaw)
        # ... 执行逻辑 ...
        
        # 步骤 3: 任务结尾 - 强制写入复盘
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        review = self.review_manager.create_review(
            task_summary=task_description,
            operation_pattern="示例模式",
            mistake_record="",
            reusable_knowledge="",
            next_time_strategy="",
            tags=["示例"],
            success=True,
            duration_seconds=duration,
        )
        
        return {
            "status": "completed",
            "review": review.to_dict(),
            "context": context,
        }


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 创建复盘管理器
    manager = TraceReviewManager()
    
    # 创建复盘记录
    review = manager.create_review(
        task_summary="测试任务：文件读取和编辑",
        operation_pattern="read→edit→save",
        mistake_record="无",
        reusable_knowledge="使用 read 工具读取文件，edit 工具编辑，write 工具写入",
        next_time_strategy="优先使用 edit 工具进行小修改",
        tags=["文件操作", "测试"],
        success=True,
        duration_seconds=1.5,
        tools_used=["read", "edit", "write"],
    )
    
    print(f"✅ 复盘记录已保存：{review.task_id}")
    print(f"📊 统计信息：{manager.get_stats()}")
    
    # 搜索相似记忆
    similar = manager.search_similar("文件编辑任务", limit=3)
    print(f"🔍 找到 {len(similar)} 条相似记忆")
    
    # 执行器示例
    executor = TaskExecutor(manager)
    result = executor.execute_task("测试任务：文件读取和编辑")
    print(f"📦 执行结果：{result['status']}")
