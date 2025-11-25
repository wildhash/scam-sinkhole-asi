#!/bin/bash

# ScamSinkhole Quick Start Script

echo "🛡️  ScamSinkhole ASI - Quick Start"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - AGI_API_KEY (OpenAI API key)"
    echo "   - TELNYX_API_KEY (Telnyx API key)"
    echo "   - TELNYX_PHONE_NUMBER (Your Telnyx phone number)"
    echo ""
    read -p "Press Enter to open .env in your editor..."
    ${EDITOR:-nano} .env
fi

echo ""
echo "🚀 Starting ScamSinkhole ASI..."
echo ""
echo "Once started, open your browser to:"
echo "   http://localhost:8000"
echo ""
echo "API documentation available at:"
echo "   http://localhost:8000/docs"
echo ""

# Start the server
python main.py
