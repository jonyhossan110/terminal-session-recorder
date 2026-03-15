"""
Terminal Session Recorder v2.0.0
Enterprise-grade pentesting documentation tool

Author: Md. Jony Hassain
Organization: HexaCyberLab Web Agency
License: MIT
"""

__version__ = "2.0.0"
__author__ = "Md. Jony Hassain"
__email__ = "jonyhossan110@gmail.com"
__license__ = "MIT"

from tsr.core.recorder import SessionRecorder
from tsr.core.database import SessionDatabase
from tsr.core.config import Config

__all__ = [
    "SessionRecorder",
    "SessionDatabase",
    "Config",
    "__version__",
]
