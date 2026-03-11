"""
检查并修复 generated_questions 表结构
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from app.config import settings

def fix_table():
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
        
        # 获取当前表结构
        cursor.execute("SHOW CREATE TABLE generated_questions")
        result = cursor.fetchone()
        print("当前表创建语句:")
        print(result[1])
        print("\n" + "="*60 + "\n")
        
        # 删除旧表
        cursor.execute("DROP TABLE IF EXISTS generated_questions")
        conn.commit()
        print("旧表已删除")
        
        # 重新创建表，确保列顺序与模型定义完全一致
        cursor.execute("""
            CREATE TABLE generated_questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task_id INT NOT NULL,
                content TEXT NOT NULL,
                question_type VARCHAR(20) NOT NULL,
                difficulty VARCHAR(10) NOT NULL,
                answer VARCHAR(500),
                explanation TEXT,
                design_reason TEXT,
                distractor_reasons TEXT,
                knowledge_points VARCHAR(500),
                options_json TEXT,
                is_selected TINYINT(1) DEFAULT 0,
                is_draft TINYINT(1) DEFAULT 0,
                is_discarded TINYINT(1) DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                difficulty_reason TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生成题目表'
        """)
        conn.commit()
        print("新表创建成功！")
        
        # 验证新表结构
        cursor.execute("DESCRIBE generated_questions")
        columns = cursor.fetchall()
        print("\n新表结构:")
        for col in columns:
            print(f"  {col[0]}: {col[1]}")
        
    except Exception as e:
        print(f"错误: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_table()
