"""
数据验证工具
"""

from typing import Tuple


def validate_question_request(data: dict) -> Tuple[bool, str]:
    """验证题目请求数据"""
    required_fields = ["knowledge_input", "question_types", "type_counts", "difficulty"]

    for field in required_fields:
        if field not in data:
            return False, f"缺少必需字段: {field}"

    if not isinstance(data.get("question_types"), list):
        return False, "question_types必须是数组"

    if not isinstance(data.get("type_counts"), dict):
        return False, "type_counts必须是对象"

    return True, ""
