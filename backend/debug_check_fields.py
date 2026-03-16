"""
调试脚本：检查 generated_questions 表和 questions 表中的字段
"""
from sqlalchemy import text
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def check_generated_questions():
    """检查 generated_questions 表中的数据"""
    print("=" * 80)
    print("检查 generated_questions 表")
    print("=" * 80)
    
    with engine.connect() as conn:
        # 检查表结构
        print("\n1. 表结构:")
        result = conn.execute(text("DESCRIBE generated_questions"))
        for row in result:
            print(f"  - {row[0]}: {row[1]}")
        
        # 查询最新的5条记录
        print("\n2. 最新的5条记录:")
        result = conn.execute(text("""
            SELECT id, task_id, content, design_reason, difficulty_reason, 
                   distractor_reasons, created_at
            FROM generated_questions 
            ORDER BY id DESC 
            LIMIT 5
        """))
        
        for row in result:
            print(f"\n  记录 ID: {row[0]}")
            print(f"  任务 ID: {row[1]}")
            print(f"  内容: {row[2][:50] if row[2] else 'None'}...")
            print(f"  design_reason: {row[3][:50] if row[3] else 'None'}...")
            print(f"  difficulty_reason: {row[4][:50] if row[4] else 'None'}...")
            print(f"  distractor_reasons: {row[5][:100] if row[5] else 'None'}...")
            print(f"  创建时间: {row[6]}")

def check_questions():
    """检查 questions 表中的数据"""
    print("\n" + "=" * 80)
    print("检查 questions 表")
    print("=" * 80)
    
    with engine.connect() as conn:
        # 检查表结构
        print("\n1. 表结构:")
        result = conn.execute(text("DESCRIBE questions"))
        for row in result:
            print(f"  - {row[0]}: {row[1]}")
        
        # 查询最新的5条AI生成的记录
        print("\n2. 最新的5条AI生成的记录:")
        result = conn.execute(text("""
            SELECT id, content, design_reason, difficulty_reason, 
                   distractor_reasons, generated_question_id, created_at
            FROM questions 
            WHERE source = 'AI生成'
            ORDER BY id DESC 
            LIMIT 5
        """))
        
        for row in result:
            print(f"\n  记录 ID: {row[0]}")
            print(f"  内容: {row[1][:50] if row[1] else 'None'}...")
            print(f"  design_reason: {row[2][:50] if row[2] else 'None'}...")
            print(f"  difficulty_reason: {row[3][:50] if row[3] else 'None'}...")
            print(f"  distractor_reasons: {row[4][:100] if row[4] else 'None'}...")
            print(f"  generated_question_id: {row[5]}")
            print(f"  创建时间: {row[6]}")

if __name__ == "__main__":
    check_generated_questions()
    check_questions()
