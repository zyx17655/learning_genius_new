"""
测试脚本：直接测试入库逻辑
"""
from sqlalchemy import text
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import GeneratedQuestion

def test_adopt():
    """测试入库"""
    print("=" * 80)
    print("测试入库逻辑")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 获取一条最新的 generated_question
        print("\n1. 获取最新的 generated_question...")
        gq = db.query(GeneratedQuestion).order_by(GeneratedQuestion.id.desc()).first()
        
        if not gq:
            print("   没有找到 generated_question！")
            return
        
        print(f"   找到 generated_question ID: {gq.id}")
        print(f"   design_reason: {gq.design_reason[:50] if gq.design_reason else 'None'}...")
        print(f"   difficulty_reason: {gq.difficulty_reason[:50] if gq.difficulty_reason else 'None'}...")
        print(f"   distractor_reasons: {gq.distractor_reasons[:100] if gq.distractor_reasons else 'None'}...")
        
        # 使用原生 SQL 插入
        print("\n2. 开始插入到 questions 表...")
        
        with engine.connect() as conn:
            # 开启事务
            trans = conn.begin()
            
            try:
                result = conn.execute(text("""
                    INSERT INTO questions (
                        content, question_type, difficulty, status, source,
                        answer, explanation, design_reason, difficulty_reason,
                        distractor_reasons, generated_question_id, creator,
                        created_at, updated_at
                    ) VALUES (
                        :content, :question_type, :difficulty, :status, :source,
                        :answer, :explanation, :design_reason, :difficulty_reason,
                        :distractor_reasons, :generated_question_id, :creator,
                        NOW(), NOW()
                    )
                """), {
                    "content": gq.content,
                    "question_type": gq.question_type,
                    "difficulty": gq.difficulty,
                    "status": "草稿" if gq.is_draft else "已审核",
                    "source": "AI生成",
                    "answer": gq.answer,
                    "explanation": gq.explanation,
                    "design_reason": gq.design_reason,
                    "difficulty_reason": gq.difficulty_reason,
                    "distractor_reasons": gq.distractor_reasons,
                    "generated_question_id": gq.id,
                    "creator": "AI"
                })
                
                q_id = result.lastrowid
                print(f"   插入成功！新题目 ID: {q_id}")
                
                # 插入选项
                if gq.options_json:
                    options = json.loads(gq.options_json)
                    print(f"   正在插入 {len(options)} 个选项...")
                    for idx, opt in enumerate(options):
                        conn.execute(text("""
                            INSERT INTO options (question_id, content, is_correct, order_index)
                            VALUES (:question_id, :content, :is_correct, :order_index)
                        """), {
                            "question_id": q_id,
                            "content": opt.get("content", ""),
                            "is_correct": opt.get("is_correct", False),
                            "order_index": idx
                        })
                
                # 提交事务
                trans.commit()
                print("   事务提交成功！")
                
                # 验证插入结果
                print("\n3. 验证插入结果...")
                verify_result = conn.execute(text("""
                    SELECT id, design_reason, difficulty_reason, distractor_reasons, generated_question_id
                    FROM questions WHERE id = :q_id
                """), {"q_id": q_id})
                
                verify_row = verify_result.fetchone()
                if verify_row:
                    print(f"   题目 ID: {verify_row[0]}")
                    print(f"   design_reason: {'有值' if verify_row[1] else 'NULL'}")
                    print(f"   difficulty_reason: {'有值' if verify_row[2] else 'NULL'}")
                    print(f"   distractor_reasons: {'有值' if verify_row[3] else 'NULL'}")
                    print(f"   generated_question_id: {verify_row[4]}")
                
            except Exception as e:
                trans.rollback()
                print(f"   错误: {e}")
                import traceback
                traceback.print_exc()
    
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_adopt()
