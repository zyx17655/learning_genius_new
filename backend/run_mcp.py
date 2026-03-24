"""
MCP Server 启动脚本

使用方法:
    python run_mcp.py

默认端口: 8765
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from mcp_server.server import app

    print("=" * 60)
    print("智能题库 MCP 服务")
    print("=" * 60)
    print("服务地址: http://localhost:8765")
    print("API文档: http://localhost:8765/docs")
    print("健康检查: http://localhost:8765/health")
    print("=" * 60)
    print()
    print("启动中...")

    uvicorn.run(app, host="0.0.0.0", port=8765)
