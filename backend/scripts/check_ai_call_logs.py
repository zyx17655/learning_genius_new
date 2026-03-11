"""
检查 ai_call_logs 表是否存在
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
        
        # 检查 ai_call_logs 表是否存在
        cursor.execute("SHOW TABLES LIKE 'ai_call_logs'")
        result = cursor.fetchone()
        if result:
            print("ai_call_logs 表存在")
            cursor.execute("DESCRIBE ai_call_logs")
            columns = cursor.fetchall()
            print("\nai_call_logs 表结构:")
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
        else:
            print("ai_call_logs 表不存在！正在创建...")
            cursor.execute("""
                CREATE TABLE ai_call_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task_id INT NULL,
                    call_type VARCHAR(50) NOT NULL,
                    model VARCHAR(50) DEFAULT 'moonshot-v1-8k',
                    prompt TEXT NOT NULL,
                    system_prompt TEXT,
                    response TEXT,
                    status VARCHAR(20) DEFAULT 'pending',
                    error_message TEXT,
                    token_count INT DEFAULT 0,
                    duration_ms INT DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES generation_tasks(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI调用日志表'
            """)
            conn.commit()
            print("ai_call_logs 表创建成功！")
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_table()
