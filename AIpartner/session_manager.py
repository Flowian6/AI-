"""
会话管理模块 - 处理会话的创建、切换、删除
"""
import streamlit as st
from storage import save_to_storage


def switch_to_session(session_name):
    """切换到指定会话，从内存中加载会话数据到 session_state"""
    if session_name in st.session_state.user_sessions:
        session_data = st.session_state.user_sessions[session_name]
        st.session_state.name = session_data["name"]
        st.session_state.nature = session_data["nature"]
        st.session_state.messages = session_data["messages"]
        st.session_state.session_name = session_name
        st.session_state.current_session = session_name
        save_to_storage()
        # 加载该角色的头像（如果没有则默认为机器人）
        st.session_state.ai_avatar = session_data.get("avatar", "🤖")


def delete_session(session_name):
    """删除指定会话，并切换到其他会话或清空状态"""
    if session_name in st.session_state.user_sessions:
        del st.session_state.user_sessions[session_name]
        save_to_storage()
        
        if session_name == st.session_state.current_session:
            remaining_sessions = list(st.session_state.user_sessions.keys())
            if remaining_sessions:
                switch_to_session(remaining_sessions[0])
            else:
                st.session_state.current_session = None
                st.session_state.session_name = None
                st.session_state.name = None
                st.session_state.nature = None
                st.session_state.messages = []


def create_new_session(session_name, name, nature, avatar="🤖"):
    """创建一个新的会话并切换到该会话"""
    st.session_state.user_sessions[session_name] = {
        "name": name,
        "nature": nature,
        "avatar": avatar,
        "messages": []
    }
    switch_to_session(session_name)
    save_to_storage()


def save_current_avatar(avatar):
    """保存当前角色的头像"""
    if st.session_state.get('session_name'):
        st.session_state.ai_avatar = avatar
        st.session_state.user_sessions[st.session_state.session_name]["avatar"] = avatar
        save_to_storage()


def clear_current_messages():
    """清空当前会话的消息"""
    if st.session_state.get('session_name'):
        st.session_state.messages = []
        st.session_state.user_sessions[st.session_state.session_name]["messages"] = []
        save_to_storage()
