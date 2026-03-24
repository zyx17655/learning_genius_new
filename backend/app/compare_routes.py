"""
题目质量对比路由 - 用于对比题库题目与真题质量
支持单题对比和整体对比（多题vs多题）
"""
import os
import json
import logging
import tempfile
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

router = APIRouter(tags=["题目对比"])
logger = logging.getLogger(__name__)


# 请求模型
class QuestionData(BaseModel):
    """题目数据结构"""
    id: Optional[int] = None
    content: str
    question_type: Optional[str] = "单选"
    difficulty: Optional[str] = "L2"
    options: Optional[list] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None


class CompareRequest(BaseModel):
    """单题对比请求模型"""
    questionA: QuestionData  # 题库题目
    questionB: QuestionData  # 真题


class BatchCompareRequest(BaseModel):
    """批量/整体对比请求模型"""
    questionsA: List[QuestionData]  # 题库题目列表
    questionsB: List[QuestionData]  # 真题列表
    compareMode: str = "overall"  # "single" - 逐题对比, "overall" - 整体对比


class CompareResponse(BaseModel):
    """单题对比响应模型"""
    winner: str  # 'A', 'B', 或 'tie'
    scores: dict  # {"A": 85, "B": 78}
    analysis: str  # 详细分析
    dimensions: Optional[dict] = None  # 多维度评分
    suggestions: Optional[list] = None  # 改进建议


class BatchCompareResponse(BaseModel):
    """批量对比响应模型"""
    compareMode: str  # "single" 或 "overall"
    overallResult: Optional[CompareResponse] = None  # 整体对比结果
    singleResults: Optional[List[CompareResponse]] = None  # 逐题对比结果
    summary: dict  # 统计摘要


# OCR 相关导入
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("OCR功能不可用，请安装 pytesseract 和 Pillow")


def get_llm_client():
    """
    获取大模型客户端配置
    使用用户自定义的API Key和模型配置
    """
    api_key = os.getenv("COMPARE_LLM_API_KEY")
    api_base = os.getenv("COMPARE_LLM_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    model_name = os.getenv("COMPARE_LLM_MODEL", "qwen3-max")
    
    if not api_key:
        logger.error("未配置对比功能的大模型API Key")
        return None, None, None
    
    return api_key, api_base, model_name


def format_question_for_prompt(question: QuestionData, index: Optional[int] = None) -> str:
    """将题目格式化为prompt文本"""
    prefix = f"题目 {index}: " if index else ""
    result = f"""
{prefix}【题目类型】: {question.question_type or '未知'}
【难度等级】: {question.difficulty or '未知'}
【题目内容】: {question.content}
"""
    
    if question.options and len(question.options) > 0:
        result += "【选项】:\n"
        for idx, opt in enumerate(question.options):
            label = chr(65 + idx)  # A, B, C, D...
            content = opt.get('content', '') if isinstance(opt, dict) else str(opt)
            is_correct = opt.get('is_correct', False) if isinstance(opt, dict) else False
            correct_mark = " (正确答案)" if is_correct else ""
            result += f"  {label}. {content}{correct_mark}\n"
    
    if question.answer:
        result += f"【答案】: {question.answer}\n"
    
    if question.explanation:
        result += f"【解析】: {question.explanation}\n"
    
    return result


def format_questions_list(questions: List[QuestionData], side: str) -> str:
    """格式化题目列表"""
    result = f"=== {side} 共{len(questions)}道题 ===\n\n"
    
    # 统计题型分布
    type_counts = {}
    difficulty_counts = {}
    for q in questions:
        type_counts[q.question_type or '未知'] = type_counts.get(q.question_type or '未知', 0) + 1
        difficulty_counts[q.difficulty or '未知'] = difficulty_counts.get(q.difficulty or '未知', 0) + 1
    
    result += "【题型分布】: " + ", ".join([f"{k}:{v}" for k, v in type_counts.items()]) + "\n"
    result += "【难度分布】: " + ", ".join([f"{k}:{v}" for k, v in difficulty_counts.items()]) + "\n\n"
    
    # 列出每道题
    for i, q in enumerate(questions, 1):
        result += format_question_for_prompt(q, i) + "\n"
    
    return result


def build_single_compare_prompt(question_a: QuestionData, question_b: QuestionData) -> str:
    """构建单题对比分析的prompt"""
    prompt = f"""你是一位资深的教育评估专家，擅长分析题目质量。请对比以下两道题目，从多个维度评估哪道题目质量更优。

=== 题目 A (题库题目) ===
{format_question_for_prompt(question_a)}

=== 题目 B (真题) ===
{format_question_for_prompt(question_b)}

请从以下维度进行详细对比分析：

1. **科学性**：题目表述是否准确，概念是否清晰，是否存在知识性错误
2. **合理性**：难度设置是否合理，与考察目标是否匹配
3. **严谨性**：逻辑是否严密，选项设置是否合理（如果是选择题）
4. **表达质量**：语言是否简洁明了，是否存在歧义
5. **教育价值**：是否能有效考察学生的知识掌握和能力水平

请按以下JSON格式输出你的分析结果（只输出JSON，不要添加其他文字说明）：

{
    "winner": "A或B或tie",
    "scores": {
        "A": 85,
        "B": 78
    },
    "analysis": "详细分析文本，说明哪边更合理及理由...",
    "dimensions": {
        "scientific": {
            "name": "科学性",
            "scoreA": 90,
            "scoreB": 85,
            "description": "题目A在概念准确性上更优..."
        },
        "reasonable": {
            "name": "合理性",
            "scoreA": 80,
            "scoreB": 82,
            "description": "题目B的难度设置更合理..."
        },
        "rigorous": {
            "name": "严谨性",
            "scoreA": 85,
            "scoreB": 75,
            "description": "题目A逻辑更严密..."
        },
        "expression": {
            "name": "表达质量",
            "scoreA": 88,
            "scoreB": 80,
            "description": "题目A语言更简洁明了..."
        },
        "educational": {
            "name": "教育价值",
            "scoreA": 82,
            "scoreB": 85,
            "description": "题目B更能考察学生能力..."
        }
    },
    "suggestions": [
        {
            "target": "A",
            "content": "建议题目A改进..."
        },
        {
            "target": "B",
            "content": "建议题目B改进..."
        }
    ]
}

重要提示：请直接返回JSON格式的结果，不要添加markdown代码块标记（如 ```json），也不要添加任何其他文字说明。确保输出的是有效的JSON格式。"""
    
    return prompt


def build_overall_compare_prompt(questions_a: List[QuestionData], questions_b: List[QuestionData]) -> str:
    """构建整体对比分析的prompt"""
    prompt = f"""你是一位资深的教育评估专家，擅长分析题库质量。请对比以下两组题目（题库题目 vs 真题），进行整体质量评估。

{format_questions_list(questions_a, "A组 - 题库题目")}

{format_questions_list(questions_b, "B组 - 真题")}

请从以下维度进行整体对比分析：

1. **科学性**：题目表述是否准确，概念是否清晰，是否存在知识性错误
2. **合理性**：难度分布是否合理，题型搭配是否科学
3. **严谨性**：逻辑是否严密，选项设置是否合理
4. **表达质量**：语言是否简洁明了，是否存在歧义
5. **教育价值**：是否能有效考察学生的知识掌握和能力水平
6. **覆盖面**：知识点覆盖是否全面，考察角度是否多样
7. **创新性**：题目设计是否有新意，是否能激发学生思考

请按以下JSON格式输出你的分析结果（只输出JSON，不要添加其他文字说明）：

{
    "winner": "A或B或tie",
    "scores": {
        "A": 85,
        "B": 78
    },
    "analysis": "详细分析文本，从整体角度说明哪组题目更合理及理由...",
    "dimensions": {
        "scientific": {
            "name": "科学性",
            "scoreA": 90,
            "scoreB": 85,
            "description": "A组题目在概念准确性上更优..."
        },
        "reasonable": {
            "name": "合理性",
            "scoreA": 80,
            "scoreB": 82,
            "description": "B组难度分布更合理..."
        },
        "rigorous": {
            "name": "严谨性",
            "scoreA": 85,
            "scoreB": 75,
            "description": "A组逻辑更严密..."
        },
        "expression": {
            "name": "表达质量",
            "scoreA": 88,
            "scoreB": 80,
            "description": "A组语言更简洁明了..."
        },
        "educational": {
            "name": "教育价值",
            "scoreA": 82,
            "scoreB": 85,
            "description": "B组更能考察学生能力..."
        },
        "coverage": {
            "name": "覆盖面",
            "scoreA": 85,
            "scoreB": 88,
            "description": "B组知识点覆盖更全面..."
        },
        "innovation": {
            "name": "创新性",
            "scoreA": 78,
            "scoreB": 82,
            "description": "B组题目设计更有新意..."
        }
    },
    "suggestions": [
        {
            "target": "A",
            "content": "建议题库改进..."
        },
        {
            "target": "B",
            "content": "建议真题改进..."
        }
    ]
}

重要提示：请直接返回JSON格式的结果，不要添加markdown代码块标记（如 ```json），也不要添加任何其他文字说明。确保输出的是有效的JSON格式。"""
    
    return prompt


async def call_llm_for_compare(prompt: str) -> dict:
    """
    调用大模型进行对比分析
    使用用户自定义的API配置（当前为Qwen3-Max）
    """
    api_key, api_base, model_name = get_llm_client()
    
    if not api_key:
        logger.warning("未配置API Key，返回模拟对比结果")
        return {
            "winner": "A",
            "scores": {"A": 85, "B": 78},
            "analysis": "【模拟结果】题库题目在整体质量上更优，概念表述准确，逻辑严密。真题虽然也不错，但在严谨性方面略有欠缺。",
            "dimensions": {
                "scientific": {"name": "科学性", "scoreA": 90, "scoreB": 85, "description": "题库概念表述更准确"},
                "reasonable": {"name": "合理性", "scoreA": 80, "scoreB": 82, "description": "真题难度分布更合理"},
                "rigorous": {"name": "严谨性", "scoreA": 85, "scoreB": 75, "description": "题库逻辑更严密"},
                "expression": {"name": "表达质量", "scoreA": 88, "scoreB": 80, "description": "题库语言更简洁"},
                "educational": {"name": "教育价值", "scoreA": 82, "scoreB": 85, "description": "真题更能考察能力"},
                "coverage": {"name": "覆盖面", "scoreA": 85, "scoreB": 88, "description": "真题知识点覆盖更全面"},
                "innovation": {"name": "创新性", "scoreA": 78, "scoreB": 82, "description": "真题设计更有新意"}
            },
            "suggestions": [
                {"target": "A", "content": "可以进一步优化难度分布，增加创新性题目"},
                {"target": "B", "content": "建议修正部分题目的表述，使其更加严谨准确"}
            ]
        }
    
    try:
        # 使用OpenAI SDK调用（兼容模式，适用于Qwen等模型）
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=api_key,
                base_url=api_base
            )
            
            logger.info(f"调用大模型: {model_name}")
            
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "你是一位资深的教育评估专家，擅长分析题目质量。请客观、专业地评估题目，输出有效的JSON格式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            logger.info("大模型调用成功")
            
        except ImportError:
            # 如果没有openai库，使用requests
            import requests
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "你是一位资深的教育评估专家，擅长分析题目质量。请客观、专业地评估题目，输出有效的JSON格式。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            logger.info(f"使用requests调用大模型: {model_name}")
            
            response = requests.post(
                f"{api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            logger.info("大模型调用成功")
        
        # 解析JSON响应
        import re
        logger.info(f"大模型返回内容长度: {len(content)}")
        logger.debug(f"大模型返回内容: {content[:500]}...")
        
        # 尝试提取JSON代码块
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            logger.info("从代码块中提取到JSON")
        else:
            # 尝试直接匹配JSON对象
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                json_str = json_match.group(0)
                logger.info("从文本中提取到JSON对象")
            else:
                json_str = content
                logger.warning("未找到JSON格式，使用原始内容")
        
        try:
            result = json.loads(json_str)
            logger.info(f"JSON解析成功，winner: {result.get('winner', 'unknown')}")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            logger.error(f"尝试解析的内容: {json_str[:200]}...")
            raise HTTPException(status_code=500, detail=f"AI返回结果解析失败: {str(e)}")
        
    except Exception as e:
        logger.error(f"调用大模型失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI分析失败: {str(e)}")


@router.post("/questions", response_model=CompareResponse)
async def compare_questions(request: CompareRequest):
    """
    对比两道题目质量（单题对比）
    """
    try:
        logger.info("开始单题质量对比分析")
        
        prompt = build_single_compare_prompt(request.questionA, request.questionB)
        result = await call_llm_for_compare(prompt)
        
        logger.info(f"单题对比完成，结果: {result.get('winner', 'unknown')}")
        
        return CompareResponse(
            winner=result.get("winner", "tie"),
            scores=result.get("scores", {"A": 0, "B": 0}),
            analysis=result.get("analysis", ""),
            dimensions=result.get("dimensions"),
            suggestions=result.get("suggestions")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"对比分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"对比分析失败: {str(e)}")


@router.post("/batch", response_model=BatchCompareResponse)
async def batch_compare(request: BatchCompareRequest):
    """
    批量对比题目质量
    支持两种模式：
    1. single: 逐题对比（题目数量需相同）
    2. overall: 整体对比（题目数量可不同，从整体质量角度评估）
    """
    try:
        logger.info(f"开始批量对比，模式: {request.compareMode}")
        
        if request.compareMode == "single":
            # 逐题对比模式
            if len(request.questionsA) != len(request.questionsB):
                raise HTTPException(
                    status_code=400,
                    detail="逐题对比模式要求两组题目数量相同"
                )
            
            single_results = []
            for i, (qa, qb) in enumerate(zip(request.questionsA, request.questionsB)):
                try:
                    prompt = build_single_compare_prompt(qa, qb)
                    result = await call_llm_for_compare(prompt)
                    single_results.append(CompareResponse(
                        winner=result.get("winner", "tie"),
                        scores=result.get("scores", {"A": 0, "B": 0}),
                        analysis=result.get("analysis", ""),
                        dimensions=result.get("dimensions"),
                        suggestions=result.get("suggestions")
                    ))
                except Exception as e:
                    logger.error(f"第 {i+1} 题对比失败: {str(e)}")
                    single_results.append(CompareResponse(
                        winner="tie",
                        scores={"A": 0, "B": 0},
                        analysis=f"对比失败: {str(e)}",
                        dimensions=None,
                        suggestions=None
                    ))
            
            # 计算统计摘要
            win_count = {"A": 0, "B": 0, "tie": 0}
            total_score_a = 0
            total_score_b = 0
            for r in single_results:
                win_count[r.winner] = win_count.get(r.winner, 0) + 1
                total_score_a += r.scores.get("A", 0)
                total_score_b += r.scores.get("B", 0)
            
            return BatchCompareResponse(
                compareMode="single",
                singleResults=single_results,
                summary={
                    "total": len(single_results),
                    "winCount": win_count,
                    "avgScoreA": round(total_score_a / len(single_results), 2) if single_results else 0,
                    "avgScoreB": round(total_score_b / len(single_results), 2) if single_results else 0
                }
            )
            
        else:
            # 整体对比模式（题目数量可不同）
            prompt = build_overall_compare_prompt(request.questionsA, request.questionsB)
            result = await call_llm_for_compare(prompt)
            
            overall_result = CompareResponse(
                winner=result.get("winner", "tie"),
                scores=result.get("scores", {"A": 0, "B": 0}),
                analysis=result.get("analysis", ""),
                dimensions=result.get("dimensions"),
                suggestions=result.get("suggestions")
            )
            
            return BatchCompareResponse(
                compareMode="overall",
                overallResult=overall_result,
                summary={
                    "totalA": len(request.questionsA),
                    "totalB": len(request.questionsB),
                    "winner": overall_result.winner,
                    "scoreA": overall_result.scores.get("A", 0),
                    "scoreB": overall_result.scores.get("B", 0)
                }
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"批量对比分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"批量对比分析失败: {str(e)}")


@router.post("/upload-and-ocr")
async def upload_and_ocr(file: UploadFile = File(...)):
    """
    上传文件并进行OCR识别
    支持PDF、图片等格式
    """
    try:
        logger.info(f"接收到文件上传: {file.filename}")
        
        # 检查文件类型
        allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'}
        file_ext = os.path.splitext(file.filename.lower())[1]
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的文件类型: {file_ext}，请上传PDF或图片文件"
            )
        
        # 保存上传的文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # 根据文件类型进行OCR
            if file_ext == '.pdf':
                text = await ocr_pdf(tmp_path)
            else:
                text = await ocr_image(tmp_path)
            
            logger.info(f"OCR识别完成，文本长度: {len(text)}")
            
            return {
                "filename": file.filename,
                "text": text,
                "length": len(text)
            }
            
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR识别失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR识别失败: {str(e)}")


async def ocr_pdf(file_path: str) -> str:
    """
    对PDF文件进行OCR识别
    优先使用PyMuPDF（纯Python，无需外部依赖），失败时尝试pdf2image+pytesseract
    """
    # 首先尝试使用PyMuPDF（推荐，无需poppler）
    try:
        import fitz  # PyMuPDF
        
        logger.info("使用PyMuPDF进行PDF文本提取")
        doc = fitz.open(file_path)
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_parts.append(text)
        
        doc.close()
        
        # 如果成功提取到文本，直接返回
        if text_parts and any(t.strip() for t in text_parts):
            return "\n\n".join(text_parts)
        
        logger.warning("PyMuPDF未提取到文本，尝试OCR识别")
        
    except ImportError:
        logger.warning("PyMuPDF未安装")
    except Exception as e:
        logger.warning(f"PyMuPDF提取失败: {str(e)}")
    
    # 如果PyMuPDF不可用或未提取到文本，尝试使用pdf2image+pytesseract进行OCR
    try:
        from pdf2image import convert_from_path
        
        logger.info("使用pdf2image+pytesseract进行OCR识别")
        images = convert_from_path(file_path, dpi=300)
        text_parts = []
        
        for i, image in enumerate(images):
            logger.info(f"正在识别PDF第 {i+1}/{len(images)} 页")
            if OCR_AVAILABLE:
                text = pytesseract.image_to_string(image, lang='chi_sim+eng')
                text_parts.append(text)
            else:
                raise HTTPException(
                    status_code=500,
                    detail="PDF需要OCR识别，但未安装pytesseract"
                )
        
        return "\n\n".join(text_parts)
        
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="PDF处理失败。请安装PyMuPDF: pip install PyMuPDF，或安装poppler+pdf2image"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF OCR识别失败: {str(e)}"
        )


async def ocr_image(file_path: str) -> str:
    """
    对图片进行OCR识别
    """
    if not OCR_AVAILABLE:
        raise HTTPException(
            status_code=500,
            detail="OCR功能不可用，请安装 pytesseract 和 Pillow"
        )
    
    try:
        image = Image.open(file_path)
        
        # 使用中文+英文识别
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        
        return text
        
    except Exception as e:
        logger.error(f"图片OCR失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片识别失败: {str(e)}")
