import requests
import json

url = "http://localhost:5001/api/ai/generate"

data = {
    "knowledge_input": "傅立叶变换",
    "question_types": ["单选题"],
    "type_counts": {"单选题": 2},
    "difficulty_config": {},
    "distractor_list": [],
    "preference_list": [],
    "total_count": 2
}

print("发送请求到:", url)
print("请求数据:", json.dumps(data, ensure_ascii=False, indent=2))
print("\n等待响应...\n")

try:
    response = requests.post(url, json=data, timeout=120)
    print(f"状态码: {response.status_code}")
    
    try:
        result = response.json()
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    except:
        print(f"响应文本: {response.text}")
except requests.exceptions.Timeout:
    print("错误: 请求超时")
except requests.exceptions.ConnectionError:
    print("错误: 无法连接到服务器")
except Exception as e:
    print(f"错误: {e}")
