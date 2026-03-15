# Terminal Session Recorder (TSR) v2.0.0 - Complete Installation Guide

> **TSR v2.0.0** includes auto-terminal recording, LinkedIn integration, enhanced security monitoring, and comprehensive export capabilities.

## Table of Contents
- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Linux Installation](#linux-installation)
- [macOS Installation](#macos-installation)
- [Windows Installation](#windows-installation)
- [Feature Demonstrations](#feature-demonstrations)
- [Testing & Validation](#testing--validation)
- [Troubleshooting](#troubleshooting)
- [Compatibility Matrix](#compatibility-matrix)
- [Uninstallation](#uninstallation)

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum, 2GB recommended
- **Disk Space**: 100MB for installation, additional space for session recordings
- **OS**: Linux, macOS, or Windows 10+

### Recommended Requirements
- **Python**: 3.9+
- **RAM**: 4GB+
- **Disk Space**: 1GB+ for extensive session storage
- **Network**: Required for LinkedIn integration and cloud exports

## Quick Start

### One-Line Install (All Platforms)
```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/jonyhossan110/terminal-session-recorder/main/install.sh | bash

# Windows (PowerShell as Administrator)
irm https://raw.githubusercontent.com/jonyhossan110/terminal-session-recorder/main/install.ps1 | iex
```

### Basic Usage After Installation
```bash
# Start recording a session
tsr record --user-name "Your Name"

# View recorded sessions
tsr list

# Export session to PDF
tsr export 1 --format pdf

# Share on LinkedIn
tsr linkedin share 1 --message "Check out this terminal session!"
```

## Linux Installation

### Ubuntu/Debian (Complete Setup)

#### Step 1: Update System and Install Prerequisites
```bash
# Update package lists
sudo apt update

# Install Python and development tools
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential

# Install image processing libraries
sudo apt install -y libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev libtiff-dev

# Install OCR dependencies
sudo apt install -y tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev

# Install network monitoring tools
sudo apt install -y libpcap-dev tcpdump

# Install additional tools
sudo apt install -y git curl wget

# Expected output:
# Reading package lists... Done
# Building dependency tree
# Reading state information... Done
# ...packages will be installed...
# Do you want to continue? [Y/n] y
```

#### Step 2: Clone Repository and Setup
```bash
# Clone the repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Expected output:
# Cloning into 'terminal-session-recorder'...
# remote: Enumerating objects: XXX, done.
# remote: Counting objects: 100% (XXX/XXX), done.
# ...

# Make setup script executable
chmod +x setup_linux.sh

# Run automated setup
./setup_linux.sh

# Expected output:
# Setting up Terminal Session Recorder v2.0.0...
# Creating virtual environment...
# Installing dependencies...
# Installation completed successfully!
```

#### Step 3: Configure Network Monitoring (Optional)
```bash
# Allow Python to capture packets without root privileges
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# Expected output:
# (no output if successful)
```

#### Step 4: Setup Auto-Recording (Optional)
Add to your `~/.bashrc`:
```bash
# TSR Auto-recording for every new terminal
if [ -z "$TSR_AUTO_REC" ]; then
  export TSR_AUTO_REC=1
  tsr record --user-name "$USER" --output-dir "$HOME/.tsr/sessions"
  exit
fi
```

#### Step 5: Verify Installation
```bash
# Activate virtual environment
source .venv/bin/activate

# Check version
tsr --version

# Expected output:
# Terminal Session Recorder v2.0.0

# Check help
tsr --help

# Expected output:
# usage: tsr [-h] [--version] {record,list,export,linkedin,server,init} ...
#
# Terminal Session Recorder v2.0.0
#
# positional arguments:
#   {record,list,export,linkedin,server,init}
#     record              Start recording a terminal session
#     list                List recorded sessions
#     export              Export session data
#     linkedin            LinkedIn integration commands
#     server              Start web dashboard server
#     init                Initialize TSR configuration
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --version             show program's version number and exit
```

### CentOS/RHEL/Fedora Setup

#### CentOS/RHEL 7/8
```bash
# Install EPEL repository
sudo yum install -y epel-release

# Install Python and tools
sudo yum install -y python3 python3-pip python3-devel gcc gcc-c++ make

# Install image libraries
sudo yum install -y libjpeg-devel zlib-devel libpng-devel freetype-devel libtiff-devel

# Install Tesseract
sudo yum install -y tesseract tesseract-devel leptonica-devel

# Install network tools
sudo yum install -y libpcap-devel tcpdump

# Clone and setup (same as Ubuntu steps 2-5 above)
```

#### Fedora
```bash
# Install packages
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++ make
sudo dnf install -y libjpeg-devel zlib-devel libpng-devel freetype-devel libtiff-devel
sudo dnf install -y tesseract tesseract-devel leptonica-devel
sudo dnf install -y libpcap-devel tcpdump

# Continue with steps 2-5 from Ubuntu guide
```

### Arch Linux Setup
```bash
# Install packages
sudo pacman -S python python-pip python-virtualenv
sudo pacman -S libjpeg-turbo zlib libpng freetype2 libtiff
sudo pacman -S tesseract tesseract-data-eng leptonica
sudo pacman -S libpcap tcpdump git

# Continue with steps 2-5 from Ubuntu guide
```

## macOS Installation

### Using Homebrew (Recommended)

#### Step 1: Install Homebrew (if not already installed)
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH (follow the instructions shown after installation)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### Step 2: Install Dependencies
```bash
# Install Python
brew install python

# Install Tesseract OCR
brew install tesseract tesseract-lang

# Install image libraries
brew install libjpeg libpng freetype libtiff

# Install other tools
brew install libpcap tcpdump git

# Expected output for each:
# ==> Downloading https://...
# ==> Installing python
# ==> Summary: /opt/homebrew/Cellar/python/3.x.x: XXX files, XXXMB
```

#### Step 3: Clone and Setup TSR
```bash
# Clone repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install TSR with all features
pip install -e ".[all]"

# Expected output:
# Obtaining file:///path/to/terminal-session-recorder
# Installing collected packages: ...
# Successfully installed terminal-session-recorder-2.0.0 ...
```

#### Step 4: Initialize Configuration
```bash
# Initialize TSR
tsr init

# Expected output:
# TSR configuration initialized at /Users/username/.tsr/config.yaml
# Please edit the configuration file to customize settings.
```

#### Step 5: Setup Auto-Recording (Optional)
Add to your `~/.zshrc` or `~/.bashrc`:
```zsh
# TSR Auto-recording for every new terminal
if [ -z "$TSR_AUTO_REC" ]; then
  export TSR_AUTO_REC=1
  exec tsr record --user-name "$USER" --output-dir "$HOME/.tsr/sessions"
fi
```

#### Step 6: Verify Installation
```bash
# Check version
tsr --version

# Expected output:
# Terminal Session Recorder v2.0.0

# Test basic functionality
tsr --help
```

### Manual macOS Setup (Without Homebrew)
```bash
# Install Python 3.8+ from python.org
# Download and install Tesseract: https://github.com/tesseract-ocr/tesseract/wiki

# Install image libraries
pip install --upgrade Pillow

# Continue with steps 3-6 from Homebrew guide
```

## Windows Installation

### Using PowerShell (Recommended)

#### Step 1: Install Prerequisites
```powershell
# Check Python version (requires 3.8+)
python --version

# If not installed, download from https://python.org
# Make sure to check "Add Python to PATH" during installation

# Install Git (if not already installed)
# Download from https://git-scm.com/download/win

# Install Tesseract OCR
# Download from https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH: C:\Program Files\Tesseract-OCR
```

#### Step 2: Install System Dependencies
```powershell
# Install Visual Studio Build Tools (for compiling packages)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Install vcpkg for additional libraries
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
.\vcpkg install libjpeg-turbo zlib libpng freetype
```

#### Step 3: Clone and Setup TSR
```cmd
# Clone repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate.bat

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install TSR
pip install -e ".[all]"

# Expected output:
# Successfully installed terminal-session-recorder-2.0.0 ...
```

#### Step 4: Initialize Configuration
```cmd
# Initialize TSR
tsr init

# Expected output:
# TSR configuration initialized at C:\Users\username\.tsr\config.yaml
```

#### Step 5: Setup Auto-Recording (Optional)
Create a batch file `tsr_auto.bat`:
```batch
@echo off
if "%TSR_AUTO_REC%"=="" (
  set TSR_AUTO_REC=1
  tsr record --user-name "%USERNAME%" --output-dir "%USERPROFILE%\.tsr\sessions"
  exit
)
```

Add to Windows Terminal settings or create a custom profile that runs this batch file.

#### Step 6: Configure Windows Firewall (for Network Monitoring)
```powershell
# Allow TSR through firewall for network monitoring
New-NetFirewallRule -DisplayName "TSR Network Monitoring" -Direction Inbound -Program "python.exe" -Action Allow
```

#### Step 7: Verify Installation
```cmd
# Check version
tsr --version

# Expected output:
# Terminal Session Recorder v2.0.0

# Test help
tsr --help
```

### Chocolatey Installation (Alternative)
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install dependencies
choco install python git tesseract

# Continue with steps 3-7 from PowerShell guide
```

## Feature Demonstrations

### Basic Recording Session

#### Start Recording
```bash
# Start a recording session
tsr record --user-name "Demo User" --output-dir ./demo_session

# Expected output:
# TSR v2.0.0 - Terminal Session Recorder
# Recording started at: 2024-01-15 10:30:00
# Session ID: 12345
# Output directory: /path/to/demo_session
# Press Ctrl+C to stop recording
```

#### Run Some Commands (in the recording session)
```bash
# Run test commands
echo "Hello, TSR!"
ls -la
ps aux | head -10
curl -s https://httpbin.org/ip
python3 -c "import sys; print(f'Python version: {sys.version}')"
```

#### Stop Recording (Ctrl+C)
```bash
# Expected output when stopping:
# Recording stopped at: 2024-01-15 10:35:00
# Session saved to: /path/to/demo_session/session_12345.json
# Duration: 5 minutes 0 seconds
# Commands recorded: 4
```

### Advanced Recording with All Features

#### Start Full-Featured Recording
```bash
tsr record \
  --user-name "Advanced Demo" \
  --output-dir ./advanced_demo \
  --enable-screenshots \
  --enable-network-monitor \
  --export-formats json,pdf,html \
  --tags "demo,advanced,testing"

# Expected output:
# TSR v2.0.0 - Terminal Session Recorder
# Features enabled: screenshots, network monitoring
# Export formats: json, pdf, html
# Recording started at: 2024-01-15 11:00:00
# Session ID: 12346
```

#### Test Network Monitoring
```bash
# Generate some network activity
ping -c 4 google.com
curl -I https://github.com
wget --spider https://httpbin.org/get
```

#### Test Screenshot Capture
```bash
# Commands that would trigger screenshots
echo "This is a test command"
ls -la /etc | head -20
top -n 1
```

### LinkedIn Integration Demo

#### Setup LinkedIn API (First Time)
```bash
# Initialize LinkedIn integration
tsr linkedin setup

# Expected output:
# LinkedIn API Setup
# Visit: https://www.linkedin.com/oauth/v2/authorization?...
# Enter authorization code: _____
```

#### Share a Session on LinkedIn
```bash
# Share session with custom message
tsr linkedin share 12345 --message "Check out this terminal session recording! #TSR #DevTools"

# Expected output:
# Authenticating with LinkedIn...
# Posting to LinkedIn...
# Successfully shared session 12345 on LinkedIn
# Post URL: https://www.linkedin.com/feed/update/urn:li:activity:...
```

#### List LinkedIn Posts
```bash
tsr linkedin list

# Expected output:
# LinkedIn Posts:
# 1. "Terminal session recording demo" - Posted 2024-01-15 12:00:00
# 2. "Advanced TSR features showcase" - Posted 2024-01-15 11:30:00
```

### Export Demonstrations

#### Export to PDF
```bash
tsr export 12345 --format pdf --output ./exports/session_12345.pdf

# Expected output:
# Exporting session 12345 to PDF...
# Including screenshots: Yes
# Including network data: Yes
# Export completed: ./exports/session_12345.pdf
```

#### Export to HTML
```bash
tsr export 12345 --format html --output ./exports/session_12345.html

# Expected output:
# Exporting session 12345 to HTML...
# Generating interactive timeline...
# Export completed: ./exports/session_12345.html
```

#### Export to JSON
```bash
tsr export 12345 --format json --output ./exports/session_12345.json

# Expected output:
# Exporting session 12345 to JSON...
# Export completed: ./exports/session_12345.json
```

### Web Dashboard Demo

#### Start Web Server
```bash
tsr server --port 5000

# Expected output:
# TSR Web Dashboard v2.0.0
# Starting server on http://localhost:5000
# Press Ctrl+C to stop
```

#### Access Dashboard Features
- Open browser to `http://localhost:5000`
- View real-time sessions
- Browse recorded sessions
- Export sessions via web interface
- Monitor system resources

## Testing & Validation

### Automated Testing
```bash
# Run full test suite
python -m pytest tests/ -v

# Expected output:
# ============================= test session starts ==============================
# platform linux -- Python 3.9.7, pyright 1.1.200
# collected 25 items
#
# tests/test_basic.py ..........                                      [ 40%]
# tests/test_recorder.py ..........                                   [ 80%]
# tests/test_linkedin.py .....                                        [100%]
#
# ======================== 25 passed in 12.34s =========================
```

### Manual Testing Checklist

#### Basic Functionality Test
```bash
# Test 1: Version check
tsr --version
# Expected: Terminal Session Recorder v2.0.0

# Test 2: Help display
tsr --help
# Expected: Shows all available commands

# Test 3: Configuration initialization
tsr init
# Expected: Configuration created successfully
```

#### Recording Test
```bash
# Test 4: Start recording
tsr record --user-name "Test User" --output-dir ./test_output &
# Expected: Recording starts, process runs in background

# Test 5: Run commands in new terminal
echo "test command 1"
ls -la
date
# Expected: Commands are captured

# Test 6: Stop recording
pkill -f "tsr record"
# Expected: Recording stops, session file created
```

#### Feature Tests
```bash
# Test 7: Screenshot capability
tsr record --enable-screenshots --user-name "Screenshot Test"
# Run some commands, then check for screenshot files

# Test 8: Network monitoring
sudo tsr record --enable-network-monitor --user-name "Network Test"
# Generate network traffic, check for packet captures

# Test 9: Export functionality
tsr export 1 --format pdf
# Expected: PDF file created successfully
```

#### Integration Tests
```bash
# Test 10: LinkedIn setup (mock)
tsr linkedin setup --dry-run
# Expected: OAuth flow simulation successful

# Test 11: Web dashboard
tsr server &
sleep 5
curl -s http://localhost:5000 | head -10
# Expected: HTML dashboard content returned
pkill -f "tsr server"
```

### Performance Testing
```bash
# Test 12: Load testing
time tsr record --user-name "Performance Test" --output-dir ./perf_test &
# Run intensive commands for 5 minutes
sleep 300
pkill -f "tsr record"

# Test 13: Memory usage check
ps aux | grep tsr | grep -v grep
# Expected: Memory usage under 200MB for basic recording
```

## Troubleshooting

### Common Linux Issues

#### "python3: command not found"
```bash
# Solution for Ubuntu/Debian
sudo apt install python3 python3-pip

# Solution for CentOS/RHEL
sudo yum install python3 python3-pip

# Verify
python3 --version
```

#### "ModuleNotFoundError: No module named 'PIL'"
```bash
# Install system libraries
sudo apt install libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev

# Reinstall Pillow
pip install --upgrade --force-reinstall Pillow
```

#### "ImportError: libtesseract.so.4"
```bash
# Install Tesseract properly
sudo apt install tesseract-ocr libtesseract-dev

# Reinstall pytesseract
pip install --upgrade --force-reinstall pytesseract
```

#### Network Monitoring Permission Denied
```bash
# Option 1: Run with sudo
sudo tsr record --enable-network-monitor

# Option 2: Grant capabilities
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# Option 3: Add user to wireshark group
sudo usermod -a -G wireshark $USER
# Logout and login again
```

### Common macOS Issues

#### "Permission denied" for /usr/local
```bash
# Use Homebrew prefix
brew install python tesseract

# Or install to user directory
pip install --user -e ".[all]"
```

#### Tesseract not found
```bash
# Install via Homebrew
brew install tesseract tesseract-lang

# Add to PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Common Windows Issues

#### "python is not recognized"
```bash
# Add Python to PATH during installation
# Or manually add to environment variables:
# Path = C:\Users\username\AppData\Local\Programs\Python\Python39\
```

#### "Microsoft Visual C++ 14.0 is required"
```bash
# Install Build Tools for Visual Studio
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or use pre-compiled wheels
pip install --only-binary=all -e ".[all]"
```

#### Network monitoring fails
```powershell
# Run PowerShell as Administrator
# Allow TSR through Windows Firewall
New-NetFirewallRule -DisplayName "TSR" -Direction Inbound -Program "python.exe" -Action Allow
```

### General Issues

#### "tsr: command not found"
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate.bat  # Windows

# Or install globally
pip install --user -e .
export PATH="$HOME/.local/bin:$PATH"
```

#### Configuration errors
```bash
# Reset configuration
rm -rf ~/.tsr
tsr init

# Check configuration file
cat ~/.tsr/config.yaml
```

#### Database errors
```bash
# Reset database
rm ~/.tsr/sessions.db
tsr init
```

#### Memory issues
```bash
# Disable screenshots for memory-constrained systems
tsr record --disable-screenshots

# Reduce screenshot interval
tsr record --screenshot-interval 30
```

## Compatibility Matrix

| Feature | Linux | macOS | Windows | Notes |
|---------|-------|-------|---------|-------|
| Basic Recording | ✅ | ✅ | ✅ | All platforms |
| Screenshots | ✅ | ✅ | ✅ | Requires PIL/Pillow |
| OCR | ✅ | ✅ | ✅ | Requires Tesseract |
| Network Monitoring | ✅ | ✅ | ✅ | Requires libpcap/WinPcap |
| PDF Export | ✅ | ✅ | ✅ | Requires reportlab |
| HTML Export | ✅ | ✅ | ✅ | All platforms |
| JSON Export | ✅ | ✅ | ✅ | All platforms |
| CSV Export | ✅ | ✅ | ✅ | All platforms |
| Web Dashboard | ✅ | ✅ | ✅ | Flask-based |
| LinkedIn Integration | ✅ | ✅ | ✅ | Requires API credentials |
| Auto-recording | ✅ | ✅ | ⚠️ | Limited on Windows |
| PTY Support | ✅ | ✅ | ❌ | Unix only |
| System Calls Monitoring | ✅ | ❌ | ❌ | Linux only |
| Plugin System | ✅ | ✅ | ✅ | Python-based |

### Python Version Compatibility
- **Python 3.8**: Minimal support, some features limited
- **Python 3.9+**: Full feature support recommended
- **Python 3.11+**: Best performance and latest features

### Operating System Versions
- **Linux**: Ubuntu 18.04+, CentOS 7+, Fedora 30+, Arch Linux
- **macOS**: 10.15+ (Catalina and later)
- **Windows**: 10 version 1903+, Windows 11

## Uninstallation

### Linux/macOS
```bash
# Remove virtual environment
rm -rf .venv

# Remove global installation
pip uninstall terminal-session-recorder

# Remove configuration and data
rm -rf ~/.tsr

# Remove system packages (optional)
sudo apt remove tesseract-ocr libtesseract-dev  # Ubuntu/Debian
brew uninstall tesseract  # macOS with Homebrew
```

### Windows
```cmd
# Remove virtual environment
rmdir /s /q .venv

# Remove global installation
pip uninstall terminal-session-recorder

# Remove configuration and data
rmdir /s /q %USERPROFILE%\.tsr
```

### Complete System Cleanup
```bash
# Remove all TSR-related files
find ~ -name "*tsr*" -type f -delete 2>/dev/null
find ~ -name ".tsr" -type d -exec rm -rf {} + 2>/dev/null

# Remove from PATH (if added manually)
# Edit ~/.bashrc, ~/.zshrc, or system environment variables
```

## Support and Contributing

### Getting Help
- **Documentation**: [README.md](README.md), [FEATURES.md](docs/FEATURES.md)
- **Issues**: [GitHub Issues](https://github.com/jonyhossan110/terminal-session-recorder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jonyhossan110/terminal-session-recorder/discussions)

### Reporting Bugs
When reporting issues, please include:
- TSR version (`tsr --version`)
- Python version (`python --version`)
- Operating system and version
- Full error message and traceback
- Steps to reproduce the issue

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

### Development Setup
```bash
# Clone repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/

# Run linting
flake8 tsr/ tests/
black tsr/ tests/
```

---

**Terminal Session Recorder v2.0.0** - Complete installation and usage guide. For the latest updates, visit [GitHub Repository](https://github.com/jonyhossan110/terminal-session-recorder).
