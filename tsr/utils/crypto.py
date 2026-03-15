#!/usr/bin/env python3
"""Cryptographic utilities for evidence chain"""

import hashlib
import json
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


def compute_hash(data: str, algorithm: str = 'sha256') -> str:
    """Compute cryptographic hash of data"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if algorithm == 'sha256':
        return hashlib.sha256(data).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(data).hexdigest()
    elif algorithm == 'md5':
        return hashlib.md5(data).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def compute_command_hash(command: str, timestamp: str, output: str = "") -> str:
    """Compute hash for command entry (evidence chain)"""
    data = f"{command}|{timestamp}|{output}"
    return compute_hash(data)


def generate_session_hash(session_id: str, commands: list) -> str:
    """Generate hash for entire session"""
    command_hashes = [cmd.get('hash', '') for cmd in commands]
    data = f"{session_id}|{'|'.join(command_hashes)}"
    return compute_hash(data)


class SessionEncryption:
    """Encrypt/decrypt sensitive session data"""
    
    def __init__(self, password: str):
        self.password = password
        self.key = self._derive_key(password)
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'tsr_static_salt',  # In production, use random salt
            iterations=100000,
        )
        return kdf.derive(password.encode())
    
    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
