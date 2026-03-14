# Terminal Session Recorder v1.1.1

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/terminal-session-recorder.svg)](https://pypi.org/project/terminal-session-recorder/)

A professional tool for recording terminal sessions with command logging, output capture, and automatic PDF report generation.

## Features

- **Interactive Session Recording**: Captures all terminal commands and their outputs in real-time
- **Cross-Platform Support**: Works on Windows, Linux, and macOS terminals
- **Professional PDF Reports**: Automatically generated high-quality PDF reports with custom branding
- **CSV Export**: Export session logs to CSV format for analysis
- **JSON Logging**: Detailed session data stored in structured JSON format
- **Command History**: Complete chronological record of all executed commands
- **Output Capture**: Full capture of command outputs including errors and warnings
- **Session Metadata**: Timestamps, user information, and session statistics
- **Graceful Termination**: Proper handling of session end with Ctrl+C or exit commands
- **Configurable Output**: Custom file prefixes and user naming
- **Streaming Capture**: Real-time command output streaming with minimal overhead
- **Auto-Save Safety**: Partial logs flushed to disk after each command to avoid data loss
- **Full Screen Screenshots**: Captures the entire screen after each command execution for complete context
- **Rich Visual Elements**: Professional typography, color schemes, and structured layouts

## Installation

### Quick Setup

**Windows:**
```cmd
setup_windows.bat
```

**Linux/macOS:**
```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

### Manual Installation

1. Clone the repository:
   ```
   git clone https://github.com/jonyhossan110/terminal-session-recorder.git
   cd terminal-session-recorder
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

   Or install as a package:
   ```
   pip install -e .
   ```

   Or install from built distribution:
   ```
   pip install dist/web_security_tool-1.1.0-py3-none-any.whl
   ```

## Usage

### Start Session Recording

The tool acts as an interactive terminal session recorder that captures every command you run and its output:

```
python main.py --record-session --user-name "Your Name"
```

If you don't provide `--user-name`, it will default to the system username.

### During Recording Session

- Run any terminal commands as usual (bash, zsh, cmd, PowerShell, etc.)
- The recorder logs each command and output in the background
- Session recording does not interfere with normal terminal use
- To capture HD screenshots, start the recorder with `--enable-screenshots`. When enabled, the recorder automatically captures a screenshot of the terminal area after each command and embeds it into the generated PDF. You can also capture ad-hoc screenshots during the session by typing `:snap [optional-label]`. Screenshots are saved under the session output folder (default `screenshots/`).

### End Session

Finish the session by typing `exit`, `quit`, or pressing `Ctrl+C`. The tool automatically generates:

- `terminal_session_<timestamp>.json` - Full command and output log
- `terminal_session_<timestamp>.csv` - CSV export for analysis
- `terminal_session_<timestamp>.pdf` - Professional PDF report

### Quick Start Aliases

**Linux/macOS** - Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias recordshell="python /path/to/main.py --record-session"
```

**Windows PowerShell** - Add to your profile (`$PROFILE`):
```powershell
function Record-Shell { python "C:\path\to\main.py" --record-session }
```

## Command Line Options

- `--record-session`: Start the interactive terminal session recorder (required)
- `--user-name USER_NAME`: Name to display in the session report (optional, defaults to system username)
- `--organization ORG`: Organization/agency name to include in the report header and cover
- `-o, --output OUTPUT`: Output file prefix for session files (optional)
- `--output-dir DIR`: Directory where JSON/CSV/PDF artifacts are written (defaults to current working directory or config)
- `--timeout SECONDS`: Per-command timeout; useful to keep long-running commands from blocking the session
- `--enable-screenshots`: Allow in-session terminal-area screenshot capture via `:snap`
- `--screenshot-dir DIR`: Directory to store captured screenshots (defaults to `<output>/screenshots`)

## PDF Report Features

The professional PDF reports include:

- **Cover Page**: Custom terminal logo, session title, and executive summary
- **Professional Branding**: Clean color scheme with terminal-themed elements
- **Session Timeline**: Chronological command execution timeline
- **Command Details**: Individual command entries with timestamps and outputs
- **Session Statistics**: Total commands, session duration, and performance metrics
- **Structured Layout**: Clear sections with icons and proper spacing
- **Status Indicators**: Color-coded indicators for command success/failure
- **Page Headers/Footers**: Consistent branding with timestamps and page numbers
- **High-Quality Typography**: Professional fonts and sizing throughout

## Sample PDF Structure

1. **Session Summary** - Overview of the recorded session with key statistics
2. **Session Metadata** - Recording details, user information, and timestamps
3. **Command Timeline** - Chronological list of all executed commands
4. **Command Details** - Individual command entries with inputs and outputs
5. **Session Statistics** - Total commands, success rates, and performance metrics
6. **Output Analysis** - Summary of command outputs and error patterns
7. **Session Duration** - Timeline analysis and session length breakdown

## Requirements

- Python 3.6+
- reportlab (for PDF generation)
- subprocess (built-in)
- csv (built-in)
- json (built-in)
- pathlib (built-in)

## Changelog

### v1.1.0 (2026-03-14)
- Added terminal session recording feature (`--record-session`)
- Customizable user name in session prompts (`--user-name`)
- Organization branding line in PDFs (defaults to HexaCyberLab Web Agency; override with `--organization`)
- Professional PDF reports for session logs with cover page, headers/footers, and improved styling
- Enhanced PDF design with better typography and layout
- Signal handling for graceful session termination
- Configuration file support (`~/.web_security_tool/config.json`)
- CSV export for session logs
- Table of contents in PDF reports
- Project build system with wheel and source distributions
- Streaming output capture with per-command timeouts and configurable command limits
- Auto-save after each command to reduce data loss risk
- New CLI switches: `--output-dir` and `--timeout` for faster, more predictable runs
- HD screenshot capture via `:snap` with PDF embedding

### v1.1.0 (2024-12-XX)
- Refactored to focus on terminal session recording functionality
- Removed web security scanning features
- Added cross-platform terminal session recording
- Enhanced PDF reports for session logging
- Added CSV export functionality
- Improved configuration management

### v1.0.0 (2024-12-XX)
- Initial release with terminal session recording
- Interactive command logging and output capture
- Professional PDF report generation
- JSON and CSV export formats
- Cross-platform compatibility

## Disclaimer

This tool records terminal sessions for documentation and analysis purposes. Use responsibly and ensure you have appropriate permissions when recording sessions that may contain sensitive information. The tool captures all command inputs and outputs, so be mindful of what you execute during recording sessions.
