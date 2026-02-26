# File Encryptor

A simple, secure file and folder encryption application for Windows with an easy-to-use GUI.

## Features

- **Strong Encryption**: AES-256 encryption using the industry-standard `cryptography` library
- **Dual Mode**: Encrypt with password or key file
- **Folder Support**: Automatically compresses and encrypts entire folders
- **Batch Operations**: Encrypt/decrypt multiple files at once
- **File Search**: Search directories for files to encrypt/decrypt
- **User-Friendly**: Simple GUI with progress tracking
- **Secure**: Uses PBKDF2 key derivation with 480,000 iterations

## Installation

### From Source

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

### Building Executable

To create a standalone Windows executable:

```bash
pyinstaller --onefile --windowed --name="FileEncryptor" main.py
```

The executable will be in the `dist` folder.

## Usage

### Basic Workflow

1. **Select Files/Folders**:
   - Click "Add Files" to select individual files
   - Click "Add Folder" to select an entire folder
   - Use the search feature to find files in a directory

2. **Choose Encryption Mode**:
   - **Password Mode**: Enter a password (minimum 8 characters recommended)
   - **Key File Mode**: Generate a new key file or load an existing one

3. **Encrypt**:
   - Select files from the list (checkboxes)
   - Click "Encrypt Selected"
   - Encrypted files will have a `.locked` extension

4. **Decrypt**:
   - Select `.locked` files
   - Enter the same password or load the same key file
   - Click "Decrypt Selected"
   - Original files will be restored

### Password Mode

**Pros:**
- Easy to use
- No need to manage key files
- Good for personal use

**Cons:**
- Security depends on password strength
- Must remember the password

**Tips:**
- Use a strong password (mix of letters, numbers, symbols)
- Minimum 8 characters, but longer is better
- Don't reuse passwords from other services

### Key File Mode

**Pros:**
- Maximum security (256-bit random key)
- No need to remember a password
- Good for automated processes

**Cons:**
- Must keep the key file safe
- Losing the key file means losing access to encrypted data

**Tips:**
- Store key files in a secure location
- Make backups of key files
- Never share key files over insecure channels

### Searching for Files

The search feature helps you find files to encrypt or decrypt:

1. Enter a directory path or browse
2. Set search pattern (use `*` for wildcards, e.g., `*.txt` for text files)
3. Enable "Recursive" to search subdirectories
4. Enable "Only .locked files" to find encrypted files
5. Click "Search"

### Batch Operations

- Select multiple files using checkboxes
- "Select All" checkbox in the file list
- All selected files will be processed with the same password/key
- Progress bar shows current operation status

## File Format

Encrypted files use the `.locked` extension and contain:

- **Header**: Metadata about the encryption method, original filename, and compression
- **Encrypted Data**: The actual file content, encrypted with AES-256

The file format is:
```
[MAGIC:4][VERSION:1][MODE:1][SALT:32][COMPRESSED:1][FILENAME_LEN:2][FILENAME:N][ENCRYPTED_DATA]
```

This allows the application to:
- Verify the file is a valid encrypted file
- Determine the encryption mode
- Restore the original filename and folder structure
- Detect if the file was a compressed folder

## Security Notes

### What This Application Does:

✅ Uses strong AES-256 encryption
✅ Implements PBKDF2 key derivation (480,000 iterations)
✅ Generates cryptographically secure random keys
✅ Protects file contents and folder structures
✅ Uses industry-standard cryptography library

### What This Application Does NOT Do:

❌ Hide metadata (file sizes, timestamps, encrypted file names are visible)
❌ Protect against malware on your computer
❌ Protect against keyloggers capturing your password
❌ Provide plausible deniability
❌ Securely delete original files (use specialized tools for that)

### Best Practices:

1. **Password Security**:
   - Use unique, strong passwords
   - Don't share passwords via email or messaging apps
   - Consider using a password manager

2. **Key File Security**:
   - Store key files on encrypted storage
   - Make offline backups
   - Never store key files in the same location as encrypted files

3. **Backup Strategy**:
   - Keep backups of important files before encrypting
   - Test decryption before deleting originals
   - Store encrypted backups in multiple locations

4. **Computer Security**:
   - Keep your OS and antivirus updated
   - Be cautious of malware and keyloggers
   - Use full-disk encryption for sensitive data

## Troubleshooting

### "Incorrect password or corrupted file"
- Double-check your password (case-sensitive)
- Ensure you're using the correct key file
- The file may be corrupted (try a backup)

### "Invalid key file"
- Ensure the key file hasn't been modified
- Key files must be the original generated file

### "File not found" or "Permission denied"
- Check if the file exists
- Ensure you have read/write permissions
- Close any programs that might have the file open

### Files won't decrypt
- Verify you're using the same password/key used for encryption
- Check that the `.locked` file isn't corrupted
- Ensure the file was encrypted with this application

## Development

### Project Structure

```
file_encryptor/
├── main.py              # Main application entry point and GUI
├── crypto_handler.py    # Encryption/decryption logic
├── file_manager.py      # File operations and batch processing
├── ui_components.py     # Reusable UI widgets
├── config.py            # Configuration constants
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Running Tests

Basic functionality test:

```python
# Test encryption with password
from crypto_handler import CryptoHandler
CryptoHandler.encrypt_file('test.txt', 'test.txt.locked', 0, password='testpass123')
CryptoHandler.decrypt_file('test.txt.locked', '.', password='testpass123')
```

### Contributing

Contributions are welcome! Please:
1. Test your changes thoroughly
2. Follow the existing code style
3. Add comments for complex logic
4. Update documentation as needed

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This software is provided for legitimate use only. Users are responsible for:
- Complying with local laws and regulations
- Keeping backups of important data
- Managing passwords and key files securely
- Understanding the limitations of the software

The authors are not responsible for data loss, misuse, or any damages resulting from the use of this software.

## Support

For issues, questions, or suggestions, please open an issue on the project repository.

---

**Remember**: Encryption is only as strong as your password/key management. Keep your passwords secure and your key files safe!
