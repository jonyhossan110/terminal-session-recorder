#!/usr/bin/env python3
"""System Resource Monitor"""

import asyncio
import psutil
from datetime import datetime


class ResourceMonitor:
    """Monitor CPU, memory, disk, and network usage"""
    
    def __init__(self, recorder):
        self.recorder = recorder
        self.running = False
        self.task = None
        self.interval = 5.0  # seconds
        
    async def start(self):
        """Start monitoring"""
        self.running = True
        self.task = asyncio.create_task(self._monitor_loop())
        
    async def stop(self):
        """Stop monitoring"""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
    
    async def _monitor_loop(self):
        """Monitoring loop"""
        while self.running:
            try:
                stats = self._collect_stats()
                # Store in database or file
                # await self.recorder.db.add_system_event(...)
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[warn] Resource monitoring error: {e}")
                
    def _collect_stats(self):
        """Collect current resource stats"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': dict(psutil.net_io_counters()._asdict()),
        }
