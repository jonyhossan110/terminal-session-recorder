#!/bin/bash
# Linux/macOS Setup Script for TSR v2.0.0

echo "╔═══════════════════════════════════════════════════╗"
echo "║  Terminal Session Recorder v2.0.0                 ║"
echo "║  Setup Script for Linux/macOS                     ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install system packages
install_system_deps() {
    echo "📦 Installing system dependencies..."

    if command_exists apt; then
        # Ubuntu/Debian
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential
        sudo apt install -y tesseract-ocr tesseract-ocr-eng libtesseract-dev
        sudo apt install -y libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev
        sudo apt install -y libpcap-dev tcpdump
    elif command_exists yum; then
        # CentOS/RHEL
        sudo yum install -y python3 python3-pip python3-devel gcc gcc-c++
        sudo yum install -y tesseract tesseract-devel leptonica-devel
        sudo yum install -y libjpeg-devel zlib-devel libpng-devel freetype-devel
        sudo yum install -y libpcap-devel tcpdump
    elif command_exists dnf; then
        # Fedora
        sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++
        sudo dnf install -y tesseract tesseract-devel leptonica-devel
        sudo dnf install -y libjpeg-devel zlib-devel libpng-devel freetype-devel
        sudo dnf install -y libpcap-devel tcpdump
    elif command_exists pacman; then
        # Arch Linux
        sudo pacman -S --noconfirm python python-pip python-virtualenv
        sudo pacman -S --noconfirm tesseract tesseract-data-eng leptonica
        sudo pacman -S --noconfirm libjpeg-turbo zlib libpng freetype2
        sudo pacman -S --noconfirm libpcap tcpdump
    elif command_exists brew; then
        # macOS with Homebrew
        brew install python tesseract
    else
        echo "⚠️  Warning: Could not detect package manager. Please install system dependencies manually."
        echo "   See INSTALL.md for details."
    fi
}

# Check Python version
if ! command_exists python3; then
    echo "❌ Python 3 not found. Installing..."
    install_system_deps

    if ! command_exists python3; then
        echo "❌ Python 3 installation failed. Please install Python 3.8+ manually."
        exit 1
    fi
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION detected"

# Check if version is 3.8+
if [ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.8" ]; then
    echo "❌ Python 3.8+ required (you have $PYTHON_VERSION)"
    echo "   Please upgrade Python or use a newer version."
    exit 1
fi

# Install system dependencies if not already installed
echo ""
echo "🔧 Checking system dependencies..."
if ! command_exists tesseract; then
    echo "   Installing Tesseract OCR..."
    install_system_deps
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

# Setup network permissions for scapy (optional)
echo ""
echo "🔒 Setting up network permissions..."
if command_exists setcap; then
    sudo setcap cap_net_raw,cap_net_admin=eip $(which python3) 2>/dev/null || true
fi

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
echo "📖 Full Guide:"
echo "  cat INSTALL.md"
echo ""
