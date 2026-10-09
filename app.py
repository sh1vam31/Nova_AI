import streamlit as st
import speech_recognition as sr
import os
import webbrowser
import datetime
import json
import re
import psutil
from utils import (
    ai_chat, ai_completion, save_ai_response, 
    get_weather, get_weather_data, calculate, get_news, save_note, read_notes
)
from config import apikey
import openai
from ai_providers import get_available_providers, get_provider_models, PROVIDERS

# Page configuration
st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Ultra-Professional Dark Theme CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"], section.main {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: #0B0F19 !important;
    color: #E2E8F0;
}

/* Header & Footer Styling */
header[data-testid="stHeader"] { 
    background: transparent !important; 
    z-index: 100 !important;
}
footer { visibility: hidden; }

/* Sidebar Collapse & Expand Toggle Arrow Buttons */
[data-testid="stSidebarCollapseButton"] {
    position: relative !important;
    margin-top: 1rem !important;
    display: flex !important;
    align-items: center !important;
    z-index: 999999 !important;
}

[data-testid="collapsedControl"] {
    position: relative !important;
    margin-top: 0.5rem !important;
    display: flex !important;
    align-items: center !important;
    z-index: 999999 !important;
}

button[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] button {
    background-color: #111827 !important;
    border: 1px solid #1F293D !important;
    color: #3B82F6 !important;
    border-radius: 8px !important;
    padding: 6px 12px !important;
    height: 36px !important;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.3) !important;
    transition: all 0.2s ease-in-out !important;
    cursor: pointer !important;
}
[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="collapsedControl"] button:hover {
    background-color: #1E293B !important;
    border-color: #3B82F6 !important;
    color: #60A5FA !important;
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.5) !important;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 98% !important;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0D1322;
}
::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

/* Sidebar Styling & Upper Space Removal */
section[data-testid="stSidebar"] {
    background-color: #0A0E17 !important;
    border-right: 1px solid #1E293B !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0rem !important;
}
[data-testid="stSidebarUserContent"] {
    padding-top: 0.2rem !important;
}
[data-testid="stSidebarHeader"] {
    height: 0px !important;
    min-height: 0px !important;
    padding: 0px !important;
    margin: 0px !important;
}

.brand-container {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.5rem 0 0.8rem 0 !important;
    margin-top: 0.2rem !important;
}
.brand-icon {
    font-size: 24px;
    background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0px 0px 10px rgba(59, 130, 246, 0.5));
}
.brand-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.5px;
    margin: 0;
}
.brand-sub {
    font-size: 0.75rem;
    color: #64748B;
    margin-top: -4px;
}

/* Sidebar Nav Pills */
.nav-section-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #475569;
    margin: 1.2rem 0 0.5rem 0;
}

.recent-chat-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    border-radius: 8px;
    background: #111827;
    border: 1px solid #1F293D;
    color: #CBD5E1;
    font-size: 0.85rem;
    margin-bottom: 6px;
    transition: all 0.2s ease;
    cursor: pointer;
}
.recent-chat-item:hover {
    border-color: #3B82F6;
    background: #1E293B;
    color: #F8FAFC;
}
.recent-chat-time {
    font-size: 0.7rem;
    color: #64748B;
}

/* User Profile Badge */
.user-profile-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    background: #111827;
    border: 1px solid #1E293B;
    border-radius: 12px;
    margin-top: 2rem;
}
.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: #FFFFFF;
}

/* Main Top Header */
.top-header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1.2rem;
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 14px;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}
.header-title-box {
    display: flex;
    align-items: center;
    gap: 12px;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 20px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #10B981;
    font-size: 0.75rem;
    font-weight: 500;
}
.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: #10B981;
    box-shadow: 0 0 8px #10B981;
}

/* Chat Messages */
.chat-bubble-user {
    background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
    border: 1px solid #3B82F6;
    color: #FFFFFF;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px auto;
    max-width: 80%;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
}

.chat-card-assistant {
    background: #111827;
    border: 1px solid #1F293D;
    padding: 16px 20px;
    border-radius: 16px 16px 16px 4px;
    margin: 10px 0;
    max-width: 88%;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.msg-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.msg-avatar-spark {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: white;
}

/* Rich Widgets */
.weather-card-widget {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 18px 22px;
    margin-top: 10px;
}
.weather-temp-main {
    font-size: 2.2rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-right: 12px;
}
.weather-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #1E293B;
    font-size: 0.85rem;
    color: #94A3B8;
}

.action-status-card {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.action-progress-bar {
    height: 4px;
    width: 100%;
    background: #1E293B;
    border-radius: 2px;
    overflow: hidden;
    margin-top: 6px;
}
.action-progress-fill {
    height: 100%;
    width: 100%;
    background: linear-gradient(90deg, #3B82F6, #10B981);
    animation: pulse 2s infinite;
}

/* Dashboard Cards (Right Column) */
.dash-card {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 14px;
}
.dash-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.85rem;
    font-weight: 600;
    color: #94A3B8;
    margin-bottom: 12px;
}

.stat-ring-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    text-align: center;
}
.stat-box {
    background: #111827;
    border: 1px solid #1F293D;
    border-radius: 10px;
    padding: 10px 4px;
}
.stat-val {
    font-size: 1.1rem;
    font-weight: 700;
    color: #38BDF8;
}
.stat-lbl {
    font-size: 0.68rem;
    color: #64748B;
    margin-top: 2px;
}

.clock-display {
    font-size: 1.35rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.5px;
}

/* Quick Action Buttons Grid */
.quick-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}

/* Streamlit Button Overrides */
div.stButton > button {
    background-color: #111827 !important;
    color: #E2E8F0 !important;
    border: 1px solid #1F293D !important;
    border-radius: 10px !important;
    padding: 0.4rem 0.6rem !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    word-break: keep-all !important;
    height: 44px !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease-in-out !important;
}
div.stButton > button:hover {
    background-color: #1E293B !important;
    border-color: #3B82F6 !important;
    color: #F8FAFC !important;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.25) !important;
}

/* Primary Mic Button Override */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #60A5FA !important;
    box-shadow: 0 0 18px rgba(37, 99, 235, 0.4) !important;
}

</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "command_history" not in st.session_state:
    st.session_state.command_history = [
        {"command": "Weather in London", "timestamp": "3 mins ago", "type": "weather"},
        {"command": "Open YouTube", "timestamp": "12 mins ago", "type": "website"},
        {"command": "Calculate 25 + 17", "timestamp": "2 hours ago", "type": "calculator"},
        {"command": "Save note Meeting at 4PM", "timestamp": "5 hours ago", "type": "note"}
    ]
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False

# Helper Functions
def say_text(text):
    try:
        os.system(f'say "{text}"')
    except Exception as e:
        pass

def take_voice_command():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # Increased duration to calibrate noise better
            r.adjust_for_ambient_noise(source, duration=1.0)
            # Increased timeout so it waits longer for you to start speaking
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
        query = r.recognize_google(audio, language="en-in")
        return query
    except sr.WaitTimeoutError:
        return "Error: I didn't hear anything. Please try speaking again."
    except sr.UnknownValueError:
        return "Error: I couldn't understand what you said."
    except Exception as e:
        return f"Error: {str(e)}"

def process_command(query, ai_model="gpt-3.5-turbo", temperature=0.7, ai_provider="openai"):
    query_lower = query.lower()
    response_data = {"type": "chat", "text": "", "extra": None}
    
    # Websites — comprehensive list with flexible matching
    sites = [
        ["youtube",         "https://www.youtube.com"],
        ["wikipedia",       "https://www.wikipedia.org"],
        ["google",          "https://www.google.com"],
        ["github",          "https://www.github.com"],
        ["stackoverflow",   "https://stackoverflow.com"],
        ["stack overflow",  "https://stackoverflow.com"],
        ["instagram",       "https://www.instagram.com"],
        ["whatsapp",        "https://web.whatsapp.com"],
        ["netflix",         "https://www.netflix.com"],
        ["linkedin",        "https://www.linkedin.com"],
        ["twitter",         "https://www.twitter.com"],
        ["x.com",           "https://www.x.com"],
        ["facebook",        "https://www.facebook.com"],
        ["reddit",          "https://www.reddit.com"],
        ["amazon",          "https://www.amazon.com"],
        ["spotify",         "https://open.spotify.com"],
        ["gmail",           "https://mail.google.com"],
        ["google drive",    "https://drive.google.com"],
        ["google docs",     "https://docs.google.com"],
        ["google maps",     "https://maps.google.com"],
        ["maps",            "https://maps.google.com"],
        ["chatgpt",         "https://chat.openai.com"],
        ["openai",          "https://www.openai.com"],
        ["notion",          "https://www.notion.so"],
        ["figma",           "https://www.figma.com"],
        ["twitch",          "https://www.twitch.tv"],
        ["discord",         "https://www.discord.com"],
        ["slack",           "https://www.slack.com"],
        ["zoom",            "https://zoom.us"],
        ["medium",          "https://www.medium.com"],
        ["canva",           "https://www.canva.com"],
        ["pinterest",       "https://www.pinterest.com"],
        ["snapchat",        "https://www.snapchat.com"],
        ["tiktok",          "https://www.tiktok.com"],
        ["flipkart",        "https://www.flipkart.com"],
        ["paytm",           "https://www.paytm.com"],
        ["hotstar",         "https://www.hotstar.com"],
        ["primevideo",      "https://www.primevideo.com"],
        ["prime video",     "https://www.primevideo.com"],
    ]

    # Trigger words that indicate the user wants to open something
    open_triggers = [
        "open", "launch", "go to", "navigate to", "visit",
        "show me", "take me to", "start", "load", "access", "browse"
    ]

    for site in sites:
        site_name = site[0]
        site_url  = site[1]
        # Check: trigger word + site name  OR  just the site name alone
        triggered = any(
            f"{trigger} {site_name}" in query_lower for trigger in open_triggers
        ) or query_lower.strip() == site_name

        if triggered:
            try:
                webbrowser.open(site_url)
                response_data["type"] = "website"
                response_data["text"] = f"Opening {site_name.title()}..."
                response_data["extra"] = {"site_name": site_name.title(), "url": site_url}
                return response_data
            except Exception as e:
                response_data["type"] = "error"
                response_data["text"] = f"Error opening {site_name}: {str(e)}"
                return response_data

    # Time & Date
    if "the time" in query_lower or "what time" in query_lower:
        curr_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        response_data["type"] = "time"
        response_data["text"] = f"Sir, the current time is {curr_time}"
        return response_data
        
    if "the date" in query_lower or "what date" in query_lower:
        curr_date = datetime.datetime.now().strftime("%B %d, %Y")
        response_data["type"] = "date"
        response_data["text"] = f"Today's date is {curr_date}"
        return response_data

    # Weather
    if "weather" in query_lower:
        city = "London"
        match = re.search(r'weather\s+(?:in|for|at|of)?\s*([a-zA-Z\s]+)', query, re.IGNORECASE)
        if match and match.group(1).strip():
            city = match.group(1).strip()
        wdata = get_weather_data(city)
        response_data["type"] = "weather"
        if "error" in wdata:
            response_data["text"] = wdata["error"]
        else:
            response_data["text"] = f"Here's the current weather in {wdata['city']}:"
            response_data["extra"] = wdata
        return response_data

    # Calculator
    if "calculate" in query_lower or ("what is" in query_lower and any(op in query_lower for op in ["+", "-", "*", "/"])):
        res = calculate(query)
        response_data["type"] = "calculator"
        response_data["text"] = res
        return response_data

    # Notes
    if "save note" in query_lower or "remember" in query_lower:
        note_content = query.replace("save note", "").replace("remember", "").strip()
        res = save_note(note_content)
        response_data["type"] = "note"
        response_data["text"] = res
        return response_data

    if "read notes" in query_lower or "show notes" in query_lower:
        res = read_notes()
        response_data["type"] = "note"
        response_data["text"] = res
        return response_data

    # Mac App Launcher — open native macOS apps by voice/text command
    import subprocess
    mac_apps = [
        ["notepad",         "TextEdit"],
        ["textedit",        "TextEdit"],
        ["notes",           "Notes"],
        ["calculator",      "Calculator"],
        ["calendar",        "Calendar"],
        ["finder",          "Finder"],
        ["terminal",        "Terminal"],
        ["vs code",         "Visual Studio Code"],
        ["vscode",          "Visual Studio Code"],
        ["visual studio code", "Visual Studio Code"],
        ["safari",          "Safari"],
        ["chrome",          "Google Chrome"],
        ["firefox",         "Firefox"],
        ["maps",            "Maps"],
        ["music",           "Music"],
        ["photos",          "Photos"],
        ["facetime",        "FaceTime"],
        ["messages",        "Messages"],
        ["mail",            "Mail"],
        ["reminders",       "Reminders"],
        ["preview",         "Preview"],
        ["activity monitor", "Activity Monitor"],
        ["system preferences", "System Preferences"],
        ["system settings", "System Settings"],
        ["app store",       "App Store"],
        ["xcode",           "Xcode"],
        ["whatsapp",        "WhatsApp"],
        ["telegram",        "Telegram"],
        ["slack",           "Slack"],
        ["zoom",            "zoom.us"],
        ["discord",         "Discord"],
        ["spotify",         "Spotify"],
        ["vlc",             "VLC"],
        ["pycharm",         "PyCharm"],
        ["cursor",          "Cursor"],
    ]

    for app_keyword, app_name in mac_apps:
        triggered = any(
            f"{trigger} {app_keyword}" in query_lower for trigger in open_triggers
        ) or query_lower.strip() == app_keyword

        if triggered:
            try:
                subprocess.Popen(["open", "-a", app_name])
                response_data["type"] = "website"
                response_data["text"] = f"Opening {app_name}..."
                response_data["extra"] = {"site_name": app_name, "url": ""}
                return response_data
            except Exception as e:
                response_data["type"] = "error"
                response_data["text"] = f"Couldn't open {app_name}: {str(e)}"
                return response_data

    # Default LLM Chat
    messages = [
        {"role": "system", "content": "You are Jarvis, a sleek, modern AI assistant running on macOS (Apple Mac). The user is on a Mac, NOT Windows. Always give Mac-specific instructions and commands. Be friendly, concise, and helpful."}
    ]
    for prev in st.session_state.chat_history[-8:]:
        messages.append({"role": prev["role"], "content": prev["content"]})
    messages.append({"role": "user", "content": query})
    
    ai_resp = ai_chat(messages, model=ai_model, temperature=temperature, provider=ai_provider)
    response_data["type"] = "chat"
    response_data["text"] = ai_resp
    return response_data

# ================= SIDEBAR (LEFT NAVIGATION DRAWER) =================
with st.sidebar:
    st.markdown("""
    <div class="brand-container">
        <div class="brand-icon">✦</div>
        <div>
            <div class="brand-title">Jarvis</div>
            <div class="brand-sub">AI Assistant for Your Desktop</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.chat_history = []
        st.success("Started new chat session!")
        st.rerun()

    st.markdown('<div class="nav-section-title">Navigation</div>', unsafe_allow_html=True)
    if st.button("💬 Chat Session", use_container_width=True):
        st.toast("Active: Chat Session", icon="💬")
    if st.button("💻 Control Laptop", use_container_width=True):
        st.toast("Control Laptop mode (Coming Soon!)", icon="💻")
    if st.button("📱 Apps & Files", use_container_width=True):
        st.toast("Apps & Files browser (Coming Soon!)", icon="📱")
    if st.button("📜 Command History", use_container_width=True):
        st.toast("Viewing Command History...", icon="📜")
    
    with st.expander("⚙️ Provider & Settings"):
        available_providers = get_available_providers() or ["openai"]
        provider_names = [PROVIDERS[p]["name"] for p in available_providers if p in PROVIDERS]
        provider_keys = [p for p in available_providers if p in PROVIDERS]
        
        selected_provider_name = st.selectbox("AI Provider", provider_names, index=0)
        selected_provider = provider_keys[provider_names.index(selected_provider_name)] if selected_provider_name in provider_names else "openai"
        
        provider_models = get_provider_models(selected_provider)
        model_options = provider_models if provider_models else ["gpt-3.5-turbo", "gpt-4"]
        ai_model = st.selectbox("AI Model", model_options)
        temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.7, 0.1)
        enable_tts = st.checkbox("Enable Speech Output", value=False)

    st.markdown('<div class="nav-section-title">Recent Chats</div>', unsafe_allow_html=True)
    recent_chats_list = [
        "Weather in London", "Open VS Code project", "Summarize PDF", "Create presentation", "Fix error in code"
    ]
    for rchat in recent_chats_list:
        st.markdown(f'''
        <div class="recent-chat-item">
            <span>💬 {rchat}</span>
            <span class="recent-chat-time">Recent</span>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("""
    <div class="user-profile-card">
        <div class="user-avatar">S</div>
        <div style="flex-grow: 1;">
            <div style="font-weight: 600; font-size: 0.85rem; color: #F8FAFC;">Shivam C.</div>
            <div style="font-size: 0.72rem; color: #10B981;">Pro Plan • Active</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= 2-COLUMN MAIN CONTENT (CENTER CHAT + RIGHT DASHBOARD) =================
col_main, col_dash = st.columns([3.2, 1.4])

# ----------------- CENTER COLUMN: CHAT INTERFACE -----------------
with col_main:
    # Header Bar
    st.markdown("""
    <div class="top-header-container">
        <div class="header-title-box">
            <span style="font-size: 22px;">🤖</span>
            <div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; display: flex; align-items: center; gap: 10px;">
                    Jarvis AI Assistant
                    <span class="status-pill"><span class="status-dot"></span> Online</span>
                </div>
                <div style="font-size: 0.78rem; color: #64748B;">Chat, get things done, and control your desktop — all in one place.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat Container Window
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div style="text-align: center; padding: 2.5rem 1rem; background: #0F172A; border: 1px solid #1E293B; border-radius: 16px; margin-bottom: 1.5rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">✨</div>
                <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">How can Jarvis assist you today?</h3>
                <p style="color: #64748B; font-size: 0.88rem; max-width: 500px; margin: 0 auto;">
                    Try asking for weather updates, controlling browser applications, saving notes, or having a complex AI conversation.
                </p>
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'''
                <div class="chat-bubble-user">
                    <div style="font-size: 0.92rem;">{msg["content"]}</div>
                    <div style="font-size: 0.68rem; opacity: 0.75; text-align: right; margin-top: 4px;">{msg.get("timestamp", "")}</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                resp_obj = msg.get("resp_data", {"type": "chat", "text": msg["content"], "extra": None})
                mtype = resp_obj.get("type", "chat")
                text_content = resp_obj.get("text", msg["content"])
                extra = resp_obj.get("extra", None)
                
                st.markdown(f'''
                <div class="chat-card-assistant">
                    <div class="msg-header">
                        <div class="msg-avatar-spark">✦</div>
                        <span style="font-weight: 600; font-size: 0.88rem; color: #F8FAFC;">Jarvis</span>
                        <span style="font-size: 0.7rem; color: #64748B; margin-left: auto;">{msg.get("timestamp", "")}</span>
                    </div>
                    <div style="font-size: 0.92rem; color: #CBD5E1;">{text_content}</div>
                ''', unsafe_allow_html=True)
                
                # Render Weather Widget Card if weather response
                if mtype == "weather" and extra and isinstance(extra, dict):
                    st.markdown(f'''
                    <div class="weather-card-widget">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div>
                                <span class="weather-temp-main">🌤️ {extra.get("temp", "--")}°C</span>
                                <span style="font-size: 1.05rem; font-weight: 600; color: #CBD5E1;">{extra.get("description", "Weather")}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #94A3B8;">📍 {extra.get("city")}, {extra.get("country")}</div>
                        </div>
                        <div class="weather-grid">
                            <div>Feels like: <strong style="color: #F8FAFC;">{extra.get("feels_like")}°C</strong></div>
                            <div>Humidity: <strong style="color: #F8FAFC;">{extra.get("humidity")}%</strong></div>
                            <div>Wind: <strong style="color: #F8FAFC;">{extra.get("wind_speed")} km/h</strong></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                # Render Action Progress Bar Card if Website Action
                elif mtype == "website" and extra:
                    st.markdown(f'''
                    <div class="action-status-card">
                        <span style="font-size: 24px;">🌐</span>
                        <div style="flex-grow: 1;">
                            <div style="font-weight: 600; font-size: 0.88rem; color: #F8FAFC;">Launching {extra.get("site_name")}</div>
                            <div style="font-size: 0.75rem; color: #64748B;">Opening application on your system...</div>
                            <div class="action-progress-bar"><div class="action-progress-fill"></div></div>
                        </div>
                        <span style="color: #10B981; font-size: 18px;">✓</span>
                    </div>
                    ''', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

    # Input Dock Area at Bottom
    st.markdown("<br>", unsafe_allow_html=True)

    # Session state for clearing input
    if "input_buffer" not in st.session_state:
        st.session_state.input_buffer = ""
    if "input_key_counter" not in st.session_state:
        st.session_state.input_key_counter = 0

    input_col1, input_col2, input_col3 = st.columns([4.2, 1.1, 0.9])

    with input_col1:
        user_text = st.text_input(
            "Message Jarvis...",
            placeholder="Ask Jarvis anything or give a command (e.g. 'Weather in London', 'Open YouTube')...",
            key=f"main_text_input_{st.session_state.input_key_counter}",
            label_visibility="collapsed"
        )

    with input_col2:
        send_clicked = st.button("✈️ Send", use_container_width=True)

    with input_col3:
        mic_clicked = st.button("🎙️ Speak", use_container_width=True, type="primary")

    # ── Handle Send ──────────────────────────────────────────────────────────
    if send_clicked and user_text:
        timestamp = datetime.datetime.now().strftime("%I:%M %p")
        st.session_state.chat_history.append({"role": "user", "content": user_text, "timestamp": timestamp})

        with st.spinner("Jarvis processing..."):
            resp = process_command(user_text, ai_model=ai_model, temperature=temperature, ai_provider=selected_provider)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": resp["text"],
                "resp_data": resp,
                "timestamp": timestamp
            })
            st.session_state.command_history.insert(0, {
                "command": user_text,
                "timestamp": timestamp,
                "type": resp["type"]
            })
            if enable_tts:
                say_text(resp["text"])

        # Clear input box by incrementing the key → forces a fresh widget
        st.session_state.input_key_counter += 1
        st.rerun()

    # ── Handle Speak / Mic ────────────────────────────────────────────────────
    if mic_clicked:
        with st.spinner("🎤 Listening... Speak now!"):
            voice_query = take_voice_command()
            if voice_query:
                if "Error" in voice_query:
                    st.error(f"Microphone issue: {voice_query}", icon="⚠️")
                    st.toast("Make sure your microphone is connected and allowed.", icon="🎤")
                else:
                    timestamp = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.chat_history.append({"role": "user", "content": voice_query, "timestamp": timestamp})
                    resp = process_command(voice_query, ai_model=ai_model, temperature=temperature, ai_provider=selected_provider)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": resp["text"],
                        "resp_data": resp,
                        "timestamp": timestamp
                    })
                    if enable_tts:
                        say_text(resp["text"])
                    st.session_state.input_key_counter += 1
                    st.rerun()

# ----------------- RIGHT COLUMN: DASHBOARD & QUICK CONTROLS -----------------
with col_dash:
    # 1. System Status Card
    cpu_pct = psutil.cpu_percent()
    mem_pct = psutil.virtual_memory().percent
    disk_pct = psutil.disk_usage('/').percent
    try:
        batt = psutil.sensors_battery()
        batt_pct = batt.percent if batt else 92
    except:
        batt_pct = 92

    st.markdown(f'''
    <div class="dash-card">
        <div class="dash-card-header">
            <span>📊 System Status</span>
            <span style="color: #10B981; font-weight: 500;">● Operational</span>
        </div>
        <div class="stat-ring-container">
            <div class="stat-box">
                <div class="stat-val">{int(cpu_pct)}%</div>
                <div class="stat-lbl">CPU</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{int(mem_pct)}%</div>
                <div class="stat-lbl">Memory</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{int(disk_pct)}%</div>
                <div class="stat-lbl">Disk</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{int(batt_pct)}%</div>
                <div class="stat-lbl">Battery</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 2. Digital Clock & Date Card
    curr_time_str = datetime.datetime.now().strftime("%I:%M:%S %p")
    curr_date_str = datetime.datetime.now().strftime("%a, %b %d, %Y")
    st.markdown(f'''
    <div class="dash-card">
        <div class="dash-card-header">
            <span>📅 Local Time</span>
            <span style="color: #38BDF8;">{curr_date_str}</span>
        </div>
        <div class="clock-display">⏰ {curr_time_str}</div>
        <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">📍 System Location • Active</div>
    </div>
    ''', unsafe_allow_html=True)

    # 3. Quick Actions Grid
    st.markdown('<div class="dash-card-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
    
    qcol1, qcol2 = st.columns(2)
    with qcol1:
        if st.button("▶️ YouTube", use_container_width=True):
            webbrowser.open("https://www.youtube.com")
            st.toast("Opening YouTube...")
        if st.button("🌤️ Weather", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Weather in London", "timestamp": "Now"})
            wresp = process_command("Weather in London")
            st.session_state.chat_history.append({"role": "assistant", "content": wresp["text"], "resp_data": wresp, "timestamp": "Now"})
            st.rerun()
    with qcol2:
        if st.button("🌐 Google", use_container_width=True):
            webbrowser.open("https://www.google.com")
            st.toast("Opening Google...")
        if st.button("🧮 Calculator", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Calculate 25 * 4", "timestamp": "Now"})
            cresp = process_command("Calculate 25 * 4")
            st.session_state.chat_history.append({"role": "assistant", "content": cresp["text"], "resp_data": cresp, "timestamp": "Now"})
            st.rerun()

    # 4. Recent Commands Feed
    st.markdown('<div class="dash-card-header" style="margin-top: 1rem;">📜 Recent Commands</div>', unsafe_allow_html=True)
    for cmd_item in st.session_state.command_history[:4]:
        st.markdown(f'''
        <div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; font-size: 0.8rem;">
            <span style="color: #CBD5E1;">⚡ {cmd_item["command"]}</span>
            <span style="color: #64748B; font-size: 0.7rem;">{cmd_item["timestamp"]}</span>
        </div>
        ''', unsafe_allow_html=True)
