import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI 챗봇", page_icon="🤖", layout="centered")

st.title("🤖 AI 챗봇")
st.caption("GPT-4o-mini 기반 챗봇입니다. 무엇이든 물어보세요!")

# API 키는 Streamlit Community Cloud의 secrets에서 가져옴
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" in st.session_state and st.button("대화 초기화", type="secondary"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 친절하고 유능한 AI 어시스턴트입니다. 한국어로 답변해 주세요."},
                *st.session_state.messages,
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
