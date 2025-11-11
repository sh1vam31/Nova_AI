"""
Free AI API Providers
Supports multiple free AI APIs as alternatives to OpenAI
"""
import os
import requests
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

# Provider configurations
PROVIDERS = {
    "openai": {
        "name": "OpenAI (GPT-3.5/GPT-4)",
        "requires_key": True,
        "free_tier": False,
        "key_env": "OPENAI_API_KEY"
    },
    "groq": {
        "name": "Groq (Free & Fast)",
        "requires_key": True,
        "free_tier": True,
        "key_env": "GROQ_API_KEY",
        "models": ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]
    },
    "huggingface": {
        "name": "Hugging Face (Free)",
        "requires_key": True,
        "free_tier": True,
        "key_env": "HUGGINGFACE_API_KEY",
        "models": ["mistralai/Mistral-7B-Instruct-v0.2", "google/gemma-7b-it", "meta-llama/Llama-2-7b-chat-hf"]
    },
    "together": {
        "name": "Together AI (Free Tier)",
        "requires_key": True,
        "free_tier": True,
        "key_env": "TOGETHER_API_KEY",
        "models": ["meta-llama/Llama-2-70b-chat-hf", "mistralai/Mixtral-8x7B-Instruct-v0.1"]
    },
    "anthropic": {
        "name": "Anthropic Claude (Free Trial)",
        "requires_key": True,
        "free_tier": True,
        "key_env": "ANTHROPIC_API_KEY",
        "models": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229"]
    }
}

def get_provider_key(provider: str) -> Optional[str]:
    """Get API key for a provider"""
    if provider not in PROVIDERS:
        return None
    key_env = PROVIDERS[provider]["key_env"]
    return os.getenv(key_env)

def chat_groq(messages: List[Dict], model: str = "llama-3.1-8b-instant", temperature: float = 0.7) -> str:
    """Chat using Groq API (Free & Very Fast)"""
    try:
        from groq import Groq
        
        api_key = get_provider_key("groq")
        if not api_key:
            return "Error: GROQ_API_KEY not found in .env file. Get a free key from https://console.groq.com/"
        
        client = Groq(api_key=api_key)
        
        # Available models (llama-3.1-70b-versatile is deprecated, use llama-3.3-70b-versatile instead)
        available_models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]
        
        # Replace deprecated model with the new one
        if model == "llama-3.1-70b-versatile":
            model = "llama-3.3-70b-versatile"
        
        # Build list of models to try (requested model first, then fallbacks)
        if model in available_models:
            models_to_try = [model] + [m for m in available_models if m != model]
        else:
            # If model not in available list, use all available models
            models_to_try = available_models
        
        last_error = None
        for model_to_try in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=model_to_try,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=1000
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                last_error = e
                error_msg = str(e)
                # If it's not a model-specific error (like auth), break immediately
                if "401" in error_msg or "unauthorized" in error_msg.lower():
                    break
                # Continue trying other models for model-specific errors
                if "400" in error_msg or "model" in error_msg.lower() or "deprecated" in error_msg.lower():
                    continue
                # For other errors, break
                break
        
        # If all models failed, return helpful error
        error_msg = str(last_error) if last_error else "Unknown error"
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            return "Error: Invalid Groq API key. Please check your GROQ_API_KEY in the .env file."
        elif "400" in error_msg or "model" in error_msg.lower() or "deprecated" in error_msg.lower():
            available_models_str = ", ".join(available_models)
            return f"Error: Could not find a working model. Tried: {', '.join(models_to_try[:3])}... Available models: {available_models_str}. Please check Groq's status or try a different model."
        return f"Error with Groq API: {error_msg}"
    except ImportError:
        return "Error: groq package not installed. Run: pip install groq"
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            return "Error: Invalid Groq API key. Please check your GROQ_API_KEY in the .env file."
        return f"Error with Groq API: {error_msg}"

def chat_huggingface(messages: List[Dict], model: str = "mistralai/Mistral-7B-Instruct-v0.2", temperature: float = 0.7) -> str:
    """Chat using Hugging Face Inference API (Free)"""
    try:
        api_key = get_provider_key("huggingface")
        if not api_key:
            return "Error: HUGGINGFACE_API_KEY not found in .env file. Get a free key from https://huggingface.co/settings/tokens"
        
        # Convert messages to prompt format
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                prompt += f"System: {content}\n\n"
            elif role == "user":
                prompt += f"User: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        prompt += "Assistant: "
        
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": temperature,
                "return_full_text": False
            }
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
            elif isinstance(result, dict):
                return result.get("generated_text", str(result)).strip()
            return str(result).strip()
        else:
            return f"Error: Hugging Face API returned status {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error with Hugging Face API: {str(e)}"

def chat_together(messages: List[Dict], model: str = "meta-llama/Llama-2-70b-chat-hf", temperature: float = 0.7) -> str:
    """Chat using Together AI API (Free Tier)"""
    try:
        api_key = get_provider_key("together")
        if not api_key:
            return "Error: TOGETHER_API_KEY not found in .env file. Get a free key from https://api.together.xyz/"
        
        api_url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: Together AI API returned status {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error with Together AI API: {str(e)}"

def chat_anthropic(messages: List[Dict], model: str = "claude-3-haiku-20240307", temperature: float = 0.7) -> str:
    """Chat using Anthropic Claude API (Free Trial)"""
    try:
        import anthropic
        
        api_key = get_provider_key("anthropic")
        if not api_key:
            return "Error: ANTHROPIC_API_KEY not found in .env file. Get a free key from https://console.anthropic.com/"
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Convert messages format for Claude
        system_message = None
        claude_messages = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                system_message = content
            elif role in ["user", "assistant"]:
                claude_messages.append({
                    "role": role,
                    "content": content
                })
        
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=temperature,
            system=system_message if system_message else "You are a helpful AI assistant.",
            messages=claude_messages
        )
        
        return response.content[0].text.strip()
    except ImportError:
        return "Error: anthropic package not installed. Run: pip install anthropic"
    except Exception as e:
        return f"Error with Anthropic API: {str(e)}"

def chat_openai(messages: List[Dict], model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
    """Chat using OpenAI API"""
    try:
        import openai
        from config import apikey
        
        if not apikey or apikey == "your_api_key_here" or len(apikey) < 20:
            return "Error: Invalid OpenAI API key. Please set a valid OPENAI_API_KEY in your .env file."
        
        client = openai.OpenAI(api_key=apikey)
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error with OpenAI API: {str(e)}"

def chat_with_provider(provider: str, messages: List[Dict], model: str = None, temperature: float = 0.7) -> str:
    """Main function to chat with any provider"""
    if provider == "groq":
        default_model = "llama-3.1-8b-instant"  # Fast and reliable default
        return chat_groq(messages, model or default_model, temperature)
    elif provider == "huggingface":
        default_model = "mistralai/Mistral-7B-Instruct-v0.2"
        return chat_huggingface(messages, model or default_model, temperature)
    elif provider == "together":
        default_model = "meta-llama/Llama-2-70b-chat-hf"
        return chat_together(messages, model or default_model, temperature)
    elif provider == "anthropic":
        default_model = "claude-3-haiku-20240307"
        return chat_anthropic(messages, model or default_model, temperature)
    elif provider == "openai":
        default_model = "gpt-3.5-turbo"
        return chat_openai(messages, model or default_model, temperature)
    else:
        return f"Error: Unknown provider '{provider}'"

def get_available_providers() -> List[str]:
    """Get list of available providers based on API keys"""
    available = []
    for provider, config in PROVIDERS.items():
        if not config["requires_key"]:
            available.append(provider)
        elif get_provider_key(provider):
            available.append(provider)
    return available

def get_provider_models(provider: str) -> List[str]:
    """Get available models for a provider"""
    if provider in PROVIDERS and "models" in PROVIDERS[provider]:
        return PROVIDERS[provider]["models"]
    return []

