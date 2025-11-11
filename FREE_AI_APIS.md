# 🆓 Free AI API Setup Guide

This guide will help you set up free AI APIs as alternatives to OpenAI. These providers offer free tiers that work great for chat applications.

## Available Free AI Providers

### 1. **Groq** ⚡ (Recommended - Very Fast & Free)
- **Free Tier**: Yes, generous free tier
- **Speed**: Extremely fast responses
- **Models**: Llama 3.1 (8B Instant), Llama 3.3 (70B), Mixtral, Gemma 2
- **Recommended Model**: `llama-3.1-8b-instant` (fast and reliable)
- **Get API Key**: https://console.groq.com/
- **Setup**:
  1. Sign up at https://console.groq.com/
  2. Create an API key
  3. Add to `.env` file: `GROQ_API_KEY=your_key_here`
- **Note**: The app will automatically use the best available model if your selected model isn't available

### 2. **Hugging Face** 🤗 (Free)
- **Free Tier**: Yes, free inference API
- **Models**: Mistral, Gemma, Llama 2
- **Get API Key**: https://huggingface.co/settings/tokens
- **Setup**:
  1. Sign up at https://huggingface.co/
  2. Go to Settings > Access Tokens
  3. Create a new token
  4. Add to `.env` file: `HUGGINGFACE_API_KEY=your_key_here`

### 3. **Together AI** 🚀 (Free Tier)
- **Free Tier**: Yes, $25 free credits
- **Models**: Llama 2, Mixtral, and more
- **Get API Key**: https://api.together.xyz/
- **Setup**:
  1. Sign up at https://api.together.xyz/
  2. Get your API key
  3. Add to `.env` file: `TOGETHER_API_KEY=your_key_here`

### 4. **Anthropic Claude** 🧠 (Free Trial)
- **Free Tier**: Yes, free trial with credits
- **Models**: Claude 3 Haiku, Claude 3 Sonnet
- **Get API Key**: https://console.anthropic.com/
- **Setup**:
  1. Sign up at https://console.anthropic.com/
  2. Create an API key
  3. Add to `.env` file: `ANTHROPIC_API_KEY=your_key_here`

## Quick Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get API keys** from the providers above (pick one or more)

3. **Add to `.env` file**:
   ```bash
   # Choose one or more free providers
   GROQ_API_KEY=your_groq_key_here
   HUGGINGFACE_API_KEY=your_huggingface_key_here
   TOGETHER_API_KEY=your_together_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

5. **Select provider** in the sidebar under "AI Settings"

## Recommended Setup

**For best performance and speed:**
- Use **Groq** - It's free, fast, and reliable
- Get API key from: https://console.groq.com/
- Add `GROQ_API_KEY=your_key` to `.env`

**For most models:**
- Use **Hugging Face** - Largest model selection
- Get API key from: https://huggingface.co/settings/tokens
- Add `HUGGINGFACE_API_KEY=your_key` to `.env`

## Features

- ✅ **Automatic Fallback**: If OpenAI fails, automatically tries free providers
- ✅ **Provider Selection**: Choose your preferred AI provider in the UI
- ✅ **Multiple Models**: Each provider offers different models
- ✅ **Free Tier Support**: All providers have free tiers
- ✅ **No Credit Card Required**: Most providers don't require credit card for free tier

## Provider Comparison

| Provider | Speed | Free Tier | Models | Ease of Setup |
|----------|-------|-----------|--------|---------------|
| Groq | ⚡⚡⚡ Very Fast | ✅ Generous | Llama, Mixtral, Gemma | ⭐⭐⭐ Easy |
| Hugging Face | ⚡⚡ Fast | ✅ Free | Mistral, Gemma, Llama | ⭐⭐⭐ Easy |
| Together AI | ⚡⚡ Fast | ✅ $25 Credits | Llama, Mixtral | ⭐⭐⭐ Easy |
| Anthropic | ⚡⚡ Fast | ✅ Free Trial | Claude 3 | ⭐⭐⭐ Easy |

## Troubleshooting

### "API key not found" error
- Make sure you've added the API key to your `.env` file
- Check that the key name matches exactly (e.g., `GROQ_API_KEY`)
- Restart the app after adding the key

### "Provider not available" error
- Install required packages: `pip install groq huggingface-hub together anthropic`
- Check that your API key is valid
- Verify the provider's service status

### Slow responses
- Try Groq for fastest responses
- Check your internet connection
- Some models are slower than others

## Need Help?

- Check the provider's documentation
- Verify your API key is correct
- Make sure you have an active internet connection
- Check that the required packages are installed

---

**Enjoy using free AI APIs! 🎉**

