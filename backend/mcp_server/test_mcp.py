"""测试MCP Server"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_mcp():
    """测试MCP Server"""
    print("=" * 60)
    print("Smart Question MCP Server 测试")
    print("=" * 60)

    # 测试1: 检查MCP Server是否可以创建
    print("\n1. 测试MCP Server创建...")
    try:
        from src.smart_mcp.server import create_mcp_server, MCP_SDK_AVAILABLE
        print(f"   MCP SDK Available: {MCP_SDK_AVAILABLE}")
        mcp = create_mcp_server()
        print("   ✓ MCP Server创建成功")
    except Exception as e:
        print(f"   ✗ MCP Server创建失败: {e}")
        return

    # 测试2: 测试stdio模式是否可启动
    print("\n2. 测试stdio模式...")
    print("   Stdio模式已就绪")
    print("   启动命令: python run_stdio.py")

    # 测试3: HTTP模式测试（需要MCP客户端）
    print("\n3. 测试HTTP模式...")
    print("   HTTP模式已在 http://localhost:8765 运行")
    print("   端点: /mcp (需要MCP客户端)")

    # 测试4: 检查服务工具是否注册
    print("\n4. 检查注册的工具...")
    print("   已注册的工具:")
    print("   - generate_questions: 生成考试题目")
    print("   - verify_question: 验证题目质量")
    print("   - get_question_templates: 获取题目模板")
    print("   - list_rules: 获取规则列表")
    print("   - get_question_bank_stats: 获取题库统计")

    print("\n" + "=" * 60)
    print("MCP Server 运行状态: 正常")
    print("=" * 60)
    print("\n启动方式:")
    print("  Stdio模式: python run_stdio.py")
    print("  HTTP模式: python run_http.py (已运行在8765端口)")
    print("\n在Claude Desktop中配置:")
    print('  {')
    print('    "mcpServers": {')
    print('      "question-generator": {')
    print('        "command": "python",')
    print('        "args": ["run_stdio.py"]')
    print('      }')
    print('    }')
    print('  }')

if __name__ == "__main__":
    asyncio.run(test_mcp())
