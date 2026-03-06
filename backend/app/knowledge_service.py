import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy import or_

from app.database import get_db
from app.models import KnowledgeDocument, KnowledgeChunk
from app.knowledge_parser import PDFParser, MarkdownParser, WordParser, TxtParser

logger = logging.getLogger(__name__)

class KnowledgeService:
    def __init__(self, db):
        self.db = db
        self.pdf_parser = PDFParser(chunk_size=2000, overlap=200)
        self.md_parser = MarkdownParser(chunk_size=2000)
        self.word_parser = WordParser(chunk_size=2000)
        self.txt_parser = TxtParser(chunk_size=2000)
    
    def process_document(self, file_path: str, original_name: str) -> KnowledgeDocument:
        doc = KnowledgeDocument(
            filename=os.path.basename(file_path),
            original_name=original_name,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            file_type=os.path.splitext(original_name)[1].lower().replace('.', ''),
            status="processing"
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        
        try:
            file_ext = os.path.splitext(original_name)[1].lower()
            
            if file_ext == '.pdf':
                result = self.pdf_parser.parse_pdf(file_path)
            elif file_ext in ['.md', '.markdown']:
                result = self.md_parser.parse_markdown(file_path)
            elif file_ext in ['.docx', '.doc']:
                result = self.word_parser.parse_word(file_path)
            elif file_ext == '.txt':
                result = self.txt_parser.parse_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            if result.get("error"):
                doc.status = "failed"
                self.db.commit()
                raise Exception(result["error"])
            
            chunks_data = result.get("chunks", [])
            
            for idx, chunk_data in enumerate(chunks_data):
                chunk = KnowledgeChunk(
                    document_id=doc.id,
                    title=chunk_data.get("title", f"片段{idx+1}"),
                    content=chunk_data.get("content", ""),
                    category=chunk_data.get("category", "通用知识"),
                    keywords=chunk_data.get("keywords", ""),
                    page_number=chunk_data.get("page_number"),
                    chunk_index=idx,
                    char_count=chunk_data.get("char_count", 0)
                )
                self.db.add(chunk)
            
            doc.total_chunks = len(chunks_data)
            doc.status = "completed"
            doc.processed_at = datetime.now()
            self.db.commit()
            
            logger.info(f"Document {original_name} processed: {len(chunks_data)} chunks")
            return doc
        
        except Exception as e:
            doc.status = "failed"
            self.db.commit()
            logger.error(f"Error processing document: {str(e)}")
            raise
    
    def get_categories(self) -> List[str]:
        categories = self.db.query(KnowledgeChunk.category).distinct().all()
        return [c[0] for c in categories if c[0]]
    
    def search_chunks(
        self,
        query: str = None,
        category: str = None,
        limit: int = 5,
        max_chars: int = 6000
    ) -> List[Dict]:
        q = self.db.query(KnowledgeChunk)
        
        if category:
            q = q.filter(KnowledgeChunk.category == category)
        
        if query:
            q = q.filter(
                or_(
                    KnowledgeChunk.title.contains(query),
                    KnowledgeChunk.content.contains(query),
                    KnowledgeChunk.keywords.contains(query)
                )
            )
        
        chunks = q.limit(limit * 3).all()
        
        result = []
        total_chars = 0
        
        for chunk in chunks:
            if total_chars + chunk.char_count > max_chars:
                break
            
            result.append({
                "id": chunk.id,
                "title": chunk.title,
                "content": chunk.content,
                "category": chunk.category,
                "char_count": chunk.char_count
            })
            total_chars += chunk.char_count
        
        return result
    
    def get_chunks_by_category(self, category: str, max_chars: int = 6000) -> List[Dict]:
        chunks = self.db.query(KnowledgeChunk).filter(
            KnowledgeChunk.category == category
        ).all()
        
        result = []
        total_chars = 0
        
        for chunk in chunks:
            if total_chars + chunk.char_count > max_chars:
                break
            
            result.append({
                "id": chunk.id,
                "title": chunk.title,
                "content": chunk.content,
                "category": chunk.category,
                "char_count": chunk.char_count
            })
            total_chars += chunk.char_count
        
        return result
    
    def get_all_documents(self) -> List[Dict]:
        docs = self.db.query(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc()).all()
        return [
            {
                "id": doc.id,
                "filename": doc.filename,
                "original_name": doc.original_name,
                "file_size": doc.file_size,
                "file_type": doc.file_type,
                "status": doc.status,
                "total_chunks": doc.total_chunks,
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
                "processed_at": doc.processed_at.isoformat() if doc.processed_at else None
            }
            for doc in docs
        ]
    
    def get_chunk_count(self, category: str = None) -> int:
        q = self.db.query(KnowledgeChunk)
        if category:
            q = q.filter(KnowledgeChunk.category == category)
        return q.count()
    
    def get_document_count(self) -> int:
        return self.db.query(KnowledgeDocument).count()
    
    def delete_document(self, document_id: int) -> bool:
        doc = self.db.query(KnowledgeDocument).filter(KnowledgeDocument.id == document_id).first()
        if doc:
            if doc.file_path and os.path.exists(doc.file_path):
                os.remove(doc.file_path)
            self.db.delete(doc)
            self.db.commit()
            return True
        return False
