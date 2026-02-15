import streamlit as st
import requests
import os
import time
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://confidential-maryjo-odiluk-23764298.koyeb.app/api/v1")

# Page Config
st.set_page_config(
    page_title="SensiBOT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* 1. THEME */
    .stApp {
        background-color: #343541;
        color: #d1d5db;
    }
    section[data-testid="stSidebar"] {
        background-color: #202123;
        border-right: 1px solid #4d4d4f;
    }
    
    /* 2. HEADERS */
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ececf1;
        padding: 15px 5px;
        text-align: center;
        border-bottom: 1px solid #4d4d4f;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ececf1;
        margin-bottom: 1rem;
    }
    .start-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        text-align: center;
        color: #ececf1;
    }

    /* 3. CHAT BUBBLES */
    div[data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* 4. NEW CHAT BUTTON (Green) */
    section[data-testid="stSidebar"] button[kind="secondary"] {
        background-color: #0fa47f !important;
        border: 1px solid #0fa47f !important;
        color: white !important;
        transition: background-color 0.2s;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: #0d8a6a !important;
        border-color: #0d8a6a !important;
    }

    /* 5. INPUT AREA STYLING (FIXED RED BORDER) */
    .stTextInput {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%; 
        z-index: 1000;
    }
    
    /* Input Field */
    .stTextInput input {
        background-color: #40414f;
        color: white;
        border: 1px solid #2f303d !important;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
        padding-left: 50px !important; /* Space for + button */
        height: 54px;
    }
    
    /* OVERRIDE RED FOCUS */
    .stTextInput input:focus {
        border-color: #6b6c7b !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* 6. UPLOAD BUTTON ("+") - INSIDE INPUT */
    /* Position relative to viewport but aligned with the centered input */
    /* Input is centered (left: 50%, transX -50%). Width 60%. */
    /* Left edge of input is at 20% of viewport width. */
    /* We place button at 20% + a small margin. */
    
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 28px; /* Vertically centered in the 54px input (approx) */
        left: calc(20% + 10px); /* 20% is the start of the 60% wide centered input */
        z-index: 1001;
        width: 40px;
        height: 40px;
    }

    div[data-testid="stPopover"] button {
        background-color: transparent !important;
        border: none !important;
        color: #acacbe !important;
        padding: 0 !important;
        font-size: 24px !important;
        height: 100% !important;
        width: 100% !important;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: none !important;
    }

    div[data-testid="stPopover"] button:hover {
        color: white !important;
        background-color: rgba(255,255,255,0.1) !important;
        border-radius: 6px;
    }
    
    /* Media Query for Mobile responsiveness */
    @media (max-width: 768px) {
        .stTextInput {
            width: 90%;
        }
        div[data-testid="stPopover"] {
            left: calc(5% + 10px); /* 5% is start of 90% wide input */
        }
    }

    /* 7. PILLS */
    .pill-container {
        position: fixed;
        bottom: 85px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        display: flex;
        gap: 10px;
        z-index: 999;
        pointer-events: none; 
    }
    .file-pill {
        pointer-events: auto;
        background-color: #40414f;
        border: 1px solid #565869;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.8rem;
        color: #ececf1;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* History Items */
    div.stButton > button:first-child {
        text-align: left;
        border: none;
        background: transparent;
    }
    div.stButton > button:hover {
        background-color: #2a2b32;
    }

</style>
""", unsafe_allow_html=True)

# --- Session Logic ---
if "sessions" not in st.session_state:
    default_id = str(uuid.uuid4())
    st.session_state.sessions = {
        default_id: {
            "id": default_id, "title": "New Chat", "messages": [], "files": [] 
        }
    }
    st.session_state.active_session_id = default_id

def get_active_session():
    if st.session_state.active_session_id not in st.session_state.sessions:
        if st.session_state.sessions:
            st.session_state.active_session_id = list(st.session_state.sessions.keys())[0]
        else:
            new_id = str(uuid.uuid4())
            st.session_state.sessions[new_id] = {
                "id": new_id, "title": "New Chat", "messages": [], "files": []
            }
            st.session_state.active_session_id = new_id
    return st.session_state.sessions[st.session_state.active_session_id]

def delete_session(session_id):
    active = st.session_state.sessions[session_id]
    for f in active["files"]:
        try:
            requests.delete(f"{API_BASE_URL}/documents/{f}")
        except:
            pass
    del st.session_state.sessions[session_id]
    st.rerun()

# --- API ---
def upload_file_api(file):
    try:
        files = {"file": (file.name, file, file.type)}
        res = requests.post(f"{API_BASE_URL}/documents/upload", files=files)
        return res.status_code == 200
    except:
        return False

# ---------------- LAYOUT ----------------

# 1. SIDEBAR
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 SensiBOT</div>', unsafe_allow_html=True)
    
    if st.button("✨ New Chat", type="secondary", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {
            "id": new_id, "title": "New Chat", "messages": [], "files": []
        }
        st.session_state.active_session_id = new_id
        st.rerun()

    st.markdown("---")
    st.caption("History")

    ids = list(st.session_state.sessions.keys())
    for sid in reversed(ids):
        sess = st.session_state.sessions[sid]
        if len(sess["messages"]) > 0:
            isActive = (sid == st.session_state.active_session_id)
            title = f"**{sess['title']}**" if isActive else sess['title']
            
            c1, c2 = st.columns([0.85, 0.15])
            if c1.button(title, key=f"c_{sid}", use_container_width=True):
                st.session_state.active_session_id = sid
                st.rerun()
            with c2.popover("⋮"):
                st.write("Actions")
                if st.button("Delete", key=f"d_{sid}"):
                    delete_session(sid)

# 2. MAIN
active = get_active_session()

if not active["messages"]:
    st.markdown(
        """
        <div class="start-screen">
            <div style="font-size: 5rem; margin-bottom: 20px;">🤖</div>
            <div class="main-title">SensiBOT</div>
            <p>Ready to help.</p>
        </div>
        """, unsafe_allow_html=True
    )

for msg in active["messages"]:
    with st.chat_message(msg["role"], avatar="🤖" if msg["role"]=="assistant" else None):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "usage" in msg:
            st.caption(f"💰 ${msg['usage'].get('estimated_cost',0):.6f}")

# 3. UPLOAD BUTTON (The "Plus")
with st.popover("➕", use_container_width=False):
    st.markdown("### Upload")
    uploaded = st.file_uploader("File", type=["pdf", "txt"], label_visibility="collapsed")
    if uploaded:
        if st.button(f"Upload {uploaded.name}"):
            with st.spinner("Processing..."):
                if upload_file_api(uploaded):
                    active["files"].append(uploaded.name)
                    st.success("Done!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Failed")

# 4. PILLS
if active["files"]:
    files_html = "".join([f'<div class="file-pill">📄 {f}</div>' for f in active["files"]])
    st.markdown(f'<div class="pill-container">{files_html}</div>', unsafe_allow_html=True)

# 5. INPUT
if prompt := st.chat_input("Message SensiBOT..."):
    active["messages"].append({"role": "user", "content": prompt})
    if len(active["messages"]) == 1:
        active["title"] = (prompt[:18] + "..") if len(prompt) > 20 else prompt
    st.rerun()

# 6. RESPONSE
if active["messages"] and active["messages"][-1]["role"] == "user":
    last_msg = active["messages"][-1]["content"]
    with st.chat_message("assistant", avatar="🤖"):
        ph = st.empty()
        has_files = len(active["files"]) > 0
        payload = {"message": last_msg, "use_rag": has_files, "conversation_id": active["id"]}
        try:
            with st.spinner("Thinking..."):
                res = requests.post(f"{API_BASE_URL}/chat", json=payload)
                if res.status_code == 200:
                    d = res.json()
                    ph.markdown(d["response"])
                    st.caption(f"💰 ${d.get('usage',{}).get('estimated_cost',0):.6f}")
                    active["messages"].append({"role": "assistant", "content": d["response"], "usage": d.get("usage",{})})
                else:
                    ph.error(res.text)
        except Exception as e:
            ph.error(str(e))
