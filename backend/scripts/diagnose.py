import requests
import json
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("诊断测试开始")
print("=" * 60)

# 测试4: 直接测试Kimi API
print("\n[测试4] 直接测试Kimi API...")
try:
    from app.config import settings
    import httpx
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    api_key = settings.KIMI_API_KEY
    print(f"API Key (前20位): {api_key[:20]}...")
    
    with httpx.Client(timeout=30.0, verify=False) as client:
        response = client.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "moonshot-v1-8k",
                "messages": [
                    {"role": "user", "content": "你好，请回复'测试成功'"}
                ],
                "temperature": 0.7,
                "max_tokens": 100
            }
        )
        print(f"Kimi API状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Kimi回复: {result['choices'][0]['message']['content']}")
        else:
            print(f"Kimi API错误: {response.text}")
except Exception as e:
    print(f"Kimi API测试错误: {e}")
    import traceback
    traceback.print_exc()

# 测试5: 完整的AI生成流程
print("\n[测试5] 完整AI生成流程...")
try:
    start_time = time.time()
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
        timeout=120
    )
    elapsed = time.time() - start_time
    print(f"响应时间: {elapsed:.2f}秒")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"AI生成错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("诊断测试完成")
print("=" * 60)
