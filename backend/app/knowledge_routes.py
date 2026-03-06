import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models import KnowledgeDocument, KnowledgeChunk
from app.knowledge_service import KnowledgeService

router = APIRouter()

class SearchRequest(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    limit: int = 5
    max_chars: int = 6000

@router.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    return {"code": 0, "data": service.get_all_documents()}

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.pdf', '.md', '.markdown', '.docx', '.doc', '.txt']:
        raise HTTPException(status_code=400, detail="Supported formats: PDF, Markdown, Word (.docx/.doc), TXT")
    
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base", "raw")
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        service = KnowledgeService(db)
        doc = service.process_document(file_path, file.filename)
        
        return {
            "code": 0,
            "message": "Document uploaded and processed successfully",
            "data": {
                "id": doc.id,
                "filename": doc.filename,
                "total_chunks": doc.total_chunks,
                "status": doc.status
            }
        }
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    if service.delete_document(document_id):
        return {"code": 0, "message": "Document deleted"}
    return {"code": 1, "message": "Document not found"}

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    return {"code": 0, "data": service.get_categories()}

@router.post("/search")
def search_knowledge(request: SearchRequest, db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    chunks = service.search_chunks(
        query=request.query,
        category=request.category,
        limit=request.limit,
        max_chars=request.max_chars
    )
    return {"code": 0, "data": chunks}

@router.get("/chunks/{category}")
def get_chunks_by_category(category: str, max_chars: int = 6000, db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    chunks = service.get_chunks_by_category(category, max_chars)
    return {"code": 0, "data": chunks}

@router.get("/stats")
def get_knowledge_stats(db: Session = Depends(get_db)):
    service = KnowledgeService(db)
    doc_count = service.get_document_count()
    chunk_count = service.get_chunk_count()
    categories = service.get_categories()
    
    return {
        "code": 0,
        "data": {
            "document_count": doc_count,
            "chunk_count": chunk_count,
            "category_count": len(categories),
            "categories": categories
        }
    }
