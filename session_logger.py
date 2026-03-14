#!/usr/bin/env python3
"""Terminal Session Recorder

High-speed, cross-platform terminal session recorder that streams command output in real time
while persisting JSON/CSV logs and a professional PDF report.
"""

import csv
import json
import os
import signal
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import List

try:
    from PIL import Image
except ImportError:
    Image = None

import ctypes
from ctypes import wintypes

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image as RLImage
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


def get_terminal_window_rect():
    """Get the rectangle of the current terminal/console window in pixels."""
    # For VS Code integrated terminal, GetConsoleWindow may not work properly
    # Return None to use fallback capture of bottom screen portion
    return None


class TerminalSessionRecorder:
    """High-speed terminal session recorder with streaming output and multi-format exports."""

    def __init__(self, output_prefix=None, output_dir=None, user_name=None, config=None, timeout=None):
        self.config = config or {}
        session_cfg = self.config.get('session_recording', {})

        self.output_dir = output_dir or self.config.get('output_dir') or os.getcwd()
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        self.output_prefix = output_prefix or f"terminal_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        default_name = self.config.get('user_name', 'cmd')
        self.user_name = (user_name or default_name).strip() or "cmd"
        self.organization = self.config.get('organization', '')
        self.timeout = timeout or self.config.get('command_timeout', 30)
        self.max_commands = session_cfg.get('max_commands', 5000)
        self.truncate_chars = session_cfg.get('truncate_output', 1600)
        self.auto_save = session_cfg.get('auto_save', True)
        self.enable_screens = session_cfg.get('enable_screenshots', False)
        self.screenshot_dir = str(Path(self.output_dir) / session_cfg.get('screenshot_dir', 'screenshots'))
        self.screenshot_format = session_cfg.get('screenshot_format', 'png')
        self.export_formats = set(self.config.get('export_formats', ['json', 'pdf', 'csv']))

        self.start_time = datetime.now()
        self.commands = []
        self.screenshots = []
        self.json_file = os.path.join(self.output_dir, f"{self.output_prefix}.json")
        self.pdf_file = os.path.join(self.output_dir, f"{self.output_prefix}.pdf")
        self.csv_file = os.path.join(self.output_dir, f"{self.output_prefix}.csv")
        self._saved = False
        if self.enable_screens:
            Path(self.screenshot_dir).mkdir(parents=True, exist_ok=True)
        self._register_signal_handlers()

    # ------------------------------------------------------------------ lifecycle helpers
    def _register_signal_handlers(self):
        try:
            signal.signal(signal.SIGINT, self._handle_signal)
            signal.signal(signal.SIGTERM, self._handle_signal)
        except (ValueError, OSError, AttributeError):
            # Some platforms (notably Windows) may not support all signals
            pass

    def _handle_signal(self, signum, frame):  # pragma: no cover - signal handlers are hard to unit test
        self.log(f"\nSession ended (signal {signum}). Saving report...")
        self.save_report()
        sys.exit(0)

    # ------------------------------------------------------------------ utilities
    def log(self, message: str):
        """Lightweight logger; keep prints minimal to avoid slowing the shell."""
        print(message)

    def _truncate(self, text: str, max_chars: int = None) -> str:
        max_chars = max_chars or self.truncate_chars
        if not text:
            return ""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n...[truncated]"

    def _capture_stream(self, stream, buffer: List[str], writer):
        """Drain a stream to both console and in-memory buffer."""
        for line in iter(stream.readline, ''):
            buffer.append(line)
            writer.write(line)
            writer.flush()
        stream.close()

    def _execute_command(self, command: str) -> dict:
        entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'command',
            'command': command,
            'return_code': None,
            'stdout': '',
            'stderr': '',
        }

        try:
            proc = subprocess.Popen(
                command,
                shell=True,                # Windows compatibility; caller controls input
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            stdout_lines: List[str] = []
            stderr_lines: List[str] = []

            threads = [
                threading.Thread(target=self._capture_stream, args=(proc.stdout, stdout_lines, sys.stdout), daemon=True),
                threading.Thread(target=self._capture_stream, args=(proc.stderr, stderr_lines, sys.stderr), daemon=True),
            ]
            for t in threads:
                t.start()

            try:
                proc.wait(timeout=self.timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                entry['return_code'] = -1
                entry['stderr'] = f"Command timed out after {self.timeout}s"
                return entry

            for t in threads:
                t.join(timeout=1)

            entry['return_code'] = proc.returncode
            entry['stdout'] = ''.join(stdout_lines)
            entry['stderr'] = ''.join(stderr_lines)
        except Exception as exc:
            entry['return_code'] = -1
            entry['stderr'] = str(exc)

        return entry

    def _capture_screenshot(self, label: str = None):
        if not self.enable_screens:
            self.log("[info] Screenshots disabled. Run with --enable-screenshots to enable.")
            return None
        try:
            import mss
            from mss import tools
        except ImportError:
            self.log("[warn] Screenshot support requires the 'mss' package. Install it to enable captures.")
            return None

        Path(self.screenshot_dir).mkdir(parents=True, exist_ok=True)
        idx = len(self.screenshots) + 1
        safe_label = (label or "shot").replace(" ", "_")
        filename = f"{self.output_prefix}_shot{idx:03d}_{safe_label}.{self.screenshot_format}"
        path = Path(self.screenshot_dir) / filename

        # Get terminal window rect
        terminal_rect = get_terminal_window_rect()
        if terminal_rect and terminal_rect['width'] > 200 and terminal_rect['height'] > 100:
            # Use the calculated rect if it seems reasonable
            monitor = {
                'left': max(0, terminal_rect['left']),
                'top': max(0, terminal_rect['top']),
                'width': min(terminal_rect['width'], 1920),  # Cap width
                'height': min(terminal_rect['height'], 1080)  # Cap height
            }
        else:
            # Full screen capture
            with mss.mss() as sct:
                screen = sct.monitors[1]
                monitor = {
                    'left': 0,
                    'top': 0,
                    'width': screen['width'],
                    'height': screen['height']
                }

        with mss.mss() as sct:
            img = sct.grab(monitor)
            tools.to_png(img.rgb, img.size, output=str(path))
            resolution = f"{img.width}x{img.height}"

        record = {
            'label': label or f"Screenshot {idx}",
            'path': str(path),
            'captured_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'resolution': resolution,
        }
        self.screenshots.append(record)
        self.log(f"[ok] Full screenshot captured: {path} ({resolution})")
        return record

    def _record_entry(self, entry: dict):
        entry['stdout'] = self._truncate(entry.get('stdout', ''))
        entry['stderr'] = self._truncate(entry.get('stderr', ''))
        self.commands.append(entry)
        if len(self.commands) > self.max_commands:
            # Keep the most recent commands to cap memory usage
            self.commands = self.commands[-self.max_commands:]

        # Capture a screenshot for each command if enabled
        if self.enable_screens and entry.get('type') == 'command':
            try:
                # Wait a bit for the output to be displayed in the terminal
                time.sleep(1.0)
                shot = self._capture_screenshot(label=entry.get('command'))
                if shot:
                    entry['screenshot'] = shot
            except Exception as exc:
                self.log(f"[warn] Screenshot capture failed: {exc}")

        if self.auto_save:
            self._write_partial_json()

    def _write_partial_json(self):
        """Persist a partial log after each command to avoid data loss on crash."""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self._build_report(include_end=False), f, indent=2, ensure_ascii=False)
        except Exception:
            # Do not interrupt the interactive session for transient disk errors
            pass

    def _build_report(self, include_end: bool = True) -> dict:
        end_time = datetime.now()
        command_entries = [c for c in self.commands if c.get('type', 'command') == 'command']
        return {
            'session_start': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'session_end': end_time.strftime('%Y-%m-%d %H:%M:%S') if include_end else None,
            'duration_seconds': int((end_time - self.start_time).total_seconds()),
            'command_count': len(command_entries),
            'failed_commands': sum(1 for c in command_entries if c.get('return_code', 0) != 0),
            'commands': self.commands,
            'screenshots': self.screenshots,
        }

    # ------------------------------------------------------------------ main loop
    def run(self):
        self.log("[start] Terminal session recorder ready.")
        if self.enable_screens:
            self.log("[info] Screenshots enabled - images will be captured after each command and embedded in the PDF.")
        self.log("Type 'exit' or 'quit' to end the session and generate the report.\n")

        try:
            while True:
                try:
                    command = input(f'{self.user_name}> ').strip()
                except EOFError:
                    self.log('\nSession ended (EOF).')
                    break

                if not command:
                    continue

                if command.lower() in ('exit', 'quit'):
                    self.log('Session ended by user.')
                    break

                if command.lower().startswith((':snap', ':screenshot')):
                    label = command.partition(' ')[2].strip() or None
                    shot = self._capture_screenshot(label)
                    if shot:
                        meta_entry = {
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'type': 'screenshot',
                            'command': command,
                            'path': shot['path'],
                            'label': shot['label'],
                            'resolution': shot['resolution'],
                        }
                        self.commands.append(meta_entry)
                        if self.auto_save:
                            self._write_partial_json()
                    continue

                entry = self._execute_command(command)
                self._record_entry(entry)

        except KeyboardInterrupt:
            self.log('\nSession ended (KeyboardInterrupt).')

        finally:
            self.save_report()

    # ------------------------------------------------------------------ exports
    def save_report(self):
        if self._saved:
            return
        self._saved = True

        report = self._build_report()

        if 'json' in self.export_formats:
            try:
                with open(self.json_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                self.log(f"[ok] Session log saved to {self.json_file}")
            except Exception:
                self.log("[warn] Failed to save JSON log.")
                self.log(traceback.format_exc())

        if 'csv' in self.export_formats:
            try:
                self.export_csv(report)
                self.log(f"[ok] CSV export saved to {self.csv_file}")
            except Exception:
                self.log("[warn] Failed to export CSV.")
                self.log(traceback.format_exc())

        if 'pdf' in self.export_formats:
            try:
                self.generate_pdf_report(report)
                self.log(f"[ok] PDF report saved to {self.pdf_file}")
            except Exception:
                self.log("[warn] Failed to generate PDF report.")
                self.log(traceback.format_exc())

    def generate_pdf_report(self, report):
        doc = SimpleDocTemplate(
            self.pdf_file,
            pagesize=letter,
            topMargin=1.0 * inch,
            bottomMargin=1.0 * inch,
            leftMargin=1.0 * inch,
            rightMargin=1.0 * inch,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'Title', parent=styles['Title'], fontSize=26, textColor=HexColor('#1B4F72'), alignment=1, spaceAfter=24
        )
        subtitle_style = ParagraphStyle(
            'Subtitle', parent=styles['Heading2'], fontSize=14, textColor=HexColor('#2E86AB'), alignment=1, spaceAfter=18
        )
        normal = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, spaceAfter=8)
        heading = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=HexColor('#1B4F72'), spaceAfter=6)
        code = ParagraphStyle('Code', parent=styles['Code'], fontSize=8, leading=10)
        code_emphasis = ParagraphStyle('CodeEmphasis', parent=styles['Code'], fontSize=9, leading=11, textColor=HexColor('#1B4F72'))

        def header_footer(canvas, doc_obj):
            canvas.saveState()
            width, height = doc_obj.pagesize
            canvas.setFont('Helvetica-Bold', 9)
            canvas.setFillColor(HexColor('#1B4F72'))
            title_line = "Md. Jony Hassain | HexaCyberLab Web Agency"
            canvas.drawString(doc_obj.leftMargin, height - 0.75 * inch, title_line)
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.grey)
            canvas.drawRightString(width - doc_obj.rightMargin, height - 0.75 * inch, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            canvas.setFont('Helvetica', 8)
            footer_line = f"Generated by: {self.user_name}"
            canvas.drawString(doc_obj.leftMargin, 0.75 * inch, footer_line)
            canvas.drawRightString(width - doc_obj.rightMargin, 0.75 * inch, f"Page {canvas.getPageNumber()}")

            # Add watermark
            try:
                logo_path = os.path.join(os.path.dirname(__file__), 'hexacyberlab-logo.png')
                if os.path.exists(logo_path):
                    canvas.setFillAlpha(0.1)  # Semi-transparent
                    canvas.drawImage(logo_path, width/2 - 1*inch, height/2 - 1*inch, width=2*inch, height=2*inch, mask='auto')
                    canvas.setFillAlpha(1.0)  # Reset alpha
            except Exception:
                pass  # Silently ignore if logo can't be loaded

            canvas.restoreState()

        story = []

        # Cover Page
        story.append(Paragraph('Terminal Session Report', title_style))
        story.append(Paragraph(f"Recorded By: <b>{self.user_name}</b>", subtitle_style))
        if self.organization:
            story.append(Paragraph(f"Organization: <b>{self.organization}</b>", normal))
        story.append(Paragraph(f"Session Start: <b>{report['session_start']}</b>", normal))
        story.append(Paragraph(f"Session End: <b>{report['session_end']}</b>", normal))
        story.append(Paragraph(f"Total Commands: <b>{report['command_count']}</b>", normal))
        story.append(Paragraph(f"Failed Commands: <b>{report['failed_commands']}</b>", normal))
        story.append(Paragraph(f"Duration (seconds): <b>{report['duration_seconds']}</b>", normal))
        story.append(Spacer(1, 18))
        story.append(Paragraph('Notes:', heading))
        story.append(Paragraph('This report captures all executed commands and their outputs during the recorded session. The logs are intended for audit, troubleshooting, and documentation.', normal))
        story.append(PageBreak())

        # Table of Contents
        story.append(Paragraph('Table of Contents', heading))
        toc_entries = []
        for idx, entry in enumerate(report['commands'], start=1):
            toc_entries.append(f"{idx}. {entry['command'][:80]}{'...' if len(entry['command']) > 80 else ''}")
        toc_text = '<br/>'.join(toc_entries) if toc_entries else 'No commands recorded.'
        story.append(Paragraph(toc_text, normal))
        story.append(PageBreak())

        # Command log sections
        for idx, entry in enumerate(report['commands'], start=1):
            story.append(Paragraph(f"<b>{idx}. Command:</b> {entry['command']}", heading))
            story.append(Paragraph(f"<b>Timestamp:</b> {entry['timestamp']}", normal))
            story.append(Paragraph(f"<b>Return Code:</b> {entry.get('return_code')}", normal))

            if entry.get('type') == 'screenshot':
                story.append(Paragraph(f"<b>Screenshot Path:</b> {entry.get('path', '')}", normal))
                story.append(Paragraph(f"<b>Resolution:</b> {entry.get('resolution', '')}", normal))
                story.append(Spacer(1, 10))
                if idx % 5 == 0:
                    story.append(PageBreak())
                continue

            if entry.get('stdout'):
                story.append(Paragraph('<b>Output:</b>', code_emphasis))
                story.append(Paragraph(entry['stdout'].replace('\n', '<br/>'), code))

            if entry.get('stderr'):
                story.append(Paragraph('<b>Error Output:</b>', code_emphasis))
                story.append(Paragraph(entry['stderr'].replace('\n', '<br/>'), ParagraphStyle('Error', parent=code, textColor=colors.red)))

            if entry.get('screenshot'):
                shot = entry['screenshot']
                story.append(Paragraph('<b>Screenshot captured:</b>', normal))
                story.append(Paragraph(f"{shot.get('label', '')} ({shot.get('resolution', '')})", normal))
                try:
                    if Image:
                        pil_img = Image.open(shot['path'])
                        iw, ih = pil_img.size
                        max_width = doc.width
                        scale = min(1.0, max_width / iw)
                        story.append(RLImage(pil_img, width=iw * scale, height=ih * scale))
                    else:
                        img = ImageReader(shot['path'])
                        iw, ih = img.getSize()
                        max_width = doc.width
                        scale = min(1.0, max_width / iw)
                        story.append(RLImage(shot['path'], width=iw * scale, height=ih * scale))
                except Exception:
                    story.append(Paragraph(f"[unable to render image: {shot.get('path', '')}]", normal))

            story.append(Spacer(1, 10))
            if idx % 5 == 0:
                story.append(PageBreak())

        if report.get('screenshots'):
            story.append(PageBreak())
            story.append(Paragraph('Screenshots', heading))
            for shot in report['screenshots']:
                story.append(Paragraph(f"{shot['label']} ({shot['resolution']}) — {shot['captured_at']}", normal))
                try:
                    if Image:
                        pil_img = Image.open(shot['path'])
                        iw, ih = pil_img.size
                        max_width = doc.width
                        scale = min(1.0, max_width / iw)
                        story.append(RLImage(pil_img, width=iw * scale, height=ih * scale))
                    else:
                        img = ImageReader(shot['path'])
                        iw, ih = img.getSize()
                        max_width = doc.width
                        scale = min(1.0, max_width / iw)
                        story.append(RLImage(shot['path'], width=iw * scale, height=ih * scale))
                except Exception:
                    story.append(Paragraph(f"[unable to render image: {shot['path']}]", normal))
                story.append(Spacer(1, 12))

        doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

    def export_csv(self, report):
        """Export session data to CSV format."""
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'command', 'return_code', 'stdout', 'stderr']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in report['commands']:
                writer.writerow({
                    'timestamp': entry.get('timestamp', ''),
                    'command': entry.get('command', ''),
                    'return_code': entry.get('return_code', ''),
                    'stdout': self._truncate(entry.get('stdout', '')) if entry.get('type') == 'command' else '',
                    'stderr': self._truncate(entry.get('stderr', '')) if entry.get('type') == 'command' else entry.get('resolution', '')
                })


if __name__ == '__main__':
    recorder = TerminalSessionRecorder()
    recorder.run()
