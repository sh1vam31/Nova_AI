import streamlit as st
import speech_recognition as sr
import os
import webbrowser
import datetime
import time
import json
from utils import (
    ai_chat, ai_completion, save_ai_response, 
    get_weather, calculate, get_news, save_note, read_notes
)
from config import apikey
import openai
from ai_providers import get_available_providers, get_provider_models, PROVIDERS

openai.api_key = apikey

# Page configuration
st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .assistant-message {
        background-color: #f1f8e9;
        text-align: left;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3rem;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "command_history" not in st.session_state:
    st.session_state.command_history = []
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False
if "notes" not in st.session_state:
    st.session_state.notes = []

# Helper functions
def say_text(text):
    """Text-to-speech using system command"""
    try:
        os.system(f'say "{text}"')
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")

def take_voice_command():
    """Capture voice command from microphone"""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        query = r.recognize_google(audio, language="en-in")
        return query
    except sr.WaitTimeoutError:
        return "Timeout: No speech detected"
    except sr.UnknownValueError:
        return "Could not understand audio"
    except Exception as e:
        return f"Error: {str(e)}"

def process_command(query, ai_model="gpt-3.5-turbo", temperature=0.7, ai_provider="openai"):
    """Process user command and return response"""
    query_lower = query.lower()
    response = ""
    command_type = "chat"
    
    # Website opening
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"],
        ["github", "https://www.github.com"],
        ["stackoverflow", "https://www.stackoverflow.com"],
        ["instagram", "https://www.instagram.com"],
        ["facebook", "https://www.facebook.com"],
        ["twitter", "https://www.twitter.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["reddit", "https://www.reddit.com"],
        ["whatsapp", "https://web.whatsapp.com"],
        ["gmail", "https://mail.google.com"],
        ["netflix", "https://www.netflix.com"],
        ["spotify", "https://open.spotify.com"],
    ]
    
    for site in sites:
        # Check for "open [site]" command - more flexible matching
        site_patterns = [f"open {site[0]}", f"open {site[0]}.com", f"open {site[0]}.net"]
        if any(pattern in query_lower for pattern in site_patterns):
            response = f"Opening {site[0]}..."
            try:
                webbrowser.open(site[1])
                command_type = "website"
                return response, command_type
            except Exception as e:
                return f"Error opening {site[0]}: {str(e)}", "error"
    
    # Time
    if "the time" in query_lower or "what time" in query_lower:
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        response = f"Sir, the time is {hour}:{minute}"
        command_type = "time"
        return response, command_type
    
    # Date
    if "the date" in query_lower or "what date" in query_lower:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        response = f"Today's date is {date}"
        command_type = "date"
        return response, command_type
    
    # Weather
    if "weather" in query_lower:
        city = "London"  # Default city
        # Try to extract city name from query
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() == "weather" and i + 1 < len(words):
                city = words[i + 1]
                break
        response = get_weather(city)
        command_type = "weather"
        return response, command_type
    
    # Calculator
    if "calculate" in query_lower or "what is" in query_lower and any(op in query_lower for op in ["+", "-", "*", "/", "plus", "minus", "times", "divided"]):
        response = calculate(query)
        command_type = "calculator"
        return response, command_type
    
    # News
    if "news" in query_lower:
        topic = "technology"
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() == "news" and i + 1 < len(words):
                topic = words[i + 1]
                break
        response = get_news(topic)
        command_type = "news"
        return response, command_type
    
    # Notes
    if "save note" in query_lower or "remember" in query_lower:
        note_content = query
        if "save note" in query_lower:
            note_content = query.replace("save note", "").strip()
        elif "remember" in query_lower:
            note_content = query.replace("remember", "").strip()
        response = save_note(note_content)
        command_type = "note"
        return response, command_type
    
    if "read notes" in query_lower or "show notes" in query_lower:
        response = read_notes()
        command_type = "note"
        return response, command_type
    
    # AI completion
    if "using artificial intelligence" in query_lower:
        prompt = query
        ai_response = ai_completion(prompt)
        save_ai_response(prompt, ai_response)
        response = ai_response
        command_type = "ai_completion"
        return response, command_type
    
    # Default: Chat with AI
    # Build conversation context with more history for better conversations
    messages = [{"role": "system", "content": "You are Jarvis, a helpful AI assistant. Be conversational, friendly, and helpful. Keep responses concise but engaging. You can have natural conversations with the user."}]
    
    # Include more chat history for context (last 10 messages = 5 exchanges)
    for chat in st.session_state.chat_history[-10:]:
        if chat["role"] == "user":
            messages.append({"role": "user", "content": chat["content"]})
        elif chat["role"] == "assistant":
            messages.append({"role": "assistant", "content": chat["content"]})
    
    messages.append({"role": "user", "content": query})
    
    try:
        response = ai_chat(messages, model=ai_model, temperature=temperature, provider=ai_provider)
        command_type = "chat"
    except Exception as e:
        response = f"Error: {str(e)}"
        command_type = "error"
    
    return response, command_type

# Main UI
st.markdown('<h1 class="main-header">🤖 Jarvis AI Assistant</h1>', unsafe_allow_html=True)

# Welcome message on first run
if not st.session_state.chat_history:
    st.info("👋 Welcome to Jarvis AI Assistant! You can interact with me using text or voice commands. Check out the sidebar for settings and quick commands.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Voice settings
    st.subheader("Voice Settings")
    enable_tts = st.checkbox("Enable Text-to-Speech", value=True)
    language = st.selectbox("Language", ["en-in", "en-us", "en-gb"])
    
    # AI Settings
    st.subheader("AI Settings")
    
    # Get available providers
    available_providers = get_available_providers()
    if not available_providers:
        available_providers = ["openai"]  # Default fallback
    
    # Provider selection
    provider_names = [PROVIDERS[p]["name"] for p in available_providers if p in PROVIDERS]
    provider_keys = [p for p in available_providers if p in PROVIDERS]
    
    if not provider_names:
        provider_names = ["OpenAI (GPT-3.5/GPT-4)"]
        provider_keys = ["openai"]
    
    selected_provider_name = st.selectbox(
        "AI Provider",
        provider_names,
        index=0
    )
    selected_provider = provider_keys[provider_names.index(selected_provider_name)] if selected_provider_name in provider_names else (available_providers[0] if available_providers else "openai")
    
    # Model selection based on provider
    provider_models = get_provider_models(selected_provider)
    if selected_provider == "openai":
        model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
    elif provider_models:
        model_options = provider_models
    else:
        model_options = ["default"]
    
    ai_model = st.selectbox("AI Model", model_options)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    
    # Show provider info
    if selected_provider in PROVIDERS:
        provider_info = PROVIDERS[selected_provider]
        if provider_info["free_tier"]:
            st.info(f"✅ {provider_info['name']} - Free tier available")
        else:
            st.warning(f"💰 {provider_info['name']} - Paid service")
    
    # Show API key status
    st.caption("💡 Tip: Add API keys to .env file to enable providers")
    
    # Features
    st.subheader("Features")
    show_history = st.checkbox("Show Command History", value=True)
    auto_save = st.checkbox("Auto-save Responses", value=True)
    
    # Quick actions
    st.subheader("Quick Actions")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.command_history = []
        st.success("Chat history cleared!")
    
    if st.button("📥 Export Chat"):
        if st.session_state.chat_history:
            chat_data = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="Download Chat History",
                data=chat_data,
                file_name=f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Status
    st.subheader("Status")
    if st.session_state.is_listening:
        st.error("🎤 Listening...")
    else:
        st.success("✅ Ready")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat")
    
    # Chat history display
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><b>You:</b> {chat["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><b>Jarvis:</b> {chat["content"]}</div>', unsafe_allow_html=True)
                if "timestamp" in chat:
                    st.caption(f"Time: {chat['timestamp']}")
    
    # Input methods
    st.subheader("Input Method")
    input_method = st.radio("Choose input method:", ["Text", "Voice"], horizontal=True)
    
    if input_method == "Text":
        user_input = st.text_input("Type your message:", key="text_input")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Send", use_container_width=True):
                if user_input:
                    with st.spinner("Processing..."):
                        response, command_type = process_command(user_input, ai_model=ai_model, temperature=temperature, ai_provider=selected_provider)
                        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                        
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": user_input,
                            "timestamp": timestamp
                        })
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response,
                            "timestamp": timestamp,
                            "type": command_type
                        })
                        st.session_state.command_history.append({
                            "command": user_input,
                            "response": response,
                            "type": command_type,
                            "timestamp": timestamp
                        })
                        
                        if enable_tts:
                            say_text(response)
                        
                        st.rerun()
        
        with col_btn2:
            if st.button("🗣️ Voice Input", use_container_width=True):
                st.session_state.is_listening = True
                with st.spinner("Listening... Speak now!"):
                    try:
                        query = take_voice_command()
                        if query and "Error" not in query and "Timeout" not in query and "Could not understand" not in query:
                            # Process the voice command directly
                            with st.spinner("Processing your command..."):
                                response, command_type = process_command(query, ai_model=ai_model, temperature=temperature, ai_provider=selected_provider)
                                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                                
                                st.session_state.chat_history.append({
                                    "role": "user",
                                    "content": query,
                                    "timestamp": timestamp
                                })
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": response,
                                    "timestamp": timestamp,
                                    "type": command_type
                                })
                                st.session_state.command_history.append({
                                    "command": query,
                                    "response": response,
                                    "type": command_type,
                                    "timestamp": timestamp
                                })
                                
                                if enable_tts:
                                    say_text(response)
                                
                                st.rerun()
                        else:
                            st.warning(f"Voice recognition: {query}")
                            st.session_state.is_listening = False
                    except Exception as e:
                        st.error(f"Voice input error: {str(e)}")
                        st.session_state.is_listening = False
                    finally:
                        if st.session_state.is_listening:
                            st.session_state.is_listening = False
    
    else:  # Voice input
        st.info("Click the button below to start voice recognition")
        if st.button("🎤 Start Listening", use_container_width=True, type="primary"):
            st.session_state.is_listening = True
            with st.spinner("Listening... Speak now!"):
                try:
                    query = take_voice_command()
                    if query and "Error" not in query and "Timeout" not in query:
                        with st.spinner("Processing your command..."):
                            response, command_type = process_command(query, ai_model=ai_model, temperature=temperature)
                            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                            
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": query,
                                "timestamp": timestamp
                            })
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": response,
                                "timestamp": timestamp,
                                "type": command_type
                            })
                            st.session_state.command_history.append({
                                "command": query,
                                "response": response,
                                "type": command_type,
                                "timestamp": timestamp
                            })
                            
                            if enable_tts:
                                say_text(response)
                            
                            st.success(f"You said: {query}")
                            st.success(f"Jarvis: {response}")
                            st.rerun()
                    else:
                        st.warning(query)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    st.session_state.is_listening = False

with col2:
    st.header("📊 Information")
    
    # Current time
    st.subheader("⏰ Current Time")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    st.metric("Time", current_time)
    st.metric("Date", current_date)
    
    # Quick commands
    st.subheader("⚡ Quick Commands")
    quick_commands = [
        "What's the time?",
        "What's the date?",
        "Open YouTube",
        "Open Google",
        "Calculate 25 + 17",
        "Weather in London",
    ]
    
    for cmd in quick_commands:
        if st.button(cmd, key=f"quick_{cmd}", use_container_width=True):
            with st.spinner("Processing..."):
                response, command_type = process_command(cmd, ai_model=ai_model, temperature=temperature, ai_provider=selected_provider)
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": cmd,
                    "timestamp": timestamp
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": timestamp,
                    "type": command_type
                })
                
                if enable_tts:
                    say_text(response)
                
                st.rerun()
    
    # Command history
    if show_history and st.session_state.command_history:
        st.subheader("📜 Recent Commands")
        for cmd in st.session_state.command_history[-5:]:
            with st.expander(f"{cmd['timestamp']} - {cmd['type']}"):
                st.write(f"**Command:** {cmd['command']}")
                st.write(f"**Response:** {cmd['response'][:100]}...")

# Footer
st.markdown("---")
st.markdown("### 🎯 Available Commands")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("• Open YouTube")
    st.write("• Open Instagram")
    st.write("• Open WhatsApp")
    st.write("• Open Google")
    st.write("• Open Wikipedia")
with col2:
    st.write("• What's the time?")
    st.write("• What's the date?")
    st.write("• Weather in [city]")
with col3:
    st.write("• Calculate [expression]")
    st.write("• Save note [content]")
    st.write("• Read notes")
    st.write("• Chat naturally with Jarvis")

