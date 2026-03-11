import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings()

key = os.getenv("KIMI_API_KEY", "")
print(f"Testing API Key: {key[:20] if key else '未设置'}...")

if not key:
    print("请在 .env 文件中设置 KIMI_API_KEY")
    exit(1)

try:
    r = requests.post(
        "https://api.moonshot.cn/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": "kimi-k2-turbo-preview", "messages": [{"role": "user", "content": "test"}], "temperature": 1},
        timeout=30,
        verify=False
    )
    print(f"Status: {r.status_code}")
    print(r.text)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
