"""
重建 generated_questions 表
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from app.config import settings

def recreate_table():
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
        
        print("正在备份旧表...")
        cursor.execute("CREATE TABLE IF NOT EXISTS generated_questions_backup AS SELECT * FROM generated_questions")
        conn.commit()
        print("备份完成")
        
        print("正在删除旧表...")
        cursor.execute("DROP TABLE IF EXISTS generated_questions")
        conn.commit()
        print("旧表已删除")
        
        print("正在创建新表...")
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
                difficulty_reason TEXT,
                FOREIGN KEY (task_id) REFERENCES generation_tasks(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生成题目表'
        """)
        conn.commit()
        print("新表创建成功！")
        
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
    recreate_table()
