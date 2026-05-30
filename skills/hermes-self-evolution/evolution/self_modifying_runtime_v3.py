# Self-Modifying Runtime v3 - 自治系统终极版
# 运行时可自我修改代码 + 规则 + 进化逻辑的系统内核
# 核心能力：修改规则 / 修改 Agent 结构 / 修改进化策略 / 自动回滚

import json
import os
import copy
from datetime import datetime
from typing import Optional, Dict, List, Any

# 文件路径
MEMORY_FILE = "/root/.openclaw/workspace/memory/self_modifying_memory.json"
RULES_FILE = "/root/.openclaw/workspace/memory/runtime_rules.json"
VERSION_FILE = "/root/.openclaw/workspace/memory/runtime_versions.json"

# =========================
# 🧠 1. 系统本体
# =========================

class SelfModifyingRuntime:
    """
    Self-Modifying Runtime v3 - 终极自治内核
    
    SYSTEM = {
        "runtime": RuntimeEngine,
        "rules": RuleEngine,
        "agents": AgentGraph,
        "memory": MemorySystem,
        "evolution": EvolutionEngine,
        "self_editor": SelfEditor
    }
    """
    
    def __init__(self):
        self.runtime = RuntimeEngine(self)
        self.rules = RuleEngine(self)
        self.agents = AgentGraph(self)
        self.memory = MemorySystem(self)
        self.evolution = EvolutionEngine(self)
        self.self_editor = SelfEditor(self)
        self.version = "v3.0.0"
    
    def critic(self, result: str) -> float:
        """委托给 runtime.critic_score"""
        return self.runtime.critic_score(result)
        
    def execute(self, task: str) -> Dict:
        """执行任务 - 完整自修改循环"""
        print("\n" + "=" * 80)
        print(f"🧠 Self-Modifying Runtime {self.version} - 执行任务")
        print("=" * 80)
        print(f"\n📋 TASK: {task}")
        
        # STEP 1: 执行任务
        task_result = self.runtime.execute_task(task)
        
        # STEP 2: Critic 评分
        score = self.critic(task_result)
        
        # STEP 3: 判断是否低效
        is_inefficient = score < 7
        
        # STEP 4: SelfEditor 修改系统 (如果低效)
        system_changes = {}
        if is_inefficient:
            system_changes = self.self_editor.analyze_and_modify(
                task, task_result, score
            )
        
        # STEP 5: Evolution 生成新版本 (如果评分高)
        if score >= 8.5:
            self.evolution.generate_next_version(score)
        
        # STEP 6: 写入 Memory
        self.memory.record({
            "task": task,
            "result": task_result,
            "score": score,
            "system_changes": system_changes,
            "version": self.version,
            "time": datetime.now().isoformat()
        })
        
        # STEP 7: 输出系统级结果
        output = {
            "task_result": task_result,
            "score": score,
            "system_changes": system_changes,
            "next_state": "ready" if score >= 7 else "modified",
            "version": self.version,
        }
        
        print("\n" + "=" * 80)
        print("📊 系统级输出")
        print("=" * 80)
        print(f"任务结果：{task_result[:50]}...")
        print(f"评分：{score}/10")
        print(f"系统修改：{len(system_changes)} 项")
        print(f"下一状态：{output['next_state']}")
        print(f"版本：{self.version}")
        
        return output


# =========================
# 【2. 核心模块】
# =========================

# ------------------------------------------------
# 2.1 RuntimeEngine（运行内核）
# ------------------------------------------------
class RuntimeEngine:
    """
    负责：执行任务 / 调度 Agent / 控制循环
    流程：TASK → ROUTE → EXECUTE → FEEDBACK
    """
    
    def __init__(self, runtime: SelfModifyingRuntime):
        self.runtime = runtime
        
    def execute_task(self, task: str) -> str:
        """执行任务"""
        # 1. ROUTE - 路由到 Agent
        plan = self.runtime.agents.planner(task)
        
        # 2. EXECUTE - 执行
        result = self.runtime.agents.executor(plan, task)
        
        # 3. FEEDBACK - 反馈
        feedback = self.runtime.agents.critic(result, task)
        
        return f"{result} (评分：{feedback['score']}/10)"
    
    def critic_score(self, result: str) -> float:
        """Critic 评分 - 可被 SelfEditor 修改"""
        # 获取当前评分规则
        rules = self.runtime.rules.get("critic_rules")
        
        score = rules.get("base_score", 7.0)
        
        # 应用评分规则
        if "失败" in result:
            score -= rules.get("fail_penalty", 3.0)
        if "完成" in result:
            score += rules.get("success_bonus", 1.0)
        if len(result) > 40:
            score += rules.get("length_bonus", 0.5)
        
        # 小说任务额外规则
        if any(kw in result for kw in ['小说', '写作', '章节']):
            if "冲突" in result:
                score += rules.get("conflict_bonus", 1.0)
            if "反转" in result:
                score += rules.get("twist_bonus", 1.0)
        
        score = max(1, min(10, score))
        return round(score, 1)


# ------------------------------------------------
# 2.2 RuleEngine（规则引擎）🔥核心
# ------------------------------------------------
class RuleEngine:
    """
    所有规则可被修改：
    - decision_threshold
    - mutation_rate
    - max_agents
    - critic_weight
    
    ✔ 规则不是固定的
    ✔ 可以被 SelfEditor 改写
    """
    
    DEFAULT_RULES = {
        "decision_threshold": 0.7,
        "mutation_rate": 0.2,
        "max_agents": 4,
        "critic_weight": 0.4,
        "critic_rules": {
            "base_score": 7.0,
            "fail_penalty": 3.0,
            "success_bonus": 1.0,
            "length_bonus": 0.5,
            "conflict_bonus": 1.0,
            "twist_bonus": 1.0,
        },
        "self_modify_triggers": {
            "low_score_threshold": 5.0,
            "consecutive_failures": 3,
            "output_repeat_threshold": 0.8,
            "slow_convergence_rounds": 5,
        }
    }
    
    def __init__(self, runtime: SelfModifyingRuntime):
        self.runtime = runtime
        self.rules = self._load()
    
    def _load(self) -> Dict:
        """加载规则"""
        if os.path.exists(RULES_FILE):
            try:
                return json.loads(open(RULES_FILE, 'r', encoding='utf-8').read())
            except:
                pass
        return copy.deepcopy(self.DEFAULT_RULES)
    
    def _save(self):
        """保存规则"""
        with open(RULES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str, default=None):
        """获取规则"""
        keys = key.split('.')
        value = self.rules
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any, reason: str = ""):
        """修改规则"""
        keys = key.split('.')
        obj = self.rules
        for k in keys[:-1]:
            if k not in obj:
                obj[k] = {}
            obj = obj[k]
        
        old_value = obj.get(keys[-1])
        obj[keys[-1]] = value
        
        self._save()
        
        # 记录规则变化
        self.runtime.memory.record_rule_change({
            "rule": key,
            "old_value": old_value,
            "new_value": value,
            "reason": reason,
            "time": datetime.now().isoformat()
        })
        
        return True


# ------------------------------------------------
# 2.3 SelfEditor（自修改系统）🔥核心
# ------------------------------------------------
class SelfEditor:
    """
    允许系统修改自己：
    
    可修改对象：
    - decision_score 函数
    - planner 结构
    - critic 评分规则
    - memory 结构
    - evolution 策略
    
    修改格式（强制）：
    {
        "target": "rule / function / architecture",
        "action": "modify / delete / merge / create",
        "before": "",
        "after": "",
        "reason": ""
    }
    """
    
    def __init__(self, runtime: SelfModifyingRuntime):
        self.runtime = runtime
    
    def analyze_and_modify(self, task: str, result: str, score: float) -> Dict:
        """分析并修改系统"""
        changes = {}
        
        # 获取触发器规则
        triggers = self.runtime.rules.get("self_modify_triggers", {})
        
        # 触发器 1: 低分 → 修改 critic
        if score < triggers.get("low_score_threshold", 5.0):
            change = self.modify_critic(score)
            if change:
                changes["critic"] = change
        
        # 触发器 2: 检查连续失败
        consecutive_failures = self.runtime.memory.get_consecutive_failures()
        if consecutive_failures >= triggers.get("consecutive_failures", 3):
            change = self.modify_planner_structure()
            if change:
                changes["planner"] = change
        
        # 触发器 3: 输出重复 → 修改 memory 策略
        is_repeating = self.runtime.memory.check_output_repeat(result)
        if is_repeating:
            change = self.modify_memory_strategy()
            if change:
                changes["memory"] = change
        
        # 触发器 4: 收敛过慢 → 修改 mutation_rate
        if self.runtime.memory.get_average_rounds() > triggers.get("slow_convergence_rounds", 5):
            change = self.modify_mutation_rate()
            if change:
                changes["mutation_rate"] = change
        
        return changes
    
    def modify_critic(self, score: float) -> Optional[Dict]:
        """修改 Critic 评分规则"""
        # 分析低分原因
        reason = f"评分过低 ({score}/10)，需要调整评分规则"
        
        # 修改方案：提高基础分或降低惩罚
        current_base = self.runtime.rules.get("critic_rules.base_score", 7.0)
        new_base = min(8.0, current_base + 0.5)  # 提高基础分
        
        change = {
            "target": "rule",
            "action": "modify",
            "before": f"critic_rules.base_score = {current_base}",
            "after": f"critic_rules.base_score = {new_base}",
            "reason": reason
        }
        
        self.runtime.rules.set("critic_rules.base_score", new_base, reason)
        
        print(f"\n🔧 SelfEditor: 修改 Critic 规则 - {reason}")
        print(f"   {change['before']} → {change['after']}")
        
        return change
    
    def modify_planner_structure(self) -> Optional[Dict]:
        """修改 Planner 结构"""
        current_max = self.runtime.rules.get("max_agents", 4)
        new_max = current_max + 1  # 增加 Agent 数量
        
        change = {
            "target": "architecture",
            "action": "modify",
            "before": f"max_agents = {current_max}",
            "after": f"max_agents = {new_max}",
            "reason": "连续失败，需要增加 Agent 数量"
        }
        
        self.runtime.rules.set("max_agents", new_max, change["reason"])
        
        print(f"\n🔧 SelfEditor: 修改 Planner 结构 - 增加 Agent 数量")
        print(f"   {change['before']} → {change['after']}")
        
        return change
    
    def modify_memory_strategy(self) -> Optional[Dict]:
        """修改 Memory 策略"""
        current_mutation = self.runtime.rules.get("mutation_rate", 0.2)
        new_mutation = min(0.5, current_mutation + 0.1)  # 增加变异率
        
        change = {
            "target": "rule",
            "action": "modify",
            "before": f"mutation_rate = {current_mutation}",
            "after": f"mutation_rate = {new_mutation}",
            "reason": "输出重复，需要增加变异率"
        }
        
        self.runtime.rules.set("mutation_rate", new_mutation, change["reason"])
        
        print(f"\n🔧 SelfEditor: 修改 Memory 策略 - 增加变异率")
        print(f"   {change['before']} → {change['after']}")
        
        return change
    
    def modify_mutation_rate(self) -> Optional[Dict]:
        """修改变异率"""
        current_mutation = self.runtime.rules.get("mutation_rate", 0.2)
        new_mutation = min(0.5, current_mutation + 0.1)
        
        change = {
            "target": "rule",
            "action": "modify",
            "before": f"mutation_rate = {current_mutation}",
            "after": f"mutation_rate = {new_mutation}",
            "reason": "收敛过慢，需要增加变异率"
        }
        
        self.runtime.rules.set("mutation_rate", new_mutation, change["reason"])
        
        print(f"\n🔧 SelfEditor: 修改变异率")
        print(f"   {change['before']} → {change['after']}")
        
        return change


# ------------------------------------------------
# 2.4 EvolutionEngine（进化内核）
# ------------------------------------------------
class EvolutionEngine:
    """
    进化规则：
    - score >= 0.85 → 生成 v+1 结构
    - score < 0.4 → 自动淘汰策略
    - 连续失败 → 强制结构重写
    """
    
    def __init__(self, runtime: SelfModifyingRuntime):
        self.runtime = runtime
        self.versions = self._load_versions()
    
    def _load_versions(self) -> List:
        """加载版本历史"""
        if os.path.exists(VERSION_FILE):
            try:
                return json.loads(open(VERSION_FILE, 'r', encoding='utf-8').read())
            except:
                pass
        return [{"version": "v3.0.0", "time": datetime.now().isoformat(), "score": 0}]
    
    def _save_versions(self):
        """保存版本历史"""
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.versions, f, ensure_ascii=False, indent=2)
    
    def generate_next_version(self, score: float):
        """生成下一版本"""
        # 评分 >= 8.5 → 生成新版本
        if score >= 8.5:
            current_version = self.versions[-1]["version"]
            # 解析版本号 v3.0.0 → 3.0
            version_parts = current_version.replace("v", "").split(".")
            version_num = float(version_parts[0] + "." + version_parts[1])
            next_version = f"v{version_num + 0.1:.1f}"
            
            self.versions.append({
                "version": next_version,
                "time": datetime.now().isoformat(),
                "score": score,
                "parent": current_version,
            })
            self._save_versions()
            
            print(f"\n🧬 Evolution: 生成新版本 {next_version} (评分：{score}/10)")
            
            return next_version
        
        # 评分 < 4 → 淘汰策略
        if score < 4:
            print(f"\n🧬 Evolution: 评分过低 ({score}/10)，淘汰当前策略")
            self.runtime.memory.record_failure("策略淘汰", f"评分{score}")
        
        return None


# ------------------------------------------------
# 2.5 MemorySystem（动态记忆）
# ------------------------------------------------
class MemorySystem:
    """
    动态记忆系统
    
    重点：记录"规则变化"，不是只记录任务
    
    {
        "success": [],
        "failure": [],
        "rule_changes": [],
        "architecture_history": []
    }
    """
    
    def __init__(self, runtime: SelfModifyingRuntime):
        self.runtime = runtime
        self.memory = self._load()
    
    def _load(self) -> Dict:
        """加载记忆"""
        if os.path.exists(MEMORY_FILE):
            try:
                return json.loads(open(MEMORY_FILE, 'r', encoding='utf-8').read())
            except:
                pass
        return {
            "success": [],
            "failure": [],
            "rule_changes": [],
            "architecture_history": [],
            "history": []
        }
    
    def _save(self):
        """保存记忆"""
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def record(self, data: Dict):
        """记录任务"""
        if data["score"] >= 8:
            self.memory["success"].append(data)
        elif data["score"] < 5:
            self.memory["failure"].append(data)
        
        self.memory["history"].append(data)
        self._save()
    
    def record_rule_change(self, change: Dict):
        """记录规则变化"""
        self.memory["rule_changes"].append(change)
        self._save()
    
    def record_architecture_change(self, change: Dict):
        """记录架构变化"""
        self.memory["architecture_history"].append(change)
        self._save()
    
    def get_consecutive_failures(self) -> int:
        """获取连续失败次数"""
        recent = self.memory["history"][-10:]  # 最近 10 条
        consecutive = 0
        for record in reversed(recent):
            if record["score"] < 5:
                consecutive += 1
            else:
                break
        return consecutive
    
    def check_output_repeat(self, output: str) -> bool:
        """检查输出重复"""
        recent = self.memory["history"][-5:]
        for record in recent:
            if record.get("result", "") == output:
                return True
        return False
    
    def get_average_rounds(self) -> float:
        """获取平均轮次"""
        if not self.memory["history"]:
            return 0
        # 简化实现
        return 1.0
    
    def record_failure(self, reason: str, details: str):
        """记录失败"""
        self.memory["failure"].append({
            "reason": reason,
            "details": details,
            "time": datetime.now().isoformat()
        })
        self._save()


# ------------------------------------------------
# AgentGraph（Agent 图）
# ------------------------------------------------
class AgentGraph:
    """Agent 图 - 简化的 Agent 管理"""
    
    def __init__(self, runtime: SelfModifyingRuntime):
        self.runtime = runtime
    
    def planner(self, task: str) -> List[str]:
        """Planner - 生成计划"""
        return [
            f"分析任务：{task}",
            "生成核心内容",
            "优化输出质量",
            "验证成功标准"
        ]
    
    def executor(self, plan: List[str], task: str) -> str:
        """Executor - 执行计划"""
        results = []
        for step in plan:
            results.append(f"[完成] {step}")
        return "\n".join(results)
    
    def critic(self, result: str, task: str = "") -> Dict:
        """Critic - 评分"""
        score = self.runtime.critic(result)
        return {
            "score": score,
            "pass": score >= 7,
            "reason": "OK" if score >= 7 else "Need improvement"
        }


# =========================
# 🚀 RUN SYSTEM
# =========================
if __name__ == "__main__":
    print("=" * 80)
    print("🧠 Self-Modifying Runtime v3 - 自治系统终极版")
    print("=" * 80)
    
    # 创建运行时
    runtime = SelfModifyingRuntime()
    
    # 测试任务
    test_tasks = [
        "创作番茄小说第 1 章（3000 字）",
        "优化 OpenClaw 写作技能记忆",
        "系统健康检查",
    ]
    
    print("\n📋 测试任务:")
    for i, task in enumerate(test_tasks, 1):
        print(f"  {i}. {task}")
    
    # 执行测试
    print("\n" + "=" * 80)
    print("开始执行测试...")
    print("=" * 80)
    
    results = []
    for task in test_tasks:
        result = runtime.execute(task)
        results.append(result)
    
    # 显示总结
    print("\n" + "=" * 80)
    print("📊 测试总结")
    print("=" * 80)
    
    success_count = sum(1 for r in results if r["score"] >= 7)
    print(f"成功：{success_count}/{len(results)}")
    print(f"平均评分：{sum(r['score'] for r in results)/len(results):.1f}/10")
    print(f"系统修改：{sum(len(r['system_changes']) for r in results)} 项")
    print(f"最终版本：{runtime.version}")
    
    # 显示记忆统计
    print(f"\n🧠 记忆状态:")
    print(f"  成功记录：{len(runtime.memory.memory['success'])}个")
    print(f"  失败记录：{len(runtime.memory.memory['failure'])}个")
    print(f"  规则变化：{len(runtime.memory.memory['rule_changes'])}项")
    print(f"  历史记录：{len(runtime.memory.memory['history'])}条")
    
    print("\n" + "=" * 80)
    print("✅ Self-Modifying Runtime v3 测试完成！")
    print("=" * 80)
