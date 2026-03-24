"""直接测试MCP Server核心功能"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_core_functions():
    """直接测试核心功能"""

    print("="*60)
    print("直接测试 MCP Server 核心功能")
    print("="*60)

    # 1. 测试工具定义
    print("\n1. 测试工具定义...")
    from src.mcp.tools import get_tool_definitions
    tools = get_tool_definitions()
    print(f"   ✓ 找到 {len(tools)} 个工具")
    for tool in tools:
        print(f"      - {tool['name']}")

    # 2. 测试适配器注册
    print("\n2. 测试适配器注册...")
    from src.adapters.kimi_adapter import KimiAdapter
    from src.adapters.openai_adapter import OpenAIAdapter
    from src.adapters import list_adapters
    adapters = list_adapters()
    print(f"   ✓ 已注册的适配器: {adapters}")

    # 3. 测试获取适配器
    print("\n3. 测试获取适配器...")
    from src.adapters import get_adapter
    try:
        adapter = get_adapter("kimi", {
            "api_key": "test",
            "model_name": "kimi-k2-turbo-preview",
            "base_url": "https://api.moonshot.cn/v1"
        })
        print(f"   ✓ 成功获取 Kimi 适配器: {type(adapter).__name__}")
    except Exception as e:
        print(f"   ✗ 获取适配器失败: {e}")

    # 4. 测试规则服务
    print("\n4. 测试规则服务...")
    from src.services.rule_service import RuleService
    rule_service = RuleService()
    rules = await rule_service.list_rules()
    print(f"   ✓ 获取到 {len(rules)} 条规则")
    for rule in rules:
        print(f"      - {rule['name']} (默认: {rule['is_default']})")

    # 5. 测试模板服务
    print("\n5. 测试模板服务...")
    from src.services.question_gen import QuestionGenService
    gen_service = QuestionGenService()
    templates = await gen_service.get_templates()
    print(f"   ✓ 获取到 {len(templates)} 个模板")
    for t in templates:
        print(f"      - {t['type']}: {t['template'][:40]}...")

    # 6. 测试出题服务（不实际调用API）
    print("\n6. 测试出题服务（构建Prompt）...")
    prompt = gen_service._build_prompt(
        knowledge_input="Python基础语法包括变量、数据类型、条件语句和循环语句",
        question_types=["单选", "判断"],
        type_counts={"单选": 2, "判断": 1},
        difficulty="简单"
    )
    print(f"   ✓ Prompt构建成功，长度: {len(prompt)} 字符")
    print(f"   前200字符预览:\n   {prompt[:200]}...")

    # 7. 测试验证服务
    print("\n7. 测试验证服务...")
    from src.services.question_verify import VerifyService
    verify_service = VerifyService()
    verify_prompt = verify_service._build_verification_prompt(
        question_content="下列关于Python变量的说法，正确的是？",
        question_type="单选",
        answer="C",
        options=[
            {"content": "变量必须先声明后使用", "is_correct": False},
            {"content": "变量可以随时改变类型", "is_correct": False},
            {"content": "变量名区分大小写", "is_correct": True},
            {"content": "变量不需要指定类型", "is_correct": False}
        ],
        knowledge_context="Python变量相关知识点"
    )
    print(f"   ✓ 验证Prompt构建成功，长度: {len(verify_prompt)} 字符")

    print("\n" + "="*60)
    print("核心功能测试完成!")
    print("="*60)
    print("\n注意: 由于没有配置 KIMI_API_KEY，实际API调用会失败。")
    print("配置 API Key 后，即可正常使用。")

if __name__ == "__main__":
    asyncio.run(test_core_functions())
