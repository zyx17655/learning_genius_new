"""
检查 generation_tasks 表是否存在
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from app.config import settings

def check_tables():
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
        
        # 检查 generation_tasks 表是否存在
        cursor.execute("SHOW TABLES LIKE 'generation_tasks'")
        result = cursor.fetchone()
        if result:
            print("generation_tasks 表存在")
            cursor.execute("DESCRIBE generation_tasks")
            columns = cursor.fetchall()
            print("\ngeneration_tasks 表结构:")
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
        else:
            print("generation_tasks 表不存在！")
        
        print("\n" + "="*60 + "\n")
        
        # 检查 generated_questions 表
        cursor.execute("SHOW TABLES LIKE 'generated_questions'")
        result = cursor.fetchone()
        if result:
            print("generated_questions 表存在")
            cursor.execute("DESCRIBE generated_questions")
            columns = cursor.fetchall()
            print("\ngenerated_questions 表结构:")
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
        else:
            print("generated_questions 表不存在！")
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_tables()
