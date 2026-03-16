"""
检查内容匹配问题
"""
from sqlalchemy import text
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def check_content():
    """检查内容"""
    print("=" * 80)
    print("检查内容")
    print("=" * 80)
    
    with engine.connect() as conn:
        # 获取最新的一条 question
        print("\n1. 最新的一条 question:")
        q_result = conn.execute(text("""
            SELECT id, content
            FROM questions
            WHERE source = 'AI生成'
            ORDER BY id DESC
            LIMIT 1
        """))
        q_row = q_result.fetchone()
        if q_row:
            q_id, q_content = q_row
            print(f"   题目 ID: {q_id}")
            print(f"   内容: {q_content}")
            
            # 获取最新的几条 generated_questions
            print("\n2. 最新的 3 条 generated_questions:")
            gq_result = conn.execute(text("""
                SELECT id, content
                FROM generated_questions
                ORDER BY id DESC
                LIMIT 3
            """))
            for gq_row in gq_result:
                gq_id, gq_content = gq_row
                print(f"\n   generated_question ID: {gq_id}")
                print(f"   内容: {gq_content}")
                
                # 比较前50个字符
                if q_content and gq_content:
                    print(f"\n   比较前50个字符:")
                    print(f"   question:        '{q_content[:50]}'")
                    print(f"   generated_question: '{gq_content[:50]}'")
                    print(f"   是否匹配: {q_content[:50] == gq_content[:50]}")

if __name__ == "__main__":
    check_content()
