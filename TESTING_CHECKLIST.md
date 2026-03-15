# ✅ Testing Checklist - TSR v2.0.0

Before publishing, ensure all tests pass.

## 🧪 Installation Testing

### Linux (Ubuntu 22.04)
```bash
# Fresh install
□ Extract archive
□ Run setup_linux.sh
□ Virtual environment created
□ All dependencies installed
□ No error messages
□ tsr command available
□ Version shows 2.0.0

# Manual install
□ pip install -e . works
□ pip install -e ".[all]" works
□ All optional dependencies install
```

### macOS
```bash
□ Setup script runs successfully
□ No permission issues
□ Python 3.8+ detected correctly
□ All features work
```

### Windows 10/11
```bash
□ setup_windows.bat runs
□ Virtual environment created
□ Dependencies installed
□ No encoding errors
□ Commands work in cmd.exe
□ Commands work in PowerShell
```

---

## 🎯 Core Functionality

### Basic Recording
```bash
□ tsr record starts successfully
□ Prompt appears: "username>"
□ Commands execute normally
□ Output displays in real-time
□ Exit/quit command works
□ Reports generated automatically
□ JSON file created
□ PDF file created
□ HTML file created
□ CSV file created
```

### Command Classification
```bash
□ nmap commands → SCANNING
□ sqlmap commands → EXPLOITATION
□ metasploit → EXPLOITATION
□ whois/dig → RECONNAISSANCE
□ Unknown commands → UNKNOWN
□ Confidence scores reasonable
□ Tags generated correctly
```

### Database Operations
```bash
□ Database file created
□ Sessions table created
□ Commands table created
□ Session metadata saved
□ Commands saved with timestamps
□ Search queries work
□ Statistics calculated correctly
□ Foreign keys enforced
□ Indices improve performance
```

---

## 📊 Export Features

### PDF Reports
```bash
□ PDF generated successfully
□ Cover page displays
□ Metadata correct
□ Command log formatted
□ Syntax highlighting works
□ Page numbers present
□ Headers/footers correct
□ Tables formatted properly
□ No encoding errors
□ File opens in PDF reader
```

### HTML Reports
```bash
□ HTML file valid
□ Opens in browser
□ Interactive filtering works
□ Search functionality works
□ Collapsible sections work
□ Syntax highlighting correct
□ Responsive design works
□ Dark theme applied
□ No JavaScript errors
```

### JSON Export
```bash
□ Valid JSON syntax
□ All data preserved
□ Timestamps correct
□ Nested structures valid
□ UTF-8 encoding correct
□ Can be re-imported
```

### CSV Export
```bash
□ Valid CSV format
□ Headers present
□ Data rows correct
□ Opens in Excel
□ No encoding issues
□ Timestamps formatted correctly
```

---

## 🔧 CLI Commands

### tsr record
```bash
□ --user-name works
□ --organization works
□ --output-dir works
□ --timeout works
□ --enable-screenshots works
□ --enable-video works
□ --enable-network works
□ --db-path works
□ --help shows usage
```

### tsr list
```bash
□ Lists all sessions
□ --limit works
□ --user filter works
□ --format json works
□ --format table works
□ Shows session details
□ Session ID correct
```

### tsr search
```bash
□ --search text works
□ --command-type filter works
□ --user filter works
□ Results accurate
□ Limit respected
```

### tsr export
```bash
□ --format pdf works
□ --format html works
□ --format json works
□ --format csv works
□ --format all works
□ --output custom path works
□ File created at correct location
```

### tsr init
```bash
□ Creates config directory
□ Creates config.yaml
□ Default values correct
□ Writes to ~/.tsr/
```

---

## 🔌 Plugin System

### Built-in Plugins
```bash
□ MetasploitPlugin loads
□ NmapPlugin loads
□ Plugins detect commands
□ Metadata added correctly
□ No errors in plugin execution
```

### Plugin Hooks
```bash
□ on_session_start() called
□ on_command_execute() called
□ on_command_complete() called
□ on_session_end() called
□ Return values handled
□ Exceptions handled gracefully
```

---

## 📡 Web Dashboard

### Server Startup
```bash
□ tsr-server starts
□ Port 5000 opens
□ No Flask errors
□ SocketIO initializes
□ Dashboard accessible at localhost:5000
```

### Dashboard Features
```bash
□ Sessions list displays
□ Statistics update
□ Real-time updates work
□ WebSocket connects
□ Search/filter works
□ Session details load
□ No console errors
```

---

## 🎬 Session Replay

### tsr-replay
```bash
□ Loads session correctly
□ Displays metadata
□ Commands play in order
□ Timing respected
□ --speed modifier works
□ --interactive mode works
□ Output displays correctly
□ Completes successfully
```

---

## 🔍 Monitoring Features

### Resource Monitor
```bash
□ Starts without errors
□ CPU usage tracked
□ Memory usage tracked
□ Disk I/O tracked
□ Network I/O tracked
□ Data stored correctly
```

### Network Monitor (with scapy)
```bash
□ Scapy imports (if installed)
□ Packet capture starts
□ PCAP file created
□ Packets saved
□ No permission errors (if root)
```

### Screenshot Capture
```bash
□ mss imports (if installed)
□ Screenshot captured
□ PNG file created
□ Resolution correct
□ Path stored in database
□ :snap command works
```

### System Call Monitor
```bash
□ strace available (Linux)
□ Monitor starts
□ Log file created
□ System calls recorded
□ No performance issues
```

---

## 🔐 Security Features

### Data Redaction
```bash
□ Passwords redacted
□ API keys redacted
□ Tokens redacted
□ SSH keys redacted
□ AWS credentials redacted
□ Regex patterns correct
```

### Hashing
```bash
□ SHA-256 hashes generated
□ Command hashes unique
□ Session hash correct
□ Integrity verifiable
```

### Encryption (if enabled)
```bash
□ Data encrypted correctly
□ Decryption works
□ Key derivation secure
□ No data corruption
```

---

## 🧪 Error Handling

### Invalid Input
```bash
□ Invalid session ID → error message
□ Invalid command type → handled
□ Invalid file path → error message
□ Empty commands → skipped
□ Timeout exceeded → handled
```

### Edge Cases
```bash
□ Very long commands → truncated
□ Binary output → handled
□ Non-UTF-8 output → handled
□ Large outputs → truncated
□ Rapid commands → all captured
□ Ctrl+C → graceful shutdown
```

### Database Errors
```bash
□ Locked database → retry logic
□ Corrupted database → error message
□ Disk full → error message
□ Permission denied → error message
```

---

## 🌐 Cross-Platform

### Linux
```bash
□ Ubuntu 22.04 ✓
□ Debian 12 ✓
□ Fedora 38 ✓
□ Arch Linux ✓
□ PTY/TTY works
□ All features functional
```

### macOS
```bash
□ macOS 13 (Ventura) ✓
□ macOS 14 (Sonoma) ✓
□ PTY/TTY works
□ All features functional
```

### Windows
```bash
□ Windows 10 ✓
□ Windows 11 ✓
□ Basic recording works
□ PTY not available (expected)
□ All other features work
```

---

## 📦 Package Testing

### Build
```bash
□ python -m build succeeds
□ Wheel created
□ Source distribution created
□ No warnings
```

### Installation from Package
```bash
□ pip install dist/*.whl works
□ All commands available
□ Dependencies installed
□ Entry points work
```

### PyPI Upload (Test)
```bash
□ twine check passes
□ Upload to TestPyPI works
□ Install from TestPyPI works
□ All features functional
```

---

## 🔄 CI/CD

### GitHub Actions
```bash
□ Workflow file valid
□ All Python versions tested (3.8-3.12)
□ Linting passes
□ Import tests pass
□ Build succeeds
□ No failures
```

---

## 📝 Documentation

### README.md
```bash
□ Markdown renders correctly
□ All links work
□ Code examples valid
□ Screenshots/images load
□ Table of contents accurate
□ Badges display
```

### INSTALL.md
```bash
□ Instructions clear
□ Commands tested
□ All platforms covered
□ Troubleshooting accurate
```

### CHANGELOG.md
```bash
□ All versions listed
□ Changes documented
□ Format consistent
□ Links work
```

### Code Documentation
```bash
□ Docstrings present
□ Type hints correct
□ Examples valid
□ API documented
```

---

## 🚀 Performance

### Speed Tests
```bash
□ Command execution < 200ms
□ Database queries < 10ms
□ PDF generation < 5s
□ HTML generation < 2s
□ Session load < 1s
□ Search queries < 100ms
```

### Load Tests
```bash
□ 1000 commands → no issues
□ 10 sessions → performs well
□ Large outputs → handled
□ Concurrent access → safe
```

---

## 🎨 User Experience

### CLI UX
```bash
□ Clear error messages
□ Progress indicators work
□ Colors display correctly
□ Help text useful
□ Examples provided
```

### Web UI
```bash
□ Intuitive navigation
□ Responsive design
□ Good performance
□ Clear labels
□ Error messages helpful
```

---

## ✅ Final Checks

### Pre-Release
```bash
□ Version numbers consistent
□ All tests passing
□ No TODO/FIXME in code
□ No debug prints
□ No hardcoded paths
□ No sensitive data
□ License file present
□ Authors credited
```

### Post-Install Verification
```bash
tsr --version                    # Shows 2.0.0
tsr --help                       # Shows all commands
tsr init                         # Creates config
tsr record --user-name "Test"    # Starts recording
tsr list                         # Shows sessions
tsr-server                       # Starts dashboard
```

---

## 📊 Test Results Template

```
Date: _______________
Tester: _______________
OS: _______________
Python: _______________

Installation:      □ Pass  □ Fail
Core Features:     □ Pass  □ Fail
Export:            □ Pass  □ Fail
CLI:               □ Pass  □ Fail
Plugins:           □ Pass  □ Fail
Web Dashboard:     □ Pass  □ Fail
Replay:            □ Pass  □ Fail
Monitoring:        □ Pass  □ Fail
Security:          □ Pass  □ Fail
Documentation:     □ Pass  □ Fail

Issues Found:
_______________________________________________
_______________________________________________

Overall: □ Ready for Release  □ Needs Work
```

---

## 🐛 Bug Reporting

If you find issues during testing:

1. Check GitHub Issues first
2. Create new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Error messages/logs

---

**Testing completed? Ready to publish! 🚀**
