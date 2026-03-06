import requests
import json
import time

print("测试AI生成流程...")
print("=" * 60)

start_time = time.time()
try:
    response = requests.post(
        "http://localhost:5001/api/ai/generate",
        json={
            "knowledge_input": "傅立叶变换",
            "question_types": ["单选题"],
            "type_counts": {"单选题": 1},
            "difficulty_config": {},
            "distractor_list": [],
            "preference_list": [],
            "total_count": 1
        },
        timeout=180
    )
    elapsed = time.time() - start_time
    print(f"响应时间: {elapsed:.2f}秒")
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
except requests.exceptions.Timeout:
    print("错误: 请求超时（180秒）")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
