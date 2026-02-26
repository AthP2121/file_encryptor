# How to Create a Windows Installer

This guide shows you how to create a professional installer for File Encryptor, just like commercial software.

## What You'll Create

**Installer Features:**
- ✅ Professional installation wizard
- ✅ Installs to Program Files
- ✅ Creates Start Menu shortcuts
- ✅ Creates Desktop shortcut (optional)
- ✅ Adds to Windows "Programs & Features" for uninstall
- ✅ Shows license agreement
- ✅ Can be distributed as a single .exe file
- ✅ ~10-15 MB installer size

## Method 1: Automated Build (Easiest)

### Prerequisites

1. **Install Inno Setup** (free):
   - Download: https://jrsoftware.org/isdl.php
   - Install to default location: `C:\Program Files (x86)\Inno Setup 6\`

2. **Have the project set up** (Python + dependencies installed)

### Build the Installer

```batch
REM Just run this batch file!
build_installer.bat
```

This will:
1. Build the portable .exe with PyInstaller
2. Create the installer with Inno Setup
3. Output both files

**Results:**
- Portable: `dist\FileEncryptor.exe` (~30-50 MB)
- Installer: `installer_output\FileEncryptor_Setup_v1.0.0.exe` (~10-15 MB)

---

## Method 2: Manual Build (Step by Step)

### Step 1: Install Inno Setup

1. Download Inno Setup 6: https://jrsoftware.org/isdl.php
2. Run the installer
3. Install to default location

### Step 2: Build the Executable

```powershell
# In Windows Terminal
cd %USERPROFILE%\file_encryptor
venv\Scripts\Activate.ps1
python build_exe.py
```

**Output:** `dist\FileEncryptor.exe`

### Step 3: Customize the Installer Script (Optional)

Edit `installer_script.iss`:

```ini
#define MyAppName "File Encryptor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Name"        ; ← Change this
#define MyAppURL "https://yourwebsite.com" ; ← Change this
```

### Step 4: Compile the Installer

**Option A - GUI:**
1. Open Inno Setup Compiler
2. File → Open: `installer_script.iss`
3. Build → Compile
4. Wait ~30 seconds
5. Done!

**Option B - Command Line:**
```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss
```

**Output:** `installer_output\FileEncryptor_Setup_v1.0.0.exe`

---

## Testing the Installer

### Test Installation

1. **Run the installer:**
   ```
   installer_output\FileEncryptor_Setup_v1.0.0.exe
   ```

2. **Follow the wizard:**
   - Accept license
   - Choose installation location
   - Select shortcuts
   - Install

3. **Verify installation:**
   - Check Start Menu for "File Encryptor"
   - Check Desktop for shortcut (if selected)
   - Run the application

### Test Uninstallation

1. **Uninstall via:**
   - Start Menu → File Encryptor → Uninstall
   - OR Settings → Apps → File Encryptor → Uninstall

2. **Verify:**
   - Application removed from Program Files
   - Shortcuts removed
   - Entry removed from Programs list

---

## Customizing the Installer

### Add Custom Icon

1. Create or download an `.ico` file (256x256 recommended)
2. Save as `icon.ico` in project folder
3. Update `installer_script.iss`:
   ```ini
   SetupIconFile=icon.ico
   ```

### Change Installation Location

In `installer_script.iss`:
```ini
; Install to user folder instead of Program Files
DefaultDirName={autopf}\{#MyAppName}      ; Current (Program Files)
DefaultDirName={localappdata}\{#MyAppName} ; User folder
DefaultDirName=C:\FileEncryptor            ; Fixed location
```

### Add More Files

In `installer_script.iss` under `[Files]`:
```ini
; Add example files
Source: "examples\*"; DestDir: "{app}\examples"; Flags: ignoreversion recursesubdirs

; Add configuration file
Source: "config.ini"; DestDir: "{app}"; Flags: ignoreversion
```

### Create Multiple Shortcuts

In `installer_script.iss` under `[Icons]`:
```ini
; Add "Help" shortcut to Start Menu
Name: "{group}\Help"; Filename: "{app}\README.md"

; Add "Examples" folder shortcut
Name: "{group}\Examples"; Filename: "{app}\examples"
```

### Change Installer Appearance

```ini
; Use classic wizard style
WizardStyle=classic

; Or modern style (default)
WizardStyle=modern

; Custom wizard images (optional)
WizardImageFile=wizard_image.bmp
WizardSmallImageFile=wizard_small.bmp
```

---

## Distribution

### Single File Distribution

**The installer is ONE file:**
```
FileEncryptor_Setup_v1.0.0.exe  (~10-15 MB)
```

**Distribute via:**
- Email attachment
- File sharing (Google Drive, Dropbox, etc.)
- Website download
- USB drive
- GitHub Releases

### Professional Distribution

1. **Create a website landing page**
   - Download button
   - Features list
   - Screenshots
   - Documentation link

2. **Use GitHub Releases:**
   ```bash
   # Tag a release
   git tag v1.0.0
   git push origin v1.0.0

   # Upload installer to GitHub Releases
   # Users download: FileEncryptor_Setup_v1.0.0.exe
   ```

3. **Code Signing (Optional, Advanced):**
   - Get a code signing certificate (~$100-300/year)
   - Sign the installer to remove "Unknown Publisher" warning
   - Increases trust for users

---

## Advanced: Auto-Update System

Want to add automatic updates? Here's the concept:

### Version Check File

Host a `version.json` on your website:
```json
{
  "version": "1.0.1",
  "download_url": "https://yoursite.com/FileEncryptor_Setup_v1.0.1.exe",
  "changelog": "Bug fixes and improvements"
}
```

### Add Update Checker to Python App

```python
# In main.py, add this function
import requests
import json

def check_for_updates():
    try:
        response = requests.get('https://yoursite.com/version.json')
        data = response.json()

        if data['version'] > APP_VERSION:
            # Show update dialog
            messagebox.showinfo(
                'Update Available',
                f"Version {data['version']} is available!\n\n"
                f"Changes: {data['changelog']}\n\n"
                f"Download from: {data['download_url']}"
            )
    except:
        pass  # Silently fail if no internet
```

---

## Installer Script Reference

### Key Sections Explained

```ini
[Setup]
; App metadata and installation settings

[Languages]
; Supported languages (can add more)

[Tasks]
; Optional tasks users can choose (shortcuts, etc.)

[Files]
; Files to install and where they go

[Icons]
; Shortcuts to create (Start Menu, Desktop, etc.)

[Run]
; Programs to run after installation

[Code]
; Pascal script for advanced customization
```

### Common Customizations

**Require admin rights:**
```ini
PrivilegesRequired=admin
```

**Install for all users:**
```ini
PrivilegesRequired=admin
DefaultDirName={commonpf}\{#MyAppName}
```

**Silent installation option:**
```ini
; Users can run: setup.exe /SILENT
; Or: setup.exe /VERYSILENT
```

---

## Troubleshooting

### "FileEncryptor.exe not found"

**Problem:** Installer script can't find the executable

**Solution:**
1. Make sure you built the .exe first: `python build_exe.py`
2. Check that `dist\FileEncryptor.exe` exists
3. Verify path in `installer_script.iss` matches

### "Cannot open icon file"

**Problem:** Icon file missing

**Solution:**
1. Comment out the icon line in `installer_script.iss`:
   ```ini
   ;SetupIconFile=icon.ico
   ```
2. Or create/download an icon file

### "Inno Setup not found"

**Problem:** Build script can't find Inno Setup

**Solution:**
1. Check installation path:
   ```
   C:\Program Files (x86)\Inno Setup 6\ISCC.exe
   ```
2. Update path in `build_installer.bat` if different

### Installer too large

**Problem:** Installer is 50+ MB

**Solution:**
1. The .exe is already compressed by PyInstaller
2. Inno Setup compresses further
3. To reduce size further:
   - Exclude unnecessary modules in `build_exe.py`
   - Use UPX compression (advanced)

---

## Comparison: Portable vs Installer

| Feature | Portable .exe | Installer |
|---------|---------------|-----------|
| File size | 30-50 MB | 10-15 MB |
| Installation | None | ~1 minute |
| Shortcuts | Manual | Automatic |
| Uninstaller | None | Built-in |
| Professional | Less | More |
| Distribution | Single file | Single file |
| User experience | Simple | Polished |

**Recommendation:** Provide both!
- **Portable** for quick testing and USB drives
- **Installer** for permanent installations

---

## Next Steps

1. **Build your first installer:**
   ```batch
   build_installer.bat
   ```

2. **Test it thoroughly:**
   - Install on a clean Windows VM
   - Test all features
   - Test uninstallation

3. **Customize:**
   - Add your name/company
   - Add custom icon
   - Adjust shortcuts

4. **Distribute:**
   - Upload to GitHub Releases
   - Share on your website
   - Send to users

---

## Resources

- **Inno Setup Documentation:** https://jrsoftware.org/ishelp/
- **Inno Setup Examples:** https://jrsoftware.org/isinfo.php
- **PyInstaller Docs:** https://pyinstaller.org/en/stable/
- **Code Signing Info:** https://www.ssl.com/how-to/code-signing-certificates/

---

**You now have everything to create professional Windows installers!** 🎉

The installer will make your application look and feel like commercial software, giving users confidence in installing and using it.
