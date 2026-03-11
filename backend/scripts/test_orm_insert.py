"""
测试 AI 生成并捕获完整错误
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from app.database import SessionLocal
from app.models import GeneratedQuestion, GenerationTask

def test_insert():
    db = SessionLocal()
    
    try:
        # 创建测试任务
        task = GenerationTask(
            knowledge_input="测试知识点",
            question_types="单选",
            status="completed"
        )
        db.add(task)
        db.flush()
        print(f"创建任务: id={task.id}")
        
        # 模拟 AI 返回的题目数据
        test_question = {
            "content": "测试题目内容 $C(s,\\tau)$",
            "question_type": "单选",
            "difficulty": "简单",
            "answer": "A",
            "explanation": "测试解析",
            "design_reason": "测试设计理由",
            "difficulty_reason": "测试难度理由",
            "distractor_reasons": json.dumps([]),
            "knowledge_points": "测试知识点",
            "options_json": json.dumps([
                {"content": "选项A", "is_correct": True},
                {"content": "选项B", "is_correct": False}
            ])
        }
        
        # 创建 GeneratedQuestion 对象
        gq = GeneratedQuestion(
            task_id=task.id,
            content=test_question["content"],
            question_type=test_question["question_type"],
            difficulty=test_question["difficulty"],
            answer=test_question["answer"],
            explanation=test_question["explanation"],
            design_reason=test_question["design_reason"],
            difficulty_reason=test_question["difficulty_reason"],
            distractor_reasons=test_question["distractor_reasons"],
            knowledge_points=test_question["knowledge_points"],
            options_json=test_question["options_json"]
        )
        
        print(f"\nGeneratedQuestion 对象属性:")
        for col in GeneratedQuestion.__table__.columns:
            attr = getattr(gq, col.name, "N/A")
            print(f"  {col.name}: {repr(attr)[:100]}")
        
        db.add(gq)
        print("\n尝试提交...")
        db.commit()
        print("成功！")
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_insert()
