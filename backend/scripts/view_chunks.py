import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models import KnowledgeChunk

db = SessionLocal()
chunks = db.query(KnowledgeChunk).limit(5).all()

print(f"数据库中共有 {db.query(KnowledgeChunk).count()} 条知识片段\n")
print("=" * 60)

for c in chunks:
    print(f"ID: {c.id}")
    print(f"标题: {c.title}")
    print(f"分类: {c.category}")
    print(f"内容长度: {len(c.content)} 字")
    print(f"内容预览: {c.content[:100]}...")
    print("=" * 60)

db.close()
