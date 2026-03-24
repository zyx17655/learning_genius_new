"""
Smart Question MCP Server启动脚本
支持stdio和HTTP两种模式
"""

import sys
import os
import asyncio

# 添加src目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.smart_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())
