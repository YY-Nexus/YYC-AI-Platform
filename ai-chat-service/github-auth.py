from fastapi import FastAPI, Request, HTTPException, APIRouter, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Optional, Dict, Any
import os
import requests
import json
import logging
from datetime import datetime, timedelta
import jwt

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter()

# 更新 GitHub OAuth 配置
GITHUB_REDIRECT_URI = 'https://yyc3ai.0379.email/auth/github/callback'
GITHUB_SETUP_URL = 'https://yyc3ai.0379.email/auth/setup'

# 从环境变量获取GitHub应用凭据
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', '')
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')

class GitHubIntegration:
    def __init__(self):
        self.client_id = GITHUB_CLIENT_ID
        self.client_secret = GITHUB_CLIENT_SECRET
        self.redirect_uri = GITHUB_REDIRECT_URI
        self.setup_url = GITHUB_SETUP_URL
        
    def get_authorization_url(self, setup_redirect=False):
        """生成 GitHub 授权 URL"""
        redirect_url = self.setup_url if setup_redirect else self.redirect_uri
        return (
            "https://github.com/oauth/authorize"
            f"?client_id={self.client_id}"
            f"&redirect_uri={redirect_url}"
            f"&scope=repo,user,write:repo_hook"
        )

# 初始化GitHub集成
github = GitHubIntegration()

@router.route('/auth/github')
def auth_github(request: Request):
    """发起 GitHub OAuth 授权"""
    setup_redirect = request.query_params.get('setup', False)
    return RedirectResponse(github.get_authorization_url(setup_redirect=setup_redirect))

@router.route('/auth/github/callback')
def auth_github_callback(request: Request):
    """GitHub OAuth 回调处理"""
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="缺少授权码")
    
    # 交换访问令牌
    try:
        token_response = requests.post(
            'https://github.com/login/oauth/access_token',
            json={
                'client_id': GITHUB_CLIENT_ID,
                'client_secret': GITHUB_CLIENT_SECRET,
                'code': code
            },
            headers={'Accept': 'application/json'}
        )
        
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        
        if not access_token:
            raise HTTPException(status_code=400, detail=f"获取令牌失败: {token_data}")
        
        # 获取用户信息
        user_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        user_data = user_response.json()
        
        # 生成JWT令牌
        payload = {
            'user_id': user_data.get('id'),
            'username': user_data.get('login'),
            'email': user_data.get('email'),
            'github_token': access_token,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        
        jwt_token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        
        # 设置Cookie
        response = RedirectResponse('/setup-complete' if 'setup' in request.query_params else '/dashboard')
        response.set_cookie('auth_token', jwt_token, httponly=True, max_age=3600*24*7)
        
        logger.info(f"用户 {user_data.get('login')} 登录成功")
        return response
        
    except Exception as e:
        logger.error(f"OAuth回调处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"认证失败: {str(e)}")

@router.route('/auth/setup')
def auth_setup():
    """安装后设置页面"""
    return RedirectResponse(github.get_authorization_url(setup_redirect=True))

@router.route('/auth/logout')
def logout():
    """退出登录"""
    response = RedirectResponse('/')
    response.delete_cookie('auth_token')
    return response

# 用于验证JWT的依赖项
def get_current_user(request: Request):
    """获取当前登录用户"""
    token = request.cookies.get('auth_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未授权访问")
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌")

# 注册路由到应用
def register_github_routes(app: FastAPI):
    app.include_router(router)