FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ ./src/
COPY run_stdio.py .
COPY run_http.py .

# 环境变量
ENV PYTHONPATH=/app

# 默认运行stdio模式
CMD ["python", "run_stdio.py"]
