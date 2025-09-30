#!/bin/bash

echo "🚀 启动 M4 Max AI开发平台..."

# 加载环境变量
if [ -f "scripts/load-env.sh" ]; then
    source scripts/load-env.sh
else
    echo "⚠️  无法加载环境变量，请确保 scripts/load-env.sh 存在"
fi

# 检查关键环境变量
if [ -z "$DEEPSEEK_API_KEY" ] || [ "$DEEPSEEK_API_KEY" = "请在此处填入你的真实DeepSeek API密钥" ]; then
    echo "❌ 错误: 请设置有效的 DEEPSEEK_API_KEY"
    echo "   编辑 .env.local 文件并填入真实的 DeepSeek API 密钥"
    exit 1
fi

# 检查 Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请启动Docker"
    exit 1
fi

# 检查私钥文件
if [ ! -f "ssl/private-key.pem" ]; then
    echo "❌ GitHub 私钥文件不存在"
    echo "   请将 GitHub 应用的私钥保存为 ssl/private-key.pem"
    exit 1
fi

echo "📦 启动Docker服务..."
docker-compose -f docker-compose-m4.yml up -d

echo "⏳ 等待服务启动..."
sleep 15

# 检查服务状态
echo "🔍 服务状态:"
docker-compose -f docker-compose-m4.yml ps

echo ""
echo "✅ M4 Max AI平台启动完成!"
echo ""
echo "📱 访问地址:"
echo "   - 可视化编程: http://localhost:8501"
echo "   - AI API文档: http://localhost:8000/docs"
echo "   - 实时预览: http://localhost:3001"
echo "   - Ollama管理: http://localhost:11434"
