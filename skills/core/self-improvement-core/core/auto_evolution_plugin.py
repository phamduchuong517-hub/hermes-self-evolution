#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cognitive Plugin v1.0 - 通用认知插件

为其他技能提供：
- 状态识别接口
- 阶段判断接口
- 路径推演接口
- 结构化分析框架
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 导入 Bagua Engine v3.0
from bagua_engine_v3 import BaguaEngineV3


class CognitivePlugin:
    """通用认知插件 v1.0"""
    
    def __init__(self):
        self.version = '1.0'
        self.bagua_engine = BaguaEngineV3()
        self.cache = {}
    
    def analyze(self, problem: str, context: Dict = None, 
                include_wuxing: bool = True, include_bagua: bool = True) -> Dict:
        """
        通用认知分析接口
        
        Args:
            problem: 问题描述
            context: 上下文信息
            include_wuxing: 是否包含五行分析
            include_bagua: 是否包含八卦分析
        
        Returns:
            认知分析结果
        """
        # 调用 Bagua Engine v3.0
        result = self.bagua_engine.analyze(problem, context)
        
        # 构建认知插件输出
        cognitive_result = {
            'version': self.version,
            'timestamp': datetime.now().isoformat(),
            'problem': problem,
            
            # 状态识别
            'state_recognition': {
                'primary_state': result['bagua_mapping']['primary_name'],
                'secondary_state': result['bagua_mapping']['secondary_name'],
                'stage': result['stage_analysis']['current_stage'],
            },
            
            # 阶段判断
            'stage_judgment': {
                'current_stage': result['stage_analysis']['current_stage'],
                'stage_description': result['stage_analysis']['stage_description'],
                'next_stage': result['stage_analysis']['next_stage'],
            },
            
            # 路径推演
            'path_inference': result['evolution_paths'],
        }
        
        # 可选：五行分析
        if include_wuxing:
            cognitive_result['five_elements'] = {
                'dominant': result['five_elements']['dominant_element'],
                'weak': result['five_elements']['weak_element'],
                'balance_score': result['five_elements']['balance_score'],
                'interpretation': result['five_elements']['interpretation'],
            }
        
        # 可选：八卦分析
        if include_bagua:
            cognitive_result['bagua'] = {
                'primary': result['bagua_mapping']['primary_trigram'],
                'secondary': result['bagua_mapping']['secondary_trigram'],
                'contradiction': result['key_contradiction'],
            }
        
        # 建议动作
        cognitive_result['suggested_actions'] = result['suggested_actions']
        
        return cognitive_result
    
    def get_state(self, problem: str) -> Dict:
        """
        状态识别接口
        
        Args:
            problem: 问题描述
        
        Returns:
            状态识别结果
        """
        result = self.bagua_engine.analyze(problem)
        return {
            'primary_state': result['bagua_mapping']['primary_name'],
            'secondary_state': result['bagua_mapping']['secondary_name'],
            'stage': result['stage_analysis']['current_stage'],
            'element': result['bagua_mapping']['primary_element'],
        }
    
    def get_stage(self, problem: str) -> Dict:
        """
        阶段判断接口
        
        Args:
            problem: 问题描述
        
        Returns:
            阶段判断结果
        """
        result = self.bagua_engine.analyze(problem)
        return {
            'current_stage': result['stage_analysis']['current_stage'],
            'stage_description': result['stage_analysis']['stage_description'],
            'next_stage': result['stage_analysis']['next_stage'],
        }
    
    def get_paths(self, problem: str) -> List[Dict]:
        """
        路径推演接口
        
        Args:
            problem: 问题描述
        
        Returns:
            演化路径列表
        """
        result = self.bagua_engine.analyze(problem)
        return result['evolution_paths']
    
    def get_suggestions(self, problem: str) -> List[str]:
        """
        建议动作接口
        
        Args:
            problem: 问题描述
        
        Returns:
            建议动作列表
        """
        result = self.bagua_engine.analyze(problem)
        return result['suggested_actions']
    
    def analyze_with_cache(self, problem: str, cache_ttl: int = 3600) -> Dict:
        """
        带缓存的分析接口
        
        Args:
            problem: 问题描述
            cache_ttl: 缓存有效期 (秒)
        
        Returns:
            认知分析结果
        """
        # 检查缓存
        if problem in self.cache:
            cached = self.cache[problem]
            age = (datetime.now() - datetime.fromisoformat(cached['timestamp'])).total_seconds()
            if age < cache_ttl:
                return cached['result']
        
        # 执行分析
        result = self.analyze(problem)
        
        # 更新缓存
        self.cache[problem] = {
            'timestamp': datetime.now().isoformat(),
            'result': result,
        }
        
        return result
    
    def export_config(self) -> Dict:
        """导出配置"""
        return {
            'version': self.version,
            'bagua_engine_version': self.bagua_engine.version,
            'features': [
                'state_recognition',
                'stage_judgment',
                'path_inference',
                'five_elements_analysis',
                'bagua_mapping',
                'suggested_actions',
            ],
            'interfaces': [
                'analyze',
                'get_state',
                'get_stage',
                'get_paths',
                'get_suggestions',
                'analyze_with_cache',
            ],
        }


def main():
    """测试"""
    plugin = CognitivePlugin()
    
    # 测试问题
    test_problems = [
        "我想做一个小说项目，但没有用户",
        "如何优化我的 OpenClaw 技能系统",
    ]
    
    for problem in test_problems:
        print(f"\n{'='*60}")
        print(f"问题：{problem}")
        print(f"{'='*60}")
        
        result = plugin.analyze(problem)
        
        print(f"\n状态识别：{result['state_recognition']}")
        print(f"阶段判断：{result['stage_judgment']}")
        print(f"路径推演：{len(result['path_inference'])}条")
        print(f"建议动作：{len(result['suggested_actions'])}条")
    
    # 导出配置
    config = plugin.export_config()
    print(f"\n配置：{json.dumps(config, indent=2, ensure_ascii=False)}")


if __name__ == '__main__':
    main()
