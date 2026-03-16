"""
数据库迁移脚本：添加 generated_question_id 字段到 questions 表
"""
from sqlalchemy import text
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def migrate():
    """添加 generated_question_id 字段到 questions 表"""
    try:
        with engine.connect() as conn:
            # 检查字段是否已存在 (MySQL语法)
            result = conn.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'questions' AND COLUMN_NAME = 'generated_question_id'
            """))
            
            if result.rowcount == 0:
                # 添加字段 (MySQL语法)
                conn.execute(text("""
                    ALTER TABLE questions 
                    ADD COLUMN generated_question_id INT,
                    ADD CONSTRAINT fk_generated_question 
                    FOREIGN KEY (generated_question_id) REFERENCES generated_questions(id) 
                    ON DELETE SET NULL
                """))
                conn.commit()
                print("✅ 成功添加 generated_question_id 字段到 questions 表")
            else:
                print("ℹ️ generated_question_id 字段已存在，跳过")
                
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate()
