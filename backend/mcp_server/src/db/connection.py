"""
数据库连接管理
"""

import os
import sys
from typing import Generator

# 添加backend目录到路径以访问主系统的数据库
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def get_db():
    """获取数据库连接"""
    try:
        from app.database import SessionLocal
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except ImportError:
        # 如果无法导入主系统的数据库，返回None
        yield None


async def init_database():
    """初始化数据库"""
    logger.info("数据库初始化...")
    # 数据库初始化逻辑
    pass


# 兼容导入
from app.database import SessionLocal
