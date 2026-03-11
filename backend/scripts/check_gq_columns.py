import sys
sys.path.insert(0, '.')

from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SHOW COLUMNS FROM generated_questions"))
    print("generated_questions Table columns:")
    for row in result:
        print(f"  Field: {row[0]}, Type: {row[1]}, Null: {row[2]}, Key: {row[3]}")
