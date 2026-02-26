# Build Directory Structure

This document explains the directory structure for building File Encryptor executables and installers.

## Directory Layout

```
file_encryptor/                     # Project root
├── build_exe.py                    # Build script (run from root)
├── build_installer.bat             # Installer build script (Windows)
├── installer_script.iss            # Inno Setup configuration
│
├── build/                          # Build artifacts (gitignored)
│   └── pyinstaller_temp/          # PyInstaller temporary files
│
├── dist/                           # Build output (gitignored)
│   └── FileEncryptor.exe          # Portable executable (~30-50 MB)
│
├── installer_output/               # Installer output (gitignored)
│   └── FileEncryptor_Setup_v1.0.0.exe  # Windows installer (~10-15 MB)
│
└── docs/                           # Documentation
    ├── CREATE_INSTALLER.md         # Installer creation guide
    └── ...
```

## Important Rules

### 1. Always Run from Project Root

All build scripts **must** be run from the project root directory:

```bash
# Correct
cd /path/to/file_encryptor
python build_exe.py

# Wrong
cd /path/to/file_encryptor/build
python build_exe.py
```

### 2. Directory Organization

- **Source files**: Root directory (`main.py`, `crypto_handler.py`, etc.)
- **Build scripts**: Root directory (`build_exe.py`, `build_installer.bat`, `installer_script.iss`)
- **Documentation**: `docs/` directory
- **Build artifacts**: Automatically created and gitignored:
  - `build/pyinstaller_temp/` - PyInstaller temporary files (auto-cleaned)
  - `dist/` - Executable output
  - `installer_output/` - Installer output

### 3. File Paths in Scripts

All scripts use **relative paths from project root**:

- `build_exe.py`: Uses `os.path.dirname(os.path.abspath(__file__))` to find root
- `installer_script.iss`: Uses relative paths like `dist\FileEncryptor.exe`, `docs\QUICKSTART.md`

## Building the Application

### Build Portable Executable

```bash
# From project root
python build_exe.py
```

**Output**: `dist/FileEncryptor.exe`

**What it does**:
1. Finds `main.py` in project root
2. Creates temporary files in `build/pyinstaller_temp/`
3. Outputs executable to `dist/FileEncryptor.exe`
4. Creates spec file in project root

### Build Windows Installer

```batch
REM From project root
build_installer.bat
```

**Output**: `installer_output/FileEncryptor_Setup_v1.0.0.exe`

**What it does**:
1. Runs `build_exe.py` to create executable
2. Uses Inno Setup to create installer
3. Packages files from:
   - `dist/FileEncryptor.exe`
   - `README.md`
   - `docs/QUICKSTART.md`
   - `LICENSE.txt`

## Troubleshooting

### "FileEncryptor.exe not found"

**Cause**: Trying to build installer before building executable, or running from wrong directory.

**Solution**:
```bash
# Ensure you're in project root
cd /path/to/file_encryptor
pwd  # Should show .../file_encryptor

# Build executable first
python build_exe.py

# Then build installer
build_installer.bat
```

### "QUICKSTART.md not found"

**Cause**: Installer script can't find documentation files.

**Solution**: Verify you're running from project root and `docs/QUICKSTART.md` exists.

### PyInstaller Creates Wrong Paths

**Cause**: Running build script from wrong directory.

**Solution**: Always run from project root. The script uses `__file__` to detect its location.

## Version History

### v1.0.0 (2024-02-26)

**Changes**:
- Reorganized build structure
- Removed duplicate build files from `build/` directory
- Fixed installer script to reference `docs/` for documentation
- Added `.gitignore` for build artifacts
- Updated all documentation to reflect correct structure

**Migration**:
If you have old build directories:
```bash
# Clean old build artifacts
rm -rf build/pyinstaller_temp/
rm -rf dist/
rm -rf installer_output/
rm -f *.spec

# Rebuild from clean state
python build_exe.py
```

## Best Practices

1. **Clean builds**: Delete `dist/` and `build/pyinstaller_temp/` before building for releases
2. **Version control**: Never commit build artifacts (they're gitignored)
3. **Testing**: Test executables on clean Windows systems without Python installed
4. **Documentation**: Keep `docs/` files up to date - they're included in installers

## Related Documentation

- `docs/CREATE_INSTALLER.md` - Detailed installer creation guide
- `docs/WINDOWS_INSTALL.md` - Windows installation instructions
- `README.md` - Main project documentation
- `CLAUDE.md` - AI development guide

---

**Remember**: Always build from the project root directory!
