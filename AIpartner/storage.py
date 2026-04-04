"""
存储模块 - 处理本地存储和服务器端存储
"""
import streamlit as st
import json
import os
from streamlit_local_storage import LocalStorage


def get_user_data_file(username):
    """获取用户数据文件路径"""
    return f"user_data_{username}.json"


def load_user_sessions(username):
    """从服务器加载用户的会话数据"""
    data_file = get_user_data_file(username)
    
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}


def save_user_sessions(username, sessions):
    """保存用户会话数据到服务器"""
    data_file = get_user_data_file(username)
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def save_avatar(username, avatar_data):
    """保存角色头像"""
    avatar_file = f"avatar_{username}.json"
    with open(avatar_file, 'w', encoding='utf-8') as f:
        json.dump({"avatar": avatar_data}, f, ensure_ascii=False, indent=2)


def load_avatar(username):
    """加载角色头像"""
    avatar_file = f"avatar_{username}.json"
    if os.path.exists(avatar_file):
        with open(avatar_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("avatar", None)
    return None


def save_to_storage():
    """根据登录类型选择存储方式"""
    is_guest = st.session_state.get('is_guest', False)
    
    if is_guest:
        localStorage = LocalStorage()
        localStorage.setItem("guest_sessions", st.session_state.user_sessions)
    else:
        save_user_sessions(st.session_state.current_user, st.session_state.user_sessions)


def init_user_sessions():
    """初始化用户的会话列表，根据登录类型选择存储方式"""
    current_user = st.session_state.get('current_user')
    is_guest = st.session_state.get('is_guest', False)
    
    if current_user and not is_guest:
        st.session_state.user_sessions = load_user_sessions(current_user)
    elif is_guest:
        localStorage = LocalStorage()
        saved_sessions = localStorage.getItem("guest_sessions")
        if saved_sessions:
            st.session_state.user_sessions = saved_sessions
        else:
            if "user_sessions" not in st.session_state:
                st.session_state.user_sessions = {}
    else:
        if "user_sessions" not in st.session_state:
            st.session_state.user_sessions = {}
    
    if "current_session" not in st.session_state:
        st.session_state.current_session = None


def load_sessions():
    """返回当前用户的所有会话名称列表"""
    return list(st.session_state.user_sessions.keys())
