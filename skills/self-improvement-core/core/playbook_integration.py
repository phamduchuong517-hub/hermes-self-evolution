#!/usr/bin/env python3
"""
Playbook Extractor Integration for Self Improvement Core
用途：将 playbook_extractor 集成到自我进化流程中
创建时间：2026-04-17
"""

import sys
import os
import importlib.util

# 动态加载 playbook_extractor
spec = importlib.util.spec_from_file_location("playbook_extractor", "/root/.openclaw/workspace/skills/playbook-extractor.py")
playbook_extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(playbook_extractor)

PlaybookExtractor = playbook_extractor.PlaybookExtractor
Playbook = playbook_extractor.Playbook

class PlaybookIntegration:
    """Playbook 集成管理器"""
    
    def __init__(self):
        self.extractor = PlaybookExtractor()
        self.playbook_file = '/root/.openclaw/workspace/memory/playbooks_memory.md'
    
    def extract_from_dialogue(self, user_input: str, agent_response: str, context: dict = None):
        """从对话中提取剧本"""
        try:
            playbook = self.extractor.extract(user_input, agent_response, context)
            if playbook:
                self._save_playbook(playbook)
                return playbook
        except Exception as e:
            print(f"Error extracting playbook: {e}")
        return None
    
    def _save_playbook(self, playbook: Playbook):
        """保存剧本到记忆文件"""
        try:
            os.makedirs(os.path.dirname(self.playbook_file), exist_ok=True)
            
            with open(self.playbook_file, 'a', encoding='utf-8') as f:
                f.write(f"\n## {playbook.scenario}\n\n")
                f.write(f"**偏好**: {playbook.user_preference}\n\n")
                f.write(f"**策略**: {playbook.success_pattern}\n\n")
                f.write(f"**置信度**: {playbook.confidence:.2f}\n")
                f.write(f"**标签**: {', '.join(playbook.tags)}\n")
                f.write(f"**创建**: {playbook.created_at}\n")
                f.write("---\n")
            
            print(f"✓ Playbook saved: {playbook.scenario}")
        except Exception as e:
            print(f"Error saving playbook: {e}")
    
    def load_playbooks(self, scenario: str = None) -> list:
        """加载剧本"""
        playbooks = []
        if os.path.exists(self.playbook_file):
            with open(self.playbook_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 简单解析 Markdown 格式
                # 完整实现需要更复杂的解析逻辑
        return playbooks

if __name__ == "__main__":
    # 测试
    integration = PlaybookIntegration()
    print("Playbook Integration initialized")
    print(f"Playbook file: {integration.playbook_file}")
