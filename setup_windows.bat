@echo off
REM Windows Setup Script for TSR v2.0

echo ================================================
echo   Terminal Session Recorder v2.0.0
echo   Setup Script for Windows
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install TSR
echo.
echo Installing Terminal Session Recorder...
pip install -e .[all]

REM Initialize config
echo.
echo Initializing configuration...
tsr init

echo.
echo ================================================
echo   Installation Complete!
echo ================================================
echo.
echo Quick Start:
echo   .venv\Scripts\activate.bat
echo   tsr record --user-name "Your Name"
echo.
echo Documentation:
echo   tsr --help
echo   type README.md
echo.
pause
