"""
工具函数
"""

import logging
import sys

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """设置日志"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)

    return logger


def validate_question_request(data: dict) -> tuple:
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
