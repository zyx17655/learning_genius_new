import requests
import json

# MCP服务地址
MCP_URL = "http://localhost:8765/mcp/generate_questions"

# 测试数据
test_data = {
    "knowledge_input": "Python基础语法：变量、数据类型、运算符、条件语句、循环语句。",
    "question_types": ["单选", "判断"],
    "type_counts": {"单选": 2, "判断": 2},
    "difficulty_config": {
        "简单": {"count": 2, "percent": 50},
        "中等": {"count": 2, "percent": 50}
    }
}

print("=" * 60)
print("MCP服务测试")
print("=" * 60)
print(f"请求地址: {MCP_URL}")
print(f"请求参数:\n{json.dumps(test_data, ensure_ascii=False, indent=2)}")
print("=" * 60)
print("正在调用MCP服务...")
print()

try:
    response = requests.post(
        MCP_URL,
        json=test_data,  # 使用json参数，会自动设置Content-Type为application/json
        headers={"Content-Type": "application/json"},
        timeout=120
    )
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"响应结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"错误响应: {response.text}")
        
except Exception as e:
    print(f"请求失败: {e}")
