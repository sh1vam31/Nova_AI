#!/bin/bash

# Jarvis AI Assistant - Run Script
echo "🤖 Starting Jarvis AI Assistant..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created. Please add your API keys to .env file"
        echo "🔑 You need to add your OPENAI_API_KEY at minimum"
        echo ""
        read -p "Press Enter to continue after adding your API key, or Ctrl+C to exit..."
    else
        echo "❌ .env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "🚀 Starting Streamlit app..."
echo ""
streamlit run app.py

