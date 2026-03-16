import requests
import json

# 测试 API
url = "http://localhost:5001/api/questions"
params = {
    "page": 1,
    "per_page": 10
}

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    data = response.json()
    print(f"Total questions: {data.get('total', 0)}")
    print(f"Questions count: {len(data.get('questions', []))}")
    if data.get('questions'):
        print(f"First question: {data['questions'][0]['content'][:50]}...")
except Exception as e:
    print(f"Error: {e}")
