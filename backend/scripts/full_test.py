import requests
import json
import time
import sys

print("=" * 60)
print("AI生成测试")
print("=" * 60)

# 测试1: 检查后端服务
print("\n[1] 检查后端服务...")
try:
    r = requests.get("http://localhost:5001/", timeout=5)
    print(f"    后端服务: OK (状态码: {r.status_code})")
except Exception as e:
    print(f"    后端服务: 失败 - {e}")
    sys.exit(1)

# 测试2: 检查知识库
print("\n[2] 检查知识库...")
try:
    r = requests.get("http://localhost:5001/api/knowledge/stats", timeout=5)
    data = r.json()
    print(f"    知识库: OK (文档: {data['data']['document_count']}, 片段: {data['data']['chunk_count']})")
except Exception as e:
    print(f"    知识库: 失败 - {e}")

# 测试3: AI生成
print("\n[3] 测试AI生成...")
print("    发送请求... (这可能需要30-60秒)")

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
    print(f"    响应时间: {elapsed:.1f}秒")
    print(f"    状态码: {r.status_code}")
    
    result = r.json()
    if result.get("code") == 0:
        print(f"    结果: 成功!")
        print(f"    任务ID: {result['data']['task_id']}")
        print(f"    题目数量: {result['data']['count']}")
        
        # 获取题目详情
        task_id = result['data']['task_id']
        qr = requests.get(f"http://localhost:5001/api/ai/tasks/{task_id}/questions", timeout=10)
        questions = qr.json()
        if questions.get('data'):
            for i, q in enumerate(questions['data'][:2], 1):
                print(f"\n    题目{i}: {q['content'][:100]}...")
    else:
        print(f"    结果: 失败 - {result.get('message')}")
        
except requests.exceptions.Timeout:
    print("    错误: 请求超时(180秒)")
except Exception as e:
    print(f"    错误: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
