#!/usr/bin/env python3
"""Advanced Configuration Manager with YAML/JSON support and validation"""

import json
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class SessionConfig:
    """Session recording configuration"""
    auto_save: bool = True
    max_commands: int = 10000
    truncate_output: int = 5000
    enable_screenshots: bool = True
    enable_video: bool = False
    screenshot_dir: str = "screenshots"
    video_dir: str = "videos"
    screenshot_format: str = "png"
    command_timeout: int = 300


@dataclass
class DatabaseConfig:
    """Database configuration"""
    backend: str = "sqlite"  # sqlite, postgresql
    path: str = "sessions.db"
    host: str = "localhost"
    port: int = 5432
    username: str = ""
    password: str = ""
    database: str = "tsr"


@dataclass
class MonitoringConfig:
    """System monitoring configuration"""
    enable_network: bool = False
    enable_strace: bool = False
    enable_resources: bool = True
    network_interface: str = "any"
    pcap_dir: str = "captures"


@dataclass
class ExportConfig:
    """Export configuration"""
    formats: list = field(default_factory=lambda: ["json", "pdf", "html", "csv"])
    pdf_theme: str = "professional"
    html_template: str = "default"
    compress_exports: bool = False


@dataclass
class CloudConfig:
    """Cloud storage configuration"""
    enabled: bool = False
    provider: str = "none"  # s3, gcs, dropbox
    bucket: str = ""
    access_key: str = ""
    secret_key: str = ""
    auto_upload: bool = False


@dataclass
class SecurityConfig:
    """Security configuration"""
    enable_encryption: bool = False
    enable_hashing: bool = True
    enable_signing: bool = False
    hash_algorithm: str = "sha256"
    redact_passwords: bool = True
    redact_tokens: bool = True


@dataclass
class PluginConfig:
    """Plugin configuration"""
    enabled_plugins: list = field(default_factory=list)
    plugin_dir: str = "~/.tsr/plugins"


class Config:
    """Advanced configuration manager with validation and persistence"""

    DEFAULT_CONFIG_LOCATIONS = [
        "~/.tsr/config.yaml",
        "~/.tsr/config.json",
        "/etc/tsr/config.yaml",
        "./tsr.yaml",
        "./tsr.json",
    ]

    def __init__(self, config_file: Optional[str] = None):
        self.config_file = self._find_config_file(config_file)
        self.user_name = "Md. Jony Hassain"
        self.organization = "HexaCyberLab Web Agency"
        self.output_dir = os.getcwd()
        
        # Initialize sub-configurations
        self.session = SessionConfig()
        self.database = DatabaseConfig()
        self.monitoring = MonitoringConfig()
        self.export = ExportConfig()
        self.cloud = CloudConfig()
        self.security = SecurityConfig()
        self.plugins = PluginConfig()
        
        # Load configuration if file exists
        if self.config_file and os.path.exists(self.config_file):
            self.load()

    def _find_config_file(self, config_file: Optional[str]) -> Optional[str]:
        """Find configuration file from default locations"""
        if config_file:
            return os.path.expanduser(config_file)
        
        for location in self.DEFAULT_CONFIG_LOCATIONS:
            path = Path(os.path.expanduser(location))
            if path.exists():
                return str(path)
        
        return None

    def load(self, config_file: Optional[str] = None) -> None:
        """Load configuration from file"""
        file_path = config_file or self.config_file
        if not file_path or not os.path.exists(file_path):
            return
        
        with open(file_path, 'r') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        
        self._apply_config(data)

    def _apply_config(self, data: Dict[str, Any]) -> None:
        """Apply configuration data to config objects"""
        # Top-level settings
        self.user_name = data.get('user_name', self.user_name)
        self.organization = data.get('organization', self.organization)
        self.output_dir = data.get('output_dir', self.output_dir)
        
        # Sub-configurations
        if 'session' in data:
            for key, value in data['session'].items():
                if hasattr(self.session, key):
                    setattr(self.session, key, value)
        
        if 'database' in data:
            for key, value in data['database'].items():
                if hasattr(self.database, key):
                    setattr(self.database, key, value)
        
        if 'monitoring' in data:
            for key, value in data['monitoring'].items():
                if hasattr(self.monitoring, key):
                    setattr(self.monitoring, key, value)
        
        if 'export' in data:
            for key, value in data['export'].items():
                if hasattr(self.export, key):
                    setattr(self.export, key, value)
        
        if 'cloud' in data:
            for key, value in data['cloud'].items():
                if hasattr(self.cloud, key):
                    setattr(self.cloud, key, value)
        
        if 'security' in data:
            for key, value in data['security'].items():
                if hasattr(self.security, key):
                    setattr(self.security, key, value)
        
        if 'plugins' in data:
            for key, value in data['plugins'].items():
                if hasattr(self.plugins, key):
                    setattr(self.plugins, key, value)

    def save(self, config_file: Optional[str] = None) -> None:
        """Save configuration to file"""
        file_path = config_file or self.config_file
        if not file_path:
            # Create default config location
            config_dir = Path.home() / '.tsr'
            config_dir.mkdir(exist_ok=True)
            file_path = str(config_dir / 'config.yaml')
            self.config_file = file_path
        
        data = self.to_dict()
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(data, f, indent=2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'user_name': self.user_name,
            'organization': self.organization,
            'output_dir': self.output_dir,
            'session': asdict(self.session),
            'database': asdict(self.database),
            'monitoring': asdict(self.monitoring),
            'export': asdict(self.export),
            'cloud': asdict(self.cloud),
            'security': asdict(self.security),
            'plugins': asdict(self.plugins),
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation (e.g., 'session.auto_save')"""
        parts = key.split('.')
        obj = self
        
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return default
        
        return obj

    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot notation"""
        parts = key.split('.')
        obj = self
        
        for part in parts[:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return
        
        if hasattr(obj, parts[-1]):
            setattr(obj, parts[-1], value)

    def update_from_args(self, args) -> None:
        """Update configuration from command-line arguments"""
        if hasattr(args, 'user_name') and args.user_name:
            self.user_name = args.user_name
        if hasattr(args, 'organization') and args.organization:
            self.organization = args.organization
        if hasattr(args, 'output_dir') and args.output_dir:
            self.output_dir = args.output_dir
        if hasattr(args, 'timeout') and args.timeout:
            self.session.command_timeout = args.timeout
        if hasattr(args, 'enable_screenshots'):
            self.session.enable_screenshots = args.enable_screenshots
        if hasattr(args, 'enable_video'):
            self.session.enable_video = args.enable_video
        if hasattr(args, 'enable_network'):
            self.monitoring.enable_network = args.enable_network
        if hasattr(args, 'enable_strace'):
            self.monitoring.enable_strace = args.enable_strace

    def resolve_output_dir(self) -> str:
        """Resolve and create output directory"""
        output_dir = Path(self.output_dir).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir)

    def validate(self) -> bool:
        """Validate configuration"""
        # Add validation logic here
        if self.session.command_timeout <= 0:
            raise ValueError("command_timeout must be positive")
        
        if self.database.backend not in ['sqlite', 'postgresql']:
            raise ValueError("database backend must be 'sqlite' or 'postgresql'")
        
        return True


# Singleton instance
_config_instance = None


def get_config(config_file: Optional[str] = None) -> Config:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_file)
    return _config_instance
