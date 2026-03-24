"""
MCP工具处理器
处理各种工具调用请求
"""

import logging
from typing import Any, Dict

logger = logging.getLogger("mcp.handlers")


async def handle_tool_call(tool_name: str, arguments: Dict) -> Any:
    """处理工具调用"""

    logger.info(f"处理工具调用: {tool_name}, 参数: {arguments}")

    if tool_name == "generate_questions":
        from ..services.question_gen import QuestionGenService
        service = QuestionGenService()
        result = await service.generate(
            knowledge_input=arguments.get("knowledge_input"),
            question_types=arguments.get("question_types"),
            type_counts=arguments.get("type_counts"),
            difficulty=arguments.get("difficulty"),
            rule_id=arguments.get("rule_id")
        )
        return format_generation_result(result)

    elif tool_name == "verify_question":
        from ..services.question_verify import VerifyService
        service = VerifyService()
        result = await service.verify(
            question_content=arguments.get("question_content"),
            question_type=arguments.get("question_type"),
            answer=arguments.get("answer"),
            options=arguments.get("options", []),
            knowledge_context=arguments.get("knowledge_context", "")
        )
        return format_verification_result(result)

    elif tool_name == "get_question_templates":
        from ..services.question_gen import QuestionGenService
        service = QuestionGenService()
        templates = await service.get_templates(arguments.get("question_type"))
        return {"templates": templates}

    elif tool_name == "list_rules":
        from ..services.rule_service import RuleService
        service = RuleService()
        rules = await service.list_rules()
        return {"rules": rules}

    elif tool_name == "get_question_bank_stats":
        from ..services.question_gen import QuestionGenService
        service = QuestionGenService()
        stats = await service.get_stats()
        return {"stats": stats}

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


def format_generation_result(result: Dict) -> Dict:
    """格式化生成结果"""
    return {
        "success": True,
        "questions": result.get("questions", []),
        "statistics": result.get("statistics", {}),
        "message": f"成功生成 {len(result.get('questions', []))} 道题目",
        "model_used": result.get("model_used", "unknown"),
        "tokens_used": result.get("tokens_used", 0)
    }


def format_verification_result(result: Dict) -> Dict:
    """格式化验证结果"""
    return {
        "success": result.get("is_valid", True),
        "is_valid": result.get("is_valid", True),
        "score": result.get("total_score", 0),
        "scores": result.get("scores", {}),
        "issues": result.get("issues", []),
        "suggestions": result.get("suggestions", "")
    }
