#!/usr/bin/env python3
"""Configuration Manager for Web Security Tool"""

import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file=None):
        if config_file is None:
            # Cross-platform config directory
            if os.name == 'nt':  # Windows
                config_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'web_security_tool')
            else:  # Unix-like systems
                config_dir = os.path.join(os.path.expanduser('~'), '.web_security_tool')
            self.config_file = os.path.join(config_dir, 'config.json')
        else:
            self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                # Corrupt or unreadable config; fall back to defaults
                return self.get_default_config()
        return self.get_default_config()

    def get_default_config(self):
        """Get default configuration."""
        return {
            'user_name': 'Md. Jony Hassain',
            'organization': 'HexaCyberLab Web Agency',
            'output_dir': os.getcwd(),
            'pdf_theme': 'professional',
            'command_timeout': 30,
            'max_workers': 3,
            'export_formats': ['json', 'pdf', 'csv'],
            'session_recording': {
                'auto_save': True,
                'max_commands': 5000,
                'truncate_output': 1600,
                'enable_screenshots': True,
                'screenshot_dir': 'screenshots',
                'screenshot_format': 'png'
            }
        }

    def save_config(self):
        """Save current configuration to file."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key, default=None):
        """Get configuration value."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set configuration value."""
        self.config[key] = value
        self.save_config()

    def update_from_args(self, args):
        """Update config from command line arguments."""
        self.config.setdefault('session_recording', self.get_default_config()['session_recording'])
        if hasattr(args, 'user_name') and args.user_name:
            self.config['user_name'] = args.user_name
        if hasattr(args, 'organization') and args.organization:
            self.config['organization'] = args.organization
        if hasattr(args, 'output_dir') and args.output_dir:
            self.config['output_dir'] = args.output_dir
        if hasattr(args, 'timeout') and args.timeout:
            self.config['command_timeout'] = args.timeout
        if hasattr(args, 'enable_screenshots') and args.enable_screenshots:
            self.config['session_recording']['enable_screenshots'] = True
        if hasattr(args, 'disable_screenshots') and args.disable_screenshots:
            self.config['session_recording']['enable_screenshots'] = False
        if hasattr(args, 'screenshot_dir') and args.screenshot_dir:
            self.config['session_recording']['screenshot_dir'] = args.screenshot_dir

    def resolve_output_dir(self):
        """Return an existing output directory, creating it if needed."""
        output_dir = Path(self.config.get('output_dir', os.getcwd())).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir)
