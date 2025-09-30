#!/bin/bash

echo "🔍 验证最终配置..."

# 检查必要的环境变量
required_vars=(
    "APP_CLIENT_ID"
    "APP_CLIENT_SECRET"
    "APP_WEBHOOK_SECRET" 
    "APP_APP_ID"
    "APP_PRIVATE_KEY_PATH"
    "APP_REDIRECT_URI"
    "APP_SETUP_URL"
    "APP_BASE_URL"
    "SESSION_SECRET"
    "DEEPSEEK_API_KEY"
)

echo "📋 环境变量检查:"
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

# 检查私钥文件
echo ""
echo "🔑 私钥文件检查:"
if [ -f "$APP_PRIVATE_KEY_PATH" ]; then
    echo "  ✅ 私钥文件存在: $APP_PRIVATE_KEY_PATH"
    # 验证私钥格式
    if openssl rsa -in "$APP_PRIVATE_KEY_PATH" -check -noout 2>/dev/null; then
        echo "  ✅ 私钥格式有效"
    else
        echo "  ❌ 私钥格式无效"
    fi
else
    echo "  ❌ 私钥文件不存在: $APP_PRIVATE_KEY_PATH"
fi

# 检查域名配置
echo ""
echo "🌐 域名配置检查:"
domains=(
    "https://yyc3ai.0379.email"
    "https://yyc3ai.0379.email/auth/github/callback"
    "https://yyc3ai.0379.email/auth/setup"
    "https://yyc3ai.0379.email/api/webhook/github"
)

for domain in "${domains[@]}"; do
    if curl -s --head "$domain" | grep -q "200 OK\|301 Moved Permanently"; then
        echo "  ✅ $domain: 可访问"
    else
        echo "  ❌ $domain: 无法访问"
    fi
done

echo ""
echo "📊 配置验证完成!"