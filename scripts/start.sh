#!/bin/bash

echo "🚀 启动AI开发平台..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请启动Docker"
    exit 1
fi

# 创建必要的目录
mkdir -p shared_workspace
mkdir -p ai-chat-service
mkdir -p visual-programming
mkdir -p preview-server

# 启动服务
echo "📦 启动Docker服务..."
docker-compose up -d

echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

echo "✅ 平台启动完成!"
echo ""
echo "📱 访问地址:"
echo "   - 可视化编程: http://localhost:8501"
echo "   - Git服务: http://localhost:3000"
echo "   - 预览服务: http://localhost:3001"
echo "   - API文档: http://localhost:8000/docs"