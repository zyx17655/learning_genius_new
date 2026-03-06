import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models import KnowledgeDocument, KnowledgeChunk

db = SessionLocal()

print("清理旧的知识库数据...")
deleted_chunks = db.query(KnowledgeChunk).delete()
deleted_docs = db.query(KnowledgeDocument).delete()
db.commit()

print(f"删除了 {deleted_chunks} 个知识片段")
print(f"删除了 {deleted_docs} 个文档")

db.close()

print("清理完成!")
