from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from datetime import datetime
import json

from app.database import get_db
from app.models import KnowledgePoint, Tag, Question, Option, GenerationTask, GeneratedQuestion, QuestionKnowledge, QuestionTag
from app.schemas import (
    QuestionCreate, QuestionUpdate, QuestionResponse, QuestionListResponse,
    StatsResponse, GenerationTaskCreate, GeneratedQuestionResponse, ApiResponse
)

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "message": "服务运行正常"}

@router.get("/knowledge-points")
def get_knowledge_points(db: Session = Depends(get_db)):
    points = db.query(KnowledgePoint).filter(KnowledgePoint.parent_id == None).all()
    return [{"id": p.id, "name": p.name, "level": p.level} for p in points]

@router.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return [{"id": t.id, "name": t.name} for t in tags]

@router.get("/questions", response_model=QuestionListResponse)
def get_questions(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    question_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    
    if question_type:
        query = query.filter(Question.question_type == question_type)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if status:
        query = query.filter(Question.status == status)
    if keyword:
        query = query.filter(Question.content.contains(keyword))
    
    total = query.count()
    questions = query.order_by(Question.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    
    result = []
    for q in questions:
        options = db.query(Option).filter(Option.question_id == q.id).order_by(Option.order_index).all()
        knowledge_points = [kp.name for kp in q.knowledge_points]
        tags = [t.name for t in q.tags]
        
        result.append(QuestionResponse(
            id=q.id,
            content=q.content,
            question_type=q.question_type,
            difficulty=q.difficulty,
            status=q.status,
            source=q.source,
            answer=q.answer,
            explanation=q.explanation,
            creator=q.creator,
            reviewer=q.reviewer,
            created_at=q.created_at,
            updated_at=q.updated_at,
            options=[{"id": o.id, "content": o.content, "is_correct": o.is_correct} for o in options],
            knowledge_points=knowledge_points,
            tags=tags
        ))
    
    return QuestionListResponse(questions=result, total=total, page=page, per_page=per_page)

@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    options = db.query(Option).filter(Option.question_id == q.id).order_by(Option.order_index).all()
    knowledge_points = [kp.name for kp in q.knowledge_points]
    tags = [t.name for t in q.tags]
    
    return QuestionResponse(
        id=q.id,
        content=q.content,
        question_type=q.question_type,
        difficulty=q.difficulty,
        status=q.status,
        source=q.source,
        answer=q.answer,
        explanation=q.explanation,
        creator=q.creator,
        reviewer=q.reviewer,
        created_at=q.created_at,
        updated_at=q.updated_at,
        options=[{"id": o.id, "content": o.content, "is_correct": o.is_correct} for o in options],
        knowledge_points=knowledge_points,
        tags=tags
    )

@router.post("/questions", response_model=ApiResponse)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    q = Question(
        content=question.content,
        question_type=question.question_type,
        difficulty=question.difficulty,
        status=question.status,
        source=question.source,
        answer=question.answer,
        explanation=question.explanation,
        creator=question.creator
    )
    db.add(q)
    db.flush()
    
    for idx, opt in enumerate(question.options):
        option = Option(
            question_id=q.id,
            content=opt.content,
            is_correct=opt.is_correct,
            order_index=idx
        )
        db.add(option)
    
    for kp_input in question.knowledge_point_ids:
        if isinstance(kp_input, int):
            kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == kp_input).first()
        else:
            kp = db.query(KnowledgePoint).filter(KnowledgePoint.name == kp_input).first()
            if not kp:
                kp = KnowledgePoint(name=kp_input, level=1)
                db.add(kp)
                db.flush()
        if kp:
            q.knowledge_points.append(kp)
    
    for tag_name in question.tag_names:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()
        q.tags.append(tag)
    
    db.commit()
    return ApiResponse(message="创建成功", data={"id": q.id})

@router.put("/questions/{question_id}", response_model=ApiResponse)
def update_question(question_id: int, question: QuestionUpdate, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    update_data = question.dict(exclude_unset=True)
    
    if "options" in update_data:
        db.query(Option).filter(Option.question_id == q.id).delete()
        for idx, opt in enumerate(update_data["options"]):
            option = Option(
                question_id=q.id,
                content=opt["content"],
                is_correct=opt["is_correct"],
                order_index=idx
            )
            db.add(option)
        del update_data["options"]
    
    if "knowledge_point_ids" in update_data:
        q.knowledge_points = []
        for kp_id in update_data["knowledge_point_ids"]:
            kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == kp_id).first()
            if kp:
                q.knowledge_points.append(kp)
        del update_data["knowledge_point_ids"]
    
    if "tag_names" in update_data:
        q.tags = []
        for tag_name in update_data["tag_names"]:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
            q.tags.append(tag)
        del update_data["tag_names"]
    
    for key, value in update_data.items():
        setattr(q, key, value)
    
    q.updated_at = datetime.utcnow()
    db.commit()
    return ApiResponse(message="更新成功")

@router.delete("/questions/{question_id}", response_model=ApiResponse)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    db.delete(q)
    db.commit()
    return ApiResponse(message="删除成功")

@router.post("/questions/{question_id}/review", response_model=ApiResponse)
def review_question(question_id: int, reviewer: str = "系统", db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    q.status = "已审核"
    q.reviewer = reviewer
    q.updated_at = datetime.utcnow()
    db.commit()
    return ApiResponse(message="审核成功")

@router.post("/questions/batch-review", response_model=ApiResponse)
def batch_review(ids: List[int], reviewer: str = "系统", db: Session = Depends(get_db)):
    db.query(Question).filter(Question.id.in_(ids)).update(
        {"status": "已审核", "reviewer": reviewer, "updated_at": datetime.utcnow()},
        synchronize_session=False
    )
    db.commit()
    return ApiResponse(message=f"已审核 {len(ids)} 题")

@router.post("/questions/batch-draft", response_model=ApiResponse)
def batch_draft(ids: List[int], db: Session = Depends(get_db)):
    db.query(Question).filter(Question.id.in_(ids)).update(
        {"status": "草稿", "updated_at": datetime.utcnow()},
        synchronize_session=False
    )
    db.commit()
    return ApiResponse(message=f"已设为草稿 {len(ids)} 题")

@router.post("/questions/batch-delete", response_model=ApiResponse)
def batch_delete(ids: List[int], db: Session = Depends(get_db)):
    db.query(Question).filter(Question.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return ApiResponse(message=f"已删除 {len(ids)} 题")

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Question).count()
    reviewed = db.query(Question).filter(Question.status == "已审核").count()
    pending = db.query(Question).filter(Question.status == "待审核").count()
    draft = db.query(Question).filter(Question.status == "草稿").count()
    
    type_stats = []
    for t in ["单选", "多选", "判断", "填空", "主观"]:
        count = db.query(Question).filter(Question.question_type == t).count()
        type_stats.append({"type": t, "count": count})
    
    return {
        "total": total,
        "reviewed": reviewed,
        "pending": pending,
        "draft": draft,
        "type_stats": type_stats
    }

@router.post("/generation-tasks", response_model=ApiResponse)
def create_generation_task(task: GenerationTaskCreate, db: Session = Depends(get_db)):
    new_task = GenerationTask(
        knowledge_input=task.knowledge_input,
        knowledge_ids=",".join(map(str, task.knowledge_ids)) if task.knowledge_ids else None,
        question_types=",".join(task.question_types) if task.question_types else "",
        type_counts=json.dumps(task.type_counts) if task.type_counts else None,
        difficulty_config=json.dumps(task.difficulty_config) if task.difficulty_config else None,
        distractor_list=json.dumps(task.distractor_list) if task.distractor_list else None,
        preference_list=json.dumps(task.preference_list) if task.preference_list else None,
        custom_requirement=task.custom_requirement,
        question_count=task.total_count,
        status="pending"
    )
    db.add(new_task)
    db.commit()
    return ApiResponse(message="任务创建成功", data={"taskId": new_task.id})

@router.get("/generation-tasks/{task_id}/questions", response_model=List[GeneratedQuestionResponse])
def get_generated_questions(task_id: int, db: Session = Depends(get_db)):
    questions = db.query(GeneratedQuestion).filter(GeneratedQuestion.task_id == task_id).all()
    
    result = []
    for q in questions:
        options = json.loads(q.options_json) if q.options_json else []
        distractor_reasons = json.loads(q.distractor_reasons) if q.distractor_reasons else []
        knowledge_points = q.knowledge_points.split(",") if q.knowledge_points else []
        
        result.append(GeneratedQuestionResponse(
            id=q.id,
            content=q.content,
            question_type=q.question_type,
            difficulty=q.difficulty,
            answer=q.answer,
            explanation=q.explanation,
            design_reason=q.design_reason,
            distractor_reasons=distractor_reasons,
            knowledge_points=knowledge_points,
            options=options,
            is_selected=q.is_selected,
            is_draft=q.is_draft,
            is_discarded=q.is_discarded
        ))
    
    return result

@router.post("/generation-tasks/{task_id}/adopt", response_model=ApiResponse)
def adopt_generated_questions(task_id: int, question_ids: List[int], db: Session = Depends(get_db)):
    count = 0
    for qid in question_ids:
        gq = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == qid, GeneratedQuestion.task_id == task_id).first()
        if gq:
            q = Question(
                content=gq.content,
                question_type=gq.question_type,
                difficulty=gq.difficulty,
                status="草稿" if gq.is_draft else "已审核",
                source="AI生成",
                answer=gq.answer,
                explanation=gq.explanation,
                design_reason=gq.design_reason,
                difficulty_reason=gq.difficulty_reason,
                distractor_reasons=gq.distractor_reasons,
                creator="AI"
            )
            db.add(q)
            db.flush()
            
            if gq.options_json:
                options = json.loads(gq.options_json)
                for idx, opt in enumerate(options):
                    option = Option(
                        question_id=q.id,
                        content=opt.get("content", ""),
                        is_correct=opt.get("is_correct", False),
                        order_index=idx
                    )
                    db.add(option)
            
            db.delete(gq)
            count += 1
    
    db.commit()
    return ApiResponse(message=f"已入库 {count} 题")
