#!/usr/bin/env python3
"""HTML Interactive Report Exporter"""

import aiofiles
from jinja2 import Template


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TSR Report - {{ session.session_id }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
               background: #0d1117; color: #c9d1d9; line-height: 1.6; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
                 padding: 40px; border-radius: 10px; margin-bottom: 30px; }
        h1 { color: white; font-size: 2.5em; margin-bottom: 10px; }
        .meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px; margin: 30px 0; }
        .meta-card { background: #161b22; padding: 20px; border-radius: 8px;
                     border-left: 4px solid #388bfd; }
        .meta-label { color: #8b949e; font-size: 0.9em; margin-bottom: 5px; }
        .meta-value { font-size: 1.3em; font-weight: bold; color: #58a6ff; }
        .command-list { margin-top: 30px; }
        .command-item { background: #0d1117; border: 1px solid #30363d; 
                        border-radius: 6px; margin-bottom: 15px; overflow: hidden; }
        .command-header { background: #161b22; padding: 15px; cursor: pointer;
                          display: flex; justify-content: space-between; align-items: center; }
        .command-header:hover { background: #1c2128; }
        .command-text { font-family: 'Courier New', monospace; color: #79c0ff; }
        .command-type { background: #388bfd; color: white; padding: 4px 12px;
                        border-radius: 12px; font-size: 0.85em; }
        .command-body { padding: 20px; display: none; }
        .command-body.active { display: block; }
        .output { background: #0d1117; border: 1px solid #30363d; padding: 15px;
                  border-radius: 6px; font-family: 'Courier New', monospace;
                  font-size: 0.9em; white-space: pre-wrap; word-wrap: break-word; }
        .success { border-left: 4px solid #3fb950; }
        .error { border-left: 4px solid #f85149; }
        .filter-bar { background: #161b22; padding: 20px; border-radius: 8px;
                      margin-bottom: 20px; display: flex; gap: 15px; flex-wrap: wrap; }
        .filter-bar input, .filter-bar select { background: #0d1117; border: 1px solid #30363d;
                                                 color: #c9d1d9; padding: 10px; border-radius: 6px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px; margin-bottom: 30px; }
        .stat-box { background: #161b22; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 2.5em; font-weight: bold; color: #58a6ff; }
        .stat-label { color: #8b949e; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ Terminal Session Report</h1>
            <p style="color: #e6edf3;">Session ID: {{ session.session_id }}</p>
            <p style="color: #e6edf3;">{{ session.user_name }} • {{ session.organization }}</p>
        </header>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{{ session.command_count }}</div>
                <div class="stat-label">Total Commands</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{{ session.failed_commands }}</div>
                <div class="stat-label">Failed Commands</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{{ session.duration_seconds }}s</div>
                <div class="stat-label">Session Duration</div>
            </div>
        </div>

        <div class="filter-bar">
            <input type="text" id="searchBox" placeholder="Search commands..." onkeyup="filterCommands()">
            <select id="typeFilter" onchange="filterCommands()">
                <option value="">All Types</option>
                <option value="reconnaissance">Reconnaissance</option>
                <option value="exploitation">Exploitation</option>
                <option value="scanning">Scanning</option>
            </select>
        </div>

        <div class="command-list" id="commandList">
            {% for cmd in commands %}
            <div class="command-item {% if cmd.return_code == 0 %}success{% else %}error{% endif %}" data-type="{{ cmd.command_type }}">
                <div class="command-header" onclick="toggleCommand(this)">
                    <div>
                        <div class="command-text">$ {{ cmd.command }}</div>
                        <small style="color: #8b949e;">{{ cmd.timestamp }}</small>
                    </div>
                    <span class="command-type">{{ cmd.command_type }}</span>
                </div>
                <div class="command-body">
                    {% if cmd.stdout %}
                    <h4 style="color: #8b949e; margin-bottom: 10px;">Output:</h4>
                    <div class="output">{{ cmd.stdout }}</div>
                    {% endif %}
                    {% if cmd.stderr %}
                    <h4 style="color: #f85149; margin: 15px 0 10px;">Error:</h4>
                    <div class="output" style="border-color: #f85149;">{{ cmd.stderr }}</div>
                    {% endif %}
                    <div style="margin-top: 15px; color: #8b949e; font-size: 0.9em;">
                        Return Code: {{ cmd.return_code }} | Duration: {{ cmd.duration_ms }}ms
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        function toggleCommand(header) {
            const body = header.nextElementSibling;
            body.classList.toggle('active');
        }

        function filterCommands() {
            const search = document.getElementById('searchBox').value.toLowerCase();
            const type = document.getElementById('typeFilter').value;
            const items = document.querySelectorAll('.command-item');
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                const itemType = item.getAttribute('data-type');
                const matchSearch = text.includes(search);
                const matchType = !type || itemType === type;
                item.style.display = (matchSearch && matchType) ? 'block' : 'none';
            });
        }
    </script>
</body>
</html>
"""


class HTMLExporter:
    def __init__(self, config):
        self.config = config
        self.template = Template(HTML_TEMPLATE)
    
    async def export(self, session, commands, output_path):
        """Export session to interactive HTML"""
        html_content = self.template.render(
            session=session,
            commands=commands
        )
        
        async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
            await f.write(html_content)
        
        return output_path
