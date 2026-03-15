#!/usr/bin/env python3
"""Nmap Scan Parser Plugin"""

import re
from tsr.plugins.base import BasePlugin


class NmapPlugin(BasePlugin):
    """Parse and enhance nmap scan results"""
    
    @property
    def name(self) -> str:
        return "nmap"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    async def on_session_start(self):
        self.scan_count = 0
    
    async def on_command_execute(self, command: str):
        """Detect nmap commands"""
        if command.startswith('nmap'):
            self.scan_count += 1
            
            # Parse scan type
            scan_type = 'basic'
            if '-sS' in command:
                scan_type = 'SYN scan'
            elif '-sT' in command:
                scan_type = 'TCP connect scan'
            elif '-sU' in command:
                scan_type = 'UDP scan'
            elif '-sV' in command:
                scan_type = 'Version detection'
            
            return {
                'detected': True,
                'scan_number': self.scan_count,
                'scan_type': scan_type
            }
        return {}
    
    async def on_command_complete(self, command: str, result):
        """Parse nmap output for open ports"""
        if command.startswith('nmap'):
            output = result.get('stdout', '')
            # Could extract open ports, services, etc.
            open_ports = re.findall(r'(\d+)/tcp\s+open', output)
            if open_ports:
                print(f"[NmapPlugin] Detected {len(open_ports)} open ports")
    
    async def on_session_end(self):
        if self.scan_count > 0:
            print(f"[NmapPlugin] Total nmap scans: {self.scan_count}")
