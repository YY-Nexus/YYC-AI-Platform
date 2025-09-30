# AI 开发平台 - Apple M4 Max 优化版

基于 Docker 的全栈 AI 开发环境，专为 Apple M4 Max 128GB 优化，提供可视化编程界面、AI 代码生成和实时预览功能。

## 🌐 域名配置

当前平台使用以下域名：
- **主域名**: https://yyc3ai.0379.email
- **API 路由**: https://yyc3ai.0379.email/api/
- **GitHub 认证**: https://yyc3ai.0379.email/auth/
- **实时预览**: https://yyc3ai.0379.email/preview/

## 🚀 快速开始

## 🚀 快速开始

### 系统要求
- **硬件**: Apple M4 Max 128GB（推荐）或兼容的 Apple Silicon 设备
- **软件**: macOS Sequoia 15.0+, Docker Desktop, Homebrew

### 环境准备

1. **设置 DeepSeek API 密钥**
```bash
# 已在 ~/.zshrc 中设置
echo 'export DEEPSEEK_API_KEY="你的API密钥"' >> ~/.zshrc
source ~/.zshrc
```

2. **验证环境配置**
```bash
./verify-env.sh
```

### 🎯 脚本运行顺序

#### 方案一：M4 Max 优化版本（推荐）
```bash
# 1. 启动完整平台（M4优化）
./start-m4.sh

# 2. 监控服务状态
./monitor-m4.sh
```

#### 方案二：通用版本
```bash
# 1. 启动通用版本
./start.sh

# 2. 监控服务状态  
./monitor-m4.sh
```

#### 方案三：开发调试模式
```bash
# 直接使用 Docker Compose（带日志输出）
docker-compose -f docker-compose-m4.yml up --build
```

## 📁 项目结构

```
ai-platform/
├── ai-chat-service/          # AI聊天后端服务
│   ├── main_optimized.py     # M4优化版本
│   ├── main.py               # 基础版本
│   └── requirements.txt
├── visual-programming/       # Streamlit可视化界面
│   ├── main.py
│   └── requirements.txt
├── preview-server/           # 实时预览服务
│   └── package.json
├── shared_workspace/         # 代码共享目录
├── ollama-models/           # 本地模型存储
├── docker-compose-m4.yml    # M4优化配置
├── docker-compose.yml       # 通用配置
├── init.sql                # MySQL数据库初始化
├── .env                    # 环境配置
├── start-m4.sh            # M4启动脚本
├── start.sh               # 通用启动脚本
└── monitor-m4.sh          # 监控脚本
```

## 🔧 核心服务

### 1. AI 聊天服务 (`ai-chat-service`)
- **端口**: 8000
- **功能**: DeepSeek API 集成、Ollama 本地模型、代码生成
- **API 文档**: http://localhost:8000/docs

### 2. 可视化编程界面 (`visual-programming`) 
- **端口**: 8501
- **功能**: Streamlit Web 界面、代码编辑器、项目管理
- **访问**: http://localhost:8501

### 3. 实时预览服务 (`preview-server`)
- **端口**: 3001
- **功能**: 代码实时预览、WebSocket 通信
- **访问**: http://localhost:3001

### 4. Ollama 本地模型服务
- **端口**: 11434
- **模型**: Llama2、CodeLlama、DeepSeek-Coder
- **管理**: http://localhost:11434

### 5. MySQL 数据库
- **端口**: 3306
- **数据库**: ai_platform
- **用户**: ai_user / ai_password

## ⚡ 性能优化特性

### M4 Max 专属优化
- 🚀 **ARM64 原生容器优化**
- 💾 **128GB 内存充分利用**
- 🔥 **多核并行处理** (8 workers)
- 🧠 **大模型本地运行** (13B 参数)
- ⚡ **高速模型缓存**

### 内存分配策略
```yaml
Ollama: 64GB    # 大模型运行
MySQL: 2GB      # 数据库缓存
AI服务: 8GB     # 处理并发请求
预览服务: 4GB   # 实时编译
```

## 📊 监控和管理

### 实时监控
```bash
# 查看所有服务状态
./monitor-m4.sh

# 查看 Docker 资源使用
docker stats

# 查看服务日志
docker-compose -f docker-compose-m4.yml logs -f
```

### 服务管理命令
```bash
# 启动服务
docker-compose -f docker-compose-m4.yml start

# 停止服务  
docker-compose -f docker-compose-m4.yml stop

# 重启服务
docker-compose -f docker-compose-m4.yml restart

# 查看服务状态
docker-compose -f docker-compose-m4.yml ps
```

## 🛠️ 故障排除

### 常见问题

1. **DeepSeek API 密钥未设置**
   ```bash
   # 检查环境变量
   echo $DEEPSEEK_API_KEY
   
   # 重新设置
   echo 'export DEEPSEEK_API_KEY="你的密钥"' >> ~/.zshrc
   source ~/.zshrc
   ```

2. **端口冲突**
   ```bash
   # 检查端口占用
   lsof -i :8501
   lsof -i :8000
   lsof -i :3001
   
   # 修改 docker-compose-m4.yml 中的端口映射
   ```

3. **Docker 内存不足**
   ```bash
   # 调整 Docker Desktop 内存限制
   # Docker Desktop -> Settings -> Resources -> Memory
   # 推荐: 16GB+ for M4 Max
   ```

4. **数据库连接失败**
   ```bash
   # 检查 MySQL 容器
   docker logs ai_platform_mysql
   
   # 重新初始化数据库
   docker-compose -f docker-compose-m4.yml down -v
   docker-compose -f docker-compose-m4.yml up -d mysql
   ```

### 日志查看
```bash
# 查看特定服务日志
docker-compose -f docker-compose-m4.yml logs ai-chat
docker-compose -f docker-compose-m4.yml logs visual-programming
docker-compose -f docker-compose-m4.yml logs mysql

# 实时日志跟踪
docker-compose -f docker-compose-m4.yml logs -f ai-chat
```

## 🔄 更新和维护

### 更新代码
```bash
# 拉取最新代码
git pull origin main

# 重建服务
docker-compose -f docker-compose-m4.yml up -d --build
```

### 数据备份
```bash
# 备份数据库
docker exec ai_platform_mysql mysqldump -u ai_user -pai_password ai_platform > backup.sql

# 备份工作区
tar -czf workspace_backup.tar.gz shared_workspace/
```

### 清理资源
```bash
# 停止并删除所有容器
docker-compose -f docker-compose-m4.yml down

# 清理未使用的镜像
docker image prune -a

# 清理卷（谨慎使用，会删除数据）
docker volume prune
```

## 🎨 使用示例

### 基础工作流
1. **访问可视化界面**: http://localhost:8501
2. **选择 AI 模型**: DeepSeek API 或本地 Ollama
3. **输入编程需求**: 描述你想要的代码功能
4. **生成并预览**: 实时查看生成的代码效果
5. **保存到项目**: 管理你的代码项目

### 高级功能
- 🔍 **代码性能分析**: 针对 M4 芯片优化建议
- 📁 **项目管理**: Git 集成和版本控制
- 🔄 **实时协作**: 多用户同时编辑和预览
- 🧪 **测试生成**: 自动生成单元测试

## 📞 技术支持

### 获取帮助
1. 查看服务日志: `./monitor-m4.sh`
2. 验证环境配置: `./verify-env.sh`  
3. 检查系统状态: http://localhost:8000/system/status

## 🚀 生产环境部署指南

### 更新环境变量
```bash
# 更新 .env 文件中的所有 URL
sed -i '' 's/ai-platform\.0379\.email/yyc3ai.0379.email/g' .env

# 更新代码文件
sed -i '' 's/ai-platform\.0379\.email/yyc3ai.0379.email/g' .github/workflows/github-auth.py
sed -i '' 's/ai-platform\.0379\.email/yyc3ai.0379.email/g' .github/workflows/github-webhook.py

# 验证更新
./verify-env.sh
```

### 部署服务
```bash
# 停止旧服务
docker-compose -f .github/workflows/docker-compose.prod.yml down

# 构建新镜像
docker-compose -f .github/workflows/docker-compose.prod.yml build

# 启动新服务
docker-compose -f .github/workflows/docker-compose.prod.yml up -d

# 检查服务状态
docker-compose -f .github/workflows/docker-compose.prod.yml ps
```

### 测试集成
```bash
# 测试健康检查
curl https://yyc3ai.0379.email/health

# 测试 GitHub Webhook
curl -X POST \
  -H "X-GitHub-Event: ping" \
  -H "Content-Type: application/json" \
  -d '{"zen": "Testing new domain"}' \
  https://yyc3ai.0379.email/api/webhook/github
```

## 📝 域名更新检查清单

- [ ] 更新 `.env` 文件中的所有 URL
- [ ] 更新 GitHub 应用设置中的 URL
- [ ] 更新代码中的硬编码 URL
- [ ] 配置 Nginx 或反向代理
- [ ] 更新 SSL 证书
- [ ] 测试所有端点
- [ ] 验证 GitHub Webhook 交付
- [ ] 测试 OAuth 回调流程

### 问题反馈
- 服务启动问题: 检查 Docker 日志
- API 连接问题: 验证 DeepSeek 密钥
- 性能问题: 调整内存分配参数

---

**享受你在 M4 Max 上的 AI 编程体验！** 🚀
