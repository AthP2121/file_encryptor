@echo off
REM File Encryptor - Windows Launcher
REM Double-click this file to run the application

echo ========================================
echo File Encryptor - Starting...
echo ========================================
echo.

REM Change to script directory
cd /d %~dp0

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Application failed to start
    echo ========================================
    pause
)
