from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json
import logging
import sys
import time
import httpx
import ssl

from app.database import get_db
from app.models import QuestionRule

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logging.getLogger().handlers[0].stream.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)
router = APIRouter()


class CorePrincipleItem(BaseModel):
    title: str
    content: str


class WorkflowItem(BaseModel):
    title: str
    content: str


class SpecificationItem(BaseModel):
    title: str
    content: str


class DistractorMechanicItem(BaseModel):
    type: str
    description: str


class DomainSkillItem(BaseModel):
    title: str
    content: str


class RuleCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    scene: Optional[str] = ""
    status: Optional[str] = "启用"
    role: str
    corePrinciples: List[CorePrincipleItem] = []
    workflow: List[WorkflowItem] = []
    specifications: List[SpecificationItem] = []
    distractorMechanics: List[DistractorMechanicItem] = []
    domainSkills: List[DomainSkillItem] = []
    outputTemplate: Optional[str] = ""
    notationConvention: Optional[str] = ""
    assessmentFocus: Optional[str] = ""
    subjectTraps: Optional[str] = ""
    stemStyle: Optional[str] = ""
    solutionBlueprint: Optional[str] = ""


class RuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scene: Optional[str] = None
    status: Optional[str] = None
    role: Optional[str] = None
    corePrinciples: Optional[List[CorePrincipleItem]] = None
    workflow: Optional[List[WorkflowItem]] = None
    specifications: Optional[List[SpecificationItem]] = None
    distractorMechanics: Optional[List[DistractorMechanicItem]] = None
    domainSkills: Optional[List[DomainSkillItem]] = None
    outputTemplate: Optional[str] = None
    notationConvention: Optional[str] = None
    assessmentFocus: Optional[str] = None
    subjectTraps: Optional[str] = None
    stemStyle: Optional[str] = None
    solutionBlueprint: Optional[str] = None


class RuleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    scene: Optional[str]
    status: str
    isDefault: bool
    role: str
    corePrinciples: List[dict]
    workflow: List[dict]
    specifications: List[dict]
    distractorMechanics: List[dict]
    domainSkills: List[dict]
    outputTemplate: Optional[str]
    notationConvention: Optional[str]
    assessmentFocus: Optional[str]
    subjectTraps: Optional[str]
    stemStyle: Optional[str]
    solutionBlueprint: Optional[str]
    creator: str
    useCount: int
    createdAt: str
    updatedAt: str

    class Config:
        from_attributes = True


def rule_to_response(rule: QuestionRule) -> dict:
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
        "notationConvention": rule.notation_convention or "",
        "assessmentFocus": rule.assessment_focus or "",
        "subjectTraps": rule.subject_traps or "",
        "stemStyle": rule.stem_style or "",
        "solutionBlueprint": rule.solution_blueprint or "",
        "creator": rule.creator,
        "useCount": rule.use_count,
        "createdAt": rule.created_at.strftime("%Y-%m-%d %H:%M") if rule.created_at else "",
        "updatedAt": rule.updated_at.strftime("%Y-%m-%d %H:%M") if rule.updated_at else ""
    }


@router.post("/rules/init-default")
def init_default_rule(db: Session = Depends(get_db)):
    existing = db.query(QuestionRule).filter(QuestionRule.is_default == True).first()
    if existing:
        return {"message": "默认规则已存在", "rule_id": existing.id}
    
    default_rule = QuestionRule(
        name="通用命题规则",
        description="适用于各学科的通用命题规则模板",
        scene="通用场景",
        status="启用",
        is_default=True,
        role="你是一位拥有深厚学术背景的大学教授及教务命题专家，精通教育学、认知心理学与测量学。你的核心职责是：基于给定的知识素材，设计出高质量、高区分度、符合教学大纲的标准化试题。",
        core_principles=json.dumps([
            {"title": "学术标准", "content": "题目必须准确反映学科知识，无科学性错误，符合主流教材与学术共识。"},
            {"title": "认知层次覆盖", "content": "题目应覆盖记忆、理解、应用、分析、评价、创造等多个认知层次。"},
            {"title": "区分度优化", "content": "题目应能有效区分不同水平的学生，避免过易或过难。"},
            {"title": "干扰项质量", "content": "干扰项应具有合理性、迷惑性，能反映学生的典型错误认知。"}
        ]),
        workflow=json.dumps([
            {"title": "知识拆解", "content": "分析知识素材，提取核心概念、原理、公式、定理等关键知识点。"},
            {"title": "考点设计", "content": "根据知识点设计考察点，确定考察的认知层次和难度等级。"},
            {"title": "题目生成", "content": "基于考点生成题目内容，确保语言准确、表述清晰、逻辑严密。"},
            {"title": "干扰项设计", "content": "为选择题设计高质量干扰项，确保每个干扰项都有明确的错误原因。"},
            {"title": "答案解析", "content": "提供详细的答案解析，说明正确答案的理由和错误选项的原因。"}
        ]),
        specifications=json.dumps([
            {"title": "数学与参数鲁棒性", "content": "所有数值参数必须经过验证，确保计算结果准确无误。"},
            {"title": "情境真实性", "content": "情境题应基于真实或合理的假设场景，避免脱离实际。"}
        ]),
        distractor_mechanics=json.dumps([
            {"type": "概念混淆", "description": "使用相似但不同的概念作为干扰项。"},
            {"type": "计算错误", "description": "常见计算错误结果作为干扰项。"},
            {"type": "逻辑陷阱", "description": "设置需要仔细思考才能避免的逻辑陷阱。"}
        ]),
        domain_skills=json.dumps([
            {"title": "概念理解", "content": "考察对基本概念和定义的理解。"},
            {"title": "原理应用", "content": "考察对原理和定理的应用能力。"},
            {"title": "综合分析", "content": "考察综合运用知识解决问题的能力。"}
        ]),
        output_template="",
        creator="系统",
        use_count=0
    )
    
    db.add(default_rule)
    db.commit()
    db.refresh(default_rule)
    
    return {"message": "默认规则创建成功", "rule_id": default_rule.id}


@router.get("/rules")
def get_rules(db: Session = Depends(get_db)):
    rules = db.query(QuestionRule).order_by(QuestionRule.is_default.desc(), QuestionRule.created_at.desc()).all()
    return {"rules": [rule_to_response(r) for r in rules]}


@router.get("/rules/{rule_id}")
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(QuestionRule).filter(QuestionRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    return rule_to_response(rule)


@router.post("/rules")
def create_rule(rule: RuleCreate, db: Session = Depends(get_db)):
    new_rule = QuestionRule(
        name=rule.name,
        description=rule.description,
        scene=rule.scene,
        status=rule.status,
        is_default=False,
        role=rule.role,
        core_principles=json.dumps([p.dict() for p in rule.corePrinciples]),
        workflow=json.dumps([w.dict() for w in rule.workflow]),
        specifications=json.dumps([s.dict() for s in rule.specifications]),
        distractor_mechanics=json.dumps([d.dict() for d in rule.distractorMechanics]),
        domain_skills=json.dumps([s.dict() for s in rule.domainSkills]),
        output_template=rule.outputTemplate,
        notation_convention=rule.notationConvention,
        assessment_focus=rule.assessmentFocus,
        subject_traps=rule.subjectTraps,
        stem_style=rule.stemStyle,
        solution_blueprint=rule.solutionBlueprint,
        creator="用户",
        use_count=0
    )
    
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    
    return {"message": "创建成功", "rule": rule_to_response(new_rule)}


@router.put("/rules/{rule_id}")
def update_rule(rule_id: int, rule: RuleUpdate, db: Session = Depends(get_db)):
    existing = db.query(QuestionRule).filter(QuestionRule.id == rule_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="规则不存在")
    
    update_data = rule.dict(exclude_unset=True)
    
    if "name" in update_data:
        existing.name = update_data["name"]
    if "description" in update_data:
        existing.description = update_data["description"]
    if "scene" in update_data:
        existing.scene = update_data["scene"]
    if "status" in update_data:
        existing.status = update_data["status"]
    if "role" in update_data:
        existing.role = update_data["role"]
    if "corePrinciples" in update_data:
        existing.core_principles = json.dumps([p.dict() for p in update_data["corePrinciples"]])
    if "workflow" in update_data:
        existing.workflow = json.dumps([w.dict() for w in update_data["workflow"]])
    if "specifications" in update_data:
        existing.specifications = json.dumps([s.dict() for s in update_data["specifications"]])
    if "distractorMechanics" in update_data:
        existing.distractor_mechanics = json.dumps([d.dict() for d in update_data["distractorMechanics"]])
    if "domainSkills" in update_data:
        existing.domain_skills = json.dumps([s.dict() for s in update_data["domainSkills"]])
    if "outputTemplate" in update_data:
        existing.output_template = update_data["outputTemplate"]
    if "notationConvention" in update_data:
        existing.notation_convention = update_data["notationConvention"]
    if "assessmentFocus" in update_data:
        existing.assessment_focus = update_data["assessmentFocus"]
    if "subjectTraps" in update_data:
        existing.subject_traps = update_data["subjectTraps"]
    if "stemStyle" in update_data:
        existing.stem_style = update_data["stemStyle"]
    if "solutionBlueprint" in update_data:
        existing.solution_blueprint = update_data["solutionBlueprint"]
    
    existing.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(existing)
    
    return {"message": "更新成功", "rule": rule_to_response(existing)}


@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(QuestionRule).filter(QuestionRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    
    if rule.is_default:
        raise HTTPException(status_code=400, detail="默认规则不可删除")
    
    db.delete(rule)
    db.commit()
    
    return {"message": "删除成功"}


@router.post("/rules/analyze")
async def analyze_questions(
    files: List[UploadFile] = File(...),
    rule_name: str = Form(...),
    db: Session = Depends(get_db)
):
    logger.info(f"开始分析试题文件，规则名称: {rule_name}")
    
    logger.info(f"收到 {len(files)} 个文件")
    for idx, file in enumerate(files):
        logger.info(f"文件 {idx + 1}: {file.filename}, 类型: {file.content_type}")
    
    try:
        from app.config import settings
        
        file_contents = []
        total_chars = 0
        max_chars = 50000
        
        for file in files:
            content = await file.read()
            filename_lower = file.filename.lower() if file.filename else ""
            
            if filename_lower.endswith('.pdf'):
                try:
                    import fitz
                    pdf_document = fitz.open(stream=content, filetype="pdf")
                    text_content = ""
                    for page_num in range(min(len(pdf_document), 50)):
                        page = pdf_document[page_num]
                        text_content += page.get_text()
                    pdf_document.close()
                    logger.info(f"成功解析PDF文件 {file.filename}，共 {len(text_content)} 字符")
                except ImportError:
                    logger.warning("PyMuPDF未安装，尝试使用pdfplumber")
                    try:
                        import pdfplumber
                        import io
                        with pdfplumber.open(io.BytesIO(content)) as pdf:
                            text_content = ""
                            for page in pdf.pages[:50]:
                                page_text = page.extract_text()
                                if page_text:
                                    text_content += page_text + "\n"
                        logger.info(f"成功使用pdfplumber解析PDF文件 {file.filename}")
                    except ImportError:
                        logger.error("PDF解析库未安装，请安装PyMuPDF或pdfplumber")
                        text_content = f"[PDF文件 {file.filename} 无法解析，请安装PDF解析库]"
                except Exception as e:
                    logger.error(f"解析PDF文件失败: {e}")
                    text_content = f"[PDF文件 {file.filename} 解析失败: {str(e)}]"
            elif filename_lower.endswith(('.docx', '.doc')):
                try:
                    import docx
                    import io
                    doc = docx.Document(io.BytesIO(content))
                    text_content = "\n".join([para.text for para in doc.paragraphs])
                    logger.info(f"成功解析Word文件 {file.filename}")
                except ImportError:
                    logger.error("python-docx未安装")
                    text_content = f"[Word文件 {file.filename} 无法解析，请安装python-docx]"
                except Exception as e:
                    logger.error(f"解析Word文件失败: {e}")
                    text_content = f"[Word文件 {file.filename} 解析失败: {str(e)}]"
            else:
                try:
                    text_content = content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        text_content = content.decode('gbk', errors='ignore')
                    except:
                        text_content = content.decode('utf-8', errors='ignore')
            
            if total_chars + len(text_content) > max_chars:
                text_content = text_content[:max_chars - total_chars]
                logger.warning(f"文件 {file.filename} 内容过长，已截断")
            
            file_contents.append({
                "filename": file.filename,
                "content": text_content
            })
            total_chars += len(text_content)
            
            if total_chars >= max_chars:
                logger.warning(f"已达到最大字符数限制 {max_chars}，停止读取更多文件")
                break
        
        logger.info(f"成功读取 {len(file_contents)} 个文件的内容，总字符数: {total_chars}")
        
        default_rule = db.query(QuestionRule).filter(QuestionRule.is_default == True).first()
        
        if not default_rule:
            logger.error("未找到默认规则")
            return {
                "success": False,
                "message": "系统未初始化默认规则，请先初始化"
            }
        
        default_rule_content = f"""
【默认规则 - 通用命题规则】

角色设定(Role):
{default_rule.role or '无'}

核心原则(Core Principles):
{json.dumps(json.loads(default_rule.core_principles) if default_rule.core_principles else [], ensure_ascii=False, indent=2)}

工作流程(Workflow):
{json.dumps(json.loads(default_rule.workflow) if default_rule.workflow else [], ensure_ascii=False, indent=2)}

命题规范(Specifications):
{json.dumps(json.loads(default_rule.specifications) if default_rule.specifications else [], ensure_ascii=False, indent=2)}

干扰项设置(Distractor Mechanics):
{json.dumps(json.loads(default_rule.distractor_mechanics) if default_rule.distractor_mechanics else [], ensure_ascii=False, indent=2)}

专项技能(Domain Skills):
{json.dumps(json.loads(default_rule.domain_skills) if default_rule.domain_skills else [], ensure_ascii=False, indent=2)}

输出模板(Output Template):
{default_rule.output_template or '无'}
"""
        
        exam_content = chr(10).join([f"=== 文件 {f['filename']} ===\n{f['content']}" for f in file_contents])
        
        prompt = f"""## 一、身份设定

你是一位资深的命题分析官，擅长从具体的试卷题目中洞察命题者的思维模型和学科习惯。

你的核心能力：
1. 深度文本挖掘：从试卷素材中提取命题风格、符号体系、语言特征
2. 风格采样：识别学科特有的表达习惯和考察偏好
3. 差异化分析：对比通用命题规则，提炼出学科特化的增量规则

---

## 二、默认规则（请内化以下通用标准，作为基础框架）

{default_rule_content}

---

## 三、试卷素材（原始数据，请基于事实进行归纳）

{exam_content}

---

## 四、生成要求

请基于上述试卷素材，提取出默认规则之外的"特化规则"。

重点分析以下维度：
1. **学科符号体系**：特定的物理量符号（如信号处理中的 $j$ vs $i$）、公式表示法、计算结果的精度要求
2. **考察偏好**：侧重于"数学推导"、"图形解析"还是"数值计算"？是否有特定定理的"出题执念"？
3. **学科特有陷阱设计**：该学科学生最容易掉进去的坑（如信号时移方向弄反、积分限写错）
4. **语感风格**：是简洁的"指令式"（已知...求...）还是复杂的"情境式"（某系统在...环境下...）
5. **解析深度与标准**：解析中是否需要列出所有中间公式？是否需要说明物理意义？

---

## 五、约束条件

1. 自定义规则只包含"学科灵魂"，不包含"通用骨架"
2. 生成的自定义规则必须是默认规则的"增量补充"或"差异化重写"
3. **role字段**：请基于试卷分析，生成一个针对该学科的专家角色定位（如：你是一位信号与系统领域的资深教授...），这是对默认角色的学科特化
4. 输出应精简、专业，直接用于后续命题指令的拼接

---

## 六、输出格式

请严格按照以下JSON格式返回：

{{
    "name": "{rule_name}",
    "description": "基于试卷分析生成的简短描述（一句话）",
    "role": "基于试卷分析出的学科专家角色定位（针对该学科的特化角色描述）",
    "scene": "适用场景（如：信号与系统、Python基础等）",
    "status": "启用",
    "notationConvention": "学科表达与符号习惯的具体内容（涉及公式请使用LaTeX格式，如 $j$ vs $i$）",
    "assessmentFocus": "考察偏好与方法论的具体内容",
    "subjectTraps": "干扰项逻辑陷阱的具体内容",
    "stemStyle": "语言风格与题干结构的具体内容",
    "solutionBlueprint": "解析深度与标准的具体内容（涉及公式请使用LaTeX格式）"
}}

## 数学/物理/化学公式格式要求（重要！）

所有数学、物理、化学公式及变量名**必须**使用标准 LaTeX 格式：

1. **行内公式**：使用 `$...$` 包裹，如 `$E=mc^2$`、`$\\int_a^b f(x)dx$`、`$\\alpha + \\beta$`
2. **块级公式**：使用 `$$...$$` 包裹，如 `$$\\sum_{{i=1}}^{{n}} x_i = x_1 + x_2 + \\cdots + x_n$$`
3. **变量名**：所有变量必须使用 LaTeX 格式，如 `$x$`、`$y$`、`$\\theta$`、`$\\omega$`
4. **常见符号**：
   - 分数：`$\\frac{{a}}{{b}}$`
   - 上标：`$x^2$`、`$e^{{ix}}$`
   - 下标：`$x_1$`、`$A_{{ij}}$`
   - 根号：`$\\sqrt{{2}}$`、`$\\sqrt[n]{{x}}$`
   - 希腊字母：`$\\alpha$`、`$\\beta$`、`$\\gamma$`、`$\\theta$`、`$\\omega$`
   - 运算符：`$\\times$`、`$\\div$`、`$\\pm$`、`$\\leq$`、`$\\geq$`
   - 积分：`$\\int$`、`$\\iint$`、`$\\oint$`
   - 求和：`$\\sum_{{i=1}}^{{n}}$`
   - 极限：`$\\lim_{{x \\to \\infty}}$`

**示例**：
- 正确：`求 $x^2 + 2x + 1 = 0$ 的解`
- 正确：`计算 $$\\int_0^1 x^2 dx$$ 的值`
- 正确：`已知 $\\alpha = 30^\\circ$，求 $\\sin \\alpha$`
- 错误：`求 x^2 + 2x + 1 = 0 的解`（变量未使用 LaTeX）
"""
        
        logger.info("=" * 80)
        logger.info("发送给Kimi的Prompt:")
        logger.info(prompt)
        logger.info("=" * 80)
        
        KIMI_API_KEY = settings.KIMI_API_KEY
        KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"
        
        system_prompt = """请严格按照JSON格式返回结果。确保所有字段都有具体内容，不要返回空字符串。"""
        
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                logger.info(f"尝试调用Kimi API (第{attempt + 1}次)...")
                
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                with httpx.Client(
                    timeout=180.0, 
                    verify=ssl_context, 
                    follow_redirects=True,
                    http2=False
                ) as client:
                    response = client.post(
                        KIMI_API_URL,
                        headers={
                            "Authorization": f"Bearer {KIMI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "kimi-k2-turbo-preview",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 1,
                            "max_tokens": 16384
                        }
                    )
                    
                    logger.info(f"Kimi API响应状态码: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        content = result["choices"][0]["message"]["content"]
                        
                        logger.info("=" * 80)
                        logger.info("kimi返回的内容:")
                        logger.info(content)
                        logger.info("=" * 80)
                        
                        try:
                            import re
                            json_start = content.find('{')
                            json_end = content.rfind('}') + 1
                            
                            if json_start != -1 and json_end > json_start:
                                json_str = content[json_start:json_end]
                                result_data = json.loads(json_str)
                                
                                logger.info("成功解析kimi返回的JSON")
                                logger.info(f"生成的规则名称: {result_data.get('name')}")
                                logger.info(f"完整返回数据: {json.dumps(result_data, ensure_ascii=False, indent=2)}")
                                
                                normalized_data = {
                                    "name": result_data.get("name", rule_name),
                                    "description": result_data.get("description", ""),
                                    "role": result_data.get("role", ""),
                                    "scene": result_data.get("scene", ""),
                                    "status": result_data.get("status", "启用"),
                                    "isDefault": False,
                                    "notationConvention": result_data.get("notationConvention", "") or result_data.get("notation_convention", ""),
                                    "assessmentFocus": result_data.get("assessmentFocus", "") or result_data.get("assessment_focus", ""),
                                    "subjectTraps": result_data.get("subjectTraps", "") or result_data.get("subject_traps", ""),
                                    "stemStyle": result_data.get("stemStyle", "") or result_data.get("stem_style", ""),
                                    "solutionBlueprint": result_data.get("solutionBlueprint", "") or result_data.get("solution_blueprint", "")
                                }
                                
                                logger.info(f"规范化后的数据: {json.dumps(normalized_data, ensure_ascii=False, indent=2)}")
                                
                                return {
                                    "success": True,
                                    "rule": normalized_data,
                                    "message": "分析完成"
                                }
                            else:
                                logger.error("未在响应中找到JSON对象")
                                return {
                                    "success": False,
                                    "message": "未在响应中找到JSON对象"
                                }
                        except json.JSONDecodeError as e:
                            logger.error(f"解析kimi返回的JSON失败: {e}")
                            logger.error(f"原始响应内容: {content}")
                            return {
                                "success": False,
                                "message": f"解析失败: {str(e)}"
                            }
                    else:
                        error_msg = f"API Error: {response.status_code} - {response.text}"
                        logger.error(error_msg)
                        if attempt < max_retries - 1:
                            logger.info(f"{retry_delay}秒后重试...")
                            time.sleep(retry_delay)
                            continue
                        return {
                            "success": False,
                            "message": error_msg
                        }
                        
            except httpx.ConnectError as e:
                logger.error(f"连接错误 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    continue
                return {
                    "success": False,
                    "message": f"连接Kimi API失败，请检查网络连接: {str(e)}"
                }
            except Exception as e:
                logger.error(f"请求异常 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    continue
                raise
                
    except Exception as e:
        logger.error(f"处理文件失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "success": False,
            "message": f"处理失败: {str(e)}"
        }
