import httpx
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("KIMI_API_KEY", "")

if not api_key:
    print("请在 .env 文件中设置 KIMI_API_KEY")
    exit(1)

print("直接测试Kimi API...")

with httpx.Client(timeout=60.0, verify=False) as client:
    response = client.post(
        "https://api.moonshot.cn/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "moonshot-v1-8k",
            "messages": [
                {"role": "user", "content": "请生成一道关于傅立叶变换的单选题，返回JSON格式"}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"回复: {result['choices'][0]['message']['content']}")
    else:
        print(f"错误: {response.text}")
