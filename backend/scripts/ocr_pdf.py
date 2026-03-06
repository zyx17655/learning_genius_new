import os
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_scanned_pdf(pdf_path, output_dir=None):
    from pdf2image import convert_from_path
    from paddleocr import PaddleOCR
    
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(pdf_path), "ocr_output")
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_file = os.path.join(output_dir, f"{pdf_name}_ocr.txt")
    
    logger.info(f"初始化PaddleOCR...")
    ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    
    logger.info(f"转换PDF为图片: {pdf_path}")
    try:
        pages = convert_from_path(pdf_path, dpi=200)
    except Exception as e:
        logger.error(f"PDF转换失败: {e}")
        logger.info("请确保已安装poppler: https://github.com/oschwartz10612/poppler-windows/releases")
        logger.info("下载后解压，将bin目录添加到系统PATH环境变量")
        return None
    
    total_pages = len(pages)
    logger.info(f"共 {total_pages} 页")
    
    all_text = []
    all_text.append(f"# {pdf_name}\n\n")
    all_text.append(f"OCR处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    all_text.append("=" * 60 + "\n\n")
    
    for i, page in enumerate(pages, 1):
        logger.info(f"处理第 {i}/{total_pages} 页...")
        
        temp_img = os.path.join(output_dir, f"temp_page_{i}.png")
        page.save(temp_img, 'PNG')
        
        try:
            result = ocr.ocr(temp_img, cls=True)
            
            page_text = f"\n## 第 {i} 页\n\n"
            
            if result and result[0]:
                for line in result[0]:
                    if line and len(line) >= 2:
                        text = line[1][0]
                        confidence = line[1][1]
                        if confidence > 0.5:
                            page_text += text + "\n"
            
            all_text.append(page_text)
        except Exception as e:
            logger.error(f"第 {i} 页OCR失败: {e}")
            all_text.append(f"\n## 第 {i} 页\n\n[OCR处理失败]\n")
        
        if os.path.exists(temp_img):
            os.remove(temp_img)
        
        if i % 10 == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(''.join(all_text))
            logger.info(f"已保存进度到: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(all_text))
    
    logger.info(f"OCR完成！结果保存到: {output_file}")
    
    return output_file

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_base", "raw")
        pdf_files = [f for f in os.listdir(raw_dir) if f.lower().endswith('.pdf')]
        if pdf_files:
            pdf_path = os.path.join(raw_dir, pdf_files[0])
            logger.info(f"找到PDF文件: {pdf_path}")
        else:
            logger.error("没有找到PDF文件")
            sys.exit(1)
    
    process_scanned_pdf(pdf_path)
