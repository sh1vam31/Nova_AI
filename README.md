#Nova AI Assistant

A modern voice and text-controlled AI assistant with a beautiful web UI built using Streamlit. Jarvis can help you with various tasks including web browsing, calculations, weather, notes, and AI-powered conversations.

## ✨ Features

### Core Features
- 🎤 **Voice Recognition**: Speak commands naturally
- 💬 **Text Input**: Type commands if you prefer
- 🤖 **AI Chat**: Conversational AI using multiple providers
  - **OpenAI** (GPT-3.5, GPT-4) - Paid
  - **Groq** (Llama, Mixtral) - 🆓 Free & Very Fast
  - **Hugging Face** (Mistral, Gemma) - 🆓 Free
  - **Together AI** (Llama, Mixtral) - 🆓 Free Tier
  - **Anthropic Claude** - 🆓 Free Trial
- 🌐 **Web Navigation**: Open websites with voice commands
- ⏰ **Time & Date**: Get current time and date
- 🌤️ **Weather**: Get weather information (requires API key)
- 🧮 **Calculator**: Perform mathematical calculations
- 📝 **Notes**: Save and retrieve notes
- 📰 **News**: Get news updates (requires API key)

### UI Features
- 🎨 **Modern Interface**: Beautiful, responsive web UI
- 💾 **Chat History**: View conversation history
- 📊 **Command History**: Track all commands and responses
- ⚙️ **Settings Panel**: Customize voice, AI model, and more
- 📥 **Export Chat**: Download chat history as JSON
- 🎯 **Quick Commands**: One-click access to common commands

## 🚀 Quick Start

1. **Clone the repository** (or download the files)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Get a FREE API key** (choose one):
   - **Groq** (Recommended - Fast & Free): https://console.groq.com/
   - **Hugging Face** (Free): https://huggingface.co/settings/tokens
   - **Together AI** (Free Tier): https://api.together.xyz/
   - **Anthropic Claude** (Free Trial): https://console.anthropic.com/
   
   📖 **Step-by-step instructions**: See [HOW_TO_GET_API_KEYS.md](HOW_TO_GET_API_KEYS.md) for detailed guide
4. **Create `.env` file** and add your API key:
   ```
   GROQ_API_KEY=your_groq_key_here
   ```
   (Or use any other free provider)
5. **Run the app**: `streamlit run app.py`
6. **Select provider** in the sidebar and start chatting!

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Microphone (for voice input)
- macOS (for text-to-speech using `say` command) - Linux/Windows users can use `pyttsx3` instead

### Setup Steps

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**:
   - Create a `.env` file in the project root
   - **For Free AI (Recommended)**: Add a free AI API key:
     ```
     # Groq (Recommended - Fast & Free)
     GROQ_API_KEY=your_groq_api_key_here
     
     # OR Hugging Face (Free)
     HUGGINGFACE_API_KEY=your_huggingface_api_key_here
     
     # OR Together AI (Free Tier)
     TOGETHER_API_KEY=your_together_api_key_here
     ```
   - **For OpenAI (Optional - Paid)**:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - **Free AI Setup**: See [FREE_AI_APIS.md](FREE_AI_APIS.md) for detailed instructions on free AI providers
   - **OpenAI Setup**: See [GET_API_KEY.md](GET_API_KEY.md) for OpenAI API key instructions
   - **Optional**: Add Weather and News API keys:
     ```
     WEATHER_API_KEY=your_weather_api_key_here
     NEWS_API_KEY=your_news_api_key_here
     ```

4. **Run the application**:
   
   **Option 1: Using the run script (Recommended)**:
   ```bash
   ./run.sh
   ```
   
   **Option 2: Manual run**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**:
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in the terminal

## 📖 Usage

### Voice Commands

- **"Open YouTube"** - Opens YouTube in your browser
- **"Open Google"** - Opens Google
- **"What's the time?"** - Gets current time
- **"What's the date?"** - Gets current date
- **"Weather in London"** - Gets weather for a city
- **"Calculate 25 + 17"** - Performs calculations
- **"Save note [content]"** - Saves a note
- **"Read notes"** - Reads saved notes
- **"Using artificial intelligence [prompt]"** - Uses AI for specific tasks

### Text Input

Simply type your command in the text input field and click "Send" or press Enter.

### Quick Commands

Use the quick command buttons in the sidebar for common tasks.

## 🔧 Configuration

### Settings Panel

- **Voice Settings**:
  - Enable/disable text-to-speech
  - Choose language (en-in, en-us, en-gb)

- **AI Settings**:
  - Select AI model (gpt-3.5-turbo, text-davinci-003)
  - Adjust temperature (0.0 - 1.0)

- **Features**:
  - Show/hide command history
  - Auto-save responses

## 🎯 Available Commands

### Website Commands
- Open YouTube
- Open Google
- Open Wikipedia
- Open GitHub
- Open StackOverflow

### Information Commands
- What's the time?
- What's the date?
- Weather in [city]
- News about [topic]

### Utility Commands
- Calculate [expression]
- Save note [content]
- Read notes

### AI Commands
- Chat naturally with Jarvis
- "Using artificial intelligence [your prompt]"

## 🔒 Security

- API keys are stored in `.env` file (not committed to git)
- Use environment variables for sensitive data
- Never share your API keys publicly

## 🐛 Troubleshooting

### Voice Recognition Issues
- Make sure your microphone is working
- Check microphone permissions in system settings
- Try speaking clearly and in a quiet environment

### API Key Issues
- Verify your OpenAI API key is correct
- Check that the `.env` file exists and contains the key
- Ensure you have credits in your OpenAI account

### Text-to-Speech Issues
- On macOS, the `say` command should work by default
- On Linux, install `espeak` or `festival`
- On Windows, install `pyttsx3` dependencies

## 🚧 Future Enhancements

- [ ] Support for more languages
- [ ] Integration with calendar and reminders
- [ ] Email sending capabilities
- [ ] Music playback control
- [ ] Screen recording and screenshot
- [ ] File management commands
- [ ] Integration with smart home devices


**Enjoy using Jarvis AI Assistant! 🚀**

