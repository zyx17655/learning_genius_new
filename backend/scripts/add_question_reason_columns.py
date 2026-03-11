"""
添加 design_reason, difficulty_reason, distractor_reasons 列到 questions 表
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
        
        columns_to_add = [
            ("design_reason", "TEXT", "题目设计依据"),
            ("difficulty_reason", "TEXT", "难度设定理由"),
            ("distractor_reasons", "TEXT", "干扰项设计理由JSON")
        ]
        
        for col_name, col_type, col_comment in columns_to_add:
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'questions'
                AND COLUMN_NAME = %s
            """, (settings.MYSQL_DATABASE, col_name))
            
            if not cursor.fetchone():
                print(f"Adding {col_name} column...")
                cursor.execute(f"""
                    ALTER TABLE questions 
                    ADD COLUMN {col_name} {col_type} COMMENT '{col_comment}'
                    AFTER explanation
                """)
                conn.commit()
                print(f"Column {col_name} added successfully!")
            else:
                print(f"Column {col_name} already exists.")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
