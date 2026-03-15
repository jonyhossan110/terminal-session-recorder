#!/bin/bash
# Linux/macOS Setup Script for TSR v2.0

echo "╔═══════════════════════════════════════════════════╗"
echo "║  Terminal Session Recorder v2.0.0                 ║"
echo "║  Setup Script for Linux/macOS                     ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION detected"

# Check if version is 3.8+
if [ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.8" ]; then
    echo "❌ Python 3.8+ required (you have $PYTHON_VERSION)"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install TSR
echo ""
echo "📥 Installing Terminal Session Recorder..."
pip install -e ".[all]"

# Initialize config
echo ""
echo "⚙️  Initializing configuration..."
tsr init

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║  Installation Complete! ✓                         ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
echo "🎯 Quick Start:"
echo "  source .venv/bin/activate"
echo "  tsr record --user-name 'Your Name'"
echo ""
echo "📚 Documentation:"
echo "  tsr --help"
echo "  cat README.md"
echo ""
echo "🌐 Web Dashboard:"
echo "  tsr-server"
echo "  Open: http://localhost:5000"
echo ""
