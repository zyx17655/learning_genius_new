from app import db
from datetime import datetime

class KnowledgePoint(db.Model):
    __tablename__ = 'knowledge_points'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('knowledge_points.id'))
    level = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 单选/多选/判断/填空/主观
    difficulty = db.Column(db.String(20), nullable=False)  # L1-L5
    status = db.Column(db.String(20), nullable=False, default='草稿')  # 草稿/已审核/已禁用
    knowledge_point_id = db.Column(db.Integer, db.ForeignKey('knowledge_points.id'))
    explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = db.relationship('Tag', secondary='question_tags', backref='questions')

class QuestionTag(db.Model):
    __tablename__ = 'question_tags'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, nullable=False)

class GenerationTask(db.Model):
    __tablename__ = 'generation_tasks'
    id = db.Column(db.Integer, primary_key=True)
    knowledge_point_ids = db.Column(db.String(255), nullable=False)
    question_types = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    question_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending/running/completed/failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    result = db.Column(db.Text)