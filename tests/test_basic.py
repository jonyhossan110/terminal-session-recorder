#!/usr/bin/env python3
"""Basic tests for TSR"""

import pytest
from tsr import __version__
from tsr.core.config import Config
from tsr.core.classifier import get_classifier, CommandCategory


def test_version():
    """Test version is defined"""
    assert __version__ == "2.0.0"


def test_config_init():
    """Test config initialization"""
    config = Config()
    assert config.user_name is not None
    assert config.organization is not None


def test_classifier():
    """Test command classifier"""
    classifier = get_classifier()
    
    # Test nmap classification
    category, tags, confidence = classifier.classify("nmap -sV 192.168.1.1")
    assert category == CommandCategory.SCANNING
    assert confidence > 0.5
    
    # Test sqlmap classification
    category, tags, confidence = classifier.classify("sqlmap -u http://test.com --dbs")
    assert category == CommandCategory.EXPLOITATION
    
    # Test metasploit classification
    category, tags, confidence = classifier.classify("msfconsole")
    assert category == CommandCategory.EXPLOITATION


def test_config_persistence():
    """Test config save/load"""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_file = f.name
    
    try:
        # Create and save config
        config1 = Config(config_file)
        config1.user_name = "Test User"
        config1.save()
        
        # Load config
        config2 = Config(config_file)
        assert config2.user_name == "Test User"
    finally:
        if os.path.exists(config_file):
            os.unlink(config_file)


@pytest.mark.asyncio
async def test_database_operations():
    """Test database operations"""
    import tempfile
    from tsr.core.database import SessionDatabase, SessionMetadata, CommandEntry
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_file = f.name
    
    try:
        async with SessionDatabase(db_file) as db:
            # Create session
            metadata = SessionMetadata(
                session_id="test_session_001",
                user_name="Test User",
                start_time="2026-03-15T00:00:00"
            )
            await db.create_session(metadata)
            
            # Add command
            entry = CommandEntry(
                session_id="test_session_001",
                timestamp="2026-03-15T00:00:01",
                command="echo test",
                return_code=0,
                stdout="test\n"
            )
            cmd_id = await db.add_command(entry)
            assert cmd_id > 0
            
            # Retrieve session
            session = await db.get_session("test_session_001")
            assert session is not None
            assert session['user_name'] == "Test User"
            
            # Get commands
            commands = await db.get_commands("test_session_001")
            assert len(commands) == 1
            assert commands[0]['command'] == "echo test"
    finally:
        import os
        if os.path.exists(db_file):
            os.unlink(db_file)
