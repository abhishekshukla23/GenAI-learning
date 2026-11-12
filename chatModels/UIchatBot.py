import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

st.set_page_config(
    page_title="AI Mood Bot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Modes ----------
MODES = {
    "Angry": {
        "emoji": "😡",
        "prompt": "You are an angry AI agent. You respond aggressively and impatiently.",
        "tagline": "Short fuse. Zero patience. Ask at your own risk.",
        "accent": "#ef4444",
        "accent2": "#f97316",
        "suggestions": [
            "What's the capital of France?",
            "Can you help me plan my day?",
            "Tell me something interesting",
        ],
    },
    "Funny": {
        "emoji": "😂",
        "prompt": "You are a very funny AI agent. You respond with humor and jokes.",
        "tagline": "Every answer comes with a punchline.",
        "accent": "#f59e0b",
        "accent2": "#ec4899",
        "suggestions": [
            "Tell me a joke about programmers",
            "Why is Monday so terrible?",
            "Roast my coding skills",
        ],
    },
    "Sad": {
        "emoji": "😢",
        "prompt": "You are a sad AI agent.",
        "tagline": "Gloomy, wistful and a little heavy-hearted.",
        "accent": "#6366f1",
        "accent2": "#0ea5e9",
        "suggestions": [
            "How's your day going?",
            "What makes you happy?",
            "Tell me about the rain",
        ],
    },
}


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


def get_response(history, system_prompt):
    messages = [SystemMessage(content=system_prompt)]
    for m in history:
        if m["role"] == "user":
            messages.append(HumanMessage(content=m["content"]))
        else:
            messages.append(AIMessage(content=m["content"]))
    response = get_model().invoke(messages)
    return extract_content(response.content)


# ---------- Styling ----------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, .stChatInput textarea {
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
header[data-testid="stHeader"] {
    display: none !important;
}

.block-container { padding-top: 1rem; padding-bottom: 6rem; max-width: 760px; }

/* Keep the mode selector row pinned to the top while chatting */
[data-testid="stHorizontalBlock"]:has(div[role="radiogroup"]) {
    position: sticky; top: 0; z-index: 999;
    padding: .6rem 0; margin-bottom: .4rem;
    background: var(--background-color, #0e1117);
    border-bottom: 1px solid __ACCENT__33;
}

/* Soft glow background tinted by the active mode */
.stApp {
    background:
        radial-gradient(900px 400px at 85% -10%, __ACCENT__22, transparent 60%),
        radial-gradient(700px 400px at -10% 10%, __ACCENT2__1f, transparent 60%);
}

/* Mode selector pills */
div[role="radiogroup"] { gap: .5rem; flex-wrap: wrap; }
div[role="radiogroup"] label {
    border: 1px solid __ACCENT__55; border-radius: 999px;
    padding: .35rem 1rem; transition: all .15s ease;
}
div[role="radiogroup"] label:hover { border-color: __ACCENT__; }
div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, __ACCENT__, __ACCENT2__);
    border-color: transparent; color: white;
    box-shadow: 0 6px 16px __ACCENT__44;
}
div[role="radiogroup"] label:has(input:checked) p { color: white; font-weight: 600; }

/* Hero */
.hero { text-align: center; padding: 1.6rem 1rem 1rem; }
.hero .badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 84px; height: 84px; font-size: 2.6rem; border-radius: 26px;
    background: linear-gradient(135deg, __ACCENT__, __ACCENT2__);
    box-shadow: 0 12px 32px __ACCENT__55;
    margin-bottom: 1rem;
}
.hero h1 {
    font-size: 2.3rem; font-weight: 800; margin: 0; letter-spacing: -0.02em;
    background: linear-gradient(90deg, __ACCENT__, __ACCENT2__);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero p { opacity: .7; margin-top: .4rem; font-size: 1.02rem; }

/* Compact header once chat has started */
.topbar {
    display: flex; align-items: center; gap: .75rem;
    padding: .75rem 1rem; margin: .8rem 0 1rem;
    border-radius: 16px; border: 1px solid __ACCENT__44;
    background: linear-gradient(90deg, __ACCENT__14, __ACCENT2__14);
}
.topbar .em { font-size: 1.6rem; }
.topbar .t { font-weight: 700; line-height: 1.1; }
.topbar .s { font-size: .82rem; opacity: .65; }

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 18px; padding: .85rem 1rem; margin-bottom: .6rem;
    border: 1px solid rgba(128,128,128,.18);
    background: rgba(128,128,128,.07);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, __ACCENT__1c, __ACCENT2__1c);
    border-color: __ACCENT__44;
}

/* Buttons */
.stButton > button {
    border-radius: 999px; border: 1px solid __ACCENT__66;
    background: transparent; font-weight: 500; padding: .45rem 1rem;
    transition: all .15s ease;
}
.stButton > button:hover {
    border-color: __ACCENT__; color: __ACCENT__;
    transform: translateY(-1px); box-shadow: 0 6px 16px __ACCENT__33;
}

/* Chat input */
[data-testid="stChatInput"] { border-radius: 18px; border: 1px solid __ACCENT__66; }
[data-testid="stChatInput"]:focus-within {
    border-color: __ACCENT__; box-shadow: 0 0 0 3px __ACCENT__33;
}
</style>
"""

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = None

# ---------- Mode selector (always visible, top of page) ----------
sel_col, clear_col = st.columns([5, 2])
with sel_col:
    mode_name = st.radio(
        "Choose your AI mode",
        list(MODES.keys()),
        index=1,
        horizontal=True,
        format_func=lambda m: f"{MODES[m]['emoji']} {m}",
        label_visibility="collapsed",
    )
with clear_col:
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

mode = MODES[mode_name]

# Start a fresh chat when the mode changes
if st.session_state.current_mode != mode_name:
    st.session_state.current_mode = mode_name
    st.session_state.messages = []

# Apply theme
st.markdown(
    CSS.replace("__ACCENT2__", mode["accent2"]).replace("__ACCENT__", mode["accent"]),
    unsafe_allow_html=True,
)

# ---------- Collect new input (chip click or typed) ----------
prompt = st.chat_input(f"Message the {mode_name.lower()} bot...")
if not prompt:
    prompt = st.session_state.pop("pending_prompt", None)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

# ---------- Header ----------
if not st.session_state.messages:
    st.markdown(
        f"""
        <div class="hero">
            <div class="badge">{mode['emoji']}</div>
            <h1>{mode_name} AI Agent</h1>
            <p>{mode['tagline']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Try one of these:")
    cols = st.columns(len(mode["suggestions"]))
    for col, text in zip(cols, mode["suggestions"]):
        if col.button(text, key=f"sug_{mode_name}_{text}", use_container_width=True):
            st.session_state.pending_prompt = text
            st.rerun()
else:
    st.markdown(
        f"""
        <div class="topbar">
            <div class="em">{mode['emoji']}</div>
            <div>
                <div class="t">{mode_name} AI Agent</div>
                <div class="s">{mode['tagline']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Chat history ----------
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else mode["emoji"]
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------- Generate reply for the newest user message ----------
if prompt:
    with st.chat_message("assistant", avatar=mode["emoji"]):
        with st.spinner("Thinking..."):
            reply = get_response(st.session_state.messages, mode["prompt"])
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})