from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    __table_args__ = {'comment': '知识文档表 - 存储上传的知识文档'}
    
    id = Column(Integer, primary_key=True, comment='主键ID')
    filename = Column(String(255), nullable=False, comment='文件名')
    original_name = Column(String(255), nullable=False, comment='原始文件名')
    file_path = Column(String(500), nullable=False, comment='文件存储路径')
    file_size = Column(Integer, default=0, comment='文件大小(字节)')
    file_type = Column(String(20), default="pdf", comment='文件类型：pdf/docx/doc/xlsx/xls/txt')
    status = Column(String(20), default="pending", comment='状态：pending-待处理, processing-处理中, completed-已完成, failed-失败')
    total_chunks = Column(Integer, default=0, comment='分块总数')
    processed_at = Column(DateTime, comment='处理完成时间')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    
    chunks = relationship("KnowledgeChunk", back_populates="document", cascade="all, delete-orphan")

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    __table_args__ = {'comment': '知识分块表 - 存储文档分块后的内容'}
    
    id = Column(Integer, primary_key=True, index=True, comment='主键ID')
    document_id = Column(Integer, ForeignKey("knowledge_documents.id", ondelete="CASCADE"), nullable=False, comment='关联文档ID')
    title = Column(String(255), nullable=False, comment='分块标题')
    content = Column(Text, nullable=False, comment='分块内容')
    category = Column(String(100), comment='知识分类')
    keywords = Column(String(500), comment='关键词')
    page_number = Column(Integer, comment='页码')
    chunk_index = Column(Integer, default=0, comment='分块索引')
    char_count = Column(Integer, default=0, comment='字符数')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    
    document = relationship("KnowledgeDocument", back_populates="chunks")

class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"
    __table_args__ = {'comment': '知识点表 - 存储知识点层级结构'}
    
    id = Column(Integer, primary_key=True, index=True, comment='主键ID')
    name = Column(String(100), nullable=False, comment='知识点名称')
    parent_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=True, comment='父知识点ID')
    level = Column(Integer, default=1, comment='层级：1-一级, 2-二级, 3-三级')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    children = relationship("KnowledgePoint", backref="parent", remote_side=[id])
    questions = relationship("Question", secondary="question_knowledge", back_populates="knowledge_points")

class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = {'comment': '标签表 - 存储题目标签'}
    
    id = Column(Integer, primary_key=True, index=True, comment='主键ID')
    name = Column(String(50), unique=True, nullable=False, comment='标签名称')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    
    questions = relationship("Question", secondary="question_tags", back_populates="tags")

class Question(Base):
    __tablename__ = "questions"
    __table_args__ = {'comment': '题目表 - 存储所有题目的基本信息'}
    
    id = Column(Integer, primary_key=True, index=True, comment='主键ID')
    content = Column(Text, nullable=False, comment='题目内容')
    question_type = Column(String(20), default="单选", comment='题目类型：单选/多选/判断/填空/主观')
    difficulty = Column(String(10), default="Medium", comment='难度等级：Easy-简单, Medium-中等, Hard-困难')
    status = Column(String(20), default="草稿", comment='状态：草稿/已发布/已归档')
    source = Column(String(50), default="手动录入", comment='来源：手动录入/AI生成/导入')
    answer = Column(String(500), comment='正确答案')
    explanation = Column(Text, comment='答案解析')
    design_reason = Column(Text, comment='题目设计依据')
    difficulty_reason = Column(Text, comment='难度设定理由')
    distractor_reasons = Column(Text, comment='干扰项设计理由JSON')
    creator = Column(String(50), default="系统", comment='创建者')
    reviewer = Column(String(50), comment='审核者')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")
    knowledge_points = relationship("KnowledgePoint", secondary="question_knowledge", back_populates="questions")
    tags = relationship("Tag", secondary="question_tags", back_populates="questions")

class Option(Base):
    __tablename__ = "options"
    __table_args__ = {'comment': '选项表 - 存储选择题的选项'}
    
    id = Column(Integer, primary_key=True, index=True, comment='主键ID')
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, comment='关联题目ID')
    content = Column(Text, nullable=False, comment='选项内容')
    is_correct = Column(Boolean, default=False, comment='是否正确答案')
    order_index = Column(Integer, default=0, comment='选项顺序')
    
    question = relationship("Question", back_populates="options")

class QuestionKnowledge(Base):
    __tablename__ = "question_knowledge"
    __table_args__ = {'comment': '题目知识点关联表 - 题目与知识点的多对多关系'}
    
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True, comment='题目ID')
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id", ondelete="CASCADE"), primary_key=True, comment='知识点ID')

class QuestionTag(Base):
    __tablename__ = "question_tags"
    __table_args__ = {'comment': '题目标签关联表 - 题目与标签的多对多关系'}
    
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True, comment='题目ID')
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True, comment='标签ID')

class GenerationTask(Base):
    __tablename__ = "generation_tasks"
    __table_args__ = {'comment': '生成任务表 - 记录AI生成题目的任务'}
    
    id = Column(Integer, primary_key=True, comment='主键ID')
    knowledge_input = Column(String(500), comment='知识范围输入')
    knowledge_ids = Column(String(255), comment='关联知识点ID列表，逗号分隔')
    question_types = Column(String(255), nullable=False, comment='题目类型列表，逗号分隔')
    type_counts = Column(Text, comment='各类型题目数量配置JSON')
    difficulty_config = Column(Text, comment='难度配置JSON')
    distractor_list = Column(Text, comment='干扰项配置JSON')
    preference_list = Column(Text, comment='内容偏好配置JSON')
    custom_requirement = Column(Text, comment='自定义要求')
    question_count = Column(Integer, default=0, comment='题目总数')
    status = Column(String(20), default="pending", comment='状态：pending-等待中, running-执行中, completed-已完成, failed-失败')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    completed_at = Column(DateTime, comment='完成时间')
    result = Column(Text, comment='执行结果JSON')
    
    generated_questions = relationship("GeneratedQuestion", back_populates="task", cascade="all, delete-orphan")
    ai_call_logs = relationship("AICallLog", back_populates="task", cascade="all, delete-orphan")

class GeneratedQuestion(Base):
    __tablename__ = "generated_questions"
    __table_args__ = {'comment': '生成题目表 - 存储AI生成的题目'}
    
    id = Column(Integer, primary_key=True, comment='主键ID')
    task_id = Column(Integer, ForeignKey("generation_tasks.id", ondelete="CASCADE"), nullable=False, comment='关联生成任务ID')
    content = Column(Text, nullable=False, comment='题目内容')
    question_type = Column(String(20), nullable=False, comment='题目类型：单选/多选/判断/填空/主观')
    difficulty = Column(String(10), nullable=False, comment='难度等级：Easy-简单/Medium-中等/Hard-困难')
    answer = Column(String(500), comment='正确答案')
    explanation = Column(Text, comment='答案解析')
    design_reason = Column(Text, comment='设计理由')
    distractor_reasons = Column(Text, comment='干扰项设计理由JSON')
    knowledge_points = Column(String(500), comment='关联知识点，逗号分隔')
    options_json = Column(Text, comment='选项JSON')
    is_selected = Column(Boolean, default=False, comment='是否被选中')
    is_draft = Column(Boolean, default=False, comment='是否草稿')
    is_discarded = Column(Boolean, default=False, comment='是否已丢弃')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    difficulty_reason = Column(Text, comment='难度设定理由')
    
    task = relationship("GenerationTask", back_populates="generated_questions")

class QuestionRule(Base):
    __tablename__ = "question_rules"
    __table_args__ = {'comment': '出题规则表 - 存储出题规则配置'}
    
    id = Column(Integer, primary_key=True, index=True, comment='主键ID')
    name = Column(String(100), nullable=False, comment='规则名称')
    description = Column(Text, comment='规则描述')
    scene = Column(String(100), comment='适用场景')
    status = Column(String(20), default="启用", comment='状态：启用/禁用')
    is_default = Column(Boolean, default=False, comment='是否默认规则')
    role = Column(Text, comment='角色设定prompt')
    core_principles = Column(Text, comment='核心原则JSON')
    workflow = Column(Text, comment='工作流程JSON')
    specifications = Column(Text, comment='命题规范JSON')
    distractor_mechanics = Column(Text, comment='干扰项设置JSON')
    domain_skills = Column(Text, comment='专项技能JSON')
    output_template = Column(Text, comment='输出模板')
    notation_convention = Column(Text, comment='学科表达与符号习惯')
    assessment_focus = Column(Text, comment='考察偏好与方法论')
    subject_traps = Column(Text, comment='干扰项逻辑陷阱')
    stem_style = Column(Text, comment='语言风格与题干结构')
    solution_blueprint = Column(Text, comment='解析深度与标准')
    creator = Column(String(50), default="系统", comment='创建者')
    use_count = Column(Integer, default=0, comment='使用次数')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

class AICallLog(Base):
    __tablename__ = "ai_call_logs"
    __table_args__ = {'comment': 'AI调用日志表 - 记录每次AI调用的prompt和响应'}
    
    id = Column(Integer, primary_key=True, comment='主键ID')
    task_id = Column(Integer, ForeignKey("generation_tasks.id", ondelete="CASCADE"), nullable=True, comment='关联生成任务ID')
    call_type = Column(String(50), nullable=False, comment='调用类型：question_generation-题目生成, rule_analysis-规则分析')
    model = Column(String(50), default="moonshot-v1-8k", comment='使用的AI模型')
    prompt = Column(Text, nullable=False, comment='发送给AI的完整prompt内容')
    system_prompt = Column(Text, comment='系统提示词')
    response = Column(Text, comment='AI返回的完整响应内容')
    status = Column(String(20), default="pending", comment='调用状态：pending-等待中, running-执行中, success-成功, failed-失败')
    error_message = Column(Text, comment='错误信息')
    token_count = Column(Integer, default=0, comment='消耗的token数量')
    duration_ms = Column(Integer, default=0, comment='调用耗时(毫秒)')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    
    task = relationship("GenerationTask", back_populates="ai_call_logs")
