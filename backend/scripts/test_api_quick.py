import requests
import json

print("测试API...")

# 测试1: 简单GET请求
print("\n[1] 测试GET请求...")
try:
    r = requests.get("http://localhost:5001/", timeout=5)
    print(f"状态码: {r.status_code}")
    print(f"响应: {r.json()}")
except Exception as e:
    print(f"错误: {e}")

# 测试2: 知识库API
print("\n[2] 测试知识库API...")
try:
    r = requests.get("http://localhost:5001/api/knowledge/stats", timeout=5)
    print(f"状态码: {r.status_code}")
    print(f"响应: {json.dumps(r.json(), ensure_ascii=False)[:200]}...")
except Exception as e:
    print(f"错误: {e}")

# 测试3: AI生成API (短超时)
print("\n[3] 测试AI生成API (10秒超时)...")
try:
    r = requests.post(
        "http://localhost:5001/api/ai/generate",
        json={"knowledge_input": "test", "question_types": ["单选"], "type_counts": {"单选": 1}, "total_count": 1},
        timeout=10
    )
    print(f"状态码: {r.status_code}")
    print(f"响应: {r.text[:500]}")
except requests.exceptions.Timeout:
    print("错误: 请求超时(10秒)")
except Exception as e:
    print(f"错误: {e}")

print("\n测试完成")
