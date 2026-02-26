# CLAUDE.md - AI Development Guide

This file provides guidance for AI assistants working on this codebase.

## Project Overview

**File Encryptor** - A secure file encryption application with AES-256 encryption, dual authentication modes (password/key file), and a full-featured Tkinter GUI.

- **Language**: Python 3.8+
- **Primary Use**: Personal/professional file security
- **Status**: Production-ready (v1.0.0)
- **Architecture**: Modular MVC-style with separated concerns

## Core Architecture

### Module Responsibilities

```
crypto_handler.py   → Pure encryption/decryption logic (no I/O besides file read/write)
file_manager.py     → File operations, compression, batch processing
ui_components.py    → Reusable GUI widgets (no business logic)
main.py             → Application orchestration, event handling, threading
config.py           → ALL constants, messages, and configuration
```

**Critical Rule**: Maintain this separation. Don't mix crypto logic into UI code or put UI code in crypto handlers.

### Key Design Patterns

1. **Threading for Long Operations**
   - All encryption/decryption operations run in threads (see `main.py` lines 200-220)
   - UI updates via callbacks passed to `BatchProcessor`
   - Never block the main thread

2. **Static Methods for Crypto**
   - `CryptoHandler` uses static methods (stateless design)
   - Each operation is self-contained
   - Easier to test and reason about

3. **Path Handling**
   - Use `pathlib.Path` for new code (legacy uses `os.path`)
   - Always use absolute paths for file operations

## Security Rules (NON-NEGOTIABLE)

### Critical Constants (DO NOT MODIFY)

```python
PBKDF2_ITERATIONS = 480000  # OWASP 2023+ recommendation
SALT_SIZE = 32              # Cryptographic standard
KEY_SIZE = 32               # AES-256 requirement
```

**Never reduce these values.** Increasing is acceptable with version bump.

### Cryptography Requirements

1. **Always use `cryptography` library**
   - Never use `pycrypto`, `pycryptodome`, or manual implementations
   - Never implement custom crypto algorithms

2. **Salt Management**
   - Every encrypted file gets unique random salt
   - Stored in file header (password mode only)
   - Never reuse salts

3. **Key Derivation**
   - PBKDF2-HMAC-SHA256 only
   - Salt must be cryptographically random (`os.urandom()`)

4. **File Format Compatibility**
   - Maintain backward compatibility with v1 `.locked` files
   - If format changes, increment `FILE_VERSION` and add migration

### Testing Requirements for Security Changes

Any change to `crypto_handler.py` **must**:
1. Pass all tests in `test_encryption.py`
2. Successfully decrypt files created before the change
3. Be reviewed for security implications

Run: `python test_encryption.py` before committing crypto changes.

## Code Style and Conventions

### General Style
- Follow PEP 8
- Use descriptive variable names (no single-letter except loop counters)
- Type hints preferred for public methods
- Docstrings for all classes and public methods (Google style)

### Error Handling
```python
# Good - Specific exceptions with clear messages
raise ValueError("Password required for password mode")

# Bad - Generic exceptions
raise Exception("Error")
```

### Constants
- All magic numbers/strings go in `config.py`
- Use UPPER_SNAKE_CASE for constants
- Group related constants together

### UI Code
- Keep event handlers in `main.py` thin (delegate to other modules)
- No business logic in `ui_components.py`
- Use ttk widgets (not tk) for consistency

## File Structure Standards

### Custom .locked File Format

```
[Header: 4+1+1+32+1+2+N bytes]
├─ Magic bytes (4): b"FLCK"
├─ Version (1): FILE_VERSION
├─ Mode (1): MODE_PASSWORD or MODE_KEYFILE
├─ Salt (32): Random salt (password mode) or zeros (key mode)
├─ Compressed (1): 0 or 1
├─ Filename length (2): Big-endian unsigned short
└─ Filename (N): UTF-8 encoded

[Body: Remaining bytes]
└─ Encrypted data: Fernet-encrypted file content
```

**Never break this format** without versioning properly.

## Development Guidelines

### Before Adding Features

1. **Check existing patterns** - Search codebase for similar functionality
2. **Read config.py first** - See if constants/messages already exist
3. **Consider security impact** - Any crypto changes need extra scrutiny
4. **Think about threading** - Will it block the UI?

### When to Create New Modules

Only create new `.py` files for:
- Completely new major functionality (e.g., cloud sync, CLI)
- When existing files exceed ~500 lines
- When functionality doesn't fit existing module responsibilities

**Don't create** utility modules for 1-2 helper functions.

### Testing Strategy

- Unit tests for crypto operations (critical)
- Integration tests for file operations
- Manual GUI testing (no automated UI tests yet)

**Minimum test coverage**: All functions in `crypto_handler.py` and `file_manager.py`

## Future Development Priorities

See `PROJECT_SUMMARY.md` "Future Enhancement Opportunities" for full list.

### High Priority (Approved for Development)
1. **Password strength meter** - Visual indicator in password entry
2. **Secure file deletion** - Overwrite original files before deletion
3. **Drag-and-drop support** - Use `tkinterdnd2` library

### Medium Priority (Consider First)
4. File integrity verification (HMAC)
5. Compression level options
6. Settings persistence (save last mode/directory)

### Requires Architectural Discussion
- Command-line interface (affects structure)
- Plugin system (major refactor)
- Database for file tracking (new dependency)

## What NOT to Do

### Never Do These Without Asking

1. **Don't reduce security parameters** (iterations, key sizes, salt sizes)
2. **Don't bypass security checks** ("temporary" workarounds become permanent)
3. **Don't add heavyweight dependencies** (keep it lightweight)
4. **Don't break file format compatibility** (users have encrypted files)
5. **Don't implement custom crypto** (ever)

### Avoid Over-Engineering

- Don't add abstractions for single use cases
- Don't add configuration for things that never change
- Don't create "future-proof" systems for speculative features
- Keep it simple - this is a focused tool, not a framework

### UI/UX Principles

- Keep interface simple and uncluttered
- One-click operations where possible
- Clear error messages with actionable advice
- Progress feedback for operations >1 second

## Common Tasks

### Adding a New UI Widget
1. Create reusable component in `ui_components.py`
2. Use ttk for styling consistency
3. Accept callbacks for actions (don't reference `main.py`)
4. Test with both password and key file modes

### Adding a New Encryption Feature
1. Implement in `crypto_handler.py` as static method
2. Add constants to `config.py`
3. Write test in `test_encryption.py`
4. Verify backward compatibility
5. Update `PROJECT_SUMMARY.md` if significant

### Adding a File Operation
1. Implement in `file_manager.py` or `BatchProcessor`
2. Use pathlib for paths if possible
3. Handle errors gracefully (files in use, permissions, etc.)
4. Add progress callbacks if operation can be slow

## Dependencies

Current minimal dependencies:
- `cryptography==46.0.5` - Encryption (required)
- `pyinstaller==6.19.0` - Executable building (dev only)

### Adding New Dependencies

Ask these questions first:
1. Is it really necessary, or can we use stdlib?
2. Is it actively maintained?
3. Does it have security implications?
4. What's the file size impact on executables?

Prefer stdlib over external packages when possible.

## Building and Distribution

### Creating Executable
```bash
python build_exe.py  # Uses PyInstaller with configured options
```

### Before Release
1. Run all tests: `python test_encryption.py`
2. Test on clean system (no dev dependencies)
3. Verify executable works without Python installed
4. Check file size (<50MB target)
5. Update version in `config.py` and `PROJECT_SUMMARY.md`

## Questions or Unclear Requirements?

When uncertain about:
- **Security decisions** → Ask before implementing
- **Architectural changes** → Discuss before coding
- **Breaking changes** → Always get approval
- **New dependencies** → Justify the need

For minor bug fixes and UI tweaks, proceed with confidence.

## Additional Resources

- **README.md** - User documentation
- **QUICKSTART.md** - Getting started guide
- **PROJECT_SUMMARY.md** - Complete project overview
- **example_usage.py** - Programmatic usage examples
- **test_encryption.py** - Test suite and examples

---

**Remember**: This is security software. When in doubt, err on the side of caution. A simple, secure implementation beats a complex, fragile one.
