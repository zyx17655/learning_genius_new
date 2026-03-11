"""
重建 ai_call_logs 表
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
        
        # 删除旧表
        cursor.execute("DROP TABLE IF EXISTS ai_call_logs")
        conn.commit()
        print("旧表已删除")
        
        # 重新创建表
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
        print("新表创建成功！")
        
        # 验证新表结构
        cursor.execute("DESCRIBE ai_call_logs")
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
