#!/usr/bin/env python3
"""
Terminal Session Recorder
A professional tool for recording terminal sessions with command logging and PDF reports.
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description="Terminal Session Recorder - A professional tool for recording terminal sessions with command logging and PDF reports.")
    parser.add_argument("--record-session", action="store_true",
                        help="Start an interactive command session recorder that logs commands + outputs and saves a professional PDF report when finished.")
    parser.add_argument("--auto-shell", action="store_true",
                        help="Start an interactive shell and record all terminal output (useful for auto-recording new terminals via ~/.bashrc).")
    parser.add_argument("--user-name", help="Name to display in the session report (e.g., your name)")
    parser.add_argument("--organization", help="Organization or agency name to include in reports")
    parser.add_argument("-o", "--output", help="Output prefix for session files (optional)")
    parser.add_argument("--output-dir", help="Directory to write session artifacts (defaults to current working directory or config value)")
    parser.add_argument("--timeout", type=int, help="Per-command timeout in seconds (overrides config)")
    parser.add_argument("--enable-screenshots", action="store_true",
                        help="Allow in-session HD screenshot capture via :snap commands (requires mss+Pillow)")
    parser.add_argument("--disable-screenshots", action="store_true",
                        help="Disable automatic screenshot capture (overrides config default)")
    parser.add_argument("--screenshot-dir", help="Directory (relative or absolute) to store captured screenshots")
    args = parser.parse_args()

    if not args.record_session and not args.auto_shell:
        parser.error('Use --record-session or --auto-shell to start the terminal session recorder')

    from session_logger import TerminalSessionRecorder
    from config_manager import ConfigManager

    config = ConfigManager()
    config.update_from_args(args)

    recorder = TerminalSessionRecorder(
        output_prefix=(args.output or None),
        output_dir=config.resolve_output_dir(),
        user_name=config.get('user_name'),
        config=config.config,
        timeout=args.timeout
    )

    if args.auto_shell:
        recorder.run_shell()
    else:
        recorder.run()

if __name__ == "__main__":
    main()
