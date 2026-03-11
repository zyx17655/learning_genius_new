"""
添加 difficulty_reason 列到 generated_questions 表
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from app.config import settings

def migrate():
    conn = pymysql.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE,
        charset='utf8mb4'
    )
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'generated_questions'
            AND COLUMN_NAME = 'difficulty_reason'
        """, (settings.MYSQL_DATABASE,))
        
        if not cursor.fetchone():
            print("Adding difficulty_reason column...")
            cursor.execute("""
                ALTER TABLE generated_questions 
                ADD COLUMN difficulty_reason TEXT COMMENT '难度设定理由'
                AFTER created_at
            """)
            conn.commit()
            print("Column added successfully!")
        else:
            print("Column difficulty_reason already exists.")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
