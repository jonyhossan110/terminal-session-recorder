#!/usr/bin/env python3
"""Screenshot Capture Module"""

import asyncio
from datetime import datetime
from pathlib import Path

try:
    import mss
    import mss.tools
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False


async def capture_screenshot(session_id, label, config):
    """Capture full screen screenshot"""
    if not MSS_AVAILABLE:
        raise ImportError("Screenshot support requires mss")
    
    # Setup screenshot directory
    screenshot_dir = Path(config.session.screenshot_dir)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_label = label.replace(' ', '_').replace('/', '_')[:50]
    filename = f"{session_id}_{timestamp}_{safe_label}.png"
    filepath = screenshot_dir / filename
    
    # Capture screenshot
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=str(filepath))
    
    return str(filepath)
