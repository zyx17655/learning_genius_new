"""测试MCP Server API"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import httpx
import json

async def test_api():
    """测试API"""

    # 首先检查依赖是否安装
    print("1. 检查MCP Server导入...")
    try:
        from src.mcp.server import QuestionMCPServer
        print("   ✓ QuestionMCPServer 导入成功")
    except ImportError as e:
        print(f"   ✗ 导入失败: {e}")
        return

    print("\n2. 检查适配器导入...")
    try:
        from src.adapters import get_adapter
        print("   ✓ 适配器模块导入成功")
    except ImportError as e:
        print(f"   ✗ 导入失败: {e}")
        return

    print("\n3. 检查服务导入...")
    try:
        from src.services.question_gen import QuestionGenService
        from src.services.question_verify import VerifyService
        from src.services.rule_service import RuleService
        print("   ✓ 服务模块导入成功")
    except ImportError as e:
        print(f"   ✗ 导入失败: {e}")
        return

    print("\n4. 测试工具定义...")
    try:
        from src.mcp.tools import get_tool_definitions
        tools = get_tool_definitions()
        print(f"   ✓ 找到 {len(tools)} 个工具定义:")
        for tool in tools:
            print(f"      - {tool['name']}: {tool['description'][:50]}...")
    except ImportError as e:
        print(f"   ✗ 导入失败: {e}")
        return

    print("\n5. 测试服务器配置...")
    try:
        from src.config.settings import settings
        print(f"   ✓ 服务名称: {settings.SERVER_NAME}")
        print(f"   ✓ 服务版本: {settings.SERVER_VERSION}")
        print(f"   ✓ 默认模型: {settings.DEFAULT_MODEL}")
    except ImportError as e:
        print(f"   ✗ 导入失败: {e}")
        return

    print("\n6. 尝试连接测试服务器 (http://localhost:8765)...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8765/health")
            if response.status_code == 200:
                print(f"   ✓ 服务器响应: {response.json()}")
            else:
                print(f"   ⚠ 服务器返回状态码: {response.status_code}")
    except httpx.ConnectError:
        print("   ⚠ 服务器未运行 (这是正常的，服务还没启动)")
        print("   要启动服务器，请运行: python run_http.py")
    except Exception as e:
        print(f"   ⚠ 连接错误: {e}")

    print("\n" + "="*60)
    print("MCP Server 基础检查完成!")
    print("="*60)
    print("\n启动服务器的命令:")
    print("  HTTP模式: python run_http.py")
    print("  Stdio模式: python run_stdio.py")
    print("  双模式: python run.py --mode dual")

if __name__ == "__main__":
    asyncio.run(test_api())
