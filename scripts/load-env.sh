#!/bin/bash

echo "📁 加载环境变量..."

# 加载 .env 文件
if [ -f ".env" ]; then
    echo "✅ 加载 .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env 文件不存在"
    exit 1
fi

# 加载 .env.local 文件（如果存在）
if [ -f ".env.local" ]; then
    echo "✅ 加载 .env.local"
    export $(cat .env.local | grep -v '^#' | xargs)
else
    echo "⚠️  .env.local 文件不存在，使用默认配置"
fi

# 验证关键环境变量
echo ""
echo "🔍 环境变量验证:"
required_vars=("DEEPSEEK_API_KEY" "APP_CLIENT_ID" "APP_CLIENT_SECRET")
for var in "${required_vars[@]}"; do
    if [ -n "${!var}" ]; then
        if [[ $var == *"SECRET"* ]] || [[ $var == *"KEY"* ]]; then
            # 先获取变量值再计算长度
            value="${!var}"
            echo "  ✅ $var: 已设置 (长度: ${#value})"
        else
            echo "  ✅ $var: ${!var}"
        fi
    else
        echo "  ❌ $var: 未设置"
    fi
done
