"""
Smart Question MCP Server - HTTP模式启动
专门用于启动HTTP服务
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio


async def main():
    """启动HTTP服务器"""
    from src.smart_mcp.server import create_mcp_server, MCP_SDK_AVAILABLE

    if not MCP_SDK_AVAILABLE:
        print("MCP SDK not available")
        return

    mcp = create_mcp_server()

    print("Starting Smart Question MCP Server in HTTP mode on 0.0.0.0:8765...")
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())
