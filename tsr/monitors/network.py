#!/usr/bin/env python3
"""Network Traffic Monitor using Scapy"""

import asyncio
from datetime import datetime
from pathlib import Path

try:
    from scapy.all import sniff, wrpcap, AsyncSniffer
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


class NetworkMonitor:
    """Monitor and capture network traffic during session"""
    
    def __init__(self, recorder):
        if not SCAPY_AVAILABLE:
            raise ImportError("Network monitoring requires scapy")
        
        self.recorder = recorder
        self.config = recorder.config
        self.running = False
        self.sniffer = None
        self.packets = []
        self.pcap_path = None
        
    async def start(self):
        """Start network capture"""
        if not self.running:
            self.running = True
            
            # Setup PCAP file
            pcap_dir = Path(self.config.monitoring.pcap_dir)
            pcap_dir.mkdir(parents=True, exist_ok=True)
            self.pcap_path = pcap_dir / f"{self.recorder.session_id}.pcap"
            
            # Start async sniffer
            self.sniffer = AsyncSniffer(
                iface=self.config.monitoring.network_interface,
                prn=self._packet_handler,
                store=True
            )
            self.sniffer.start()
            print(f"[NetworkMonitor] Capturing on {self.config.monitoring.network_interface}")
    
    async def stop(self):
        """Stop capture and save PCAP"""
        if self.sniffer and self.running:
            self.running = False
            self.sniffer.stop()
            
            if self.packets:
                wrpcap(str(self.pcap_path), self.packets)
                print(f"[NetworkMonitor] Saved {len(self.packets)} packets to {self.pcap_path}")
    
    def _packet_handler(self, packet):
        """Handle captured packet"""
        self.packets.append(packet)


class SimpleNetworkMonitor:
    """Fallback network monitor without scapy"""
    
    def __init__(self, recorder):
        self.recorder = recorder
        
    async def start(self):
        print("[NetworkMonitor] Scapy not available, network monitoring disabled")
    
    async def stop(self):
        pass
