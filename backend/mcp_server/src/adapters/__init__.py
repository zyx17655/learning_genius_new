"""
适配器模块
包含各种AI模型的适配器
"""

from .base import BaseModelAdapter, ChatResponse, get_adapter, register_adapter, list_adapters

__all__ = [
    "BaseModelAdapter",
    "ChatResponse",
    "get_adapter",
    "register_adapter",
    "list_adapters"
]
