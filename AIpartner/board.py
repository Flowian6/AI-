"""
共享写字板模块 - 处理 Bug 反馈和建议
"""
import streamlit as st
import hashlib
import json
import os
from datetime import datetime


def save_shared_board():
    """保存共享写字板到服务器"""
    board_file = "shared_board.json"
    with open(board_file, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.shared_board_messages, f, ensure_ascii=False, indent=2)


def get_user_identifier(author):
    """获取用户的唯一标识"""
    if not author:
        return None
    return hashlib.md5(f"user_{author}".encode()).hexdigest()[:16]


def add_board_message(author, content):
    """添加留言到共享写字版"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    message_id = hashlib.md5(f"{timestamp}{content}".encode()).hexdigest()[:8]
    user_identifier = get_user_identifier(author)
    
    st.session_state.shared_board_messages.append({
        "id": message_id,
        "author": author,
        "content": content,
        "timestamp": timestamp,
        "user_identifier": user_identifier
    })
    
    save_shared_board()
    st.session_state.board_user_identifier = user_identifier


def delete_board_message(message_id, user_identifier):
    """删除指定的留言，只有发布者才能删除"""
    for i, message in enumerate(st.session_state.shared_board_messages):
        if message["id"] == message_id and message["user_identifier"] == user_identifier:
            del st.session_state.shared_board_messages[i]
            save_shared_board()
            return True
    return False


def show_shared_board():
    """显示共享写字板页面"""
    st.title("📝 共享写字板 - Bug 反馈与建议")
    st.markdown("---")
    
    st.info("💡 欢迎在此反馈 bug 或提出建议！所有人的留言都是可见的，方便大家交流和反馈问题。")
    
    with st.form("board_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            author = st.text_input("昵称（可选）", placeholder="请输入您的昵称", key="board_author")
        with col2:
            submit_button = st.form_submit_button("提交留言", use_container_width=True)
        
        content = st.text_area("留言内容", placeholder="请详细描述您遇到的 bug 或建议...", height=100, key="board_content")
        
        if submit_button:
            if content.strip():
                if not author.strip():
                    author = "匿名用户"
                add_board_message(author, content)
                st.success("✅ 留言已提交，感谢您的反馈！")
                st.rerun()
            else:
                st.error("❌ 请输入留言内容！")
    
    st.markdown("---")
    st.subheader(f"📋 留言列表 ({len(st.session_state.shared_board_messages)}条)")
    
    if st.session_state.shared_board_messages:
        for message in reversed(st.session_state.shared_board_messages):
            with st.chat_message("user", avatar="👤"):
                col1, col2 = st.columns([6, 1])
                with col1:
                    st.markdown(f"**{message['author']}** · {message['timestamp']}")
                    st.write(message['content'])
                with col2:
                    current_user_id = st.session_state.get('board_user_identifier', None)
                    if current_user_id and current_user_id == message['user_identifier']:
                        if st.button("🗑️ 删除", key=f"delete_msg_{message['id']}", type="secondary", use_container_width=True):
                            if delete_board_message(message['id'], message['user_identifier']):
                                st.success("✅ 留言已删除")
                                st.rerun()
                            else:
                                st.error("❌ 删除失败，请刷新页面后重试")
    else:
        st.warning("暂无留言，快来成为第一个反馈的人吧！")


def init_shared_board():
    """初始化共享写字版"""
    if "shared_board_messages" not in st.session_state:
        board_file = "shared_board.json"
        if os.path.exists(board_file):
            with open(board_file, 'r', encoding='utf-8') as f:
                st.session_state.shared_board_messages = json.load(f)
        else:
            st.session_state.shared_board_messages = []
