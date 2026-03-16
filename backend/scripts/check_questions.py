from app.database import SessionLocal
from app.models import Question

db = SessionLocal()
count = db.query(Question).count()
print(f'题目总数: {count}')

questions = db.query(Question).limit(3).all()
for q in questions:
    print(f'ID: {q.id}, 内容: {q.content[:50]}...')

db.close()
