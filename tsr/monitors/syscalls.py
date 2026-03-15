#!/usr/bin/env python3
"""System Call Monitor using strace"""

import asyncio
import subprocess
from pathlib import Path


class SyscallMonitor:
    """Monitor system calls using strace (Linux only)"""
    
    def __init__(self, recorder):
        self.recorder = recorder
        self.config = recorder.config
        self.running = False
        self.strace_proc = None
        self.log_file = None
        
    async def start(self):
        """Start strace monitoring"""
        import sys
        if sys.platform != 'linux':
            print("[SyscallMonitor] strace only available on Linux")
            return
        
        self.running = True
        log_dir = Path(self.config.output_dir) / 'strace_logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = log_dir / f"{self.recorder.session_id}.strace"
        
        # Start strace on current process
        cmd = ['strace', '-f', '-o', str(self.log_file), '-p', str(self.recorder.pty_recorder.child_pid)]
        
        try:
            self.strace_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"[SyscallMonitor] Logging to {self.log_file}")
        except FileNotFoundError:
            print("[SyscallMonitor] strace not found, install with: sudo apt install strace")
        except Exception as e:
            print(f"[SyscallMonitor] Failed to start: {e}")
    
    async def stop(self):
        """Stop strace"""
        if self.strace_proc:
            self.strace_proc.terminate()
            try:
                self.strace_proc.wait(timeout=5)
            except:
                self.strace_proc.kill()
            print(f"[SyscallMonitor] Stopped, log saved to {self.log_file}")
