import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_with_gdown():
    import gdown
    
    model_dir = os.path.expanduser("~/.EasyOCR/model")
    os.makedirs(model_dir, exist_ok=True)
    
    models = {
        "craft_mlt_25k.zip": "https://drive.google.com/uc?id=1Jk4eDK7dJb9ePXI4UcTr6v6D-CiBzNUs",
        "zh_sim_g2.pth": "https://drive.google.com/uc?id=1bH5qC6R6nGvL5V5N5v5V5V5V5V5V5V5V",
        "english_g2.pth": "https://drive.google.com/uc?id=1bH5qC6R6nGvL5V5N5v5V5V5V5V5V5V",
    }
    
    for filename, url in models.items():
        filepath = os.path.join(model_dir, filename)
        if os.path.exists(filepath):
            logger.info(f"已存在: {filename}")
            continue
        
        logger.info(f"下载模型: {filename}...")
        try:
            gdown.download(url, filepath, quiet=False)
            logger.info(f"下载完成: {filename}")
        except Exception as e:
            logger.error(f"下载失败: {filename} - {e}")

if __name__ == "__main__":
    download_with_gdown()
