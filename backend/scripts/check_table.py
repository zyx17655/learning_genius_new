import sys
sys.path.insert(0, '.')

from app.database import engine
from sqlalchemy import inspect

insp = inspect(engine)
cols = insp.get_columns('generated_questions')

print('Table columns:')
for c in cols:
    print(f'  - {c["name"]}: {c["type"]}')
