import os
import re
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PDFParser:
    def __init__(self, chunk_size: int = 2000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def parse_pdf(self, file_path: str) -> Dict[str, Any]:
        try:
            import pdfplumber
        except ImportError:
            logger.error("pdfplumber not installed. Run: pip install pdfplumber")
            return {"error": "pdfplumber not installed", "chunks": []}
        
        chunks = []
        full_text = ""
        page_texts = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                total_pages = len(pdf.pages)
                logger.info(f"PDF has {total_pages} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""
                    page_texts.append({
                        "page": page_num,
                        "text": text
                    })
                    full_text += text + "\n"
                
                chapters = self._extract_chapters(page_texts)
                
                if chapters:
                    logger.info(f"Found {len(chapters)} chapters")
                    for chapter in chapters:
                        chapter_chunks = self._split_chapter_to_chunks(chapter)
                        chunks.extend(chapter_chunks)
                else:
                    logger.info("No chapters found, splitting by size")
                    chunks = self._split_by_size(full_text, page_texts)
        
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            return {"error": str(e), "chunks": []}
        
        return {
            "total_pages": total_pages,
            "total_chunks": len(chunks),
            "chunks": chunks
        }
    
    def _extract_chapters(self, page_texts: List[Dict]) -> List[Dict]:
        chapters = []
        current_chapter = None
        current_content = []
        current_start_page = 1
        
        chapter_patterns = [
            r'^第[一二三四五六七八九十百]+[章节篇部]\s*(.+)$',
            r'^[一二三四五六七八九十百]+[、.．]\s*(.+)$',
            r'^\d+[、.．]\s*(.+)$',
            r'^第\d+章\s*(.+)$',
            r'^Chapter\s*\d+[:：]?\s*(.+)$',
            r'^[A-Z][A-Za-z\s]+[:：]?\s*$',
        ]
        
        for page_data in page_texts:
            page_num = page_data["page"]
            text = page_data["text"]
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                is_chapter_title = False
                chapter_title = None
                
                for pattern in chapter_patterns:
                    match = re.match(pattern, line, re.IGNORECASE)
                    if match:
                        is_chapter_title = True
                        chapter_title = match.group(1).strip() if match.groups() else line
                        break
                
                if is_chapter_title and len(line) < 50:
                    if current_chapter:
                        chapters.append({
                            "title": current_chapter,
                            "content": "\n".join(current_content),
                            "start_page": current_start_page,
                            "end_page": page_num - 1
                        })
                    
                    current_chapter = chapter_title or line
                    current_content = []
                    current_start_page = page_num
                else:
                    current_content.append(line)
        
        if current_chapter and current_content:
            chapters.append({
                "title": current_chapter,
                "content": "\n".join(current_content),
                "start_page": current_start_page,
                "end_page": page_texts[-1]["page"]
            })
        
        return chapters
    
    def _split_chapter_to_chunks(self, chapter: Dict) -> List[Dict]:
        chunks = []
        content = chapter["content"]
        title = chapter["title"]
        
        if len(content) <= self.chunk_size:
            chunks.append({
                "title": title,
                "content": content,
                "category": title,
                "page_number": chapter.get("start_page", 1),
                "char_count": len(content)
            })
        else:
            sentences = re.split(r'([。！？\n])', content)
            sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
            
            current_chunk = ""
            chunk_index = 0
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) > self.chunk_size:
                    if current_chunk:
                        chunks.append({
                            "title": f"{title} ({chunk_index + 1})",
                            "content": current_chunk.strip(),
                            "category": title,
                            "page_number": chapter.get("start_page", 1),
                            "chunk_index": chunk_index,
                            "char_count": len(current_chunk)
                        })
                        chunk_index += 1
                    current_chunk = sentence
                else:
                    current_chunk += sentence
            
            if current_chunk:
                chunks.append({
                    "title": f"{title} ({chunk_index + 1})" if chunk_index > 0 else title,
                    "content": current_chunk.strip(),
                    "category": title,
                    "page_number": chapter.get("start_page", 1),
                    "chunk_index": chunk_index,
                    "char_count": len(current_chunk)
                })
        
        return chunks
    
    def _split_by_size(self, full_text: str, page_texts: List[Dict]) -> List[Dict]:
        chunks = []
        sentences = re.split(r'([。！？\n])', full_text)
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        "title": f"知识片段 {chunk_index + 1}",
                        "content": current_chunk.strip(),
                        "category": "通用知识",
                        "chunk_index": chunk_index,
                        "char_count": len(current_chunk)
                    })
                    chunk_index += 1
                current_chunk = sentence
            else:
                current_chunk += sentence
        
        if current_chunk:
            chunks.append({
                "title": f"知识片段 {chunk_index + 1}",
                "content": current_chunk.strip(),
                "category": "通用知识",
                "chunk_index": chunk_index,
                "char_count": len(current_chunk)
            })
        
        return chunks

class MarkdownParser:
    def __init__(self, chunk_size: int = 2000):
        self.chunk_size = chunk_size
    
    def parse_markdown(self, file_path: str) -> Dict[str, Any]:
        chunks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sections = self._extract_sections(content)
            
            for section in sections:
                if len(section["content"]) <= self.chunk_size:
                    chunks.append({
                        "title": section["title"],
                        "content": section["content"],
                        "category": section.get("category", section["title"]),
                        "char_count": len(section["content"])
                    })
                else:
                    sub_chunks = self._split_section(section)
                    chunks.extend(sub_chunks)
            
            return {
                "total_chunks": len(chunks),
                "chunks": chunks
            }
        
        except Exception as e:
            logger.error(f"Error parsing Markdown: {str(e)}")
            return {"error": str(e), "chunks": []}
    
    def _extract_sections(self, content: str) -> List[Dict]:
        sections = []
        lines = content.split('\n')
        current_section = {"title": "概述", "content": "", "level": 0}
        
        for line in lines:
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if header_match:
                if current_section["content"].strip():
                    sections.append(current_section)
                
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = {
                    "title": title,
                    "content": "",
                    "level": level,
                    "category": title
                }
            else:
                current_section["content"] += line + "\n"
        
        if current_section["content"].strip():
            sections.append(current_section)
        
        return sections
    
    def _split_section(self, section: Dict) -> List[Dict]:
        chunks = []
        content = section["content"]
        title = section["title"]
        
        sentences = re.split(r'([。！？\n])', content)
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        "title": f"{title} ({chunk_index + 1})",
                        "content": current_chunk.strip(),
                        "category": section.get("category", title),
                        "chunk_index": chunk_index,
                        "char_count": len(current_chunk)
                    })
                    chunk_index += 1
                current_chunk = sentence
            else:
                current_chunk += sentence
        
        if current_chunk:
            chunks.append({
                "title": f"{title} ({chunk_index + 1})" if chunk_index > 0 else title,
                "content": current_chunk.strip(),
                "category": section.get("category", title),
                "chunk_index": chunk_index,
                "char_count": len(current_chunk)
            })
        
        return chunks

class WordParser:
    def __init__(self, chunk_size: int = 2000):
        self.chunk_size = chunk_size
    
    def parse_word(self, file_path: str) -> Dict[str, Any]:
        try:
            from docx import Document
        except ImportError:
            logger.error("python-docx not installed. Run: pip install python-docx")
            return {"error": "python-docx not installed", "chunks": []}
        
        chunks = []
        
        try:
            doc = Document(file_path)
            
            sections = self._extract_sections(doc)
            
            for section in sections:
                if len(section["content"]) <= self.chunk_size:
                    chunks.append({
                        "title": section["title"],
                        "content": section["content"],
                        "category": section.get("category", section["title"]),
                        "char_count": len(section["content"])
                    })
                else:
                    sub_chunks = self._split_section(section)
                    chunks.extend(sub_chunks)
            
            return {
                "total_chunks": len(chunks),
                "chunks": chunks
            }
        
        except Exception as e:
            logger.error(f"Error parsing Word: {str(e)}")
            return {"error": str(e), "chunks": []}
    
    def _extract_sections(self, doc) -> List[Dict]:
        sections = []
        current_section = {"title": "概述", "content": "", "category": "概述"}
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            
            is_heading = False
            heading_title = None
            
            if para.style.name.startswith('Heading'):
                is_heading = True
                heading_title = text
            elif re.match(r'^第[一二三四五六七八九十百]+[章节篇部]', text):
                is_heading = True
                heading_title = text
            elif re.match(r'^\d+[、.．]\s*.+', text) and len(text) < 50:
                is_heading = True
                heading_title = text
            
            if is_heading:
                if current_section["content"].strip():
                    sections.append(current_section)
                
                current_section = {
                    "title": heading_title,
                    "content": "",
                    "category": heading_title
                }
            else:
                current_section["content"] += text + "\n"
        
        if current_section["content"].strip():
            sections.append(current_section)
        
        return sections
    
    def _split_section(self, section: Dict) -> List[Dict]:
        chunks = []
        content = section["content"]
        title = section["title"]
        
        sentences = re.split(r'([。！？\n])', content)
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        "title": f"{title} ({chunk_index + 1})",
                        "content": current_chunk.strip(),
                        "category": section.get("category", title),
                        "chunk_index": chunk_index,
                        "char_count": len(current_chunk)
                    })
                    chunk_index += 1
                current_chunk = sentence
            else:
                current_chunk += sentence
        
        if current_chunk:
            chunks.append({
                "title": f"{title} ({chunk_index + 1})" if chunk_index > 0 else title,
                "content": current_chunk.strip(),
                "category": section.get("category", title),
                "chunk_index": chunk_index,
                "char_count": len(current_chunk)
            })
        
        return chunks

class TxtParser:
    def __init__(self, chunk_size: int = 2000):
        self.chunk_size = chunk_size
    
    def parse_txt(self, file_path: str) -> Dict[str, Any]:
        chunks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sections = self._extract_sections(content)
            
            for section in sections:
                if len(section["content"]) <= self.chunk_size:
                    chunks.append({
                        "title": section["title"],
                        "content": section["content"],
                        "category": section.get("category", section["title"]),
                        "char_count": len(section["content"])
                    })
                else:
                    sub_chunks = self._split_section(section)
                    chunks.extend(sub_chunks)
            
            return {
                "total_chunks": len(chunks),
                "chunks": chunks
            }
        
        except Exception as e:
            logger.error(f"Error parsing TXT: {str(e)}")
            return {"error": str(e), "chunks": []}
    
    def _extract_sections(self, content: str) -> List[Dict]:
        sections = []
        lines = content.split('\n')
        current_section = {"title": "概述", "content": "", "category": "概述"}
        
        chapter_patterns = [
            r'^第[一二三四五六七八九十百]+[章节篇部]\s*(.*)$',
            r'^[一二三四五六七八九十百]+[、.．]\s*(.+)$',
            r'^\d+[、.．]\s*(.+)$',
            r'^第\d+章\s*(.*)$',
        ]
        
        for line in lines:
            text = line.strip()
            if not text:
                continue
            
            is_heading = False
            heading_title = None
            
            for pattern in chapter_patterns:
                if re.match(pattern, text) and len(text) < 50:
                    is_heading = True
                    heading_title = text
                    break
            
            if is_heading:
                if current_section["content"].strip():
                    sections.append(current_section)
                
                current_section = {
                    "title": heading_title,
                    "content": "",
                    "category": heading_title
                }
            else:
                current_section["content"] += text + "\n"
        
        if current_section["content"].strip():
            sections.append(current_section)
        
        return sections
    
    def _split_section(self, section: Dict) -> List[Dict]:
        chunks = []
        content = section["content"]
        title = section["title"]
        
        sentences = re.split(r'([。！？\n])', content)
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        "title": f"{title} ({chunk_index + 1})",
                        "content": current_chunk.strip(),
                        "category": section.get("category", title),
                        "chunk_index": chunk_index,
                        "char_count": len(current_chunk)
                    })
                    chunk_index += 1
                current_chunk = sentence
            else:
                current_chunk += sentence
        
        if current_chunk:
            chunks.append({
                "title": f"{title} ({chunk_index + 1})" if chunk_index > 0 else title,
                "content": current_chunk.strip(),
                "category": section.get("category", title),
                "chunk_index": chunk_index,
                "char_count": len(current_chunk)
            })
        
        return chunks
