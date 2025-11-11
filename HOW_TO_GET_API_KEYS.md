# 🔑 How to Get Free AI API Keys

This guide will walk you through getting free API keys for all the supported AI providers. **You only need ONE API key** to get started, but you can add multiple for more options.

## 🚀 Quick Start - Get Groq API Key (Recommended)

**Groq is the fastest and easiest to set up!**

### Step 1: Sign Up
1. Go to https://console.groq.com/
2. Click **"Sign Up"** or **"Sign In"** if you already have an account
3. Sign up with your email, Google, or GitHub account

### Step 2: Get API Key
1. Once logged in, you'll see your API keys on the dashboard
2. Click **"Create API Key"** or copy an existing key
3. **Copy the API key** - it looks like: `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 3: Add to Your Project
1. Open your `.env` file in the project folder
2. Add this line:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
3. Save the file

### Step 4: Test It
1. Run: `streamlit run app.py`
2. In the sidebar, select **"Groq (Free & Fast)"** as the AI Provider
3. Start chatting!

**That's it! Groq is free and very fast. No credit card required.**

---

## 🤗 Hugging Face API Key

### Step 1: Sign Up
1. Go to https://huggingface.co/
2. Click **"Sign Up"** in the top right
3. Create an account (free)

### Step 2: Get API Key
1. Once logged in, click on your **profile icon** (top right)
2. Go to **"Settings"**
3. Click on **"Access Tokens"** in the left sidebar
4. Click **"New token"**
5. Give it a name (e.g., "Jarvis AI")
6. Select **"Read"** permission (enough for inference)
7. Click **"Generate token"**
8. **Copy the token** immediately - it looks like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 3: Add to Your Project
1. Open your `.env` file
2. Add this line:
   ```
   HUGGINGFACE_API_KEY=hf_your_actual_key_here
   ```
3. Save the file

### Step 4: Test It
1. Run: `streamlit run app.py`
2. Select **"Hugging Face (Free)"** as the AI Provider
3. Start chatting!

**Hugging Face is completely free. No credit card required.**

---

## 🚀 Together AI API Key

### Step 1: Sign Up
1. Go to https://api.together.xyz/
2. Click **"Sign Up"** or **"Get Started"**
3. Create an account with your email

### Step 2: Get API Key
1. Once logged in, go to your **dashboard**
2. You'll see your API key displayed
3. Click **"Copy"** to copy the API key
4. It looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 3: Add to Your Project
1. Open your `.env` file
2. Add this line:
   ```
   TOGETHER_API_KEY=your_actual_key_here
   ```
3. Save the file

### Step 4: Test It
1. Run: `streamlit run app.py`
2. Select **"Together AI (Free Tier)"** as the AI Provider
3. Start chatting!

**Together AI gives you $25 in free credits. No credit card required for free tier.**

---

## 🧠 Anthropic Claude API Key

### Step 1: Sign Up
1. Go to https://console.anthropic.com/
2. Click **"Sign Up"** or **"Get Started"**
3. Create an account with your email

### Step 2: Get API Key
1. Once logged in, go to **"API Keys"** in the sidebar
2. Click **"Create Key"**
3. Give it a name (e.g., "Jarvis AI")
4. Click **"Create Key"**
5. **Copy the API key** immediately - it looks like: `sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 3: Add to Your Project
1. Open your `.env` file
2. Add this line:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-your_actual_key_here
   ```
3. Save the file

### Step 4: Test It
1. Run: `streamlit run app.py`
2. Select **"Anthropic Claude (Free Trial)"** as the AI Provider
3. Start chatting!

**Anthropic Claude offers a free trial with credits. Credit card may be required.**

---

## 📝 Complete .env File Example

Here's what your `.env` file should look like with multiple API keys:

```bash
# Free AI API Keys (Choose one or more)
GROQ_API_KEY=gsk_your_groq_key_here
HUGGINGFACE_API_KEY=hf_your_huggingface_key_here
TOGETHER_API_KEY=your_together_key_here
ANTHROPIC_API_KEY=sk-ant-api03-your_anthropic_key_here

# Optional: OpenAI (Paid)
OPENAI_API_KEY=sk-proj-your_openai_key_here

# Optional: Weather API
WEATHER_API_KEY=your_weather_key_here

# Optional: News API
NEWS_API_KEY=your_news_key_here
```

---

## ✅ Which Provider Should I Use?

### 🏆 Best for Speed: **Groq**
- ⚡ Extremely fast responses
- 🆓 Free tier
- ✅ No credit card required
- 📦 Easy to set up
- **Recommended for most users**

### 🎯 Best for Variety: **Hugging Face**
- 🤗 Largest selection of models
- 🆓 Completely free
- ✅ No credit card required
- 📚 Great for experimentation

### 💰 Best for Credits: **Together AI**
- 💵 $25 free credits
- 🆓 Free tier available
- ✅ No credit card required
- 🚀 Good performance

### 🧠 Best for Quality: **Anthropic Claude**
- 🎯 High-quality responses
- 🆓 Free trial
- ⚠️ Credit card may be required
- 💼 Good for professional use

---

## 🔧 Troubleshooting

### "API key not found" Error
- Make sure you've added the key to your `.env` file
- Check that there are no extra spaces around the `=`
- Verify the key name is exactly correct (e.g., `GROQ_API_KEY`)
- Restart the app after adding the key

### "Invalid API key" Error
- Verify you copied the entire key (no truncation)
- Check that the key hasn't expired
- Make sure you're using the correct key format
- Try generating a new key

### "Provider not available" in UI
- Make sure the API key is in your `.env` file
- Check that the key name matches exactly
- Verify the key is valid and active
- Restart the app

### Key Not Working
- Check the provider's website for service status
- Verify your account is active
- Make sure you haven't exceeded rate limits
- Try generating a new API key

---

## 🎯 Quick Comparison

| Provider | Speed | Free Tier | Credit Card | Setup Difficulty |
|----------|-------|-----------|-------------|------------------|
| **Groq** | ⚡⚡⚡ Very Fast | ✅ Yes | ❌ No | ⭐ Easy |
| **Hugging Face** | ⚡⚡ Fast | ✅ Yes | ❌ No | ⭐ Easy |
| **Together AI** | ⚡⚡ Fast | ✅ Yes ($25) | ❌ No | ⭐ Easy |
| **Anthropic** | ⚡⚡ Fast | ✅ Trial | ⚠️ Maybe | ⭐⭐ Medium |

---

## 📚 Additional Resources

- **Groq Documentation**: https://console.groq.com/docs
- **Hugging Face Docs**: https://huggingface.co/docs
- **Together AI Docs**: https://docs.together.ai/
- **Anthropic Docs**: https://docs.anthropic.com/

---

## 🆘 Need Help?

1. Check the provider's status page
2. Verify your API key is correct
3. Make sure your `.env` file is in the project root
4. Restart the app after adding keys
5. Check the error messages for specific issues

---

## 🎉 You're All Set!

Once you've added at least one API key to your `.env` file:
1. Run: `streamlit run app.py`
2. Select your preferred provider in the sidebar
3. Start chatting with Jarvis!

**Remember**: You only need **ONE** API key to get started. Groq is recommended for the best experience!

---

**Happy chatting! 🚀**

