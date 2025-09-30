#!/bin/bash

echo "🔍 验证环境配置..."

# 检查必要的环境变量文件
if [ -f ".env" ]; then
    echo "✅ .env 文件存在"
else
    echo "❌ .env 文件不存在"
    exit 1
fi

if [ -f ".env.local" ]; then
    echo "✅ .env.local 文件存在"
else
    echo "⚠️  .env.local 文件不存在，运行 ./scripts/setup-env.sh 创建"
fi

# 检查关键目录
echo ""
echo "📁 检查目录结构:"
directories=("ai-chat-service" "visual-programming" "preview-server" "shared_workspace" "ollama-models" "ssl")
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir 目录存在"
    else
        echo "  ❌ $dir 目录不存在"
    fi
done

# 检查关键文件
echo ""
echo "📄 检查关键文件:"
files=("docker-compose-m4.yml" "docker-compose.yml" "init.sql")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file 文件存在"
    else
        echo "  ❌ $file 文件不存在"
    fi
done

# 检查 DeepSeek API 密钥配置
echo ""
echo "🔑 检查 DeepSeek API 配置:"
if [ -f ".env.local" ]; then
    if grep -q "DEEPSEEK_API_KEY=请在此处填入" .env.local || ! grep -q "DEEPSEEK_API_KEY" .env.local; then
        echo "  ❌ 请编辑 .env.local 文件，填入真实的 DeepSeek API 密钥"
    else
        echo "  ✅ DeepSeek API 密钥已配置"
    fi
fi

# 检查 GitHub 私钥文件
echo ""
echo "🔐 检查 GitHub 私钥:"
if [ -f "ssl/private-key.pem" ]; then
    echo "  ✅ GitHub 私钥文件存在"
    # 检查私钥格式
    if grep -q "BEGIN.*PRIVATE KEY" ssl/private-key.pem; then
        echo "  ✅ 私钥格式正确"
    else
        echo "  ❌ 私钥格式不正确"
    fi
else
    echo "  ❌ GitHub 私钥文件不存在"
    echo "     请从 GitHub 应用设置下载私钥并保存为 ssl/private-key.pem"
fi

echo ""
echo "📋 环境验证完成!"
