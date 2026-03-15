#!/usr/bin/env python3
"""JSON Exporter"""

import json
import aiofiles
from pathlib import Path


class JSONExporter:
    def __init__(self, config):
        self.config = config
    
    async def export(self, session, commands, output_path):
        """Export session to JSON"""
        data = {
            'session': session,
            'commands': commands,
            'metadata': {
                'exported_by': 'TSR v2.0.0',
                'format_version': '2.0',
            }
        }
        
        async with aiofiles.open(output_path, 'w') as f:
            await f.write(json.dumps(data, indent=2, ensure_ascii=False))
        
        return output_path
