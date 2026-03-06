import httpx
import json
import time
import ssl
from typing import List, Dict, Any, Optional
from app.config import settings
import logging
import traceback
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KIMI_API_KEY = settings.KIMI_API_KEY
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"

def generate_questions_with_kimi(
    knowledge_input: str,
    question_types: List[str],
    type_counts: Dict[str, int],
    difficulty_config: Dict[str, Any],
    distractor_list: List[Dict],
    preference_list: List[Dict],
    custom_requirement: str = "",
    knowledge_chunks: List[Dict] = None,
    task_id: Optional[int] = None,
    db = None,
    rule = None
) -> List[Dict]:
    
    prompt = build_generation_prompt(
        knowledge_input, question_types, type_counts,
        difficulty_config, distractor_list, preference_list, custom_requirement,
        knowledge_chunks,
        rule
    )
    
    logger.info("=" * 80)
    logger.info("【完整PROMPT内容】")
    logger.info("=" * 80)
    logger.info(prompt)
    logger.info("=" * 80)
    logger.info("【PROMPT结束】")
    logger.info("=" * 80)
    
    logger.info(f"=== 开始调用Kimi API ===")
    logger.info(f"知识范围: {knowledge_input}")
    logger.info(f"题型: {question_types}")
    logger.info(f"题型数量: {type_counts}")
    logger.info(f"API Key: {KIMI_API_KEY[:20]}...")
    
    system_prompt = """你是一位资深的教育测量与评价专家，拥有20年的考试命题经验。你擅长：
1. 根据布鲁姆认知分类设计不同层次的题目
2. 设计科学合理的干扰项，能够有效区分不同水平的学生
3. 编写清晰、准确、有教育价值的题目
4. 确保题目内容与知识点紧密相关

请严格按照JSON格式返回结果，确保题目质量达到专业考试标准。必须严格按照要求的数量生成题目，不能多也不能少。"""
    
    ai_call_log = None
    if db and task_id:
        from app.models import AICallLog
        ai_call_log = AICallLog(
            task_id=task_id,
            call_type="question_generation",
            model="moonshot-v1-8k",
            prompt=prompt,
            system_prompt=system_prompt,
            status="running"
        )
        db.add(ai_call_log)
        db.commit()
        db.refresh(ai_call_log)
        logger.info(f"创建AI调用记录: log_id={ai_call_log.id}")
    
    start_time = time.time()
    
    max_retries = 3
    retry_delay = 2
    last_error = None
    
    for attempt in range(max_retries):
        try:
            with httpx.Client(
                timeout=180.0,
                verify=False,
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
                        "model": "moonshot-v1-8k",
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 8000
                    }
                )
                
                duration_ms = int((time.time() - start_time) * 1000)
                logger.info(f"Kimi API响应状态码: {response.status_code}, 耗时: {duration_ms}ms, 尝试次数: {attempt + 1}")
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    token_count = result.get("usage", {}).get("total_tokens", 0)
                    
                    logger.info("=" * 80)
                    logger.info("【AI返回完整内容】")
                    logger.info("=" * 80)
                    logger.info(content)
                    logger.info("=" * 80)
                    logger.info("【AI返回内容结束】")
                    logger.info("=" * 80)
                    
                    logger.info(f"Kimi返回内容长度: {len(content)}, tokens: {token_count}")
                    
                    if ai_call_log:
                        ai_call_log.response = content
                        ai_call_log.status = "success"
                        ai_call_log.token_count = token_count
                        ai_call_log.duration_ms = duration_ms
                        db.commit()
                    
                    questions = parse_ai_response(content)
                    logger.info(f"解析成功，共 {len(questions)} 道题目")
                    
                    if len(questions) == 0:
                        logger.warning("解析结果为空，使用fallback")
                        return generate_fallback_questions(knowledge_input, question_types, type_counts, difficulty_config)
                    
                    return questions
                else:
                    error_msg = f"API Error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    last_error = error_msg
                    
                    if attempt < max_retries - 1:
                        logger.info(f"将在 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        continue
                    
                    if ai_call_log:
                        ai_call_log.status = "failed"
                        ai_call_log.error_message = error_msg
                        ai_call_log.duration_ms = duration_ms
                        db.commit()
                    
                    return generate_fallback_questions(knowledge_input, question_types, type_counts, difficulty_config)
                    
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_msg = f"{type(e).__name__}: {str(e)}"
            logger.error(f"Kimi API Exception (尝试 {attempt + 1}/{max_retries}): {error_msg}")
            last_error = error_msg
            
            if attempt < max_retries - 1:
                logger.info(f"将在 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                continue
    
    if ai_call_log:
        ai_call_log.status = "failed"
        ai_call_log.error_message = last_error or "Unknown error"
        ai_call_log.duration_ms = int((time.time() - start_time) * 1000)
        db.commit()
    
    return generate_fallback_questions(knowledge_input, question_types, type_counts, difficulty_config)

def build_generation_prompt(
    knowledge_input: str,
    question_types: List[str],
    type_counts: Dict[str, int],
    difficulty_config: Dict[str, Any],
    distractor_list: List[Dict],
    preference_list: List[Dict],
    custom_requirement: str,
    knowledge_chunks: List[Dict] = None,
    rule = None
) -> str:
    difficulty_desc = {
        "L1": "记忆层次 - 考查对基本概念、定义、事实的记忆和回忆",
        "L2": "理解层次 - 考查对概念原理的理解、解释和归纳",
        "L3": "应用层次 - 考查在具体情境中运用知识解决问题的能力",
        "L4": "分析层次 - 考查分析、比较、推理、归纳的能力",
        "L5": "创造层次 - 考查创新思维、综合运用、评价判断的能力"
    }
    
    total_count = sum(type_counts.values())
    
    difficulty_text = "\n".join([
        f"- {k}（{difficulty_desc.get(k, '')}）：需要 {v.get('count', 0)} 题"
        for k, v in difficulty_config.items() if v.get('count', 0) > 0
    ])
    
    distractor_text = "\n".join([f"- {d.get('name', '')}：{d.get('description', '设计有针对性的干扰项')}" for d in distractor_list]) if distractor_list else "根据常见错误理解设计干扰项"
    preference_text = "\n".join([f"- {p.get('name', '')}：{p.get('description', '')}" for p in preference_list]) if preference_list else "无特殊偏好"
    
    type_text = "、".join([f"{t}({type_counts.get(t, 0)}题)" for t in question_types])
    
    knowledge_content = ""
    if knowledge_chunks:
        knowledge_content = "\n\n## 参考资料（知识库内容）\n\n"
        for chunk in knowledge_chunks:
            knowledge_content += f"### {chunk.get('title', '知识点')}\n\n{chunk.get('content', '')}\n\n"
    
    rule_content = ""
    if rule:
        rule_content = "\n\n## 🎯 出题规则（必须严格遵守）\n\n"
        
        if rule.role:
            rule_content += f"### 角色设定\n{rule.role}\n\n"
        
        if rule.core_principles:
            try:
                principles = json.loads(rule.core_principles) if isinstance(rule.core_principles, str) else rule.core_principles
                rule_content += "### 核心原则\n"
                for p in principles:
                    rule_content += f"- **{p.get('title', '')}**：{p.get('content', '')}\n"
                rule_content += "\n"
            except:
                pass
        
        if rule.workflow:
            try:
                workflow = json.loads(rule.workflow) if isinstance(rule.workflow, str) else rule.workflow
                rule_content += "### 工作流程\n"
                for w in workflow:
                    rule_content += f"- **{w.get('title', '')}**：{w.get('content', '')}\n"
                rule_content += "\n"
            except:
                pass
        
        if rule.specifications:
            try:
                specs = json.loads(rule.specifications) if isinstance(rule.specifications, str) else rule.specifications
                rule_content += "### 命题规范\n"
                for s in specs:
                    rule_content += f"- **{s.get('title', '')}**：{s.get('content', '')}\n"
                rule_content += "\n"
            except:
                pass
        
        if rule.distractor_mechanics:
            try:
                mechanics = json.loads(rule.distractor_mechanics) if isinstance(rule.distractor_mechanics, str) else rule.distractor_mechanics
                rule_content += "### 干扰项设置逻辑\n"
                for m in mechanics:
                    rule_content += f"- **{m.get('type', '')}**：{m.get('description', '')}\n"
                rule_content += "\n"
            except:
                pass
        
        if rule.domain_skills:
            try:
                skills = json.loads(rule.domain_skills) if isinstance(rule.domain_skills, str) else rule.domain_skills
                rule_content += "### 专项命题技能\n"
                for s in skills:
                    rule_content += f"- **{s.get('title', '')}**：{s.get('content', '')}\n"
                rule_content += "\n"
            except:
                pass
        
        if rule.output_template:
            rule_content += f"### 输出模板\n{rule.output_template}\n\n"
    
    prompt = f"""# 考试题目生成任务

## 基本信息
- **知识范围**：{knowledge_input if knowledge_input else "根据选定的知识点生成"}
- **总题数**：{total_count} 题（必须严格生成 {total_count} 道题，不能多也不能少！）
- **题型分布**：{type_text}
{knowledge_content}{rule_content}
## 难度层次要求（布鲁姆认知分类）
{difficulty_text}

## 题目设计要求

### 干扰项设计原则
{distractor_text}

### 内容偏好
{preference_text}

### 自定义要求
{custom_requirement if custom_requirement else "无"}

## ⚠️ 重要约束（必须严格遵守）

1. **数量约束**：必须生成且仅生成 {total_count} 道题目，不能多也不能少！
2. **题型约束**：严格按照题型数量分配：{type_text}
3. **难度约束**：严格按照难度数量分配

## 题目质量标准

### 1. 题目内容
- 必须是一个完整、清晰的问题
- 题干要与知识点紧密相关
- 避免直接复制知识点描述
- 题目要有实际考查意义

### 2. 选项设计（选择题）
- 每个选项必须是具体、明确的内容
- 正确答案必须准确无误
- 干扰项要有迷惑性，基于常见错误理解
- 选项之间不能有包含关系
- 选项长度要基本一致

### 3. 答案与解析
- 答案要明确、准确
- 解析要说明为什么这个答案正确
- 解析要指出其他选项为什么错误

### 4. 难度匹配
- L1：直接考查概念记忆
- L2：需要理解概念含义
- L3：需要在具体场景中应用
- L4：需要分析比较多个概念
- L5：需要综合运用多个知识点

## 输出格式要求

请严格按照以下JSON格式输出，不要添加任何其他文字：

```json
[
  {{
    "content": "完整的题目内容（必须是一个问题）",
    "question_type": "单选",
    "difficulty": "L2",
    "answer": "A",
    "explanation": "详细解析：为什么A正确，其他选项为什么错误",
    "design_reason": "【必填】题目设计依据：说明本题考查哪个知识点，为什么这样设计题目，考查学生什么能力",
    "difficulty_reason": "【必填】难度层级说明：例如'本题属于L2理解层次，因为需要学生理解XXX概念的含义，而不是简单记忆'",
    "knowledge_points": ["知识点1", "知识点2"],
    "options": [
      {{"content": "选项A的具体内容（不是'选项A'这样的占位符）", "is_correct": true}},
      {{"content": "选项B的具体内容", "is_correct": false}},
      {{"content": "选项C的具体内容", "is_correct": false}},
      {{"content": "选项D的具体内容", "is_correct": false}}
    ],
    "distractor_reasons": [
      {{"option": "B", "type": "概念混淆型", "reason": "【必填】说明为什么设置此干扰项，它是什么类型的干扰（如：概念混淆型、过度概括型、以偏概全型、逆向思维型等），针对学生的什么错误理解"}}
    ]
  }}
]
```

## 字段填写要求（重要！）

### design_reason（题目设计依据）- 必填
说明本题的设计意图，例如：
- "本题考查CRH380动车空调系统的核心组成，通过对比不同车型的配置差异，考查学生对系统架构的理解"
- "本题设计目的是检验学生对隔离锁安全机制工作原理的掌握程度"

### difficulty_reason（难度层级说明）- 必填
说明为什么这道题属于该难度层级，例如：
- "L1记忆层次：本题直接考查学生对CRH380空调系统组成的记忆，不需要理解或应用"
- "L2理解层次：本题需要学生理解电控系统的工作原理，而非简单记忆"
- "L3应用层次：本题要求学生将隔离锁安全机制的知识应用到具体故障场景中"

### distractor_reasons（干扰项设计原因）- 选择题必填
每个干扰项必须说明：
1. 干扰类型：概念混淆型、过度概括型、以偏概全型、逆向思维型、常见误区型等
2. 设计原因：针对学生的什么错误理解，为什么能起到干扰作用

例如：
```json
{{
  "option": "B",
  "type": "概念混淆型",
  "reason": "学生常将空调系统的制冷剂类型与冷却液类型混淆，此干扰项针对这一常见错误"
}}
```

## 特别提醒

1. ⚠️ 必须生成 {total_count} 道题目，严格按照题型数量分配，不能多也不能少
2. 题目内容必须是真正的问题，不能是知识点的简单复述
3. 选项必须是具体的内容，不能是"正确描述"、"错误描述"这样的占位符
4. 每道题都要有完整的解析和设计原因
5. design_reason、difficulty_reason、distractor_reasons 必须填写完整

现在请开始生成 {total_count} 道高质量的考试题目："""
    
    return prompt

def parse_ai_response(content: str) -> List[Dict]:
    try:
        json_start = content.find('[')
        json_end = content.rfind(']') + 1
        if json_start != -1 and json_end > json_start:
            json_str = content[json_start:json_end]
            questions = json.loads(json_str)
            return validate_questions(questions)
        else:
            logger.error("未找到JSON数组")
            return []
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析错误: {e}")
        logger.error(f"尝试解析的内容: {content[:1000]}")
        return []

def validate_questions(questions: List[Dict]) -> List[Dict]:
    validated = []
    for q in questions:
        design_reason = q.get("design_reason", "")
        difficulty_reason = q.get("difficulty_reason", "")
        
        if not design_reason:
            design_reason = f"本题考查{', '.join(q.get('knowledge_points', ['相关知识']))}的内容，设计目的是检验学生对知识点的掌握程度。"
        
        if not difficulty_reason:
            diff = q.get("difficulty", "L2")
            diff_desc = {
                "L1": "记忆层次，直接考查概念记忆",
                "L2": "理解层次，需要理解概念含义",
                "L3": "应用层次，需要在具体场景中应用",
                "L4": "分析层次，需要分析比较多个概念",
                "L5": "创造层次，需要综合运用多个知识点"
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
            "difficulty": q.get("difficulty", "L2"),
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

def generate_fallback_questions(
    knowledge_input: str,
    question_types: List[str],
    type_counts: Dict[str, int],
    difficulty_config: Dict[str, Any]
) -> List[Dict]:
    logger.warning("=== 使用Fallback生成逻辑（Kimi API调用失败）===")
    
    questions = []
    difficulties = []
    for level, config in difficulty_config.items():
        for _ in range(config.get("count", 0)):
            difficulties.append(level)
    
    idx = 0
    for q_type in question_types:
        count = type_counts.get(q_type, 0)
        for i in range(count):
            diff = difficulties[idx] if idx < len(difficulties) else "L2"
            
            if q_type == "单选":
                questions.append({
                    "content": f"关于{knowledge_input}，下列说法正确的是？",
                    "question_type": "单选",
                    "difficulty": diff,
                    "answer": "A",
                    "explanation": f"这是关于{knowledge_input}的基础知识点考查。",
                    "design_reason": f"本题考查{knowledge_input}的核心概念，设计目的是检验学生对基础知识的掌握程度。",
                    "difficulty_reason": f"本题属于{diff}层次，考查学生对{knowledge_input}的理解。",
                    "knowledge_points": [knowledge_input],
                    "options": [
                        {"content": "正确描述选项", "is_correct": True},
                        {"content": "错误描述选项1", "is_correct": False},
                        {"content": "错误描述选项2", "is_correct": False},
                        {"content": "错误描述选项3", "is_correct": False}
                    ],
                    "distractor_reasons": [
                        {"option": "B", "type": "常见误区型", "reason": "基于学生对概念的常见误解设计"}
                    ],
                    "selected": False,
                    "isDraft": False,
                    "isDiscarded": False
                })
            elif q_type == "判断":
                questions.append({
                    "content": f"{knowledge_input}是重要的知识点。",
                    "question_type": "判断",
                    "difficulty": diff,
                    "answer": "正确",
                    "explanation": f"这个说法是正确的。",
                    "design_reason": f"本题考查{knowledge_input}的基本概念判断。",
                    "difficulty_reason": f"本题属于{diff}层次，考查学生对{knowledge_input}的判断能力。",
                    "knowledge_points": [knowledge_input],
                    "options": [],
                    "distractor_reasons": [],
                    "selected": False,
                    "isDraft": False,
                    "isDiscarded": False
                })
            
            idx += 1
    
    return questions
