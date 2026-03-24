# 标准MCP改造设计方案

## 一、项目概述

### 1.1 改造目标
将现有的业务特定MCP服务重构为符合行业标准的**Model Control Protocol (MCP)** 平台，具备以下特性：
- **标准化接口**：遵循RESTful API规范，支持MCP协议标准
- **多模型支持**：支持Kimi、OpenAI、Qwen等多种AI模型
- **模块化架构**：业务逻辑与模型控制分离
- **高可用性**：保证现有题库管理、规则管理等模块稳定运行

### 1.2 改造原则
- **平稳过渡**：新架构与现有业务并行运行，渐进迁移
- **功能隔离**：MCP核心功能与业务功能解耦
- **向后兼容**：保留现有API接口，确保前端功能正常
- **可扩展性**：预留插件机制，支持未来业务扩展

---

## 二、系统架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              前端应用 (Vue)                                    │
│   题库管理 | 规则管理 | AI生成 | 题目对比 | MCP日志 | MCP管理                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         API Gateway (5001端口)                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ 题库路由  │  │ 规则路由  │  │ AI生成路由 │  │ 对比路由  │  │ MCP路由   │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                    │                    │
                    ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           业务服务层 (Business Services)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ QuestionBank  │  │   RuleMgr    │  │ QuestionGen  │  │  ModelCtrl   │  │
│  │   Service     │  │   Service    │  │   Service    │  │   Service    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                                                 │
                                        ┌─────────────────────┴─────────────┐
                                        ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MCP Core (8765端口) - 新架构                          │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                           MCP Protocol Layer                            │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐       │ │
│  │  │   Model    │  │  Task      │  │   Config   │  │   Monitor   │       │ │
│  │  │  Registry  │  │  Scheduler │  │  Manager   │  │   Service   │       │ │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        Model Adapter Layer                              │ │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐           │ │
│  │  │  Kimi  │  │OpenAI │  │  Qwen  │  │ Claude │  │ Custom │           │ │
│  │  │Adapter │  │Adapter│  │Adapter │  │Adapter │  │Adapter │           │ │
│  │  └────────┘  └────────┘  └────────┘  └────────┘  └────────┘           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           External AI Providers                              │
│        Kimi API    │    OpenAI API    │    Qwen API    │    Claude API       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 目录结构设计

```
backend/
├── app/                              # 现有业务模块（保持不变）
│   ├── main.py                       # FastAPI主应用入口
│   ├── models.py                     # 数据库ORM模型
│   ├── ai_service.py                 # AI服务（业务层）
│   ├── ai_routes.py                  # AI路由
│   ├── question_bank_routes.py        # 题库路由
│   ├── rule_routes.py                # 规则路由
│   └── ...
│
├── mcp_server/                       # MCP服务（全新重构）
│   ├── __init__.py
│   ├── main.py                       # MCP主入口（端口8765）
│   │
│   ├── core/                         # MCP核心层
│   │   ├── __init__.py
│   │   ├── protocol.py               # MCP协议定义
│   │   ├── base.py                   # 基础类和接口
│   │   ├── registry.py               # 模型注册中心
│   │   ├── scheduler.py              # 任务调度器
│   │   ├── config_manager.py          # 配置管理器
│   │   └── monitor.py                # 监控服务
│   │
│   ├── adapters/                     # 模型适配器层
│   │   ├── __init__.py
│   │   ├── base_adapter.py           # 适配器基类
│   │   ├── kimi_adapter.py           # Kimi适配器
│   │   ├── openai_adapter.py         # OpenAI适配器
│   │   ├── qwen_adapter.py           # Qwen适配器
│   │   └── anthropic_adapter.py      # Anthropic/Claude适配器
│   │
│   ├── services/                     # MCP业务服务
│   │   ├── __init__.py
│   │   ├── question_gen_service.py  # 出题服务（从现有ai_service迁移）
│   │   ├── text_gen_service.py       # 文本生成服务
│   │   └── verify_service.py         # 验证服务
│   │
│   ├── api/                         # MCP API接口
│   │   ├── __init__.py
│   │   ├── v1/                      # API v1版本
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # 模型管理接口
│   │   │   ├── tasks.py             # 任务管理接口
│   │   │   ├── config.py            # 配置管理接口
│   │   │   └── monitor.py           # 监控接口
│   │   └── middleware.py            # 中间件
│   │
│   ├── db/                          # 数据库
│   │   ├── __init__.py
│   │   ├── mcp_models.py            # MCP相关数据库模型
│   │   └── migrations/               # 数据库迁移
│   │
│   ├── utils/                       # 工具函数
│   │   ├── __init__.py
│   │   ├── logger.py                # 日志工具
│   │   ├── crypto.py                # 加密工具
│   │   └── validators.py            # 数据验证
│   │
│   └── config/                      # 配置文件
│       ├── __init__.py
│       ├── settings.py              # MCP设置
│       └── models.yaml              # 模型配置文件
│
├── run.py                           # 现有主应用启动脚本（端口5001）
├── run_mcp.py                       # MCP服务启动脚本（端口8765）
└── requirements.txt                 # 依赖
```

---

## 三、核心模块设计

### 3.1 MCP Protocol Layer（协议层）

#### 3.1.1 模型注册中心 (ModelRegistry)

**职责**：
- 注册和发现可用的AI模型
- 管理模型元数据（名称、版本、能力描述）
- 维护模型状态（在线/离线/忙碌）
- 模型负载均衡

**核心接口**：
```python
class ModelRegistry:
    def register_model(self, model_info: ModelInfo) -> str:
        """注册新模型，返回模型ID"""

    def unregister_model(self, model_id: str) -> bool:
        """注销模型"""

    def get_model(self, model_id: str) -> Optional[ModelInfo]:
        """获取模型信息"""

    def list_models(self, filters: Dict = None) -> List[ModelInfo]:
        """列出所有可用模型"""

    def update_model_status(self, model_id: str, status: ModelStatus) -> bool:
        """更新模型状态"""

    def get_available_model(self, capabilities: List[str] = None) -> Optional[ModelInfo]:
        """获取可用的模型"""
```

#### 3.1.2 任务调度器 (TaskScheduler)

**职责**：
- 接收和创建任务
- 任务排队和优先级管理
- 任务状态跟踪
- 失败重试机制
- 负载均衡

**核心接口**：
```python
class TaskScheduler:
    def create_task(self, task_type: str, params: Dict, priority: int = 5) -> str:
        """创建新任务"""

    def get_task_status(self, task_id: str) -> TaskStatus:
        """获取任务状态"""

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""

    def list_tasks(self, filters: Dict = None) -> List[TaskInfo]:
        """列出任务"""

    def retry_task(self, task_id: str) -> str:
        """重试失败任务"""
```

#### 3.1.3 配置管理器 (ConfigManager)

**职责**：
- 集中管理模型配置
- API密钥安全管理
- 温度、token等参数配置
- 配置文件热更新

**核心接口**：
```python
class ConfigManager:
    def get_model_config(self, model_id: str) -> ModelConfig:
        """获取模型配置"""

    def update_model_config(self, model_id: str, config: ModelConfig) -> bool:
        """更新模型配置"""

    def validate_config(self, config: ModelConfig) -> bool:
        """验证配置有效性"""

    def reload_configs(self) -> bool:
        """重新加载配置"""
```

#### 3.1.4 监控服务 (MonitorService)

**职责**：
- 收集和报告系统指标
- API调用统计
- 错误率监控
- 响应时间追踪
- 健康检查

**核心接口**：
```python
class MonitorService:
    def record_request(self, model_id: str, duration_ms: int, success: bool):
        """记录请求"""

    def get_stats(self, time_range: str = "1h") -> Dict:
        """获取统计信息"""

    def get_health_status(self) -> HealthStatus:
        """获取健康状态"""

    def get_model_stats(self, model_id: str) -> ModelStats:
        """获取模型统计"""
```

### 3.2 Model Adapter Layer（适配器层）

#### 3.2.1 适配器基类

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseModelAdapter(ABC):
    """AI模型适配器基类"""

    def __init__(self, config: ModelConfig):
        self.config = config
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
        """聊天补全"""
        pass

    @abstractmethod
    async def validate_connection(self) -> bool:
        """验证连接"""
        pass

    def get_capabilities(self) -> List[str]:
        """获取模型能力"""
        return ["chat"]
```

#### 3.2.2 Kimi适配器

```python
class KimiAdapter(BaseModelAdapter):
    """Kimi模型适配器"""

    CAPABILITIES = ["chat", "function_call", "json_mode"]

    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = "https://api.moonshot.cn/v1"
        self.model_name = config.model_name or "kimi-k2-turbo-preview"

    async def initialize(self) -> bool:
        """初始化httpx客户端"""
        self.client = httpx.Client(timeout=180.0, verify=False)
        return True

    async def chat_completion(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> ChatResponse:
        """调用Kimi API"""
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

        if response.status_code == 200:
            result = response.json()
            return ChatResponse(
                content=result["choices"][0]["message"]["content"],
                usage=result.get("usage", {}),
                model=self.model_name
            )
        else:
            raise AdapterError(f"Kimi API error: {response.status_code}")
```

#### 3.2.3 其他适配器（OpenAI, Qwen, Anthropic）

结构类似，继承BaseModelAdapter，实现各自Provider的API调用逻辑。

### 3.3 Service Layer（服务层）

#### 3.3.1 出题服务 (QuestionGenService)

```python
class QuestionGenService:
    """出题业务服务"""

    def __init__(
        self,
        registry: ModelRegistry,
        scheduler: TaskScheduler,
        config_manager: ConfigManager
    ):
        self.registry = registry
        self.scheduler = scheduler
        self.config_manager = config_manager

    async def generate_questions(
        self,
        knowledge_input: str,
        question_types: List[str],
        type_counts: Dict[str, int],
        difficulty_config: Dict[str, Any],
        rule_id: Optional[int] = None,
        model_id: Optional[str] = None
    ) -> GenerationResult:
        """生成题目"""

        # 获取模型
        if model_id:
            model = self.registry.get_model(model_id)
        else:
            model = self.registry.get_available_model(["question_generation"])

        if not model:
            raise ServiceError("No available model")

        # 获取模型适配器
        adapter = self.config_manager.get_adapter(model.model_id)

        # 构建Prompt
        prompt = self._build_question_prompt(...)

        # 调用模型
        response = await adapter.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )

        # 解析和验证
        questions = self._parse_response(response.content)
        verified_questions = await self._verify_questions(questions, adapter)

        return GenerationResult(
            questions=verified_questions,
            model_used=model.model_id,
            token_usage=response.usage
        )

    async def _verify_questions(
        self,
        questions: List[Dict],
        adapter: BaseModelAdapter
    ) -> List[Dict]:
        """验证题目"""
        verified = []
        for q in questions:
            verification = await self._verify_single_question(q, adapter)
            if verification.is_valid:
                verified.append(q)
            else:
                # 记录问题
                logger.warning(f"Question verification failed: {verification.issues}")
        return verified
```

---

## 四、API接口设计

### 4.1 MCP API v1

#### 4.1.1 模型管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/models | 列出所有模型 |
| POST | /api/v1/models | 注册新模型 |
| GET | /api/v1/models/{model_id} | 获取模型详情 |
| PUT | /api/v1/models/{model_id} | 更新模型配置 |
| DELETE | /api/v1/models/{model_id} | 删除模型 |
| POST | /api/v1/models/{model_id}/enable | 启用模型 |
| POST | /api/v1/models/{model_id}/disable | 禁用模型 |

#### 4.1.2 任务管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/tasks | 创建任务 |
| GET | /api/v1/tasks | 列出任务 |
| GET | /api/v1/tasks/{task_id} | 获取任务详情 |
| POST | /api/v1/tasks/{task_id}/cancel | 取消任务 |
| POST | /api/v1/tasks/{task_id}/retry | 重试任务 |

#### 4.1.3 配置管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/config/models | 获取所有模型配置 |
| PUT | /api/v1/config/models/{model_id} | 更新模型配置 |
| POST | /api/v1/config/reload | 重新加载配置 |

#### 4.1.4 监控接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/monitor/stats | 获取统计信息 |
| GET | /api/v1/monitor/health | 健康检查 |
| GET | /api/v1/monitor/models/{model_id}/stats | 获取模型统计 |

#### 4.1.5 业务接口（出题）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/generate/questions | 生成题目 |
| GET | /api/v1/generate/tasks/{task_id}/status | 获取生成任务状态 |
| GET | /api/v1/generate/tasks/{task_id}/questions | 获取生成的题目 |

### 4.2 响应格式

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": { },
  "timestamp": "2026-03-24T10:30:00Z",
  "request_id": "req_xxx"
}
```

### 4.3 错误格式

```json
{
  "success": false,
  "code": 1001,
  "message": "Model not found",
  "error": {
    "details": "The requested model_id 'xxx' does not exist",
    "suggestion": "Please check the model_id or register the model first"
  },
  "timestamp": "2026-03-24T10:30:00Z",
  "request_id": "req_xxx"
}
```

---

## 五、数据库设计

### 5.1 新增数据库表

#### mcp_models - 模型配置表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(36) | 模型ID (UUID) |
| name | VARCHAR(100) | 模型名称 |
| provider | VARCHAR(50) | 提供商 (kimi/openai/qwen/anthropic) |
| model_name | VARCHAR(100) | 底层模型名称 |
| api_key_encrypted | TEXT | 加密的API密钥 |
| api_base_url | VARCHAR(255) | API基础URL |
| capabilities | JSON | 模型能力列表 |
| default_params | JSON | 默认参数配置 |
| is_enabled | BOOLEAN | 是否启用 |
| is_default | BOOLEAN | 是否为默认模型 |
| status | VARCHAR(20) | 状态 (online/offline/busy) |
| priority | INT | 优先级 |
| config | JSON | 其他配置 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### mcp_tasks - 任务表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(36) | 任务ID (UUID) |
| task_type | VARCHAR(50) | 任务类型 |
| model_id | VARCHAR(36) | 使用的模型ID |
| status | VARCHAR(20) | 状态 |
| priority | INT | 优先级 |
| input_params | JSON | 输入参数 |
| output_result | JSON | 输出结果 |
| error_message | TEXT | 错误信息 |
| retry_count | INT | 重试次数 |
| started_at | DATETIME | 开始时间 |
| completed_at | DATETIME | 完成时间 |
| created_at | DATETIME | 创建时间 |

#### mcp_call_logs - 调用日志表（增强）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| request_id | VARCHAR(36) | 请求ID |
| model_id | VARCHAR(36) | 模型ID |
| task_id | VARCHAR(36) | 任务ID |
| call_type | VARCHAR(50) | 调用类型 |
| prompt_tokens | INT | Prompt token数 |
| completion_tokens | INT | Completion token数 |
| total_tokens | INT | 总token数 |
| duration_ms | INT | 耗时(毫秒) |
| status | VARCHAR(20) | 状态 |
| error_message | TEXT | 错误信息 |
| created_at | DATETIME | 创建时间 |

---

## 六、改造实施计划

### 6.1 阶段一：基础架构搭建（1-2周）

**目标**：搭建MCP核心框架，实现基础功能

**任务**：
1. 创建新的目录结构
2. 实现MCP Core模块
   - 基础类和接口定义
   - ModelRegistry（模型注册中心）
   - ConfigManager（配置管理器）
   - 基础的日志和监控
3. 实现Model Adapter Layer
   - BaseAdapter基类
   - KimiAdapter适配器
4. 搭建API框架
   - API v1路由定义
   - 中间件（认证、日志、错误处理）
5. 创建数据库模型
6. 编写单元测试

**交付物**：
- 新的MCP服务框架
- 可用的Kimi适配器
- 基本的API接口

### 6.2 阶段二：业务迁移（1-2周）

**目标**：迁移现有业务逻辑，验证功能正确性

**任务**：
1. 迁移QuestionGenService（出题服务）
2. 实现TaskScheduler（任务调度器）
3. 迁移和增强验证逻辑
4. 实现MonitorService（监控服务）
5. 迁移API接口到新架构
6. 集成测试

**交付物**：
- 完整的出题服务
- 任务调度系统
- 监控和日志功能

### 6.3 阶段三：多模型支持（1周）

**目标**：实现其他模型适配器

**任务**：
1. 实现OpenAI适配器
2. 实现Qwen适配器
3. 实现Anthropic适配器
4. 实现适配器的动态切换
5. 测试和优化

**交付物**：
- 多模型支持
- 模型负载均衡

### 6.4 阶段四：优化与文档（1周）

**目标**：性能优化和文档完善

**任务**：
1. 性能优化
2. 安全性增强
3. API文档完善
4. 编写使用手册
5. 部署脚本优化
6. 演练和测试

**交付物**：
- 生产可用的MCP服务
- 完整的文档
- 部署指南

---

## 七、兼容性设计

### 7.1 向后兼容

**现有API兼容**：
- 保留 `/api/mcp/logs` 接口
- 保留 `/api/mcp/stats` 接口
- 新增 `/api/mcp/generate` 接口兼容现有调用方式

**数据库兼容**：
- 保留现有的 `mcp_call_logs` 表结构
- 新增表使用新命名避免冲突
- 不修改现有业务表

### 7.2 渐进式迁移

**迁移策略**：
1. 新架构并行部署，不影响现有服务
2. 逐步将业务迁移到新架构
3. 保留旧接口作为备份
4. 确认无误后关闭旧接口

---

## 八、风险和对策

| 风险 | 影响 | 对策 |
|------|------|------|
| 改造影响现有业务 | 高 | 并行部署，充分测试 |
| 多模型适配复杂性 | 中 | 先实现Kimi，验证架构后再扩展 |
| 性能下降 | 中 | 代码优化，缓存机制 |
| 数据库迁移 | 中 | 保留旧表，逐步迁移 |
| API兼容性问题 | 低 | 保留旧接口，逐个验证 |

---

## 九、预期成果

### 9.1 功能成果

- ✅ 标准化的MCP协议实现
- ✅ 多模型支持（Kimi、OpenAI、Qwen、Anthropic）
- ✅ 完整的任务管理和调度系统
- ✅ 集中的模型配置和监控
- ✅ 向后兼容的API接口
- ✅ 详细的日志和统计

### 9.2 技术成果

- ✅ 模块化的架构设计
- ✅ 插件式的模型适配器
- ✅ 高可用的服务设计
- ✅ 完善的测试覆盖
- ✅ 详细的开发文档

---

## 十、后续扩展方向

1. **Function Calling支持**：支持AI模型调用外部函数
2. **流式输出**：支持Server-Sent Events流式响应
3. **缓存层**：引入Redis缓存常用结果
4. **微服务化**：拆分为独立的微服务
5. **Kubernetes部署**：容器化和自动扩缩容

---

## 十一、总结

本设计方案遵循以下原则：

1. **标准化**：采用业界标准的MCP协议设计
2. **模块化**：清晰的层次划分，便于维护和扩展
3. **兼容性**：保证现有业务稳定，平滑过渡
4. **可扩展**：预留扩展接口，支持未来业务发展
5. **可观测**：完善的监控和日志，便于问题排查

请审阅此设计方案，如有需要调整的地方请反馈，我将根据您的意见进行修改。
