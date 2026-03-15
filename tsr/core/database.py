#!/usr/bin/env python3
"""Asynchronous SQLite Database Manager for Session Data"""

import aiosqlite
import asyncio
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class CommandEntry:
    """Command entry data structure"""
    id: Optional[int] = None
    session_id: str = ""
    timestamp: str = ""
    command: str = ""
    command_type: str = "unknown"  # reconnaissance, exploitation, post-exploit, etc.
    return_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    duration_ms: int = 0
    screenshot_path: Optional[str] = None
    video_path: Optional[str] = None
    network_capture: Optional[str] = None
    hash: str = ""
    tags: str = ""  # JSON array of tags


@dataclass
class SessionMetadata:
    """Session metadata"""
    id: Optional[int] = None
    session_id: str = ""
    user_name: str = ""
    organization: str = ""
    start_time: str = ""
    end_time: Optional[str] = None
    duration_seconds: int = 0
    command_count: int = 0
    failed_commands: int = 0
    platform: str = ""
    hostname: str = ""
    ip_address: str = ""
    session_hash: str = ""
    tags: str = ""  # JSON array


class SessionDatabase:
    """Asynchronous SQLite database for session management"""

    SCHEMA_VERSION = 2

    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[aiosqlite.Connection] = None
        self._initialized = False

    async def connect(self) -> None:
        """Establish database connection"""
        if self._conn is None:
            self._conn = await aiosqlite.connect(str(self.db_path))
            self._conn.row_factory = aiosqlite.Row
            await self._initialize_schema()

    async def close(self) -> None:
        """Close database connection"""
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def _initialize_schema(self) -> None:
        """Initialize database schema"""
        if self._initialized:
            return

        async with self._conn.cursor() as cursor:
            # Sessions table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    user_name TEXT,
                    organization TEXT,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration_seconds INTEGER DEFAULT 0,
                    command_count INTEGER DEFAULT 0,
                    failed_commands INTEGER DEFAULT 0,
                    platform TEXT,
                    hostname TEXT,
                    ip_address TEXT,
                    session_hash TEXT,
                    tags TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Commands table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    command TEXT NOT NULL,
                    command_type TEXT DEFAULT 'unknown',
                    return_code INTEGER,
                    stdout TEXT,
                    stderr TEXT,
                    duration_ms INTEGER DEFAULT 0,
                    screenshot_path TEXT,
                    video_path TEXT,
                    network_capture TEXT,
                    hash TEXT,
                    tags TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            # Screenshots table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS screenshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    command_id INTEGER,
                    path TEXT NOT NULL,
                    label TEXT,
                    resolution TEXT,
                    captured_at TEXT NOT NULL,
                    hash TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                    FOREIGN KEY (command_id) REFERENCES commands(id)
                )
            """)

            # Network captures table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS network_captures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    command_id INTEGER,
                    pcap_path TEXT NOT NULL,
                    interface TEXT,
                    packet_count INTEGER DEFAULT 0,
                    captured_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                    FOREIGN KEY (command_id) REFERENCES commands(id)
                )
            """)

            # System events table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    command_id INTEGER,
                    event_type TEXT NOT NULL,
                    event_data TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                    FOREIGN KEY (command_id) REFERENCES commands(id)
                )
            """)

            # Tags table (for better querying)
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    category TEXT,
                    description TEXT
                )
            """)

            # Create indices for faster queries
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_commands_session ON commands(session_id)")
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_commands_timestamp ON commands(timestamp)")
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_commands_type ON commands(command_type)")
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_start ON sessions(start_time)")
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_screenshots_session ON screenshots(session_id)")

            await self._conn.commit()
            self._initialized = True

    async def create_session(self, metadata: SessionMetadata) -> str:
        """Create a new session"""
        if not self._conn:
            await self.connect()

        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO sessions (
                    session_id, user_name, organization, start_time, platform, 
                    hostname, ip_address, session_hash, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                metadata.session_id,
                metadata.user_name,
                metadata.organization,
                metadata.start_time,
                metadata.platform,
                metadata.hostname,
                metadata.ip_address,
                metadata.session_hash,
                metadata.tags,
            ))
            await self._conn.commit()
            return metadata.session_id

    async def update_session(self, session_id: str, **kwargs) -> None:
        """Update session metadata"""
        if not self._conn:
            await self.connect()

        # Build UPDATE query dynamically
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)
        
        if not fields:
            return

        fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(session_id)

        query = f"UPDATE sessions SET {', '.join(fields)} WHERE session_id = ?"
        
        async with self._conn.cursor() as cursor:
            await cursor.execute(query, values)
            await self._conn.commit()

    async def add_command(self, entry: CommandEntry) -> int:
        """Add command entry to database"""
        if not self._conn:
            await self.connect()

        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO commands (
                    session_id, timestamp, command, command_type, return_code,
                    stdout, stderr, duration_ms, screenshot_path, video_path,
                    network_capture, hash, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.session_id,
                entry.timestamp,
                entry.command,
                entry.command_type,
                entry.return_code,
                entry.stdout,
                entry.stderr,
                entry.duration_ms,
                entry.screenshot_path,
                entry.video_path,
                entry.network_capture,
                entry.hash,
                entry.tags,
            ))
            await self._conn.commit()
            return cursor.lastrowid

    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session metadata"""
        if not self._conn:
            await self.connect()

        async with self._conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def get_commands(self, session_id: str, limit: int = None) -> List[Dict[str, Any]]:
        """Get all commands for a session"""
        if not self._conn:
            await self.connect()

        query = "SELECT * FROM commands WHERE session_id = ? ORDER BY timestamp"
        if limit:
            query += f" LIMIT {limit}"

        async with self._conn.cursor() as cursor:
            await cursor.execute(query, (session_id,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def search_sessions(
        self,
        user_name: Optional[str] = None,
        organization: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Search sessions with filters"""
        if not self._conn:
            await self.connect()

        query = "SELECT * FROM sessions WHERE 1=1"
        params = []

        if user_name:
            query += " AND user_name = ?"
            params.append(user_name)
        
        if organization:
            query += " AND organization = ?"
            params.append(organization)
        
        if start_date:
            query += " AND start_time >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND start_time <= ?"
            params.append(end_date)
        
        if tags:
            # Simple tag search (can be improved with JSON queries)
            for tag in tags:
                query += " AND tags LIKE ?"
                params.append(f"%{tag}%")

        query += " ORDER BY start_time DESC LIMIT ?"
        params.append(limit)

        async with self._conn.cursor() as cursor:
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def search_commands(
        self,
        session_id: Optional[str] = None,
        command_type: Optional[str] = None,
        search_text: Optional[str] = None,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """Search commands with filters"""
        if not self._conn:
            await self.connect()

        query = "SELECT * FROM commands WHERE 1=1"
        params = []

        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        
        if command_type:
            query += " AND command_type = ?"
            params.append(command_type)
        
        if search_text:
            query += " AND (command LIKE ? OR stdout LIKE ?)"
            params.append(f"%{search_text}%")
            params.append(f"%{search_text}%")

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        async with self._conn.cursor() as cursor:
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def get_statistics(self, session_id: str) -> Dict[str, Any]:
        """Get session statistics"""
        if not self._conn:
            await self.connect()

        async with self._conn.cursor() as cursor:
            # Command type distribution
            await cursor.execute("""
                SELECT command_type, COUNT(*) as count
                FROM commands
                WHERE session_id = ?
                GROUP BY command_type
            """, (session_id,))
            type_distribution = {row['command_type']: row['count'] for row in await cursor.fetchall()}

            # Success/failure stats
            await cursor.execute("""
                SELECT 
                    SUM(CASE WHEN return_code = 0 THEN 1 ELSE 0 END) as success_count,
                    SUM(CASE WHEN return_code != 0 THEN 1 ELSE 0 END) as failure_count,
                    AVG(duration_ms) as avg_duration
                FROM commands
                WHERE session_id = ?
            """, (session_id,))
            stats = dict(await cursor.fetchone())

            return {
                'type_distribution': type_distribution,
                **stats
            }

    async def delete_session(self, session_id: str) -> None:
        """Delete a session and all related data"""
        if not self._conn:
            await self.connect()

        async with self._conn.cursor() as cursor:
            await cursor.execute("DELETE FROM commands WHERE session_id = ?", (session_id,))
            await cursor.execute("DELETE FROM screenshots WHERE session_id = ?", (session_id,))
            await cursor.execute("DELETE FROM network_captures WHERE session_id = ?", (session_id,))
            await cursor.execute("DELETE FROM system_events WHERE session_id = ?", (session_id,))
            await cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            await self._conn.commit()

    async def vacuum(self) -> None:
        """Optimize database"""
        if not self._conn:
            await self.connect()
        
        await self._conn.execute("VACUUM")
        await self._conn.commit()

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
