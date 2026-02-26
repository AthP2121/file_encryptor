# Copilot Instructions for File Encryptor

## Build, Test, and Lint Commands

- **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
- **Run application:**
  ```bash
  python main.py
  ```
- **Build executable:**
  ```bash
  python build_exe.py
  # or
  pyinstaller --onefile --windowed --name="FileEncryptor" main.py
  ```
- **Build Windows installer:**
  ```bash
  build_installer.bat
  ```
- **Run all tests:**
  ```bash
  python test_encryption.py
  ```
- **Run a single test (example):**
  ```python
  from crypto_handler import CryptoHandler
  CryptoHandler.encrypt_file('test.txt', 'test.txt.locked', 0, password='testpass123')
  CryptoHandler.decrypt_file('test.txt.locked', '.', password='testpass123')
  ```

## High-Level Architecture

- **Modular MVC-style:**
  - `main.py`: Application entry point, GUI orchestration, threading
  - `crypto_handler.py`: Pure encryption/decryption logic (AES-256, PBKDF2, file format)
  - `file_manager.py`: File operations, compression, batch processing
  - `ui_components.py`: Reusable Tkinter/ttk widgets (no business logic)
  - `config.py`: All constants, messages, and configuration
- **Threading:** All encryption/decryption runs in threads; UI updates via callbacks; main thread never blocked
- **File Format:** Custom `.locked` files with header (magic, version, mode, salt, compression, filename) and encrypted data; backward compatibility required

## Key Conventions

- **Security Parameters:**
  - PBKDF2_ITERATIONS = 480000
  - SALT_SIZE = 32
  - KEY_SIZE = 32
  - Never reduce these values; only increase with version bump
- **Cryptography:**
  - Only use `cryptography` library (never pycrypto/pycryptodome/manual)
  - Unique random salt per file (password mode); salt in header
  - PBKDF2-HMAC-SHA256 for key derivation
- **Constants:** All magic numbers/strings in `config.py`, UPPER_SNAKE_CASE
- **UI:** Use ttk widgets; keep event handlers in `main.py` thin; no business logic in `ui_components.py`
- **Path Handling:** Use `pathlib.Path` for new code; always use absolute paths
- **Testing:** Any change to `crypto_handler.py` must pass all tests in `test_encryption.py` and decrypt old files
- **Build Artifacts:** Run build scripts from project root; build output in `dist/`, installer in `installer_output/`

## AI Assistant Guidance

- Follow module boundaries strictly (see CLAUDE.md for details)
- Never break file format compatibility without versioning and migration
- Do not bypass security checks or reduce security parameters
- For new features, check `config.py` and existing patterns first
- For architectural changes, ask for approval

---

This file summarizes build/test commands, architecture, and key conventions for Copilot and other AI assistants. Would you like to adjust anything or add coverage for areas I may have missed?