"""
Kimi模型适配器
"""

import httpx
from typing import List, Dict, Any
from .base import BaseModelAdapter, ChatResponse, register_adapter
import logging

logger = logging.getLogger("adapters.kimi")


class KimiAdapter(BaseModelAdapter):
    """Kimi模型适配器"""

    CAPABILITIES = ["chat", "json_mode"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.base_url = config.get("base_url", "https://api.moonshot.cn/v1")
        self.model_name = config.get("model_name", "kimi-k2-turbo-preview")

    async def initialize(self) -> bool:
        """初始化"""
        try:
            self.client = httpx.Client(timeout=180.0, verify=False)
            logger.info(f"KimiAdapter initialized with model: {self.model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize KimiAdapter: {e}")
            return False

    async def chat_completion(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> ChatResponse:
        """发送聊天请求"""

        if not self.client:
            await self.initialize()

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

        logger.info(f"Kimi API request: model={self.model_name}, messages={len(messages)}")

        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                error_msg = f"Kimi API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            result = response.json()
            logger.info(f"Kimi API response: usage={result.get('usage', {})}")

            return ChatResponse(
                content=result["choices"][0]["message"]["content"],
                usage=result.get("usage", {}),
                model=self.model_name,
                finish_reason=result["choices"][0].get("finish_reason")
            )

        except httpx.TimeoutException:
            logger.error("Kimi API timeout")
            raise RuntimeError("Kimi API request timeout")
        except Exception as e:
            logger.error(f"Kimi API error: {e}")
            raise

    async def validate_connection(self) -> bool:
        """验证连接"""
        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": "Hi"}],
                    "max_tokens": 10
                }
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Kimi connection validation failed: {e}")
            return False


register_adapter("kimi", KimiAdapter)
