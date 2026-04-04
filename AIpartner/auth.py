"""
认证模块 - 处理用户登录、注册和游客模式
"""
import streamlit as st
import hashlib
import json
import os
from datetime import datetime


def check_password():
    """检查用户是否已登录"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        return True
    
    show_login_page()
    return False


def show_login_page():
    """显示登录页面"""
    st.markdown('<h1 style="text-align: center; color: #1f77b4;">🤖 AI 智能伴侣 - 用户登录</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 登录", "📝 注册"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("用户名", placeholder="请输入用户名", key="login_username")
            password = st.text_input("密码", type="password", placeholder="请输入密码", key="login_password")
            
            submit = st.form_submit_button("登录", use_container_width=True, type="primary")
            
            if submit:
                if login(username, password):
                    st.success("✅ 登录成功！")
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.is_guest = False
                    st.rerun()
                else:
                    st.error("❌ 用户名或密码错误")
        
        st.divider()
        
        if st.button("🚀 快速体验（游客模式）", use_container_width=True, type="secondary", key="guest_login_btn"):
            guest_login()
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("用户名", placeholder="至少 3 个字符", key="reg_username")
            new_password = st.text_input("密码", type="password", placeholder="至少 6 个字符", key="reg_password")
            confirm_password = st.text_input("确认密码", type="password", placeholder="再次输入密码", key="reg_confirm")
            
            register_submit = st.form_submit_button("注册", use_container_width=True, type="secondary")
            
            if register_submit:
                success, message = register_user(new_username, new_password, confirm_password)
                if success:
                    st.success(f"✅ {message} 现在可以登录了！")
                else:
                    st.error(f"❌ {message}")
    
    st.markdown("""
**💡 登录方式说明：**

- **账号登录**：数据存储在服务器，支持跨设备共享
- **游客模式**：数据存储在本地浏览器，无法跨设备共享""")


def login(username, password):
    """验证用户名和密码"""
    users_file = "users.json"
    
    if os.path.exists(users_file):
        with open(users_file, 'r', encoding='utf-8') as f:
            users = json.load(f)
    else:
        users = {
            "admin": {
                "password": hashlib.md5("123456".encode()).hexdigest(),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    
    if username in users:
        password_hash = hashlib.md5(password.encode()).hexdigest()
        if users[username]["password"] == password_hash:
            return True
    return False


def register_user(username, password, confirm_password):
    """注册新用户"""
    users_file = "users.json"
    
    if password != confirm_password:
        return False, "两次输入的密码不一致"
    
    if len(username) < 3:
        return False, "用户名至少需要 3 个字符"
    
    if len(password) < 6:
        return False, "密码至少需要 6 个字符"
    
    if os.path.exists(users_file):
        with open(users_file, 'r', encoding='utf-8') as f:
            users = json.load(f)
    else:
        users = {}
    
    if username in users:
        return False, "用户名已存在"
    
    users[username] = {
        "password": hashlib.md5(password.encode()).hexdigest(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    
    return True, "注册成功！"


def logout():
    """登出用户"""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.is_guest = False
    st.rerun()


def guest_login():
    """游客登录"""
    import random
    guest_name = f"游客_{random.randint(1000, 9999)}"
    st.session_state.logged_in = True
    st.session_state.current_user = guest_name
    st.session_state.is_guest = True
    st.rerun()
