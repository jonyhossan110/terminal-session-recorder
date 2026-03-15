#!/usr/bin/env python3
"""Output formatting utilities"""

from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel


console = Console()


def print_session_table(sessions: list):
    """Print sessions in a formatted table"""
    table = Table(title="Terminal Sessions")
    
    table.add_column("Session ID", style="cyan")
    table.add_column("User", style="magenta")
    table.add_column("Commands", justify="right", style="green")
    table.add_column("Duration", justify="right")
    table.add_column("Start Time", style="blue")
    
    for session in sessions:
        table.add_row(
            session['session_id'][:30],
            session['user_name'],
            str(session['command_count']),
            f"{session['duration_seconds']}s",
            session['start_time']
        )
    
    console.print(table)


def print_command_syntax(command: str, language: str = "bash"):
    """Print command with syntax highlighting"""
    syntax = Syntax(command, language, theme="monokai", line_numbers=False)
    console.print(syntax)


def print_success(message: str):
    """Print success message"""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str):
    """Print error message"""
    console.print(f"[red]✗[/red] {message}")


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_panel(title: str, content: str, style: str = "blue"):
    """Print content in a panel"""
    panel = Panel(content, title=title, border_style=style)
    console.print(panel)
