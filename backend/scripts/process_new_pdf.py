import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.knowledge_service import KnowledgeService

def process_new_pdf():
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_base", "raw")
    
    target_file = "3-小波分析完美教程经典.pdf"
    file_path = os.path.join(raw_dir, target_file)
    
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    print(f"处理文件: {target_file}")
    print(f"文件大小: {os.path.getsize(file_path) / 1024 / 1024:.2f} MB")
    
    db = SessionLocal()
    service = KnowledgeService(db)
    
    try:
        doc = service.process_document(file_path, target_file)
        print(f"\n处理完成!")
        print(f"  - 文档ID: {doc.id}")
        print(f"  - 知识片段数: {doc.total_chunks}")
        print(f"  - 状态: {doc.status}")
    except Exception as e:
        print(f"处理失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    db.close()

if __name__ == "__main__":
    process_new_pdf()
