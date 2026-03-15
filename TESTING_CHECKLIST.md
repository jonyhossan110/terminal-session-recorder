# ✅ Testing Checklist - TSR v2.0.0

Before publishing, ensure all tests pass.

## 🚀 Step-by-Step Testing Guide

### Prerequisites
```bash
# Ensure you're in the project directory
cd terminal-session-recorder

# Activate virtual environment
source .venv/bin/activate

# Verify installation
tsr --version  # Should show 2.0.0
tsr --help     # Should show all commands
```

### Step 1: Basic Recording Test
```bash
# Create test directory
mkdir -p test_output
cd test_output

# Start basic recording
tsr record --user-name "Test User" --organization "Test Corp"

# In the TSR prompt, run these commands:
whoami
pwd
ls -la
echo "Hello TSR v2.0!"
date
ps aux | head -5
exit

# Check if files were created
ls -la
# Should see: session_*.json, session_*.pdf, session_*.html, session_*.csv
```

### Step 2: Advanced Recording with Screenshots
```bash
# Test with screenshots (requires GUI)
tsr record --user-name "Test User" --enable-screenshots --output-dir ./screenshots_test

# Run some commands that change the terminal output
clear
echo "Testing screenshots"
ls -la /
df -h
top -n 1 | head -10
exit

# Check screenshot files
ls screenshots_test/
# Should see screenshot_*.png files
```

### Step 3: Network Monitoring Test
```bash
# Test network monitoring (may require sudo)
sudo tsr record --user-name "Test User" --enable-network-monitor --output-dir ./network_test

# Run network-related commands
ping -c 3 google.com
curl -I https://github.com
nslookup github.com
exit

# Check network data in JSON output
cat network_test/session_*.json | grep -A 10 network_packets
```

### Step 4: Plugin System Test
```bash
# Test Nmap plugin
tsr record --user-name "Test User" --output-dir ./plugin_test

# Run nmap command
nmap -sV -p 80,443 localhost
exit

# Check if command was classified as SCANNING
cat plugin_test/session_*.json | grep -A 5 classification

# Test Metasploit plugin (if available)
msfconsole -q -x "version; exit"
# Check classification in output
```

### Step 5: Export Features Test
```bash
# Generate a session first
tsr record --user-name "Export Test" --output-dir ./export_test
# Run: echo "Testing exports"; ls; exit

# Test individual exports
tsr export --session-id $(ls export_test/session_*.json | head -1 | xargs basename | sed 's/session_//;s/\.json//') --format pdf --output export_test/manual.pdf
tsr export --session-id $(ls export_test/session_*.json | head -1 | xargs basename | sed 's/session_//;s/\.json//') --format html --output export_test/manual.html
tsr export --session-id $(ls export_test/session_*.json | head -1 | xargs basename | sed 's/session_//;s/\.json//') --format json --output export_test/manual.json
tsr export --session-id $(ls export_test/session_*.json | head -1 | xargs basename | sed 's/session_//;s/\.json//') --format csv --output export_test/manual.csv

# Verify files
ls -la export_test/
file export_test/manual.pdf   # Should be PDF
file export_test/manual.html  # Should be HTML
python3 -c "import json; json.load(open('export_test/manual.json'))"  # Should not error
head export_test/manual.csv   # Should have CSV headers
```

### Step 6: Web Dashboard Test
```bash
# Start web server in background
tsr-server &
SERVER_PID=$!

# Wait a moment
sleep 3

# Test if server is running
curl -s http://localhost:5000 | head -10
# Should return HTML content

# Test API endpoints
curl -s http://localhost:5000/api/sessions | head -5
curl -s http://localhost:5000/api/stats | head -5

# Open in browser (if GUI available)
# firefox http://localhost:5000 or chrome http://localhost:5000

# Stop server
kill $SERVER_PID
```

### Step 7: Session Replay Test
```bash
# Create a session to replay
tsr record --user-name "Replay Test" --output-dir ./replay_test
# Run: echo "First command"; sleep 1; echo "Second command"; exit

# Test replay
tsr replay --session-id $(ls replay_test/session_*.json | head -1 | xargs basename | sed 's/session_//;s/\.json//')
# Should replay the commands with timing
```

### Step 8: Database and Search Test
```bash
# List all sessions
tsr list
# Should show all recorded sessions

# Search for specific commands
tsr search --query "echo"
# Should find sessions with echo commands

# Search by user
tsr search --user "Test User"
# Should find sessions by that user

# Test statistics
tsr stats
# Should show session counts, command types, etc.
```

### Step 9: Configuration Test
```bash
# Check current config
cat ~/.tsr/config.yaml

# Test config reload
tsr init --force
# Should recreate config

# Test custom config
cp ~/.tsr/config.yaml ~/.tsr/config.backup
echo "database_path: ./custom.db" >> ~/.tsr/config.yaml
tsr record --user-name "Config Test" --output-dir ./config_test
# Should use custom database
ls custom.db  # Should exist
exit

# Restore config
mv ~/.tsr/config.backup ~/.tsr/config.yaml
```

### Step 10: CLI Options Test
```bash
# Test various CLI options
tsr record --help
tsr list --help
tsr search --help
tsr export --help

# Test output directory option
tsr record --user-name "CLI Test" --output-dir /tmp/tsr_test
ls /tmp/tsr_test/
# Should create files in /tmp/tsr_test

# Test timeout option
timeout 10 tsr record --user-name "Timeout Test" --timeout 5
# Should exit after 5 seconds
```

### Step 11: Error Handling Test
```bash
# Test invalid commands
tsr invalid-command
# Should show error and help

# Test missing required options
tsr record
# Should prompt for user name or show error

# Test invalid session ID
tsr export --session-id invalid-id
# Should show error

# Test network without permissions
tsr record --enable-network-monitor 2>&1 | grep -i permission
# Should show permission warning (if not root)
```

### Step 12: Performance Test
```bash
# Test with large output
tsr record --user-name "Performance Test" --output-dir ./perf_test
# Run: find /usr -name "*.py" 2>/dev/null | head -100
# Run: ps aux
# Run: dmesg | tail -50
exit

# Check file sizes
ls -lh perf_test/
# Should be reasonable sizes

# Test multiple sessions
for i in {1..5}; do
  tsr record --user-name "Batch Test $i" --output-dir ./batch_test_$i
  echo "Test command $i"; exit
done

tsr list | grep "Batch Test" | wc -l
# Should show 5 sessions
```

### Step 13: Integration Test
```bash
# Full workflow test
mkdir integration_test
cd integration_test

# Record with all features
tsr record --user-name "Integration Test" --enable-screenshots --enable-network-monitor --organization "Test Corp"

# Run comprehensive commands
echo "=== System Info ==="
uname -a
whoami
pwd

echo "=== Network Test ==="
ping -c 2 8.8.8.8

echo "=== File Operations ==="
touch test_file.txt
echo "Test content" > test_file.txt
cat test_file.txt
rm test_file.txt

echo "=== Process Info ==="
ps | head -5

exit

# Export all formats
SESSION_ID=$(ls session_*.json | head -1 | sed 's/session_//;s/\.json//')
tsr export --session-id $SESSION_ID --format all

# Start web server and check
tsr-server &
sleep 2
curl -s http://localhost:5000/api/sessions | grep "Integration Test"
kill %1

# Verify all files created
ls -la
# Should have: session files, exports, screenshots, network data
```

### Cleanup
```bash
# Remove test files
rm -rf test_output screenshots_test network_test plugin_test export_test
rm -rf replay_test config_test perf_test batch_test_* integration_test
rm -f custom.db

# Reset database if needed
rm -f ~/.tsr/sessions.db
tsr init
```

---

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
