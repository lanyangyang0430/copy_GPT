import streamlit as st
import requests

# ========== DeepSeek 接口调用 ==========
def query_deepseek_r1(messages, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": messages}
    
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "出错了，请稍后重试。")

# ========== 地理助手设定 ==========
preset_answers = {
    "河口冲击岛是怎么形成的": "结合之前的学习内容，河口冲积岛是在河流、海水、地转偏向力的共同作用下形成的，其中外力搬运与堆积作用贯穿了整个地理过程。由于受力情况的复杂性，河口冲击岛有着连续的生消过程。",
    "崇明岛的沙洲是如何演变的": "由于长期受河流泥沙堆积与海水顶托的作用，长江河口处在唐初形成了沙洲，这是崇明岛的雏形，而后宋元期间沙洲不断形成、扩展，明末清初合并，完成了基本地貌塑造。在这一进程中，岛屿整体往河口移动。",
    "崇明岛的形态在未来会如何变化": "老师，我认为，就像三沙的生消过程一样，长江自西向东流，受地转偏向力的影响，冲刷南岸，在北岸沉积。因此，崇明岛的面积在不断扩大，最终会并向北岸陆地，新的冲积岛会取代崇明岛的地位，成为长江新一轮旋回的河口巨型沙洲。",
    "如何规划崇明岛的未来发展": "我们应结合人地协调观，坚持可持续发展目标，用现实案例教育学生如何平衡好保护与发展，合理引导崇明岛未来的生态利用与空间开发。"
}

other_response = "我们先把关注的重心放在本节课探讨的内容上吧！"

# ========== Streamlit 页面 ==========
st.set_page_config(page_title="地理学习助手", page_icon="🌍", layout="wide")
st.title("🌍 地理学习助手")
st.caption("你的随身地理老师")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.initialized = False

# ========== 初次加载欢迎语 ==========
if not st.session_state.initialized:
    welcome_text = (
        "同学们好，欢迎来到《崇明岛的前世今生》课堂，请大家思考以下几个问题：\n\n"
        "1. 河口冲击岛是怎么形成的？\n"
        "2. 崇明岛的沙洲是如何演变的？\n"
        "3. 崇明岛的形态在未来会如何变化？\n"
        "4. 如何规划崇明岛的未来发展？"
    )
    with st.chat_message("assistant"):
        st.markdown(welcome_text)
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})
    st.session_state.initialized = True

# ========== 预设问题按钮 ==========
st.markdown("### 📌 快速提问")
col1, col2 = st.columns(2)
with col1:
    if st.button("河口冲击岛是怎么形成的？"):
        user_input = "河口冲击岛是怎么形成的"
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)
        reply = preset_answers["河口冲击岛是怎么形成的"]
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    if st.button("崇明岛的形态在未来会如何变化？"):
        user_input = "崇明岛的形态在未来会如何变化"
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)
        reply = preset_answers["崇明岛的形态在未来会如何变化"]
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

with col2:
    if st.button("崇明岛的沙洲是如何演变的？"):
        user_input = "崇明岛的沙洲是如何演变的"
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)
        reply = preset_answers["崇明岛的沙洲是如何演变的"]
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    if st.button("如何规划崇明岛的未来发展？"):
        user_input = "如何规划崇明岛的未来发展"
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)
        reply = preset_answers["如何规划崇明岛的未来发展"]
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ========== 自由提问对话框 ==========
user_input = st.chat_input("请输入您的问题...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # 判断是否为预设问题
    matched = False
    for key in preset_answers:
        if key in user_input:
            reply = preset_answers[key]
            matched = True
            break

    if not matched:
        reply = other_response
    
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
