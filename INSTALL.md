# Installation Guide

## Quick Install (Recommended)

### Linux/macOS

```bash
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder
chmod +x setup_linux.sh
./setup_linux.sh
```

### Windows

```cmd
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder
setup_windows.bat
```

## Manual Installation

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/jonyhossan110/terminal-session-recorder.git
   cd terminal-session-recorder
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate.bat  # Windows
   ```

3. **Install TSR**
   ```bash
   # Full installation (all features)
   pip install -e ".[all]"
   
   # Minimal installation
   pip install -e .
   
   # Development installation
   pip install -e ".[dev]"
   ```

4. **Initialize Configuration**
   ```bash
   tsr init
   ```

5. **Verify Installation**
   ```bash
   tsr --version
   tsr --help
   ```

## Optional Dependencies

### For Screenshots
```bash
pip install mss Pillow
```

### For OCR
```bash
pip install pytesseract opencv-python
# Also install tesseract: sudo apt install tesseract-ocr
```

### For Network Monitoring
```bash
pip install scapy
# Requires root/admin privileges
```

### For Cloud Storage
```bash
# AWS S3
pip install boto3

# Google Cloud
pip install google-cloud-storage
```

## Platform-Specific Notes

### Linux (Complete Setup Guide)

#### Step 1: System Requirements
**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential
sudo apt install -y tesseract-ocr tesseract-ocr-eng libtesseract-dev
sudo apt install -y libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev
sudo apt install -y libpcap-dev tcpdump  # For network monitoring
```

**CentOS/RHEL/Fedora:**
```bash
# CentOS/RHEL
sudo yum install -y python3 python3-pip python3-devel gcc gcc-c++
sudo yum install -y tesseract tesseract-devel leptonica-devel
sudo yum install -y libjpeg-devel zlib-devel libpng-devel freetype-devel
sudo yum install -y libpcap-devel tcpdump

# Fedora
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++
sudo dnf install -y tesseract tesseract-devel leptonica-devel
sudo dnf install -y libjpeg-devel zlib-devel libpng-devel freetype-devel
sudo dnf install -y libpcap-devel tcpdump
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip python-virtualenv
sudo pacman -S tesseract tesseract-data-eng leptonica
sudo pacman -S libjpeg-turbo zlib libpng freetype2
sudo pacman -S libpcap tcpdump
```

#### Step 2: Clone and Setup
```bash
# Clone repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Make setup script executable
chmod +x setup_linux.sh

# Run automated setup
./setup_linux.sh
```

#### Step 3: Manual Installation (Alternative)
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and tools
pip install --upgrade pip setuptools wheel

# Install with all features
pip install -e ".[all]"

# Initialize configuration
tsr init
```

#### Step 4: Network Monitoring Setup (Optional)
```bash
# Allow Python to capture packets without root
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# Or run TSR with sudo for network features
sudo -E .venv/bin/python3 -m tsr.cli record --network-monitor
```

#### Step 5: Verify Installation
```bash
# Activate environment
source .venv/bin/activate

# Check version
tsr --version

# Test basic functionality
tsr --help

# Test recording (in a new terminal)
tsr record --user-name "Test User" --output-dir ./test_session
```

### Common Linux Errors & Solutions

#### Error: "python3: command not found"
```bash
# Install Python 3
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo yum install python3 python3-pip  # CentOS/RHEL
sudo dnf install python3 python3-pip  # Fedora
```

#### Error: "ModuleNotFoundError: No module named 'PIL'"
```bash
# Install system libraries for Pillow
sudo apt install libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev
pip install --upgrade Pillow
```

#### Error: "ImportError: libtesseract.so.4: cannot open shared object file"
```bash
# Install Tesseract properly
sudo apt install tesseract-ocr libtesseract-dev
pip install --upgrade pytesseract
```

#### Error: "Permission denied" for network monitoring
```bash
# Option 1: Run with sudo
sudo -E .venv/bin/python3 -m tsr.cli record --network-monitor

# Option 2: Grant capabilities (recommended)
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

#### Error: "Failed building wheel for scapy"
```bash
# Install development tools
sudo apt install python3-dev build-essential libpcap-dev
pip install scapy
```

#### Error: "Virtual environment not activating"
```bash
# Use correct activation command
source .venv/bin/activate  # Not: source .venv/bin/activate.fish or others

# Check if you're in the right directory
pwd  # Should be: /path/to/terminal-session-recorder
```

#### Error: "tsr: command not found"
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Or install globally
pip install --user -e .

# Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

### Testing the Installation

#### Basic Test
```bash
source .venv/bin/activate
tsr --version
tsr --help
```

#### Full Feature Test
```bash
# Create test directory
mkdir test_session
cd test_session

# Start recording with all features
tsr record \
  --user-name "Test User" \
  --output-dir ./output \
  --enable-screenshots \
  --enable-network-monitor \
  --export-formats json,pdf

# In another terminal, run some commands
echo "Testing TSR recording"
ls -la
ps aux | head -5

# Stop recording (Ctrl+C)
```

#### Web Dashboard Test
```bash
# Start web server
tsr-server

# Open browser: http://localhost:5000
```

### Performance Optimization

#### For Better Screenshot Performance
```bash
# Install optimized libraries
sudo apt install libjpeg-turbo-progs
pip install --upgrade Pillow
```

#### For Network Monitoring
```bash
# Increase buffer size
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.rmem_default=26214400
```

### Uninstallation

```bash
# Remove virtual environment
rm -rf .venv

# Remove global installation
pip uninstall terminal-session-recorder

# Remove configuration
rm -rf ~/.tsr

# Remove system packages (optional)
sudo apt remove tesseract-ocr libtesseract-dev
```

**System Packages** (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv tesseract-ocr
```

**Network Monitoring**:
```bash
# Requires root for packet capture
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

### macOS

**Using Homebrew**:
```bash
brew install python tesseract
```

### Windows

**Additional Tools**:
- Install Python from [python.org](https://python.org)
- Add Python to PATH during installation
- Tesseract: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Troubleshooting

### Issue: Command not found
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Or install globally
pip install --user -e .
```

### Issue: Permission denied
```bash
# Give execute permission
chmod +x setup_linux.sh

# Or run with python
python setup.py install
```

### Issue: Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Uninstallation

```bash
# If installed with pip
pip uninstall terminal-session-recorder

# Remove config and data
rm -rf ~/.tsr
```

## Upgrading

```bash
cd terminal-session-recorder
git pull
pip install -e ".[all]" --upgrade
```

## Docker (Coming Soon)

```bash
docker pull hexacyberlab/tsr:latest
docker run -it hexacyberlab/tsr
```

## Next Steps

After installation:

1. Read the [README.md](README.md)
2. Copy `config.example.yaml` to `~/.tsr/config.yaml`
3. Run `tsr record --user-name "Your Name"`
4. Check `tsr --help` for all commands

## Support

- GitHub Issues: [Report bugs](https://github.com/jonyhossan110/terminal-session-recorder/issues)
- Email: jonyhossan110@gmail.com
