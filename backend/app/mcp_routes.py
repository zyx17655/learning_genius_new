from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json

from app.database import get_db
from app.models import McpCallLog

router = APIRouter()


class McpLogResponse(BaseModel):
    id: int
    request_params: str
    response_result: Optional[str]
    status: str
    error_message: Optional[str]
    duration_ms: int
    created_at: datetime

    class Config:
        from_attributes = True


class McpLogDetailResponse(BaseModel):
    id: int
    request_params: dict
    response_result: Optional[dict]
    status: str
    error_message: Optional[str]
    duration_ms: int
    created_at: str


@router.get("/logs")
def get_mcp_logs(
    page: int = 1,
    per_page: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(McpCallLog)

    if status:
        query = query.filter(McpCallLog.status == status)

    total = query.count()
    logs = query.order_by(McpCallLog.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return {
        "code": 0,
        "data": {
            "logs": [
                {
                    "id": log.id,
                    "request_params": log.request_params,
                    "response_result": log.response_result,
                    "status": log.status,
                    "error_message": log.error_message,
                    "duration_ms": log.duration_ms,
                    "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else ""
                }
                for log in logs
            ],
            "total": total,
            "page": page,
            "per_page": per_page
        }
    }


@router.get("/logs/{log_id}")
def get_mcp_log_detail(log_id: int, db: Session = Depends(get_db)):
    log = db.query(McpCallLog).filter(McpCallLog.id == log_id).first()

    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")

    try:
        request_params = json.loads(log.request_params) if log.request_params else {}
    except:
        request_params = log.request_params

    try:
        response_result = json.loads(log.response_result) if log.response_result else None
    except:
        response_result = log.response_result

    return {
        "code": 0,
        "data": {
            "id": log.id,
            "request_params": request_params,
            "response_result": response_result,
            "status": log.status,
            "error_message": log.error_message,
            "duration_ms": log.duration_ms,
            "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else ""
        }
    }


@router.get("/stats")
def get_mcp_stats(db: Session = Depends(get_db)):
    total = db.query(McpCallLog).count()
    completed = db.query(McpCallLog).filter(McpCallLog.status == "completed").count()
    failed = db.query(McpCallLog).filter(McpCallLog.status == "failed").count()

    recent_logs = db.query(McpCallLog).order_by(McpCallLog.created_at.desc()).limit(10).all()
    recent_total_duration = sum(log.duration_ms for log in recent_logs if log.duration_ms)
    avg_duration = recent_total_duration // len(recent_logs) if recent_logs else 0

    return {
        "code": 0,
        "data": {
            "total_calls": total,
            "completed_calls": completed,
            "failed_calls": failed,
            "avg_duration_ms": avg_duration
        }
    }


@router.delete("/logs/cleanup")
def cleanup_mcp_logs(days: int = 30, db: Session = Depends(get_db)):
    from datetime import timedelta
    cutoff_date = datetime.now() - timedelta(days=days)

    deleted = db.query(McpCallLog).filter(McpCallLog.created_at < cutoff_date).delete()
    db.commit()

    return {
        "code": 0,
        "message": f"已删除 {deleted} 条 {days} 天前的日志"
    }
