"""
数据库模型
定义MCP Server相关的数据库模型
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class McpCallLog(Base):
    """MCP调用日志表"""
    __tablename__ = "mcp_call_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    request_id = Column(String(36), index=True, comment="请求ID")
    call_type = Column(String(50), comment="调用类型")
    model_used = Column(String(100), comment="使用的模型")
    prompt_tokens = Column(Integer, default=0, comment="Prompt token数")
    completion_tokens = Column(Integer, default=0, comment="Completion token数")
    total_tokens = Column(Integer, default=0, comment="总token数")
    duration_ms = Column(Integer, comment="耗时(毫秒)")
    status = Column(String(20), comment="状态: success, failed")
    error_message = Column(Text, comment="错误信息")
    request_params = Column(Text, comment="请求参数JSON")
    response_result = Column(Text, comment="响应结果JSON")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
