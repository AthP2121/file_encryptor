# Quick Start Guide

## Installation

### Option 1: Run from Source (Recommended for Linux/WSL)

1. **Install Python 3.8+** (if not already installed)

2. **Clone or download this repository**

3. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

4. **Activate virtual environment:**
   ```bash
   # Linux/Mac
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application:**
   ```bash
   python main.py
   ```

### Option 2: Build Windows Executable

1. **Follow steps 1-5 above**

2. **Build executable:**
   ```bash
   python build_exe.py
   ```

3. **Find executable in `dist/` folder:**
   - `dist/FileEncryptor.exe` (or `FileEncryptor` on Linux)
   - Can run without Python installed
   - Portable - copy to any Windows PC

## First Time Usage

### Using Password Mode (Easiest)

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Add files to encrypt:**
   - Click "Add Files" to select files
   - OR click "Add Folder" to encrypt an entire folder

3. **Choose Password mode** (default)

4. **Enter a strong password:**
   - Minimum 8 characters
   - Mix of letters, numbers, symbols
   - **IMPORTANT:** Remember this password!

5. **Click "Encrypt Selected"**
   - Encrypted files will have `.locked` extension
   - Original files remain (unless you checked "Delete original files")

6. **To decrypt:**
   - Select the `.locked` files
   - Enter the same password
   - Click "Decrypt Selected"

### Using Key File Mode (Most Secure)

1. **Generate a key file:**
   - Select "Key File" mode
   - Click "Generate Key"
   - Save the `.key` file in a safe location
   - **CRITICAL:** Backup this key file!

2. **Encrypt files:**
   - Add files to encrypt
   - Click "Encrypt Selected"

3. **To decrypt:**
   - Click "Load Key" and select your `.key` file
   - Select the `.locked` files
   - Click "Decrypt Selected"

## Common Tasks

### Encrypt a Single File

1. Click "Add Files"
2. Select your file
3. Choose password or key mode
4. Click "Encrypt Selected"

### Encrypt Multiple Files

1. Click "Add Files" and select multiple files (Ctrl+Click or Shift+Click)
2. OR use the Search feature to find files
3. Select files in the list (use "Select All" checkbox)
4. Click "Encrypt Selected"

### Encrypt a Folder

1. Click "Add Folder"
2. Select the folder
3. Choose password or key mode
4. Click "Encrypt Selected"
5. The entire folder will be compressed and encrypted as one `.locked` file

### Find and Decrypt All Encrypted Files

1. Use the Search section:
   - Browse to a directory
   - Check "Only .locked files"
   - Click "Search"
2. Select files from results
3. Enter password or load key
4. Click "Decrypt Selected"

## Testing

Run the test suite to verify everything works:

```bash
source venv/bin/activate  # Activate virtual environment
python test_encryption.py
```

Expected output:
```
============================================================
File Encryptor Test Suite
============================================================

Testing password encryption...
✓ Password encryption test PASSED

Testing key file encryption...
✓ Key file encryption test PASSED

Testing folder encryption...
✓ Folder encryption test PASSED

Testing file search...
✓ File search test PASSED

============================================================
Tests passed: 4/4
============================================================
```

## Command Line Examples

See `example_usage.py` for programmatic usage:

```bash
python example_usage.py
```

This demonstrates:
- Password encryption
- Key file encryption
- Folder encryption
- Batch operations
- File searching

## Troubleshooting

### "Module not found" error
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### GUI doesn't appear
- Make sure you're not running on a headless server
- On WSL2, you need an X server (like VcXsrv or WSLg)
- Try running on Windows directly

### "Permission denied" errors
- Check file permissions
- Make sure files aren't open in another program
- Run as administrator (Windows) if needed

### Can't decrypt files
- Verify you're using the correct password (case-sensitive!)
- Verify you're using the correct key file
- Make sure the `.locked` file isn't corrupted

## Security Tips

1. **Passwords:**
   - Use unique passwords for important files
   - Don't use dictionary words
   - Consider using a password manager

2. **Key Files:**
   - Store key files separate from encrypted files
   - Make encrypted backups of key files
   - Never email key files unencrypted

3. **Backups:**
   - Always test decryption before deleting originals
   - Keep backups of important files
   - Store backups in multiple locations

4. **General:**
   - Keep your computer secure (antivirus, updates)
   - Log out when away from computer
   - Use full-disk encryption on your device

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [example_usage.py](example_usage.py) for API examples
- Run [test_encryption.py](test_encryption.py) to verify installation

## Getting Help

If you encounter issues:
1. Check this guide and README.md
2. Run the test suite to verify installation
3. Check file permissions and paths
4. Make sure dependencies are installed correctly

---

**Remember:** Always test encryption/decryption before relying on it for important data!
