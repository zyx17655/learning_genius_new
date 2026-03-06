import os
import sys
import logging
import ssl
import urllib.request

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_with_mirror():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    model_dir = os.path.expanduser("~/.EasyOCR/model")
    os.makedirs(model_dir, exist_ok=True)
    
    models = [
        ("craft_mlt_25k.zip", [
            "https://ghproxy.com/https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/craft_mlt_25k.zip",
            "https://mirror.ghproxy.com/https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/craft_mlt_25k.zip",
            "https://hub.fastgit.xyz/JaidedAI/EasyOCR/releases/download/v1.3/craft_mlt_25k.zip",
        ]),
    ]
    
    for filename, urls in models:
        filepath = os.path.join(model_dir, filename)
        if os.path.exists(filepath):
            logger.info(f"已存在: {filename}")
            continue
        
        for url in urls:
            logger.info(f"尝试下载: {filename}")
            logger.info(f"URL: {url}")
            
            try:
                urllib.request.urlretrieve(url, filepath)
                logger.info(f"下载完成: {filename}")
                break
            except Exception as e:
                logger.error(f"下载失败: {e}")
                if os.path.exists(filepath):
                    os.remove(filepath)
                continue

if __name__ == "__main__":
    download_with_mirror()
