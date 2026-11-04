import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

st.set_page_config(page_title="Funny AI Agent", page_icon="🤡", layout="centered")


# ---------- Model logic ----------
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-large-4", temperature=0.9)


def extract_content(content):
    if isinstance(content, list):
        text_parts = [
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "".join(text_parts).strip()
    return str(content)


def get_response(history):
    messages = [SystemMessage(content="You are a funny AI agent")]
    for m in history:
        if m["role"] == "user":
            messages.append(HumanMessage(content=m["content"]))
        else:
            messages.append(AIMessage(content=m["content"]))
    response = get_model().invoke(messages)
    return extract_content(response.content)


# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🤡 Funny AI Agent")
    st.caption("Powered by Mistral")
    st.divider()
    st.selectbox("Model", ["mistral-large-4"], disabled=True)
    st.slider("Temperature", 0.0, 1.0, 0.9, 0.1, disabled=True)
    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- Header ----------
st.title("🤡 Funny AI Agent")
st.caption("Ask me anything. I promise to be mildly amusing.")

# ---------- Chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Input ----------
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_response(st.session_state.messages)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})