import requests
import json
import time

print("测试1: 检查后端服务...")
try:
    r = requests.get("http://localhost:5001/", timeout=5)
    print(f"后端服务状态: {r.status_code}")
except Exception as e:
    print(f"后端服务错误: {e}")
    exit(1)

print("\n测试2: 检查知识库...")
try:
    r = requests.get("http://localhost:5001/api/knowledge/stats", timeout=5)
    print(f"知识库: {r.json()}")
except Exception as e:
    print(f"知识库错误: {e}")

print("\n测试3: 发送AI生成请求...")
data = {
    "knowledge_input": "傅立叶变换",
    "question_types": ["单选题"],
    "type_counts": {"单选题": 1},
    "difficulty_config": {},
    "distractor_list": [],
    "preference_list": [],
    "total_count": 1
}

print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")

start = time.time()
try:
    r = requests.post("http://localhost:5001/api/ai/generate", json=data, timeout=120)
    elapsed = time.time() - start
    print(f"\n响应时间: {elapsed:.1f}秒")
    print(f"状态码: {r.status_code}")
    print(f"响应: {json.dumps(r.json(), ensure_ascii=False, indent=2)}")
except requests.exceptions.Timeout:
    print("错误: 请求超时(120秒)")
except Exception as e:
    print(f"错误: {e}")
