# Terminal Session Recorder (TSR) v2.0.0

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/jonyhossan110/terminal-session-recorder)

**Enterprise-grade terminal session recorder for penetration testing, security audits, and professional documentation**

Developed by **Md. Jony Hassain** | **HexaCyberLab Web Agency**

---

## ✨ Features

- 🎥 **Session Recording** - Full terminal session capture with metadata
- ⚡ **Auto-Terminal Recording** - Every new terminal session is automatically recorded
- 🧠 **Smart Classification** - Auto-detects pentesting tools (nmap, metasploit, etc.)
- 📸 **Screenshot Capture** - Full-screen captures with OCR support
- 🌐 **Network Monitoring** - Packet capture integration (scapy)
- 📊 **Resource Tracking** - CPU, memory, disk, and network I/O monitoring
- 🔐 **Evidence Chain** - Cryptographic hashing for audit trails
- 📋 **Multi-Format Export** - PDF, HTML, JSON, CSV reports
- 🔗 **LinkedIn Sharing** - Professional social media integration
- 🌐 **Web Dashboard** - Real-time monitoring and management
- 🔌 **Plugin Architecture** - Extensible with custom plugins
- 🗄️ **SQLite Database** - Fast querying and session management
- 🔄 **Session Replay** - Interactive playback of recorded sessions
- 🖥️ **PTY/TTY Support** - Full terminal emulation on Linux/macOS

---

## 📦 Installation

### Linux Installation

#### Ubuntu/Debian (Complete Setup)

**Step 1: Update System and Install Prerequisites**
```bash
# Update package lists
sudo apt update

# Install Python and development tools
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential

# Install image processing libraries
sudo apt install -y libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev

# Install OCR dependencies
sudo apt install -y tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev

# Install network monitoring tools
sudo apt install -y libpcap-dev tcpdump

# Install additional tools
sudo apt install -y git curl wget
```

**Step 2: Clone Repository and Setup**
```bash
# Clone the repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Make setup script executable
chmod +x setup_linux.sh

# Run automated setup
./setup_linux.sh
```

**Step 3: Configure Network Monitoring (Optional)**
```bash
# Allow Python to capture packets without root privileges
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

**Step 4: Setup Auto-Recording (Optional)**
Add to your `~/.bashrc`:
```bash
# TSR Auto-recording for every new terminal
if [ -z "$TSR_AUTO_REC" ]; then
  export TSR_AUTO_REC=1
  tsr record --user-name "$USER" --output-dir "$HOME/.tsr/sessions"
  exit
fi
```

**Step 5: Verify Installation**
```bash
# Activate virtual environment
source .venv/bin/activate

# Check version
tsr --version

# Check help
tsr --help
```

#### CentOS/RHEL/Fedora Setup

**CentOS/RHEL 7/8:**
```bash
# Install EPEL repository
sudo yum install -y epel-release

# Install Python and tools
sudo yum install -y python3 python3-pip python3-devel gcc gcc-c++ make

# Install image libraries
sudo yum install -y libjpeg-devel zlib-devel libpng-devel freetype-devel

# Install Tesseract
sudo yum install -y tesseract tesseract-devel leptonica-devel

# Install network tools
sudo yum install -y libpcap-devel tcpdump

# Clone and setup (same as Ubuntu steps 2-5 above)
```

**Fedora:**
```bash
# Install packages
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++ make
sudo dnf install -y libjpeg-devel zlib-devel libpng-devel freetype-devel
sudo dnf install -y tesseract tesseract-devel leptonica-devel
sudo dnf install -y libpcap-devel tcpdump

# Continue with steps 2-5 from Ubuntu guide
```

#### Arch Linux Setup
```bash
# Install packages
sudo pacman -S python python-pip python-virtualenv
sudo pacman -S libjpeg-turbo zlib libpng freetype2
sudo pacman -S tesseract tesseract-data-eng leptonica
sudo pacman -S libpcap tcpdump git

# Continue with steps 2-5 from Ubuntu guide
```

### macOS Installation

#### Using Homebrew (Recommended)

**Step 1: Install Homebrew (if not already installed)**
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH (follow the instructions shown after installation)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Step 2: Install Dependencies**
```bash
# Install Python
brew install python

# Install Tesseract OCR
brew install tesseract tesseract-lang

# Install image libraries
brew install libjpeg libpng freetype libtiff

# Install other tools
brew install libpcap tcpdump git
```

**Step 3: Clone and Setup TSR**
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
```

**Step 4: Initialize Configuration**
```bash
# Initialize TSR
tsr init
```

**Step 5: Setup Auto-Recording (Optional)**
Add to your `~/.zshrc` or `~/.bashrc`:
```zsh
# TSR Auto-recording for every new terminal
if [ -z "$TSR_AUTO_REC" ]; then
  export TSR_AUTO_REC=1
  exec tsr record --user-name "$USER" --output-dir "$HOME/.tsr/sessions"
fi
```

**Step 6: Verify Installation**
```bash
# Check version
tsr --version

# Test basic functionality
tsr --help
```

#### Manual macOS Setup (Without Homebrew)
```bash
# Install Python 3.8+ from python.org
# Download and install Tesseract: https://github.com/tesseract-ocr/tesseract/wiki

# Install image libraries
pip install --upgrade Pillow

# Continue with steps 3-6 from Homebrew guide
```

### Windows Installation

#### Using PowerShell (Recommended)

**Step 1: Install Prerequisites**
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

**Step 2: Install System Dependencies**
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

**Step 3: Clone and Setup TSR**
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
```

**Step 4: Initialize Configuration**
```cmd
# Initialize TSR
tsr init
```

**Step 5: Setup Auto-Recording (Optional)**
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

**Step 6: Configure Windows Firewall (for Network Monitoring)**
```powershell
# Allow TSR through firewall for network monitoring
New-NetFirewallRule -DisplayName "TSR Network Monitoring" -Direction Inbound -Program "python.exe" -Action Allow
```

**Step 7: Verify Installation**
```cmd
# Check version
tsr --version

# Test help
tsr --help
```

#### Chocolatey Installation (Alternative)
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install dependencies
choco install python git tesseract

# Continue with steps 3-7 from PowerShell guide
```

---

## 🎯 Quick Usage

### Basic Recording
```bash
# Start recording
tsr record --user-name "Your Name"

# Your commands are now being recorded...
$ nmap -sV 192.168.1.1
$ ls -la
$ exit

# Session automatically saved
```

### View Sessions
```bash
# List all sessions
tsr list

# View specific session
tsr list SESSION_ID
```

### Export Reports
```bash
# Export to PDF
tsr export SESSION_ID --format pdf

# Export to HTML
tsr export SESSION_ID --format html

# Export to JSON
tsr export SESSION_ID --format json
```

### Share on LinkedIn
```bash
# Share session summary
tsr linkedin share SESSION_ID
```

### Start Web Dashboard
```bash
# Start dashboard
tsr server

# Open: http://localhost:5000
```

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file

---

## 👨‍💻 Author

**Md. Jony Hassain**
- Email: jonyhossan110@gmail.com
- Organization: HexaCyberLab Web Agency
- GitHub: [@jonyhossan110](https://github.com/jonyhossan110)

---

**Terminal Session Recorder v2.0.0** - Professional terminal session recording for security professionals.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file

---

## 👨‍💻 Author

**Md. Jony Hassain**
- Email: jonyhossan110@gmail.com
- Organization: HexaCyberLab Web Agency
- GitHub: [@jonyhossan110](https://github.com/jonyhossan110)

---

**Terminal Session Recorder v2.0.0** - Professional terminal session recording for security professionals.
