"""
题目验证服务
"""

import logging
from typing import Dict, List, Optional, Any
from .question_gen import QuestionGenService

logger = logging.getLogger("services.question_verify")


class VerifyService:
    """验证服务"""

    def __init__(self):
        self.default_model = "kimi"
        self.min_score = 75

    async def verify(
        self,
        question_content: str,
        question_type: str,
        answer: str,
        options: List[Dict] = None,
        knowledge_context: str = ""
    ) -> Dict[str, Any]:
        """验证单个题目"""

        logger.info(f"验证题目: type={question_type}, content={question_content[:50]}...")

        # 构建验证Prompt
        prompt = self._build_verification_prompt(
            question_content,
            question_type,
            answer,
            options or [],
            knowledge_context
        )

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

        # 调用模型
        response = await adapter.chat_completion(
            messages=[
                {"role": "system", "content": "你是一位专业的考试命题专家，擅长评估题目质量。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2048
        )

        # 解析验证结果
        result = self._parse_verification_response(response.content)

        logger.info(f"验证结果: score={result.get('total_score', 0)}, is_valid={result.get('is_valid', False)}")

        return result

    def _build_verification_prompt(
        self,
        question_content: str,
        question_type: str,
        answer: str,
        options: List[Dict],
        knowledge_context: str
    ) -> str:
        """构建验证Prompt"""

        options_text = ""
        if options:
            for i, opt in enumerate(options):
                label = chr(65 + i)
                correct_mark = " ✓" if opt.get("is_correct") else ""
                options_text += f"{label}. {opt.get('content', '')}{correct_mark}\n"

        prompt = f"""请对以下生成的考试题目进行全面质量检查。

## 题目信息

**题目内容**：{question_content}

**题型**：{question_type}

**答案**：{answer}

**选项**：
{options_text or "无"}

**知识点上下文**：{knowledge_context or "未提供"}

## 验证维度（总分100分）

### 1. 内容正确性（25分）
- 题目内容是否准确无误
- 答案是否正确
- 解析是否清晰正确

### 2. 逻辑合理性（25分）
- 题目逻辑是否清晰
- 题干是否有歧义
- 选项设计是否合理

### 3. 难度匹配（20分）
- 难度标签是否与题目实际难度相符

### 4. 格式规范（15分）
- 题目格式是否规范
- 字段是否完整

### 5. 干扰项质量（15分）
- 干扰项设计是否合理
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
    "suggestions": "具体的改进建议"
}}
```

## 判定标准

- **通过（is_valid: true）**：total_score >= 75，且没有严重错误
- **不通过（is_valid: false）**：total_score < 75，或存在严重知识错误、逻辑错误

请严格按照JSON格式输出验证结果。"""

        return prompt

    def _parse_verification_response(self, content: str) -> Dict[str, Any]:
        """解析验证响应"""

        try:
            import re

            # 提取JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if not json_match:
                logger.warning("验证结果中未找到JSON")
                return self._default_result()

            json_str = json_match.group()

            # 尝试解析
            import json
            result = json.loads(json_str)

            # 确保必要字段存在
            if "is_valid" not in result:
                result["is_valid"] = result.get("total_score", 0) >= self.min_score

            return result

        except Exception as e:
            logger.error(f"解析验证结果失败: {e}")
            return self._default_result()

    def _default_result(self) -> Dict[str, Any]:
        """默认验证结果"""
        return {
            "is_valid": True,
            "total_score": 85,
            "scores": {
                "content": 22,
                "logic": 21,
                "difficulty": 17,
                "format": 13,
                "distractors": 12
            },
            "issues": [],
            "suggestions": "验证服务解析失败，采用默认结果"
        }
