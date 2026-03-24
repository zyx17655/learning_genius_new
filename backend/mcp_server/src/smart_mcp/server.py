"""
Smart Question MCP Server
基于FastMCP的标准化MCP Server
支持stdio和HTTP两种模式
"""

import asyncio
import logging
import sys
import os
from typing import Any

# 添加src目录到路径
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("smart_mcp")

# MCP SDK导入
try:
    from mcp.server.fastmcp import FastMCP
    MCP_SDK_AVAILABLE = True
except ImportError:
    logger.error("MCP SDK not installed. Please run: pip install mcp")
    MCP_SDK_AVAILABLE = False


def create_mcp_server() -> FastMCP:
    """创建MCP服务器"""
    if not MCP_SDK_AVAILABLE:
        raise RuntimeError("MCP SDK not available")

    mcp = FastMCP(
        name="smart-question-generator",
        instructions="智能出题MCP Server - 基于MCP协议的标准化出题服务",
        host="0.0.0.0",
        port=8765
    )

    # 注册工具
    @mcp.tool()
    async def generate_questions(
        knowledge_input: str,
        question_types: list,
        type_counts: dict,
        difficulty: str,
        rule_id: int = None
    ) -> str:
        """
        根据知识素材生成考试题目

        Args:
            knowledge_input: 知识素材内容
            question_types: 题目类型列表，如["单选", "判断"]
            type_counts: 各题型数量，如{"单选": 5, "判断": 3}
            difficulty: 难度（简单/中等/困难）
            rule_id: 可选，规则ID

        Returns:
            生成的题目列表（JSON格式）
        """
        from services.question_gen import QuestionGenService

        logger.info(f"生成题目: types={question_types}, counts={type_counts}, difficulty={difficulty}")

        service = QuestionGenService()
        result = await service.generate(
            knowledge_input=knowledge_input,
            question_types=question_types,
            type_counts=type_counts,
            difficulty=difficulty,
            rule_id=rule_id
        )

        return str({
            "success": True,
            "questions": result.get("questions", []),
            "statistics": result.get("statistics", {}),
            "message": f"成功生成 {len(result.get('questions', []))} 道题目"
        })

    @mcp.tool()
    async def verify_question(
        question_content: str,
        question_type: str,
        answer: str,
        options: list = None,
        knowledge_context: str = ""
    ) -> str:
        """
        验证单个题目的质量

        Args:
            question_content: 题目内容
            question_type: 题型
            answer: 正确答案
            options: 选项列表
            knowledge_context: 知识点上下文

        Returns:
            验证结果（JSON格式）
        """
        from services.question_verify import VerifyService

        logger.info(f"验证题目: type={question_type}")

        service = VerifyService()
        result = await service.verify(
            question_content=question_content,
            question_type=question_type,
            answer=answer,
            options=options or [],
            knowledge_context=knowledge_context
        )

        return str({
            "success": result.get("is_valid", True),
            "score": result.get("total_score", 0),
            "issues": result.get("issues", []),
            "suggestions": result.get("suggestions", "")
        })

    @mcp.tool()
    async def get_question_templates(question_type: str = None) -> str:
        """
        获取题目模板

        Args:
            question_type: 可选，题型筛选

        Returns:
            题目模板列表
        """
        from services.question_gen import QuestionGenService

        service = QuestionGenService()
        templates = await service.get_templates(question_type)
        return str({"templates": templates})

    @mcp.tool()
    async def list_rules() -> str:
        """
        获取可用规则列表

        Returns:
            规则列表
        """
        from services.rule_service import RuleService

        service = RuleService()
        rules = await service.list_rules()
        return str({"rules": rules})

    @mcp.tool()
    async def get_question_bank_stats() -> str:
        """
        获取题库统计信息

        Returns:
            统计信息
        """
        from services.question_gen import QuestionGenService

        service = QuestionGenService()
        stats = await service.get_stats()
        return str({"stats": stats})

    return mcp


async def main():
    """主入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Smart Question MCP Server")
    parser.add_argument("--mode", choices=["stdio", "http", "sse"], default="stdio",
                        help="Server运行模式: stdio (MCP协议), http (HTTP), sse (SSE)")

    args = parser.parse_args()

    if not MCP_SDK_AVAILABLE:
        logger.error("MCP SDK not available, cannot start server")
        return

    mcp = create_mcp_server()

    logger.info(f"Starting Smart Question MCP Server in {args.mode} mode...")

    if args.mode == "stdio":
        await mcp.run_stdio_async()
    elif args.mode == "http":
        await mcp.run_streamable_http_async()
    elif args.mode == "sse":
        await mcp.run_sse_async()


if __name__ == "__main__":
    asyncio.run(main())
