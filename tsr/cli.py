#!/usr/bin/env python3
"""
Terminal Session Recorder v2.0.0 - Main CLI Interface
Enterprise-grade pentesting documentation tool
"""

import asyncio
import sys
import click
import os
from pathlib import Path

from tsr import __version__
from tsr.core.config import Config
from tsr.core.database import SessionDatabase
from tsr.core.recorder import SessionRecorder


@click.group()
@click.version_option(version=__version__)
@click.option('--config', '-c', type=click.Path(), help='Config file path')
@click.pass_context
def cli(ctx, config):
    """Terminal Session Recorder - Enterprise pentesting documentation tool"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(config)


@cli.command()
@click.option('--user-name', '-u', help='User name for session')
@click.option('--organization', '-org', help='Organization name')
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory')
@click.option('--timeout', '-t', type=int, help='Command timeout (seconds)')
@click.option('--enable-screenshots/--no-screenshots', default=None, help='Enable/disable screenshots')
@click.option('--enable-video/--no-video', default=False, help='Enable video recording')
@click.option('--enable-network/--no-network', default=False, help='Enable network monitoring')
@click.option('--enable-strace/--no-strace', default=False, help='Enable system call tracing')
@click.option('--db-path', type=click.Path(), help='Database file path')
@click.pass_context
def record(ctx, user_name, organization, output_dir, timeout, enable_screenshots, 
           enable_video, enable_network, enable_strace, db_path):
    """Start interactive terminal session recording"""
    
    config = ctx.obj['config']
    
    # Update config from CLI args
    if user_name:
        config.user_name = user_name
    if organization:
        config.organization = organization
    if output_dir:
        config.output_dir = output_dir
    if timeout:
        config.session.command_timeout = timeout
    if enable_screenshots is not None:
        config.session.enable_screenshots = enable_screenshots
    if enable_video:
        config.session.enable_video = enable_video
    if enable_network:
        config.monitoring.enable_network = enable_network
    if enable_strace:
        config.monitoring.enable_strace = enable_strace
    
    # Initialize database
    db_file = db_path or config.database.path
    if output_dir:
        db_file = str(Path(output_dir) / 'sessions.db')
    
    # Run async recorder
    asyncio.run(_record_session(config, db_file))


async def _record_session(config: Config, db_path: str):
    """Async session recording"""
    async with SessionDatabase(db_path) as db:
        recorder = SessionRecorder(config, db)
        
        try:
            await recorder.start()
            await recorder.interactive_loop()
        except KeyboardInterrupt:
            click.echo("\n[TSR] Session interrupted by user")
        finally:
            await recorder.stop()
            
            # Generate reports
            click.echo("\n[TSR] Generating reports...")
            await _generate_reports(recorder, config)


async def _generate_reports(recorder, config):
    """Generate all configured report formats"""
    from tsr.exporters.pdf import PDFExporter
    from tsr.exporters.html import HTMLExporter
    from tsr.exporters.json_export import JSONExporter
    from tsr.exporters.csv_export import CSVExporter
    
    output_dir = Path(config.resolve_output_dir())
    session_id = recorder.session_id
    
    # Get session data
    session = await recorder.db.get_session(session_id)
    commands = await recorder.db.get_commands(session_id)
    
    # Export based on config
    if 'json' in config.export.formats:
        exporter = JSONExporter(config)
        path = await exporter.export(session, commands, output_dir / f"{session_id}.json")
        click.echo(f"[ok] JSON: {path}")
    
    if 'csv' in config.export.formats:
        exporter = CSVExporter(config)
        path = await exporter.export(session, commands, output_dir / f"{session_id}.csv")
        click.echo(f"[ok] CSV: {path}")
    
    if 'html' in config.export.formats:
        exporter = HTMLExporter(config)
        path = await exporter.export(session, commands, output_dir / f"{session_id}.html")
        click.echo(f"[ok] HTML: {path}")
    
    if 'pdf' in config.export.formats:
        exporter = PDFExporter(config)
        path = await exporter.export(session, commands, output_dir / f"{session_id}.pdf")
        click.echo(f"[ok] PDF: {path}")


@cli.command()
@click.argument('session_id', required=False)
@click.option('--limit', '-n', default=10, help='Number of sessions to show')
@click.option('--user', help='Filter by user')
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list(ctx, session_id, limit, user, format):
    """List recorded sessions"""
    config = ctx.obj['config']
    asyncio.run(_list_sessions(config, session_id, limit, user, format))


async def _list_sessions(config, session_id, limit, user, format):
    """List sessions from database"""
    async with SessionDatabase(config.database.path) as db:
        if session_id:
            # Show specific session
            session = await db.get_session(session_id)
            if session:
                if format == 'json':
                    import json
                    click.echo(json.dumps(session, indent=2))
                else:
                    click.echo(f"\nSession: {session['session_id']}")
                    click.echo(f"User: {session['user_name']}")
                    click.echo(f"Start: {session['start_time']}")
                    click.echo(f"Commands: {session['command_count']}")
            else:
                click.echo(f"Session not found: {session_id}")
        else:
            # List sessions
            sessions = await db.search_sessions(user_name=user, limit=limit)
            
            if format == 'json':
                import json
                click.echo(json.dumps(sessions, indent=2))
            else:
                click.echo(f"\nFound {len(sessions)} sessions:\n")
                click.echo(f"{'Session ID':<30} {'User':<20} {'Commands':<10} {'Start Time'}")
                click.echo("-" * 80)
                for s in sessions:
                    click.echo(
                        f"{s['session_id']:<30} {s['user_name']:<20} "
                        f"{s['command_count']:<10} {s['start_time']}"
                    )


@cli.command()
@click.argument('session_id')
@click.option('--format', type=click.Choice(['pdf', 'html', 'json', 'csv', 'all']), default='pdf')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.pass_context
def export(ctx, session_id, format, output):
    """Export session to various formats"""
    config = ctx.obj['config']
    asyncio.run(_export_session(config, session_id, format, output))


async def _export_session(config, session_id, format_type, output_path):
    """Export session data"""
    async with SessionDatabase(config.database.path) as db:
        session = await db.get_session(session_id)
        if not session:
            click.echo(f"Session not found: {session_id}")
            return
        
        commands = await db.get_commands(session_id)
        
        output_dir = Path(output_path).parent if output_path else Path(config.output_dir)
        
        formats_to_export = ['pdf', 'html', 'json', 'csv'] if format_type == 'all' else [format_type]
        
        for fmt in formats_to_export:
            if fmt == 'pdf':
                from tsr.exporters.pdf import PDFExporter
                exporter = PDFExporter(config)
                path = output_path or output_dir / f"{session_id}.pdf"
                await exporter.export(session, commands, path)
                click.echo(f"[ok] PDF exported: {path}")
            
            elif fmt == 'html':
                from tsr.exporters.html import HTMLExporter
                exporter = HTMLExporter(config)
                path = output_path or output_dir / f"{session_id}.html"
                await exporter.export(session, commands, path)
                click.echo(f"[ok] HTML exported: {path}")
            
            elif fmt == 'json':
                from tsr.exporters.json_export import JSONExporter
                exporter = JSONExporter(config)
                path = output_path or output_dir / f"{session_id}.json"
                await exporter.export(session, commands, path)
                click.echo(f"[ok] JSON exported: {path}")
            
            elif fmt == 'csv':
                from tsr.exporters.csv_export import CSVExporter
                exporter = CSVExporter(config)
                path = output_path or output_dir / f"{session_id}.csv"
                await exporter.export(session, commands, path)
                click.echo(f"[ok] CSV exported: {path}")


@cli.command()
@click.argument('session_id')
@click.option('--message', '-m', help='Custom message for LinkedIn post')
@click.option('--access-token', help='LinkedIn access token (or set LINKEDIN_ACCESS_TOKEN env var)')
@click.option('--dry-run/--no-dry-run', default=False, help='Show what would be posted without actually posting')
@click.pass_context
def linkedin(ctx, session_id, message, access_token, dry_run):
    """Share session summary on LinkedIn"""
    config = ctx.obj['config']
    asyncio.run(_share_linkedin(config, session_id, message, access_token, dry_run))


async def _share_linkedin(config, session_id, message, access_token, dry_run):
    """Share session summary on LinkedIn"""
    import requests
    import json
    from datetime import datetime
    
    # Get access token
    token = access_token or os.environ.get('LINKEDIN_ACCESS_TOKEN')
    if not token:
        click.echo("[error] LinkedIn access token required. Set LINKEDIN_ACCESS_TOKEN env var or use --access-token")
        click.echo("Get token from: https://developer.linkedin.com/docs/oauth2")
        return
    
    # Get session data
    async with SessionDatabase(config.database.path) as db:
        session = await db.get_session(session_id)
        if not session:
            click.echo(f"Session not found: {session_id}")
            return
        
        commands = await db.get_commands(session_id)
        stats = await db.get_statistics(session_id)
    
    # Generate post content
    duration = session.get('duration_seconds', 0)
    command_count = session.get('command_count', 0)
    failed_count = session.get('failed_commands', 0)
    
    # Create message
    if not message:
        message = f"""🔍 Terminal Session Recording - {session_id}

📊 Session Summary:
• Duration: {duration}s
• Commands: {command_count}
• Failed: {failed_count}
• User: {session.get('user_name', 'Unknown')}

#Pentesting #Security #TerminalRecording #TSR #CyberSecurity

Generated by Terminal Session Recorder v{__version__}
"""
    
    # LinkedIn API endpoints
    profile_url = "https://api.linkedin.com/v2/people/~"
    share_url = "https://api.linkedin.com/v2/shares"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    try:
        # Get profile info
        profile_response = requests.get(profile_url, headers=headers)
        if profile_response.status_code != 200:
            click.echo(f"[error] Failed to get LinkedIn profile: {profile_response.text}")
            return
        
        profile_data = profile_response.json()
        person_urn = profile_data.get('id')
        
        # Prepare share data
        share_data = {
            "owner": f"urn:li:person:{person_urn}",
            "text": {
                "text": message
            },
            "distribution": {
                "linkedInDistributionTarget": {}
            }
        }
        
        if dry_run:
            click.echo("[dry-run] Would post to LinkedIn:")
            click.echo("-" * 50)
            click.echo(message)
            click.echo("-" * 50)
            click.echo(f"Session ID: {session_id}")
            click.echo(f"Token: {token[:10]}...")
            return
        
        # Post to LinkedIn
        response = requests.post(share_url, headers=headers, json=share_data)
        
        if response.status_code == 201:
            click.echo("[ok] Successfully posted to LinkedIn!")
            click.echo(f"Session {session_id} shared with {len(message)} characters")
        else:
            click.echo(f"[error] Failed to post to LinkedIn: {response.status_code}")
            click.echo(f"Response: {response.text}")
            
    except Exception as e:
        click.echo(f"[error] LinkedIn API error: {e}")


@cli.command()
@click.option('--user', help='Filter by user')
@click.option('--command-type', help='Filter by command type')
@click.option('--search', help='Search in commands')
@click.option('--limit', '-n', default=50, help='Max results')
@click.pass_context
def search(ctx, user, command_type, search, limit):
    """Search commands across all sessions"""
    config = ctx.obj['config']
    asyncio.run(_search_commands(config, user, command_type, search, limit))


async def _search_commands(config, user, command_type, search_text, limit):
    """Search commands in database"""
    async with SessionDatabase(config.database.path) as db:
        commands = await db.search_commands(
            command_type=command_type,
            search_text=search_text,
            limit=limit
        )
        
        click.echo(f"\nFound {len(commands)} commands:\n")
        for cmd in commands:
            click.echo(f"[{cmd['timestamp']}] {cmd['command']}")
            if cmd['command_type'] != 'unknown':
                click.echo(f"  Type: {cmd['command_type']}")


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize TSR configuration"""
    config = ctx.obj['config']
    config_dir = Path.home() / '.tsr'
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / 'config.yaml'
    config.config_file = str(config_file)
    config.save()
    
    click.echo(f"[ok] Configuration initialized: {config_file}")
    click.echo("\nEdit the config file to customize settings.")


def main():
    """Main entry point"""
    try:
        cli(obj={})
    except Exception as e:
        click.echo(f"[error] {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
