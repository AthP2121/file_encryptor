@echo off
REM File Encryptor - Windows Setup Script
REM Run this once to set up the application

echo ========================================
echo File Encryptor - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/4] Python found:
python --version
echo.

echo [2/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

echo [4/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Double-click "run.bat"
echo   OR
echo   2. Open Windows Terminal and run:
echo      venv\Scripts\activate
echo      python main.py
echo.
echo To build standalone .exe:
echo   1. Run: venv\Scripts\activate
echo   2. Run: python build_exe.py
echo   3. Find exe in: dist\FileEncryptor.exe
echo.
pause
