#!/usr/bin/env python3
"""Setup script for Terminal Session Recorder v2.0.0"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="terminal-session-recorder",
    version="2.0.0",
    author="Md. Jony Hassain",
    author_email="jonyhossan110@gmail.com",
    description="Enterprise-grade Terminal Session Recorder for Pentesting & Security Audits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonyhossan110/terminal-session-recorder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.8",
    install_requires=[
        "reportlab>=4.0.0",
        "Pillow>=10.0.0",
        "aiofiles>=23.0.0",
        "aiosqlite>=0.19.0",
        "asyncio>=3.4.3",
        "psutil>=5.9.0",
        "rich>=13.0.0",
        "textual>=0.40.0",
        "asciinema>=2.3.0",
        "scapy>=2.5.0",
        "cryptography>=41.0.0",
        "pyyaml>=6.0",
        "jinja2>=3.1.0",
        "flask>=3.0.0",
        "flask-socketio>=5.3.0",
        "python-socketio>=5.10.0",
        "requests>=2.31.0",
        "pygments>=2.16.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "ocr": [
            "pytesseract>=0.3.10",
            "opencv-python>=4.8.0",
        ],
        "cloud": [
            "boto3>=1.28.0",  # AWS S3
            "google-cloud-storage>=2.10.0",  # Google Cloud
        ],
        "monitoring": [
            "mss>=9.0.1",
            "pyshark>=0.6",
        ],
    },
    entry_points={
        "console_scripts": [
            "tsr=tsr.cli:main",
            "tsr-server=tsr.server:main",
            "tsr-replay=tsr.replay:main",
        ],
    },
    include_package_data=True,
    package_data={
        "tsr": [
            "templates/*.html",
            "templates/*.jinja2",
            "static/*.css",
            "static/*.js",
            "plugins/*.py",
        ],
    },
)
