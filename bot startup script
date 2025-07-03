# Create a startup script
startup_script = """#!/bin/bash

# Freelancers Bot Startup Script
echo "🤖 Starting Freelancers Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running!"
    echo "🔑 Your M-Pesa credentials are already configured in config.py"
fi

# Run the application
echo "🚀 Starting Freelancers Bot..."
echo "📱 M-Pesa integration ready!"
echo "🧠 AI features ready!"
echo "🌐 Visit http://localhost:5000"
echo ""

python app.py
"""

with open("freelancers_bot/start.sh", "w") as f:
    f.write(startup_script)

# Make the script executable
import os
os.chmod("freelancers_bot/start.sh", 0o755)

print("Startup script created!")
