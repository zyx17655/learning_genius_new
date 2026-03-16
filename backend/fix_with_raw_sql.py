"""
使用原生 SQL 来修复入库问题，绕过可能的 SQLAlchemy ORM 问题
"""
from sqlalchemy import text
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def migrate_old_questions():
    """将已入库的题目的缺失字段从 generated_questions 表补全"""
    print("=" * 80)
    print("尝试补全已入库题目的缺失字段")
    print("=" * 80)
    
    with engine.connect() as conn:
        # 查找有 generated_question_id 但字段为 NULL 的记录
        result = conn.execute(text("""
            SELECT q.id, q.generated_question_id 
            FROM questions q 
            WHERE q.source = 'AI生成' 
              AND q.generated_question_id IS NOT NULL
              AND (q.design_reason IS NULL OR q.difficulty_reason IS NULL OR q.distractor_reasons IS NULL)
        """))
        
        count = 0
        for row in result:
            q_id = row[0]
            gq_id = row[1]
            
            print(f"\n正在补全题目 ID: {q_id}, 关联的生成题目 ID: {gq_id}")
            
            # 从 generated_questions 表获取数据
            gq_result = conn.execute(text("""
                SELECT design_reason, difficulty_reason, distractor_reasons 
                FROM generated_questions 
                WHERE id = :gq_id
            """), {"gq_id": gq_id})
            
            gq_data = gq_result.fetchone()
            if gq_data:
                # 更新 questions 表
                conn.execute(text("""
                    UPDATE questions 
                    SET design_reason = :dr,
                        difficulty_reason = :dfr,
                        distractor_reasons = :dsr
                    WHERE id = :q_id
                """), {
                    "dr": gq_data[0],
                    "dfr": gq_data[1], 
                    "dsr": gq_data[2],
                    "q_id": q_id
                })
                conn.commit()
                print(f"✓ 成功补全题目 {q_id}")
                count += 1
        
        print(f"\n总共补全了 {count} 道题目")

def test_insert_with_raw_sql():
    """使用原生 SQL 测试插入一条记录"""
    print("\n" + "=" * 80)
    print("测试使用原生 SQL 插入")
    print("=" * 80)
    
    with engine.connect() as conn:
        # 获取最新的一条生成题目
        result = conn.execute(text("""
            SELECT id, content, question_type, difficulty, answer, explanation,
                   design_reason, difficulty_reason, distractor_reasons
            FROM generated_questions 
            ORDER BY id DESC 
            LIMIT 1
        """))
        
        gq = result.fetchone()
        if gq:
            print(f"\n使用生成题目 ID: {gq[0]}")
            print(f"设计原因长度: {len(gq[6]) if gq[6] else 0}")
            print(f"难度原因长度: {len(gq[7]) if gq[7] else 0}")
            print(f"干扰项长度: {len(gq[8]) if gq[8] else 0}")
            
            # 尝试插入
            result = conn.execute(text("""
                INSERT INTO questions (
                    content, question_type, difficulty, status, source,
                    answer, explanation, design_reason, difficulty_reason, 
                    distractor_reasons, generated_question_id, creator
                ) VALUES (
                    :content, :qt, :diff, '草稿', 'AI生成',
                    :answer, :exp, :dr, :dfr, :dsr, :gq_id, 'AI'
                )
            """), {
                "content": gq[1],
                "qt": gq[2],
                "diff": gq[3],
                "answer": gq[4],
                "exp": gq[5],
                "dr": gq[6],
                "dfr": gq[7],
                "dsr": gq[8],
                "gq_id": gq[0]
            })
            conn.commit()
            
            new_id = result.lastrowid
            print(f"\n✓ 使用原生 SQL 插入成功，新题目 ID: {new_id}")
            
            # 验证是否真的保存了
            verify = conn.execute(text("""
                SELECT design_reason, difficulty_reason, distractor_reasons, generated_question_id
                FROM questions 
                WHERE id = :q_id
            """), {"q_id": new_id})
            
            verify_data = verify.fetchone()
            if verify_data:
                print(f"\n验证结果:")
                print(f"  design_reason: {'✓ 有内容' if verify_data[0] else '✗ 空'}")
                print(f"  difficulty_reason: {'✓ 有内容' if verify_data[1] else '✗ 空'}")
                print(f"  distractor_reasons: {'✓ 有内容' if verify_data[2] else '✗ 空'}")
                print(f"  generated_question_id: {verify_data[3]}")

if __name__ == "__main__":
    migrate_old_questions()
    test_insert_with_raw_sql()
