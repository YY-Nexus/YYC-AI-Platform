#!/bin/bash

echo "🔍 M4 Max AI平台性能监控"

echo ""
echo "📊 Docker容器资源使用:"
docker stats --no-stream

echo ""
echo "🤖 Ollama模型状态:"
curl -s http://localhost:11434/api/tags | jq .

echo ""
echo "🗄️  MySQL连接状态:"
docker exec ai_platform_mysql mysql -u ai_user --password="$MYSQL_PASSWORD" -e "SHOW PROCESSLIST;" ai_platform

echo ""
echo "🌐 服务健康状态:"
curl -s http://localhost:8000/system/status | jq .