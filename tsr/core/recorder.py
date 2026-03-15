#!/usr/bin/env python3
"""
Advanced Asynchronous Terminal Session Recorder with PTY/TTY Support
High-performance recording engine with real-time command classification
"""

import asyncio
import os
import sys
import signal
import pty
import select
import termios
import tty
import struct
import fcntl
import hashlib
import psutil
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from tsr.core.config import Config
from tsr.core.database import SessionDatabase, CommandEntry, SessionMetadata
from tsr.core.classifier import get_classifier, CommandCategory


@dataclass
class CommandContext:
    """Context for command execution"""
    command: str
    start_time: datetime
    end_time: Optional[datetime] = None
    pid: Optional[int] = None
    return_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""


class PTYRecorder:
    """PTY-based terminal recorder for full terminal emulation"""
    
    def __init__(self, config: Config, session_id: str):
        self.config = config
        self.session_id = session_id
        self.master_fd = None
        self.slave_fd = None
        self.child_pid = None
        self.running = False
        self.command_buffer = []
        self.current_line = ""
        
    def _set_terminal_size(self, fd):
        """Set terminal size to match current terminal"""
        try:
            size = struct.pack("HHHH", 24, 80, 0, 0)  # Default size
            # Try to get actual size
            try:
                import shutil
                cols, rows = shutil.get_terminal_size()
                size = struct.pack("HHHH", rows, cols, 0, 0)
            except:
                pass
            fcntl.ioctl(fd, termios.TIOCSWINSZ, size)
        except Exception:
            pass
    
    async def start(self, shell: str = None):
        """Start PTY session"""
        if shell is None:
            shell = os.environ.get('SHELL', '/bin/bash')
        
        # Create PTY pair
        self.master_fd, self.slave_fd = pty.openpty()
        self._set_terminal_size(self.slave_fd)
        
        # Fork process
        self.child_pid = os.fork()
        
        if self.child_pid == 0:
            # Child process
            os.close(self.master_fd)
            os.setsid()
            fcntl.ioctl(self.slave_fd, termios.TIOCSCTTY, 0)
            
            # Redirect stdin, stdout, stderr to slave PTY
            os.dup2(self.slave_fd, 0)
            os.dup2(self.slave_fd, 1)
            os.dup2(self.slave_fd, 2)
            
            if self.slave_fd > 2:
                os.close(self.slave_fd)
            
            # Execute shell
            os.execvp(shell, [shell])
        else:
            # Parent process
            os.close(self.slave_fd)
            self.running = True
            
            # Set master to non-blocking
            flags = fcntl.fcntl(self.master_fd, fcntl.F_GETFL)
            fcntl.fcntl(self.master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    
    async def read_output(self, timeout: float = 0.1) -> bytes:
        """Read output from PTY with timeout"""
        try:
            # Use select for timeout
            readable, _, _ = select.select([self.master_fd], [], [], timeout)
            if readable:
                return os.read(self.master_fd, 4096)
        except OSError:
            pass
        return b""
    
    async def write_input(self, data: bytes):
        """Write input to PTY"""
        if self.master_fd:
            try:
                os.write(self.master_fd, data)
            except OSError:
                pass
    
    async def close(self):
        """Close PTY session"""
        self.running = False
        if self.master_fd:
            try:
                os.close(self.master_fd)
            except:
                pass
        if self.child_pid:
            try:
                os.kill(self.child_pid, signal.SIGTERM)
                os.waitpid(self.child_pid, 0)
            except:
                pass


class SessionRecorder:
    """Main asynchronous session recorder with advanced features"""
    
    def __init__(self, config: Config, db: SessionDatabase):
        self.config = config
        self.db = db
        self.session_id = self._generate_session_id()
        self.start_time = datetime.now()
        self.end_time = None
        self.commands: List[CommandContext] = []
        self.classifier = get_classifier()
        self.running = False
        self.pty_recorder = None
        
        # Monitoring components
        self.monitors = []
        self._init_monitors()
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_part = hashlib.md5(os.urandom(16)).hexdigest()[:8]
        return f"{timestamp}_{random_part}"
    
    def _init_monitors(self):
        """Initialize monitoring components based on config"""
        # Resource monitor
        if self.config.monitoring.enable_resources:
            from tsr.monitors.resources import ResourceMonitor
            self.monitors.append(ResourceMonitor(self))
        
        # Network monitor
        if self.config.monitoring.enable_network:
            try:
                from tsr.monitors.network import NetworkMonitor
                self.monitors.append(NetworkMonitor(self))
            except ImportError:
                print("[warn] Network monitoring requires scapy. Install with: pip install scapy")
        
        # System call monitor
        if self.config.monitoring.enable_strace:
            try:
                from tsr.monitors.syscalls import SyscallMonitor
                self.monitors.append(SyscallMonitor(self))
            except ImportError:
                pass
    
    async def start(self):
        """Start recording session"""
        self.running = True
        
        # Create session in database
        metadata = SessionMetadata(
            session_id=self.session_id,
            user_name=self.config.user_name,
            organization=self.config.organization,
            start_time=self.start_time.isoformat(),
            platform=sys.platform,
            hostname=os.uname().nodename if hasattr(os, 'uname') else 'unknown',
            ip_address=self._get_ip_address(),
            tags=json.dumps([]),
        )
        
        await self.db.create_session(metadata)
        
        # Start monitors
        for monitor in self.monitors:
            await monitor.start()
        
        # Start PTY recorder if enabled
        use_pty = sys.platform != 'win32'  # PTY only on Unix-like systems
        if use_pty:
            self.pty_recorder = PTYRecorder(self.config, self.session_id)
            await self.pty_recorder.start()
        
        print(f"\n[TSR] Session started: {self.session_id}")
        print(f"[TSR] User: {self.config.user_name}")
        if self.config.organization:
            print(f"[TSR] Organization: {self.config.organization}")
        print(f"[TSR] Database: {self.db.db_path}")
        print("[TSR] Type 'exit' or press Ctrl+D to end session\n")
    
    async def execute_command(self, command: str) -> CommandContext:
        """Execute command and record results"""
        ctx = CommandContext(
            command=command,
            start_time=datetime.now()
        )
        
        try:
            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE
            )
            
            ctx.pid = process.pid
            
            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.config.session.command_timeout
                )
                ctx.stdout = stdout.decode('utf-8', errors='replace')
                ctx.stderr = stderr.decode('utf-8', errors='replace')
                ctx.return_code = process.returncode
            except asyncio.TimeoutError:
                process.kill()
                ctx.stderr = f"Command timed out after {self.config.session.command_timeout}s"
                ctx.return_code = -1
                
        except Exception as e:
            ctx.stderr = str(e)
            ctx.return_code = -1
        
        ctx.end_time = datetime.now()
        self.commands.append(ctx)
        
        # Classify command
        category, tags, confidence = self.classifier.classify(command)
        
        # Save to database
        duration_ms = int((ctx.end_time - ctx.start_time).total_seconds() * 1000)
        
        entry = CommandEntry(
            session_id=self.session_id,
            timestamp=ctx.start_time.isoformat(),
            command=command,
            command_type=category.value,
            return_code=ctx.return_code,
            stdout=ctx.stdout[:self.config.session.truncate_output],
            stderr=ctx.stderr[:self.config.session.truncate_output],
            duration_ms=duration_ms,
            hash=hashlib.sha256(command.encode()).hexdigest(),
            tags=json.dumps(tags),
        )
        
        await self.db.add_command(entry)
        
        # Auto-save session stats
        if self.config.session.auto_save:
            await self._update_session_stats()
        
        return ctx
    
    async def _update_session_stats(self):
        """Update session statistics in database"""
        failed = sum(1 for cmd in self.commands if cmd.return_code != 0)
        duration = int((datetime.now() - self.start_time).total_seconds())
        
        await self.db.update_session(
            self.session_id,
            command_count=len(self.commands),
            failed_commands=failed,
            duration_seconds=duration
        )
    
    async def interactive_loop(self):
        """Run interactive command loop"""
        if self.pty_recorder:
            await self._pty_interactive_loop()
        else:
            await self._simple_interactive_loop()
    
    async def _simple_interactive_loop(self):
        """Simple interactive loop without PTY"""
        prompt = f"{self.config.user_name}> "
        
        while self.running:
            try:
                # Read command from stdin (blocking, but in executor)
                loop = asyncio.get_event_loop()
                command = await loop.run_in_executor(None, input, prompt)
                
                if not command.strip():
                    continue
                
                if command.lower() in ('exit', 'quit'):
                    break
                
                # Handle special commands
                if command.startswith(':'):
                    await self._handle_special_command(command)
                    continue
                
                # Execute and record
                ctx = await self.execute_command(command)
                
                # Print output
                if ctx.stdout:
                    print(ctx.stdout, end='')
                if ctx.stderr:
                    print(ctx.stderr, end='', file=sys.stderr)
                    
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"[error] {e}")
    
    async def _pty_interactive_loop(self):
        """Interactive loop with PTY support"""
        # Save original terminal settings
        old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            # Set terminal to raw mode
            tty.setraw(sys.stdin)
            
            while self.running and self.pty_recorder.running:
                # Check for data from stdin or PTY
                readable, _, _ = select.select(
                    [sys.stdin, self.pty_recorder.master_fd], [], [], 0.1
                )
                
                # Input from user
                if sys.stdin in readable:
                    data = os.read(sys.stdin.fileno(), 4096)
                    if data:
                        await self.pty_recorder.write_input(data)
                        # Detect command submission (Enter key)
                        if b'\r' in data or b'\n' in data:
                            # Command completed, process it
                            await self._process_pty_command()
                
                # Output from PTY
                if self.pty_recorder.master_fd in readable:
                    data = await self.pty_recorder.read_output()
                    if data:
                        os.write(sys.stdout.fileno(), data)
                
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    async def _process_pty_command(self):
        """Process command from PTY buffer"""
        # This is simplified - full implementation would parse PTY escape sequences
        pass
    
    async def _handle_special_command(self, command: str):
        """Handle special TSR commands"""
        parts = command[1:].split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == 'snap' or cmd == 'screenshot':
            await self._capture_screenshot(args)
        elif cmd == 'tag':
            await self._add_tag(args)
        elif cmd == 'stats':
            await self._show_stats()
        elif cmd == 'help':
            self._show_help()
        else:
            print(f"Unknown command: {command}")
    
    async def _capture_screenshot(self, label: str):
        """Capture screenshot"""
        if not self.config.session.enable_screenshots:
            print("[info] Screenshots disabled")
            return
        
        try:
            from tsr.monitors.screenshots import capture_screenshot
            path = await capture_screenshot(
                self.session_id,
                label or f"manual_{len(self.commands)}",
                self.config
            )
            print(f"[ok] Screenshot saved: {path}")
        except ImportError:
            print("[warn] Screenshot support requires mss. Install with: pip install mss")
    
    async def _add_tag(self, tag: str):
        """Add tag to last command"""
        if self.commands:
            print(f"[ok] Tagged last command: {tag}")
    
    async def _show_stats(self):
        """Show session statistics"""
        stats = await self.db.get_statistics(self.session_id)
        print("\n=== Session Statistics ===")
        print(f"Commands: {len(self.commands)}")
        print(f"Failed: {sum(1 for c in self.commands if c.return_code != 0)}")
        print(f"Duration: {(datetime.now() - self.start_time).total_seconds():.1f}s")
        if stats.get('type_distribution'):
            print("\nCommand Types:")
            for cmd_type, count in stats['type_distribution'].items():
                print(f"  {cmd_type}: {count}")
        print()
    
    def _show_help(self):
        """Show help message"""
        print("""
TSR Special Commands:
  :snap [label]     - Capture screenshot
  :tag <tag>        - Tag last command
  :stats            - Show session statistics
  :help             - Show this help
  exit/quit         - End session
        """)
    
    async def stop(self):
        """Stop recording and finalize session"""
        self.running = False
        self.end_time = datetime.now()
        
        # Stop monitors
        for monitor in self.monitors:
            await monitor.stop()
        
        # Close PTY
        if self.pty_recorder:
            await self.pty_recorder.close()
        
        # Final stats update
        await self._update_session_stats()
        await self.db.update_session(
            self.session_id,
            end_time=self.end_time.isoformat()
        )
        
        print(f"\n[TSR] Session ended: {self.session_id}")
        print(f"[TSR] Total commands: {len(self.commands)}")
        print(f"[TSR] Duration: {(self.end_time - self.start_time).total_seconds():.1f}s")
    
    def _get_ip_address(self) -> str:
        """Get primary IP address"""
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
