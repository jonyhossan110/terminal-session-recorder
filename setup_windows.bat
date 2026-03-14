@echo off
REM Windows Setup Script for Web Security Tool

echo 🚀 Setting up Web Security Tool on Windows

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% detected

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

echo ✅ Setup complete!
echo.
echo 🎯 Usage:
echo   .venv\Scripts\activate.bat
echo   python main.py --record-session --user-name YOUR_NAME
echo   python main.py https://example.com -o report.json
echo.
echo 💡 Add to PowerShell profile for easy access:
echo   Add-Content $PROFILE "function Record-Shell { python 'C:\path\to\main.py' --record-session --user-name YOUR_NAME }"
echo   Then run: Record-Shell

pause