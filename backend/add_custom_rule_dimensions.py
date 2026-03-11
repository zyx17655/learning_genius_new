"""
添加自定义规则专属维度字段到question_rules表

Revision ID: add_custom_rule_dimensions
Revises: 
Create Date: 2024-01-01

"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('question_rules', sa.Column('notation_convention', sa.Text(), nullable=True, comment='学科表达与符号习惯'))
    op.add_column('question_rules', sa.Column('assessment_focus', sa.Text(), nullable=True, comment='考察偏好与方法论'))
    op.add_column('question_rules', sa.Column('subject_traps', sa.Text(), nullable=True, comment='干扰项逻辑陷阱'))
    op.add_column('question_rules', sa.Column('stem_style', sa.Text(), nullable=True, comment='语言风格与题干结构'))
    op.add_column('question_rules', sa.Column('solution_blueprint', sa.Text(), nullable=True, comment='解析深度与标准'))


def downgrade():
    op.drop_column('question_rules', 'notation_convention')
    op.drop_column('question_rules', 'assessment_focus')
    op.drop_column('question_rules', 'subject_traps')
    op.drop_column('question_rules', 'stem_style')
    op.drop_column('question_rules', 'solution_blueprint')
