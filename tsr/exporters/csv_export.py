#!/usr/bin/env python3
"""CSV Exporter"""

import csv
import aiofiles


class CSVExporter:
    def __init__(self, config):
        self.config = config
    
    async def export(self, session, commands, output_path):
        """Export commands to CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'command', 'command_type', 'return_code',
                'duration_ms', 'stdout', 'stderr'
            ])
            writer.writeheader()
            for cmd in commands:
                writer.writerow({
                    'timestamp': cmd.get('timestamp', ''),
                    'command': cmd.get('command', ''),
                    'command_type': cmd.get('command_type', ''),
                    'return_code': cmd.get('return_code', ''),
                    'duration_ms': cmd.get('duration_ms', ''),
                    'stdout': cmd.get('stdout', '')[:500],
                    'stderr': cmd.get('stderr', '')[:500],
                })
        
        return output_path
