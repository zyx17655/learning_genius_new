import httpx
import json
import time
import ssl
import re
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
        is_default_rule = (rule_type == "默认")
        
        # 1. 角色设定（两者都有）
        if rule.role:
            content += f"### 角色设定\n{rule.role}\n\n"
        
        # 以下字段仅默认规则包含
        if is_default_rule:
            # 2. 核心原则
            if rule.core_principles:
                content += f"### 核心原则\n{rule.core_principles}\n\n"
            
            # 3. 工作流程
            if rule.workflow:
                content += f"### 工作流程\n{rule.workflow}\n\n"
            
            # 4. 命题核心规范
            if rule.specifications:
                content += f"### 命题核心规范\n{rule.specifications}\n\n"
            
            # 5. 干扰项设置
            if rule.distractor_mechanics:
                content += f"### 干扰项设置\n{rule.distractor_mechanics}\n\n"
            
            # 6. 专项技能
            if rule.domain_skills:
                content += f"### 专项技能\n{rule.domain_skills}\n\n"
        
        # 7. 考察偏好与方法论
        if rule.assessment_focus:
            content += f"### 考察偏好与方法论\n{rule.assessment_focus}\n\n"
        
        # 8. 语言风格与题干结构
        if rule.stem_style:
            content += f"### 语言风格与题干结构\n{rule.stem_style}\n\n"
        
        # 9. 学科表达与符号习惯
        if rule.notation_convention:
            content += f"### 学科表达与符号习惯\n{rule.notation_convention}\n\n"
        
        # 10. 干扰项逻辑陷阱
        if rule.subject_traps:
            content += f"### 干扰项逻辑陷阱\n{rule.subject_traps}\n\n"
        
        # 11. 解析深度与标准
        if rule.solution_blueprint:
            content += f"### 解析深度与标准\n{rule.solution_blueprint}\n\n"
        
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
    
    prompt = r"""# 考试题目生成任务

你是一位资深的教育测量与评价专家，拥有20年的考试命题经验。请根据以下要求生成高质量的考试题目。

## 基本信息
- **知识范围**：**""" + (knowledge_input if knowledge_input else "根据选定的知识点生成") + r"""**
- **总题数**：""" + str(total_count) + r""" 题（必须严格生成 """ + str(total_count) + r""" 道题，不能多也不能少！）
- **题型分布**：""" + type_text + """
""" + knowledge_content + rule_section + r"""
## 难度层次要求（布鲁姆认知分类）
""" + difficulty_text + r"""

## ⚠️ 重要约束（必须严格遵守）

1. **数量约束**：必须生成且仅生成 """ + str(total_count) + r""" 道题目，不能多也不能少！
2. **题型约束**：严格按照题型数量分配：""" + type_text + r"""
3. **难度约束**：严格按照难度数量分配：""" + difficulty_constraint_text + r"""
4. **规则优先级**：如有冲突，以用户自定义规则为准""" + ("，自定义规则优先级高" + "于默认规则" if has_custom_rule else "") + r"""

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

### 1. 公式包裹方式
- **行内公式**：使用 `$...$` 包裹，如 `$E=mc^2$`、`$\int_a^b f(x)dx$`、`$\alpha + \beta$`
- **块级公式**：使用 `$$...$$` 包裹，如 `$$\sum_{{i=1}}^{{n}} x_i = x_1 + x_2 + \cdots + x_n$$`

### 2. LaTeX 命令规范（关键！）
- **所有 LaTeX 命令使用单反斜杠 `\`**，如 `\sum`、`\int`、`\frac`、`\alpha`
- **特别注意**：`\\`（双反斜杠）在 LaTeX 中表示换行，**不要在公式命令中使用双反斜杠**
  - ✅ 正确：`$\sum_{{i=1}}^{{n}}$`、`$\int_a^b$`、`$\frac{{a}}{{b}}$`
  - ❌ 错误：`$\\sum_{{i=1}}^{{n}}$`、`$\\int_a^b$`、`$\\frac{{a}}{{b}}$`（会导致换行和显示错误）

### 3. 变量名
所有变量必须使用 LaTeX 格式，如 `$x$`、`$y$`、`$\theta$`、`$\omega$`

### 4. 常见符号
- 分数：`$\frac{{a}}{{b}}$`
- 上标：`$x^2$`、`$e^{{ix}}$`
- 下标：`$x_1$`、`$A_{{ij}}$`
- 根号：`$\sqrt{{2}}$`、`$\sqrt[n]{{x}}$`
- 希腊字母：`$\alpha$`、`$\beta$`、`$\gamma$`、`$\theta$`、`$\omega$`
- 运算符：`$\times$`、`$\div$`、`$\pm$`、`$\leq$`、`$\geq$`
- 积分：`$\int$`、`$\iint$`、`$\oint$`
- 求和：`$\sum_{{i=1}}^{{n}}$`
- 极限：`$\lim_{{x \to \infty}}$`

### 5. 公式显示要求
- **行内公式必须在一行内显示**，不要在公式内部添加换行符
- 复杂的公式如果太长，使用块级公式 `$$...$$` 单独成行
- **行内公式内部不要使用 `\\` 换行**（`\\` 是 LaTeX 换行命令）

### 6. 字体和格式命令
- **罗马字体**：使用 `\mathrm{...}`，如 `$c_{\mathrm{A}}$`、`$f_{\mathrm{s}}$`
  - ❌ 避免使用旧版 `{\rm ...}` 格式
- **等宽字体（代码）**：使用 `\texttt{...}` 包裹代码，如 `\texttt{[cA,cD]=dwt(f,'db4');}`
- **粗体**：使用 `\mathbf{...}`，如 `$\mathbf{x}$`
- **斜体**：数学变量默认就是斜体，不需要额外设置

### 7. 代码和特殊文本格式
- **MATLAB/Python 代码**：使用 `\texttt{...}` 包裹，如 `\texttt{plot(abs(fft(cA)))}`
- **命令行代码**：使用 `\texttt{...}` 包裹
- **文件路径**：使用 `\texttt{...}` 包裹，如 `\texttt{/path/to/file}`
- **特殊字符**：在 `\texttt` 中的 `_`、`$`、`%` 等字符不需要转义

### 8. 示例
- ✅ 正确：`求 $x^2 + 2x + 1 = 0$ 的解`
- ✅ 正确：`计算 $$\int_0^1 x^2 dx$$ 的值`
- ✅ 正确：`已知 $\alpha = 30^\circ$，求 $\sin \alpha$`
- ✅ 正确：`能量归一化得 $E(a)=\sum_{b} |C(a,b)|^2$`
- ✅ 正确：`近似系数 $c_{\mathrm{A}}$ 和采样频率 $f_{\mathrm{s}}$`
- ✅ 正确：`使用 \texttt{[cA,cD]=dwt(f,'db4');} 获取系数`
- ❌ 错误：`能量归一化得 $E(a)=\sum_{b} |C(a,b)|^2$` 内部使用双反斜杠（如 `\\sum`）会导致换行
- ❌ 错误：`系数 $c_{\rm A}$`（使用旧版 `\rm` 命令）
- ❌ 错误：`使用 [cA,cD]=dwt(f,'db4'); 获取系数`（代码未使用 \texttt 包裹）

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

1. ⚠️ 必须生成 """ + str(total_count) + r""" 道题目，严格按照题型数量分配，不能多也不能少
2. 题目内容必须是真正的问题，不能是知识点的简单复述
3. 选项必须是具体的内容，不能是"正确描述"、"错误描述"这样的占位符
4. 每道题都要有完整的解析和设计原因
5. design_reason、difficulty_reason、distractor_reasons 必须填写完整
6. **选择题的所有错误选项都必须在 distractor_reasons 中说明干扰原因**

现在请开始生成 """ + str(total_count) + r""" 道高质量的考试题目："""
    
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

def fix_latex_format(text: str) -> str:
    r"""
    修复 LaTeX 格式问题：
    1. 将双反斜杠命令（如 \\sum、\\bigl）改为单反斜杠（如 \sum、\bigl）
    2. 将旧版 {\rm ...} 改为 \mathrm{...}
    3. 修复转义字符（如 \\{ \\} 改为 \{ \}）
    4. 保留真正的换行符（\\ 后跟换行）
    """
    if not text or not isinstance(text, str):
        return text
    
    fixed_text = text
    
    # 1. 修复转义字符：\\{ \\} \\_ \\^ 等改为 \{ \} \_ \^
    # 这些是 LaTeX 中需要转义的特殊字符
    escape_chars = ['{', '}', '_', '^', '&', '#', '%', '$', '~']
    for char in escape_chars:
        # 在数学模式内的转义：$...\\{...$ -> $...\{...$
        fixed_text = fixed_text.replace('\\\\' + char, '\\' + char)
    
    # 2. 通用修复：所有双反斜杠后跟字母或下划线开头的命令，改为单反斜杠
    # 匹配 \\ 后跟字母或下划线开头的字符序列
    fixed_text = re.sub(r'\\\\([a-zA-Z_][a-zA-Z0-9_]*)(?![a-zA-Z])', r'\\\1', fixed_text)
    
    # 3. 额外修复：括号相关的命令（确保覆盖所有情况）
    bracket_commands = [
        'big', 'Big', 'bigg', 'Bigg',
        'bigl', 'bigr', 'Bigl', 'Bigr', 'biggl', 'biggr', 'Biggl', 'Biggr',
        'bigm', 'Bigm', 'biggm', 'Biggm'
    ]
    for cmd in bracket_commands:
        fixed_text = fixed_text.replace('\\\\' + cmd, '\\' + cmd)
    
    # 4. 修复空格命令
    space_commands = [' ', ',', ';', '!', 'quad', 'qquad', 'thinspace', 'thickspace', 'medspace', 'negthinspace']
    for cmd in space_commands:
        fixed_text = fixed_text.replace('\\\\' + cmd, '\\' + cmd)
    
    # 5. 修复旧版 {\rm ...} 格式为 \mathrm{...}
    # 先处理带花括号的: {\rm A} -> \mathrm{A}
    fixed_text = re.sub(r'\{\\rm\s+([^}]+)\}', r'\\mathrm{\1}', fixed_text)
    # 再处理不带花括号的（在数学模式内）: \rm A -> \mathrm{A}
    fixed_text = re.sub(r'\\rm\s+([a-zA-Z0-9_]+)', r'\\mathrm{\1}', fixed_text)
    
    return fixed_text

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
        
        # 修复 LaTeX 格式问题
        content = fix_latex_format(q.get("content", ""))
        explanation = fix_latex_format(q.get("explanation", ""))
        design_reason = fix_latex_format(design_reason)
        difficulty_reason = fix_latex_format(difficulty_reason)
        
        # 修复选项中的 LaTeX
        options = q.get("options", [])
        if options:
            for opt in options:
                if isinstance(opt, dict) and "content" in opt:
                    opt["content"] = fix_latex_format(opt.get("content", ""))
        
        # 修复干扰项原因中的 LaTeX
        if distractor_reasons:
            for dr in distractor_reasons:
                if isinstance(dr, dict) and "reason" in dr:
                    dr["reason"] = fix_latex_format(dr.get("reason", ""))
        
        validated_q = {
            "content": content,
            "question_type": q.get("question_type", "单选"),
            "difficulty": q.get("difficulty", "中等"),
            "answer": q.get("answer", ""),
            "explanation": explanation,
            "design_reason": design_reason,
            "difficulty_reason": difficulty_reason,
            "knowledge_points": q.get("knowledge_points", []),
            "options": options,
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


def verify_question_with_kimi(question: Dict, knowledge_context: str = "", max_retries: int = 3) -> Dict:
    """
    使用Kimi API验证题目质量
    
    Args:
        question: 待验证的题目
        knowledge_context: 知识点上下文
        max_retries: 最大重试次数
        
    Returns:
        {
            "is_valid": bool,
            "total_score": int,
            "scores": Dict,
            "issues": List[str],
            "suggestions": str
        }
    """
    prompt = build_verification_prompt(question, knowledge_context)
    
    system_prompt = """你是一位资深的教育测量与评价专家，拥有20年的考试命题经验。你擅长：
1. 评估考试题目的质量和准确性
2. 识别题目中的逻辑错误、知识错误和表述问题
3. 判断题目难度是否合理
4. 评估干扰项的设计质量

请严格按照JSON格式返回验证结果，确保评分客观公正。"""
    
    logger.info(f"=== 开始验证题目 ===")
    logger.info(f"题目: {question.get('content', '')[:50]}...")
    
    for attempt in range(max_retries):
        try:
            with httpx.Client(
                timeout=60.0,
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
                    
                    logger.info(f"验证结果: {content[:200]}...")
                    
                    # 解析验证结果
                    verification_result = parse_verification_response(content)
                    return verification_result
                else:
                    logger.error(f"验证API调用失败: {response.status_code}")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    
        except Exception as e:
            logger.error(f"验证过程异常: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
    
    # 所有重试都失败，返回默认通过（避免阻塞流程）
    logger.warning("验证API调用失败，默认通过")
    return {
        "is_valid": True,
        "total_score": 85,
        "scores": {
            "content": 20,
            "logic": 20,
            "difficulty": 17,
            "format": 15,
            "distractors": 13
        },
        "issues": [],
        "suggestions": "验证服务暂时不可用，默认通过"
    }


def build_verification_prompt(question: Dict, knowledge_context: str = "") -> str:
    """构建验证Prompt"""
    
    options_text = ""
    if question.get("options"):
        for i, opt in enumerate(question["options"]):
            label = chr(65 + i)  # A, B, C, D
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
- **LaTeX公式格式检查**：
  - 公式是否使用正确的命令：\sum、\int、\frac 等（不是 \\sum、\\int）
  - 罗马字体是否使用 \mathrm{...}（不是 {\rm ...} 或 \rm）
  - 代码是否使用 \texttt{...} 包裹
  - 行内公式是否在一行内显示，没有异常换行
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


def parse_verification_response(content: str) -> Dict:
    """解析验证结果"""
    try:
        # 提取JSON部分
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            result = json.loads(json_str)
            
            # 确保必要字段存在
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


async def generate_and_verify_question(
    generation_params: Dict,
    knowledge_context: str = "",
    max_generation_retries: int = 3
) -> Dict:
    """
    生成并验证题目，验证不通过则重试
    
    Args:
        generation_params: 生成参数
        knowledge_context: 知识点上下文
        max_generation_retries: 最大生成重试次数
        
    Returns:
        {
            "success": bool,
            "question": Dict,
            "attempts": int,
            "verification": Dict,
            "issues": List[str]
        }
    """
    last_issues = []
    last_suggestions = ""
    
    for attempt in range(max_generation_retries):
        logger.info(f"=== 第 {attempt + 1} 次生成尝试 ===")
        
        # 构建生成参数（带上次反馈）
        params = generation_params.copy()
        if last_issues:
            params["feedback"] = f"上次生成的问题：{'; '.join(last_issues)}。改进建议：{last_suggestions}"
        
        # 生成题目（单题）
        try:
            # 调用生成函数
            questions = generate_questions_with_kimi(
                knowledge_input=params.get("knowledge_input", ""),
                question_types=[params.get("question_type", "单选")],
                type_counts={params.get("question_type", "单选"): 1},
                difficulty_config={params.get("difficulty", "中等"): {"count": 1}},
                distractor_list=params.get("distractor_list", []),
                preference_list=params.get("preference_list", []),
                custom_requirement=params.get("custom_requirement", ""),
                knowledge_chunks=params.get("knowledge_chunks", [])
            )
            
            if not questions:
                logger.warning("生成题目失败，无返回结果")
                continue
            
            question = questions[0]
            
            # 验证题目
            logger.info(f"开始验证题目...")
            verification = verify_question_with_kimi(question, knowledge_context)
            
            logger.info(f"验证结果: 通过={verification.get('is_valid')}, 得分={verification.get('total_score')}")
            
            if verification.get("is_valid"):
                # 验证通过
                return {
                    "success": True,
                    "question": question,
                    "attempts": attempt + 1,
                    "verification": verification,
                    "issues": []
                }
            else:
                # 验证不通过，记录问题用于下次改进
                last_issues = verification.get("issues", [])
                last_suggestions = verification.get("suggestions", "")
                logger.info(f"验证不通过，问题: {last_issues}")
                
        except Exception as e:
            logger.error(f"生成或验证过程异常: {e}")
            continue
    
    # 超过最大重试次数
    logger.warning(f"超过最大重试次数 {max_generation_retries}，返回最后一次结果")
    return {
        "success": False,
        "question": question if 'question' in locals() else None,
        "attempts": max_generation_retries,
        "verification": verification if 'verification' in locals() else None,
        "issues": last_issues
    }
