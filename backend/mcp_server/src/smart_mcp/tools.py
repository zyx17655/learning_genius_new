"""
MCP工具定义
定义智能出题可用的工具
"""

import logging
from typing import Any

logger = logging.getLogger("mcp.tools")

TOOLS = [
    {
        "name": "generate_questions",
        "description": "根据知识素材生成考试题目，支持单选题、多选题、判断题、填空题和主观题",
        "inputSchema": {
            "type": "object",
            "properties": {
                "knowledge_input": {
                    "type": "string",
                    "description": "知识素材内容，包含需要考查的知识点"
                },
                "question_types": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["单选", "多选", "判断", "填空", "主观"]
                    },
                    "description": "题目类型列表"
                },
                "type_counts": {
                    "type": "object",
                    "description": "各题型数量，如 {'单选': 5, '判断': 3}",
                    "additionalProperties": {"type": "integer"}
                },
                "difficulty": {
                    "type": "string",
                    "enum": ["简单", "中等", "困难"],
                    "description": "题目难度"
                },
                "rule_id": {
                    "type": "integer",
                    "description": "可选，使用的规则ID，不传则使用默认规则"
                }
            },
            "required": ["knowledge_input", "question_types", "type_counts", "difficulty"]
        }
    },
    {
        "name": "verify_question",
        "description": "验证单个题目的质量，返回评分、问题列表和改进建议",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question_content": {
                    "type": "string",
                    "description": "题目内容"
                },
                "question_type": {
                    "type": "string",
                    "description": "题型，如'单选'、'多选'等"
                },
                "answer": {
                    "type": "string",
                    "description": "正确答案"
                },
                "options": {
                    "type": "array",
                    "description": "选项列表（选择题需要）",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string", "description": "选项内容"},
                            "is_correct": {"type": "boolean", "description": "是否正确"}
                        }
                    }
                },
                "knowledge_context": {
                    "type": "string",
                    "description": "知识点上下文，用于验证题目是否与知识点相关"
                }
            },
            "required": ["question_content", "question_type", "answer"]
        }
    },
    {
        "name": "get_question_templates",
        "description": "获取题目模板列表，帮助了解不同题型的标准格式",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question_type": {
                    "type": "string",
                    "enum": ["单选", "多选", "判断", "填空", "主观"],
                    "description": "题目类型，不传则返回所有模板"
                }
            }
        }
    },
    {
        "name": "list_rules",
        "description": "获取可用的出题规则列表，返回规则ID和名称",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_question_bank_stats",
        "description": "获取题库统计信息，包括各题型数量、难度分布等",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def get_tool_definitions():
    """获取工具定义列表"""
    return TOOLS


def get_tool_by_name(name: str):
    """根据名称获取工具定义"""
    for tool in TOOLS:
        if tool["name"] == name:
            return tool
    return None
