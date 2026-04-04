"""
公告模块 - 显示应用公告和更新日志
"""
import streamlit as st


def get_announcement_content():
    """
    获取公告内容
    
    在这里更新公告内容，每次发布新版本时修改此函数的返回值
    """
    return """
    ### ⚠️ 公告
    **程序由个人编写**
    **仅供娱乐，禁止商用**

    - 本应用为 AI 角色扮演聊天程序
    - 所有内容仅供娱乐和消遣
    - 禁止用于任何商业用途
    - 伴侣性格的自由度非常高，欢迎探索
    - 欢迎反馈 bug 和建议
    因为烧的是我自己的 token，有点费钱
    如果大家玩的开心的话
    可以发点小红包支持我
    一分两分不嫌少，一块两块喊大佬
    谢谢大家！！！

    v2.2 更新公告：
    - 新增共享写字板功能，所有用户均可留言反馈 bug 和建议
    - 留言全员可见，促进用户间交流
    - 支持删除自己的留言（通过用户标识验证）
    - 侧边栏新增快捷入口，方便随时访问
    
    v2.1 更新公告：
    - 新增 AI 头像自定义功能，支持 10 种预设头像和图片上传
    - 每个角色可独立设置头像，互不干扰
    - 头像数据随角色会话保存，切换角色时自动加载对应头像
    - 支持上传 PNG、JPG 格式图片作为头像
    
    v2.0 更新公告：
    - 新增账号登录功能，数据可存储在云端（支持多设备共享对话）
    - 新增游客登录功能，无需注册账号便可使用该程序（会话仅限本地存储）
    - 侧边栏新增 bug 与建议反馈，所有用户均可看见，请文明发言哦

    点击下方的 ✓ 按钮表示您已阅读并同意以上声明
    """


def show_announcement():
    """
    显示公告浮窗（仅首次访问时显示）
    """
    # 初始化公告显示状态
    if "disclaimer_shown" not in st.session_state:
        st.session_state.disclaimer_shown = False

    if not st.session_state.disclaimer_shown:
        with st.expander("📢 重要提示 - 请阅读", expanded=True):
            st.markdown(get_announcement_content())
            
            if st.button("✓ 我已阅读并同意", key="agree_disclaimer"):
                st.session_state.disclaimer_shown = True
                st.rerun()
        
        st.divider()
