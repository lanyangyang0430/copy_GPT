import streamlit as st
import requests

# DeepSeek 接口调用
def query_deepseek_r1(messages, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": messages}
    response = requests.post(url, json=data, headers=headers)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "出错了，请稍后重试。")

# 设置关键词列表
KEY_TERMS = [
    "冲积岛", "泥沙沉积", "河口三角洲", "水流速度", "海水顶托", "地转偏向力",
    "沙洲迁移", "湿地扩张", "海岸侵蚀", "海平面上升", "潮汐作用",
    "围垦造田", "三峡工程", "防护堤坝", "生态农业", "过度开发",
    "生态保护区", "湿地修复", "碳中和", "生态旅游", "环境承载力","崇明岛"
]

# Streamlit 页面设置
st.set_page_config(page_title="地理学习助手", page_icon="🌍", layout="wide")
st.title("🌍 地理学习助手")
st.caption("你的随身地理老师")

api_key = "sk-580808926dbf44b2980e912d2e8384cf"  # 替换为你的实际Key

# 聊天记录初始化
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.initialized = False

# 初次欢迎语
if not st.session_state.initialized:
    welcome = (
        "同学们好，欢迎来到《崇明岛的前世今生》课堂，请大家思考以下几个问题：\n\n"
        "1. 河口冲积岛是怎么形成的？\n"
        "2. 崇明岛的沙洲是如何演变的？\n"
        "3. 崇明岛的形态在未来会如何变化？\n"
        "4. 如何规划崇明岛的未来发展？"
    )
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    st.session_state.initialized = True

# 快速提问（改为四个按钮）
st.markdown("### ✏️ 试试这样问 ➜")
col1, col2 = st.columns(2)

with col1:
    if st.button("河口冲积岛是怎么形成的？"):
        question = "河口冲积岛是怎么形成的？"
        answer = "结合之前的学习内容，河口冲积岛是在河流、海水、地转偏向力的共同作用下形成的，其中外力搬运与堆积作用贯穿了整个地理过程。由于受力情况的复杂性，河口冲积岛有着连续的生消过程。"
        st.chat_message("user").markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    if st.button("崇明岛的沙洲是如何演变的？"):
        question = "崇明岛的沙洲是如何演变的？"
        answer = "由于长期受河流泥沙堆积与海水顶托的作用，长江河口处在唐初形成了沙洲，这是崇明岛的雏形，而后宋元期间沙洲不断形成、扩展，明末清初合并，完成了基本地貌塑造。在这一进程中，岛屿整体往河口移动。"
        st.chat_message("user").markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

with col2:
    if st.button("崇明岛的形态在未来会如何变化？"):
        question = "崇明岛的形态在未来会如何变化？"
        answer = "老师，我认为，就像三沙的生消过程一样，长江自西向东流，受地转偏向力的影响，冲刷南岸，在北岸沉积。因此，崇明岛的面积在不断扩大，最终会并向北岸陆地，新的冲积岛会取代崇明岛的地位，成为长江新一轮旋回的河口巨型沙洲。"
        st.chat_message("user").markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    if st.button("如何规划崇明岛的未来发展？"):
        question = "如何规划崇明岛的未来发展？"
        answer = "我们应结合人地协调观，坚持可持续发展目标，用现实案例教育学生如何平衡好保护与发展，合理引导崇明岛未来的生态利用与空间开发。"
        st.chat_message("user").markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# ✅ 在页面顶部循环显示全部对话记录（包括按钮触发和 AI 回答）
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 主对话框
user_input = st.chat_input("请输入您的问题...")
if user_input:
    # 记录用户发言
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 检查是否包含关键词（决定是否调用 AI）
    if any(term in user_input for term in KEY_TERMS):
        # 构造对话历史上下文（保留所有会话）
        deepseek_prompt = [
            {"role": "system", "content": "你是高中地理老师，教学严谨而生动，结合地理教材内容与现实案例讲解课程知识。请贴合课程内容、地理原理和人地协调观，结合可持续发展的真实案例进行讲解。"},
            *st.session_state.messages
        ]
        response = query_deepseek_r1(deepseek_prompt, api_key)
    else:
        response = "我们先把关注的重心放在本节课探讨的内容上吧！"

    # 显示 AI 回应
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
