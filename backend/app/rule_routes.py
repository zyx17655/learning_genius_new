import os
import json
import logging
import tempfile
import httpx
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import QuestionRule
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

KIMI_API_KEY = settings.KIMI_API_KEY
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"

class RuleItem(BaseModel):
    name: str
    description: Optional[str] = ""
    scene: Optional[str] = ""
    status: Optional[str] = "启用"
    role: str
    corePrinciples: List[dict] = []
    workflow: List[dict] = []
    specifications: List[dict] = []
    distractorMechanics: List[dict] = []
    domainSkills: List[dict] = []
    outputTemplate: Optional[str] = ""

class RuleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    scene: Optional[str]
    status: str
    isDefault: bool
    role: Optional[str]
    corePrinciples: List[dict]
    workflow: List[dict]
    specifications: List[dict]
    distractorMechanics: List[dict]
    domainSkills: List[dict]
    outputTemplate: Optional[str]
    creator: str
    useCount: int
    createdAt: str
    updatedAt: str

def rule_to_dict(rule: QuestionRule) -> dict:
    return {
        "id": rule.id,
        "name": rule.name,
        "description": rule.description or "",
        "scene": rule.scene or "",
        "status": rule.status,
        "isDefault": rule.is_default,
        "role": rule.role or "",
        "corePrinciples": json.loads(rule.core_principles) if rule.core_principles else [],
        "workflow": json.loads(rule.workflow) if rule.workflow else [],
        "specifications": json.loads(rule.specifications) if rule.specifications else [],
        "distractorMechanics": json.loads(rule.distractor_mechanics) if rule.distractor_mechanics else [],
        "domainSkills": json.loads(rule.domain_skills) if rule.domain_skills else [],
        "outputTemplate": rule.output_template or "",
        "creator": rule.creator,
        "useCount": rule.use_count,
        "createdAt": rule.created_at.strftime("%Y-%m-%d") if rule.created_at else "",
        "updatedAt": rule.updated_at.strftime("%Y-%m-%d") if rule.updated_at else ""
    }

@router.get("/rules")
def get_rules(db: Session = Depends(get_db)):
    rules = db.query(QuestionRule).order_by(QuestionRule.is_default.desc(), QuestionRule.created_at.desc()).all()
    return {"rules": [rule_to_dict(r) for r in rules]}

@router.get("/rules/{rule_id}")
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(QuestionRule).filter(QuestionRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    return rule_to_dict(rule)

@router.post("/rules")
def create_rule(rule: RuleItem, db: Session = Depends(get_db)):
    new_rule = QuestionRule(
        name=rule.name,
        description=rule.description,
        scene=rule.scene,
        status=rule.status,
        is_default=False,
        role=rule.role,
        core_principles=json.dumps(rule.corePrinciples, ensure_ascii=False),
        workflow=json.dumps(rule.workflow, ensure_ascii=False),
        specifications=json.dumps(rule.specifications, ensure_ascii=False),
        distractor_mechanics=json.dumps(rule.distractorMechanics, ensure_ascii=False),
        domain_skills=json.dumps(rule.domainSkills, ensure_ascii=False),
        output_template=rule.outputTemplate,
        creator="用户"
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return {"success": True, "rule": rule_to_dict(new_rule)}

@router.put("/rules/{rule_id}")
def update_rule(rule_id: int, rule: RuleItem, db: Session = Depends(get_db)):
    existing = db.query(QuestionRule).filter(QuestionRule.id == rule_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="规则不存在")
    
    existing.name = rule.name
    existing.description = rule.description
    existing.scene = rule.scene
    existing.status = rule.status
    existing.role = rule.role
    existing.core_principles = json.dumps(rule.corePrinciples, ensure_ascii=False)
    existing.workflow = json.dumps(rule.workflow, ensure_ascii=False)
    existing.specifications = json.dumps(rule.specifications, ensure_ascii=False)
    existing.distractor_mechanics = json.dumps(rule.distractorMechanics, ensure_ascii=False)
    existing.domain_skills = json.dumps(rule.domainSkills, ensure_ascii=False)
    existing.output_template = rule.outputTemplate
    
    db.commit()
    db.refresh(existing)
    return {"success": True, "rule": rule_to_dict(existing)}

@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(QuestionRule).filter(QuestionRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    if rule.is_default:
        raise HTTPException(status_code=400, detail="默认规则不能删除")
    
    db.delete(rule)
    db.commit()
    return {"success": True}

@router.post("/rules/init-default")
def init_default_rule(db: Session = Depends(get_db)):
    existing = db.query(QuestionRule).filter(QuestionRule.is_default == True).first()
    if existing:
        return {"success": True, "message": "默认规则已存在", "rule": rule_to_dict(existing)}
    
    default_rule = QuestionRule(
        name="大学通用出题规则",
        description="适用于大学各学科的通用出题规则，遵循学术标准，注重思维层级和结构严谨性。",
        scene="通用场景",
        status="启用",
        is_default=True,
        role="你是一位拥有深厚学术背景的大学教授及教务命题专家。你擅长根据特定的学科知识点，设计具有学术深度、逻辑严密且符合高阶认知目标（分析、评价、创造）的考试题目。",
        core_principles=json.dumps([
            {"title": "学术标准", "content": "题目表述需符合学术规范，术语使用准确，背景设定需具有专业真实性。"},
            {"title": "思维层级", "content": "题目应超越简单的知识点检索，重点考察学生对理论的理解、案例分析及解决复杂问题的能力。"},
            {"title": "结构严谨", "content": "选择题的干扰项（Distractors）必须具有逻辑诱导性，非随机堆砌；简答与论述题需配有明确的评分维度。"},
            {"title": "去模板化", "content": "避免生成一眼就能看出AI痕迹的陈旧题目，倾向于结合前沿研究、行业动态或经典悖论进行命题。"}
        ], ensure_ascii=False),
        workflow=json.dumps([
            {"title": "知识拆解", "content": "分析用户提供的素材或主题，提取核心概念及潜在的考察维度。"},
            {"title": "多维命题", "content": "根据指定的题型，从不同难度（基础应用、综合分析、批判挑战）进行创作。"},
            {"title": "自检优化", "content": "在输出前进行自我审视，确保题目无歧义、答案准确、解析透彻。"}
        ], ensure_ascii=False),
        specifications="[]",
        distractor_mechanics="[]",
        domain_skills="[]",
        output_template="",
        creator="系统",
        use_count=0
    )
    db.add(default_rule)
    db.commit()
    db.refresh(default_rule)
    return {"success": True, "rule": rule_to_dict(default_rule)}

@router.post("/rules/analyze")
async def analyze_questions(
    files: List[UploadFile] = File(...),
    rule_name: str = Form(...),
    db: Session = Depends(get_db)
):
    all_questions_text = []
    temp_files = []
    
    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.xlsx', '.xls', '.docx', '.doc', '.txt', '.pdf']:
            raise HTTPException(status_code=400, detail=f"不支持的文件格式: {file.filename}，请上传Excel、Word、TXT或PDF文件")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
            temp_files.append(tmp_path)
        
        try:
            questions_text = extract_questions_from_file(tmp_path, file_ext)
            if questions_text and len(questions_text.strip()) > 0:
                all_questions_text.append(f"=== 文件: {file.filename} ===\n{questions_text}")
            else:
                logger.warning(f"文件 {file.filename} 未提取到内容")
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            for tf in temp_files:
                if os.path.exists(tf):
                    os.remove(tf)
            raise HTTPException(status_code=400, detail=f"文件 {file.filename} 解析失败: {str(e)}")
    
    try:
        combined_text = "\n\n".join(all_questions_text)
        
        if not combined_text or len(combined_text.strip()) < 100:
            raise HTTPException(status_code=400, detail="未能从文件中提取到足够的试题内容")
        
        generated_rule = await analyze_questions_with_ai(combined_text, rule_name)
        
        return {"success": True, "rule": generated_rule}
    
    finally:
        for tmp_path in temp_files:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

def extract_questions_from_file(file_path: str, file_ext: str) -> str:
    questions = []
    
    try:
        if file_ext in ['.xlsx', '.xls']:
            import openpyxl
            wb = openpyxl.load_workbook(file_path)
            for sheet in wb.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    row_text = ' '.join([str(cell) if cell else '' for cell in row])
                    if row_text.strip():
                        questions.append(row_text)
        
        elif file_ext == '.docx':
            from docx import Document
            doc = Document(file_path)
            for para in doc.paragraphs:
                if para.text.strip():
                    questions.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    row_text = ' '.join([cell.text for cell in row.cells])
                    questions.append(row_text)
        
        elif file_ext == '.doc':
            logger.warning(f"检测到.doc格式文件，尝试读取...")
            text_content = ""
            
            try:
                import win32com.client
                word = win32com.client.Dispatch("Word.Application")
                word.Visible = False
                abs_path = os.path.abspath(file_path)
                doc = word.Documents.Open(abs_path)
                text_content = doc.Content.Text or ""
                doc.Close(False)
                word.Quit()
                if text_content.strip():
                    questions.append(text_content)
                    logger.info(f"成功使用win32com读取.doc文件，内容长度: {len(text_content)}")
            except Exception as e1:
                logger.error(f"win32com failed: {str(e1)}")
                try:
                    import subprocess
                    result = subprocess.run(['antiword', file_path], capture_output=True, text=True, timeout=30)
                    if result.returncode == 0 and result.stdout.strip():
                        questions.append(result.stdout)
                        logger.info(f"成功使用antiword读取.doc文件")
                    else:
                        raise Exception("antiword不可用")
                except Exception as e2:
                    logger.error(f"antiword failed: {str(e2)}")
                    raise Exception("无法读取.doc文件。建议：请将文件另存为.docx格式后重新上传，或使用Excel/PDF/TXT格式。")
        
        elif file_ext == '.pdf':
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text() or ""
                        if text.strip():
                            questions.append(text)
            except ImportError:
                logger.error("pdfplumber not installed. Run: pip install pdfplumber")
                return ""
        
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                questions = f.read().split('\n')
        
        return '\n'.join([q for q in questions if q.strip()])
    
    except Exception as e:
        logger.error(f"Error extracting questions: {str(e)}")
        raise

async def analyze_questions_with_ai(questions_text: str, rule_name: str) -> dict:
    max_content_length = 6000
    truncated_text = questions_text[:max_content_length]
    if len(questions_text) > max_content_length:
        logger.warning(f"试题内容过长，已截取前{max_content_length}字符进行分析")
    
    prompt = f"""# 任务：深度分析试题并生成专业出题规则指南

你是一位拥有深厚学术背景的教育测量与评价专家、大学教授及教务命题专家。你需要深度分析以下试题内容，提取命题核心理念、干扰项设计逻辑、数学约束标准、专项命题技能等，生成一个结构完整、专业严谨的出题规则指南。

## 试题内容
{truncated_text}

## 分析维度

请从以下维度进行深度分析：

### 1. 命题核心哲学 (Core Principles)
分析试题体现的命题理念，包括：学术标准、思维层级考查、结构严谨性、创新性要求等。

### 2. 干扰项设置深度逻辑 (Distractor Mechanics)
分析选择题干扰项的设计规律，如：常见误区型、相似概念型、部分正确型、参数陷阱型等。

### 3. 数学约束与鲁棒性标准 (Specifications)
分析试题中的数学规范要求，如：参数整齐性、物理可实现性、计算验证要求等。

### 4. 专项命题技能 (Domain Skills)
分析试题涉及的特定领域命题技能，包括各知识模块的命题要点和禁忌。

## 输出格式要求

请严格按照以下JSON格式输出：

```json
{{
  "role": "你是一位拥有深厚学术背景的大学教授及教务命题专家...",
  "corePrinciples": [
    {{"title": "原则名称", "content": "详细内容"}}
  ],
  "workflow": [
    {{"title": "步骤名称", "content": "详细内容"}}
  ],
  "specifications": [
    {{"title": "规范名称", "content": "详细内容"}}
  ],
  "distractorMechanics": [
    {{"type": "干扰项类型", "description": "设计原则"}}
  ],
  "domainSkills": [
    {{"title": "技能名称", "content": "详细内容"}}
  ],
  "outputTemplate": "输出模板格式"
}}
```"""

    try:
        logger.info(f"开始调用KIMI API，prompt长度: {len(prompt)}")
        async with httpx.AsyncClient(timeout=120.0, verify=False) as client:
            response = await client.post(
                KIMI_API_URL,
                headers={
                    "Authorization": f"Bearer {KIMI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "moonshot-v1-8k",
                    "messages": [
                        {"role": "system", "content": "你是一位拥有深厚学术背景的教育测量与评价专家、大学教授及教务命题专家。你擅长深度分析试题特征，提炼命题核心理念、干扰项设计逻辑、数学约束标准、专项命题技能等，生成的规则必须专业、详细、具有实际指导意义。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 6000
                }
            )
            
            logger.info(f"KIMI API响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    rule_data = json.loads(content[json_start:json_end])
                    
                    return {
                        "name": rule_name,
                        "description": f"基于试题分析自动生成的出题规则",
                        "scene": "",
                        "status": "启用",
                        "isDefault": False,
                        "role": rule_data.get("role", ""),
                        "corePrinciples": rule_data.get("corePrinciples", []),
                        "workflow": rule_data.get("workflow", []),
                        "specifications": rule_data.get("specifications", []),
                        "distractorMechanics": rule_data.get("distractorMechanics", []),
                        "domainSkills": rule_data.get("domainSkills", []),
                        "outputTemplate": rule_data.get("outputTemplate", ""),
                        "creator": "AI分析生成",
                        "useCount": 0,
                        "createdAt": datetime.now().strftime("%Y-%m-%d"),
                        "updatedAt": datetime.now().strftime("%Y-%m-%d")
                    }
            
            error_detail = response.text
            logger.error(f"AI analysis failed: {response.status_code}, response: {error_detail}")
            raise HTTPException(status_code=500, detail=f"AI分析失败: {error_detail}")
    
    except Exception as e:
        logger.error(f"Error in AI analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI分析出错: {str(e)}")
