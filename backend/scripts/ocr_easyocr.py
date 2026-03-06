import os
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_model(url, filepath):
    import urllib.request
    import ssl
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        urllib.request.urlretrieve(url, filepath)
        return True
    except Exception as e:
        logger.error(f"下载失败: {e}")
        return False

def process_scanned_pdf(pdf_path, output_dir=None):
    import easyocr
    import pypdfium2 as pdfium
    
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(pdf_path), "ocr_output")
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_file = os.path.join(output_dir, f"{pdf_name}_ocr.txt")
    
    model_dir = os.path.expanduser("~/.EasyOCR/model")
    os.makedirs(model_dir, exist_ok=True)
    
    models = {
        "craft_mlt_25k.zip": "https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/craft_mlt_25k.zip",
        "zh_sim_g2.pth": "https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/zh_sim_g2.pth",
        "english_g2.pth": "https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.pth",
    }
    
    for filename, url in models.items():
        filepath = os.path.join(model_dir, filename)
        if not os.path.exists(filepath):
            logger.info(f"下载模型: {filename}...")
            if download_model(url, filepath):
                logger.info(f"模型下载完成: {filename}")
            else:
                logger.error(f"模型下载失败: {filename}")
                return None
    
    logger.info(f"初始化EasyOCR...")
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, download_enabled=True)
    
    logger.info(f"打开PDF: {pdf_path}")
    logger.info(f"文件大小: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
    
    pdf = pdfium.PdfDocument(pdf_path)
    total_pages = len(pdf)
    logger.info(f"共 {total_pages} 页")
    
    all_text = []
    all_text.append(f"# {pdf_name}\n\n")
    all_text.append(f"OCR处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    all_text.append("=" * 60 + "\n\n")
    
    for i in range(total_pages):
        page_num = i + 1
        logger.info(f"处理第 {page_num}/{total_pages} 页...")
        
        try:
            page = pdf[i]
            bitmap = page.render(scale=2)
            pil_image = bitmap.to_pil()
            
            temp_img = os.path.join(output_dir, f"temp_page_{page_num}.png")
            pil_image.save(temp_img)
            
            results = reader.readtext(temp_img)
            
            page_text = f"\n## 第 {page_num} 页\n\n"
            for detection in results:
                text = detection[1]
                confidence = detection[2]
                if confidence > 0.3:
                    page_text += text + "\n"
            
            all_text.append(page_text)
            
            if os.path.exists(temp_img):
                os.remove(temp_img)
            
        except Exception as e:
            logger.error(f"第 {page_num} 页OCR失败: {e}")
            all_text.append(f"\n## 第 {page_num} 页\n\n[OCR处理失败]\n")
        
        if page_num % 10 == 0:
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
