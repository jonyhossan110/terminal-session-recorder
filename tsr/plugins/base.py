#!/usr/bin/env python3
"""Base Plugin System"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BasePlugin(ABC):
    """Base class for TSR plugins"""
    
    def __init__(self, recorder):
        self.recorder = recorder
        self.config = recorder.config
        self.enabled = True
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""
        pass
    
    @abstractmethod
    async def on_session_start(self):
        """Called when session starts"""
        pass
    
    @abstractmethod
    async def on_command_execute(self, command: str) -> Dict[str, Any]:
        """Called before command execution"""
        pass
    
    @abstractmethod
    async def on_command_complete(self, command: str, result: Dict[str, Any]):
        """Called after command execution"""
        pass
    
    @abstractmethod
    async def on_session_end(self):
        """Called when session ends"""
        pass


class PluginManager:
    """Manage and execute plugins"""
    
    def __init__(self, recorder):
        self.recorder = recorder
        self.plugins = []
    
    def register(self, plugin: BasePlugin):
        """Register a plugin"""
        if plugin.enabled:
            self.plugins.append(plugin)
    
    async def on_session_start(self):
        """Trigger session start for all plugins"""
        for plugin in self.plugins:
            try:
                await plugin.on_session_start()
            except Exception as e:
                print(f"[Plugin:{plugin.name}] Error in on_session_start: {e}")
    
    async def on_command_execute(self, command: str) -> Dict[str, Any]:
        """Trigger command execute for all plugins"""
        metadata = {}
        for plugin in self.plugins:
            try:
                result = await plugin.on_command_execute(command)
                if result:
                    metadata[plugin.name] = result
            except Exception as e:
                print(f"[Plugin:{plugin.name}] Error in on_command_execute: {e}")
        return metadata
    
    async def on_command_complete(self, command: str, result: Dict[str, Any]):
        """Trigger command complete for all plugins"""
        for plugin in self.plugins:
            try:
                await plugin.on_command_complete(command, result)
            except Exception as e:
                print(f"[Plugin:{plugin.name}] Error in on_command_complete: {e}")
    
    async def on_session_end(self):
        """Trigger session end for all plugins"""
        for plugin in self.plugins:
            try:
                await plugin.on_session_end()
            except Exception as e:
                print(f"[Plugin:{plugin.name}] Error in on_session_end: {e}")
