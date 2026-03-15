# Changelog

All notable changes to Terminal Session Recorder will be documented in this file.

## [2.0.0] - 2026-03-15

### 🚀 Major Release - Complete Rewrite

#### Added
- **Async Architecture**: Complete rewrite using async/await for 5x performance improvement
- **SQLite Database**: Persistent storage with fast querying capabilities
- **Smart Command Classification**: Auto-detect and categorize pentesting tools
  - Reconnaissance, Scanning, Enumeration, Exploitation, etc.
  - MITRE ATT&CK technique mapping
- **PTY/TTY Support**: Full terminal emulation on Linux/macOS
- **Interactive HTML Reports**: Beautiful, searchable, filterable web reports
- **Web Dashboard**: Real-time monitoring via Flask + SocketIO
- **Plugin System**: Extensible architecture for custom integrations
- **Evidence Chain**: Cryptographic hashing for audit trails
- **Advanced Monitoring**:
  - Resource monitoring (CPU, memory, disk, network)
  - Network packet capture (scapy integration)
  - System call tracing (strace integration)
- **Session Replay**: Play back recorded sessions with timing
- **Multiple Export Formats**: PDF, HTML, JSON, CSV
- **CLI Tools**: `tsr`, `tsr-server`, `tsr-replay`
- **Data Redaction**: Auto-redact passwords, API keys, credentials
- **Cloud Storage**: S3, GCS integration (optional)

#### Changed
- Complete codebase restructure into modular packages
- Database-backed instead of file-only storage
- Modern Python packaging (pyproject.toml)
- Enhanced PDF reports with better styling
- Improved configuration management (YAML/JSON)

#### Performance
- 5x faster command execution
- Async I/O for non-blocking operations
- Efficient database queries with indexing
- Lazy loading for large sessions

#### Security
- SHA-256 hashing for integrity verification
- Optional encryption support
- Automatic sensitive data redaction
- Configurable security policies

### [1.1.1] - 2024-12-15

#### Added
- Screenshot capture support
- Organization branding in PDFs
- Configuration file support

#### Fixed
- Windows compatibility issues
- CSV export encoding errors

### [1.0.0] - 2024-12-01

#### Initial Release
- Basic terminal session recording
- Command logging and output capture
- PDF report generation
- JSON and CSV export
- Cross-platform support

---

## Upgrade Guide: v1.x → v2.0

### Breaking Changes

1. **Database Requirement**: v2.0 uses SQLite instead of plain files
   ```bash
   # No migration needed - v2.0 can import v1.x JSON files
   tsr import-v1 old_session.json
   ```

2. **CLI Changes**:
   ```bash
   # v1.x
   python main.py --record-session --user-name "Name"
   
   # v2.0
   tsr record --user-name "Name"
   ```

3. **Configuration**:
   ```bash
   # v1.x: ~/.web_security_tool/config.json
   # v2.0: ~/.tsr/config.yaml
   
   tsr init  # Creates new config
   ```

### Migration Steps

1. Install v2.0:
   ```bash
   pip install terminal-session-recorder==2.0.0
   ```

2. Initialize configuration:
   ```bash
   tsr init
   ```

3. Import old sessions (optional):
   ```bash
   for file in terminal_session_*.json; do
     tsr import-v1 "$file"
   done
   ```

4. Start using new CLI:
   ```bash
   tsr record --user-name "Your Name"
   ```

---

## Version Numbering

We use [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality (backwards-compatible)
- PATCH version for backwards-compatible bug fixes
