FROM python:3.11-slim

WORKDIR /app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt .
RUN pip install -r requirements.txt

# 安装针对ARM64优化的科学计算包
RUN pip install \
    plotly==5.17.0 \
    scikit-learn==1.3.0 \
    --no-cache-dir

COPY . .

EXPOSE 8501

# 优化Streamlit设置
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]