import requests
import json

# 测试健康检查
print("=" * 60)
print("1. 测试健康检查")
print("=" * 60)
try:
    response = requests.get("http://localhost:8765/health", timeout=5)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
except Exception as e:
    print(f"错误: {e}")

# 测试生成题目
print("\n" + "=" * 60)
print("2. 测试生成题目")
print("=" * 60)

test_data = {
    "knowledge_input": "Python基础语法：1.变量：变量是存储数据的容器，Python中的变量不需要声明类型，使用前必须赋值。2.数据类型：Python支持多种数据类型，包括整数(int)、浮点数(float)、字符串(str)、布尔值(bool)等。",
    "question_types": ["单选", "判断"],
    "type_counts": {"单选": 1, "判断": 1},
    "difficulty_config": {
        "简单": {"count": 1, "percent": 50},
        "中等": {"count": 1, "percent": 50}
    }
}

try:
    response = requests.post(
        "http://localhost:8765/mcp/generate_questions",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=60
    )
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"错误: {e}")
