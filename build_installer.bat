@echo off
REM Build script for creating the Windows installer
REM This script builds both the .exe and the installer

echo ========================================
echo File Encryptor - Installer Builder
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [2/4] Building executable with PyInstaller...
echo This may take a few minutes...
python build_exe.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)
echo Executable built successfully: dist\FileEncryptor.exe
echo.

REM Check if Inno Setup is installed
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo.
    echo ========================================
    echo Inno Setup Not Found
    echo ========================================
    echo.
    echo To create an installer, you need to install Inno Setup:
    echo.
    echo 1. Download from: https://jrsoftware.org/isdl.php
    echo 2. Install Inno Setup 6
    echo 3. Run this script again
    echo.
    echo For now, you can use the portable .exe:
    echo   dist\FileEncryptor.exe
    echo.
    pause
    exit /b 0
)

echo [3/4] Creating installer with Inno Setup...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss
if errorlevel 1 (
    echo ERROR: Failed to create installer
    pause
    exit /b 1
)
echo.

echo [4/4] Cleaning up...
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Portable .exe:
echo   dist\FileEncryptor.exe
echo.
echo Installer:
echo   installer_output\FileEncryptor_Setup_v1.0.0.exe
echo.
echo You can distribute either file to users.
echo The installer provides a professional installation experience.
echo.
pause
