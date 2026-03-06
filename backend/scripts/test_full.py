import requests
import json
import time

print("=" * 60)
print("完整测试：傅立叶变换 - 2道单选，1道填空，1道多选")
print("=" * 60)

data = {
    "knowledge_input": "傅立叶变换",
    "question_types": ["单选题", "填空题", "多选题"],
    "type_counts": {"单选题": 2, "填空题": 1, "多选题": 1},
    "difficulty_config": {},
    "distractor_list": [],
    "preference_list": [],
    "total_count": 4
}

print(f"\n请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
print("\n发送请求中，请等待...\n")

start_time = time.time()
try:
    response = requests.post(
        "http://localhost:5001/api/ai/generate",
        json=data,
        timeout=180
    )
    elapsed = time.time() - start_time
    print(f"响应时间: {elapsed:.2f}秒")
    print(f"状态码: {response.status_code}")
    
    result = response.json()
    print(f"\n响应结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get("code") == 0:
        print("\n✅ 测试成功！")
        task_id = result.get("data", {}).get("task_id")
        if task_id:
            print(f"\n获取生成的题目...")
            questions_response = requests.get(f"http://localhost:5001/api/ai/tasks/{task_id}/questions")
            questions = questions_response.json()
            print(f"生成的题目: {json.dumps(questions, ensure_ascii=False, indent=2)[:2000]}...")
    else:
        print(f"\n❌ 测试失败: {result.get('message')}")
        
except requests.exceptions.Timeout:
    print("❌ 错误: 请求超时（180秒）")
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
