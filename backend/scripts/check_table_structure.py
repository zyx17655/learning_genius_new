"""
检查 generated_questions 表的列顺序
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from app.config import settings

def check_table():
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
        
        # 获取表结构
        cursor.execute("DESCRIBE generated_questions")
        columns = cursor.fetchall()
        
        print("generated_questions 表结构:")
        print("-" * 40)
        for col in columns:
            print(f"{col[0]: {col[1]} {col[2]} {col[3]} {col[4]} {col[5]}")
        
        # 检查模型定义的列
        from app.models import GeneratedQuestion
        print("\n模型定义的列:")
        for col in GeneratedQuestion.__table__.columns:
            print(f"- {col.name}")
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_table()
