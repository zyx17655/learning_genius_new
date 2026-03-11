from sqlalchemy import create_engine, text
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    print("开始添加自定义规则专属维度字段...")
    
    try:
        conn.execute(text("ALTER TABLE question_rules ADD COLUMN notation_convention TEXT COMMENT '学科表达与符号习惯'"))
        print("✓ 添加字段: notation_convention")
    except Exception as e:
        print(f"× notation_convention: {e}")
    
    try:
        conn.execute(text("ALTER TABLE question_rules ADD COLUMN assessment_focus TEXT COMMENT '考察偏好与方法论'"))
        print("✓ 添加字段: assessment_focus")
    except Exception as e:
        print(f"× assessment_focus: {e}")
    
    try:
        conn.execute(text("ALTER TABLE question_rules ADD COLUMN subject_traps TEXT COMMENT '干扰项逻辑陷阱'"))
        print("✓ 添加字段: subject_traps")
    except Exception as e:
        print(f"× subject_traps: {e}")
    
    try:
        conn.execute(text("ALTER TABLE question_rules ADD COLUMN stem_style TEXT COMMENT '语言风格与题干结构'"))
        print("✓ 添加字段: stem_style")
    except Exception as e:
        print(f"× stem_style: {e}")
    
    try:
        conn.execute(text("ALTER TABLE question_rules ADD COLUMN solution_blueprint TEXT COMMENT '解析深度与标准'"))
        print("✓ 添加字段: solution_blueprint")
    except Exception as e:
        print(f"× solution_blueprint: {e}")
    
    conn.commit()
    print("\n数据库迁移完成！")
