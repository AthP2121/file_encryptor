# Windows Installation Guide

## Quick Install (For Users)

### Option A: Standalone Executable (Recommended)

**No Python Required!**

1. Download `FileEncryptor.exe` from the release
2. Double-click to run
3. That's it!

---

## Developer Install (Run from Source)

### Prerequisites

1. **Install Python 3.8 or higher**
   - Download: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Verify installation:
     ```cmd
     python --version
     ```

### Installation Steps

#### Step 1: Copy Project Files

**Option A - From WSL:**
```powershell
# In Windows Terminal (PowerShell)
xcopy "\\wsl.localhost\Ubuntu\home\ath\projects\file_encryptor" "%USERPROFILE%\file_encryptor" /E /I /H
cd %USERPROFILE%\file_encryptor
```

**Option B - Manual Copy:**
1. Open File Explorer
2. Navigate to: `\\wsl.localhost\Ubuntu\home\ath\projects\file_encryptor`
3. Copy entire folder to: `C:\Users\YourName\file_encryptor`

#### Step 2: Open Windows Terminal

1. Press `Win + X`
2. Select "Windows Terminal" or "PowerShell"
3. Navigate to project:
   ```powershell
   cd %USERPROFILE%\file_encryptor
   ```

#### Step 3: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it (PowerShell)
venv\Scripts\Activate.ps1
```

**If you get an error** about execution policies:
```powershell
# Run this first (as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
venv\Scripts\Activate.ps1
```

**Alternative for CMD** (not PowerShell):
```cmd
venv\Scripts\activate.bat
```

#### Step 4: Install Dependencies

```powershell
# Make sure venv is activated (you'll see "(venv)" in prompt)
pip install -r requirements.txt
```

Expected output:
```
Installing collected packages: cryptography, pyinstaller, ...
Successfully installed cryptography-46.0.5 pyinstaller-6.19.0 ...
```

#### Step 5: Run the Application

```powershell
python main.py
```

The GUI window should appear! 🎉

---

## Building Standalone Executable

### Build on Windows

```powershell
# Make sure venv is activated
venv\Scripts\Activate.ps1

# Build the executable
python build_exe.py
```

**Output:**
- Executable: `dist\FileEncryptor.exe`
- Size: ~30-50 MB
- Can run on any Windows PC without Python

### Distribute the Executable

Share `dist\FileEncryptor.exe` with anyone:
- No Python installation needed
- No dependencies needed
- Just double-click to run
- Portable (can run from USB drive)

---

## Testing

### Run Test Suite

```powershell
# With venv activated
python test_encryption.py
```

Expected output:
```
============================================================
File Encryptor Test Suite
============================================================

✓ Password encryption test PASSED
✓ Key file encryption test PASSED
✓ Folder encryption test PASSED
✓ File search test PASSED

Tests passed: 4/4
============================================================
```

### Run Examples

```powershell
python example_usage.py
```

---

## Troubleshooting

### Python not found

**Problem:** `'python' is not recognized as an internal or external command`

**Solution:**
1. Reinstall Python from https://www.python.org/downloads/
2. **Check "Add Python to PATH"** during installation
3. Restart Windows Terminal
4. Try: `py --version` instead of `python --version`

### Cannot activate virtual environment (PowerShell)

**Problem:** `cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pip install fails

**Problem:** `error: Microsoft Visual C++ 14.0 or greater is required`

**Solution:**
1. Install Visual C++ Build Tools
2. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
3. Install "Desktop development with C++"

**OR use pre-built wheels:**
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### GUI doesn't appear

**Problem:** Application runs but no window appears

**Solution:**
1. Check if Windows Defender is blocking it
2. Try running as Administrator
3. Check Task Manager for running Python processes
4. Verify tkinter is installed:
   ```powershell
   python -c "import tkinter"
   ```

### "Module not found" errors

**Problem:** `ModuleNotFoundError: No module named 'cryptography'`

**Solution:**
```powershell
# Make sure virtual environment is activated
venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Creating Desktop Shortcut

### For Python Version

1. Right-click on Desktop → New → Shortcut
2. Location:
   ```
   C:\Users\YourName\file_encryptor\venv\Scripts\python.exe C:\Users\YourName\file_encryptor\main.py
   ```
3. Name: "File Encryptor"

### For .exe Version

1. Copy `dist\FileEncryptor.exe` to desktop
2. Right-click → "Create shortcut"

---

## Uninstallation

### Remove Application

```powershell
# Delete project folder
Remove-Item -Recurse -Force "%USERPROFILE%\file_encryptor"
```

### Remove Python (optional)

1. Settings → Apps → Python → Uninstall

---

## Quick Reference

### Daily Usage

```powershell
# Open Windows Terminal
cd %USERPROFILE%\file_encryptor

# Activate environment
venv\Scripts\Activate.ps1

# Run application
python main.py
```

### One-Line Launcher

Create a batch file `run.bat`:
```batch
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
python main.py
pause
```

Double-click `run.bat` to launch!

---

## Need Help?

- Read: `README.md` for full documentation
- Read: `QUICKSTART.md` for usage guide
- Check: `test_encryption.py` to verify installation
- Run: `example_usage.py` to see examples

**Support:** Create an issue with:
- Windows version
- Python version (`python --version`)
- Error message (if any)
- Steps to reproduce
