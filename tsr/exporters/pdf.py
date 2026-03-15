#!/usr/bin/env python3
"""PDF Report Exporter"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.colors import HexColor


class PDFExporter:
    def __init__(self, config):
        self.config = config
    
    async def export(self, session, commands, output_path):
        """Export session to PDF"""
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            topMargin=inch,
            bottomMargin=inch,
            leftMargin=inch,
            rightMargin=inch,
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=HexColor('#1f6feb'),
            spaceAfter=12
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#388bfd'),
            spaceAfter=6
        )
        
        # Title
        story.append(Paragraph("Terminal Session Report", title_style))
        story.append(Spacer(1, 12))
        
        # Metadata
        story.append(Paragraph(f"<b>Session ID:</b> {session['session_id']}", styles['Normal']))
        story.append(Paragraph(f"<b>User:</b> {session['user_name']}", styles['Normal']))
        if session.get('organization'):
            story.append(Paragraph(f"<b>Organization:</b> {session['organization']}", styles['Normal']))
        story.append(Paragraph(f"<b>Start Time:</b> {session['start_time']}", styles['Normal']))
        story.append(Paragraph(f"<b>Duration:</b> {session['duration_seconds']}s", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Statistics
        story.append(Paragraph("Session Statistics", heading_style))
        stats_data = [
            ['Metric', 'Value'],
            ['Total Commands', str(session['command_count'])],
            ['Failed Commands', str(session['failed_commands'])],
            ['Success Rate', f"{((session['command_count'] - session['failed_commands']) / max(session['command_count'], 1) * 100):.1f}%"],
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f6feb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f6f8fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(stats_table)
        story.append(PageBreak())
        
        # Commands
        story.append(Paragraph("Command Log", heading_style))
        story.append(Spacer(1, 12))
        
        for idx, cmd in enumerate(commands, 1):
            # Command header
            cmd_header = f"<b>{idx}. {cmd['command']}</b>"
            story.append(Paragraph(cmd_header, styles['Heading3']))
            story.append(Paragraph(f"<i>Type:</i> {cmd['command_type']} | <i>Time:</i> {cmd['timestamp']}", styles['Normal']))
            
            # Output
            if cmd.get('stdout'):
                story.append(Spacer(1, 6))
                output_text = cmd['stdout'][:1000].replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(f"<font face='Courier' size='8'>{output_text}</font>", styles['Code']))
            
            # Errors
            if cmd.get('stderr'):
                story.append(Spacer(1, 6))
                error_style = ParagraphStyle('Error', parent=styles['Code'], textColor=colors.red)
                error_text = cmd['stderr'][:500].replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(f"<font face='Courier' size='8'>{error_text}</font>", error_style))
            
            story.append(Spacer(1, 12))
            
            if idx % 10 == 0:
                story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        return output_path
