"""
MCP Server配置
"""

import os
from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """模型配置"""
    enabled: bool = True
    api_key: str = ""
    base_url: str = ""
    model_name: str = ""
    capabilities: list = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=lambda: {
        "temperature": 0.7,
        "max_tokens": 32768
    })


@dataclass
class Settings:
    """MCP Server设置"""

    # 服务配置
    SERVER_NAME: str = "smart-question-generator"
    SERVER_VERSION: str = "1.0.0"
    SERVER_PORT: int = 8765

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_DATABASE: str = "lt_intelligent_teaching"

    # 默认模型
    DEFAULT_MODEL: str = "kimi"

    # 模型配置
    MODELS: Dict[str, ModelConfig] = field(default_factory=lambda: {
        "kimi": ModelConfig(
            enabled=True,
            api_key=os.getenv("KIMI_API_KEY", ""),
            base_url="https://api.moonshot.cn/v1",
            model_name="kimi-k2-turbo-preview",
            capabilities=["chat", "json_mode"],
            params={"temperature": 0.7, "max_tokens": 32768}
        ),
        "openai": ModelConfig(
            enabled=False,
            api_key=os.getenv("OPENAI_API_KEY", ""),
            base_url="https://api.openai.com/v1",
            model_name="gpt-4",
            capabilities=["chat", "function_call"],
            params={"temperature": 0.7, "max_tokens": 4096}
        ),
        "qwen": ModelConfig(
            enabled=False,
            api_key=os.getenv("DASHSCOPE_API_KEY", ""),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            model_name="qwen-max",
            capabilities=["chat"],
            params={"temperature": 0.7, "max_tokens": 8192}
        )
    })

    # 出题配置
    GENERATION_MAX_RETRIES: int = 3
    GENERATION_RETRY_DELAY: int = 2
    VERIFY_ALL: bool = True
    MIN_SCORE: int = 75

    @property
    def DATABASE_URL(self) -> str:
        """获取数据库URL"""
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}?charset=utf8mb4"
        )


# 全局设置实例
settings = Settings()
