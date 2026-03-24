"""
规则服务
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("services.rule_service")


class RuleService:
    """规则服务"""

    def __init__(self):
        pass

    async def list_rules(self) -> List[Dict[str, Any]]:
        """获取规则列表"""

        # 默认规则
        default_rule = {
            "id": 1,
            "name": "默认规则",
            "description": "系统默认的出题规则",
            "is_default": True,
            "core_principles": [
                "题目内容必须准确无误",
                "答案必须唯一正确",
                "干扰项必须具有合理性"
            ]
        }

        rules = [default_rule]

        logger.info(f"返回 {len(rules)} 条规则")

        return rules

    async def get_rule(self, rule_id: int) -> Optional[Dict[str, Any]]:
        """获取指定规则"""

        if rule_id == 1:
            return {
                "id": 1,
                "name": "默认规则",
                "description": "系统默认的出题规则",
                "is_default": True,
                "core_principles": [
                    "题目内容必须准确无误",
                    "答案必须唯一正确",
                    "干扰项必须具有合理性"
                ],
                "workflow": "分析知识点 -> 设计题目 -> 生成选项 -> 验证质量",
                "specifications": {
                    "single_choice": {
                        "min_options": 4,
                        "max_options": 4,
                        "correct_only_one": True
                    },
                    "multi_choice": {
                        "min_options": 2,
                        "max_options": 4,
                        "correct_at_least_one": True
                    },
                    "true_false": {
                        "only_two_options": True
                    }
                }
            }

        return None

    async def get_default_rule(self) -> Optional[Dict[str, Any]]:
        """获取默认规则"""
        return await self.get_rule(1)
