"""
修复脚本：补全已入库题目的缺失字段
从 generated_questions 表获取数据并更新 questions 表
"""
from sqlalchemy import text
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def fix_existing_questions():
    """补全已入库题目的缺失字段"""
    print("=" * 80)
    print("补全已入库题目的缺失字段")
    print("=" * 80)
    
    with engine.connect() as conn:
        # 查询需要修复的题目
        print("\n1. 查询需要修复的题目...")
        result = conn.execute(text("""
            SELECT q.id, q.generated_question_id, gq.design_reason, 
                   gq.difficulty_reason, gq.distractor_reasons, gq.id as gq_id
            FROM questions q
            LEFT JOIN generated_questions gq ON q.generated_question_id = gq.id
            WHERE q.source = 'AI生成' 
              AND (q.design_reason IS NULL OR q.difficulty_reason IS NULL 
                   OR q.distractor_reasons IS NULL OR q.generated_question_id IS NULL)
        """))
        
        questions_to_fix = list(result)
        print(f"   找到 {len(questions_to_fix)} 条需要修复的题目")
        
        if not questions_to_fix:
            print("\n没有需要修复的题目！")
            return
        
        # 尝试通过内容匹配找到对应的 generated_question（如果 generated_question_id 为空）
        print("\n2. 尝试通过内容匹配找到对应的 generated_question...")
        fixed_count = 0
        
        for row in questions_to_fix:
            q_id, gq_id_from_q, design_reason, difficulty_reason, distractor_reasons, gq_id = row
            
            # 如果已经有 generated_question_id，直接更新
            if gq_id:
                # 更新题目
                conn.execute(text("""
                    UPDATE questions 
                    SET design_reason = :design_reason,
                        difficulty_reason = :difficulty_reason,
                        distractor_reasons = :distractor_reasons,
                        generated_question_id = :generated_question_id
                    WHERE id = :question_id
                """), {
                    "design_reason": design_reason,
                    "difficulty_reason": difficulty_reason,
                    "distractor_reasons": distractor_reasons,
                    "generated_question_id": gq_id,
                    "question_id": q_id
                })
                fixed_count += 1
                print(f"   已修复题目 ID: {q_id} (关联 generated_question ID: {gq_id})")
            else:
                # 尝试通过内容匹配
                q_content_result = conn.execute(text("""
                    SELECT content FROM questions WHERE id = :q_id
                """), {"q_id": q_id})
                q_content_row = q_content_result.fetchone()
                if q_content_row:
                    q_content = q_content_row[0]
                    # 查找内容匹配的 generated_question
                    gq_result = conn.execute(text("""
                        SELECT id, design_reason, difficulty_reason, distractor_reasons
                        FROM generated_questions
                        WHERE content = :content
                        ORDER BY id DESC
                        LIMIT 1
                    """), {"content": q_content})
                    gq_row = gq_result.fetchone()
                    if gq_row:
                        gq_id_found, dr_found, diffr_found, distr_found = gq_row
                        # 更新题目
                        conn.execute(text("""
                            UPDATE questions 
                            SET design_reason = :design_reason,
                                difficulty_reason = :difficulty_reason,
                                distractor_reasons = :distractor_reasons,
                                generated_question_id = :generated_question_id
                            WHERE id = :question_id
                        """), {
                            "design_reason": dr_found,
                            "difficulty_reason": diffr_found,
                            "distractor_reasons": distr_found,
                            "generated_question_id": gq_id_found,
                            "question_id": q_id
                        })
                        fixed_count += 1
                        print(f"   已修复题目 ID: {q_id} (通过内容匹配，关联 generated_question ID: {gq_id_found})")
                    else:
                        print(f"   无法找到题目 ID: {q_id} 的匹配 generated_question")
        
        conn.commit()
        
        # 验证修复结果
        print(f"\n3. 修复完成，共修复 {fixed_count} 条题目")
        print("\n4. 验证修复结果...")
        result = conn.execute(text("""
            SELECT id, design_reason, difficulty_reason, distractor_reasons, generated_question_id
            FROM questions 
            WHERE source = 'AI生成'
            ORDER BY id DESC 
            LIMIT 5
        """))
        
        for row in result:
            print(f"\n  题目 ID: {row[0]}")
            print(f"  design_reason: {'有值' if row[1] else 'NULL'}")
            print(f"  difficulty_reason: {'有值' if row[2] else 'NULL'}")
            print(f"  distractor_reasons: {'有值' if row[3] else 'NULL'}")
            print(f"  generated_question_id: {row[4]}")

if __name__ == "__main__":
    fix_existing_questions()
