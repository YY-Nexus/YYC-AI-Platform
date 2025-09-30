import streamlit as st
import requests
import json
import os
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="AI可视化编程平台",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .project-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
    .code-block {
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API配置
API_BASE = os.getenv("API_URL", "http://localhost:8000")
GITEA_BASE = os.getenv("GITEA_URL", "http://localhost:3000")

def main():
    st.markdown('<div class="main-header">🚀 AI可视化编程平台</div>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("导航")
        page = st.radio("选择功能", ["AI聊天", "代码生成", "项目管理", "实时预览"])
        
        st.header("模型设置")
        model = st.selectbox("选择AI模型", ["deepseek-chat", "ollama-llama2", "ollama-codellama"])
        temperature = st.slider("创造性", 0.0, 1.0, 0.7)
        
        st.header("项目信息")
        st.info("当前工作区: /app/workspace")
    
    if page == "AI聊天":
        render_chat_interface(model, temperature)
    elif page == "代码生成":
        render_code_generation()
    elif page == "项目管理":
        render_project_management()
    elif page == "实时预览":
        render_live_preview()

def render_chat_interface(model, temperature):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 AI编程助手")
        
        # 初始化会话历史
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # 显示聊天记录
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 聊天输入
        if prompt := st.chat_input("输入你的编程问题或需求..."):
            # 添加用户消息
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 获取AI回复
            with st.chat_message("assistant"):
                with st.spinner("AI思考中..."):
                    try:
                        response = call_chat_api(st.session_state.messages, model, temperature)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"错误: {str(e)}")
    
    with col2:
        st.header("快捷操作")
        
        if st.button("清空对话"):
            st.session_state.messages = []
            st.rerun()
        
        st.subheader("代码示例")
        examples = [
            "写一个Python Flask Web应用",
            "实现一个React计数器组件",
            "写一个数据库连接工具类",
            "实现用户认证的JWT token"
        ]
        
        for example in examples:
            if st.button(example, key=example):
                st.session_state.messages.append({"role": "user", "content": example})
                st.rerun()

def render_code_generation():
    st.header("👨‍💻 智能代码生成")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("代码需求")
        language = st.selectbox("编程语言", ["python", "javascript", "java", "html", "css", "sql"])
        prompt = st.text_area("描述你想要的代码功能", height=150)
        
        context = st.text_area("上下文或现有代码（可选）", height=100)
        
        if st.button("生成代码", type="primary"):
            if prompt:
                with st.spinner("正在生成代码..."):
                    try:
                        response = call_code_generation_api(prompt, language, context)
                        st.session_state.generated_code = response["code"]
                    except Exception as e:
                        st.error(f"生成失败: {str(e)}")
    
    with col2:
        st.subheader("生成的代码")
        if "generated_code" in st.session_state:
            st.code(st.session_state.generated_code, language=language)
            
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                if st.button("复制代码"):
                    st.code(st.session_state.generated_code)
            with col2_2:
                if st.button("保存到项目"):
                    st.success("代码已保存！")
            with col2_3:
                if st.button("实时预览"):
                    st.info("在预览页面查看效果")

def render_project_management():
    st.header("📁 项目管理")
    
    tab1, tab2, tab3 = st.tabs(["项目列表", "新建项目", "Git管理"])
    
    with tab1:
        st.subheader("我的项目")
        # 模拟项目数据
        projects = [
            {"name": "Web聊天应用", "language": "Python", "modified": "2024-01-15"},
            {"name": "数据分析工具", "language": "Jupyter", "modified": "2024-01-10"},
            {"name": "移动端UI", "language": "React", "modified": "2024-01-05"}
        ]
        
        for project in projects:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{project['name']}**")
                with col2:
                    st.write(project['language'])
                with col3:
                    st.write(project['modified'])
                st.divider()
    
    with tab2:
        st.subheader("创建新项目")
        project_name = st.text_input("项目名称")
        project_desc = st.text_area("项目描述")
        project_type = st.selectbox("项目类型", ["Web应用", "数据分析", "机器学习", "移动应用", "工具库"])
        
        if st.button("创建项目"):
            if project_name:
                st.success(f"项目 '{project_name}' 创建成功！")
    
    with tab3:
        st.subheader("Git版本控制")
        st.info(f"Git服务地址: {GITEA_BASE}")
        st.write("""
        - 克隆仓库: `git clone {GITEA_BASE}/username/repo.git`
        - 提交更改: `git add . && git commit -m "message"`
        - 推送代码: `git push origin main`
        """)

def render_live_preview():
    st.header("🔍 实时预览")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("代码编辑器")
        code_content = st.text_area(
            "编辑你的代码",
            height=400,
            value='<!DOCTYPE html>\n<html>\n<head>\n    <title>我的网页</title>\n</head>\n<body>\n    <h1>Hello World!</h1>\n</body>\n</html>'
        )
        
        if st.button("更新预览"):
            st.session_state.preview_code = code_content
    
    with col2:
        st.subheader("预览效果")
        if "preview_code" in st.session_state:
            st.components.v1.html(st.session_state.preview_code, height=400)
        else:
            st.info("点击'更新预览'查看效果")

def call_chat_api(messages, model, temperature):
    """调用聊天API"""
    url = f"{API_BASE}/api/chat"
    data = {
        "messages": messages,
        "model": model,
        "temperature": temperature
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def call_code_generation_api(prompt, language, context=None):
    """调用代码生成API"""
    url = f"{API_BASE}/api/generate-code"
    data = {
        "prompt": prompt,
        "language": language,
        "context": context
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    main()