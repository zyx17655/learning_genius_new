import sys
sys.path.insert(0, '.')

from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("DESCRIBE generated_questions"))
    print("generated_questions Table structure:")
    for row in result:
        print(f"  {row}")
