import requests
import json
import time

print("发送AI生成请求...")

data = {
    "knowledge_input": "傅立叶变换",
    "question_types": ["单选题"],
    "type_counts": {"单选题": 1},
    "difficulty_config": {},
    "distractor_list": [],
    "preference_list": [],
    "total_count": 1
}

start = time.time()
try:
    r = requests.post("http://localhost:5001/api/ai/generate", json=data, timeout=180)
    elapsed = time.time() - start
    print(f"响应时间: {elapsed:.1f}秒")
    print(f"状态码: {r.status_code}")
    result = r.json()
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result.get("code") == 0:
        task_id = result.get("data", {}).get("task_id")
        if task_id:
            print(f"\n获取题目 (task_id={task_id})...")
            qr = requests.get(f"http://localhost:5001/api/ai/tasks/{task_id}/questions")
            print(f"题目: {json.dumps(qr.json(), ensure_ascii=False, indent=2)[:1000]}...")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
