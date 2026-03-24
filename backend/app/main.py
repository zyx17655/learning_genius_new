from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import router
from app.ai_routes import router as ai_router
from app.knowledge_routes import router as knowledge_router
from app.ai_log_routes import router as ai_log_router
from app.rule_routes import router as rule_router
from app.compare_routes import router as compare_router
from app.mcp_routes import router as mcp_router
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logging.getLogger().handlers[0].stream.reconfigure(encoding='utf-8')

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="智能教学系统API",
    description="智能题库管理系统后端API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.include_router(ai_router, prefix="/api/ai", tags=["AI生成"])
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["知识库"])
app.include_router(ai_log_router, prefix="/api", tags=["AI调用日志"])
app.include_router(rule_router, prefix="/api/rule", tags=["规则管理"])
app.include_router(compare_router, prefix="/api/compare", tags=["题目对比"])
app.include_router(mcp_router, prefix="/api/mcp", tags=["MCP"])

@app.get("/")
def root():
    return {"message": "智能教学系统API", "version": "1.0.0"}
