import requests
import json
import time

print("测试API...")

data = {
    "knowledge_input": "傅立叶变换",
    "question_types": ["单选题"],
    "type_counts": {"单选题": 1},
    "difficulty_config": {},
    "distractor_list": [],
    "preference_list": [],
    "total_count": 1
}

try:
    start = time.time()
    r = requests.post("http://localhost:5001/api/ai/generate", json=data, timeout=120)
    elapsed = time.time() - start
    print(f"状态码: {r.status_code}")
    print(f"响应时间: {elapsed:.1f}秒")
    print(f"结果: {json.dumps(r.json(), ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"错误: {e}")
