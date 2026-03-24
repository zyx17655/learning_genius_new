"""测试MCP Server API端点"""
import asyncio
import httpx
import json

BASE_URL = "http://localhost:8765"

async def test_endpoints():
    """测试各个API端点"""

    print("="*60)
    print("测试 MCP Server HTTP API")
    print("="*60)

    async with httpx.AsyncClient(timeout=30.0) as client:

        # 1. 服务信息
        print("\n1. GET / - 服务信息")
        response = await client.get(f"{BASE_URL}/")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)[:500]}...")

        # 2. 健康检查
        print("\n2. GET /health - 健康检查")
        response = await client.get(f"{BASE_URL}/health")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")

        # 3. 规则列表
        print("\n3. GET /rules - 规则列表")
        response = await client.get(f"{BASE_URL}/rules")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        # 4. 题目模板
        print("\n4. GET /templates - 题目模板")
        response = await client.get(f"{BASE_URL}/templates")
        print(f"   状态码: {response.status_code}")
        data = response.json()
        if data.get("success"):
            templates = data["data"]["templates"]
            print(f"   找到 {len(templates)} 个模板:")
            for t in templates:
                print(f"      - {t['type']}: {t['template'][:40]}...")

        # 5. 统计信息
        print("\n5. GET /stats - 统计信息")
        response = await client.get(f"{BASE_URL}/stats")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        # 6. 生成题目（这个需要API Key，这里只测试请求格式）
        print("\n6. POST /generate/questions - 生成题目")
        print("   (由于没有API Key，这个测试会失败，但可以看错误处理)")
        test_request = {
            "knowledge_input": "Python基础语法包括变量、数据类型、条件语句和循环语句",
            "question_types": ["单选", "判断"],
            "type_counts": {"单选": 2, "判断": 1},
            "difficulty": "简单"
        }
        try:
            response = await client.post(f"{BASE_URL}/generate/questions", json=test_request)
            print(f"   状态码: {response.status_code}")
            print(f"   响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)[:500]}...")
        except Exception as e:
            print(f"   错误: {e}")

    print("\n" + "="*60)
    print("API 测试完成!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_endpoints())
