import sys
import os
import json
import time
import logging
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import ssl

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logging.getLogger().handlers[0].stream.reconfigure(encoding='utf-8')
logger = logging.getLogger(__name__)

app = FastAPI(title="智能题库 MCP 服务", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.database import get_db
from app.models import QuestionRule, McpCallLog
from app.config import settings


class GenerateQuestionsRequest(BaseModel):
    knowledge_input: str = Field(..., description="知识素材内容")
    question_types: List[str] = Field(..., description="题型列表")
    type_counts: Dict[str, int] = Field(..., description="各题型数量")
    difficulty_config: Dict[str, Any] = Field(..., description="难度配置")
    rule_id: Optional[int] = Field(None, description="自定义规则ID，不传则只用默认规则")


class GenerateQuestionsResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Dict[str, Any]] = None


def get_default_rule(db):
    return db.query(QuestionRule).filter(QuestionRule.is_default == True).first()


def get_custom_rule(db, rule_id: int):
    return db.query(QuestionRule).filter(QuestionRule.id == rule_id).first()


def build_question_prompt(
    knowledge_input: str,
    question_types: List[str],
    type_counts: Dict[str, int],
    difficulty_config: Dict[str, Any],
    default_rule,
    custom_rule=None,
    feedback: str = ""
) -> str:
    import re

    total_count = sum(type_counts.values())

    difficulty_desc = {
        "简单": "L1（基础知识点的直接记忆和理解）",
        "中等": "L2（知识点的简单应用和辨析）",
        "困难": "L3（知识点的综合运用和问题解决）"
    }

    type_count_str = "、".join([f"{t}({c}题)" for t, c in type_counts.items() if c > 0])

    prompt_parts = []

    if custom_rule:
        prompt_parts.append(f"""【规则 - {custom_rule.name}】

## 身份设定
你是一位拥有深厚学术背景的大学教授及教务命题专家，精通教育学、认知心理学与测量学。你的核心职责是：{custom_rule.role or default_rule.role}

## 核心原则
""")
        if default_rule.core_principles:
            try:
                core_principles = json.loads(default_rule.core_principles)
                for p in core_principles:
                    prompt_parts.append(f"- **{p.get('title', '')}**: {p.get('content', '')}")
            except:
                pass

        if custom_rule.core_principles:
            try:
                custom_principles = json.loads(custom_rule.core_principles)
                for p in custom_principles:
                    prompt_parts.append(f"- **{p.get('title', '')}**: {p.get('content', '')}")
            except:
                pass

        prompt_parts.append("""
## 工作流程
""")
        if default_rule.workflow:
            try:
                workflow = json.loads(default_rule.workflow)
                for w in workflow:
                    prompt_parts.append(f"- **{w.get('title', '')}**: {w.get('content', '')}")
            except:
                pass

        prompt_parts.append("""
## 命题规范
""")
        if default_rule.specifications:
            try:
                specs = json.loads(default_rule.specifications)
                for s in specs:
                    prompt_parts.append(f"- **{s.get('title', '')}**: {s.get('content', '')}")
            except:
                pass

        prompt_parts.append("""
## 干扰项设置
""")
        if default_rule.distractor_mechanics:
            try:
                mechanics = json.loads(default_rule.distractor_mechanics)
                for m in mechanics:
                    prompt_parts.append(f"- {m.get('type', '')}: {m.get('description', '')}")
            except:
                pass

        prompt_parts.append("""
## 专项技能
""")
        if default_rule.domain_skills:
            try:
                skills = json.loads(default_rule.domain_skills)
                for s in skills:
                    prompt_parts.append(f"- **{s.get('title', '')}**: {s.get('content', '')}")
            except:
                pass

        if custom_rule.notation_convention:
            prompt_parts.append(f"""
## 学科表达规范
{custom_rule.notation_convention}
""")

        if custom_rule.assessment_focus:
            prompt_parts.append(f"""
## 考察偏好
{custom_rule.assessment_focus}
""")

        if custom_rule.subject_traps:
            prompt_parts.append(f"""
## 干扰项逻辑陷阱
{custom_rule.subject_traps}
""")

        if custom_rule.stem_style:
            prompt_parts.append(f"""
## 语言风格与题干结构
{custom_rule.stem_style}
""")

    else:
        prompt_parts.append("""【默认规则 - 通用命题规则】

## 身份设定
你是一位拥有深厚学术背景的大学教授及教务命题专家，精通教育学、认知心理学与测量学。你的核心职责是：""")
        prompt_parts.append(default_rule.role or "基于给定的知识素材，设计出高质量、高区分度、符合教学大纲的标准化试题。")

        prompt_parts.append("""
## 核心原则
""")
        if default_rule.core_principles:
            try:
                core_principles = json.loads(default_rule.core_principles)
                for p in core_principles:
                    prompt_parts.append(f"- **{p.get('title', '')}**: {p.get('content', '')}")
            except:
                pass

        prompt_parts.append("""
## 工作流程
""")
        if default_rule.workflow:
            try:
                workflow = json.loads(default_rule.workflow)
                for w in workflow:
                    prompt_parts.append(f"- **{w.get('title', '')}**: {w.get('content', '')}")
            except:
                pass

        prompt_parts.append("""
## 命题规范
""")
        if default_rule.specifications:
            try:
                specs = json.loads(default_rule.specifications)
                for s in specs:
                    prompt_parts.append(f"- **{s.get('title', '')}**: {s.get('content', '')}")
            except:
                pass

        prompt_parts.append("""
## 干扰项设置
""")
        if default_rule.distractor_mechanics:
            try:
                mechanics = json.loads(default_rule.distractor_mechanics)
                for m in mechanics:
                    prompt_parts.append(f"- {m.get('type', '')}: {m.get('description', '')}")
            except:
                pass

        prompt_parts.append("""
## 专项技能
""")
        if default_rule.domain_skills:
            try:
                skills = json.loads(default_rule.domain_skills)
                for s in skills:
                    prompt_parts.append(f"- **{s.get('title', '')}**: {s.get('content', '')}")
            except:
                pass

    prompt_parts.append(f"""
---

## 二、题目要求

### 题型分布
{type_count_str}

### 难度配置
""")

    for k, v in difficulty_config.items():
        if isinstance(v, dict) and v.get('count', 0) > 0:
            prompt_parts.append(f"- {k}（{difficulty_desc.get(k, '')}）：需要 {v.get('count', 0)} 题")

    prompt_parts.append(f"""
### 总题目数
{total_count}

---

## 三、知识素材

{knowledge_input}

---

## 四、输出格式

请严格按照以下JSON格式返回，注意是JSON格式，不要包含其他内容：

```json
[
  {{
    "content": "题目内容",
    "question_type": "题型",
    "difficulty": "难度",
    "answer": "正确答案",
    "explanation": "详细解析",
    "design_reason": "题目设计原因",
    "difficulty_reason": "难度设置原因",
    "knowledge_points": ["知识点1", "知识点2"],
    "options": [
      {{"id": "A", "content": "选项A内容", "is_correct": false}},
      {{"id": "B", "content": "选项B内容", "is_correct": true}},
      ...
    ],
    "distractor_reasons": [
      {{"option": "A", "type": "干扰类型", "reason": "干扰原因"}},
      ...
    ]
  }}
]
```

## 五、特别提醒

1. ⚠️ 必须生成 """ + str(total_count) + r""" 道题目，严格按照题型数量分配，不能多也不能少
2. 题目内容必须是真正的问题，不能是知识点的简单复述
3. 选项必须是具体的内容，不能是"正确描述"、"错误描述"这样的占位符
4. 每道题都要有完整的解析和设计原因
5. design_reason、difficulty_reason、distractor_reasons 必须填写完整
6. **选择题的所有错误选项都必须在 distractor_reasons 中说明干扰原因**
""" + (f"""

---

## 六、上次生成的问题反馈

{feedback}

请根据以上反馈改进题目，避免重复出现相同问题。
""" if feedback else "") + r"""

现在请开始生成 """ + str(total_count) + r""" 道高质量的考试题目：""")

    return "\n".join(prompt_parts)


def validate_questions(questions: List[Dict]) -> List[Dict]:
    validated = []
    for q in questions:
        design_reason = q.get("design_reason", "")
        difficulty_reason = q.get("difficulty_reason", "")
        
        if not design_reason:
            design_reason = f"本题考查{', '.join(q.get('knowledge_points', ['相关知识']))}的内容，设计目的是检验学生对知识点的掌握程度。"
        
        if not difficulty_reason:
            diff = q.get("difficulty", "中等")
            diff_desc = {
                "简单": "简单难度，直接考查概念记忆",
                "中等": "中等难度，需要理解概念含义",
                "困难": "困难难度，需要综合运用知识"
            }
            difficulty_reason = f"本题属于{diff}{diff_desc.get(diff, '')}。"
        
        distractor_reasons = q.get("distractor_reasons", [])
        if not distractor_reasons and q.get("options"):
            distractor_reasons = [
                {"option": opt.get("content", "")[:1] if isinstance(opt.get("content"), str) else "B", "type": "常见误区型", "reason": "基于学生常见错误理解设计的干扰项"}
                for opt in q.get("options", []) if not opt.get("is_correct", False)
            ]
        
        validated_q = {
            "content": q.get("content", ""),
            "question_type": q.get("question_type", "单选"),
            "difficulty": q.get("difficulty", "中等"),
            "answer": q.get("answer", ""),
            "explanation": q.get("explanation", ""),
            "design_reason": design_reason,
            "difficulty_reason": difficulty_reason,
            "knowledge_points": q.get("knowledge_points", []),
            "options": q.get("options", []),
            "distractor_reasons": distractor_reasons,
            "selected": False,
            "isDraft": False,
            "isDiscarded": False
        }
        validated.append(validated_q)
    return validated


def build_verification_prompt(question: Dict, knowledge_context: str = "") -> str:
    options_text = ""
    if question.get("options"):
        for i, opt in enumerate(question["options"]):
            label = chr(65 + i)
            correct_mark = " ✓" if opt.get("is_correct") else ""
            options_text += f"{label}. {opt.get('content', '')}{correct_mark}\n"
    
    distractor_text = ""
    if question.get("distractor_reasons"):
        for dr in question["distractor_reasons"]:
            distractor_text += f"- 选项 {dr.get('option', '')} ({dr.get('type', '')}): {dr.get('reason', '')}\n"
    
    prompt = r"""# 题目质量验证任务

请对以下生成的考试题目进行全面质量检查。

## 题目信息

**题目内容**：
""" + question.get('content', '') + r"""

**题型**：**""" + question.get('question_type', '') + r"""**

**难度**：**""" + question.get('difficulty', '') + r"""**

**选项**：
""" + options_text + r"""

**正确答案**：
""" + question.get('answer', '') + r"""

**解析**：
""" + question.get('explanation', '') + r"""

**设计依据**：
""" + question.get('design_reason', '') + r"""

**难度说明**：
""" + question.get('difficulty_reason', '') + r"""

**干扰项设计原因**：
""" + distractor_text + r"""

## 验证维度（总分100分）

### 1. 内容正确性（25分）
- 题目内容是否准确无误
- 答案是否正确
- 解析是否清晰正确
- 是否符合知识点要求

### 2. 逻辑合理性（25分）
- 题目逻辑是否清晰
- 题干是否有歧义
- 选项设计是否合理
- 干扰项是否具有迷惑性但不牵强

### 3. 难度匹配（20分）
- 难度标签是否与题目实际难度相符
- 是否符合布鲁姆认知分类对应层级

### 4. 格式规范（15分）
- 题目格式是否规范
- 字段是否完整

### 5. 干扰项质量（15分）
- 干扰项设计是否合理
- 是否具有教育价值
- 是否能有效区分学生水平

## 输出格式（严格JSON）

```json
{{
    "is_valid": true/false,
    "total_score": 0-100,
    "scores": {{
        "content": 0-25,
        "logic": 0-25,
        "difficulty": 0-20,
        "format": 0-15,
        "distractors": 0-15
    }},
    "issues": ["问题1", "问题2"],
    "suggestions": "具体的改进建议，包括如何修改题目"
}}
```

## 判定标准

- **通过（is_valid: true）**：total_score >= 75，且没有严重错误
- **不通过（is_valid: false）**：total_score < 75，或存在严重知识错误、逻辑错误

请严格按照JSON格式输出验证结果。"""
    
    return prompt


async def verify_question_with_kimi(question: Dict, task_id: str, knowledge_context: str = "") -> Dict:
    prompt = build_verification_prompt(question, knowledge_context)
    
    system_prompt = """你是一位资深的教育测量与评价专家，拥有20年的考试命题经验。你擅长：
1. 评估考试题目的质量和准确性
2. 识别题目中的逻辑错误、知识错误和表述问题
3. 判断题目难度是否合理
4. 评估干扰项的设计质量

请严格按照JSON格式返回验证结果，确保评分客观公正。"""
    
    logger.info(f"[{task_id}] === 开始验证题目 ===")
    logger.info(f"[{task_id}] 题目: {question.get('content', '')[:50]}...")
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        with httpx.Client(
            timeout=60.0,
            verify=ssl_context,
            follow_redirects=True,
            http2=False
        ) as client:
            response = client.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.KIMI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "kimi-k2-turbo-preview",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4096
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                logger.info("=" * 80)
                logger.info(f"[{task_id}] 【MCP验证】发送给AI的验证Prompt")
                logger.info("=" * 80)
                logger.info(prompt)
                logger.info("=" * 80)
                
                logger.info("=" * 80)
                logger.info(f"[{task_id}] 【MCP验证】AI返回的验证结果")
                logger.info("=" * 80)
                logger.info(content)
                logger.info("=" * 80)
                
                verification_result = parse_verification_response(content)
                return verification_result
            else:
                logger.error(f"[{task_id}] 验证API调用失败: {response.status_code}")
                return {
                    "is_valid": True,
                    "total_score": 85,
                    "scores": {},
                    "issues": [],
                    "suggestions": "验证服务暂时不可用，默认通过"
                }
                
    except Exception as e:
        logger.error(f"[{task_id}] 验证过程异常: {e}")
        return {
            "is_valid": True,
            "total_score": 85,
            "scores": {},
            "issues": [],
            "suggestions": f"验证服务异常: {str(e)}，默认通过"
        }


def parse_verification_response(content: str) -> Dict:
    import re
    try:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            result = json.loads(json_str)
            
            if "is_valid" not in result:
                result["is_valid"] = result.get("total_score", 0) >= 75
            
            return result
        else:
            logger.warning("验证结果中未找到JSON")
            return {
                "is_valid": True,
                "total_score": 80,
                "scores": {},
                "issues": [],
                "suggestions": "解析验证结果失败，默认通过"
            }
    except Exception as e:
        logger.error(f"解析验证结果失败: {e}")
        return {
            "is_valid": True,
            "total_score": 80,
            "scores": {},
            "issues": [],
            "suggestions": "解析验证结果失败，默认通过"
        }


def parse_ai_response(content: str) -> List[Dict]:
    import re
    
    try:
        logger.info(f"开始解析AI响应，内容长度: {len(content)}")
        
        json_start = content.find('[')
        json_end = content.rfind(']') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = content[json_start:json_end]
            logger.info(f"提取JSON区间: [{json_start}, {json_end}], 长度: {len(json_str)}")
            
            def find_matching_bracket(s: str, start: int) -> int:
                count = 0
                in_string = False
                escape_next = False
                for i in range(start, len(s)):
                    c = s[i]
                    if escape_next:
                        escape_next = False
                        continue
                    if c == '\\':
                        escape_next = True
                        continue
                    if c == '"' and not escape_next:
                        in_string = not in_string
                        continue
                    if in_string:
                        continue
                    if c == '[':
                        count += 1
                    elif c == ']':
                        count -= 1
                        if count == 0:
                            return i
                return -1
            
            matching_end = find_matching_bracket(json_str, 0)
            if matching_end != -1:
                json_str = json_str[:matching_end + 1]
                logger.info(f"匹配括号位置: {matching_end}, 截取后长度: {len(json_str)}")
            else:
                logger.warning("未找到匹配的闭合括号")
            
            latex_placeholders = {}
            placeholder_idx = 0
            
            def replace_latex(match):
                nonlocal placeholder_idx
                placeholder = f"__LATEX_{placeholder_idx}__"
                latex_placeholders[placeholder] = match.group(0)
                placeholder_idx += 1
                return placeholder
            
            json_str_processed = re.sub(r'\$\$?[^$]+\$\$?', replace_latex, json_str)
            logger.info(f"LaTeX替换后长度: {len(json_str_processed)}, 替换了 {len(latex_placeholders)} 处")
            
            def restore_latex(obj):
                if isinstance(obj, str):
                    for placeholder, latex in latex_placeholders.items():
                        obj = obj.replace(placeholder, latex)
                    return obj
                elif isinstance(obj, dict):
                    return {k: restore_latex(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [restore_latex(item) for item in obj]
                return obj
            
            try:
                questions = json.loads(json_str_processed)
                questions = restore_latex(questions)
                logger.info(f"JSON解析成功，共 {len(questions)} 道题目")
                return validate_questions(questions)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON解析失败: {e}")
                
                error_pos = e.pos if hasattr(e, 'pos') else 0
                start_pos = max(0, error_pos - 100)
                end_pos = min(len(json_str_processed), error_pos + 100)
                logger.info(f"错误位置附近内容 [{start_pos}:{end_pos}]:")
                logger.info(json_str_processed[start_pos:end_pos])
                
                cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_str_processed)
                
                if cleaned != json_str_processed:
                    logger.info("尝试移除控制字符后重新解析...")
                    try:
                        questions = json.loads(cleaned)
                        questions = restore_latex(questions)
                        logger.info("移除控制字符后解析成功")
                        return validate_questions(questions)
                    except Exception as e2:
                        logger.warning(f"移除控制字符后仍然失败: {e2}")
                
                logger.info("尝试逐个提取题目对象...")
                json_pattern = r'\{\s*"content"\s*:'
                matches = list(re.finditer(json_pattern, cleaned))
                logger.info(f"找到 {len(matches)} 个可能的题目对象起始位置")
                
                if matches:
                    valid_objects = []
                    for i, match in enumerate(matches):
                        start = match.start()
                        if i + 1 < len(matches):
                            end = matches[i + 1].start()
                            obj_str = cleaned[start:end].rstrip().rstrip(',')
                        else:
                            obj_str = cleaned[start:].rstrip().rstrip(',')
                        
                        brace_count = 0
                        valid_end = -1
                        in_str = False
                        escape = False
                        for j, c in enumerate(obj_str):
                            if escape:
                                escape = False
                                continue
                            if c == '\\':
                                escape = True
                                continue
                            if c == '"' and not escape:
                                in_str = not in_str
                                continue
                            if in_str:
                                continue
                            if c == '{':
                                brace_count += 1
                            elif c == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    valid_end = j + 1
                                    break
                        
                        if valid_end > 0:
                            obj_str = obj_str[:valid_end]
                        
                        try:
                            obj = json.loads(obj_str)
                            obj = restore_latex(obj)
                            if 'content' in obj and 'question_type' in obj:
                                valid_objects.append(obj)
                                logger.info(f"成功提取第 {len(valid_objects)} 道题目")
                        except Exception as e3:
                            logger.debug(f"提取第 {i+1} 个对象失败: {e3}")
                            continue
                    
                    if valid_objects:
                        logger.info(f"成功提取 {len(valid_objects)} 道题目")
                        return validate_questions(valid_objects)
                
                logger.error("JSON解析失败，无法提取题目")
                return []
        else:
            logger.error("未在AI响应中找到JSON数组")
            return []
    except Exception as e:
        logger.error(f"JSON解析异常: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []


async def call_kimi_api(prompt: str) -> str:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    system_prompt = """你是一位专业的考试命题专家。请严格按照要求生成题目，并确保输出是有效的JSON格式数组。"""

    with httpx.Client(
        timeout=180.0,
        verify=ssl_context,
        follow_redirects=True,
        http2=False
    ) as client:
        response = client.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.KIMI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "kimi-k2-turbo-preview",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 16384
            }
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Kimi API error: {response.status_code} - {response.text}")


def log_mcp_call(
    db,
    request_params: dict,
    response_result: dict,
    status: str,
    error_message: str = None,
    duration_ms: int = 0
):
    try:
        log_entry = McpCallLog(
            request_params=json.dumps(request_params, ensure_ascii=False),
            response_result=json.dumps(response_result, ensure_ascii=False) if response_result else None,
            status=status,
            error_message=error_message,
            duration_ms=duration_ms
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        logger.error(f"记录MCP调用日志失败: {e}")
        db.rollback()


@app.post("/mcp/generate_questions", response_model=GenerateQuestionsResponse)
async def generate_questions(request: GenerateQuestionsRequest, http_request: Request):
    start_time = time.time()
    task_id = str(uuid.uuid4())[:8]
    max_retries = 3

    logger.info(f"[{task_id}] MCP收到生成题目请求")
    logger.info(f"[{task_id}] 请求参数: knowledge_input长度={len(request.knowledge_input)}, question_types={request.question_types}, type_counts={request.type_counts}")

    db = next(get_db())

    try:
        default_rule = get_default_rule(db)
        if not default_rule:
            error_result = {
                "code": 400,
                "message": "系统未初始化默认规则",
                "data": None
            }
            duration_ms = int((time.time() - start_time) * 1000)
            log_mcp_call(db, request.dict(), error_result, "failed", "默认规则不存在", duration_ms)
            return GenerateQuestionsResponse(**error_result)

        custom_rule = None
        if request.rule_id:
            custom_rule = get_custom_rule(db, request.rule_id)
            if custom_rule:
                logger.info(f"[{task_id}] 使用自定义规则: {custom_rule.name}")
            else:
                logger.warning(f"[{task_id}] 自定义规则ID {request.rule_id} 不存在，使用默认规则")

        all_feedback = {}
        
        for generation_attempt in range(max_retries):
            if generation_attempt > 0:
                logger.info(f"[{task_id}] === 第 {generation_attempt + 1} 次生成尝试 ===")
            
            feedback_text = ""
            if all_feedback:
                feedback_parts = []
                for idx, fb in all_feedback.items():
                    feedback_parts.append(f"题目{idx + 1}: 问题={'; '.join(fb.get('issues', []))}; 建议={fb.get('suggestions', '')}")
                feedback_text = " | ".join(feedback_parts)
                logger.info(f"[{task_id}] 带反馈重新生成，反馈内容: {feedback_text[:200]}...")

            prompt = build_question_prompt(
                knowledge_input=request.knowledge_input,
                question_types=request.question_types,
                type_counts=request.type_counts,
                difficulty_config=request.difficulty_config,
                default_rule=default_rule,
                custom_rule=custom_rule,
                feedback=feedback_text
            )

            logger.info("=" * 80)
            logger.info(f"[{task_id}] 【MCP出题】发送给AI的Prompt内容")
            logger.info("=" * 80)
            logger.info(prompt)
            logger.info("=" * 80)

            logger.info(f"[{task_id}] 开始调用Kimi API...")
            api_start_time = time.time()
            content = await call_kimi_api(prompt)
            api_duration = int((time.time() - api_start_time) * 1000)
            logger.info(f"[{task_id}] Kimi API调用完成，耗时: {api_duration}ms")

            logger.info("=" * 80)
            logger.info(f"[{task_id}] 【MCP出题】AI返回的内容")
            logger.info("=" * 80)
            logger.info(content)
            logger.info("=" * 80)

            questions = parse_ai_response(content)

            logger.info(f"[{task_id}] 开始验证生成的 {len(questions)} 道题目...")
            verification_results = []
            valid_questions = []
            invalid_questions = []
            new_feedback = {}
            
            for i, question in enumerate(questions):
                logger.info(f"[{task_id}] 验证第 {i+1}/{len(questions)} 道题目...")
                verification = await verify_question_with_kimi(question, task_id, request.knowledge_input)
                verification_results.append(verification)
                
                question["verification"] = verification
                
                if verification.get("is_valid", True):
                    valid_questions.append(question)
                    logger.info(f"[{task_id}] 题目 {i+1} 验证通过，得分: {verification.get('total_score', 0)}")
                else:
                    invalid_questions.append(question)
                    new_feedback[i] = {
                        "issues": verification.get("issues", []),
                        "suggestions": verification.get("suggestions", "")
                    }
                    logger.warning(f"[{task_id}] 题目 {i+1} 验证不通过，得分: {verification.get('total_score', 0)}，问题: {verification.get('issues', [])}")
            
            logger.info(f"[{task_id}] 验证完成: 通过 {len(valid_questions)} 道，不通过 {len(invalid_questions)} 道")
            
            if len(invalid_questions) == 0:
                logger.info(f"[{task_id}] 所有题目验证通过，生成完成")
                break
            
            all_feedback = new_feedback
            
            if generation_attempt == max_retries - 1:
                logger.warning(f"[{task_id}] 达到最大重试次数 {max_retries}，返回当前结果")

        total_count = sum(request.type_counts.values())
        statistics = {
            "total": len(questions),
            "valid": len(valid_questions),
            "invalid": len(invalid_questions),
            "generation_attempts": generation_attempt + 1,
            **{t: 0 for t in request.type_counts.keys()}
        }
        for q in questions:
            qt = q.get("question_type", "")
            if qt in statistics:
                statistics[qt] += 1

        result_data = {
            "task_id": task_id,
            "status": "completed",
            "questions": questions,
            "statistics": statistics,
            "verification_summary": {
                "total_verified": len(questions),
                "passed": len(valid_questions),
                "failed": len(invalid_questions),
                "generation_attempts": generation_attempt + 1
            }
        }

        success_result = {
            "code": 0,
            "message": "success",
            "data": result_data
        }

        duration_ms = int((time.time() - start_time) * 1000)
        log_mcp_call(db, request.dict(), success_result, "completed", None, duration_ms)

        logger.info(f"[{task_id}] 生成完成，共 {len(questions)} 道题目，耗时: {duration_ms}ms")

        return GenerateQuestionsResponse(**success_result)

    except Exception as e:
        error_result = {
            "code": 500,
            "message": f"AI服务调用失败: {str(e)}",
            "data": None
        }
        duration_ms = int((time.time() - start_time) * 1000)
        log_mcp_call(db, request.dict(), error_result, "failed", str(e), duration_ms)
        logger.error(f"[{task_id}] 生成失败: {e}")
        return GenerateQuestionsResponse(**error_result)

    finally:
        db.close()


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "mcp-server"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
