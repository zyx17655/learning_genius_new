from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models import AICallLog

router = APIRouter()

class AICallLogResponse(BaseModel):
    id: int
    task_id: Optional[int]
    call_type: str
    model: str
    status: str
    token_count: int
    duration_ms: int
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class AICallLogDetail(BaseModel):
    id: int
    task_id: Optional[int]
    call_type: str
    model: str
    prompt: str
    system_prompt: Optional[str]
    response: Optional[str]
    status: str
    token_count: int
    duration_ms: int
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/ai-logs", response_model=List[AICallLogResponse])
def get_ai_call_logs(
    task_id: Optional[int] = Query(None, description="任务ID"),
    call_type: Optional[str] = Query(None, description="调用类型"),
    status: Optional[str] = Query(None, description="状态"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(AICallLog)
    
    if task_id:
        query = query.filter(AICallLog.task_id == task_id)
    if call_type:
        query = query.filter(AICallLog.call_type == call_type)
    if status:
        query = query.filter(AICallLog.status == status)
    
    logs = query.order_by(AICallLog.created_at.desc()).offset(offset).limit(limit).all()
    
    return logs

@router.get("/ai-logs/{log_id}", response_model=AICallLogDetail)
def get_ai_call_log_detail(log_id: int, db: Session = Depends(get_db)):
    log = db.query(AICallLog).filter(AICallLog.id == log_id).first()
    if not log:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="AI调用记录不存在")
    return log

@router.get("/tasks/{task_id}/ai-logs", response_model=List[AICallLogResponse])
def get_task_ai_logs(task_id: int, db: Session = Depends(get_db)):
    logs = db.query(AICallLog).filter(AICallLog.task_id == task_id).order_by(AICallLog.created_at.desc()).all()
    return logs
