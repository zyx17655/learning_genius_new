"""
完整模拟 AI 生成过程
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from app.database import SessionLocal, engine
from app.models import GeneratedQuestion, GenerationTask, QuestionRule
from sqlalchemy import text

def check_db_structure():
    """检查数据库表结构"""
    with engine.connect() as conn:
        print("=== generation_tasks 表结构 ===")
        result = conn.execute(text("DESCRIBE generation_tasks"))
        for row in result:
            print(f"  {row[0]}: {row[1]}")
        
        print("\n=== generated_questions 表结构 ===")
        result = conn.execute(text("DESCRIBE generated_questions"))
        for row in result:
            print(f"  {row[0]}: {row[1]}")

def test_full_flow():
    """完整测试 AI 生成流程"""
    db = SessionLocal()
    
    try:
        # 检查数据库表结构
        check_db_structure()
        
        # 创建测试任务
        print("\n=== 创建测试任务 ===")
        task = GenerationTask(
            knowledge_input="测试知识点",
            question_types="单选",
            status="running"
        )
        db.add(task)
        db.flush()
        print(f"任务 ID: {task.id}")
        
        # 模拟 AI 返回的题目数据
        test_questions = [
            {
                "content": "测试题目1 $C(s,\\tau)$",
                "question_type": "单选",
                "difficulty": "简单",
                "answer": "A",
                "explanation": "测试解析1",
                "design_reason": "测试设计理由1",
                "difficulty_reason": "测试难度理由1",
                "distractor_reasons": [],
                "knowledge_points": ["知识点1", "知识点2"],
                "options": [
                    {"content": "选项A", "is_correct": True},
                    {"content": "选项B", "is_correct": False}
                ]
            },
            {
                "content": "测试题目2",
                "question_type": "单选",
                "difficulty": "中等",
                "answer": "B",
                "explanation": "测试解析2",
                "design_reason": "测试设计理由2",
                "difficulty_reason": "测试难度理由2",
                "distractor_reasons": [],
                "knowledge_points": ["知识点3"],
                "options": [
                    {"content": "选项A", "is_correct": False},
                    {"content": "选项B", "is_correct": True}
                ]
            }
        ]
        
        print("\n=== 插入题目 ===")
        for i, q in enumerate(test_questions):
            kp = q.get("knowledge_points", [])
            if isinstance(kp, list):
                kp_str = ",".join(str(k) for k in kp if k is not None)
            else:
                kp_str = str(kp) if kp else ""
            
            gq = GeneratedQuestion(
                task_id=task.id,
                content=q.get("content", ""),
                question_type=q.get("question_type", "单选"),
                difficulty=q.get("difficulty", "中等"),
                answer=q.get("answer", ""),
                explanation=q.get("explanation", ""),
                design_reason=q.get("design_reason", ""),
                difficulty_reason=q.get("difficulty_reason", ""),
                distractor_reasons=json.dumps(q.get("distractor_reasons", [])),
                knowledge_points=kp_str,
                options_json=json.dumps(q.get("options", [])),
                is_selected=False,
                is_draft=False,
                is_discarded=False
            )
            db.add(gq)
            print(f"  题目 {i+1} 已添加")
        
        print("\n=== 提交事务 ===")
        task.status = "completed"
        task.result = json.dumps({"count": len(test_questions)})
        db.commit()
        print("成功！")
        
        # 验证数据
        print("\n=== 验证数据 ===")
        questions = db.query(GeneratedQuestion).filter(GeneratedQuestion.task_id == task.id).all()
        print(f"查询到 {len(questions)} 道题目")
        for q in questions:
            print(f"  - {q.content[:30]}...")
        
        # 清理测试数据
        print("\n=== 清理测试数据 ===")
        db.query(GeneratedQuestion).filter(GeneratedQuestion.task_id == task.id).delete()
        db.query(GenerationTask).filter(GenerationTask.id == task.id).delete()
        db.commit()
        print("测试数据已清理")
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_full_flow()
