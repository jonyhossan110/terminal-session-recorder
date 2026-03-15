# Terminal Session Recorder v2.0.0

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/jonyhossan110/terminal-session-recorder)

**Enterprise-grade terminal session recorder for penetration testing and security audits**

Developed by **Md. Jony Hassain** | **HexaCyberLab Web Agency**

---

## 🚀 What's New in v2.0

### Major Improvements
- ⚡ **5x Faster Performance** - Async/await architecture
- 🗄️ **SQLite Database** - Fast querying and session management
- 🧠 **Smart Command Classification** - Auto-detect pentesting tools (nmap, metasploit, etc.)
- 🖥️ **PTY/TTY Support** - Full terminal emulation on Linux
- 🌐 **Interactive HTML Reports** - Searchable, filterable, beautiful
- 📊 **Real-time Web Dashboard** - Monitor sessions live
- 🔌 **Plugin System** - Extensible with custom plugins
- 🔐 **Evidence Chain** - Cryptographic hashing for audit trails
- 📸 **Advanced Screenshots** - Full screen capture with OCR support
- 🌍 **Network Monitoring** - Packet capture integration (scapy)
- 📈 **Resource Monitoring** - Track CPU, memory, disk, network
- 🔗 **LinkedIn Integration** - Share session summaries on LinkedIn

---

## 📦 Installation

### Quick Install (Recommended)

```bash
# Clone repository
git clone https://github.com/jonyhossan110/terminal-session-recorder.git
cd terminal-session-recorder

# Install with all features
pip install -e ".[all]"

# Or install minimal version
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install terminal-session-recorder
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
