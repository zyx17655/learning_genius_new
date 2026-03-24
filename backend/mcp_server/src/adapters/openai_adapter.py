"""
OpenAI模型适配器
"""

import httpx
from typing import List, Dict, Any
from .base import BaseModelAdapter, ChatResponse, register_adapter
import logging

logger = logging.getLogger("adapters.openai")


class OpenAIAdapter(BaseModelAdapter):
    """OpenAI模型适配器"""

    CAPABILITIES = ["chat", "function_call"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.base_url = config.get("base_url", "https://api.openai.com/v1")
        self.model_name = config.get("model_name", "gpt-4")

    async def initialize(self) -> bool:
        """初始化"""
        try:
            self.client = httpx.Client(timeout=180.0, verify=True)
            logger.info(f"OpenAIAdapter initialized with model: {self.model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize OpenAIAdapter: {e}")
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

        logger.info(f"OpenAI API request: model={self.model_name}, messages={len(messages)}")

        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            result = response.json()
            logger.info(f"OpenAI API response: usage={result.get('usage', {})}")

            return ChatResponse(
                content=result["choices"][0]["message"]["content"],
                usage=result.get("usage", {}),
                model=self.model_name,
                finish_reason=result["choices"][0].get("finish_reason")
            )

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
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
            logger.error(f"OpenAI connection validation failed: {e}")
            return False


register_adapter("openai", OpenAIAdapter)
