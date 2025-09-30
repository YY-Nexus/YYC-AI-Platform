#!/bin/bash

echo "🔧 环境配置设置"

# 检查 .env.local 是否存在
if [ ! -f ".env.local" ]; then
    echo "📝 创建 .env.local 文件..."
    cat > .env.local << 'ENVFILE'
# ============================================
# 敏感配置 - 不要提交到代码库
# ============================================

# DeepSeek API 真实密钥
DEEPSEEK_API_KEY=请在此处填入你的真实DeepSeek API密钥

# 会话安全密钥 (运行命令生成: openssl rand -hex 32)
SESSION_SECRET=$(openssl rand -hex 32)

# 生产数据库密码
DB_PASSWORD=your_secure_database_password_here
ENVFILE
    echo "✅ 已创建 .env.local 模板"
else
    echo "✅ .env.local 文件已存在"
fi

# 生成会话密钥（如果未设置）
if grep -q "请在此处填入32位随机字符串" .env.local 2>/dev/null || ! grep -q "SESSION_SECRET" .env.local 2>/dev/null; then
    echo "🔑 生成会话密钥..."
    SESSION_KEY=$(openssl rand -hex 32)
    if grep -q "SESSION_SECRET" .env.local 2>/dev/null; then
        sed -i '' "s/SESSION_SECRET=.*/SESSION_SECRET=$SESSION_KEY/" .env.local
    else
        echo "SESSION_SECRET=$SESSION_KEY" >> .env.local
    fi
    echo "✅ 已生成会话密钥"
fi

echo ""
echo "📁 当前环境文件:"
ls -la .env*

echo ""
echo "📝 下一步操作:"
echo "1. 编辑 .env.local 文件，填入真实的 DeepSeek API 密钥"
echo "2. 确保 .env.local 在 .gitignore 中"
echo "3. 运行 ./scripts/verify-env.sh 验证配置"
