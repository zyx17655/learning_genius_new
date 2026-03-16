from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
import json
import logging
import asyncio
from datetime import datetime

from app.database import get_db
from app.models import GenerationTask, GeneratedQuestion, Question, Option
from app.ai_service import generate_questions_with_kimi, generate_and_verify_question
from app.knowledge_service import KnowledgeService
from app.schemas import ApiResponse

logger = logging.getLogger(__name__)
router = APIRouter()


# ==================== 原有接口保持不变 ====================

class GenerateRequest(BaseModel):
    knowledge_input: Optional[str] = ""
    knowledge_ids: List[int] = []
    knowledge_categories: List[str] = []
    question_types: List[str] = []
    type_counts: dict = {}
    difficulty_config: dict = {}
    distractor_list: List[dict] = []
    preference_list: List[dict] = []
    custom_requirement: Optional[str] = ""
    total_count: int = 0
    rule_id: Optional[int] = None


@router.post("/generate")
async def generate_questions(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    异步生成题目（原有接口，保持兼容）
    """
    logger.info(f"=== 收到AI生成请求 ===")
    logger.info(f"知识范围: {request.knowledge_input or request.knowledge_categories}")
    logger.info(f"题型: {request.question_types}, 数量: {request.type_counts}")
    logger.info(f"总题数: {request.total_count}")
    
    # 创建任务记录
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
        status="pending",
        result=json.dumps({
            "completed_count": 0,
            "failed_count": 0,
            "current_question": 0,
            "message": "任务已创建，等待执行"
        })
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info(f"创建生成任务: task_id={task.id}")
    
    # 启动后台任务
    background_tasks.add_task(
        run_generation_task,
        task.id,
        request
    )
    
    return {
        "code": 0,
        "message": "任务已创建",
        "data": {
            "task_id": task.id,
            "status": "pending",
            "count": request.total_count
        }
    }


async def run_generation_task(task_id: int, request: GenerateRequest):
    """
    后台执行生成任务（原有逻辑）
    """
    from app.database import SessionLocal
    from app.models import QuestionRule
    
    db = SessionLocal()
    
    try:
        task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
        if not task:
            return
        
        task.status = "running"
        db.commit()
        
        # 获取规则
        default_rule = db.query(QuestionRule).filter(QuestionRule.is_default == True).first()
        custom_rule = None
        if request.rule_id:
            custom_rule = db.query(QuestionRule).filter(QuestionRule.id == request.rule_id).first()
        
        # 获取知识块
        knowledge_chunks = None
        if request.knowledge_ids:
            from app.models import KnowledgeChunk
            chunks = db.query(KnowledgeChunk).filter(KnowledgeChunk.id.in_(request.knowledge_ids)).all()
            knowledge_chunks = [{"id": c.id, "title": c.title, "content": c.content, "category": c.category} for c in chunks]
        elif request.knowledge_categories:
            from app.models import KnowledgeChunk
            chunks = db.query(KnowledgeChunk).filter(KnowledgeChunk.category.in_(request.knowledge_categories)).all()
            knowledge_chunks = [{"id": c.id, "title": c.title, "content": c.content, "category": c.category} for c in chunks]
        
        # 生成题目
        questions = generate_questions_with_kimi(
            knowledge_input=request.knowledge_input,
            question_types=request.question_types,
            type_counts=request.type_counts,
            difficulty_config=request.difficulty_config,
            distractor_list=request.distractor_list,
            preference_list=request.preference_list,
            custom_requirement=request.custom_requirement,
            knowledge_chunks=knowledge_chunks,
            default_rule=default_rule,
            custom_rule=custom_rule
        )
        
        # 保存生成的题目
        for q in questions:
            gq = GeneratedQuestion(
                task_id=task_id,
                content=q.get("content", ""),
                question_type=q.get("question_type", "单选"),
                difficulty=q.get("difficulty", "中等"),
                answer=q.get("answer", ""),
                explanation=q.get("explanation", ""),
                design_reason=q.get("design_reason", ""),
                difficulty_reason=q.get("difficulty_reason", ""),
                distractor_reasons=json.dumps(q.get("distractor_reasons", [])),
                knowledge_points=",".join(q.get("knowledge_points", [])) if isinstance(q.get("knowledge_points"), list) else str(q.get("knowledge_points", "")),
                options_json=json.dumps(q.get("options", [])),
                is_selected=False,
                is_draft=False,
                is_discarded=False
            )
            db.add(gq)
        
        task.status = "completed"
        task.completed_at = datetime.now()
        task.result = json.dumps({
            "completed_count": len(questions),
            "failed_count": 0,
            "message": f"生成完成，成功 {len(questions)} 题"
        })
        db.commit()
        
    except Exception as e:
        logger.error(f"任务执行失败: {e}")
        task.status = "failed"
        task.result = json.dumps({"error": str(e), "message": "任务执行失败"})
        db.commit()
    finally:
        db.close()


@router.get("/tasks/{task_id}/questions")
def get_task_questions(task_id: int, db: Session = Depends(get_db)):
    """
    获取任务生成的题目
    """
    questions = db.query(GeneratedQuestion).filter(
        GeneratedQuestion.task_id == task_id
    ).all()
    
    return {
        "code": 0,
        "data": [
            {
                "id": q.id,
                "content": q.content,
                "question_type": q.question_type,
                "difficulty": q.difficulty,
                "answer": q.answer,
                "explanation": q.explanation,
                "design_reason": q.design_reason,
                "difficulty_reason": q.difficulty_reason,
                "distractor_reasons": json.loads(q.distractor_reasons) if q.distractor_reasons else [],
                "knowledge_points": q.knowledge_points,
                "options": json.loads(q.options_json) if q.options_json else [],
                "is_selected": q.is_selected,
                "is_draft": q.is_draft,
                "is_discarded": q.is_discarded
            }
            for q in questions
        ]
    }


@router.post("/questions/batch-import")
def batch_import_questions(data: dict, db: Session = Depends(get_db)):
    """
    批量导入题目到题库
    """
    from app.models import KnowledgePoint
    from sqlalchemy import text
    
    ids = data.get("ids", [])
    count = 0
    
    for gid in ids:
        gq = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == gid).first()
        if not gq or gq.is_discarded:
            continue
        
        # 创建正式题目
        q = Question(
            content=gq.content,
            question_type=gq.question_type,
            difficulty=gq.difficulty,
            answer=gq.answer,
            explanation=gq.explanation,
            design_reason=gq.design_reason,
            difficulty_reason=gq.difficulty_reason,
            distractor_reasons=gq.distractor_reasons,
            knowledge_points=gq.knowledge_points,
            status="已审核" if gq.is_selected else "草稿"
        )
        db.add(q)
        db.flush()
        
        # 添加选项
        options = json.loads(gq.options_json) if gq.options_json else []
        for opt in options:
            o = Option(
                question_id=q.id,
                content=opt.get("content", ""),
                is_correct=opt.get("is_correct", False)
            )
            db.add(o)
        
        # 关联知识点
        if gq.knowledge_points:
            kp_names = [k.strip() for k in gq.knowledge_points.split(",") if k.strip()]
            for kp_name in kp_names:
                kp = db.query(KnowledgePoint).filter(KnowledgePoint.name == kp_name).first()
                if kp:
                    db.execute(text("""
                        INSERT INTO question_knowledge (question_id, knowledge_point_id)
                        VALUES (:question_id, :knowledge_point_id)
                    """), {
                        "question_id": q.id,
                        "knowledge_point_id": kp.id
                    })
        
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


# ==================== 异步生成与验证接口 ====================

class GenerateWithVerificationRequest(BaseModel):
    """带验证的生成请求"""
    knowledge_input: Optional[str] = ""
    knowledge_ids: List[int] = []
    knowledge_categories: List[str] = []
    question_types: List[str] = []
    type_counts: dict = {}
    difficulty_config: dict = {}
    distractor_list: List[dict] = []
    preference_list: List[dict] = []
    custom_requirement: Optional[str] = ""
    total_count: int = 0
    rule_id: Optional[int] = None
    enable_verification: bool = True  # 是否启用验证
    max_generation_retries: int = 3  # 每道题最大重试次数


@router.post("/generate-with-verification")
async def generate_questions_with_verification(
    request: GenerateWithVerificationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    异步生成题目并验证
    
    流程：
    1. 创建任务，立即返回任务ID
    2. 后台异步执行生成和验证
    3. 每道题验证不通过会重试
    4. 前端通过 /tasks/{task_id}/status 查询进度
    """
    logger.info(f"=== 收到带验证的AI生成请求 ===")
    logger.info(f"知识范围: {request.knowledge_input or request.knowledge_categories}")
    logger.info(f"题型: {request.question_types}, 数量: {request.type_counts}")
    logger.info(f"总题数: {request.total_count}")
    logger.info(f"启用验证: {request.enable_verification}")
    
    # 创建任务记录
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
        status="pending",  # 初始状态为 pending
        result=json.dumps({
            "completed_count": 0,
            "failed_count": 0,
            "current_question": 0,
            "verification_enabled": request.enable_verification,
            "message": "任务已创建，等待执行"
        })
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info(f"创建生成任务: task_id={task.id}")
    
    # 启动后台任务
    background_tasks.add_task(
        run_generation_with_verification,
        task.id,
        request
    )
    
    return {
        "code": 0,
        "message": "任务已创建",
        "data": {
            "task_id": task.id,
            "status": "pending",
            "total_count": request.total_count
        }
    }


async def run_generation_with_verification(task_id: int, request: GenerateWithVerificationRequest):
    """
    后台执行生成和验证任务
    """
    from app.database import SessionLocal
    from app.models import QuestionRule
    import time
    
    db = SessionLocal()
    task_start_time = time.time()
    
    logger.info(f"=" * 80)
    logger.info(f"【异步任务启动】task_id={task_id}")
    logger.info(f"=" * 80)
    logger.info(f"任务配置:")
    logger.info(f"  - 知识范围: {request.knowledge_input or request.knowledge_categories}")
    logger.info(f"  - 题型: {request.question_types}")
    logger.info(f"  - 题型数量: {request.type_counts}")
    logger.info(f"  - 难度配置: {request.difficulty_config}")
    logger.info(f"  - 总题数: {request.total_count}")
    logger.info(f"  - 启用验证: {request.enable_verification}")
    logger.info(f"  - 最大重试次数: {request.max_generation_retries}")
    
    try:
        # 更新任务状态为运行中
        task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
        if not task:
            logger.error(f"【任务错误】任务不存在: task_id={task_id}")
            return
        
        task.status = "running"
        task.result = json.dumps({
            "completed_count": 0,
            "failed_count": 0,
            "current_question": 0,
            "verification_enabled": request.enable_verification,
            "message": "开始生成题目"
        })
        db.commit()
        logger.info(f"【任务状态】task_id={task_id} 状态更新为: running")
        
        # 获取规则
        default_rule = db.query(QuestionRule).filter(QuestionRule.is_default == True).first()
        custom_rule = None
        if request.rule_id:
            custom_rule = db.query(QuestionRule).filter(QuestionRule.id == request.rule_id).first()
            logger.info(f"【规则配置】使用自定义规则: {custom_rule.name}")
        elif default_rule:
            logger.info(f"【规则配置】使用默认规则: {default_rule.name}")
        
        # 获取知识块
        knowledge_chunks = None
        knowledge_context = ""
        
        if request.knowledge_ids:
            from app.models import KnowledgeChunk
            chunks = db.query(KnowledgeChunk).filter(KnowledgeChunk.id.in_(request.knowledge_ids)).all()
            knowledge_chunks = [{
                "id": c.id,
                "title": c.title,
                "content": c.content,
                "category": c.category
            } for c in chunks]
            knowledge_context = "\n".join([c.content for c in chunks[:3]])
            logger.info(f"【知识检索】按ID检索到 {len(knowledge_chunks)} 条知识块")
        elif request.knowledge_categories:
            from app.models import KnowledgeChunk
            chunks = db.query(KnowledgeChunk).filter(KnowledgeChunk.category.in_(request.knowledge_categories)).all()
            knowledge_chunks = [{
                "id": c.id,
                "title": c.title,
                "content": c.content,
                "category": c.category
            } for c in chunks]
            knowledge_context = "\n".join([c.content for c in chunks[:3]])
            logger.info(f"【知识检索】按分类检索到 {len(knowledge_chunks)} 条知识块")
        else:
            logger.info(f"【知识检索】未指定知识范围")
        
        # 准备批量生成参数
        total_questions = request.total_count
        logger.info(f"【生成计划】task_id={task_id} 需要生成 {total_questions} 道题目")
        logger.info(f"=" * 80)
        
        completed_count = 0
        failed_count = 0
        all_generated_questions = []
        
        # 批量生成所有题目（一次API调用）
        batch_start_time = time.time()
        logger.info(f"【批量生成】开始生成 {total_questions} 道题目...")
        
        # 更新任务状态 - 开始生成（进度 0%）
        task.result = json.dumps({
            "completed_count": 0,
            "failed_count": 0,
            "current_question": 0,
            "total_questions": total_questions * 2,  # 生成+验证，总共有2倍进度
            "verification_enabled": request.enable_verification,
            "message": f"正在批量生成 {total_questions} 道题目..."
        })
        db.commit()
        
        # 添加短暂延迟，确保前端能看到初始状态
        await asyncio.sleep(0.5)
        
        try:
            # 一次性批量生成所有题目
            from app.ai_service import generate_questions_with_kimi
            all_questions = generate_questions_with_kimi(
                knowledge_input=request.knowledge_input,
                question_types=request.question_types,
                type_counts=request.type_counts,
                difficulty_config=request.difficulty_config,
                distractor_list=request.distractor_list,
                preference_list=request.preference_list,
                custom_requirement=request.custom_requirement,
                knowledge_chunks=knowledge_chunks,
                default_rule=default_rule,
                custom_rule=custom_rule
            )
            
            batch_time = time.time() - batch_start_time
            logger.info(f"【批量生成完成】生成 {len(all_questions)} 道题目，耗时 {batch_time:.2f} 秒")
            
            # 更新生成完成状态（进度 50%）
            task.result = json.dumps({
                "completed_count": 0,
                "failed_count": 0,
                "current_question": total_questions,  # 生成阶段占一半进度
                "total_questions": total_questions * 2,  # 总进度是生成+验证
                "verification_enabled": request.enable_verification,
                "message": f"批量生成完成，共 {len(all_questions)} 题，开始验证..."
            })
            db.commit()
            
            # 添加短暂延迟，让前端看到生成完成状态
            await asyncio.sleep(0.5)
            
            if not all_questions:
                logger.error("批量生成失败，无题目返回")
                raise Exception("批量生成失败")
            
            # 如果需要验证，逐题验证
            if request.enable_verification:
                logger.info(f"【批量验证】开始验证 {len(all_questions)} 道题目...")
                
                for i, question in enumerate(all_questions):
                    current_num = i + 1
                    question_start_time = time.time()
                    
                    logger.info(f"")
                    logger.info(f"【第 {current_num}/{len(all_questions)} 题】开始验证")
                    logger.info(f"  - 题型: {question.get('question_type', '未知')}")
                    logger.info(f"  - 难度: {question.get('difficulty', '未知')}")
                    logger.info(f"  - 题目: {question.get('content', '')[:60]}...")
                    
                    # 更新进度（验证阶段从50%开始）
                    verification_progress = total_questions + current_num  # 生成占50%，验证每完成一题加1
                    task.result = json.dumps({
                        "completed_count": completed_count,
                        "failed_count": failed_count,
                        "current_question": verification_progress,
                        "total_questions": total_questions * 2,  # 总进度是生成+验证
                        "verification_enabled": request.enable_verification,
                        "message": f"正在验证第 {current_num}/{len(all_questions)} 题..."
                    })
                    db.commit()
                    
                    try:
                        # 验证题目
                        from app.ai_service import verify_question_with_kimi
                        verification = verify_question_with_kimi(question, knowledge_context)
                        
                        question_time = time.time() - question_start_time
                        
                        if verification.get("is_valid"):
                            logger.info(f"  ✓ 验证通过")
                            logger.info(f"    - 验证得分: {verification.get('total_score', 'N/A')}")
                            logger.info(f"    - 耗时: {question_time:.2f} 秒")
                            all_generated_questions.append(question)
                            completed_count += 1
                        else:
                            # 验证不通过，尝试重新生成这道题
                            logger.warning(f"  ⚠ 验证未通过，得分: {verification.get('total_score', 'N/A')}")
                            logger.warning(f"    - 问题: {verification.get('issues', [])}")
                            
                            # 重试生成
                            retry_success = False
                            for retry in range(request.max_generation_retries):
                                logger.info(f"    - 第 {retry + 1} 次重试生成...")
                                
                                retry_questions = generate_questions_with_kimi(
                                    knowledge_input=request.knowledge_input,
                                    question_types=[question.get('question_type', '单选')],
                                    type_counts={question.get('question_type', '单选'): 1},
                                    difficulty_config={question.get('difficulty', '中等'): {"count": 1}},
                                    distractor_list=request.distractor_list,
                                    preference_list=request.preference_list,
                                    custom_requirement=request.custom_requirement + f"\n\n改进建议：{verification.get('suggestions', '')}",
                                    knowledge_chunks=knowledge_chunks,
                                    default_rule=default_rule,
                                    custom_rule=custom_rule
                                )
                                
                                if retry_questions:
                                    retry_question = retry_questions[0]
                                    retry_verification = verify_question_with_kimi(retry_question, knowledge_context)
                                    
                                    if retry_verification.get("is_valid"):
                                        logger.info(f"    ✓ 重试成功，验证通过")
                                        all_generated_questions.append(retry_question)
                                        completed_count += 1
                                        retry_success = True
                                        break
                                    else:
                                        logger.warning(f"    ✗ 重试仍未通过")
                            
                            if not retry_success:
                                logger.warning(f"  ✗ 重试 {request.max_generation_retries} 次后仍未通过，使用原题")
                                all_generated_questions.append(question)
                                failed_count += 1
                        
                        # 打印进度
                        progress = (current_num / len(all_questions)) * 100
                        logger.info(f"【验证进度】{current_num}/{len(all_questions)} ({progress:.1f}%) | 成功: {completed_count} | 失败: {failed_count}")
                        
                    except Exception as e:
                        logger.error(f"  ✗ 验证异常: {str(e)}")
                        all_generated_questions.append(question)
                        failed_count += 1
                    
                    db.commit()
            else:
                # 不验证，直接使用所有生成的题目
                all_generated_questions = all_questions
                completed_count = len(all_questions)
                logger.info(f"【跳过验证】直接使用 {len(all_questions)} 道题目")
            
            # 保存所有题目到数据库
            logger.info(f"【保存题目】开始保存 {len(all_generated_questions)} 道题目到数据库...")
            
            for i, question in enumerate(all_generated_questions):
                try:
                    kp = question.get("knowledge_points", [])
                    if isinstance(kp, list):
                        kp_str = ",".join(str(k) for k in kp if k is not None)
                    else:
                        kp_str = str(kp) if kp else ""
                    
                    answer = question.get("answer", "")
                    if isinstance(answer, list):
                        answer = ",".join(str(a) for a in answer)
                    
                    gq = GeneratedQuestion(
                        task_id=task_id,
                        content=question.get("content", ""),
                        question_type=question.get("question_type", "单选"),
                        difficulty=question.get("difficulty", "中等"),
                        answer=answer,
                        explanation=question.get("explanation", ""),
                        design_reason=question.get("design_reason", ""),
                        difficulty_reason=question.get("difficulty_reason", ""),
                        distractor_reasons=json.dumps(question.get("distractor_reasons", [])),
                        knowledge_points=kp_str,
                        options_json=json.dumps(question.get("options", [])),
                        is_selected=False,
                        is_draft=False,
                        is_discarded=False
                    )
                    db.add(gq)
                    
                    if (i + 1) % 5 == 0:
                        logger.info(f"  已保存 {i + 1}/{len(all_generated_questions)} 道题目")
                    
                except Exception as e:
                    logger.error(f"  ✗ 保存第 {i + 1} 题失败: {str(e)}")
            
            db.commit()
            logger.info(f"【保存完成】成功保存 {len(all_generated_questions)} 道题目")
            
        except Exception as e:
            logger.error(f"【批量生成异常】: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            failed_count = total_questions
        
        # 任务完成
        task_end_time = time.time()
        total_time = task_end_time - task_start_time
        
        task.status = "completed"
        task.completed_at = datetime.now()
        task.result = json.dumps({
            "completed_count": completed_count,
            "failed_count": failed_count,
            "current_question": total_questions * 2,  # 进度 100%
            "total_questions": total_questions * 2,  # 总进度是生成+验证
            "verification_enabled": request.enable_verification,
            "message": f"生成完成，成功 {completed_count} 题，失败 {failed_count} 题"
        })
        db.commit()
        
        logger.info(f"")
        logger.info(f"=" * 80)
        logger.info(f"【任务完成】task_id={task_id}")
        logger.info(f"=" * 80)
        logger.info(f"统计信息:")
        logger.info(f"  - 总题数: {total_questions}")
        logger.info(f"  - 成功: {completed_count} 题")
        logger.info(f"  - 失败: {failed_count} 题")
        logger.info(f"  - 成功率: {(completed_count/total_questions*100):.1f}%")
        logger.info(f"  - 总耗时: {total_time:.2f} 秒")
        logger.info(f"  - 平均每题耗时: {total_time/total_questions:.2f} 秒")
        logger.info(f"=" * 80)
        
    except Exception as e:
        task_end_time = time.time()
        total_time = task_end_time - task_start_time
        
        logger.error(f"")
        logger.error(f"=" * 80)
        logger.error(f"【任务失败】task_id={task_id}")
        logger.error(f"=" * 80)
        logger.error(f"异常信息: {str(e)}")
        logger.error(f"执行时间: {total_time:.2f} 秒")
        import traceback
        logger.error(traceback.format_exc())
        logger.error(f"=" * 80)
        
        task.status = "failed"
        task.result = json.dumps({
            "error": str(e),
            "message": "任务执行失败"
        })
        db.commit()
    finally:
        db.close()
        logger.info(f"【数据库】task_id={task_id} 数据库连接已关闭")


@router.get("/tasks/{task_id}/status")
def get_task_status(task_id: int, db: Session = Depends(get_db)):
    """
    获取任务状态和进度
    """
    task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
    
    if not task:
        return {"code": 1, "message": "任务不存在"}
    
    # 解析结果
    try:
        result = json.loads(task.result) if task.result else {}
    except:
        result = {}
    
    # 查询已生成的题目
    generated_count = db.query(GeneratedQuestion).filter(
        GeneratedQuestion.task_id == task_id
    ).count()
    
    return {
        "code": 0,
        "data": {
            "task_id": task.id,
            "status": task.status,  # pending/running/completed/failed
            "total_count": task.question_count,
            "total_questions": result.get("total_questions", task.question_count),  # 新的进度总基数
            "generated_count": generated_count,
            "completed_count": result.get("completed_count", 0),
            "failed_count": result.get("failed_count", 0),
            "current_question": result.get("current_question", 0),
            "message": result.get("message", ""),
            "verification_enabled": result.get("verification_enabled", False),
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
    }


@router.post("/tasks/{task_id}/adopt", response_model=ApiResponse)
def adopt_generated_questions(task_id: int, question_ids: List[int], db: Session = Depends(get_db)):
    """
    将生成的题目入库到正式题库
    """
    from sqlalchemy import text
    from app.models import KnowledgePoint
    
    count = 0
    
    for qid in question_ids:
        gq = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == qid, GeneratedQuestion.task_id == task_id).first()
        if gq:
            # 使用原生 SQL 插入到 questions 表，确保所有字段都被正确保存
            result = db.execute(text("""
                INSERT INTO questions (
                    content, question_type, difficulty, status, source,
                    answer, explanation, design_reason, difficulty_reason,
                    distractor_reasons, generated_question_id, creator,
                    created_at, updated_at
                ) VALUES (
                    :content, :question_type, :difficulty, :status, :source,
                    :answer, :explanation, :design_reason, :difficulty_reason,
                    :distractor_reasons, :generated_question_id, :creator,
                    NOW(), NOW()
                )
            """), {
                "content": gq.content,
                "question_type": gq.question_type,
                "difficulty": gq.difficulty,
                "status": "草稿" if gq.is_draft else "已审核",
                "source": "AI生成",
                "answer": gq.answer,
                "explanation": gq.explanation,
                "design_reason": gq.design_reason,
                "difficulty_reason": gq.difficulty_reason,
                "distractor_reasons": gq.distractor_reasons,
                "generated_question_id": gq.id,
                "creator": "AI"
            })
            db.flush()
            
            # 获取刚才插入的题目 ID
            q_id = result.lastrowid
            
            # 插入选项
            if gq.options_json:
                options = json.loads(gq.options_json)
                for idx, opt in enumerate(options):
                    db.execute(text("""
                        INSERT INTO options (question_id, content, is_correct, order_index)
                        VALUES (:question_id, :content, :is_correct, :order_index)
                    """), {
                        "question_id": q_id,
                        "content": opt.get("content", ""),
                        "is_correct": opt.get("is_correct", False),
                        "order_index": idx
                    })
            
            # 插入知识点关联
            if gq.knowledge_points:
                # 解析知识点（逗号分隔）
                kp_names = [kp.strip() for kp in gq.knowledge_points.split(',') if kp.strip()]
                for kp_name in kp_names:
                    # 查找或创建知识点
                    kp = db.query(KnowledgePoint).filter(KnowledgePoint.name == kp_name).first()
                    if not kp:
                        # 创建新知识点
                        kp = KnowledgePoint(name=kp_name)
                        db.add(kp)
                        db.flush()
                    # 插入关联
                    db.execute(text("""
                        INSERT INTO question_knowledge (question_id, knowledge_point_id)
                        VALUES (:question_id, :knowledge_point_id)
                    """), {
                        "question_id": q_id,
                        "knowledge_point_id": kp.id
                    })
            
            count += 1
    
    db.commit()
    return ApiResponse(message=f"已入库 {count} 题")
