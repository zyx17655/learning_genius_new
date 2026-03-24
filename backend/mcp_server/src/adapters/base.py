"""
模型适配器基类
定义统一的接口规范
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger("adapters.base")


@dataclass
class ChatResponse:
    """聊天响应"""
    content: str
    usage: Dict[str, int]
    model: str
    finish_reason: Optional[str] = None


class BaseModelAdapter(ABC):
    """模型适配器基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = config.get("api_key", "")
        self.model_name = config.get("model_name", "")
        self.base_url = config.get("base_url", "")
        self.capabilities = config.get("capabilities", [])
        self.params = config.get("params", {})
        self.client = None

    @abstractmethod
    async def initialize(self) -> bool:
        """初始化适配器"""
        pass

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> ChatResponse:
        """发送聊天请求"""
        pass

    @abstractmethod
    async def validate_connection(self) -> bool:
        """验证连接"""
        pass

    def get_capabilities(self) -> List[str]:
        """获取模型能力"""
        return self.capabilities

    def supportsCapability(self, capability: str) -> bool:
        """检查是否支持某项能力"""
        return capability in self.capabilities


_ADAPTERS = {}


def register_adapter(name: str, adapter_class):
    """注册适配器"""
    _ADAPTERS[name] = adapter_class
    logger.info(f"Registered adapter: {name}")


def get_adapter(name: str, config: Dict = None) -> 'BaseModelAdapter':
    """获取适配器"""
    if name not in _ADAPTERS:
        raise ValueError(f"Unknown adapter: {name}. Available: {list(_ADAPTERS.keys())}")

    adapter_class = _ADAPTERS[name]
    adapter = adapter_class(config or {})
    return adapter


def list_adapters() -> List[str]:
    """列出所有适配器"""
    return list(_ADAPTERS.keys())
