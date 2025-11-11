# 🔑 How to Get Your OpenAI API Key

This guide will walk you through getting your OpenAI API key step by step.

## Step-by-Step Instructions

### Step 1: Create an OpenAI Account
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Click on **"Sign up"** or **"Log in"** if you already have an account
3. Sign up with your email address, or use Google/Microsoft account

### Step 2: Navigate to API Keys
1. Once logged in, click on your **profile icon** (top right corner)
2. Select **"API keys"** from the dropdown menu
   - Or go directly to: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Step 3: Create a New API Key
1. Click on **"+ Create new secret key"** button
2. Give your key a name (e.g., "Jarvis AI Assistant")
3. Click **"Create secret key"**
4. **IMPORTANT**: Copy the API key immediately - you won't be able to see it again!
   - It will look like: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 4: Add Credits to Your Account
1. OpenAI requires credits to use their API
2. Go to **"Billing"** → **"Add payment method"** or **"Add credits"**
3. Add at least $5-$10 to get started (you'll be charged only for what you use)
4. Note: OpenAI has a pay-as-you-go pricing model

### Step 5: Add API Key to Your Project
1. In your project folder, create a file named `.env`
2. Add the following line:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-api-key-here
   ```
3. Replace `sk-proj-your-actual-api-key-here` with your actual API key
4. Save the file

### Step 6: Verify Your Setup
1. Make sure the `.env` file is in the same folder as `app.py`
2. The `.env` file should NOT be committed to git (it's already in `.gitignore`)
3. Run the application: `streamlit run app.py`

## 📋 Quick Checklist

- [ ] Created OpenAI account
- [ ] Generated API key
- [ ] Added payment method/credits to account
- [ ] Created `.env` file in project folder
- [ ] Added `OPENAI_API_KEY=your_key_here` to `.env` file
- [ ] Verified `.env` is in `.gitignore` (for security)

## 💰 Pricing Information

OpenAI uses a pay-as-you-go pricing model:
- **GPT-3.5-turbo**: ~$0.002 per 1K tokens (very affordable)
- **text-davinci-003**: ~$0.02 per 1K tokens
- Typical conversation: 100-500 tokens
- You can set usage limits in your OpenAI account settings

## 🔒 Security Tips

1. **Never share your API key publicly**
2. **Never commit `.env` file to git** (already in `.gitignore`)
3. **Don't post your API key on forums or social media**
4. **Rotate your API key** if you suspect it's been compromised
5. **Set usage limits** in your OpenAI account to prevent unexpected charges

## ❓ Troubleshooting

### "Invalid API Key" Error
- Check that you copied the entire key (starts with `sk-`)
- Verify there are no extra spaces in the `.env` file
- Make sure the `.env` file is in the correct location
- Restart the application after adding the key

### "Insufficient Credits" Error
- Add credits to your OpenAI account
- Check your billing settings
- Verify your payment method is active

### "Rate Limit Exceeded" Error
- You've made too many requests too quickly
- Wait a few minutes and try again
- Consider upgrading your OpenAI plan

## 🔗 Useful Links

- [OpenAI Platform](https://platform.openai.com/)
- [API Keys Page](https://platform.openai.com/api-keys)
- [OpenAI Pricing](https://openai.com/pricing)
- [OpenAI Documentation](https://platform.openai.com/docs)
- [Billing & Usage](https://platform.openai.com/account/billing)

## 🆘 Need Help?

If you're still having issues:
1. Check the OpenAI status page: [https://status.openai.com/](https://status.openai.com/)
2. Review OpenAI's documentation
3. Check your account billing and usage
4. Verify your API key is active in your OpenAI account

---

**Remember**: Keep your API key secret and secure! 🔐

