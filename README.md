# Terminal Session Recorder (TSR) v2.0.0

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/jonyhossan110/terminal-session-recorder)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Downloads](https://img.shields.io/badge/downloads-1K+-orange.svg)]()

**Enterprise-grade terminal session recorder for penetration testing, security audits, and professional documentation**

Developed by **Md. Jony Hassain** | **HexaCyberLab Web Agency**

---

## 📋 Table of Contents

- [🚀 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [📦 Quick Installation](#-quick-installation)
- [🎯 Quick Start](#-quick-start)
- [💡 Core Features](#-core-features)
- [📋 Command Reference](#-command-reference)
- [⚙️ Configuration](#-configuration)
- [🔗 LinkedIn Integration](#-linkedin-integration)
- [🌐 Web Dashboard](#-web-dashboard)
- [🔧 Advanced Features](#-advanced-features)
- [📊 Use Cases](#-use-cases)
- [🛠️ Development](#-development)
- [🔒 Security](#-security)
- [🐛 Troubleshooting](#-troubleshooting)
- [📜 License](#-license)
- [👨‍💻 Author](#-author)

---

## 🚀 Overview

**Terminal Session Recorder (TSR) v2.0.0** is a comprehensive tool designed for penetration testers, security professionals, and IT administrators to record, analyze, and document terminal sessions with enterprise-grade features.

### What's New in v2.0.0
- ⚡ **Auto-Terminal Recording** - Every new terminal session is automatically recorded
- 🔗 **LinkedIn Integration** - Share session summaries professionally on LinkedIn
- 🖥️ **PTY/TTY Support** - Full terminal emulation for Linux/macOS
- 📊 **Real-time Web Dashboard** - Monitor sessions live with interactive interface
- 🔌 **Plugin System** - Extensible architecture with built-in plugins
- 📈 **Advanced Analytics** - Command classification and session statistics
- 🌐 **Multi-Format Exports** - PDF, HTML, JSON, CSV with professional layouts

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎥 **Session Recording** | Full terminal session capture with metadata |
| 🧠 **Smart Classification** | Auto-detects pentesting tools and command types |
| 📸 **Screenshot Capture** | Full-screen captures with OCR support |
| 🌐 **Network Monitoring** | Packet capture integration (scapy) |
| 📊 **Resource Tracking** | CPU, memory, disk, and network I/O monitoring |
| 🔐 **Evidence Chain** | Cryptographic hashing for audit trails |
| 📋 **Multi-Format Export** | PDF, HTML, JSON, CSV reports |
| 🔗 **LinkedIn Sharing** | Professional social media integration |
| 🌐 **Web Dashboard** | Real-time monitoring and management |
| 🔌 **Plugin Architecture** | Extensible with custom plugins |
| 🗄️ **SQLite Database** | Fast querying and session management |
| 🔄 **Session Replay** | Interactive playback of recorded sessions |

---

## 📦 Quick Installation

### One-Line Install (All Platforms)
```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/jonyhossan110/terminal-session-recorder/main/install.sh | bash

# Windows PowerShell (Run as Administrator)
irm https://raw.githubusercontent.com/jonyhossan110/terminal-session-recorder/main/install.ps1 | iex
```

### Standard Installation
```bash
# Clone repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Install with all features
pip install -e ".[all]"

# Initialize configuration
tsr init
```

### Platform-Specific Setup
For detailed installation instructions including system dependencies, troubleshooting, and feature demonstrations, see:
- **[📖 Complete Installation Guide](INSTALL.md)**

---

## 🎯 Quick Start

### Basic Recording Session
```bash
# Start recording
tsr record --user-name "Your Name"

# Your terminal session is now being recorded...
$ echo "Hello, TSR!"
$ ls -la
$ whoami
$ exit

# Session automatically saved with timestamp
```

### Advanced Recording with All Features
```bash
tsr record \
  --user-name "Security Professional" \
  --organization "Your Company" \
  --enable-screenshots \
  --enable-network-monitor \
  --export-formats pdf,html,json \
  --tags "pentest,reconnaissance"
```

### View Recorded Sessions
```bash
# List all sessions
tsr list

# View specific session details
tsr list SESSION_ID

# Search for commands
tsr search --command "nmap"
```

### Export Professional Reports
```bash
# Export to PDF report
tsr export SESSION_ID --format pdf --output pentest_report.pdf

# Export to interactive HTML
tsr export SESSION_ID --format html --output session_timeline.html

# Export structured data
tsr export SESSION_ID --format json --output session_data.json
```

### Share on LinkedIn
```bash
# Share session summary professionally
tsr linkedin share SESSION_ID --message "Completed comprehensive security assessment with TSR v2.0.0"
```

---

## 💡 Core Features

### 1. **Intelligent Command Classification**
TSR automatically categorizes commands into security domains:

| Category | Tools | Description |
|----------|-------|-------------|
| 🔍 **Reconnaissance** | whois, nslookup, dig, shodan | Information gathering |
| 🔎 **Scanning** | nmap, masscan, nikto, zmap | Network scanning |
| 📋 **Enumeration** | gobuster, dirb, enum4linux, ldapsearch | Service enumeration |
| 💥 **Exploitation** | metasploit, sqlmap, hydra, john | Vulnerability exploitation |
| 🔓 **Post-Exploitation** | mimikatz, empire, bloodhound | Privilege escalation |
| 🌐 **Web Security** | burp, zap, wpscan, nuclei | Web application testing |
| 🛡️ **Defense** | fail2ban, ufw, iptables | Security hardening |

### 2. **Professional Export Formats**

#### PDF Reports
- Executive summary with session statistics
- Command timeline with syntax highlighting
- Embedded screenshots and network captures
- Professional formatting with company branding
- Evidence chain verification

#### HTML Reports
- Interactive, searchable interface
- Real-time filtering and sorting
- Responsive design for all devices
- Embedded media and charts
- Shareable web links

#### Structured Data (JSON/CSV)
- Complete session metadata
- Command execution details
- Performance metrics
- API-ready format for integration

### 3. **Real-Time Monitoring Dashboard**
```bash
# Start the web interface
tsr server --port 5000

# Access at: http://localhost:5000
```

**Dashboard Features:**
- 📊 Live session monitoring
- 🔍 Advanced search and filtering
- 📈 Performance analytics
- 🎯 Command classification insights
- 📱 Responsive design
- 🔄 Real-time updates

### 4. **Auto-Terminal Recording**
Automatically record every new terminal session:

**Linux/macOS:**
```bash
# Add to ~/.bashrc or ~/.zshrc
if [ -z "$TSR_AUTO_REC" ]; then
  export TSR_AUTO_REC=1
  tsr record --user-name "$USER" --output-dir "$HOME/.tsr/sessions"
  exit
fi
```

**Windows:**
```batch
REM Add to Windows Terminal profile
if "%TSR_AUTO_REC%"=="" (
  set TSR_AUTO_REC=1
  tsr record --user-name "%USERNAME%" --output-dir "%USERPROFILE%\.tsr\sessions"
  exit
)
```

### 5. **Plugin Architecture**
Extend TSR with custom plugins:

```python
from tsr.plugins.base import BasePlugin

class CustomPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "custom-security-tools"

    async def on_command_execute(self, command: str, output: str):
        # Analyze command output
        if "vulnerability" in output.lower():
            return {"severity": "high", "type": "security"}
        return {}
```

**Built-in Plugins:**
- **MetasploitPlugin**: Enhanced Metasploit session tracking
- **NmapPlugin**: Automatic nmap result parsing
- **BurpPlugin**: Burp Suite integration
- **WiresharkPlugin**: Packet analysis integration

---

## 📋 Command Reference

### Recording Commands
```bash
tsr record                                # Start basic recording
tsr record --user-name "Name"            # Set user name
tsr record --organization "Company"      # Set organization
tsr record --enable-screenshots          # Enable screenshot capture
tsr record --enable-network-monitor      # Enable network monitoring
tsr record --enable-resource-monitor     # Enable system monitoring
tsr record --timeout 600                 # Set session timeout
tsr record --output-dir ./sessions       # Custom output directory
tsr record --tags "pentest,recon"        # Add session tags
tsr record --export-formats pdf,html     # Auto-export formats
```

### Session Management
```bash
tsr list                                 # List all sessions
tsr list --limit 20                      # Show last 20 sessions
tsr list --user "username"               # Filter by user
tsr list --date "2024-01-15"             # Filter by date
tsr list SESSION_ID                      # Show session details
tsr list --format json                   # JSON output
```

### Search & Analysis
```bash
tsr search --query "nmap"                # Search in commands
tsr search --command-type "exploitation" # Filter by category
tsr search --user "pentester"            # Filter by user
tsr search --date-range "2024-01-01:2024-01-31"  # Date range
tsr search --tags "critical"             # Filter by tags
tsr search --ip "192.168.1.1"            # Filter by IP addresses
```

### Export & Reporting
```bash
tsr export SESSION_ID --format pdf       # Export to PDF
tsr export SESSION_ID --format html      # Export to HTML
tsr export SESSION_ID --format json      # Export to JSON
tsr export SESSION_ID --format csv       # Export to CSV
tsr export SESSION_ID --format all       # Export all formats
tsr export SESSION_ID -o report.pdf      # Custom output path
tsr export --batch --user "pentester"    # Batch export user sessions
```

### LinkedIn Integration
```bash
tsr linkedin setup                       # Setup LinkedIn API access
tsr linkedin share SESSION_ID            # Share session on LinkedIn
tsr linkedin share SESSION_ID --message "Custom message"  # Custom post
tsr linkedin share SESSION_ID --dry-run  # Preview without posting
tsr linkedin list                        # List shared posts
tsr linkedin auth                        # Refresh authentication
```

### Web Dashboard
```bash
tsr server                               # Start dashboard (port 5000)
tsr server --port 8080                   # Custom port
tsr server --host 0.0.0.0                # Bind to all interfaces
tsr server --debug                       # Debug mode
```

### Special Commands (During Recording)
```bash
:snap                                    # Take screenshot
:snap "Login attempt"                    # Screenshot with description
:tag important                           # Tag last command
:stats                                   # Show session statistics
:note "Important finding"                # Add session note
:help                                    # Show help
```

---

## ⚙️ Configuration

### Configuration File Location
TSR searches for configuration in order:
1. `~/.tsr/config.yaml` (recommended)
2. `~/.tsr/config.json`
3. `./tsr.yaml` (project directory)
4. `/etc/tsr/config.yaml` (system-wide)

### Initialize Configuration
```bash
tsr init
```

### Sample Configuration
```yaml
# User Information
user_name: "Md. Jony Hassain"
organization: "HexaCyberLab Web Agency"
email: "jonyhossan110@gmail.com"

# Session Settings
session:
  auto_save: true
  max_commands: 10000
  truncate_output: 5000
  command_timeout: 300
  enable_screenshots: true
  enable_network_monitor: false
  enable_resource_monitor: true
  auto_export_formats: [json, html]

# Database Configuration
database:
  backend: sqlite
  path: "~/.tsr/sessions.db"
  connection_pool_size: 5

# Export Settings
export:
  default_formats: [pdf, html, json]
  pdf_theme: professional
  html_theme: dark
  compress_exports: false
  include_screenshots: true
  include_network_data: false

# Security Settings
security:
  enable_encryption: false
  enable_hashing: true
  redact_passwords: true
  redact_api_keys: true
  redact_tokens: true
  evidence_chain: true

# LinkedIn Integration
linkedin:
  enabled: true
  auto_share: false
  default_message_template: "Completed terminal session recording with TSR v2.0.0"

# Plugin Configuration
plugins:
  enabled_plugins:
    - metasploit
    - nmap
    - burp
  custom_plugins_path: "~/.tsr/plugins"

# Monitoring Settings
monitoring:
  screenshot_interval: 30
  resource_poll_interval: 5
  network_capture_interface: "eth0"
  enable_system_calls: false

# Logging
logging:
  level: INFO
  file: "~/.tsr/tsr.log"
  max_size: 10MB
  backup_count: 5
```

---

## 🔗 LinkedIn Integration

Share your professional terminal sessions on LinkedIn for networking and knowledge sharing.

### Setup Process

1. **Create LinkedIn Application**:
   - Visit [LinkedIn Developers](https://developer.linkedin.com/)
   - Create a new app for TSR
   - Configure OAuth 2.0 settings

2. **Required Permissions**:
   - `r_liteprofile` - Read basic profile information
   - `w_member_social` - Post on behalf of user

3. **Get Access Token**:
   ```bash
   tsr linkedin setup
   ```
   Follow the OAuth flow to authorize TSR.

### Sharing Sessions
```bash
# Share with auto-generated message
tsr linkedin share 12345

# Custom professional message
tsr linkedin share 12345 --message "Completed comprehensive penetration testing session covering reconnaissance, scanning, and exploitation phases using industry-standard tools."

# Preview before posting
tsr linkedin share 12345 --dry-run

# Share multiple sessions
tsr linkedin share 12345 12346 12347 --message "Weekly security assessment summary"
```

### Example LinkedIn Post
```
🔍 Terminal Session Recording - TSR v2.0.0

📊 Session Summary:
• Duration: 45 minutes
• Commands Executed: 127
• Tools Used: nmap, metasploit, burp
• User: Md. Jony Hassain
• Organization: HexaCyberLab Web Agency

#CyberSecurity #PenetrationTesting #TerminalRecording #TSR #SecurityAudits #EthicalHacking

Generated by Terminal Session Recorder v2.0.0
Learn more: https://github.com/jonyhossan110/terminal-session-recorder
```

### Managing LinkedIn Integration
```bash
tsr linkedin list                        # View shared posts
tsr linkedin auth                        # Refresh authentication
tsr linkedin revoke                      # Revoke access
tsr linkedin status                      # Check connection status
```

---

## 🌐 Web Dashboard

The TSR web dashboard provides real-time monitoring and management of your terminal sessions.

### Starting the Dashboard
```bash
# Default configuration
tsr server

# Custom settings
tsr server --port 8080 --host 0.0.0.0 --debug
```

### Dashboard Features

#### 📊 Real-Time Monitoring
- Live session activity
- Active recording sessions
- System resource usage
- Network activity graphs

#### 🔍 Session Management
- Browse all recorded sessions
- Advanced search and filtering
- Session details and metadata
- Command timeline view

#### 📈 Analytics & Insights
- Command type distribution
- Session duration statistics
- Tool usage analytics
- Performance metrics

#### 🎯 Interactive Features
- Real-time command streaming
- Screenshot gallery
- Network capture viewer
- Export session data

#### 🔒 Security Features
- Session-based authentication
- Role-based access control
- Audit logging
- Secure API endpoints

### API Endpoints
```bash
# Get all sessions
GET /api/sessions

# Get specific session
GET /api/sessions/{id}

# Search sessions
GET /api/search?q=nmap

# Export session
GET /api/export/{id}?format=pdf

# Real-time updates
GET /api/stream
```

---

## 🔧 Advanced Features

### Session Replay
Replay recorded sessions with various options:

```bash
# Normal speed replay
tsr replay SESSION_ID

# Speed control
tsr replay SESSION_ID --speed 2.0      # 2x speed
tsr replay SESSION_ID --speed 0.5      # Half speed

# Interactive mode
tsr replay SESSION_ID --interactive    # Step through commands

# Time range replay
tsr replay SESSION_ID --start "10:00" --end "10:30"

# Output to file
tsr replay SESSION_ID --output replay.mp4
```

### Evidence Chain & Integrity
TSR maintains cryptographic integrity of all sessions:

```python
from tsr.utils.crypto import verify_session_integrity

# Verify session hasn't been tampered with
is_valid = verify_session_integrity(session_data)
print(f"Session integrity: {'✓ Valid' if is_valid else '✗ Compromised'}")
```

### Data Redaction
Automatic redaction of sensitive information:

**Redacted Patterns:**
- Passwords: `password=REDACTED`
- API Keys: `api_key=REDACTED`
- Tokens: `token=REDACTED`
- Private Keys: `-----BEGIN PRIVATE KEY----- REDACTED`
- AWS Credentials: `AWS_ACCESS_KEY_ID=REDACTED`

### Network Capture Integration
```bash
# Enable network monitoring (requires root/admin)
sudo tsr record --enable-network-monitor

# PCAP files saved automatically
# Integrated with session timeline
# View in Wireshark or TSR dashboard
```

### Cloud Storage Integration
```yaml
cloud:
  enabled: true
  provider: s3  # s3, gcs, azure, dropbox
  bucket: my-tsr-sessions
  region: us-east-1
  auto_upload: true
  encryption: true
```

### Custom Plugin Development
```python
from tsr.plugins.base import BasePlugin
from typing import Dict, Any, Optional

class AdvancedSecurityPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "advanced-security"

    @property
    def version(self) -> str:
        return "1.0.0"

    async def on_session_start(self, session_id: str, metadata: Dict[str, Any]):
        """Called when recording starts"""
        self.logger.info(f"Advanced security monitoring started for {session_id}")

    async def on_command_execute(self, command: str, output: str, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze each command execution"""
        analysis = {}

        # Vulnerability detection
        if "sql injection" in output.lower():
            analysis["vulnerability"] = "SQL Injection"
            analysis["severity"] = "High"

        # Compliance checking
        if command.startswith("sudo") and "password" in output.lower():
            analysis["compliance"] = "Password in sudo command"

        return analysis

    async def on_session_end(self, session_id: str, summary: Dict[str, Any]):
        """Called when recording ends"""
        self.logger.info(f"Security analysis complete for {session_id}")
        # Generate security report
        await self.generate_security_report(session_id, summary)
```

---

## 📊 Use Cases

### Penetration Testing
```
🎯 Professional pentesting documentation
📋 Comprehensive audit trails
📊 Client-ready reports
🔍 Evidence collection
⏱️ Timeline reconstruction
👥 Team collaboration
```

### Security Audits & Compliance
```
📋 PCI-DSS compliance documentation
📊 ISO 27001 evidence collection
🔍 Vulnerability assessment records
📈 Risk analysis reports
⏱️ Incident response documentation
🏢 Enterprise security audits
```

### Training & Education
```
👨‍🏫 Capture training sessions
📚 Create interactive tutorials
🎯 Demonstrate techniques
📖 Build knowledge base
👥 Share expertise
🎓 Educational content creation
```

### Bug Bounty Programs
```
🎯 Document vulnerability discovery
📋 Proof of concept creation
👥 Team collaboration
📊 Impact assessment
⏱️ Timeline tracking
💰 Bounty claim documentation
```

### DevOps & System Administration
```
🔧 Infrastructure changes tracking
📊 Performance monitoring
🐛 Troubleshooting documentation
📋 Change management
⏱️ Incident response
👥 Team knowledge sharing
```

### Research & Development
```
🔬 Security research documentation
📊 Data collection and analysis
🎯 Methodology validation
📋 Experimental records
👥 Collaborative research
📈 Performance benchmarking
```

---

## 🛠️ Development

### Development Setup
```bash
# Clone repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=tsr --cov-report=html
```

### Code Quality
```bash
# Linting
flake8 tsr/ tests/
black tsr/ tests/
isort tsr/ tests/

# Type checking
mypy tsr/

# Security scanning
bandit -r tsr/
```

### Building & Packaging
```bash
# Build package
python -m build

# Install from local build
pip install dist/terminal_session_recorder-2.0.0-py3-none-any.whl

# Build documentation
sphinx-build docs/ docs/_build/html
```

### Contributing Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Write** tests for new functionality
4. **Implement** your changes
5. **Run** the test suite (`pytest tests/`)
6. **Commit** your changes (`git commit -m 'Add amazing feature'`)
7. **Push** to your branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request

### Plugin Development
- See `tsr/plugins/base.py` for base plugin interface
- Check `tsr/plugins/` for example implementations
- Plugins are automatically discovered and loaded
- Use async/await for performance

### API Documentation
```bash
# Generate API docs
sphinx-autodoc tsr/ docs/api/

# View docs
open docs/_build/html/index.html
```

---

## 🔒 Security

### Best Practices
1. **Encrypt sensitive sessions** - Enable encryption in configuration
2. **Redact credentials** - Automatic redaction is enabled by default
3. **Secure database storage** - Use encrypted filesystems
4. **Limit access permissions** - Set proper file permissions (`chmod 600`)
5. **Regular cleanup** - Remove old/unneeded sessions
6. **Network security** - Use HTTPS for web dashboard in production

### Data Protection
- **Automatic Redaction**: Passwords, API keys, tokens are automatically redacted
- **Encryption Support**: Optional AES-256 encryption for session data
- **Evidence Chain**: Cryptographic hashing ensures data integrity
- **Access Control**: Role-based permissions for multi-user environments

### Network Security
```bash
# Run dashboard with SSL
tsr server --ssl-cert cert.pem --ssl-key key.pem

# Restrict dashboard access
tsr server --allowed-ips 192.168.1.0/24

# Use reverse proxy (nginx/apache) for production
```

### Audit Trail
- All commands are logged with timestamps
- User actions are tracked
- Session integrity is cryptographically verified
- Export operations are logged

---

## 🐛 Troubleshooting

### Installation Issues

**Python Version Error**
```bash
# Check Python version
python --version

# Use Python 3.8+
python3.9 -m pip install -e ".[all]"
```

**Permission Denied**
```bash
# Install without sudo (recommended)
pip install --user -e ".[all]"

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

**Missing Dependencies**
```bash
# Install system packages
# Ubuntu/Debian
sudo apt install python3-dev build-essential

# macOS
brew install python

# Windows - install Visual Studio Build Tools
```

### Recording Issues

**Screenshots Not Working**
```bash
# Install screenshot dependencies
pip install mss Pillow

# Check display access (Linux)
xhost +local:
```

**Network Monitoring Fails**
```bash
# Install scapy
pip install scapy

# Run with elevated privileges
sudo tsr record --enable-network-monitor

# Check capabilities (Linux)
sudo setcap cap_net_raw,cap_net_admin=eip $(which python)
```

**PTY/TTY Issues**
```bash
# Check platform support
python -c "import sys; print(sys.platform)"

# PTY only works on Unix-like systems (Linux/macOS)
# Windows uses alternative terminal capture
```

### Database Issues

**Database Locked**
```bash
# Close other TSR instances
ps aux | grep tsr

# Remove lock files
rm ~/.tsr/sessions.db-wal ~/.tsr/sessions.db-shm
```

**Corrupted Database**
```bash
# Backup existing database
cp ~/.tsr/sessions.db ~/.tsr/sessions.db.backup

# Reinitialize
rm ~/.tsr/sessions.db
tsr init
```

### Export Issues

**PDF Generation Fails**
```bash
# Install reportlab
pip install reportlab

# Check font support
python -c "import reportlab.pdfbase.pdfmetrics"
```

**Memory Issues During Export**
```bash
# Export smaller batches
tsr export SESSION_ID --format pdf --max-commands 1000

# Increase system memory or use swap
```

### LinkedIn Integration Issues

**Authentication Fails**
```bash
# Clear stored tokens
rm ~/.tsr/linkedin_token.json

# Re-run setup
tsr linkedin setup
```

**Posting Fails**
```bash
# Check token validity
tsr linkedin status

# Refresh authentication
tsr linkedin auth
```

### Performance Issues

**High CPU Usage**
```bash
# Disable resource-intensive features
tsr record --disable-screenshots --disable-network-monitor

# Reduce monitoring intervals
tsr record --resource-poll-interval 10
```

**Large Session Files**
```bash
# Enable compression
# In config.yaml
export:
  compress_exports: true

# Limit output truncation
session:
  truncate_output: 1000
```

### Web Dashboard Issues

**Port Already in Use**
```bash
# Use different port
tsr server --port 8080

# Find process using port
lsof -i :5000
kill -9 <PID>
```

**Dashboard Not Accessible**
```bash
# Check firewall
sudo ufw allow 5000

# Bind to all interfaces
tsr server --host 0.0.0.0
```

---

## 📜 License

**MIT License**

Copyright (c) 2024 Md. Jony Hassain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👨‍💻 Author

**Md. Jony Hassain**
- **Email**: jonyhossan110@gmail.com
- **Organization**: HexaCyberLab Web Agency
- **GitHub**: [@jonyhossan110](https://github.com/jonyhossan110)
- **LinkedIn**: [Md. Jony Hassain](https://linkedin.com/in/jonyhossan)
- **Website**: [HexaCyberLab](https://hexacyberlab.com)

### Support
- 📧 **Email**: jonyhossan110@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/jonyhossan110/terminal-session-recorder/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/jonyhossan110/terminal-session-recorder/discussions)
- 📖 **Documentation**: [Complete Installation Guide](INSTALL.md)

---

## 🙏 Acknowledgments

- **Inspiration**: asciinema, script, ttyrec
- **Community**: Penetration testing and security research community
- **Contributors**: Open source community
- **Tools**: Python ecosystem, security research tools

---

## 📈 Roadmap

### v2.1.0 (Planned)
- [ ] Cloud storage integration (AWS S3, Google Cloud)
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard
- [ ] Mobile app companion
- [ ] API rate limiting and caching

### v2.2.0 (Future)
- [ ] AI-powered command analysis
- [ ] Automated report generation
- [ ] Integration with SIEM systems
- [ ] Compliance automation (PCI-DSS, HIPAA)
- [ ] Multi-language support

---

**Terminal Session Recorder v2.0.0** - Professional terminal session recording for security professionals.

⭐ **Star this repository** if you find it useful!
```

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize configuration
tsr init
```

---

## 🎯 Quick Start

### Basic Recording

```bash
# Start recording session
tsr record --user-name "Your Name"

# Execute commands as normal
$ nmap -sV 192.168.1.1
$ sqlmap -u "http://target.com" --dbs
$ exit

# Reports auto-generated: JSON, CSV, PDF, HTML
```

### Advanced Usage

```bash
# Record with all monitoring features
tsr record \
  --user-name "Jony" \
  --organization "HexaCyberLab" \
  --enable-screenshots \
  --enable-network \
  --timeout 300

# List all sessions
tsr list --limit 20

# Search commands
tsr search --command-type "exploitation" --search "sqlmap"

# Export specific session
tsr export SESSION_ID --format pdf --output report.pdf

# Replay session
tsr-replay SESSION_ID --interactive

# Start web dashboard
tsr-server
```

---

## 💡 Features

### Core Features

#### 1. **Smart Command Classification**
Automatically categorizes commands into:
- 🔍 Reconnaissance (whois, nslookup, dig, shodan)
- 🔎 Scanning (nmap, masscan, nikto)
- 📋 Enumeration (gobuster, dirb, enum4linux)
- 💥 Exploitation (metasploit, sqlmap, hydra)
- 🔓 Post-Exploitation (mimikatz, empire)
- ⬆️ Privilege Escalation (sudo exploits, UAC bypass)
- 🌐 Web Security (burp, zap, wpscan)
- And more...

#### 2. **Multiple Export Formats**

**PDF Reports**
- Professional cover page
- Command timeline
- Syntax highlighting
- Embedded screenshots
- Statistics and charts

**HTML Reports**
- Interactive and searchable
- Real-time filtering
- Syntax highlighting
- Responsive design

**JSON/CSV**
- Structured data export
- Easy analysis in Excel/Python
- API integration ready

#### 3. **Database-Backed Storage**

```python
# Query sessions programmatically
from tsr.core.database import SessionDatabase

async with SessionDatabase('sessions.db') as db:
    sessions = await db.search_sessions(user_name="Jony", limit=10)
    commands = await db.search_commands(command_type="exploitation")
    stats = await db.get_statistics(session_id)
```

#### 4. **Real-time Monitoring**

- **Resource Monitor**: CPU, memory, disk, network I/O
- **Network Monitor**: Packet capture (requires scapy + root)
- **System Call Monitor**: strace integration (Linux)

#### 5. **Plugin System**

Create custom plugins:

```python
from tsr.plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "my-plugin"
    
    async def on_command_execute(self, command: str):
        # Your logic here
        return {'custom': 'metadata'}
```

Built-in plugins:
- **MetasploitPlugin**: Enhanced metasploit session tracking
- **NmapPlugin**: Parse nmap results automatically
- More coming soon...

---

## 📋 Command Reference

### Recording Commands

```bash
tsr record                          # Start basic recording
tsr record --user-name "Name"       # Set user name
tsr record --enable-screenshots     # Enable screenshot capture
tsr record --enable-video           # Enable video recording (asciinema)
tsr record --enable-network         # Enable network monitoring
tsr record --enable-strace          # Enable system call tracing
tsr record --timeout 600            # Set command timeout (seconds)
tsr record --output-dir ./reports   # Custom output directory
```

### Session Management

```bash
tsr list                            # List all sessions
tsr list --limit 50                 # Show more sessions
tsr list --user "Jony"              # Filter by user
tsr list SESSION_ID                 # Show specific session details
tsr list --format json              # Output as JSON
```

### Search & Query

```bash
tsr search --search "nmap"                  # Search in commands
tsr search --command-type "reconnaissance"  # Filter by type
tsr search --user "Jony"                    # Filter by user
```

### Export & Reporting

```bash
tsr export SESSION_ID --format pdf          # Export to PDF
tsr export SESSION_ID --format html         # Export to HTML
tsr export SESSION_ID --format json         # Export to JSON
tsr export SESSION_ID --format csv          # Export to CSV
tsr export SESSION_ID --format all          # Export all formats
tsr export SESSION_ID -o custom_report.pdf  # Custom output path
```

### Social Sharing

```bash
tsr linkedin SESSION_ID                           # Share session on LinkedIn
tsr linkedin SESSION_ID --message "Custom post"   # Custom message
tsr linkedin SESSION_ID --dry-run                 # Preview without posting
tsr linkedin SESSION_ID --access-token TOKEN      # Use specific token
```

### Special Session Commands

During recording session, use special commands:

```bash
:snap                    # Capture screenshot
:snap "description"      # Capture with label
:tag important           # Tag last command
:stats                   # Show session statistics
:help                    # Show help
```

---

## ⚙️ Configuration

### Config File Location

TSR looks for config in:
1. `~/.tsr/config.yaml`
2. `~/.tsr/config.json`
3. `/etc/tsr/config.yaml`
4. `./tsr.yaml`

### Sample Configuration

```yaml
user_name: "Md. Jony Hassain"
organization: "HexaCyberLab Web Agency"
output_dir: "~/tsr_sessions"

session:
  auto_save: true
  max_commands: 10000
  truncate_output: 5000
  enable_screenshots: true
  enable_video: false
  command_timeout: 300

database:
  backend: sqlite
  path: "~/.tsr/sessions.db"

monitoring:
  enable_network: false
  enable_strace: false
  enable_resources: true

export:
  formats: [json, pdf, html, csv]
  pdf_theme: professional
  compress_exports: false

security:
  enable_encryption: false
  enable_hashing: true
  redact_passwords: true
  redact_tokens: true

plugins:
  enabled_plugins:
    - metasploit
    - nmap
```

### Initialize Config

```bash
tsr init    # Creates ~/.tsr/config.yaml
```

---

## 🔗 LinkedIn Integration

Share your pentesting session summaries directly on LinkedIn for professional networking and knowledge sharing.

### Setup LinkedIn API Access

1. **Create LinkedIn App**:
   - Go to [LinkedIn Developers](https://developer.linkedin.com/)
   - Create a new app
   - Get your **Client ID** and **Client Secret**

2. **Get Access Token**:
   ```bash
   # Install requests-oauthlib
   pip install requests-oauthlib

   # Run OAuth flow (or use LinkedIn's OAuth playground)
   # Get access token with r_liteprofile and w_member_social permissions
   ```

3. **Set Environment Variable**:
   ```bash
   export LINKEDIN_ACCESS_TOKEN="your_access_token_here"
   ```

### Share Session on LinkedIn

```bash
# Share with auto-generated message
tsr linkedin SESSION_ID

# Custom message
tsr linkedin SESSION_ID --message "Completed advanced nmap scanning session with 15+ commands executed successfully!"

# Preview without posting
tsr linkedin SESSION_ID --dry-run

# Use specific token
tsr linkedin SESSION_ID --access-token "your_token"
```

### Example LinkedIn Post

```
🔍 Terminal Session Recording - 20240315_143022_abc123

📊 Session Summary:
• Duration: 450s
• Commands: 23
• Failed: 0
• User: Md. Jony Hassain

#Pentesting #Security #TerminalRecording #TSR #CyberSecurity

Generated by Terminal Session Recorder v2.0.0
```

### LinkedIn API Permissions Required

- `r_liteprofile` - Read basic profile info
- `w_member_social` - Post on behalf of user

---

## 🌐 Web Dashboard

Start the real-time monitoring dashboard:

```bash
tsr-server

# Access at: http://localhost:5000
```

Features:
- View all sessions
- Real-time command streaming
- Statistics and charts
- Search and filter
- Session details

---

## 🔧 Advanced Features

### 1. Session Replay

```bash
# Replay at normal speed
tsr-replay SESSION_ID

# Replay at 2x speed
tsr-replay SESSION_ID --speed 2.0

# Interactive mode (step through)
tsr-replay SESSION_ID --interactive
```

### 2. Evidence Chain

All commands are cryptographically hashed:

```python
# Verify session integrity
from tsr.utils.crypto import verify_session_hash

is_valid = verify_session_hash(session_data)
```

### 3. Data Redaction

Automatically redacts sensitive data:
- Passwords (`password=REDACTED`)
- API keys (`api_key=REDACTED`)
- AWS credentials
- SSH private keys

### 4. Network Capture

```bash
# Requires root and scapy
sudo tsr record --enable-network

# PCAP files saved to ./captures/
```

### 5. Cloud Storage Integration

```yaml
cloud:
  enabled: true
  provider: s3  # or gcs, dropbox
  bucket: my-tsr-sessions
  auto_upload: true
```

---

## 📊 Use Cases

### Penetration Testing
- Document all reconnaissance commands
- Track exploitation attempts
- Generate client reports automatically
- Maintain audit trail

### Security Audits
- Compliance documentation (PCI-DSS, ISO 27001)
- Evidence collection
- Timeline reconstruction
- Team collaboration

### Training & Education
- Capture learning sessions
- Create tutorials
- Demonstrate techniques
- Build knowledge base

### Bug Bounty
- Document vulnerability discovery
- Proof of concept documentation
- Collaboration with teams
- Report generation

---

## 🛠️ Development

### Running Tests

```bash
pytest tests/
pytest tests/ --cov=tsr
```

### Building Package

```bash
python -m build
pip install dist/terminal_session_recorder-2.0.0-py3-none-any.whl
```

### Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📝 Requirements

### Core Requirements
- Python 3.8+
- reportlab
- aiofiles
- aiosqlite
- psutil
- rich
- click
- jinja2
- flask

### Optional Requirements
- **Screenshots**: `mss`, `Pillow`
- **OCR**: `pytesseract`, `opencv-python`
- **Network**: `scapy` (requires root)
- **Cloud**: `boto3`, `google-cloud-storage`

---

## 🔒 Security Considerations

### Best Practices
1. **Encrypt sensitive sessions** - Enable encryption in config
2. **Redact credentials** - Auto-redaction is enabled by default
3. **Secure database** - Store in encrypted filesystem
4. **Limit access** - Use file permissions (chmod 600)
5. **Regular cleanup** - Remove old sessions

### Permissions

Network monitoring requires root:
```bash
sudo tsr record --enable-network
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: PTY not working
```bash
# Check platform
python -c "import sys; print(sys.platform)"
# PTY only works on Linux/macOS
```

**Issue**: Network monitoring fails
```bash
# Install scapy
pip install scapy

# Run with sudo
sudo tsr record --enable-network
```

**Issue**: Screenshots not capturing
```bash
# Install mss
pip install mss Pillow
```

**Issue**: Database locked
```bash
# Check for other TSR instances
ps aux | grep tsr

# Remove lock file
rm ~/.tsr/sessions.db-wal
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

## 🙏 Acknowledgments

- Inspired by `asciinema`, `script`, and `ttyrec`
- Built for the pentesting community
- Special thanks to all contributors

---

## 🗺️ Roadmap

### Version 2.1 (Q2 2026)
- [ ] AI-powered command suggestions
- [ ] Claude API integration for auto-analysis
- [ ] MITRE ATT&CK framework mapping
- [ ] Video recording improvements
- [ ] Mobile app for report viewing

### Version 2.2 (Q3 2026)
- [ ] Team collaboration features
- [ ] Cloud-native deployments
- [ ] Kubernetes monitoring
- [ ] Docker container support
- [ ] REST API

### Version 3.0 (Q4 2026)
- [ ] Enterprise SSO integration
- [ ] Multi-user support
- [ ] Advanced analytics
- [ ] Compliance templates
- [ ] SaaS version

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/jonyhossan110/terminal-session-recorder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jonyhossan110/terminal-session-recorder/discussions)
- **Email**: jonyhossan110@gmail.com

---

## ⭐ Show Your Support

If you find TSR useful, please:
- ⭐ Star this repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code
- 📢 Share with others

---

**Made with ❤️ for the cybersecurity community**
