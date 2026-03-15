# 🚀 Quick Start Guide - Terminal Session Recorder v2.0.0

## ⚡ 5-Minute Setup

### 1. Extract & Install (Linux/macOS)

```bash
# Extract the archive
tar -xzf terminal-session-recorder-v2.0.0.tar.gz
cd terminal-session-recorder-v2

# Run automated setup
chmod +x setup_linux.sh
./setup_linux.sh

# Activate virtual environment
source .venv/bin/activate
```

### 2. Extract & Install (Windows)

```cmd
REM Extract using your preferred tool (7-Zip, WinRAR)
cd terminal-session-recorder-v2

REM Run automated setup
setup_windows.bat
```

---

## 🎯 First Recording Session

```bash
# Start recording
tsr record --user-name "Md. Jony Hassain"

# Execute some commands
$ whoami
$ nmap -sV localhost
$ echo "Testing TSR v2.0"
$ exit

# Reports auto-generated!
# Check output directory for:
# - session_XXXXXX.json
# - session_XXXXXX.pdf
# - session_XXXXXX.html
# - session_XXXXXX.csv
```

---

## 📋 Essential Commands

### Recording
```bash
# Basic recording
tsr record

# With full features
tsr record --user-name "Jony" --enable-screenshots --enable-network

# Custom timeout
tsr record --timeout 600
```

### Management
```bash
# List all sessions
tsr list

# Show specific session
tsr list SESSION_ID

# Search commands
tsr search --search "nmap"
```

### Export
```bash
# Export to PDF
tsr export SESSION_ID --format pdf

# Export all formats
tsr export SESSION_ID --format all
```

### Replay
```bash
# Replay session
tsr-replay SESSION_ID

# Interactive mode
tsr-replay SESSION_ID --interactive
```

### Web Dashboard
```bash
# Start server
tsr-server

# Open browser: http://localhost:5000
```

---

## ⚙️ Configuration

### Initialize Config
```bash
tsr init
```

### Edit Config
```bash
nano ~/.tsr/config.yaml
```

### Sample Config
```yaml
user_name: "Md. Jony Hassain"
organization: "HexaCyberLab Web Agency"
session:
  enable_screenshots: true
  command_timeout: 300
export:
  formats: [json, pdf, html]
```

---

## 🎨 Special Session Commands

During a recording session, use these special commands:

```bash
:snap                  # Capture screenshot
:snap "description"    # Capture with label
:tag important         # Tag last command
:stats                 # Show statistics
:help                  # Show help
exit                   # End session
```

---

## 🔥 Advanced Features

### Enable All Monitoring
```bash
sudo tsr record \
  --user-name "Jony" \
  --enable-screenshots \
  --enable-network \
  --enable-strace \
  --timeout 600
```

### Custom Output Directory
```bash
tsr record --output-dir ~/pentest-reports
```

### Database Location
```bash
tsr record --db-path ~/tsr-sessions.db
```

---

## 📊 Smart Command Classification

TSR automatically detects and categorizes:

- 🔍 **Reconnaissance**: whois, dig, nslookup, shodan
- 🔎 **Scanning**: nmap, masscan, nikto
- 💥 **Exploitation**: metasploit, sqlmap, hydra
- 🌐 **Web Testing**: burp, zap, wpscan
- 🔓 **Post-Exploitation**: mimikatz, empire

---

## 🐛 Troubleshooting

### Command not found
```bash
# Activate virtual environment
source .venv/bin/activate

# Or add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Permission denied (network monitoring)
```bash
# Run with sudo
sudo tsr record --enable-network

# Or set capabilities
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

### Screenshots not working
```bash
# Install dependencies
pip install mss Pillow
```

---

## 📚 Documentation

- **Full Documentation**: `README.md`
- **Installation Guide**: `INSTALL.md`
- **Features**: `docs/FEATURES.md`
- **Configuration**: `config.example.yaml`
- **Changelog**: `CHANGELOG.md`

---

## 💡 Tips & Tricks

### 1. Auto-start with alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias tsr-pentest='tsr record --user-name "Jony" --enable-screenshots'
```

### 2. Multiple sessions
```bash
# Different databases for different projects
tsr record --db-path ~/client1/sessions.db
tsr record --db-path ~/client2/sessions.db
```

### 3. Export automation
```bash
# Auto-export after recording
SESSION_ID=$(tsr list --limit 1 | grep -oP '[0-9]{8}_[0-9]{6}_[a-f0-9]{8}')
tsr export $SESSION_ID --format all
```

### 4. Search by type
```bash
# Find all exploitation commands
tsr search --command-type "exploitation"
```

---

## 🎓 Example Workflow

### Penetration Test Documentation

```bash
# 1. Start session
tsr record --user-name "Jony" --organization "HexaCyberLab"

# 2. Reconnaissance
$ whois target.com
$ nmap -sV -p- target.com
$ dig target.com

# 3. Scanning
$ nikto -h target.com
$ gobuster dir -u http://target.com -w wordlist.txt

# 4. Exploitation
$ sqlmap -u "http://target.com/page?id=1" --dbs

# 5. Take screenshots
:snap "Found SQL injection"
:snap "Database enumeration"

# 6. End session
$ exit

# 7. Review reports
# - Check PDF for client presentation
# - Use HTML for interactive review
# - Import JSON for further analysis
```

---

## 🔐 Security Best Practices

1. **Encrypt sensitive sessions**
   ```yaml
   security:
     enable_encryption: true
     redact_passwords: true
   ```

2. **Secure database**
   ```bash
   chmod 600 ~/.tsr/sessions.db
   ```

3. **Regular cleanup**
   ```bash
   # Delete old sessions
   tsr delete --older-than 30d
   ```

4. **Backup important sessions**
   ```bash
   cp ~/.tsr/sessions.db ~/backups/sessions-$(date +%Y%m%d).db
   ```

---

## 🌟 Pro Tips

### Fastest Start (Copy-Paste Ready)

```bash
# Linux/macOS - Complete Setup in One Command
git clone https://github.com/jonyhossan110/terminal-session-recorder.git && \
cd terminal-session-recorder && \
chmod +x setup_linux.sh && \
./setup_linux.sh && \
source .venv/bin/activate && \
tsr record --user-name "$(whoami)"
```

### Windows PowerShell - One Command

```powershell
# Extract manually first, then:
cd terminal-session-recorder-v2; .\setup_windows.bat; .venv\Scripts\activate.bat; tsr record --user-name $env:USERNAME
```

---

## 📞 Getting Help

- **CLI Help**: `tsr --help`
- **Command Help**: `tsr record --help`
- **GitHub Issues**: Report bugs
- **Email**: jonyhossan110@gmail.com

---

## ✅ Verification Checklist

After installation, verify:

- [ ] `tsr --version` shows v2.0.0
- [ ] `tsr list` runs without errors
- [ ] `tsr record` starts successfully
- [ ] Reports are generated
- [ ] `tsr-server` launches dashboard

---

## 🚀 You're Ready!

Your Terminal Session Recorder v2.0.0 is now ready for:
- ✅ Professional penetration testing
- ✅ Security audit documentation
- ✅ Compliance reporting
- ✅ Training sessions
- ✅ Bug bounty hunting

**Start recording your first session now! 🎉**

---

## 📖 Next Steps

1. Read the full [README.md](README.md)
2. Customize your [config.yaml](config.example.yaml)
3. Try the [web dashboard](#web-dashboard)
4. Create custom [plugins](#plugins)
5. Explore [advanced features](#advanced-features)

---

**Made with ❤️ by Md. Jony Hassain | HexaCyberLab Web Agency**
