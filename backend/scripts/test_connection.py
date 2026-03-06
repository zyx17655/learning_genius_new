import requests
import json
import time

print("测试API连接...")

# 测试1: 简单GET请求
print("\n[1] 测试GET请求...")
try:
    r = requests.get("http://localhost:5001/", timeout=5)
    print(f"    状态码: {r.status_code}")
    print(f"    响应: {r.json()}")
except Exception as e:
    print(f"    错误: {e}")

# 测试2: 简单POST请求
print("\n[2] 测试POST请求...")
try:
    r = requests.post(
        "http://localhost:5001/api/ai/generate",
        json={"knowledge_input": "test", "question_types": ["单选"], "type_counts": {"单选": 1}, "total_count": 1},
        timeout=10
    )
    print(f"    状态码: {r.status_code}")
    print(f"    响应: {r.text[:500]}")
except requests.exceptions.Timeout:
    print("    错误: 请求超时(10秒)")
except Exception as e:
    print(f"    错误: {e}")

print("\n测试完成")
