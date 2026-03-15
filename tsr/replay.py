#!/usr/bin/env python3
"""Session Replay Tool"""

import asyncio
import sys
import click
from datetime import datetime
from tsr.core.config import Config
from tsr.core.database import SessionDatabase


class SessionReplayer:
    """Replay recorded terminal session"""
    
    def __init__(self, session_id, db, speed=1.0):
        self.session_id = session_id
        self.db = db
        self.speed = speed
        self.session = None
        self.commands = []
    
    async def load(self):
        """Load session data"""
        self.session = await self.db.get_session(self.session_id)
        if not self.session:
            raise ValueError(f"Session not found: {self.session_id}")
        
        self.commands = await self.db.get_commands(self.session_id)
    
    async def replay(self, interactive=False):
        """Replay session with timing"""
        print(f"\n{'='*60}")
        print(f"Replaying session: {self.session_id}")
        print(f"User: {self.session['user_name']}")
        print(f"Commands: {len(self.commands)}")
        print(f"Speed: {self.speed}x")
        print(f"{'='*60}\n")
        
        if not self.commands:
            print("No commands to replay")
            return
        
        # Parse timestamps
        start_time = None
        
        for idx, cmd in enumerate(self.commands, 1):
            # Show command
            print(f"\n[{idx}/{len(self.commands)}] {cmd['command']}")
            print(f"Type: {cmd['command_type']} | Time: {cmd['timestamp']}")
            print("-" * 60)
            
            # Show output
            if cmd.get('stdout'):
                print(cmd['stdout'][:500])
            
            if cmd.get('stderr'):
                print(f"\n[ERROR] {cmd['stderr'][:500]}", file=sys.stderr)
            
            # Interactive mode
            if interactive:
                response = input("\n[Press Enter for next, 'q' to quit] ")
                if response.lower() == 'q':
                    break
            else:
                # Calculate delay based on original timing
                if start_time and idx < len(self.commands):
                    # Simple delay between commands
                    await asyncio.sleep(0.5 / self.speed)
        
        print(f"\n{'='*60}")
        print("Replay complete")
        print(f"{'='*60}\n")


@click.command()
@click.argument('session_id')
@click.option('--speed', '-s', default=1.0, help='Replay speed multiplier')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode (step through)')
@click.option('--db-path', help='Database path')
def main(session_id, speed, interactive, db_path):
    """Replay a recorded terminal session"""
    config = Config()
    db_file = db_path or config.database.path
    
    asyncio.run(_replay_session(session_id, db_file, speed, interactive))


async def _replay_session(session_id, db_path, speed, interactive):
    """Async replay wrapper"""
    async with SessionDatabase(db_path) as db:
        replayer = SessionReplayer(session_id, db, speed)
        await replayer.load()
        await replayer.replay(interactive)


if __name__ == '__main__':
    main()
