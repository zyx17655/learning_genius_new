import requests
import json

data = {
    "knowledge_input": "傅立叶变换",
    "knowledge_ids": [],
    "question_types": ["单选", "判断", "多选"],
    "type_counts": {"单选": 1, "多选": 1, "判断": 1, "填空": 0, "主观": 0},
    "difficulty_config": {"L1": {"count": 1, "percent": 33}, "L2": {"count": 1, "percent": 33}, "L3": {"count": 1, "percent": 33}, "L4": {"count": 0, "percent": 0}, "L5": {"count": 0, "percent": 0}},
    "distractor_list": [],
    "preference_list": [],
    "custom_requirement": "",
    "total_count": 3
}

print("发送请求...")
print(f"数据: {json.dumps(data, ensure_ascii=False)}")

try:
    r = requests.post("http://localhost:5001/api/ai/generate", json=data, timeout=180)
    print(f"状态码: {r.status_code}")
    print(f"响应: {json.dumps(r.json(), ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"错误: {e}")
