"""
出题服务
核心业务逻辑
"""

import json
import re
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger("services.question_gen")


class QuestionGenService:
    """出题服务"""

    def __init__(self):
        self.default_model = "kimi"

    async def generate(
        self,
        knowledge_input: str,
        question_types: List[str],
        type_counts: Dict[str, int],
        difficulty: str,
        rule_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """生成题目"""

        logger.info(f"生成题目: types={question_types}, counts={type_counts}, difficulty={difficulty}")

        # 导入并注册适配器
        from ..adapters import get_adapter
        from ..adapters.kimi_adapter import KimiAdapter
        from ..adapters.openai_adapter import OpenAIAdapter

        # 获取适配器
        adapter = get_adapter(self.default_model, {
            "api_key": "",
            "model_name": "kimi-k2-turbo-preview",
            "base_url": "https://api.moonshot.cn/v1"
        })
        await adapter.initialize()

        # 构建Prompt
        prompt = self._build_prompt(
            knowledge_input,
            question_types,
            type_counts,
            difficulty
        )

        # 调用模型
        response = await adapter.chat_completion(
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=32768
        )

        # 解析响应
        questions = self._parse_response(response.content)

        # 验证题目
        from .question_verify import VerifyService
        verify_service = VerifyService()
        verified_questions = []
        for q in questions:
            result = await verify_service.verify(
                question_content=q.get("content", ""),
                question_type=q.get("question_type", ""),
                answer=q.get("answer", ""),
                options=q.get("options", []),
                knowledge_context=knowledge_input
            )
            q["verification"] = result
            if result.get("is_valid", True):
                verified_questions.append(q)

        return {
            "questions": verified_questions,
            "statistics": self._calculate_statistics(verified_questions),
            "model_used": self.default_model,
            "tokens_used": response.usage.get("total_tokens", 0)
        }

    def _build_prompt(
        self,
        knowledge_input: str,
        question_types: List[str],
        type_counts: Dict[str, int],
        difficulty: str
    ) -> str:
        """构建Prompt"""

        difficulty_map = {
            "简单": "L1（基础知识点的直接记忆和理解）",
            "中等": "L2（知识点的简单应用和辨析）",
            "困难": "L3（知识点的综合运用和问题解决）"
        }

        difficulty_desc = difficulty_map.get(difficulty, difficulty_map["中等"])
        type_text = "、".join([f"{t}({count}题)" for t, count in type_counts.items() if count > 0])

        prompt = f"""你是一位专业的考试命题专家，精通教育学、认知心理学和测量学。

## 知识素材
{knowledge_input}

## 题目要求
- 题型：{type_text}
- 难度：{difficulty} - {difficulty_desc}
- 总题数：{sum(type_counts.values())}题

## 出题规范

### 单选题规范
1. 题干清晰明确，无歧义
2. 4个选项(A-D)，内容长度相近
3. 正确答案唯一
4. 干扰项有合理性，不是明显错误
5. 解析说明为什么选这个答案

### 多选题规范
1. 题干明确说明"以下哪些是正确的"等
2. 选项2-4个
3. 答案可能是一个或多个
4. 解析说明每个选项的正确与否原因

### 判断题规范
1. 陈述清晰，是非明确
2. 错误判断需要指出错误点
3. 解析说明判断依据

### 填空题规范
1. 空白处明确
2. 答案唯一或标准
3. 解析说明填空依据

### 主观题规范
1. 问题明确，答案有标准
2. 按要点给分
3. 解析说明评分标准

## 输出格式
请严格按照以下JSON格式返回，每道题包含所有字段：
```json
[
  {{
    "content": "题目内容，如：下列关于Python变量的说法，正确的是？",
    "question_type": "题型，如：单选",
    "difficulty": "难度",
    "answer": "正确答案，如：A",
    "explanation": "详细解析",
    "options": [
      {{"content": "选项A内容", "is_correct": true}},
      {{"content": "选项B内容", "is_correct": false}},
      {{"content": "选项C内容", "is_correct": false}},
      {{"content": "选项D内容", "is_correct": false}}
    ]
  }}
]
```

## 特别提醒
1. 必须严格生成指定数量的题目，不能多也不能少
2. 题目内容必须是有意义的问题，不能是知识点的简单复述
3. 选项必须具体明确，不能使用"正确"、"错误"等作为选项
4. 解析必须清晰说明答案原因
5. 必须输出有效的JSON数组格式

请开始生成："""

        return prompt

    def _get_system_prompt(self) -> str:
        """获取系统提示"""
        return """你是一位专业的考试命题专家，精通教育学、认知心理学和测量学。
请严格按照要求生成题目，确保题目质量达到专业考试标准。
必须严格按照要求的数量生成题目，不能多也不能少。
确保输出是有效的JSON格式数组。"""

    def _parse_response(self, content: str) -> List[Dict]:
        """解析AI响应"""
        try:
            logger.info(f"开始解析AI响应，内容长度: {len(content)}")

            json_start = content.find('[')
            json_end = content.rfind(']') + 1

            if json_start == -1 or json_end == 0:
                json_start = content.find('{')
                json_end = content.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                logger.error("未找到JSON对象")
                return []

            json_str = content[json_start:json_end]

            # 处理LaTeX转义
            json_str = self._fix_latex_escapes(json_str)

            questions = json.loads(json_str)
            if isinstance(questions, dict):
                questions = [questions]

            logger.info(f"成功解析出 {len(questions)} 道题目")
            return questions

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            logger.error(f"原始内容前200字符: {content[:200]}...")
            return []

    def _fix_latex_escapes(self, json_str: str) -> str:
        """修复LaTeX转义"""
        return json_str

    def _calculate_statistics(self, questions: List[Dict]) -> Dict:
        """计算统计信息"""
        stats = {
            "total": len(questions),
            "by_type": {},
            "by_difficulty": {},
            "verified": len(questions)
        }

        for q in questions:
            qt = q.get("question_type", "未知")
            diff = q.get("difficulty", "未知")

            stats["by_type"][qt] = stats["by_type"].get(qt, 0) + 1
            stats["by_difficulty"][diff] = stats["by_difficulty"].get(diff, 0) + 1

        return stats

    async def get_templates(self, question_type: str = None) -> List[Dict]:
        """获取题目模板"""
        templates = [
            {
                "type": "单选",
                "template": "下列关于{知识点}的说法，正确的是？",
                "options_count": 4,
                "example": "下列关于Python变量的说法，正确的是？\nA. 变量必须先声明后使用\nB. 变量可以随时改变类型\nC. 变量名区分大小写\nD. 变量不需要指定类型"
            },
            {
                "type": "多选",
                "template": "下列关于{知识点}的说法，正确的有？",
                "options_count": 4,
                "example": "下列关于Python列表的说法，正确的有？\nA. 列表是有序的可变序列\nB. 列表可以包含任意类型元素\nC. 列表索引从1开始\nD. 列表可以使用append方法添加元素"
            },
            {
                "type": "判断",
                "template": "判断以下关于{知识点}的说法是否正确。",
                "options_count": 0,
                "example": "Python中的列表是不可变的。"
            },
            {
                "type": "填空",
                "template": "请填写关于{知识点}的空白部分。",
                "options_count": 0,
                "example": "Python中使用___关键字来定义函数。"
            },
            {
                "type": "主观",
                "template": "请简述{知识点}的核心内容。",
                "options_count": 0,
                "example": "请简述面向对象编程的三大特性及其作用。"
            }
        ]

        if question_type:
            return [t for t in templates if t["type"] == question_type]

        return templates

    async def get_stats(self) -> Dict:
        """获取题库统计"""
        # 这里可以连接数据库获取真实统计
        return {
            "total_questions": 0,
            "by_type": {"单选": 0, "多选": 0, "判断": 0, "填空": 0, "主观": 0},
            "by_difficulty": {"简单": 0, "中等": 0, "困难": 0},
            "last_updated": datetime.now().isoformat()
        }
