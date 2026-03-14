#!/bin/bash
# Linux/macOS Setup Script for Web Security Tool

echo "🚀 Setting up Web Security Tool on Linux/macOS"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.6"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION is too old. Please upgrade to Python 3.6+."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🎯 Usage:"
echo "  source .venv/bin/activate"
echo "  python main.py --record-session --user-name YOUR_NAME"
echo "  python main.py https://example.com -o report.json"
echo ""
echo "💡 Add to your shell profile for easy access:"
echo "  echo 'alias recordshell=\"python /path/to/main.py --record-session --user-name YOUR_NAME\"' >> ~/.bashrc"
echo "  source ~/.bashrc"