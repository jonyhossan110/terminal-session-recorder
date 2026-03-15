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

### Linux

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
