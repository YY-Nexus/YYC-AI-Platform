from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
import mysql.connector
from mysql.connector import Error
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="M4 Max AI Platform API")

# 线程池执行器，利用M4多核性能
executor = ThreadPoolExecutor(max_workers=8)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 4000  # M4内存充足，增加token限制

class CodeGenerationRequest(BaseModel):
    prompt: str
    language: str = "python"
    context: Optional[str] = None
    optimize_for: str = "performance"  # M4性能优化选项

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = mysql.connector.connect(
            host='mysql',  # 与docker-compose中的服务名一致
            port=3306,
            user='ai_user',
            password='ai_password',
            database='ai_platform'
        )
        return connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

@app.get("/")
async def root():
    return {"message": "M4 Max AI Platform API", "status": "optimized"}

@app.get("/health")
async def health():
    """健康检查端点"""
    return {"status": "ok", "domain": "yyc3ai.0379.email"}

@app.get("/system/status")
async def system_status():
    """系统状态检查，显示M4优化信息"""
    return {
        "platform": "Apple M4 Max AI Platform",
        "memory_optimized": True,
        "arm64_native": True,
        "max_memory": "128GB",
        "supported_models": ["deepseek-chat", "llama2", "codellama", "deepseek-coder"],
        "performance_optimized": True
    }

@app.post("/api/chat")
async def chat_completion(request: ChatRequest):
    """优化的聊天接口，利用M4性能"""
    # 使用线程池处理CPU密集型任务
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        executor, 
        process_chat_request, 
        request
    )
    return response

def process_chat_request(request: ChatRequest):
    """处理聊天请求（在线程池中执行）"""
    try:
        if request.model == "deepseek-chat":
            return call_deepseek_api(request)
        elif request.model.startswith("ollama-"):
            model_name = request.model.replace("ollama-", "")
            return call_ollama_api(request, model_name)
        else:
            raise HTTPException(status_code=400, detail="不支持的模型")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """优化的代码生成，针对M4性能优化"""
    # 根据优化选项调整提示词
    optimization_hint = ""
    if request.optimize_for == "performance":
        optimization_hint = "请生成针对Apple Silicon ARM64架构优化的高性能代码，利用M4芯片的特性。"
    elif request.optimize_for == "memory":
        optimization_hint = "请生成内存效率高的代码，充分利用128GB大内存。"
    
    prompt = f"""
    {optimization_hint}
    
    请根据以下需求生成{request.language}代码：
    {request.prompt}
    
    {f'上下文：{request.context}' if request.context else ''}
    
    要求：
    1. 只返回代码，不要解释
    2. 确保代码完整可运行
    3. 添加必要的注释
    4. 针对Apple M4芯片优化
    """
    
    chat_request = ChatRequest(
        messages=[ChatMessage(role="user", content=prompt)],
        model="ollama-codellama" if "code" in request.prompt.lower() else "ollama-llama2",
        temperature=0.3,
        max_tokens=4000
    )
    
    response = await chat_completion(chat_request)
    return {"code": response["choices"][0]["message"]["content"]}

@app.post("/api/analyze-performance")
async def analyze_performance(code: str, language: str = "python"):
    """代码性能分析，利用M4的计算能力"""
    analysis_prompt = f"""
    分析以下{language}代码的性能特征，并为Apple M4 Max芯片提供优化建议：
    
    ```{language}
    {code}
    ```
    
    请分析：
    1. 计算复杂度
    2. 内存使用模式
    3. 并行化潜力
    4. M4芯片特定优化建议
    """
    
    chat_request = ChatRequest(
        messages=[ChatMessage(role="user", content=analysis_prompt)],
        model="ollama-llama2",
        temperature=0.2
    )
    
    response = await chat_completion(chat_request)
    return {"analysis": response["choices"][0]["message"]["content"]}

def call_deepseek_api(request: ChatRequest):
    """调用DeepSeek API"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="DeepSeek API密钥未配置")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": request.model,
        "messages": [msg.dict() for msg in request.messages],
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "stream": False
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    return response.json()

def call_ollama_api(request: ChatRequest, model_name: str):
    """调用本地Ollama API，利用M4性能"""
    url = "http://ollama:11434/api/generate"
    data = {
        "model": model_name,
        "prompt": request.messages[-1].content,
        "stream": False,
        "options": {
            "temperature": request.temperature,
            "num_predict": request.max_tokens,
            "num_ctx": 8192  # 增大上下文窗口
        }
    }
    
    response = requests.post(url, json=data, timeout=120)
    response.raise_for_status()
    result = response.json()
    return {"choices": [{"message": {"content": result["response"]}}]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        workers=2,  # 利用M4多核
        loop="asyncio"
    )