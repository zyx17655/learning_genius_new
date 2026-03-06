from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class KnowledgePointBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    level: int = 1

class KnowledgePointResponse(KnowledgePointBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

class TagResponse(TagBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class OptionBase(BaseModel):
    content: str
    is_correct: bool = False
    order_index: int = 0

class OptionResponse(OptionBase):
    id: int
    
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    content: str
    question_type: str = "单选"
    difficulty: str = "L2"
    status: str = "草稿"
    source: str = "手动录入"
    answer: Optional[str] = None
    explanation: Optional[str] = None
    creator: str = "系统"

class QuestionCreate(QuestionBase):
    options: List[OptionBase] = []
    knowledge_point_ids: List[int] = []
    tag_names: List[str] = []

class QuestionUpdate(BaseModel):
    content: Optional[str] = None
    question_type: Optional[str] = None
    difficulty: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    reviewer: Optional[str] = None
    options: Optional[List[OptionBase]] = None
    knowledge_point_ids: Optional[List[int]] = None
    tag_names: Optional[List[str]] = None

class QuestionResponse(QuestionBase):
    id: int
    reviewer: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    options: List[OptionResponse] = []
    knowledge_points: List[str] = []
    tags: List[str] = []
    
    class Config:
        from_attributes = True

class QuestionListResponse(BaseModel):
    questions: List[QuestionResponse]
    total: int
    page: int
    per_page: int

class StatsResponse(BaseModel):
    total: int
    reviewed: int
    pending: int
    draft: int
    type_stats: List[dict]

class GenerationTaskCreate(BaseModel):
    knowledge_input: Optional[str] = None
    knowledge_ids: List[int] = []
    question_types: List[str] = []
    type_counts: dict = {}
    difficulty_config: dict = {}
    distractor_list: List[dict] = []
    preference_list: List[dict] = []
    custom_requirement: Optional[str] = None
    total_count: int = 0

class GeneratedQuestionResponse(BaseModel):
    id: int
    content: str
    question_type: str
    difficulty: str
    answer: Optional[str] = None
    explanation: Optional[str] = None
    design_reason: Optional[str] = None
    distractor_reasons: Optional[List[dict]] = None
    knowledge_points: List[str] = []
    options: List[dict] = []
    is_selected: bool = False
    is_draft: bool = False
    is_discarded: bool = False
    
    class Config:
        from_attributes = True

class ApiResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[dict] = None
