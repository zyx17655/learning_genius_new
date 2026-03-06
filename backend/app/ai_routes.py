from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json
import logging

from app.database import get_db
from app.models import GenerationTask, GeneratedQuestion, Question, Option
from app.ai_service import generate_questions_with_kimi
from app.knowledge_service import KnowledgeService

logger = logging.getLogger(__name__)
router = APIRouter()

class GenerateRequest(BaseModel):
    knowledge_input: Optional[str] = ""
    knowledge_ids: List[int] = []
    knowledge_category: Optional[str] = None
    question_types: List[str] = []
    type_counts: dict = {}
    difficulty_config: dict = {}
    distractor_list: List[dict] = []
    preference_list: List[dict] = []
    custom_requirement: Optional[str] = ""
    total_count: int = 0
    rule_id: Optional[int] = None

@router.post("/generate")
async def generate_questions(request: GenerateRequest, db: Session = Depends(get_db)):
    logger.info(f"=== 收到AI生成请求 ===")
    logger.info(f"knowledge_input: {request.knowledge_input}")
    logger.info(f"question_types: {request.question_types}")
    logger.info(f"type_counts: {request.type_counts}")
    logger.info(f"total_count: {request.total_count}")
    logger.info(f"rule_id: {request.rule_id}")
    
    rule = None
    if request.rule_id:
        from app.models import QuestionRule
        rule = db.query(QuestionRule).filter(QuestionRule.id == request.rule_id).first()
        if rule:
            logger.info(f"使用规则: {rule.name}")
        else:
            logger.warning(f"规则ID {request.rule_id} 不存在")
    
    task = GenerationTask(
        knowledge_input=request.knowledge_input,
        knowledge_ids=",".join(map(str, request.knowledge_ids)) if request.knowledge_ids else None,
        question_types=",".join(request.question_types) if request.question_types else "",
        type_counts=json.dumps(request.type_counts),
        difficulty_config=json.dumps(request.difficulty_config),
        distractor_list=json.dumps(request.distractor_list),
        preference_list=json.dumps(request.preference_list),
        custom_requirement=request.custom_requirement,
        question_count=request.total_count,
        status="running"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info(f"创建任务: task_id={task.id}")
    
    try:
        knowledge_chunks = None
        ks = KnowledgeService(db)
        
        if request.knowledge_ids and len(request.knowledge_ids) > 0:
            from app.models import KnowledgeChunk
            chunks = db.query(KnowledgeChunk).filter(KnowledgeChunk.id.in_(request.knowledge_ids)).all()
            knowledge_chunks = [{
                "id": c.id,
                "title": c.title,
                "content": c.content,
                "category": c.category,
                "char_count": c.char_count
            } for c in chunks]
            logger.info(f"按ID检索知识: {request.knowledge_ids}, 结果数: {len(knowledge_chunks)}")
        elif request.knowledge_category:
            knowledge_chunks = ks.get_chunks_by_category(request.knowledge_category)
            logger.info(f"按分类检索知识: {request.knowledge_category}, 结果数: {len(knowledge_chunks) if knowledge_chunks else 0}")
        elif request.knowledge_input:
            knowledge_chunks = ks.search_chunks(query=request.knowledge_input)
            logger.info(f"按关键词检索知识: {request.knowledge_input}, 结果数: {len(knowledge_chunks) if knowledge_chunks else 0}")
        
        logger.info(f"调用Kimi API生成题目...")
        questions = generate_questions_with_kimi(
            knowledge_input=request.knowledge_input,
            question_types=request.question_types,
            type_counts=request.type_counts,
            difficulty_config=request.difficulty_config,
            distractor_list=request.distractor_list,
            preference_list=request.preference_list,
            custom_requirement=request.custom_requirement,
            knowledge_chunks=knowledge_chunks,
            task_id=task.id,
            db=db,
            rule=rule
        )
        logger.info(f"Kimi API返回 {len(questions)} 道题目")
        
        for q in questions:
            kp = q.get("knowledge_points", [])
            if isinstance(kp, list):
                kp_str = ",".join(str(k) for k in kp)
            elif isinstance(kp, str):
                kp_str = kp
            else:
                kp_str = str(kp) if kp else ""
            
            gq = GeneratedQuestion(
                task_id=task.id,
                content=q.get("content", ""),
                question_type=q.get("question_type", "单选"),
                difficulty=q.get("difficulty", "L2"),
                answer=q.get("answer", ""),
                explanation=q.get("explanation", ""),
                design_reason=q.get("design_reason", ""),
                difficulty_reason=q.get("difficulty_reason", ""),
                distractor_reasons=json.dumps(q.get("distractor_reasons", [])),
                knowledge_points=kp_str,
                options_json=json.dumps(q.get("options", [])),
                is_selected=False,
                is_draft=False,
                is_discarded=False
            )
            db.add(gq)
        
        task.status = "completed"
        task.result = json.dumps({"count": len(questions)})
        db.commit()
        
        return {
            "code": 0,
            "message": "生成成功",
            "data": {
                "task_id": task.id,
                "count": len(questions)
            }
        }
    except Exception as e:
        task.status = "failed"
        task.result = json.dumps({"error": str(e)})
        db.commit()
        return {
            "code": 1,
            "message": f"生成失败: {str(e)}",
            "data": None
        }

@router.get("/tasks/{task_id}/questions")
def get_generated_questions(task_id: int, db: Session = Depends(get_db)):
    questions = db.query(GeneratedQuestion).filter(GeneratedQuestion.task_id == task_id).all()
    
    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "content": q.content,
            "question_type": q.question_type,
            "difficulty": q.difficulty,
            "answer": q.answer,
            "explanation": q.explanation,
            "design_reason": q.design_reason,
            "difficulty_reason": q.difficulty_reason,
            "distractor_reasons": json.loads(q.distractor_reasons) if q.distractor_reasons else [],
            "knowledge_points": q.knowledge_points.split(",") if q.knowledge_points else [],
            "options": json.loads(q.options_json) if q.options_json else [],
            "is_selected": q.is_selected,
            "is_draft": q.is_draft,
            "is_discarded": q.is_discarded
        })
    
    return {"code": 0, "data": result}

@router.post("/tasks/{task_id}/adopt")
def adopt_questions(task_id: int, question_ids: List[int], db: Session = Depends(get_db)):
    count = 0
    for qid in question_ids:
        gq = db.query(GeneratedQuestion).filter(
            GeneratedQuestion.id == qid,
            GeneratedQuestion.task_id == task_id
        ).first()
        
        if gq and not gq.is_discarded:
            question = Question(
                content=gq.content,
                question_type=gq.question_type,
                difficulty=gq.difficulty,
                status="草稿" if gq.is_draft else "已审核",
                source="AI生成",
                answer=gq.answer,
                explanation=gq.explanation,
                creator="AI"
            )
            db.add(question)
            db.flush()
            
            if gq.options_json:
                options = json.loads(gq.options_json)
                for idx, opt in enumerate(options):
                    option = Option(
                        question_id=question.id,
                        content=opt.get("content", ""),
                        is_correct=opt.get("is_correct", False),
                        order_index=idx
                    )
                    db.add(option)
            
            db.delete(gq)
            count += 1
    
    db.commit()
    return {"code": 0, "message": f"已入库 {count} 题"}

@router.post("/questions/{question_id}/toggle-draft")
def toggle_draft(question_id: int, db: Session = Depends(get_db)):
    q = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == question_id).first()
    if q:
        q.is_draft = not q.is_draft
        if q.is_draft:
            q.is_selected = False
        db.commit()
        return {"code": 0, "message": "操作成功"}
    return {"code": 1, "message": "题目不存在"}

@router.post("/questions/{question_id}/toggle-discard")
def toggle_discard(question_id: int, db: Session = Depends(get_db)):
    q = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == question_id).first()
    if q:
        q.is_discarded = not q.is_discarded
        if q.is_discarded:
            q.is_selected = False
            q.is_draft = False
        db.commit()
        return {"code": 0, "message": "操作成功"}
    return {"code": 1, "message": "题目不存在"}

@router.put("/questions/{question_id}")
def update_generated_question(question_id: int, data: dict, db: Session = Depends(get_db)):
    q = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == question_id).first()
    if q:
        q.content = data.get("content", q.content)
        q.answer = data.get("answer", q.answer)
        q.explanation = data.get("explanation", q.explanation)
        if "options" in data:
            q.options_json = json.dumps(data["options"])
        db.commit()
        return {"code": 0, "message": "更新成功"}
    return {"code": 1, "message": "题目不存在"}
