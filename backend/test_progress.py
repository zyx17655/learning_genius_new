import json
from app.database import SessionLocal
from app.models import GenerationTask

def test_progress_calculation():
    """测试进度计算逻辑"""
    
    db = SessionLocal()
    
    try:
        # 查找最新的任务
        task = db.query(GenerationTask).order_by(GenerationTask.id.desc()).first()
        
        if not task:
            print("没有找到任务")
            return
        
        print(f"=" * 80)
        print(f"任务 ID: {task.id}")
        print(f"任务状态: {task.status}")
        print(f"=" * 80)
        
        print(f"任务结果原始数据:")
        print(task.result)
        print(f"=" * 80)
        
        # 解析结果
        if task.result:
            result = json.loads(task.result)
            print(f"解析后的结果:")
            print(f"  completed_count: {result.get('completed_count')}")
            print(f"  failed_count: {result.get('failed_count')}")
            print(f"  current_question: {result.get('current_question')}")
            print(f"  total_questions: {result.get('total_questions')}")
            print(f"  message: {result.get('message')}")
            print(f"  verification_enabled: {result.get('verification_enabled')}")
            print(f"=" * 80)
            
            # 计算进度
            current = result.get('current_question', 0)
            total = result.get('total_questions', 10)
            
            if total > 0:
                progress = (current / total) * 100
                print(f"进度计算: {current}/{total} = {progress:.1f}%")
            else:
                print("进度计算: 0% (total_questions=0)")
            print(f"=" * 80)
    
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_progress_calculation()
