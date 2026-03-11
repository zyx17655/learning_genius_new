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
    default_rule = None,
    custom_rule = None
) -> List[Dict]:
    
    prompt = build_generation_prompt(
        knowledge_input, question_types, type_counts,
        difficulty_config, distractor_list, preference_list, custom_requirement,
        knowledge_chunks,
        default_rule,
        custom_rule
    )
    
    logger.info(f"=== 开始调用Kimi API ===")
    logger.info(f"知识范围: {knowledge_input}")
    logger.info(f"题型: {question_types}")
    logger.info(f"题型数量: {type_counts}")
    logger.debug(f"API Key: {KIMI_API_KEY[:20]}...")
    logger.debug(f"完整Prompt长度: {len(prompt)} 字符")
    
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
            model="kimi-k2-0711-preview",
            prompt=prompt,
            system_prompt=system_prompt,
            status="running"
        )
        db.add(ai_call_log)
        db.commit()
        db.refresh(ai_call_log)
        logger.info(f"创建AI调用记录: log_id={ai_call_log.id}")
    
    start_time = time.time()
    
    logger.info("=" * 80)
    logger.info("【发送给AI的Prompt内容】")
    logger.info("=" * 80)
    logger.info(prompt)
    logger.info("=" * 80)
    
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
                        "model": "kimi-k2-turbo-preview",
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
                        "temperature": 1,
                        "max_tokens": 32768
                    }
                )
                
                duration_ms = int((time.time() - start_time) * 1000)
                logger.info(f"Kimi API响应状态码: {response.status_code}, 耗时: {duration_ms}ms, 尝试次数: {attempt + 1}")
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    token_count = result.get("usage", {}).get("total_tokens", 0)
                    
                    logger.info("=" * 80)
                    logger.info("【AI返回的内容】")
                    logger.info("=" * 80)
                    logger.info(content)
                    logger.info("=" * 80)
                    logger.info(f"返回内容长度: {len(content)} 字符, tokens: {token_count}")
                    
                    if ai_call_log:
                        ai_call_log.response = content
                        ai_call_log.status = "success"
                        ai_call_log.token_count = token_count
                        ai_call_log.duration_ms = duration_ms
                        db.commit()
                    
                    questions = parse_ai_response(content)
                    logger.info(f"题目解析成功，共 {len(questions)} 道题目")
                    
                    if len(questions) == 0:
                        logger.warning("题目解析结果为空，使用fallback生成")
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
            logger.error(f"Kimi API调用失败 (尝试 {attempt + 1}/{max_retries}): {error_msg}")
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
    default_rule = None,
    custom_rule = None
) -> str:
    difficulty_desc = {
        "简单": "考察高频核心考点，情境描述直接，干扰项区分度明显。对应认知层级：L1记忆/L2理解",
        "中等": "引入标准专业情境，要求多步逻辑推导，干扰项包含典型概念混淆。对应认知层级：L3应用/L4分析",
        "困难": "提供复杂或陌生场景，要求综合评判或方案构建，逻辑链条长且隐蔽。对应认知层级：L5评价/L6创造"
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
    
    def build_rule_content(rule, rule_type: str) -> str:
        if not rule:
            return ""
        
        content = ""
        if rule.role:
            content += f"### 角色设定\n{rule.role}\n\n"
        
        if rule.core_principles:
            try:
                principles = json.loads(rule.core_principles) if isinstance(rule.core_principles, str) else rule.core_principles
                content += "### 核心原则\n"
                for p in principles:
                    content += f"- **{p.get('title', '')}**：{p.get('content', '')}\n"
                content += "\n"
            except:
                pass
        
        if rule.workflow:
            try:
                workflow = json.loads(rule.workflow) if isinstance(rule.workflow, str) else rule.workflow
                content += "### 工作流程\n"
                for w in workflow:
                    content += f"- **{w.get('title', '')}**：{w.get('content', '')}\n"
                content += "\n"
            except:
                pass
        
        if rule.specifications:
            try:
                specs = json.loads(rule.specifications) if isinstance(rule.specifications, str) else rule.specifications
                content += "### 命题规范\n"
                for s in specs:
                    content += f"- **{s.get('title', '')}**：{s.get('content', '')}\n"
                content += "\n"
            except:
                pass
        
        if rule.distractor_mechanics:
            try:
                mechanics = json.loads(rule.distractor_mechanics) if isinstance(rule.distractor_mechanics, str) else rule.distractor_mechanics
                content += "### 干扰项设置逻辑\n"
                for m in mechanics:
                    content += f"- **{m.get('type', '')}**：{m.get('description', '')}\n"
                content += "\n"
            except:
                pass
        
        if rule.domain_skills:
            try:
                skills = json.loads(rule.domain_skills) if isinstance(rule.domain_skills, str) else rule.domain_skills
                content += "### 专项命题技能\n"
                for s in skills:
                    content += f"- **{s.get('title', '')}**：{s.get('content', '')}\n"
                content += "\n"
            except:
                pass
        
        if rule.output_template:
            content += f"### 输出模板\n{rule.output_template}\n\n"
        
        return content
    
    default_rule_content = build_rule_content(default_rule, "默认")
    custom_rule_content = build_rule_content(custom_rule, "自定义")
    
    has_custom_rule = custom_rule is not None and custom_rule_content.strip()
    
    rule_section = ""
    if default_rule_content.strip():
        rule_section = f"""
## 🎯 默认出题规则

{default_rule_content}"""
    
    if has_custom_rule:
        rule_section += """
---

⚠️ **以下为用户自定义规则，与上述默认规则冲突时以本节为准**

---

## 🔧 用户自定义规则

""" + custom_rule_content
    
    difficulty_constraint_text = "、".join([f"{k}（{v.get('count', 0)}题）" for k, v in difficulty_config.items() if v.get('count', 0) > 0])
    
    prompt = f"""# 考试题目生成任务

你是一位资深的教育测量与评价专家，拥有20年的考试命题经验。请根据以下要求生成高质量的考试题目。

## 基本信息
- **知识范围**：{knowledge_input if knowledge_input else "根据选定的知识点生成"}
- **总题数**：{total_count} 题（必须严格生成 {total_count} 道题，不能多也不能少！）
- **题型分布**：{type_text}
{knowledge_content}{rule_section}
## 难度层次要求（布鲁姆认知分类）
{difficulty_text}

## ⚠️ 重要约束（必须严格遵守）

1. **数量约束**：必须生成且仅生成 {total_count} 道题目，不能多也不能少！
2. **题型约束**：严格按照题型数量分配：{type_text}
3. **难度约束**：严格按照难度数量分配：{difficulty_constraint_text}
4. **规则优先级**：如有冲突，以用户自定义规则为准{f"，自定义规则优先级高于默认规则" if has_custom_rule else ""}

## 输出格式要求

请严格按照以下JSON格式输出，不要添加任何其他文字：

```json
[
  {{
    "content": "完整的题目内容（必须是一个问题）",
    "question_type": "单选",
    "difficulty": "简单",
    "answer": "A",
    "explanation": "详细解析：为什么A正确，其他选项为什么错误",
    "design_reason": "【必填】题目设计依据：说明本题考查哪个知识点，为什么这样设计题目，考查学生什么能力",
    "difficulty_reason": "【必填】难度层级说明：例如'本题属于简单难度，因为直接考查学生对XXX概念的记忆'",
    "knowledge_points": ["知识点1", "知识点2"],
    "options": [
      {{"content": "选项A的具体内容（不是'选项A'这样的占位符）", "is_correct": true}},
      {{"content": "选项B的具体内容", "is_correct": false}},
      {{"content": "选项C的具体内容", "is_correct": false}},
      {{"content": "选项D的具体内容", "is_correct": false}}
    ],
    "distractor_reasons": [
      {{"option": "B", "type": "概念混淆型", "reason": "【必填】说明为什么设置此干扰项，它是什么类型的干扰，针对学生的什么错误理解"}},
      {{"option": "C", "type": "常见误区型", "reason": "【必填】说明为什么设置此干扰项"}},
      {{"option": "D", "type": "过度概括型", "reason": "【必填】说明为什么设置此干扰项"}}
    ]
  }}
]
```

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

## 字段填写要求（重要！）

### difficulty（难度）- 必填
难度取值只能是：**简单**、**中等**、**困难** 三种之一，不能使用 L1、L2、L3 等其他格式。

### design_reason（题目设计依据）- 必填
说明本题的设计意图，例如：
- "本题考查CRH380动车空调系统的核心组成，通过对比不同车型的配置差异，考查学生对系统架构的理解"
- "本题设计目的是检验学生对隔离锁安全机制工作原理的掌握程度"

### difficulty_reason（难度层级说明）- 必填
说明为什么这道题属于该难度层级，例如：
- "简单难度：本题直接考查学生对CRH380空调系统组成的记忆，不需要理解或应用"
- "中等难度：本题需要学生理解电控系统的工作原理，并进行简单的逻辑推导"
- "困难难度：本题要求学生将隔离锁安全机制的知识应用到复杂故障场景中，需要综合分析"

### distractor_reasons（干扰项设计原因）- 选择题必填
**选择题的所有错误选项都必须填写干扰项原因！**

每个干扰项必须说明：
1. option：选项标识（如 B、C、D）
2. type：干扰类型（概念混淆型、过度概括型、以偏概全型、逆向思维型、常见误区型等）
3. reason：设计原因，针对学生的什么错误理解，为什么能起到干扰作用

例如：
```json
[
  {{"option": "B", "type": "概念混淆型", "reason": "学生常将空调系统的制冷剂类型与冷却液类型混淆，此干扰项针对这一常见错误"}},
  {{"option": "C", "type": "常见误区型", "reason": "学生容易误认为XXX，实际上应该是YYY，此干扰项针对这一误区"}},
  {{"option": "D", "type": "过度概括型", "reason": "学生可能将特例错误地推广到一般情况，此干扰项检验学生是否真正理解"}}
]
```

## 特别提醒

1. ⚠️ 必须生成 {total_count} 道题目，严格按照题型数量分配，不能多也不能少
2. 题目内容必须是真正的问题，不能是知识点的简单复述
3. 选项必须是具体的内容，不能是"正确描述"、"错误描述"这样的占位符
4. 每道题都要有完整的解析和设计原因
5. design_reason、difficulty_reason、distractor_reasons 必须填写完整
6. **选择题的所有错误选项都必须在 distractor_reasons 中说明干扰原因**

现在请开始生成 {total_count} 道高质量的考试题目："""
    
    return prompt

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
                
                error_pos = e.pos if hasattr(e, 'pos') else 4778
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

def generate_fallback_questions(
    knowledge_input: str,
    question_types: List[str],
    type_counts: Dict[str, int],
    difficulty_config: Dict[str, Any]
) -> List[Dict]:
    logger.warning("Kimi API调用失败，使用Fallback生成题目")
    
    questions = []
    difficulties = []
    for level, config in difficulty_config.items():
        for _ in range(config.get("count", 0)):
            difficulties.append(level)
    
    idx = 0
    for q_type in question_types:
        count = type_counts.get(q_type, 0)
        for i in range(count):
            diff = difficulties[idx] if idx < len(difficulties) else "中等"
            
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
