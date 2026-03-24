"""
Smart Question MCP Server - Stdio模式启动
用于AI应用通过MCP协议连接
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio


async def main():
    """启动stdio服务器"""
    from src.smart_mcp.server import create_mcp_server, MCP_SDK_AVAILABLE

    if not MCP_SDK_AVAILABLE:
        print("MCP SDK not available")
        return

    mcp = create_mcp_server()

    print("Starting Smart Question MCP Server in stdio mode...")
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
