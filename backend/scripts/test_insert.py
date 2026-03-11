"""
直接测试数据库插入
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
import json
from app.config import settings

def test_insert():
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
        
        # 首先创建一个测试任务
        cursor.execute("""
            INSERT INTO generation_tasks (knowledge_input, question_types, status)
            VALUES ('测试', '单选', 'completed')
        """)
        conn.commit()
        task_id = cursor.lastrowid
        print(f"创建测试任务: task_id={task_id}")
        
        # 测试插入 generated_questions
        test_data = {
            "task_id": task_id,
            "content": "测试题目内容",
            "question_type": "单选",
            "difficulty": "简单",
            "answer": "A",
            "explanation": "测试解析",
            "design_reason": "测试设计理由",
            "difficulty_reason": "测试难度理由",
            "distractor_reasons": json.dumps([]),
            "knowledge_points": "测试知识点",
            "options_json": json.dumps([
                {"content": "选项A", "is_correct": True},
                {"content": "选项B", "is_correct": False}
            ])
        }
        
        sql = """
            INSERT INTO generated_questions 
            (task_id, content, question_type, difficulty, answer, explanation, 
             design_reason, difficulty_reason, distractor_reasons, knowledge_points, options_json)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            test_data["task_id"],
            test_data["content"],
            test_data["question_type"],
            test_data["difficulty"],
            test_data["answer"],
            test_data["explanation"],
            test_data["design_reason"],
            test_data["difficulty_reason"],
            test_data["distractor_reasons"],
            test_data["knowledge_points"],
            test_data["options_json"]
        ))
        conn.commit()
        print("插入成功！")
        
        # 查询验证
        cursor.execute("SELECT * FROM generated_questions WHERE task_id = %s", (task_id,))
        result = cursor.fetchone()
        print(f"查询结果: {result}")
        
        # 清理测试数据
        cursor.execute("DELETE FROM generated_questions WHERE task_id = %s", (task_id,))
        cursor.execute("DELETE FROM generation_tasks WHERE id = %s", (task_id,))
        conn.commit()
        print("测试数据已清理")
        
    except Exception as e:
        print(f"错误: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    test_insert()
