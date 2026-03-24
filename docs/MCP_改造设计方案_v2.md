# 智能出题MCP Server - 标准MCP协议实现

## 一、项目概述

### 1.1 核心目标
将智能出题能力封装成符合**MCP (Model Context Protocol)** 协议标准的MCP Server，使其他AI应用（如Claude Desktop、Cursor、Coze等）可以通过标准协议直接调用出题功能，实现"即插即用"。

### 1.2 MCP协议简介

MCP（Model Context Protocol）是由Anthropic推出的开放标准协议，被称为"AI的USB-C接口"，具有以下特点：
- **标准化通信**：统一的JSON-RPC通信格式
- **工具调用**：AI模型可以通过MCP调用外部工具
- **资源访问**：AI模型可以访问外部数据资源
- **即插即用**：类似USB设备的即插即用体验

### 1.3 目标用户场景

```
┌─────────────────┐         ┌─────────────────┐
│  Claude Desktop  │         │     Cursor      │
└────────┬────────┘         └────────┬────────┘
         │                          │
         │   MCP Protocol (JSON-RPC) │
         │                          │
         └──────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │      智能出题 MCP Server (本题库)      │
    │  ┌─────────────────────────────────┐ │
    │  │  Tools:                          │ │
    │  │    - generate_questions          │ │
    │  │    - verify_question             │ │
    │  │    - get_question_templates      │ │
    │  │                                 │ │
    │  │  Resources:                     │ │
    │  │    - question://bank/stats       │ │
    │  │    - rule://list                │ │
    │  └─────────────────────────────────┘ │
    └───────────────────────────────────────┘
                    ▲
                    │
         ┌──────────┴───────────────┐
         │   Coze / 其他AI应用       │
         └───────────────────────────┘
```

---

## 二、技术架构设计

### 2.1 整体架构

```
┌────────────────────────────────────────────────────────────────────────┐
│                     智能出题 MCP Server                               │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   ┌──────────────────────────────────────────────────────────────┐   │
│   │                    MCP Protocol Layer                          │   │
│   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │
│   │   │ JSON-RPC    │  │   Tools     │  │  Resources  │          │   │
│   │   │   Handler   │  │   Handler   │  │   Handler   │          │   │
│   │   └─────────────┘  └─────────────┘  └─────────────┘          │   │
│   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │
│   │   │   Logging   │  │   History   │  │    Stats    │          │   │
│   │   └─────────────┘  └─────────────┘  └─────────────┘          │   │
│   └──────────────────────────────────────────────────────────────┘   │
│                                 │                                     │
│                                 ▼                                     │
│   ┌──────────────────────────────────────────────────────────────┐   │
│   │                    Business Logic Layer                       │   │
│   │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │   │
│   │   │  Question    │  │   Verify     │  │    Rule      │       │   │
│   │   │Generator     │  │  Service     │  │   Service    │       │   │
│   │   └──────────────┘  └──────────────┘  └──────────────┘       │   │
│   └──────────────────────────────────────────────────────────────┘   │
│                                 │                                     │
│                                 ▼                                     │
│   ┌──────────────────────────────────────────────────────────────┐   │
│   │                     Model Adapter Layer                        │   │
│   │   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐           │   │
│   │   │  Kimi  │  │OpenAI │  │  Qwen  │  │Claude  │           │   │
│   │   │Adapter │  │Adapter│  │Adapter │  │Adapter │           │   │
│   │   └────────┘  └────────┘  └────────┘  └────────┘           │   │
│   └──────────────────────────────────────────────────────────────┘   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 目录结构

```
question_mcp_server/
├── src/
│   ├── __init__.py
│   │
│   ├── main.py                      # MCP Server入口
│   │
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py                # MCP Server核心
│   │   ├── tools.py                 # 工具定义
│   │   ├── resources.py             # 资源定义
│   │   ├── handlers.py              # 请求处理器
│   │   └── prompts.py               # Prompt模板
│   │
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py                 # 适配器基类
│   │   ├── kimi_adapter.py         # Kimi适配器
│   │   ├── openai_adapter.py       # OpenAI适配器
│   │   ├── qwen_adapter.py          # Qwen适配器
│   │   └── anthropic_adapter.py     # Anthropic适配器
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── question_gen.py         # 出题服务
│   │   ├── question_verify.py      # 验证服务
│   │   └── rule_service.py          # 规则服务
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py               # 数据库模型
│   │   └── connection.py            # 数据库连接
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # 配置管理
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                # 日志工具
│       └── validators.py            # 数据验证
│
├── tests/
│   ├── __init__.py
│   ├── test_tools.py
│   ├── test_services.py
│   └── test_adapters.py
│
├── mcp_config.yaml                  # MCP Server配置文件
├── package.json                      # npm包配置（用于JS客户端）
├── pyproject.toml                    # Python包配置
├── uv.lock                          # 依赖锁定
├── Dockerfile                        # Docker容器化
├── docker-compose.yml               # Docker编排
│
├── README.md                        # 使用文档
└── INSTALL.md                       # 安装指南
```

---

## 三、MCP Server核心实现

### 3.1 MCP Server入口 (main.py)

```python
#!/usr/bin/env python3
"""
智能出题 MCP Server
Smart Question Generation MCP Server

基于MCP (Model Context Protocol) 协议的智能出题服务
其他AI应用可以通过标准MCP协议调用此服务
"""

import asyncio
import logging
from typing import Optional

# MCP SDK
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import ServerCapabilities, ToolsCapability, ResourcesCapability

from .config.settings import settings
from .mcp.tools import register_tools
from .mcp.resources import register_resources
from .db.connection import init_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("question_mcp_server")


class QuestionMCPServer:
    """智能出题MCP Server"""

    def __init__(self):
        self.server = Server(
            name="smart-question-generator",
            version="1.0.0",
            capabilities=ServerCapabilities(
                tools=ToolsCapability(),
                resources=ResourcesCapability()
            )
        )

    async def initialize(self):
        """初始化服务"""
        logger.info("初始化智能出题MCP Server...")

        # 初始化数据库
        await init_database()

        # 注册工具
        register_tools(self.server)

        # 注册资源
        register_resources(self.server)

        logger.info("MCP Server初始化完成")

    async def run(self):
        """运行服务"""
        await self.initialize()

        # 使用stdio方式运行（MCP标准方式）
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """主入口"""
    server = QuestionMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
```

### 3.2 工具定义 (tools.py)

```python
"""
MCP工具定义
定义智能出题可用的工具
"""

from typing import Any
from mcp.server import Server
from mcp.types import Tool, ToolInputSchema

# 工具定义
TOOLS = [
    Tool(
        name="generate_questions",
        description="根据知识素材生成考试题目",
        inputSchema=ToolInputSchema(
            type="object",
            properties={
                "knowledge_input": {
                    "type": "string",
                    "description": "知识素材内容，包含需要考查的知识点"
                },
                "question_types": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["单选", "多选", "判断", "填空", "主观"]},
                    "description": "题目类型列表"
                },
                "type_counts": {
                    "type": "object",
                    "description": "各题型数量，如 {\"单选\": 5, \"判断\": 3}",
                    "additionalProperties": {"type": "integer"}
                },
                "difficulty": {
                    "type": "string",
                    "enum": ["简单", "中等", "困难"],
                    "description": "题目难度"
                },
                "rule_id": {
                    "type": "integer",
                    "description": "可选，使用的规则ID"
                }
            },
            required: ["knowledge_input", "question_types", "type_counts", "difficulty"]
        )
    ),
    Tool(
        name="verify_question",
        description="验证单个题目的质量",
        inputSchema=ToolInputSchema(
            type="object",
            properties={
                "question_content": {"type": "string", "description": "题目内容"},
                "question_type": {"type": "string", "description": "题型"},
                "answer": {"type": "string", "description": "正确答案"},
                "options": {
                    "type": "array",
                    "description": "选项列表",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "is_correct": {"type": "boolean"}
                        }
                    }
                },
                "knowledge_context": {"type": "string", "description": "知识点上下文"}
            },
            required: ["question_content", "question_type", "answer"]
        )
    ),
    Tool(
        name="get_question_templates",
        description="获取题目模板列表",
        inputSchema=ToolInputSchema(
            type="object",
            properties={
                "question_type": {
                    "type": "string",
                    "enum": ["单选", "多选", "判断", "填空", "主观"],
                    "description": "题目类型"
                }
            }
        )
    ),
    Tool(
        name="list_rules",
        description="获取可用的出题规则列表",
        inputSchema=ToolInputSchema(
            type="object",
            properties={}
        )
    )
]


def register_tools(server: Server):
    """注册工具到MCP Server"""

    @server.list_tools()
    async def list_tools():
        """列出所有可用工具"""
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> Any:
        """调用工具"""
        from .handlers import handle_tool_call

        return await handle_tool_call(name, arguments)
```

### 3.3 工具处理器 (handlers.py)

```python
"""
MCP工具处理器
处理各种工具调用请求
"""

from typing import Any, Dict
from .services.question_gen import QuestionGenService
from .services.question_verify import VerifyService
from .services.rule_service import RuleService


async def handle_tool_call(tool_name: str, arguments: Dict) -> Any:
    """处理工具调用"""

    if tool_name == "generate_questions":
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
        service = QuestionGenService()
        templates = await service.get_templates(arguments.get("question_type"))
        return {"templates": templates}

    elif tool_name == "list_rules":
        service = RuleService()
        rules = await service.list_rules()
        return {"rules": rules}

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


def format_generation_result(result: Dict) -> Dict:
    """格式化生成结果"""
    return {
        "success": True,
        "questions": result.get("questions", []),
        "statistics": result.get("statistics", {}),
        "message": f"成功生成 {len(result.get('questions', []))} 道题目"
    }


def format_verification_result(result: Dict) -> Dict:
    """格式化验证结果"""
    return {
        "success": result.get("is_valid", True),
        "score": result.get("total_score", 0),
        "issues": result.get("issues", []),
        "suggestions": result.get("suggestions", ""),
        "details": result.get("scores", {})
    }
```

### 3.4 资源定义 (resources.py)

```python
"""
MCP资源定义
定义可访问的数据资源
"""

from typing import Any, AsyncIterator
from mcp.server import Server
from mcp.types import Resource, ResourceTemplate, TextResourceContents


def register_resources(server: Server):
    """注册资源到MCP Server"""

    @server.list_resources()
    async def list_resources() -> list[Resource]:
        """列出所有资源"""
        return [
            Resource(
                uri="question://bank/stats",
                name="question_bank_stats",
                description="题库统计信息",
                mimeType="application/json"
            ),
            Resource(
                uri="rule://list",
                name="rule_list",
                description="出题规则列表",
                mimeType="application/json"
            )
        ]

    @server.read_resource()
    async def read_resource(uri: str) -> Any:
        """读取资源"""
        from .services.rule_service import RuleService
        from .db.connection import get_db

        if uri == "question://bank/stats":
            db = next(get_db())
            stats = {
                "total_questions": db.query(Question).count(),
                "total_rules": db.query(QuestionRule).count(),
                "by_type": {},
                "by_difficulty": {}
            }
            return {"stats": stats}

        elif uri.startswith("rule://"):
            rule_id = uri.replace("rule://", "")
            service = RuleService()
            rule = await service.get_rule(rule_id)
            return rule

        raise ValueError(f"Unknown resource: {uri}")

    @server.list_resource_templates()
    async def list_resource_templates() -> list[ResourceTemplate]:
        """列出资源模板"""
        return [
            ResourceTemplate(
                uriTemplate="rule://{rule_id}",
                name="rule_detail",
                description="获取指定规则的详细信息",
                mimeType="application/json"
            )
        ]
```

---

## 四、业务服务实现

### 4.1 出题服务 (services/question_gen.py)

```python
"""
出题服务
核心业务逻辑
"""

import json
from typing import Dict, List, Optional, Any
from ..adapters import get_adapter
from ..config.settings import settings


class QuestionGenService:
    """出题服务"""

    def __init__(self):
        self.default_model = settings.DEFAULT_MODEL

    async def generate(
        self,
        knowledge_input: str,
        question_types: List[str],
        type_counts: Dict[str, int],
        difficulty: str,
        rule_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """生成题目"""

        # 获取模型适配器
        adapter = get_adapter(self.default_model)

        # 构建Prompt
        prompt = self._build_prompt(
            knowledge_input,
            question_types,
            type_counts,
            difficulty
        )

        # 调用模型
        response = await adapter.chat_completion(
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=32768
        )

        # 解析响应
        questions = self._parse_response(response.content)

        # 验证题目
        verified_questions = await self._verify_questions(questions, adapter)

        return {
            "questions": verified_questions,
            "statistics": self._calculate_statistics(verified_questions),
            "model_used": self.default_model,
            "tokens_used": response.usage.get("total_tokens", 0)
        }

    def _build_prompt(
        self,
        knowledge_input: str,
        question_types: List[str],
        type_counts: Dict[str, int],
        difficulty: str
    ) -> str:
        """构建Prompt"""
        type_text = "、".join([f"{t}({count}题)" for t, count in type_counts.items()])

        prompt = f"""请根据以下知识素材生成高质量的考试题目。

## 知识素材
{knowledge_input}

## 题目要求
- 题型：{type_text}
- 难度：{difficulty}
- 总题数：{sum(type_counts.values())}题

## 输出格式
请严格按照以下JSON格式返回：
```json
[
  {{
    "content": "题目内容",
    "question_type": "题型",
    "difficulty": "难度",
    "answer": "正确答案",
    "explanation": "详细解析",
    "options": [
      {{"content": "选项A内容", "is_correct": true}},
      {{"content": "选项B内容", "is_correct": false}}
    ]
  }}
]
```

请开始生成："""

        return prompt

    def _get_system_prompt(self) -> str:
        """获取系统提示"""
        return """你是一位专业的考试命题专家，精通教育学、认知心理学和测量学。
请严格按照要求生成题目，确保题目质量达到专业考试标准。
必须严格按照要求的数量生成题目，不能多也不能少。
确保输出是有效的JSON格式数组。"""

    def _parse_response(self, content: str) -> List[Dict]:
        """解析AI响应"""
        import re

        # 提取JSON
        json_start = content.find('[')
        json_end = content.rfind(']') + 1

        if json_start == -1 or json_end == 0:
            return []

        json_str = content[json_start:json_end]

        # 处理LaTeX转义
        json_str = self._fix_latex_escapes(json_str)

        try:
            questions = json.loads(json_str)
            if isinstance(questions, dict):
                questions = [questions]
            return questions
        except json.JSONDecodeError:
            return []

    def _fix_latex_escapes(self, json_str: str) -> str:
        """修复LaTeX转义"""
        # 移除字符串内的多余转义
        return json_str

    async def _verify_questions(
        self,
        questions: List[Dict],
        adapter
    ) -> List[Dict]:
        """验证题目"""
        verified = []
        verify_service = VerifyService()

        for q in questions:
            result = await verify_service.verify(
                question_content=q.get("content", ""),
                question_type=q.get("question_type", ""),
                answer=q.get("answer", ""),
                options=q.get("options", []),
                knowledge_context=""
            )

            q["verification"] = result
            if result.get("is_valid", True):
                verified.append(q)

        return verified

    def _calculate_statistics(self, questions: List[Dict]) -> Dict:
        """计算统计信息"""
        stats = {
            "total": len(questions),
            "by_type": {},
            "by_difficulty": {}
        }

        for q in questions:
            qt = q.get("question_type", "未知")
            diff = q.get("difficulty", "未知")

            stats["by_type"][qt] = stats["by_type"].get(qt, 0) + 1
            stats["by_difficulty"][diff] = stats["by_difficulty"].get(diff, 0) + 1

        return stats

    async def get_templates(self, question_type: str = None) -> List[Dict]:
        """获取题目模板"""
        templates = [
            {
                "type": "单选",
                "template": "下列关于{知识点}的说法，正确的是？",
                "options_count": 4
            },
            {
                "type": "多选",
                "template": "下列关于{知识点}的说法，正确的有？",
                "options_count": 4
            },
            {
                "type": "判断",
                "template": "判断以下关于{知识点}的说法是否正确。",
                "options_count": 0
            },
            {
                "type": "填空",
                "template": "请填写关于{知识点}的空白部分。",
                "options_count": 0
            },
            {
                "type": "主观",
                "template": "请简述{知识点}的核心内容。",
                "options_count": 0
            }
        ]

        if question_type:
            return [t for t in templates if t["type"] == question_type]

        return templates
```

---

## 五、适配器实现

### 5.1 适配器基类 (adapters/base.py)

```python
"""
模型适配器基类
定义统一的接口规范
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


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
        self.api_key = config.get("api_key")
        self.model_name = config.get("model_name")
        self.base_url = config.get("base_url")
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
        return ["chat"]


# 适配器注册表
_ADAPTERS = {}


def register_adapter(name: str, adapter_class):
    """注册适配器"""
    _ADAPTERS[name] = adapter_class


def get_adapter(name: str, config: Dict = None) -> BaseModelAdapter:
    """获取适配器"""
    if name not in _ADAPTERS:
        raise ValueError(f"Unknown adapter: {name}")

    adapter_class = _ADAPTERS[name]
    adapter = adapter_class(config or {})
    return adapter


def list_adapters() -> List[str]:
    """列出所有适配器"""
    return list(_ADAPTERS.keys())
```

### 5.2 Kimi适配器 (adapters/kimi_adapter.py)

```python
"""
Kimi模型适配器
"""

import httpx
from typing import List, Dict, Any
from .base import BaseModelAdapter, ChatResponse, register_adapter


class KimiAdapter(BaseModelAdapter):
    """Kimi模型适配器"""

    CAPABILITIES = ["chat", "json_mode"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://api.moonshot.cn/v1")
        self.model_name = config.get("model_name", "kimi-k2-turbo-preview")

    async def initialize(self) -> bool:
        """初始化"""
        self.client = httpx.Client(timeout=180.0, verify=False)
        return True

    async def chat_completion(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> ChatResponse:
        """发送聊天请求"""

        response = self.client.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
        )

        if response.status_code != 200:
            raise RuntimeError(f"Kimi API error: {response.status_code} - {response.text}")

        result = response.json()

        return ChatResponse(
            content=result["choices"][0]["message"]["content"],
            usage=result.get("usage", {}),
            model=self.model_name,
            finish_reason=result["choices"][0].get("finish_reason")
        )

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
        except Exception:
            return False


# 注册适配器
register_adapter("kimi", KimiAdapter)
```

---

## 六、安装和部署

### 6.1 本地安装

```bash
# 克隆项目
git clone https://github.com/your-org/question-mcp-server.git
cd question-mcp-server

# 使用uv安装
uv sync

# 配置环境变量
cp .env.example .env
# 编辑.env填入API密钥

# 运行
uv run python -m question_mcp_server
```

### 6.2 Docker部署

```yaml
# docker-compose.yml
version: '3.8'

services:
  question-mcp:
    build: .
    ports:
      - "8765:8765"
    environment:
      - KIMI_API_KEY=${KIMI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./data:/app/data
```

### 6.3 配置MCP客户端

#### Claude Desktop配置
```json
// ~/.config/claude-desktop/claude_desktop_config.json
{
  "mcpServers": {
    "question-generator": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "your-registry/question-mcp-server:latest"],
      "env": {
        "KIMI_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Cursor配置
在Cursor设置中添加MCP Server配置即可。

---

## 七、MCP Server配置

### 7.1 mcp_config.yaml

```yaml
# 智能出题MCP Server配置

server:
  name: "smart-question-generator"
  version: "1.0.0"
  description: "智能出题MCP Server - 基于MCP协议的标准化出题服务"

models:
  default: "kimi"

  kimi:
    enabled: true
    api_key: "${KIMI_API_KEY}"
    base_url: "https://api.moonshot.cn/v1"
    model_name: "kimi-k2-turbo-preview"
    capabilities:
      - "chat"
      - "json_mode"
    params:
      temperature: 0.7
      max_tokens: 32768

  openai:
    enabled: false
    api_key: "${OPENAI_API_KEY}"
    base_url: "https://api.openai.com/v1"
    model_name: "gpt-4"
    capabilities:
      - "chat"
      - "function_call"
    params:
      temperature: 0.7
      max_tokens: 4096

database:
  type: "mysql"
  url: "${DATABASE_URL}"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

generation:
  max_retries: 3
  retry_delay: 2
  verify_all: true
  min_score: 75
```

---

## 八、使用示例

### 8.1 Claude Desktop使用

```python
# 在Claude中直接调用MCP工具
# Claude: "请根据以下知识点出5道单选题：
#         Python基础语法包括变量、数据类型、条件语句和循环语句"

# Claude会自动调用MCP工具：
# tool: generate_questions
# arguments:
#   knowledge_input: "Python基础语法包括变量、数据类型、条件语句和循环语句"
#   question_types: ["单选"]
#   type_counts: {"单选": 5}
#   difficulty: "中等"
```

### 8.2 独立调用

```python
import httpx

# 通过stdio调用MCP Server
# MCP协议使用JSON-RPC over stdin/stdout

request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "generate_questions",
        "arguments": {
            "knowledge_input": "Python基础语法",
            "question_types": ["单选", "判断"],
            "type_counts": {"单选": 3, "判断": 2},
            "difficulty": "简单"
        }
    }
}
```

---

## 九、交付物清单

| 交付物 | 说明 |
|--------|------|
| MCP Server源代码 | 完整的Python实现 |
| Dockerfile | 容器化部署 |
| docker-compose.yml | Docker编排 |
| MCP配置文件 | mcp_config.yaml |
| 安装文档 | INSTALL.md |
| 使用文档 | README.md |
| API文档 | 标准的MCP协议文档 |
| 测试用例 | 单元测试和集成测试 |

---

## 十、后续扩展

1. **多语言SDK支持**：提供Python、JavaScript、Go等多语言SDK
2. **云市场发布**：发布到ModelScope、阿里云等平台
3. **认证授权**：支持API Key、OAuth等认证方式
4. **用量计费**：支持按调用量计费
5. **私有部署**：支持企业私有化部署

---

## 十一、总结

本方案将智能出题能力封装成符合**MCP协议标准**的MCP Server，核心特点：

1. **标准化**：完全遵循MCP (Model Context Protocol) 协议
2. **即插即用**：可被任何支持MCP的AI应用直接使用
3. **多模型支持**：预留多模型适配器接口
4. **易于部署**：支持Docker容器化部署
5. **功能完整**：包含出题、验证、模板等完整功能

其他系统只需配置MCP客户端，即可通过标准协议调用出题能力，无需关心内部实现。
