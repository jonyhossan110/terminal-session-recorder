#!/usr/bin/env python3
"""Input validation utilities"""

import re
from typing import Optional


def validate_session_id(session_id: str) -> bool:
    """Validate session ID format"""
    pattern = r'^[0-9]{8}_[0-9]{6}_[a-f0-9]{8}$'
    return bool(re.match(pattern, session_id))


def validate_command(command: str) -> bool:
    """Check if command is safe to execute"""
    if not command or not command.strip():
        return False
    
    # Block obviously dangerous commands
    dangerous_patterns = [
        r'rm\s+-rf\s+/',  # Recursive delete from root
        r':(){ :|:& };:',  # Fork bomb
        r'mkfs\.',  # Format filesystem
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, command):
            return False
    
    return True


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove dangerous characters
    sanitized = re.sub(r'[^\w\s-]', '', filename)
    sanitized = re.sub(r'[-\s]+', '-', sanitized)
    return sanitized[:255]  # Limit length


def redact_sensitive_data(text: str) -> str:
    """Redact passwords, tokens, and sensitive data"""
    # Redact password patterns
    text = re.sub(r'password[=:]\s*\S+', 'password=REDACTED', text, flags=re.IGNORECASE)
    text = re.sub(r'passwd[=:]\s*\S+', 'passwd=REDACTED', text, flags=re.IGNORECASE)
    
    # Redact API keys/tokens
    text = re.sub(r'(api[_-]?key|token)[=:]\s*[\w-]+', r'\1=REDACTED', text, flags=re.IGNORECASE)
    
    # Redact AWS keys
    text = re.sub(r'AKIA[0-9A-Z]{16}', 'AKIA_REDACTED', text)
    
    # Redact SSH private keys
    text = re.sub(r'-----BEGIN.*PRIVATE KEY-----.*?-----END.*PRIVATE KEY-----', 
                  'PRIVATE_KEY_REDACTED', text, flags=re.DOTALL)
    
    return text
