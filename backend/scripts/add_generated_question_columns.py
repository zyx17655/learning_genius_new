"""
添加 is_draft 和 is_discarded 列到 generated_questions 表
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
            ("is_draft", "TINYINT(1)", "是否草稿", "0"),
            ("is_discarded", "TINYINT(1)", "是否已丢弃", "0")
        ]
        
        for col_name, col_type, col_comment, col_default in columns_to_add:
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'generated_questions'
                AND COLUMN_NAME = %s
            """, (settings.MYSQL_DATABASE, col_name))
            
            if not cursor.fetchone():
                print(f"Adding {col_name} column...")
                cursor.execute(f"""
                    ALTER TABLE generated_questions 
                    ADD COLUMN {col_name} {col_type} DEFAULT {col_default} COMMENT '{col_comment}'
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
