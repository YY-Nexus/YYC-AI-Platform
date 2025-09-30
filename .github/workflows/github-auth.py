import os
import os
import requests
from flask import Flask, redirect, request, session, jsonify
import jwt
import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_SECRET')

# 更新后的环境变量名
APP_CLIENT_ID = os.getenv('APP_CLIENT_ID')
APP_CLIENT_SECRET = os.getenv('APP_CLIENT_SECRET')
APP_REDIRECT_URI = os.getenv('APP_REDIRECT_URI')
APP_SETUP_URL = os.getenv('APP_SETUP_URL')

class GitHubIntegration:
    def __init__(self):
        self.client_id = APP_CLIENT_ID
        self.client_secret = APP_CLIENT_SECRET
        self.redirect_uri = APP_REDIRECT_URI
        self.setup_url = APP_SETUP_URL
    
    def get_authorization_url(self, setup_redirect=False):
        """生成 GitHub 授权 URL"""
        redirect_url = self.setup_url if setup_redirect else self.redirect_uri
        return (
            f"https://github.com/oauth/authorize"
            f"?client_id={self.client_id}"
            f"&redirect_uri={redirect_url}"
            f"&scope=repo,user,write:repo_hook"
        )
    
    def exchange_code_for_token(self, code):
        """使用 code 交换 access token"""
        url = "https://github.com/oauth/access_token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        headers = {'Accept': 'application/json'}
        
        response = requests.post(url, data=data, headers=headers)
        return response.json()
    
    def get_user_info(self, access_token):
        """获取用户信息"""
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/user', headers=headers)
        return response.json()

github = GitHubIntegration()

@app.route('/auth/github')
def auth_github():
    """发起 GitHub OAuth 授权"""
    return redirect(github.get_authorization_url())

@app.route('/auth/github/callback')
def auth_github_callback():
    """GitHub OAuth 回调处理"""
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    # 交换 token
    token_response = github.exchange_code_for_token(code)
    access_token = token_response.get('access_token')
    
    if not access_token:
        return jsonify({'error': 'Failed to get access token'}), 400
    
    # 获取用户信息
    user_info = github.get_user_info(access_token)
    
    # 存储用户会话
    session['github_access_token'] = access_token
    session['github_user'] = user_info
    
    return redirect('/dashboard')

@app.route('/api/github/repos')
def list_repos():
    """获取用户仓库列表"""
    access_token = session.get('github_access_token')
    if not access_token:
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    return jsonify(response.json())