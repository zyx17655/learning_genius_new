from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import router
from app.ai_routes import router as ai_router
from app.knowledge_routes import router as knowledge_router
from app.rule_routes import router as rule_router
from app.ai_log_routes import router as ai_log_router

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
app.include_router(rule_router, prefix="/api/rule", tags=["规则管理"])
app.include_router(ai_log_router, prefix="/api", tags=["AI调用日志"])

@app.get("/")
def root():
    return {"message": "智能教学系统API", "version": "1.0.0"}
