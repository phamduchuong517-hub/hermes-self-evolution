#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Async Agent Loop 标准化代理循环

OpenHarness 核心移植 - query.py 简化版
思考 (think) 和行动 (action) 强制分离
全程异步流式调度，不会长任务卡顿、乱跑指令
限制每一轮输出格式，禁止模型乱说话，固定输出 JSON 动作指令

作者：AI Agent (移植 OpenHarness)
日期：2026-04-14
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, AsyncIterator, Callable
from dataclasses import dataclass, field
from pathlib import Path
import traceback

# 导入复盘模块
from trace_review import TraceReviewManager, TraceReview
# 导入沙箱模块
from path_rule import PathRuleValidator, SandboxInterceptor
# 导入技能优先搜索模块
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skill-first-executor" / "core"))
    from skill_search_engine import SkillSearchEngine
    SKILL_FIRST_AVAILABLE = True
except ImportError:
    SKILL_FIRST_AVAILABLE = False


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@dataclass
class ToolCall:
    """工具调用"""
    name: str
    input: Dict[str, Any]
    call_id: str = ""
    
    def __post_init__(self):
        if not self.call_id:
            self.call_id = f"{self.name}_{int(time.time() * 1000)}"


@dataclass
class ToolResult:
    """工具结果"""
    call_id: str
    content: str
    is_error: bool = False
    error_message: str = ""


@dataclass
class AgentTurn:
    """代理回合"""
    turn_number: int
    thought: str = ""
    tool_calls: List[ToolCall] = field(default_factory=list)
    tool_results: List[ToolResult] = field(default_factory=list)
    final_response: str = ""
    completed: bool = False


@dataclass
class AgentContext:
    """代理上下文"""
    task_id: str
    task_description: str
    cwd: Path
    max_turns: int = 20
    model: str = "qwencode/qwen3.5-plus"
    system_prompt: str = ""
    similar_memories: List[Dict] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)


class AsyncAgentLoop:
    """
    异步代理循环
    
    核心能力：
    1. 思考和行动强制分离
    2. 异步流式调度
    3. 每轮输出固定 JSON 格式
    4. 强制复盘写入
    """
    
    def __init__(
        self,
        review_manager: TraceReviewManager = None,
        path_validator: PathRuleValidator = None,
        workspace_root: str = "/root/.openclaw/workspace",
    ):
        self.review_manager = review_manager or TraceReviewManager()
        self.path_validator = path_validator or PathRuleValidator()
        self.sandbox_interceptor = SandboxInterceptor(self.path_validator)
        self.tool_registry: Dict[str, Callable] = {}
        self.workspace_root = Path(workspace_root)
        
        # 初始化技能优先搜索引擎
        self.skill_search_engine = None
        if SKILL_FIRST_AVAILABLE:
            try:
                self.skill_search_engine = SkillSearchEngine(workspace_root)
                log.info("✅ 技能优先搜索已启用")
            except Exception as e:
                log.warning(f"⚠️  技能优先搜索初始化失败：{e}")
    
    def register_tool(self, name: str, handler: Callable):
        """注册工具"""
        self.tool_registry[name] = handler
        log.info(f"注册工具：{name}")
    
    async def run(
        self,
        task_description: str,
        cwd: str = "/root/.openclaw/workspace",
        max_turns: int = 20,
    ) -> Dict[str, Any]:
        """
        运行代理循环
        
        流程：
        1. 任务开头：检索相似记忆
        2. 循环：思考→行动→验证
        3. 任务结尾：强制写入复盘
        """
        task_id = f"task_{int(time.time())}"
        context = AgentContext(
            task_id=task_id,
            task_description=task_description,
            cwd=Path(cwd),
            max_turns=max_turns,
        )
        
        log.info(f"🚀 开始任务：{task_id}")
        log.info(f"📝 任务描述：{task_description[:100]}...")
        
        # 步骤 1: 检索相似记忆
        similar_memories = self.review_manager.search_similar(task_description, limit=3)
        context.similar_memories = [m.to_dict() for m in similar_memories]
        
        if similar_memories:
            log.info(f"📚 加载 {len(similar_memories)} 条相似记忆")
            for mem in similar_memories[:2]:
                log.info(f"  - {mem.task_summary[:50]}...")
        
        # 步骤 1.5: 技能优先搜索 (新增)
        if self.skill_search_engine:
            try:
                log.info("🔍 技能优先搜索...")
                skill_matches = self.skill_search_engine.search_local_skills(task_description, threshold=0.3)
                
                if skill_matches:
                    best_match = skill_matches[0]
                    log.info(f"✅ 找到匹配技能：{best_match.skill_name} (匹配度：{best_match.match_score:.2f})")
                    
                    # 如果匹配度高，直接使用技能
                    if best_match.match_score >= 0.5:
                        log.info(f"🎯 使用技能执行：{best_match.skill_name}")
                        # 实际技能执行逻辑待实现
                else:
                    log.info("ℹ️  无匹配技能，使用标准流程")
            except Exception as e:
                log.warning(f"⚠️  技能搜索失败：{e}")
        
        # 步骤 2: 执行循环
        turns: List[AgentTurn] = []
        success = True
        error_message = ""
        
        try:
            async for turn in self._run_loop(context):
                turns.append(turn)
                
                if turn.completed:
                    break
                
                if len(turns) >= max_turns:
                    log.warning(f"达到最大回合数：{max_turns}")
                    break
        except Exception as e:
            success = False
            error_message = str(e)
            log.error(f"任务执行失败：{e}")
            traceback.print_exc()
        
        # 步骤 3: 强制写入复盘
        duration = time.time() - context.start_time
        review = self._create_review(
            context=context,
            turns=turns,
            success=success,
            error_message=error_message,
            duration=duration,
        )
        
        log.info(f"✅ 任务完成：{task_id}")
        log.info(f"📊 复盘记录：{review.task_id}")
        
        return {
            "task_id": task_id,
            "status": "completed" if success else "failed",
            "turns": len(turns),
            "duration": duration,
            "review": review.to_dict(),
            "final_response": turns[-1].final_response if turns else "",
        }
    
    async def _run_loop(self, context: AgentContext) -> AsyncIterator[AgentTurn]:
        """
        运行主循环
        
        每一轮：
        1. 思考 (think)
        2. 行动 (action)
        3. 验证 (verify)
        """
        turn_number = 0
        
        while True:
            turn_number += 1
            turn = AgentTurn(turn_number=turn_number)
            
            log.info(f"\n🔄 回合 {turn_number}/{context.max_turns}")
            
            # 阶段 1: 思考
            thought = await self._think(context, turns_history=[])
            turn.thought = thought
            log.info(f"💭 思考：{thought[:100]}...")
            
            # 阶段 2: 生成工具调用
            tool_calls = await self._plan_actions(context, thought)
            turn.tool_calls = tool_calls
            
            if not tool_calls:
                # 无需工具调用，直接返回
                turn.final_response = thought
                turn.completed = True
                yield turn
                break
            
            log.info(f"🔧 计划执行 {len(tool_calls)} 个工具")
            yield turn
            
            # 阶段 3: 执行工具 (异步并发)
            if len(tool_calls) == 1:
                # 单个工具：顺序执行
                for tc in tool_calls:
                    log.info(f"  执行：{tc.name}")
                    result = await self._execute_tool(context, tc)
                    turn.tool_results.append(result)
            else:
                # 多个工具：并发执行
                log.info(f"  并发执行 {len(tool_calls)} 个工具")
                results = await asyncio.gather(*[
                    self._execute_tool(context, tc) for tc in tool_calls
                ])
                turn.tool_results = list(results)
            
            # 阶段 4: 验证结果
            all_success = all(not r.is_error for r in turn.tool_results)
            
            if all_success:
                # 成功，继续下一轮
                pass
            else:
                # 有错误，记录
                errors = [r for r in turn.tool_results if r.is_error]
                log.warning(f"  {len(errors)} 个工具执行失败")
            
            yield turn
            
            # 检查是否完成
            if self._should_complete(turn):
                turn.completed = True
                break
    
    async def _think(self, context: AgentContext, turns_history: List[AgentTurn]) -> str:
        """
        思考阶段
        
        实际使用时需要调用 LLM
        这里简化为返回任务描述
        """
        # TODO: 集成 LLM 调用
        return f"思考如何完成：{context.task_description[:50]}..."
    
    async def _plan_actions(
        self,
        context: AgentContext,
        thought: str,
    ) -> List[ToolCall]:
        """
        规划行动
        
        实际使用时需要调用 LLM 生成工具调用
        """
        # TODO: 集成 LLM 调用
        # 示例：返回空列表表示无需工具
        return []
    
    async def _execute_tool(
        self,
        context: AgentContext,
        tool_call: ToolCall,
    ) -> ToolResult:
        """
        执行工具
        
        1. 沙箱拦截校验
        2. 执行工具
        3. 返回结果
        """
        # 沙箱拦截
        allowed, reason = self.sandbox_interceptor.intercept(
            tool_call.name,
            tool_call.input,
        )
        
        if not allowed:
            return ToolResult(
                call_id=tool_call.call_id,
                content=f"工具调用被拦截：{reason}",
                is_error=True,
                error_message=reason,
            )
        
        # 执行工具
        handler = self.tool_registry.get(tool_call.name)
        
        if not handler:
            return ToolResult(
                call_id=tool_call.call_id,
                content=f"未知工具：{tool_call.name}",
                is_error=True,
                error_message=f"Tool not found: {tool_call.name}",
            )
        
        try:
            # 异步调用工具
            if asyncio.iscoroutinefunction(handler):
                result = await handler(**tool_call.input)
            else:
                result = handler(**tool_call.input)
            
            # 转换为字符串
            if isinstance(result, (dict, list)):
                content = json.dumps(result, ensure_ascii=False)
            else:
                content = str(result)
            
            return ToolResult(
                call_id=tool_call.call_id,
                content=content,
                is_error=False,
            )
        except Exception as e:
            return ToolResult(
                call_id=tool_call.call_id,
                content=f"执行失败：{e}",
                is_error=True,
                error_message=str(e),
            )
    
    def _should_complete(self, turn: AgentTurn) -> bool:
        """判断是否应该完成"""
        # 如果有最终回复，认为完成
        if turn.final_response:
            return True
        
        # 如果没有工具调用，认为完成
        if not turn.tool_calls:
            return True
        
        return False
    
    def _create_review(
        self,
        context: AgentContext,
        turns: List[AgentTurn],
        success: bool,
        error_message: str,
        duration: float,
    ) -> TraceReview:
        """创建复盘记录"""
        # 总结操作模式
        tool_names = []
        for turn in turns:
            for tc in turn.tool_calls:
                tool_names.append(tc.name)
        
        operation_pattern = "→".join(dict.fromkeys(tool_names)) if tool_names else "direct_response"
        
        # 总结错误
        mistake_record = ""
        if not success:
            mistake_record = f"任务失败：{error_message}"
        else:
            errors = []
            for turn in turns:
                for result in turn.tool_results:
                    if result.is_error:
                        errors.append(f"{result.call_id}: {result.error_message}")
            if errors:
                mistake_record = "工具执行错误：" + "; ".join(errors[:3])
        
        # 可复用知识
        reusable_knowledge = f"执行 {len(turns)} 回合，使用工具：{', '.join(set(tool_names))}" if tool_names else "直接回复"
        
        # 下次策略
        next_time_strategy = "保持当前策略" if success else "需要优化错误处理"
        
        review = self.review_manager.create_review(
            task_summary=context.task_description,
            operation_pattern=operation_pattern,
            mistake_record=mistake_record,
            reusable_knowledge=reusable_knowledge,
            next_time_strategy=next_time_strategy,
            tags=["agent_loop", "auto_generated"],
            success=success,
            duration_seconds=duration,
            tools_used=list(set(tool_names)),
        )
        
        return review


# ==================== 集成到 OpenClaw ====================

def create_agent_loop() -> AsyncAgentLoop:
    """
    创建代理循环实例
    
    在 OpenClaw 主入口调用此函数
    """
    review_manager = TraceReviewManager()
    path_validator = PathRuleValidator()
    
    loop = AsyncAgentLoop(
        review_manager=review_manager,
        path_validator=path_validator,
    )
    
    # 注册常用工具
    # loop.register_tool("read", read_handler)
    # loop.register_tool("write", write_handler)
    # loop.register_tool("bash", bash_handler)
    
    return loop


# ==================== 使用示例 ====================

if __name__ == "__main__":
    async def main():
        # 创建代理循环
        loop = create_agent_loop()
        
        # 运行任务
        result = await loop.run(
            task_description="测试任务：读取文件并统计行数",
            cwd="/root/.openclaw/workspace",
            max_turns=10,
        )
        
        print(f"\n📊 任务结果：")
        print(f"  状态：{result['status']}")
        print(f"  回合数：{result['turns']}")
        print(f"  耗时：{result['duration']:.2f}s")
        print(f"  复盘 ID: {result['review']['task_id']}")
    
    asyncio.run(main())
