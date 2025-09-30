from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
from datetime import datetime

app = FastAPI(title="AI Platform API")

# CORS配置
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
    max_tokens: int = 2000

class CodeGenerationRequest(BaseModel):
    prompt: str
    language: str = "python"
    context: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "AI Platform API"}

@app.post("/api/chat")
async def chat_completion(request: ChatRequest):
    """处理聊天请求"""
    try:
        if request.model == "deepseek-chat":
            return await call_deepseek_api(request)
        elif request.model == "ollama":
            return await call_ollama_api(request)
        else:
            raise HTTPException(status_code=400, detail="不支持的模型")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """生成代码"""
    prompt = f"""
    请根据以下需求生成{request.language}代码：
    {request.prompt}
    
    {f'上下文：{request.context}' if request.context else ''}
    
    要求：
    1. 只返回代码，不要解释
    2. 确保代码完整可运行
    3. 添加必要的注释
    """
    
    chat_request = ChatRequest(
        messages=[ChatMessage(role="user", content=prompt)],
        model="deepseek-chat",
        temperature=0.3
    )
    
    response = await chat_completion(chat_request)
    return {"code": response["choices"][0]["message"]["content"]}

async def call_deepseek_api(request: ChatRequest):
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
    
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    return response.json()

async def call_ollama_api(request: ChatRequest):
    """调用本地Ollama API"""
    url = "http://host.docker.internal:11434/api/generate"
    data = {
        "model": "llama2",  # 或其他本地模型
        "prompt": request.messages[-1].content,
        "stream": False
    }
    
    response = requests.post(url, json=data, timeout=60)
    response.raise_for_status()
    return {"choices": [{"message": {"content": response.json()["response"]}}]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)