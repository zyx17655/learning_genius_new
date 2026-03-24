"""
Smart MCP模块
包含MCP协议处理、工具定义、资源定义等
"""

from .server import create_mcp_server, MCP_SDK_AVAILABLE

__all__ = ["create_mcp_server", "MCP_SDK_AVAILABLE"]
