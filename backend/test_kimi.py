import httpx
import json
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KIMI_API_KEY = os.getenv("KIMI_API_KEY", "")
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"

print("=== 测试Kimi API连接 ===")
print(f"API Key: {KIMI_API_KEY[:20] if KIMI_API_KEY else '未设置'}...")

if not KIMI_API_KEY:
    print("\n❌ 请在 .env 文件中设置 KIMI_API_KEY")
    exit(1)

try:
    with httpx.Client(timeout=30.0, verify=False) as client:
        response = client.post(
            KIMI_API_URL,
            headers={
                "Authorization": f"Bearer {KIMI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "moonshot-v1-8k",
                "messages": [
                    {
                        "role": "user",
                        "content": "请回复：测试成功"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 100
            }
        )
        
        print(f"\n状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ API Key 有效！")
            print(f"响应内容: {result['choices'][0]['message']['content']}")
        else:
            print(f"\n❌ API Key 无效！")
            print(f"错误内容: {response.text}")
            
except Exception as e:
    print(f"\n❌ 异常: {type(e).__name__}: {str(e)}")
