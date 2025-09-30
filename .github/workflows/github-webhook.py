import hmac
import hashlib
import os
from flask import request, jsonify, current_app as app

def verify_webhook_signature(payload_body, secret_token, signature_header):
    """验证 Webhook 签名"""
    if not signature_header:
        return False
    
    hash_object = hmac.new(
        secret_token.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)

@app.route('/api/webhook/github', methods=['POST'])
def handle_github_webhook():
    """处理 GitHub Webhook 事件 - 新域名版本"""
    # 验证签名
    signature = request.headers.get('X-Hub-Signature-256')
    secret_token = os.getenv('GITHUB_WEBHOOK_SECRET')
    
    if not verify_webhook_signature(request.data, secret_token, signature):
        app.logger.warning(f"Invalid webhook signature from {request.remote_addr}")
        return jsonify({'error': 'Invalid signature'}), 401
    
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    app.logger.info(f"Received {event_type} event from GitHub")
    
    # 处理不同的事件类型
    event_handlers = {
        'push': handle_push_event,
        'pull_request': handle_pull_request_event,
        'issues': handle_issues_event,
        'installation': handle_installation_event,
        'ping': handle_ping_event
    }
    
    handler = event_handlers.get(event_type)
    if handler:
        handler(payload)
    
    return jsonify({'status': 'processed', 'domain': 'yyc3ai.0379.email'})

@app.route('/api/webhook/github/legacy', methods=['POST'])
def handle_github_webhook_legacy():
    """处理 GitHub Webhook 事件 - 旧版本"""
    # 验证签名
    signature = request.headers.get('X-Hub-Signature-256')
    secret_token = os.getenv('GITHUB_WEBHOOK_SECRET')
    
    if not verify_webhook_signature(request.data, secret_token, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    # 处理不同的事件类型
    if event_type == 'push':
        handle_push_event(payload)
    elif event_type == 'pull_request':
        handle_pull_request_event(payload)
    elif event_type == 'issues':
        handle_issues_event(payload)
    
    return jsonify({'status': 'processed'})

def handle_push_event(payload):
    """处理 push 事件"""
    repository = payload['repository']['full_name']
    commits = payload['commits']
    
    print(f"Received push event for {repository} with {len(commits)} commits")
    
    # 触发 AI 代码分析
    analyze_code_changes(repository, commits)

def handle_pull_request_event(payload):
    """处理 PR 事件"""
    action = payload['action']
    pr_number = payload['pull_request']['number']
    repository = payload['repository']['full_name']
    
    if action in ['opened', 'synchronize']:
        # 自动代码审查
        perform_code_review(repository, pr_number)


def handle_ping_event(payload):
    """处理 Webhook ping 事件"""
    app.logger.info("Webhook configured successfully for yyc3ai.0379.email")
    

def handle_installation_event(payload):
    """处理应用安装事件"""
    action = payload.get('action')
    installation_id = payload['installation']['id']
    
    
    if action == 'created':
        app.logger.info(f"GitHub App installed: {installation_id} on yyc3ai.0379.email")
    elif action == 'deleted':
        app.logger.info(f"GitHub App uninstalled: {installation_id} from yyc3ai.0379.email")

def analyze_code_changes(repo, commits):
    """使用 AI 分析代码变更"""
    # 集成 AI 代码分析逻辑
    pass

def perform_code_review(repo, pr_number):
    """执行 AI 代码审查"""
    # 集成 AI 代码审查逻辑
    pass