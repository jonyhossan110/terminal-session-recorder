#!/usr/bin/env python3
"""Web Dashboard Server for TSR"""

import asyncio
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from pathlib import Path

from tsr.core.config import Config
from tsr.core.database import SessionDatabase


app = Flask(__name__)
app.config['SECRET_KEY'] = 'tsr-secret-key-change-me'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
active_sessions = {}
db = None
config = None


@app.route('/')
def index():
    """Dashboard home page"""
    return render_template('dashboard.html')


@app.route('/api/sessions')
async def get_sessions():
    """Get all sessions"""
    async with SessionDatabase(config.database.path) as db:
        sessions = await db.search_sessions(limit=100)
        return jsonify(sessions)


@app.route('/api/sessions/<session_id>')
async def get_session_detail(session_id):
    """Get session details"""
    async with SessionDatabase(config.database.path) as db:
        session = await db.get_session(session_id)
        commands = await db.get_commands(session_id)
        
        return jsonify({
            'session': session,
            'commands': commands
        })


@app.route('/api/sessions/<session_id>/stats')
async def get_session_stats(session_id):
    """Get session statistics"""
    async with SessionDatabase(config.database.path) as db:
        stats = await db.get_statistics(session_id)
        return jsonify(stats)


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to TSR server'})


@socketio.on('subscribe_session')
def handle_subscribe(data):
    """Subscribe to real-time session updates"""
    session_id = data.get('session_id')
    if session_id:
        # Join room for this session
        from flask_socketio import join_room
        join_room(session_id)
        emit('subscribed', {'session_id': session_id})


def broadcast_command(session_id, command_data):
    """Broadcast new command to subscribed clients"""
    socketio.emit('new_command', command_data, room=session_id)


def main():
    """Start web server"""
    global config, db
    
    config = Config()
    
    print("""
╔═══════════════════════════════════════════╗
║   TSR Web Dashboard Server                ║
║   Terminal Session Recorder v2.0.0        ║
╚═══════════════════════════════════════════╝

Server starting on http://localhost:5000
    """)
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()
