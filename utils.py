import os
import openai
import requests
import json
import datetime
import re
from config import apikey
from dotenv import load_dotenv
from ai_providers import chat_with_provider, get_available_providers, get_provider_models, PROVIDERS

load_dotenv()

# Initialize OpenAI client with API key
# OpenAI v1.0+ uses new client structure
try:
    # New OpenAI client (v1.0+) - this is the modern way
    client = openai.OpenAI(api_key=apikey)
    USE_NEW_CLIENT = True
except Exception:
    # Fallback: try old API style (for backward compatibility)
    try:
        openai.api_key = apikey
        USE_NEW_CLIENT = False
    except:
        # Last resort: create client anyway
        client = openai.OpenAI(api_key=apikey)
        USE_NEW_CLIENT = True

def get_weather(city="London"):
    """Get weather information for a city"""
    try:
        # Using OpenWeatherMap API (free tier)
        # Get API key from environment variable
        api_key = os.getenv("WEATHER_API_KEY")
        
        if not api_key or api_key == "your_weather_api_key":
            return f"Weather service: Please configure WEATHER_API_KEY in .env file. Get a free key from openweathermap.org for {city}"
        
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            return f"Weather in {city}: {desc.capitalize()}, Temperature: {temp}°C (feels like {feels_like}°C), Humidity: {humidity}%"
        else:
            return f"Error fetching weather for {city}: {response.status_code}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def calculate(expression):
    """Evaluate a mathematical expression safely"""
    try:
        # Extract mathematical expression from text
        # Find numbers and operators
        expression = expression.lower()
        
        # Replace words with operators
        expression = re.sub(r'\bplus\b', '+', expression)
        expression = re.sub(r'\bminus\b', '-', expression)
        expression = re.sub(r'\btimes\b', '*', expression)
        expression = re.sub(r'\bmultiplied by\b', '*', expression)
        expression = re.sub(r'\bdivided by\b', '/', expression)
        expression = re.sub(r'\bdivide\b', '/', expression)
        
        # Extract numbers and operators only
        math_expr = re.findall(r'[\d\.\+\-\*\/\(\)]+', expression)
        if math_expr:
            expr = ''.join(math_expr)
            # Safety check: only allow numbers, operators, and parentheses
            if re.match(r'^[0-9+\-*/().\s]+$', expr):
                result = eval(expr)
                return f"The answer is {result}"
            else:
                return "Invalid mathematical expression"
        else:
            return "Could not find a mathematical expression in your query"
    except Exception as e:
        return f"Error calculating: {str(e)}"

def get_news(topic="technology", num_articles=5):
    """Get news articles (requires news API key)"""
    try:
        # Using NewsAPI (requires API key from newsapi.org)
        api_key = os.getenv("NEWS_API_KEY")
        
        if not api_key or api_key == "your_news_api_key":
            return f"News service: Please configure NEWS_API_KEY in .env file. Get a free key from newsapi.org for {topic} news"
        
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&pageSize={num_articles}&sortBy=publishedAt"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if articles:
                news_list = []
                for i, article in enumerate(articles[:num_articles], 1):
                    title = article.get('title', 'No title')
                    source = article.get('source', {}).get('name', 'Unknown')
                    news_list.append(f"{i}. {title} ({source})")
                return f"Latest {topic} news:\n" + "\n".join(news_list)
            else:
                return f"No news articles found for {topic}"
        else:
            return f"Error fetching news: {response.status_code}"
    except Exception as e:
        return f"Error fetching news: {str(e)}"

def save_note(note_content, filename="notes.txt"):
    """Save a note to a file"""
    try:
        if not os.path.exists("Notes"):
            os.mkdir("Notes")
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note_path = os.path.join("Notes", filename)
        
        with open(note_path, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}]\n{note_content}\n")
        
        return f"Note saved successfully to {note_path}"
    except Exception as e:
        return f"Error saving note: {str(e)}"

def read_notes(filename="notes.txt"):
    """Read notes from a file"""
    try:
        note_path = os.path.join("Notes", filename)
        if os.path.exists(note_path):
            with open(note_path, "r", encoding="utf-8") as f:
                return f.read()
        return "No notes found."
    except Exception as e:
        return f"Error reading notes: {str(e)}"

def ai_chat(messages, model="gpt-3.5-turbo", temperature=0.7, provider="openai"):
    """Chat with AI using specified provider (OpenAI, Groq, Hugging Face, etc.)"""
    try:
        # Use the specified provider
        if provider and provider != "openai":
            return chat_with_provider(provider, messages, model, temperature)
        
        # Default to OpenAI
        # Validate API key first
        if not apikey or apikey == "your_api_key_here" or len(apikey) < 20:
            # Try to use a free provider as fallback
            available_providers = get_available_providers()
            if available_providers:
                free_provider = [p for p in available_providers if p != "openai"]
                if free_provider:
                    return f"OpenAI API key not found. Switching to {PROVIDERS[free_provider[0]]['name']}...\n\n" + chat_with_provider(free_provider[0], messages, None, temperature)
            return "Error: Invalid API key. Please set a valid OPENAI_API_KEY in your .env file. See GET_API_KEY.md for instructions. Alternatively, you can use free providers like Groq, Hugging Face, or Together AI."
        
        if USE_NEW_CLIENT:
            # Use new OpenAI client (v1.0+) with ChatCompletion
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        else:
            # Try to use ChatCompletion with old API
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=1000
                )
                return response["choices"][0]["message"]["content"].strip()
            except AttributeError:
                # Fallback: build conversation string for Completion API
                conversation = ""
                for msg in messages:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    if role == "system":
                        conversation += f"System: {content}\n\n"
                    elif role == "user":
                        conversation += f"User: {content}\n\n"
                    elif role == "assistant":
                        conversation += f"Assistant: {content}\n\n"
                
                conversation += "Assistant: "
                
                # Use gpt-3.5-turbo-instruct as fallback (still available)
                response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=conversation,
                    temperature=temperature,
                    max_tokens=1000,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                return response["choices"][0]["text"].strip()
    except openai.AuthenticationError as e:
        # Try free providers as fallback
        available_providers = get_available_providers()
        if available_providers:
            free_provider = [p for p in available_providers if p != "openai"]
            if free_provider:
                return f"OpenAI authentication failed. Switching to {PROVIDERS[free_provider[0]]['name']}...\n\n" + chat_with_provider(free_provider[0], messages, None, temperature)
        return "Error: Invalid API key. Please check your OPENAI_API_KEY in the .env file. The API key may be expired or incorrect. See GET_API_KEY.md for instructions on how to get a new API key."
    except openai.RateLimitError as e:
        # Try free providers as fallback
        available_providers = get_available_providers()
        if available_providers:
            free_provider = [p for p in available_providers if p != "openai"]
            if free_provider:
                return f"OpenAI rate limit exceeded. Switching to {PROVIDERS[free_provider[0]]['name']}...\n\n" + chat_with_provider(free_provider[0], messages, None, temperature)
        return "Error: Rate limit exceeded. Please wait a moment and try again, or check your OpenAI account for usage limits."
    except openai.APIError as e:
        error_msg = str(e)
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            # Try free providers as fallback
            available_providers = get_available_providers()
            if available_providers:
                free_provider = [p for p in available_providers if p != "openai"]
                if free_provider:
                    return f"OpenAI authentication failed. Switching to {PROVIDERS[free_provider[0]]['name']}...\n\n" + chat_with_provider(free_provider[0], messages, None, temperature)
            return "Error: Authentication failed (401). Your API key is invalid or expired. Please check your OPENAI_API_KEY in the .env file and ensure it's correct. See GET_API_KEY.md for help."
        elif "429" in error_msg:
            return "Error: Too many requests. Please wait a moment and try again."
        else:
            return f"Error: OpenAI API error - {error_msg}. Please check your API key and account status."
    except Exception as e:
        error_msg = str(e)
        # Provide helpful error messages
        if "deprecated" in error_msg.lower():
            return f"Error: The model has been deprecated. Using gpt-3.5-turbo instead. Original error: {error_msg}"
        elif "401" in error_msg or "unauthorized" in error_msg.lower() or "authentication" in error_msg.lower():
            # Try free providers as fallback
            available_providers = get_available_providers()
            if available_providers:
                free_provider = [p for p in available_providers if p != "openai"]
                if free_provider:
                    return f"OpenAI authentication failed. Switching to {PROVIDERS[free_provider[0]]['name']}...\n\n" + chat_with_provider(free_provider[0], messages, None, temperature)
            return "Error: Authentication failed. Your API key is invalid or expired. Please check your OPENAI_API_KEY in the .env file. See GET_API_KEY.md for instructions."
        elif "api key" in error_msg.lower():
            return f"Error: API key issue. Please check your OpenAI API key in the .env file. {error_msg}"
        elif "insufficient" in error_msg.lower() or "quota" in error_msg.lower():
            return f"Error: Insufficient credits. Please add credits to your OpenAI account. {error_msg}"
        else:
            return f"Error in AI chat: {error_msg}. Please check your API key and ensure you have credits in your OpenAI account."

def ai_completion(prompt, model="gpt-3.5-turbo-instruct", temperature=0.7, max_tokens=500):
    """Get AI completion for a prompt"""
    try:
        if USE_NEW_CLIENT:
            # Use new client with Completion API
            response = client.completions.create(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].text.strip()
        else:
            # Use old API
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response["choices"][0]["text"].strip()
    except Exception as e:
        error_msg = str(e)
        # Provide helpful error messages
        if "deprecated" in error_msg.lower():
            return f"Error: The model {model} has been deprecated. Please use gpt-3.5-turbo or gpt-4 for chat completions."
        return f"Error in AI completion: {error_msg}"

def save_ai_response(prompt, response, directory="Openai"):
    """Save AI response to a file"""
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prompt_{timestamp}.txt"
        filepath = os.path.join(directory, filename)
        
        text = f"Prompt: {prompt}\n"
        text += f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        text += f"{'='*50}\n\n"
        text += f"Response:\n{response}\n"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        
        return filepath
    except Exception as e:
        return f"Error saving response: {str(e)}"

