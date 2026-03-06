import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.knowledge_service import KnowledgeService

def process_all_pdfs():
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_base", "raw")
    
    if not os.path.exists(raw_dir):
        print(f"目录不存在: {raw_dir}")
        return
    
    pdf_files = [f for f in os.listdir(raw_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("没有找到PDF文件")
        return
    
    print(f"找到 {len(pdf_files)} 个PDF文件:")
    for f in pdf_files:
        print(f"  - {f}")
    
    db = SessionLocal()
    service = KnowledgeService(db)
    
    for pdf_file in pdf_files:
        file_path = os.path.join(raw_dir, pdf_file)
        print(f"\n处理文件: {pdf_file}")
        print(f"文件大小: {os.path.getsize(file_path) / 1024 / 1024:.2f} MB")
        
        try:
            doc = service.process_document(file_path, pdf_file)
            print(f"处理完成!")
            print(f"  - 文档ID: {doc.id}")
            print(f"  - 知识片段数: {doc.total_chunks}")
            print(f"  - 状态: {doc.status}")
        except Exception as e:
            print(f"处理失败: {str(e)}")
    
    db.close()
    print("\n所有文件处理完成!")

if __name__ == "__main__":
    process_all_pdfs()
