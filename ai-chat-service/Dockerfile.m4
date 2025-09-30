FROM python:3.11-slim

# 针对Apple Silicon优化
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 使用清华PyPI镜像加速
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt .
RUN pip install -r requirements.txt

# 安装针对ARM64优化的包
RUN pip install \
    numpy==1.24.0 \
    pandas==2.0.0 \
    scipy==1.10.0 \
    --no-cache-dir

COPY . .

EXPOSE 8000

# 优化Python设置
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV OMP_NUM_THREADS=4

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]